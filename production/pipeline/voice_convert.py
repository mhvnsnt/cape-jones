#!/usr/bin/env python3
"""Unified voice conversion / singing synthesis dispatcher.

  rvc            MIT   retrieval-based VC (community fork RVC-Project)
  so-vits-svc    AGPL  singing VC (branch 4.1-Stable)
  seed-vc        GPL-3 VC (Plachtaa)
  gpt-sovits     MIT   VC + singing, v4
  openvoice      MIT   (already in tools/OpenVoice) tone-color conversion
  diffsinger     Apache singing voice synthesis (score->vocals)
"""
import argparse, os, subprocess, sys

TOOLS = os.path.expanduser("~/workspace/tools")

ENGINES = {
    "rvc": {
        "dir": "rvc",
        "cmd": lambda i, o, v: f"cd {TOOLS}/rvc && python infer/cli.py --input_path {i} --model_path {v} --output_path {o} # see infer/cli.py --help; web UI: webui.py",
    },
    "so-vits-svc": {
        "dir": "so-vits-svc",
        "cmd": lambda i, o, v: f"cd {TOOLS}/so-vits-svc && python inference_main.py -m {v} -c configs/config.json -n {i} -o {o}",
    },
    "seed-vc": {
        "dir": "seed-vc",
        "cmd": lambda i, o, v: f"cd {TOOLS}/seed-vc && python inference.py --source {i} --target {v} --output {o} # see repo",
    },
    "gpt-sovits": {
        "dir": "gpt-sovits",
        "cmd": lambda i, o, v: f"cd {TOOLS}/gpt-sovits && python tools/infer_cli.py --input {i} --ref {v} --output {o} # VC mode",
    },
    "diffsinger": {
        "dir": "diffsinger",
        "cmd": lambda i, o, v: f"cd {TOOLS}/diffsinger && python inference/ds_infer.py --ds {i} --out {o} # .ds score file in, vocals out",
    },
}


def main():
    ap = argparse.ArgumentParser(description="Unified voice conversion dispatcher")
    ap.add_argument("--input", "-i", default="", help="source audio (or .ds score for diffsinger)")
    ap.add_argument("--out", "-o", default="/tmp/vc_out.wav")
    ap.add_argument("--model", "-m", default="", help="target voice model / ref audio")
    ap.add_argument("--engine", "-e", choices=list(ENGINES))
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list or (not args.input and not args.engine):
        for n, e in ENGINES.items():
            repo = os.path.isdir(os.path.join(TOOLS, e["dir"]))
            print(f"{n:14} {'Y' if repo else '-':5}")
        return
    order = [args.engine] if args.engine else list(ENGINES)
    for name in order:
        e = ENGINES[name]
        if not os.path.isdir(os.path.join(TOOLS, e["dir"])):
            continue
        cmd = e["cmd"](args.input, args.out, args.model)
        print(f"[voice_convert] engine={name}\n[voice_convert] cmd: {cmd}")
        if args.run:
            sys.exit(subprocess.run(cmd, shell=True).returncode)
        print("[voice_convert] dry-run only (use --run)")
        return
    print("[voice_convert] no engine repo found")


if __name__ == "__main__":
    main()
