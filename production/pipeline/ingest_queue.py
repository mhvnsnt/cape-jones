#!/usr/bin/env python3
"""
ingest_queue.py — Cape Jones FlipaClip ingest watcher.

Watches a folder for new FlipaClip exports (.mp4 / .mov) and automatically
runs the flipaclip_post.sh pipeline on them.

Drop a file into the watched folder → it gets processed → result lands in
the output folder with a timestamped name.

Usage:
  # Watch ~/FlipaclipExports and write to ~/CapeJones/processed
  ingest_queue.py --watch ~/FlipaclipExports --out ~/CapeJones/processed

  # With palette enforcement
  ingest_queue.py --watch ./inbox --out ./processed --palette show-palette.gpl

  # Dry-run (list what would be processed)
  ingest_queue.py --watch ./inbox --out ./processed --dry-run
"""

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


SUPPORTED = {".mp4", ".mov", ".webm", ".mkv"}


def is_supported(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED and path.is_file()


def already_processed(src: Path, out_dir: Path) -> bool:
    stem = src.stem
    # Look for any output that starts with the original stem
    for p in out_dir.glob(f"{stem}_post_*.mp4"):
        if p.stat().st_mtime > src.stat().st_mtime:
            return True
    return False


def run_pipeline(src: Path, out_dir: Path, pipeline_script: Path,
                 palette: str | None = None, dry_run: bool = False) -> Path | None:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_name = f"{src.stem}_post_{stamp}.mp4"
    out_path = out_dir / out_name

    if dry_run:
        print(f"[dry-run] would process {src} -> {out_path}")
        return out_path

    print(f"Processing {src.name} ...")
    cmd = [str(pipeline_script), str(src), str(out_path)]
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print(f"Pipeline failed on {src}", file=sys.stderr)
        return None

    # Optional palette enforcement on the frames of the result
    if palette and os.path.exists(palette):
        print(f"  applying palette {palette}")
        # Extract frames, enforce, re-encode (simple path)
        work = out_dir / f".pal_{stamp}"
        work.mkdir(exist_ok=True)
        frames = work / "frames"
        frames.mkdir()
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-i", str(out_path),
            str(frames / "f%04d.png"),
        ], check=True)
        pal_script = Path(__file__).parent / "palette-enforce.py"
        subprocess.run([
            sys.executable, str(pal_script), "enforce", palette,
            str(frames / "*.png"), "--outdir", str(work / "pal"),
        ], check=False)
        # Re-encode if pal frames exist
        pal_dir = work / "pal"
        if pal_dir.exists() and any(pal_dir.glob("*.png")):
            pal_out = out_dir / f"{src.stem}_post_{stamp}_pal.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-v", "error",
                "-framerate", "24", "-i", str(pal_dir / "f%04d.png"),
                "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
                str(pal_out),
            ], check=True)
            out_path = pal_out

    print(f"  done -> {out_path}")
    return out_path


def watch(watch_dir: Path, out_dir: Path, pipeline_script: Path,
          palette: str | None, poll: float, dry_run: bool):
    watch_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Watching {watch_dir} -> {out_dir} (poll {poll}s)")
    if palette:
        print(f"Palette enforcement: {palette}")

    seen = set()
    while True:
        for p in sorted(watch_dir.iterdir()):
            if not is_supported(p):
                continue
            key = (str(p), p.stat().st_mtime)
            if key in seen:
                continue
            if already_processed(p, out_dir):
                seen.add(key)
                continue
            run_pipeline(p, out_dir, pipeline_script, palette, dry_run)
            seen.add(key)
        time.sleep(poll)


def main():
    ap = argparse.ArgumentParser(description="FlipaClip ingest queue watcher")
    ap.add_argument("--watch", required=True, help="Folder to watch for exports")
    ap.add_argument("--out", required=True, help="Output folder for processed clips")
    ap.add_argument("--pipeline", default=None,
                    help="Path to flipaclip_post.sh (default: sibling)")
    ap.add_argument("--palette", default=None, help="Optional .gpl palette to enforce")
    ap.add_argument("--poll", type=float, default=5.0, help="Poll interval seconds")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    watch_dir = Path(args.watch).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve()

    if args.pipeline:
        pipeline = Path(args.pipeline).resolve()
    else:
        pipeline = Path(__file__).parent / "flipaclip_post.sh"

    if not pipeline.exists():
        print(f"Pipeline script not found: {pipeline}", file=sys.stderr)
        sys.exit(1)

    watch(watch_dir, out_dir, pipeline, args.palette, args.poll, args.dry_run)


if __name__ == "__main__":
    main()
