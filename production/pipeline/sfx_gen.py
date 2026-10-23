#!/usr/bin/env python3
"""Unified text->SFX / foley generation dispatcher.

  stable-audio  MIT code / Community License weights -- best prompt SFX
  mmaudio       (already in tools/MMAudio) -- video->SFX
  audiogen      (already in tools/audiocraft) -- research-only weights; fallback

Foley helpers: record real props -> process with pedalboard FX chain.
"""
import argparse, os, subprocess, sys

TOOLS = os.path.expanduser("~/workspace/tools")

ENGINES = {
    "stable-audio": {
        "dir": "stable-audio", "flag": "weights gated; Stability Community License (commercial OK under $1M/yr)",
        "cmd": lambda p, o: f"cd {TOOLS}/stable-audio && python scripts/generate_sfx.py --prompt '{p}' --out {o} # see repo inference scripts",
    },
    "mmaudio": {
        "dir": "MMAudio",
        "cmd": lambda p, o: f"cd {TOOLS}/MMAudio && python app.py --video <input.mp4> --prompt '{p}' --out {o} # video-conditioned SFX",
    },
}


def main():
    ap = argparse.ArgumentParser(description="Unified SFX generation dispatcher")
    ap.add_argument("--prompt", "-p", default="", help="e.g. 'cartoon punch whoosh, comedic'")
    ap.add_argument("--out", "-o", default="/tmp/sfx_out.wav")
    ap.add_argument("--engine", "-e", choices=list(ENGINES))
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list or not args.prompt:
        for n, e in ENGINES.items():
            repo = os.path.isdir(os.path.join(TOOLS, e["dir"]))
            flag = f"  !! {e['flag']}" if "flag" in e else ""
            print(f"{n:14} {'Y' if repo else '-':5}{flag}")
        return
    order = [args.engine] if args.engine else list(ENGINES)
    for name in order:
        e = ENGINES[name]
        if not os.path.isdir(os.path.join(TOOLS, e["dir"])):
            continue
        cmd = e["cmd"](args.prompt, args.out)
        print(f"[sfx_gen] engine={name}")
        if "flag" in e:
            print(f"[sfx_gen] LICENSE FLAG: {e['flag']}")
        print(f"[sfx_gen] cmd: {cmd}")
        if args.run:
            sys.exit(subprocess.run(cmd, shell=True).returncode)
        print("[sfx_gen] dry-run only (use --run)")
        return
    print("[sfx_gen] no engine repo found")


if __name__ == "__main__":
    main()
