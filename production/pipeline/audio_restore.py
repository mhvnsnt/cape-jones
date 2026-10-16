#!/usr/bin/env python3
"""Unified audio restoration / enhancement dispatcher.

  deepfilternet    Apache/MIT  real-time noise suppression (denoise speech)
  voicefixer       MIT         speech restoration (denoise+dereverb+declip+upscale)
  resemble-enhance MIT         neural speech enhancement (Resemble AI)

Also: loudness for broadcast -- use ffmpeg loudnorm:
  ffmpeg -i in.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 out.wav
"""
import argparse, os, subprocess, sys

TOOLS = os.path.expanduser("~/workspace/tools")

ENGINES = {
    "deepfilternet": {
        "dir": "deepfilternet",
        "cmd": lambda i, o: f"cd {TOOLS}/deepfilternet && cargo run --release -- --noisy-audio {i} --output {o} # or pip deepfilternet",
    },
    "voicefixer": {
        "dir": "voicefixer",
        "cmd": lambda i, o: f"cd {TOOLS}/voicefixer && python -c \"from voicefixer import VoiceFixer; VoiceFixer().restore(input='{i}', output='{o}', cuda=False)\"",
    },
    "resemble-enhance": {
        "dir": "resemble-enhance",
        "cmd": lambda i, o: f"cd {TOOLS}/resemble-enhance && python inference.py --input {i} --output {o} # see repo",
    },
    "loudnorm": {
        "dir": None,
        "cmd": lambda i, o: f"ffmpeg -y -i {i} -af loudnorm=I=-16:TP=-1.5:LRA=11 {o}",
    },
}


def main():
    ap = argparse.ArgumentParser(description="Audio restoration dispatcher")
    ap.add_argument("--input", "-i", default="")
    ap.add_argument("--out", "-o", default="/tmp/restored.wav")
    ap.add_argument("--engine", "-e", choices=list(ENGINES))
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list or (not args.input and not args.engine):
        for n, e in ENGINES.items():
            ok = True if e["dir"] is None else os.path.isdir(os.path.join(TOOLS, e["dir"]))
            print(f"{n:16} {'Y' if ok else '-':5}")
        print("\nloudnorm = broadcast loudness via ffmpeg (no repo needed)")
        return
    order = [args.engine] if args.engine else list(ENGINES)
    for name in order:
        e = ENGINES[name]
        if e["dir"] and not os.path.isdir(os.path.join(TOOLS, e["dir"])):
            continue
        cmd = e["cmd"](args.input, args.out)
        print(f"[audio_restore] engine={name}\n[audio_restore] cmd: {cmd}")
        if args.run:
            sys.exit(subprocess.run(cmd, shell=True).returncode)
        print("[audio_restore] dry-run only (use --run)")
        return
    print("[audio_restore] no engine repo found")


if __name__ == "__main__":
    main()
