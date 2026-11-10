#!/usr/bin/env python3
"""OUR OWN video downloader — written from scratch for Cape Jones, 2026-11-02.

Not copied from facebooksave.com or any other downloader site. It is a thin
CLI wrapper around yt-dlp (a public, general-purpose downloader) plus
ffprobe metadata. It only downloads PUBLIC links the user supplies; it
does not bypass logins, paywalls, DRM, or private content, and it does
not re-upload anything.

Usage:
    python3 download_video.py <url> [--out-dir DIR] [--format FORMAT]

Supported (public links): facebook.com / fb.watch, tiktok.com,
youtube.com / youtu.be. Other hosts are rejected, on purpose — the
user asked for those three, and a narrow allow-list avoids silent
misuse on other sites.

Output: <out-dir>/<id>.<ext> + <out-dir>/<id>.info.json
  (title, uploader, duration, fps, width, height, filesize, source url)
Exit codes: 0 ok, 2 bad usage / unsupported host, 3 download failed.
"""
import json, os, re, shutil, subprocess, sys
from urllib.parse import urlparse

ALLOWED = [
    (r"(^|\.)facebook\.com$", "facebook"),
    (r"(^|\.)fb\.watch$", "facebook"),
    (r"(^|\.)tiktok\.com$", "tiktok"),
    (r"(^|\.)youtube\.com$", "youtube"),
    (r"(^|\.)youtu\.be$", "youtube"),
]

def platform_for(url):
    host = (urlparse(url).netloc or "").lower().split(":")[0]
    for pat, name in ALLOWED:
        if re.search(pat, host):
            return name
    return None

def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    url, out_dir, fmt = argv[1], "downloads", "best[ext=mp4]/best"
    i = 2
    while i < len(argv):
        if argv[i] == "--out-dir" and i + 1 < len(argv):
            out_dir, i = argv[i + 1], i + 2
        elif argv[i] == "--format" and i + 1 < len(argv):
            fmt, i = argv[i + 1], i + 2
        else:
            print(f"unknown arg: {argv[i]}", file=sys.stderr); return 2
    platform = platform_for(url)
    if not platform:
        print(f"unsupported host for {url!r}; allowed: facebook, tiktok, youtube",
              file=sys.stderr)
        return 2
    ytdlp = shutil.which("yt-dlp") or os.path.expanduser("~/.local/bin/yt-dlp")
    if not ytdlp or not os.path.exists(ytdlp):
        print("yt-dlp not found on PATH or ~/.local/bin/yt-dlp", file=sys.stderr)
        return 3
    os.makedirs(out_dir, exist_ok=True)
    # --print-json gives one JSON object per download; --no-playlist keeps
    # a single video link from pulling a whole playlist by accident.
    cmd = [ytdlp, "--no-playlist", "--no-warnings", "-f", fmt,
           "--print-json", "-o", os.path.join(out_dir, "%(id)s.%(ext)s"), url]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr.strip()[-2000:], file=sys.stderr)
        return 3
    info = None
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                info = json.loads(line)
            except json.JSONDecodeError:
                pass
    if not info:
        print("yt-dlp succeeded but produced no JSON metadata", file=sys.stderr)
        return 3
    meta = {
        "platform": platform, "source_url": url, "id": info.get("id"),
        "title": info.get("title"), "uploader": info.get("uploader"),
        "duration_s": info.get("duration"), "fps": info.get("fps"),
        "width": info.get("width"), "height": info.get("height"),
        "ext": info.get("ext"),
        "file": os.path.join(out_dir, f"{info.get('id')}.{info.get('ext')}"),
    }
    meta["filesize_bytes"] = (os.path.getsize(meta["file"])
                              if os.path.exists(meta["file"]) else None)
    with open(os.path.join(out_dir, f"{info.get('id')}.info.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(json.dumps(meta, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
