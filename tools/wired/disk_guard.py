#!/usr/bin/env python3
"""disk_guard.py - artifact-lifecycle disk/quota guard for Mochiichao production.

Implements the standard artifact-lifecycle pattern used by CI artifact
stores, DVC-style ML artifact management, and Kaggle dataset publishing:

  1. PREFLIGHT HEADROOM GATE - before any pull/download/collect, expected
     bytes are checked against headroom measured TWO ways: filesystem free
     space (shutil.disk_usage) AND a canary write probe in the target
     directory. A per-user/project quota can sit below the filesystem
     level, so `df` alone cannot be trusted: an EDQUOT/ENOSPC from the
     probe means quota-blocked even when df shows space. Fail = exit 3
     with a plain numbers report; a pull that cannot finish never starts.
  2. VERIFY-THEN-EVICT - a local product file is a transit copy. It is
     sha256-verified against its manifest/hash, published to its durable
     home (a Kaggle dataset), the durable home is confirmed, and only then
     is the local copy evicted. Any failed step leaves the file in place.
  3. ORPHAN/PARTIAL REAPER - conservative classes only (see `reap`).

Stdlib only. The Kaggle CLI is invoked via subprocess for dataset ops
(resolution order: $DISK_GUARD_KAGGLE_BIN, then `kaggle` on PATH, then
~/workspace/kaggle-cli-venv/bin/kaggle).

Every subcommand prints human-readable lines and, as the LAST line of
stdout, a JSON summary object.

Exit codes: 0 ok - 2 usage/other error - 3 headroom/quota blocked -
4 hash mismatch (refused) - 5 publish/confirm failed (refused).
"""

import argparse
import errno
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

EDQUOT = getattr(errno, "EDQUOT", 122)
QUOTA_ERRNOS = {EDQUOT, errno.ENOSPC}

PROBE_NAME = ".disk-guard-probe"
DEFAULT_PROBE_BYTES = 8 * 1024 * 1024
MIN_REAP_BYTES = 1 * 1024 * 1024          # the reaper never touches < 1 MB
DEFAULT_PARTIAL_MAX_AGE_S = 2 * 3600      # reap class (a): markers older than this
INFLIGHT_MTIME_S = 120                    # sibling written within this = in-flight

# A directory counts as a kernel-output pull directory when any component of
# its name matches this pattern (run-output*, foundry-output*, kernel-output,
# *-pull*, lora-products, ...).
PULL_DIR_RE = re.compile(r"(output|pull|lora-products)", re.IGNORECASE)

DEFAULT_KAGGLE_VENV = Path.home() / "workspace" / "kaggle-cli-venv" / "bin" / "kaggle"


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

def human(n):
    n = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024.0:
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} PB"


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            data = f.read(chunk)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def emit(summary, lines):
    for line in lines:
        print(line)
    print(json.dumps(summary, indent=None, sort_keys=True))
    return summary.get("exit_code", 0)


# --------------------------------------------------------------------------
# 1. headroom: df free space + canary write probe
# --------------------------------------------------------------------------

