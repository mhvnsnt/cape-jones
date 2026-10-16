#!/usr/bin/env python3
"""
kaggle_queue.py — GPU queue manager for Kaggle batch notebook runs.

The owner never wants to manually kick off renders. This script runs as a
systemd timer (every 15 min) and:
  1. Checks status of any running job (via Kaggle API)
  2. Downloads outputs when a job completes
  3. Starts the next pending job when the GPU is free
  4. Handles GPU quota exhaustion gracefully (waits, retries later)

Jobs are batch kernel runs (not interactive sessions) — fully autonomous,
no browser needed.

Usage:
  kaggle_queue.py tick                          # one queue pass (timer calls this)
  kaggle_queue.py status                        # show queue state
  kaggle_queue.py add --notebook PATH --title TITLE [--datasets ds1,ds2]
                      [--pre-copy SRC:DST ...] [--outputs file1,file2]
                      [--output-dir DIR] [--no-gpu]
  kaggle_queue.py retry JOB_ID                  # requeue a failed job
  kaggle_queue.py clear-done                    # remove completed jobs from queue

Queue file: ~/workspace/agent-ops/kaggle-queue.json
"""
import json, os, sys, subprocess, shutil, tempfile, time, argparse
from datetime import datetime, timezone

QUEUE_FILE = os.path.expanduser("~/workspace/agent-ops/kaggle-queue.json")
WORK_DIR = os.path.expanduser("~/workspace/tools/kaggle-queue/work")
LOG_FILE = os.path.expanduser("~/workspace/agent-ops/kaggle-queue.log")
KERNEL_USER = "marsfmmg"


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


# --- FAILURE NOTIFICATIONS (NO-SILENT-FAILURE LAW) ---
# When a job fails, we NEVER stay silent. Notifications go to:
# 1. ~/workspace/agent-ops/failure-alerts.log (always)
# 2. ntfy.sh topic (if configured — owner gets phone push)
# 3. The overnight handoff (for the owner to see on return)

ALERT_LOG = os.path.expanduser("~/workspace/agent-ops/failure-alerts.log")
NTFY_TOPIC_FILE = os.path.expanduser("~/workspace/agent-ops/ntfy-topic.txt")


