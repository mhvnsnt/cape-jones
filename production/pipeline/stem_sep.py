#!/usr/bin/env python3
"""Unified stem separation dispatcher.

  demucs   MIT  4-stem (vocals/drums/bass/other), hybrid transformer
  uvr5     MIT  Ultimate Vocal Remover GUI code (MDX-Net variants etc.)

Use: pull acapellas for remixes, isolate dialogue from music beds,
karaoke versions of songs, clean stems for mixing.
"""
import argparse, os, subprocess, sys

TOOLS = os.path.expanduser("~/workspace/tools")

ENGINES = {
    "demucs": {
        "dir": "demucs",
        "cmd": lambda i, o: f"cd {TOOLS}/demucs && python -m demucs --two-stems=vocals -o {o} {i} # 4-stem default; --mp3 for mp3 out",
    },
    "uvr5": {
        "dir": "uvr5",
        "cmd": lambda i, o: f"cd {TOOLS}/uvr5 && python gui.py # GUI; CLI via separate_uvr.py in newer builds",
    },
}


def main():
    ap = argparse.ArgumentParser(description="Stem separation dispatcher")
    ap.add_argument("--input", "-i", default="")
    ap.add_argument("--out", "-o", default="/tmp/stems")
    ap.add_argument("--engine", "-e", choices=list(ENGINES))
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list or (not args.input and not args.engine):
        for n, e in ENGINES.items():
            repo = os.path.isdir(os.path.join(TOOLS, e["dir"]))
            print(f"{n:10} {'Y' if repo else '-':5}")
        return
    order = [args.engine] if args.engine else list(ENGINES)
    for name in order:
        e = ENGINES[name]
        if not os.path.isdir(os.path.join(TOOLS, e["dir"])):
            continue
        cmd = e["cmd"](args.input, args.out)
        print(f"[stem_sep] engine={name}\n[stem_sep] cmd: {cmd}")
        if args.run:
            sys.exit(subprocess.run(cmd, shell=True).returncode)
        print("[stem_sep] dry-run only (use --run)")
        return
    print("[stem_sep] no engine repo found")


if __name__ == "__main__":
    main()
