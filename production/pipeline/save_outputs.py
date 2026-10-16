#!/usr/bin/env python3
"""
save_outputs.py — BULLETPROOF in-kernel output saver for Kaggle GPU runs.

NEVER LOSE A RENDER AGAIN. Call saver.checkpoint() after EVERY unit of work
(every chunk, every segment, every milestone) — never only at the end.

How it works
------------
1. Files are staged into STAGE_DIR (accumulates across checkpoints).
2. manifest.json + heartbeat are written into the stage dir.
3. The stage dir is published as a new version of a Kaggle dataset via
   `kaggle datasets version` (fallback: `kaggle datasets create`).
   Kaggle kernels are PRE-AUTHENTICATED as the notebook owner — no API keys,
   no credential cells, no secrets in the notebook. This is the same pattern
   production teams use (verified against 2026 repos: CodeWithOz/birdclef_2026,
   umud-challenge — "Publish from the notebook ... with fallback to create").
4. The publish is verified (rc==0 + version number parsed from output).
5. Local .save_state.json records what was saved where.

If the session dies mid-run, everything checkpointed so far survives as
Kaggle dataset versions — independent of Quick Save, independent of the
session VM. A re-run resumes from the dataset (attach it via dataset_sources;
restore_from_input() handles Kaggle's zip-extraction-on-mount quirk).

Second copies (GitHub releases, TeraBox) are handled QUEUE-SIDE on the VM
(where the real credentials live) — never inside the kernel.

Design rules
------------
- Saving must NEVER kill the render. Every failure is caught, logged loudly,
  and the render continues. Local /kaggle/working outputs remain last resort.
- No third-party deps: stdlib only (+ the `kaggle` CLI preinstalled in kernels).

Env
---
  KAGGLE_SAVE_DATASET   e.g. "marsfmmg/pantera-v4-outputs" (required to save)
  SAVE_EVERY_SEC        heartbeat interval in seconds (default 120)

Notebook usage
--------------
  from save_outputs import RenderSaver
  saver = RenderSaver(dataset_slug=os.environ.get("KAGGLE_SAVE_DATASET"))
  saver.start_watchdog()
  ... render chunk ...
  saver.checkpoint("chunk-05", ["/kaggle/working/pantera_chunk05.zip"])
  ...
  saver.stop_watchdog()
"""
import atexit
import glob
import hashlib
import json
import os
import shutil
import signal
import subprocess
import tempfile
import threading
import time
import zipfile

METADATA_FILE = "dataset-metadata.json"
MANIFEST_FILE = "manifest.json"
HEARTBEAT_FILE = ".heartbeat.json"
STATE_FILE = ".save_state.json"
ERROR_LOG = ".save_errors.log"

DEFAULT_HEARTBEAT_SEC = 120
VERSION_TIMEOUT_SEC = 900  # dataset uploads can be large; be patient


def _log(msg):
    print(f"[saver] {msg}", flush=True)


_ERR_LOG_DIR = "/kaggle/working"  # overridden by RenderSaver.__init__