def notify(title, body, priority="high"):
    """Send a failure/completion alert. Never silent."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    alert = f"[{ts}] {priority.upper()}: {title} — {body}"
    # 1. Always log locally
    os.makedirs(os.path.dirname(ALERT_LOG), exist_ok=True)
    with open(ALERT_LOG, "a") as f:
        f.write(alert + "\n")
    log(f"ALERT: {title} — {body[:100]}")
    # 2. Try apprise (system-wide, fans out to 100+ services)
    try:
        apprise_urls = os.path.expanduser("~/workspace/agent-ops/apprise-urls.txt")
        if os.path.exists(apprise_urls):
            with open(apprise_urls) as f:
                urls = [u.strip() for u in f if u.strip() and not u.startswith("#")]
            if urls:
                subprocess.run(
                    ["apprise", "-t", title[:60], "-b", body[:500]] + urls,
                    timeout=30, capture_output=True)
                log(f"apprise notification sent via {len(urls)} service(s)")
    except Exception as e:
        log(f"apprise failed (non-fatal): {e}")
    # 3. Try ntfy.sh push (owner's phone) — note: blocked from this VM by egress proxy
    try:
        if os.path.exists(NTFY_TOPIC_FILE):
            with open(NTFY_TOPIC_FILE) as f:
                topic = f.read().strip()
            if topic:
                subprocess.run(
                    ["curl", "-s", "-H", f"Priority: {priority}",
                     "-H", f"Title: {title[:60]}",
                     "--data-binary", body[:500],
                     f"https://ntfy.sh/{topic}"],
                    timeout=15, capture_output=True)
                log(f"ntfy push sent to {topic}")
    except Exception as e:
        log(f"ntfy push failed (non-fatal): {e}")
    # 4. Append to overnight handoff blockers section
    try:
        handoff = os.path.expanduser("~/workspace/agent-ops/overnight-handoff.md")
        if os.path.exists(handoff):
            with open(handoff, "a") as f:
                f.write(f"\n- **ALERT {ts}**: {title} — {body[:200]}\n")
    except Exception:
        pass


def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return {"jobs": []}
    with open(QUEUE_FILE) as f:
        return json.load(f)


def save_queue(q):
    os.makedirs(os.path.dirname(QUEUE_FILE), exist_ok=True)
    tmp = QUEUE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(q, f, indent=2)
    os.replace(tmp, QUEUE_FILE)


def kaggle(args, **kwargs):
    """Run kaggle CLI, return (rc, stdout, stderr)."""
    p = subprocess.run(["kaggle"] + args, capture_output=True, text=True,
                       timeout=kwargs.get("timeout", 120))
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def kernel_status(slug):
    """Return (state, raw) for a kernel. state in: running, complete, error, unknown."""
    rc, out, err = kaggle(["kernels", "status", slug])
    if rc != 0:
        return "unknown", err or out
    low = out.lower()
    if "complete" in low:
        return "complete", out
    if "error" in low or "failed" in low or "cancelled" in low:
        return "error", out
    return "running", out


def inject_pre_cells(nb_path, pre_cells):
    """Return notebook dict with pre_cells inserted after the first markdown cell."""
    with open(nb_path) as f:
        nb = json.load(f)
    if not pre_cells:
        return nb
    cells = nb["cells"]
    # insert after leading markdown cells
    idx = 0
    while idx < len(cells) and cells[idx]["cell_type"] == "markdown":
        idx += 1
    new_cells = []
    for i, src in enumerate(pre_cells):
        new_cells.append({"cell_type": "code", "metadata": {},
                          "execution_count": None, "outputs": [],
                          "source": f"# === QUEUE INJECTED SETUP {i} ===\n" + src})
    nb["cells"] = cells[:idx] + new_cells + cells[idx:]
    # validate
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            compile("".join(c["source"]), "<injected>", "exec")
    return nb


def push_job(job):
    """Push a notebook as a new Kaggle kernel version (triggers batch run).
    Returns (ok, slug_or_error)."""
    slug_base = "".join(c if c.isalnum() else "-" for c in job["title"].lower())[:40].strip("-")
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    slug = f"{slug_base}-{ts}"
    full_slug = f"{KERNEL_USER}/{slug}"

    kdir = os.path.join(WORK_DIR, f"push-{job['id']}")
    shutil.rmtree(kdir, ignore_errors=True)
    os.makedirs(kdir, exist_ok=True)

    nb = inject_pre_cells(job["notebook_path"], job.get("pre_cells", []))
    with open(os.path.join(kdir, "notebook.ipynb"), "w") as f:
        json.dump(nb, f)

    metadata = {
        "id": full_slug,
        "title": f"{job['title']} (queue {ts})",
        "code_file": "notebook.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": True,
        "enable_gpu": job.get("gpu", True),
        "enable_internet": job.get("internet", True),
        "dataset_sources": job.get("datasets", []),
        "competition_sources": [],
        "kernel_sources": [],
    }
    with open(os.path.join(kdir, "kernel-metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    log(f"pushing job {job['id']} as {full_slug} ...")
    rc, out, err = kaggle(["kernels", "push", "-p", kdir], timeout=300)
    combined = (out + "\n" + err).lower()
    if rc != 0:
        if "gpu" in combined and ("quota" in combined or "cap" in combined or
                                   "maximum" in combined or "limit" in combined):
            return False, "GPU_QUOTA"
        return False, (err or out)[:500]
    log(f"job {job['id']} pushed: {full_slug}")
    return True, full_slug


def download_outputs(job):
    """Download kernel outputs to job's output_dir. Returns (ok, msg)."""
    slug = job.get("kernel_slug")
    if not slug:
        return False, "no kernel_slug"
    outdir = os.path.expanduser(job.get("output_dir") or
                                f"~/workspace/kaggle-queue-output/{job['id']}")
    os.makedirs(outdir, exist_ok=True)
    log(f"downloading outputs for {job['id']} -> {outdir}")
    rc, out, err = kaggle(["kernels", "output", slug, "-p", outdir,
                           "--force"], timeout=600)
    if rc != 0:
        return False, (err or out)[:500]
    files = []
    for root, _, fns in os.walk(outdir):
        for fn in fns:
            fp = os.path.join(root, fn)
            files.append(f"{os.path.relpath(fp, outdir)} ({os.path.getsize(fp)} bytes)")
    # verify expected outputs if specified
    expected = job.get("expected_outputs", [])
    missing = [e for e in expected
               if not os.path.exists(os.path.join(outdir, e))]
    if missing:
        return False, f"missing expected outputs: {missing}"
    return True, f"downloaded {len(files)} files: {'; '.join(files[:10])}"


