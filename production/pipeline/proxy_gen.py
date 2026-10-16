#!/usr/bin/env python3
"""proxy_gen.py -- batch-generate lightweight editing proxies with ffmpeg.

Animation assembly means scrubbing long timelines of heavy PNG sequences and
4K plates. Proxies make that fluid. This generates half-res (default 540p)
mpeg4 proxies next to your footage plus a manifest CSV mapping originals to
proxies for relink in any NLE.

Kdenlive note: Kdenlive has built-in proxy generation (Settings -> Configure
Kdenlive -> Proxy clips). Use this script when you want proxies made in batch,
on another machine, or with your own codec/resolution choices; then attach via
the manifest.

Usage:
  python3 proxy_gen.py footage/ --outdir footage/proxies
  python3 proxy_gen.py shot01.mp4 shot02.mov --height 360 --codec mjpeg
  python3 proxy_gen.py footage/ --outdir proxies/ --clean   # remove proxies+manifest
"""
import argparse
import csv
import json
import os
import shutil
import subprocess
import sys

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".avi", ".mxf", ".webm", ".m2ts", ".ts"}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAILED: {' '.join(cmd)}\n{r.stderr[-1500:]}", file=sys.stderr)
        sys.exit(1)
    return r


def probe(path):
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height,duration,r_frame_rate",
             "-of", "json", path])
    s = json.loads(r.stdout)["streams"][0]
    num, den = s.get("r_frame_rate", "30/1").split("/")
    return int(s["width"]), int(s["height"]), float(s.get("duration") or 0), float(num) / float(den or 1)


def main():
    ap = argparse.ArgumentParser(description="batch proxy generation")
    ap.add_argument("inputs", nargs="+", help="video files and/or directories")
    ap.add_argument("--outdir", default=None, help="proxy dir (default: <first input dir>/proxies)")
    ap.add_argument("--height", type=int, default=540, help="proxy height (width auto)")
    ap.add_argument("--codec", choices=["mpeg4", "mjpeg", "h264"], default="mpeg4")
    ap.add_argument("--suffix", default="_proxy")
    ap.add_argument("--clean", action="store_true", help="delete proxies + manifest, then exit")
    args = ap.parse_args()

    files = []
    for inp in args.inputs:
        if os.path.isdir(inp):
            for root, _, names in os.walk(inp):
                if os.path.abspath(root) == os.path.abspath(args.outdir or ""):
                    continue
                for nm in sorted(names):
                    if os.path.splitext(nm)[1].lower() in VIDEO_EXTS and args.suffix not in nm:
                        files.append(os.path.join(root, nm))
        elif os.path.isfile(inp):
            files.append(inp)
    if not files:
        print("No video files found.", file=sys.stderr)
        sys.exit(1)

    base = args.inputs[0] if os.path.isdir(args.inputs[0]) else os.path.dirname(os.path.abspath(args.inputs[0]))
    outdir = args.outdir or os.path.join(base, "proxies")
    os.makedirs(outdir, exist_ok=True)
    manifest = os.path.join(outdir, "proxy_manifest.csv")

    if args.clean:
        n = 0
        for nm in os.listdir(outdir):
            if args.suffix in nm:
                os.remove(os.path.join(outdir, nm))
                n += 1
        if os.path.exists(manifest):
            os.remove(manifest)
        print(f"Removed {n} proxies + manifest from {outdir}")
        return

    vcodec = {"mpeg4": ["-c:v", "mpeg4", "-q:v", "5"],
              "mjpeg": ["-c:v", "mjpeg", "-q:v", "4"],
              "h264": ["-c:v", "libx264", "-preset", "veryfast", "-crf", "23"]}[args.codec]

    rows = []
    for i, src in enumerate(files, 1):
        w, h, dur, fps = probe(src)
        stem = os.path.splitext(os.path.basename(src))[0]
        dst = os.path.join(outdir, stem + args.suffix + ".mp4")
        scale = f"scale=-2:{args.height}" if h > args.height else "scale=iw:ih"
        print(f"[{i}/{len(files)}] {os.path.basename(src)} {w}x{h} -> {dst}")
        run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vf", scale] + vcodec +
            ["-c:a", "aac", "-b:a", "96k", "-map_metadata", "0", dst])
        pw, ph, _, _ = probe(dst)
        rows.append({"original": os.path.abspath(src), "proxy": os.path.abspath(dst),
                     "orig_wh": f"{w}x{h}", "proxy_wh": f"{pw}x{ph}",
                     "duration_s": f"{dur:.2f}", "fps": f"{fps:.2f}"})

    with open(manifest, "w", newline="") as f:
        wri = csv.DictWriter(f, fieldnames=["original", "proxy", "orig_wh", "proxy_wh", "duration_s", "fps"])
        wri.writeheader()
        wri.writerows(rows)
    print(f"\n{len(rows)} proxies in {outdir}\nManifest: {manifest}")
    print("Kdenlive: Settings -> Configure Kdenlive -> Proxy clips, or relink via manifest.")


if __name__ == "__main__":
    main()
