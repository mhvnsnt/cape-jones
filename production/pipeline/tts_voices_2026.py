#!/usr/bin/env python3
"""Supplemental TTS dispatcher: 2026-era engines not yet in tts_voices.py.

Same conventions as tts_voices.py: dry-run by default (prints the exact
command it WOULD run), --run executes, --list shows availability.
Weights live on Kaggle/GPU boxes, never local.

Engines (all commercial-use cleared):
  pocket-tts   MIT code / CC-BY-4.0 weights -- Kyutai 100M, CPU-recommended
  orpheus-tts  Apache-2.0 -- Llama-3b backbone, emotion tags, ~200ms stream
  moss-tts     Apache-2.0 -- 8B flagship + 100M Nano (CPU), dialogue + SFX
  neutts       NeuTTS Open License v1.0 -- commercial OK under $5M/yr revenue
  luxtts       Apache-2.0 -- zipvoice-based, 150x realtime, 48kHz, cloning
  omnivoice    Apache-2.0 -- 600+ langs (DOC-ONLY: clone when disk allows)
"""
import argparse, os, shutil, subprocess, sys

TOOLS = os.path.expanduser("~/workspace/tools")

ENGINES = {
    "pocket-tts": {
        "dir": "pocket-tts", "check": None,
        "cmd": lambda t, o, v: (
            f"cd {TOOLS}/pocket-tts && python -c \"from pocket_tts import TTSModel; "
            f"m=TTSModel.load_model(); m.generate_audio('{t}', '{o}')\""),
        "needs": "HF kyutai/pocket-tts weights (~400MB, CC-BY-4.0, gated)",
    },
    "orpheus-tts": {
        "dir": "orpheus-tts", "check": None,
        "cmd": lambda t, o, v: (
            f"cd {TOOLS}/orpheus-tts && python -m orpheus_tts.infer "
            f"--text '{t}' --voice {v or 'tara'} --output {o}"),
        "needs": "Orpheus HF weights + voice name",
    },
    "moss-tts": {
        "dir": "moss-tts", "check": None,
        "cmd": lambda t, o, v: (
            f"cd {TOOLS}/moss-tts && python inference.py --text '{t}' "
            f"--output {o} --model {v or 'OpenMOSS/MOSS-TTS-100M'}"),
        "needs": "MOSS-TTS weights (100M Nano or 8B)",
    },
    "neutts": {
        "dir": "neutts", "check": None,
        "flag": "NeuTTS Open License v1.0: commercial OK under $5M/yr revenue; paid license above",
        "cmd": lambda t, o, v: (
            f"cd {TOOLS}/neutts && python -m neutts.infer --text '{t}' "
            f"--ref_audio {v} --output {o}"),
        "needs": "NeuTTS weights + ref audio for cloning",
    },
    "luxtts": {
        "dir": "luxtts", "check": None,
        "cmd": lambda t, o, v: (
            f"cd {TOOLS}/luxtts && python infer.py --text '{t}' "
            f"--ref_audio {v} --output {o}"),
        "needs": "LuxTTS weights (HF YatharthS/LuxTTS)",
    },
    "omnivoice": {
        "dir": "omnivoice", "check": None,
        "flag": "DOC-ONLY: repo not cloned (disk ceiling); https://github.com/k2-fsa/OmniVoice",
        "cmd": lambda t, o, v: (
            f"python -c \"from omnivoice import OmniVoice; m=OmniVoice.from_pretrained('k2-fsa/OmniVoice'); "
            f"m.generate(text='{t}', ref_audio='{v}').save('{o}')\""),
        "needs": "OmniVoice weights (~2.45GB, Apache-2.0)",
    },
}

PRIORITY = ["pocket-tts", "luxtts", "orpheus-tts", "neutts", "moss-tts", "omnivoice"]


def available(name):
    e = ENGINES[name]
    repo = os.path.isdir(os.path.join(TOOLS, e["dir"]))
    exe = True
    if e["check"]:
        exe = shutil.which(e["check"]) is not None
    return repo, exe


def main():
    ap = argparse.ArgumentParser(description="Supplemental 2026 TTS dispatcher")
    ap.add_argument("--text", "-t", help="text to speak")
    ap.add_argument("--out", "-o", default="/tmp/tts2026_out.wav", help="output wav")
    ap.add_argument("--engine", "-e", choices=list(ENGINES), help="force engine")
    ap.add_argument("--voice", "-v", default="", help="voice/ref-audio/model path")
    ap.add_argument("--run", action="store_true", help="actually execute (default: dry-run)")
    ap.add_argument("--list", action="store_true", help="list engines + availability")
    args = ap.parse_args()

    if args.list or (not args.text and not args.engine):
        print(f"{'engine':14} {'repo':5} {'cli':5}  notes")
        for n, e in ENGINES.items():
            repo, exe = available(n)
            flag = f"  !! {e['flag']}" if "flag" in e else ""
            print(f"{n:14} {'Y' if repo else '-':5} {'Y' if exe else '-':5}  {e['needs']}{flag}")
        return

    order = [args.engine] if args.engine else PRIORITY
    for name in order:
        repo, exe = available(name)
        if not repo:
            continue
        e = ENGINES[name]
        cmd = e["cmd"](args.text or "test", args.out, args.voice)
        print(f"[tts_voices_2026] engine={name} repo={'ok' if repo else 'missing'}")
        if "flag" in e:
            print(f"[tts_voices_2026] LICENSE FLAG: {e['flag']}")
        print(f"[tts_voices_2026] cmd: {cmd}")
        if args.run:
            r = subprocess.run(cmd, shell=True)
            sys.exit(r.returncode)
        else:
            print("[tts_voices_2026] dry-run only (use --run to execute)")
        return
    print("[tts_voices_2026] no engine repo found under ~/workspace/tools/")


if __name__ == "__main__":
    main()