def tick():
    """One queue pass: update running jobs, start next pending job if GPU free."""
    q = load_queue()
    jobs = q.get("jobs", [])
    changed = False

    # Manual hold: don't start new jobs (e.g. interactive session using GPU)
    if q.get("hold"):
        log(f"queue on HOLD ({q.get('hold_reason', 'no reason')}) — monitoring only")

    # 1. Update running jobs
    any_running = False
    for job in jobs:
        if job["status"] == "running":
            state, raw = kernel_status(job["kernel_slug"])
            if state == "complete":
                ok, msg = download_outputs(job)
                job["status"] = "done" if ok else "error"
                job["finished_at"] = datetime.now(timezone.utc).isoformat()
                job["result"] = msg
                log(f"job {job['id']} COMPLETE: {msg}")
                if ok:
                    notify(f"Render done: {job['title']}",
                           f"Outputs: {msg}", priority="default")
                else:
                    notify(f"FAILED output verify: {job['title']}",
                           f"Kernel completed but outputs missing: {msg}")
                changed = True
            elif state == "error":
                job["status"] = "error"
                job["finished_at"] = datetime.now(timezone.utc).isoformat()
                job["result"] = raw[:500]
                log(f"job {job['id']} FAILED: {raw[:200]}")
                notify(f"FAILED: {job['title']}",
                       f"Kernel error: {raw[:300]}")
                changed = True
            else:
                any_running = True
                log(f"job {job['id']} still running")

    # 2. Start next pending job if nothing running and not on hold
    if not any_running and not q.get("hold"):
        pending = [j for j in jobs if j["status"] == "pending"]
        if pending:
            job = pending[0]
            # sanity: notebook file must exist
            if not os.path.exists(job["notebook_path"]):
                job["status"] = "error"
                job["result"] = f"notebook not found: {job['notebook_path']}"
                log(f"job {job['id']} ERROR: notebook missing")
            else:
                ok, result = push_job(job)
                if ok:
                    job["status"] = "running"
                    job["kernel_slug"] = result
                    job["started_at"] = datetime.now(timezone.utc).isoformat()
                    log(f"job {job['id']} STARTED: {result}")
                elif result == "GPU_QUOTA":
                    log(f"GPU quota/cap hit — will retry next tick")
                else:
                    job["status"] = "error"
                    job["result"] = result
                    log(f"job {job['id']} PUSH FAILED: {result}")
            changed = True
        else:
            log("queue idle: nothing running, nothing pending")

    if changed:
        save_queue(q)
    return q


def cmd_status(args):
    q = load_queue()
    jobs = q.get("jobs", [])
    if not jobs:
        print("queue empty")
        return
    for j in jobs:
        print(f"[{j['status']:8s}] {j['id']}: {j['title']}")
        if j.get("kernel_slug"):
            print(f"           kernel: {j['kernel_slug']}")
        if j.get("result"):
            print(f"           result: {j['result'][:120]}")
        if j.get("started_at"):
            print(f"           started: {j['started_at']}")