def _err(msg):
    _log(f"ERROR: {msg}")
    try:
        with open(os.path.join(_ERR_LOG_DIR, ERROR_LOG), "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] {msg}\n")
    except Exception:
        pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def _run(cmd, timeout=120):
    """Run cmd list. Returns (rc, stdout, stderr). Never raises."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s: {' '.join(cmd)}"
    except FileNotFoundError:
        return 127, "", f"command not found: {cmd[0]}"
    except Exception as e:  # noqa: BLE001
        return 1, "", f"unexpected: {e}"


def _ensure_kaggle_cli():
    """Make sure `kaggle` CLI works in-kernel. Returns True/False."""
    rc, out, _ = _run(["kaggle", "--version"], timeout=30)
    if rc == 0:
        return True
    _log("kaggle CLI missing, trying pip install...")
    rc, _, err = _run([os.environ.get("PIP_BIN", "pip"), "install", "-q", "kaggle"],
                      timeout=300)
    if rc != 0:
        _err(f"pip install kaggle failed: {err[:300]}")
        return False
    rc, _, _ = _run(["kaggle", "--version"], timeout=30)
    return rc == 0


class RenderSaver:
    """Bulletproof per-checkpoint saver. See module docstring."""

    def __init__(self, stage_dir="/kaggle/working/.save_stage",
                 dataset_slug=None, heartbeat_sec=None, note="",
                 work_dir="/kaggle/working"):
        self.stage_dir = stage_dir
        self.work_dir = (work_dir if os.path.isdir(work_dir)
                         else tempfile.mkdtemp(prefix="saver-work-"))
        self.dataset_slug = (dataset_slug
                             or os.environ.get("KAGGLE_SAVE_DATASET", "")).strip()
        try:
            self.heartbeat_sec = int(os.environ.get(
                "SAVE_EVERY_SEC",
                heartbeat_sec if heartbeat_sec else DEFAULT_HEARTBEAT_SEC))
        except ValueError:
            self.heartbeat_sec = DEFAULT_HEARTBEAT_SEC
        self.note = note
        self.progress = {}
        self._watchdog = None
        self._stop = threading.Event()
        self._emergency_done = False
        self._cli_ok = None
        self._last_published_manifest_sha = ""
        global _ERR_LOG_DIR
        _ERR_LOG_DIR = self.work_dir
        os.makedirs(self.stage_dir, exist_ok=True)
        os.makedirs(self.work_dir, exist_ok=True)
        self._write_metadata()
        atexit.register(self._emergency)
        for sig in (signal.SIGTERM, signal.SIGINT):
            try:
                signal.signal(sig, self._on_signal)
            except Exception:
                pass
        if self.dataset_slug:
            _log(f"save dataset: {self.dataset_slug}")
        else:
            _log("WARNING: no KAGGLE_SAVE_DATASET set — checkpoints will stage "
                 "locally only (no off-session copy!)")

    # ---- helpers -----------------------------------------------------
    @property
    def user(self):
        return self.dataset_slug.split("/")[0] if "/" in self.dataset_slug else ""

    @property
    def dsname(self):
        return self.dataset_slug.split("/")[-1] if self.dataset_slug else ""

    def _write_metadata(self):
        if not self.dataset_slug:
            return
        meta = {"title": self.dsname, "id": self.dataset_slug,
                "licenses": [{"name": "CC0-1.0"}]}
        with open(os.path.join(self.stage_dir, METADATA_FILE), "w") as f:
            json.dump(meta, f, indent=2)

    def _manifest_path(self):
        return os.path.join(self.stage_dir, MANIFEST_FILE)

    def _read_manifest(self):
        mp = self._manifest_path()
        if os.path.exists(mp):
            try:
                with open(mp) as f:
                    return json.load(f)
            except Exception:
                pass
        return {"dataset": self.dataset_slug, "checkpoints": []}

    def _write_manifest(self, m):
        with open(self._manifest_path(), "w") as f:
            json.dump(m, f, indent=2)

    def _state_path(self):
        return os.path.join(self.work_dir, STATE_FILE)

    def _record_state(self, entry):
        try:
            st = []
            if os.path.exists(self._state_path()):
                with open(self._state_path()) as f:
                    st = json.load(f)
            st.append(entry)
            with open(self._state_path(), "w") as f:
                json.dump(st, f, indent=2)
        except Exception as e:  # noqa: BLE001
            _err(f"could not write state file: {e}")

    # ---- watchdog / heartbeat ----------------------------------------
    def _heartbeat_payload(self):
        return {
            "ts": time.time(),
            "iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "dataset": self.dataset_slug,
            "note": self.note,
            "progress": dict(self.progress),
            "pid": os.getpid(),
        }

    def heartbeat(self):
        """Write a heartbeat (liveness + progress). Never raises."""
        try:
            payload = self._heartbeat_payload()
            blob = json.dumps(payload, indent=2)
            with open(os.path.join(self.work_dir, HEARTBEAT_FILE), "w") as f:
                f.write(blob)
            with open(os.path.join(self.stage_dir, HEARTBEAT_FILE), "w") as f:
                f.write(blob)
        except Exception as e:  # noqa: BLE001
            _err(f"heartbeat write failed: {e}")

    def _watch_loop(self):
        while not self._stop.wait(self.heartbeat_sec):
            self.heartbeat()

    def start_watchdog(self):
        if self._watchdog and self._watchdog.is_alive():
            return
        self._stop.clear()
        self.heartbeat()
        self._watchdog = threading.Thread(target=self._watch_loop,
                                         name="saver-watchdog", daemon=True)
        self._watchdog.start()
        _log(f"watchdog started (heartbeat every {self.heartbeat_sec}s)")

    def stop_watchdog(self):
        self._stop.set()
        if self._watchdog:
            self._watchdog.join(timeout=5)
        self.heartbeat()
        _log("watchdog stopped")

    def _on_signal(self, signum, frame):
        _log(f"received signal {signum} — emergency save attempt")
        self._emergency()

    def _manifest_sha(self):
        try:
            return sha256_file(self._manifest_path())
        except Exception:
            return ""

    def _emergency(self):
        """Last-ditch save on interpreter shutdown. Never raises.
        Skips if nothing changed since the last confirmed publish."""
        if self._emergency_done:
            return
        self._emergency_done = True
        try:
            if self.dataset_slug and self._stage_has_files():
                if self._manifest_sha() == self._last_published_manifest_sha:
                    _log("atexit: no changes since last publish — skipping")
                    return
                _log("atexit: attempting final dataset version...")
                ok = self._publish("emergency-shutdown-save", timeout=300)
                _log(f"atexit: final save {'OK' if ok else 'FAILED'}")
        except Exception as e:  # noqa: BLE001
            _err(f"emergency save failed: {e}")

    def _stage_has_files(self):
        for root, _, files in os.walk(self.stage_dir):
            for fn in files:
                if fn not in (METADATA_FILE, MANIFEST_FILE, HEARTBEAT_FILE):
                    return True
        return False

    # ---- publish ------------------------------------------------------
    def _cli(self):
        if self._cli_ok is None:
            self._cli_ok = _ensure_kaggle_cli()
        return self._cli_ok

    def _publish(self, message, timeout=VERSION_TIMEOUT_SEC):
        """Publish stage dir as a dataset version (fallback: create).

        Returns (ok, version_str). Never raises."""
        if not self._cli():
            return False, ""
        full_msg = f"{message}" + (f" — {self.note}" if self.note else "")
        rc, out, err = _run(
            ["kaggle", "datasets", "version", "-p", self.stage_dir,
             "-m", full_msg], timeout=timeout)
        blob = (out + "\n" + err).lower()
        if rc != 0 and ("not found" in blob or "404" in blob
                        or "does not exist" in blob):
            _log("dataset does not exist yet — creating it...")
            rc, out, err = _run(
                ["kaggle", "datasets", "create", "-p", self.stage_dir],
                timeout=timeout)
            blob = (out + "\n" + err).lower()
        if rc != 0:
            _err(f"dataset publish failed rc={rc}: {(err or out)[:400]}")
            return False, ""
        import re
        m = re.search(r"versions/(\d+)", out + err)
        ver = m.group(1) if m else "unknown"
        _log(f"dataset publish OK (version {ver})")
        return True, ver

    # ---- main API ------------------------------------------------------
    def checkpoint(self, name, paths):
        """Stage `paths` and publish a dataset version. Returns True if the
        off-session copy is confirmed. NEVER raises — failures are logged
        loudly and the render must continue."""
        try:
            return self._checkpoint_inner(name, paths)
        except Exception as e:  # noqa: BLE001
            _err(f"checkpoint '{name}' raised: {e}")
            return False

    def _checkpoint_inner(self, name, paths):
        staged = []
        for p in paths:
            if not os.path.exists(p):
                _err(f"checkpoint '{name}': missing file {p} — skipping it")
                continue
            dst = os.path.join(self.stage_dir, os.path.basename(p))
            shutil.copy2(p, dst)
            staged.append({
                "name": os.path.basename(p),
                "bytes": os.path.getsize(dst),
                "sha256": sha256_file(dst),
            })
        if not staged:
            _err(f"checkpoint '{name}': nothing staged, aborting publish")
            return False

        man = self._read_manifest()
        entry = {"checkpoint": name, "ts": time.time(),
                 "iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                 "files": staged, "dataset_version": None}
        man["checkpoints"].append(entry)
        self._write_manifest(man)
        self.heartbeat()
        self.progress["last_checkpoint"] = name

        if not self.dataset_slug:
            _err("no save dataset configured — files staged locally only!")
            self._record_state({**entry, "saved": False,
                                "reason": "no-dataset-configured"})
            return False

        ok, ver = self._publish(f"checkpoint: {name}")
        entry["dataset_version"] = ver if ok else None
        # rewrite manifest with version, then re-read state is fine as-is
        man["checkpoints"][-1] = entry
        self._write_manifest(man)
        if ok:
            self._last_published_manifest_sha = self._manifest_sha()
        self._record_state({**entry, "saved": ok})
        if ok:
            _log(f"checkpoint '{name}' CONFIRMED (dataset v{ver}) — "
                 f"{len(staged)} file(s), "
                 f"{sum(s['bytes'] for s in staged)} bytes")
        else:
            _err(f"checkpoint '{name}' NOT confirmed — will retry next checkpoint; "
                 "local files in /kaggle/working remain the fallback")
        return ok

    # ---- resume ---------------------------------------------------------
    def _rezip(self, extracted_dir, zip_name):
        """Rebuild the expected zip from Kaggle's extracted-on-mount layout."""
        files = sorted(p for p in
                       glob.glob(os.path.join(extracted_dir, "**", "*"),
                                 recursive=True)
                       if os.path.isfile(p))
        if not files:
            return None
        dst = os.path.join(self.stage_dir, zip_name)
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_STORED) as zf:
            for p in files:
                zf.write(p, os.path.basename(p))
        _log(f"re-zipped {len(files)} files from extracted layout -> {zip_name}")
        return dst

    def restore_from_input(self):
        """Restore previously-saved files from an attached dataset input.

        Handles Kaggle's zip-extraction-on-mount quirk (searches for the exact
        filename; falls back to re-zipping extracted frame dirs).
        Returns {filename: local_path} for files now in /kaggle/working."""
        restored = {}
        if not self.dataset_slug:
            return restored
        cands = [f"/kaggle/input/{self.dsname}",
                 f"/kaggle/input/datasets/{self.user}/{self.dsname}"]
        inp = next((c for c in cands if os.path.isdir(c)), None)
        if not inp:
            _log("no save-dataset input attached — fresh start")
            return restored
        _log(f"save-dataset input found: {inp}")

        names = []
        man_path = os.path.join(inp, MANIFEST_FILE)
        if os.path.exists(man_path):
            try:
                with open(man_path) as f:
                    man = json.load(f)
                for cp in man.get("checkpoints", []):
                    names.extend(f["name"] for f in cp.get("files", []))
            except Exception as e:  # noqa: BLE001
                _err(f"could not read input manifest: {e}")
        if not names:
            names = [os.path.basename(p)
                     for p in glob.glob(os.path.join(inp, "*.zip"))]

        for name in names:
            hits = glob.glob(os.path.join(inp, "**", name), recursive=True)
            src = hits[0] if hits else None
            if src is None and name.endswith(".zip"):
                stem = name[:-4]
                dirs = [d for d in glob.glob(os.path.join(inp, "**", stem),
                                            recursive=True)
                        if os.path.isdir(d)]
                if dirs:
                    src = self._rezip(dirs[0], name)
            if not src:
                _err(f"restore: {name} not found in input")
                continue
            for dest_dir in (self.work_dir, self.stage_dir):
                dst = os.path.join(dest_dir, name)
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)
            restored[name] = os.path.join(self.work_dir, name)
            _log(f"restored {name}")
        return restored


if __name__ == "__main__":
    print(__doc__)