def _probe_write_file(probe_path, size):
    """Write `size` bytes to probe_path, fsync, leave the file in place.

    Isolated as its own function so tests can monkeypatch it to simulate a
    quota failure on a filesystem that still shows free space.
    """
    chunk = b"\0" * (1024 * 1024)
    remaining = size
    fd = os.open(probe_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        while remaining > 0:
            n = min(remaining, len(chunk))
            os.write(fd, chunk[:n])
            remaining -= n
        os.fsync(fd)
    finally:
        os.close(fd)


def run_canary(directory, probe_bytes=DEFAULT_PROBE_BYTES):
    """Write+fsync+delete a probe file in `directory`.

    Returns a dict: {ok, probe_bytes, path, errno, error}. ok=False with a
    quota errno means the directory is quota-blocked regardless of df.
    """
    directory = Path(directory)
    probe_path = directory / PROBE_NAME
    result = {"ok": False, "probe_bytes": probe_bytes, "path": str(directory),
              "errno": None, "error": None}
    try:
        _probe_write_file(probe_path, probe_bytes)
        result["ok"] = True
    except OSError as e:
        result["errno"] = e.errno
        result["error"] = f"{type(e).__name__}: {e}"
    finally:
        try:
            if probe_path.exists():
                probe_path.unlink()
        except OSError:
            pass
    return result


def headroom_report(path, probe_bytes=DEFAULT_PROBE_BYTES):
    p = Path(path)
    target = p if p.is_dir() else p.parent
    usage = shutil.disk_usage(target)
    canary = run_canary(target, probe_bytes)
    quota_blocked = (not canary["ok"]) and (canary["errno"] in QUOTA_ERRNOS)
    return {
        "path": str(p),
        "probe_target": str(target),
        "df_total_bytes": usage.total,
        "df_used_bytes": usage.used,
        "df_free_bytes": usage.free,
        "canary": canary,
        "quota_blocked": quota_blocked,
        "writable": canary["ok"],
    }


def cmd_check(args):
    rep = headroom_report(args.path, args.probe_bytes)
    blocked = rep["quota_blocked"] or not rep["canary"]["ok"]
    lines = [
        f"check {rep['path']}",
        f"  df free: {human(rep['df_free_bytes'])} ({rep['df_free_bytes']} bytes) "
        f"of {human(rep['df_total_bytes'])}",
        f"  canary probe: {'OK' if rep['canary']['ok'] else 'FAILED'} "
        f"({human(rep['canary']['probe_bytes'])} write+fsync in {rep['probe_target']})",
    ]
    if rep["canary"]["error"]:
        lines.append(f"  canary error: {rep['canary']['error']} (errno {rep['canary']['errno']})")
    if rep["quota_blocked"]:
        lines.append("  VERDICT: QUOTA-BLOCKED - df shows space but the canary "
                     "write hit a quota/space error. df alone cannot be trusted here.")
    elif not rep["canary"]["ok"]:
        lines.append("  VERDICT: NOT WRITABLE - canary probe failed (see error above).")
    else:
        lines.append("  VERDICT: headroom OK by both measures (df + canary).")
    rep["exit_code"] = 3 if blocked else 0
    return emit(rep, lines)


def cmd_preflight(args):
    rep = headroom_report(args.path, args.probe_bytes)
    expect = args.expect_bytes
    shortfall = max(0, expect - rep["df_free_bytes"])
    df_ok = rep["df_free_bytes"] >= expect
    ok = df_ok and rep["canary"]["ok"]
    lines = [
        f"preflight for {human(expect)} ({expect} bytes) into {rep['path']}",
        f"  df free:      {human(rep['df_free_bytes'])} ({rep['df_free_bytes']} bytes) "
        f"-> {'enough' if df_ok else 'NOT ENOUGH'}",
    ]
    if shortfall:
        lines.append(f"  shortfall:    {human(shortfall)} ({shortfall} bytes)")
    lines.append(f"  canary probe: {'OK' if rep['canary']['ok'] else 'FAILED'} "
                 f"({human(rep['canary']['probe_bytes'])})")
    if rep["canary"]["error"]:
        lines.append(f"  canary error: {rep['canary']['error']} (errno {rep['canary']['errno']})")
    if rep["quota_blocked"]:
        lines.append("  note: quota-blocked despite df space - a per-user/project "
                     "quota sits below the filesystem level.")
    lines.append("  VERDICT: " + ("GO - headroom confirmed both ways."
                                  if ok else
                                  "NO-GO (exit 3) - do not start a pull that cannot finish."))
    rep.update({"expect_bytes": expect, "shortfall_bytes": shortfall,
                "df_ok": df_ok, "go": ok, "exit_code": 0 if ok else 3})
    return emit(rep, lines)


# --------------------------------------------------------------------------
# path classification shared by inventory + reap
# --------------------------------------------------------------------------

def _is_held(path, dataset_source_dirs):
    """Protected classes the reaper never touches (inventory class 'held').

    - anything under a `terabox-upload` tree (a paused chain's transit
      masters / resume source - report-only, named class),
    - anything inside a dataset source folder (a directory holding
      dataset-metadata.json),
    - source trees / repo checkouts are protected implicitly: they match
      none of the reap classes, which only fire inside pull dirs, on
      *.kaggle-partial units, or on manifest-matched pull-dir files.
    """
    if "terabox-upload" in path.parts:
        return True
    for d in dataset_source_dirs:
        if path == d or d in path.parents:
            return True
    return False


def _in_pull_dir(path, root=None):
    """True when the path sits inside a pull dir BELOW the scan root.

    Only components relative to the root count - the root's own name (or
    anything above it) must never make every scanned file a 'pull file'.
    """
    parts = path.parts
    if root is not None:
        try:
            parts = path.relative_to(root).parts
        except ValueError:
            pass
    return any(PULL_DIR_RE.search(part) for part in parts)


def _walk_roots(roots):
    """Walk roots once. Returns (files, dataset_source_dirs, pull_dirs).

    files: list of Path. dataset_source_dirs: dirs holding
    dataset-metadata.json. pull_dirs: shallowest dirs matching PULL_DIR_RE.
    """
    files = []
    dataset_source_dirs = set()
    pull_dirs = []
    for root in roots:
        root = Path(root)
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            d = Path(dirpath)
            if "dataset-metadata.json" in filenames:
                dataset_source_dirs.add(d)
            if d != root and PULL_DIR_RE.search(d.name):
                pull_dirs.append(d)
            for name in filenames:
                files.append((root, d / name))
    # keep only shallowest pull dirs (drop ones nested inside another)
    shallow = []
    for d in pull_dirs:
        if not any(other != d and other in d.parents for other in pull_dirs):
            shallow.append(d)
    return files, dataset_source_dirs, shallow


def load_manifest_entries(manifest_path):
    """Load staged-artifact records from a manifest.

    Accepted shapes:
      - {"<name-or-relpath>": {"bytes": N, "sha256": H}, ...}   (COLLECTED format)
      - {"files": { ...same... }} or {"files": [ {...}, ... ]}
      - [ {"name"/"path"/"file": X, "bytes"/"size": N, "sha256": H}, ... ]
    Returns a list of {"name", "bytes", "sha256", "dataset"} (sha256
    lowercased; "dataset" is the recorded durable home, or None - entries
    written by publish-evict carry one, bare collection manifests do not).
    """
    if not manifest_path:
        return []
    data = json.loads(Path(manifest_path).read_text())
    entries = []

    def add(name, rec):
        if not isinstance(rec, dict):
            return
        size = rec.get("bytes", rec.get("size"))
        sha = rec.get("sha256", rec.get("sha"))
        if size is not None and sha:
            entries.append({"name": str(name), "bytes": int(size),
                            "sha256": str(sha).lower(),
                            "dataset": rec.get("dataset")})

    if isinstance(data, dict) and isinstance(data.get("files"), (dict, list)):
        data = data["files"]
    if isinstance(data, dict):
        for k, v in data.items():
            add(k, v)
    elif isinstance(data, list):
        for rec in data:
            if isinstance(rec, dict):
                add(rec.get("name") or rec.get("path") or rec.get("file"), rec)
    return entries


# --------------------------------------------------------------------------
# inventory
# --------------------------------------------------------------------------

def classify_files(roots, manifest_entries=()):
    files, dataset_source_dirs, _pull_dirs = _walk_roots(roots)
    durable = [e for e in manifest_entries if e.get("dataset")]
    staged = {(e["bytes"], e["sha256"]) for e in durable}
    staged_sizes = {e["bytes"] for e in durable}
    classes = {}
    per_file = []

    def bump(cls, size):
        c = classes.setdefault(cls, {"bytes": 0, "files": 0})
        c["bytes"] += size
        c["files"] += 1

    for root, f in files:
        try:
            size = f.stat().st_size
        except OSError:
            continue
        if _is_held(f, dataset_source_dirs):
            cls = "held"
        elif f.name.endswith(".kaggle-partial"):
            cls = "junk"
        elif (f.with_name(f.name + ".kaggle-partial")).exists():
            cls = "junk"          # partial data file of an unfinished pull
        elif _in_pull_dir(f, root):
            if size >= MIN_REAP_BYTES and size in staged_sizes \
                    and (size, sha256_file(f)) in staged:
                cls = "junk"      # staged duplicate inside a pull dir
            elif size >= MIN_REAP_BYTES:
                cls = "product"   # complete transit product awaiting publish-evict
            else:
                cls = "transit"   # small fry riding along in a pull dir
        else:
            cls = "unknown"
        bump(cls, size)
        per_file.append({"path": str(f), "bytes": size, "class": cls})
    per_file.sort(key=lambda r: -r["bytes"])
    return classes, per_file


def cmd_inventory(args):
    entries = load_manifest_entries(args.manifest)
    classes, per_file = classify_files(args.roots, entries)
    total = sum(c["bytes"] for c in classes.values())
    lines = [f"inventory of {len(args.roots)} root(s): {human(total)} total"]
    for cls in ("product", "transit", "junk", "held", "unknown"):
        if cls in classes:
            c = classes[cls]
            lines.append(f"  {cls:8s} {human(c['bytes']):>10s}  ({c['files']} files)")
    lines.append("  largest files:")
    for r in per_file[:10]:
        lines.append(f"    [{r['class']}] {human(r['bytes']):>10s}  {r['path']}")
    summary = {"roots": [str(r) for r in args.roots], "total_bytes": total,
               "classes": classes, "largest_files": per_file[:25], "exit_code": 0}
    return emit(summary, lines)


# --------------------------------------------------------------------------
# 3. reaper - conservative classes only
# --------------------------------------------------------------------------

def _open_fd_targets():
    """Best-effort set of paths currently open by any process (Linux /proc).

    Part of the documented in-flight heuristic for reap class (a): a partial
    whose file is open by a live process is never a candidate. Permission
    errors are ignored; absence of /proc just yields an empty set and the
    mtime clauses still apply.
    """
    targets = set()
    proc = Path("/proc")
    if not proc.exists():
        return targets
    for fd_dir in proc.glob("[0-9]*/fd"):
        try:
            for fd in fd_dir.iterdir():
                try:
                    targets.add(os.readlink(fd))
                except OSError:
                    continue
        except OSError:
            continue
    return targets


def _verified_by_manifest(path, size, entries):
    if size not in {e["bytes"] for e in entries}:
        return False
    sha = sha256_file(path)
    return any(e["bytes"] == size and e["sha256"] == sha for e in entries)


def find_reap_candidates(roots, manifest_entries=(), partial_max_age_s=DEFAULT_PARTIAL_MAX_AGE_S,
                         now=None):
    now = time.time() if now is None else now
    files, dataset_source_dirs, pull_dirs = _walk_roots(roots)
    entries = list(manifest_entries)
    durable = [e for e in entries if e.get("dataset")]
    staged = {(e["bytes"], e["sha256"]) for e in durable}
    staged_sizes = {e["bytes"] for e in durable}
    # class (c) verifies copies against ALL manifest entries (byte truth),
    # while class (b) above reaps only against durable-home entries.
    all_staged = {(e["bytes"], e["sha256"]) for e in entries}
    all_sizes = {e["bytes"] for e in entries}
    open_targets = _open_fd_targets()
    candidates = []
    seen = set()

    def add(path, size, cls, reason, extra_files=()):
        key = str(path)
        if key in seen:
            return
        seen.add(key)
        candidates.append({"path": key, "bytes": size, "class": cls,
                           "reason": reason,
                           "unit_files": [key] + [str(p) for p in extra_files]})

    # --- class (a): orphan *.kaggle-partial units -------------------------
    # A "unit" is the marker file X.kaggle-partial plus its sibling data
    # file X. In-flight heuristic (all must pass to reap): marker older
    # than partial_max_age_s, sibling not written within INFLIGHT_MTIME_S,
    # and neither file open by a live process (/proc fd scan).
    for _root, f in files:
        if not f.name.endswith(".kaggle-partial"):
            continue
        if _is_held(f, dataset_source_dirs):
            continue
        sibling = f.with_name(f.name[: -len(".kaggle-partial")])
        unit = [f] + ([sibling] if sibling.exists() else [])
        unit_bytes = 0
        for u in unit:
            try:
                unit_bytes += u.stat().st_size
            except OSError:
                pass
        if unit_bytes < MIN_REAP_BYTES:
            continue  # never touch anything under 1 MB
        try:
            marker_age = now - f.stat().st_mtime
        except OSError:
            continue
        if marker_age < partial_max_age_s:
            continue  # fresh partial: a pull may still own it
        if sibling.exists():
            try:
                if now - sibling.stat().st_mtime < INFLIGHT_MTIME_S:
                    continue  # being written right now
            except OSError:
                continue
        if any(str(u) in open_targets for u in unit):
            continue  # a live process holds it open
        add(f, unit_bytes, "a",
            f"orphan partial unit: marker age {int(marker_age)}s > "
            f"{int(partial_max_age_s)}s, sibling idle, not open by any process",
            extra_files=[sibling] if sibling.exists() else [])

    # --- class (b): pull-dir files byte-matching a staged manifest entry --
    if durable:
        for root, f in files:
            if _is_held(f, dataset_source_dirs) or not _in_pull_dir(f, root):
                continue
            try:
                size = f.stat().st_size
            except OSError:
                continue
            if size < MIN_REAP_BYTES or size not in staged_sizes:
                continue
            if (size, sha256_file(f)) in staged:
                add(f, size, "b",
                    "byte-identical (size+sha256) to an artifact whose manifest "
                    "entry records a durable home (dataset); this pull-dir copy "
                    "is a duplicate")

    # --- class (c): duplicate pull dirs, one copy verified complete -------
    # Group shallow pull dirs by shared relative file paths. A copy is
    # "verified complete" when it matches the manifest (if one was given)
    # or, with no manifest, when it has no *.kaggle-partial marker. Reap
    # only: partial copies, and byte-identical duplicates of a verified
    # copy. Complete copies whose bytes differ are report-only.
    by_rel = {}
    for d in pull_dirs:
        for _root, f in files:
            if d in f.parents:
                rel = str(f.relative_to(d))
                by_rel.setdefault(rel, {})[str(d)] = f
    for rel, copies in by_rel.items():
        if len(copies) < 2:
            continue
        infos = {}
        for dstr, f in copies.items():
            if _is_held(f, dataset_source_dirs):
                continue
            try:
                size = f.stat().st_size
            except OSError:
                continue
            if size < MIN_REAP_BYTES:
                continue
            partial = f.with_name(f.name + ".kaggle-partial").exists()
            verified = False
            sha = None
            if entries:
                if not partial and size in all_sizes:
                    sha = sha256_file(f)
                    verified = (size, sha) in all_staged
            else:
                verified = not partial
            infos[dstr] = {"path": f, "size": size, "partial": partial,
                           "verified": verified, "sha": sha}
        verified_copies = [i for i in infos.values() if i["verified"]]
        if not verified_copies:
            continue
        verified_shas = set()
        if entries:
            for i in verified_copies:
                if i["sha"] is None:
                    i["sha"] = sha256_file(i["path"])
                verified_shas.add((i["size"], i["sha"]))
        for i in infos.values():
            if i["verified"]:
                continue  # keep the verified one
            if i["partial"]:
                add(i["path"], i["size"], "c",
                    f"duplicate pull dir: an incomplete copy of {rel} while a "
                    f"verified complete copy exists in another pull dir")
            elif entries:
                sha = sha256_file(i["path"])
                if (i["size"], sha) in verified_shas:
                    add(i["path"], i["size"], "c",
                        f"duplicate pull dir: byte-identical duplicate of the "
                        f"verified copy of {rel}")

    candidates.sort(key=lambda c: -c["bytes"])
    return candidates


def cmd_reap(args):
    entries = load_manifest_entries(args.manifest)
    candidates = find_reap_candidates(args.roots, entries,
                                      partial_max_age_s=args.partial_max_age_hours * 3600)
    total = sum(c["bytes"] for c in candidates)
    lines = [f"reap: {len(candidates)} candidate(s), {human(total)} "
             f"({'APPLY - deleting' if args.apply else 'dry-run - nothing deleted'})"]
    for c in candidates:
        lines.append(f"  [class {c['class']}] {human(c['bytes']):>10s}  {c['path']}")
        lines.append(f"      {c['reason']}")
    deleted, errors = [], []
    if args.apply:
        for c in candidates:
            for unit_file in c["unit_files"]:
                try:
                    os.remove(unit_file)
                    deleted.append(unit_file)
                except FileNotFoundError:
                    pass
                except OSError as e:
                    errors.append({"path": unit_file, "error": str(e)})
        lines.append(f"  deleted {len(deleted)} file(s), {len(errors)} error(s)")
    summary = {"applied": bool(args.apply), "candidates": candidates,
               "candidate_bytes": total, "candidate_count": len(candidates),
               "deleted": deleted, "errors": errors, "exit_code": 0}
    return emit(summary, lines)


# --------------------------------------------------------------------------
# 2. verify-then-evict publish
# --------------------------------------------------------------------------

def resolve_kaggle_bin():
    env = os.environ.get("DISK_GUARD_KAGGLE_BIN")
    if env:
        return env
    on_path = shutil.which("kaggle")
    if on_path:
        return on_path
    if DEFAULT_KAGGLE_VENV.exists():
        return str(DEFAULT_KAGGLE_VENV)
    return "kaggle"


def _run(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def dataset_ready(kaggle_bin, dataset):
    rc, out = _run([kaggle_bin, "datasets", "status", dataset])
    return rc == 0 and "ready" in out.lower(), out.strip()


def publish_dataset(kaggle_bin, dataset, file_path):
    """Create (or version) the dataset from a hardlinked staging folder.

    Returns (ok, attempts). The staging folder hardlinks the product file
    (no extra bytes on the same filesystem; falls back to a copy) next to a
    generated dataset-metadata.json. The staging folder is always removed
    afterwards; the original file is never touched here.
    """
    slug = dataset.split("/")[-1]
    stage_dir = Path(file_path).parent / f".disk-guard-stage-{slug}"
    attempts = []
    try:
        if stage_dir.exists():
            shutil.rmtree(stage_dir)
        stage_dir.mkdir(parents=True)
        staged_file = stage_dir / Path(file_path).name
        try:
            os.link(file_path, staged_file)
        except OSError:
            shutil.copy2(file_path, staged_file)
        metadata = {
            "title": slug.replace("-", " ").replace("_", " ").title(),
            "id": dataset,
            "licenses": [{"name": "other"}],
        }
        (stage_dir / "dataset-metadata.json").write_text(json.dumps(metadata, indent=2))
        rc, out = _run([kaggle_bin, "datasets", "create", "-p", str(stage_dir)])
        attempts.append({"cmd": "datasets create", "rc": rc, "out": out.strip()[-400:]})
        if rc != 0:
            rc, out = _run([kaggle_bin, "datasets", "version", "-p", str(stage_dir),
                            "-m", "disk-guard publish-evict"])
            attempts.append({"cmd": "datasets version", "rc": rc, "out": out.strip()[-400:]})
        ready, sout = dataset_ready(kaggle_bin, dataset)
        attempts.append({"cmd": "datasets status (confirm)", "ready": ready, "out": sout[-200:]})
        return ready, attempts
    finally:
        shutil.rmtree(stage_dir, ignore_errors=True)


def cmd_publish_evict(args):
    summary = {"file": args.file, "dataset": args.dataset,
               "expected_sha256": args.sha256.lower(), "verified": False,
               "dataset_ready": False, "published": False, "evicted": False}
    lines = []
    f = Path(args.file)
    if not f.is_file():
        lines.append(f"publish-evict: {f} is not a file - refusing.")
        summary["exit_code"] = 2
        return emit(summary, lines)
    actual = sha256_file(f)
    summary["actual_sha256"] = actual
    summary["bytes"] = f.stat().st_size
    if actual.lower() != args.sha256.lower():
        lines.append(f"publish-evict: HASH MISMATCH for {f}")
        lines.append(f"  expected {args.sha256.lower()}")
        lines.append(f"  actual   {actual.lower()}")
        lines.append("  REFUSED - unverified files are never evicted; local copy kept.")
        summary["exit_code"] = 4
        return emit(summary, lines)
    summary["verified"] = True
    lines.append(f"publish-evict: {f} verified sha256 {actual[:16]}... "
                 f"({human(summary['bytes'])})")

    kaggle_bin = resolve_kaggle_bin()
    summary["kaggle_bin"] = kaggle_bin
    ready, sout = dataset_ready(kaggle_bin, args.dataset)
    if ready:
        summary["dataset_ready"] = True
        lines.append(f"  dataset {args.dataset}: already staged (status ready).")
    else:
        lines.append(f"  dataset {args.dataset}: not ready ({sout[-120:]}) - publishing...")
        ok, attempts = publish_dataset(kaggle_bin, args.dataset, f)
        summary["publish_attempts"] = attempts
        summary["published"] = ok
        summary["dataset_ready"] = ok
        if not ok:
            lines.append("  publish/confirm FAILED - REFUSED to evict; local copy kept.")
            summary["exit_code"] = 5
            return emit(summary, lines)
        lines.append(f"  dataset {args.dataset}: published and confirmed ready.")

    if args.manifest:
        mpath = Path(args.manifest)
        data = {}
        if mpath.exists():
            try:
                data = json.loads(mpath.read_text())
                if not isinstance(data, dict):
                    data = {}
            except (OSError, json.JSONDecodeError):
                data = {}
        data[f.name] = {"bytes": summary["bytes"], "sha256": actual.lower(),
                        "dataset": args.dataset,
                        "staged_at": datetime.now(timezone.utc).isoformat()}
        tmp = mpath.with_name(mpath.name + ".tmp")
        tmp.write_text(json.dumps(data, indent=2))
        os.replace(tmp, mpath)
        summary["manifest"] = str(mpath)
        lines.append(f"  recorded as staged in manifest {mpath}")

    os.remove(f)
    summary["evicted"] = True
    lines.append(f"  EVICTED local transit copy {f} - durable home: dataset {args.dataset}")
    summary["exit_code"] = 0
    return emit(summary, lines)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(prog="disk_guard",
                                description="Artifact-lifecycle disk/quota guard.")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="headroom report for a path (df + canary)")
    c.add_argument("path")
    c.add_argument("--probe-bytes", type=int, default=DEFAULT_PROBE_BYTES)
    c.set_defaults(func=cmd_check)

    c = sub.add_parser("preflight", help="gate a pull: exit 0 GO / 3 NO-GO")
    c.add_argument("--expect-bytes", type=int, required=True)
    c.add_argument("--path", required=True)
    c.add_argument("--probe-bytes", type=int, default=DEFAULT_PROBE_BYTES)
    c.set_defaults(func=cmd_preflight)

    c = sub.add_parser("inventory", help="classify space under roots")
    c.add_argument("--roots", nargs="+", required=True)
    c.add_argument("--manifest", default=None,
                   help="staged-artifact manifest for duplicate detection")
    c.set_defaults(func=cmd_inventory)

    c = sub.add_parser("reap", help="orphan/partial reaper (dry-run unless --apply)")
    c.add_argument("--roots", nargs="+", required=True)
    c.add_argument("--manifest", default=None)
    c.add_argument("--partial-max-age-hours", type=float, default=2.0)
    c.add_argument("--apply", action="store_true")
    c.set_defaults(func=cmd_reap)

    c = sub.add_parser("publish-evict",
                       help="verify -> publish/confirm dataset -> evict local copy")
    c.add_argument("--file", required=True)
    c.add_argument("--sha256", required=True)
    c.add_argument("--dataset", required=True, help="owner/slug")
    c.add_argument("--manifest", default=None,
                   help="optional manifest JSON to record the staged artifact in")
    c.set_defaults(func=cmd_publish_evict)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