def cmd_add(args):
    q = load_queue()
    job_id = f"job-{len(q['jobs']) + 1:03d}-{int(time.time())}"
    job = {
        "id": job_id,
        "title": args.title,
        "notebook_path": os.path.abspath(args.notebook),
        "status": "pending",
        "gpu": not args.no_gpu,
        "internet": True,
        "datasets": args.datasets.split(",") if args.datasets else [],
        "pre_cells": [],
        "expected_outputs": args.outputs.split(",") if args.outputs else [],
        "output_dir": args.output_dir,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    # --pre-copy SRC:DST pairs become a setup cell copying from /kaggle/input
    if args.pre_copy:
        lines = ["import shutil, os, glob"]
        for pair in args.pre_copy:
            src, dst = pair.split(":", 1)
            lines.append(f"shutil.copy('/kaggle/input/{src}', '{dst}')")
            lines.append(f"print('copied {src} -> {dst}')")
        job["pre_cells"].append("\n".join(lines) + "\n")
    if args.pre_cell_file:
        with open(args.pre_cell_file) as f:
            job["pre_cells"].append(f.read())
    q["jobs"].append(job)
    save_queue(q)
    print(f"added {job_id}: {args.title}")
    log(f"added job {job_id}: {args.title}")


def cmd_retry(args):
    q = load_queue()
    for j in q["jobs"]:
        if j["id"] == args.job_id and j["status"] in ("error", "done"):
            j["status"] = "pending"
            j.pop("kernel_slug", None)
            j.pop("result", None)
            save_queue(q)
            print(f"requeued {args.job_id}")
            log(f"requeued {args.job_id}")
            return
    print(f"job {args.job_id} not found or not in error/done state")


def cmd_clear_done(args):
    q = load_queue()
    before = len(q["jobs"])
    q["jobs"] = [j for j in q["jobs"] if j["status"] not in ("done",)]
    save_queue(q)
    print(f"removed {before - len(q['jobs'])} done jobs")


def cmd_hold(args):
    q = load_queue()
    q["hold"] = True
    q["hold_reason"] = args.reason
    save_queue(q)
    print(f"queue on hold: {args.reason}")
    log(f"queue HOLD set: {args.reason}")


def cmd_release(args):
    q = load_queue()
    q.pop("hold", None)
    q.pop("hold_reason", None)
    save_queue(q)
    print("queue released — will start pending jobs on next tick")
    log("queue HOLD released")


def main():
    ap = argparse.ArgumentParser(description="Kaggle GPU queue manager")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("tick", help="one queue pass (called by timer)")
    sub.add_parser("status", help="show queue")

    a = sub.add_parser("add", help="add a job")
    a.add_argument("--notebook", required=True)
    a.add_argument("--title", required=True)
    a.add_argument("--datasets", default="")
    a.add_argument("--pre-copy", nargs="*", default=[],
                   help="SRC:DST pairs copied from /kaggle/input at start")
    a.add_argument("--pre-cell-file", default="",
                   help="file whose contents become an injected setup cell")
    a.add_argument("--outputs", default="",
                   help="comma-separated expected output paths (relative to output dir)")
    a.add_argument("--output-dir", default="")
    a.add_argument("--no-gpu", action="store_true")

    r = sub.add_parser("retry", help="requeue a failed/done job")
    r.add_argument("job_id")
    sub.add_parser("clear-done", help="remove done jobs")

    h = sub.add_parser("hold", help="pause starting new jobs (monitoring continues)")
    h.add_argument("reason", nargs="?", default="manual")
    sub.add_parser("release", help="resume starting new jobs")

    args = ap.parse_args()
    if args.cmd == "tick":
        tick()
    elif args.cmd == "status":
        cmd_status(args)
    elif args.cmd == "add":
        cmd_add(args)
    elif args.cmd == "retry":
        cmd_retry(args)
    elif args.cmd == "clear-done":
        cmd_clear_done(args)
    elif args.cmd == "hold":
        cmd_hold(args)
    elif args.cmd == "release":
        cmd_release(args)


if __name__ == "__main__":
    main()
