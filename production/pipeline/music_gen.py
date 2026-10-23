#!/usr/bin/env python3
"""Unified music/song generation dispatcher.

Weights live on Kaggle/GPU -- nothing heavy runs here. Dry-run prints the
exact command for the target box.

Engines (all commercial-use cleared):
  ace-step      Apache  lyrics->full song, voice+accompaniment, fast
  diffrhythm    Apache  full-length song gen, latent diffusion (v1 + v2)
  songgen       Apache  single-stage AR text->song, mixed/dual-track modes
  yue           Apache* lyrics->song dual-track (*weights CC-BY-NC + individual
                        creator permission: monetization OK for individual
                        creators; companies need a license)
  stable-audio  MIT*    text->audio/SFX (weights: Stability Community License,
                        free commercial under $1M/yr revenue)
  magenta       Apache  melody/drum continuation, style helpers (compositional)
  musicgen      (already in tools/audiocraft) -- research-only weights; prefer ACE-Step
"""
import argparse, os, shutil, subprocess, sys

TOOLS = os.path.expanduser("~/workspace/tools")

ENGINES = {
    "ace-step": {
        "dir": "ace-step",
        "cmd": lambda p, o, extra: f"cd {TOOLS}/ace-step && python acestep/pipeline_ace_step.py --prompt '{p}' --lyrics '{extra.get('lyrics','')}' --audio_path {o}",
        "needs": "ACE-Step HF weights (Apache)",
    },
    "diffrhythm": {
        "dir": "diffrhythm",
        "cmd": lambda p, o, extra: f"cd {TOOLS}/diffrhythm && bash scripts/infer_prompt_ref.sh # lyrics-lrc in infer/example; style prompt: '{p}'",
        "needs": "DiffRhythm HF weights (Apache), --chunked on 8GB VRAM",
    },
    "songgen": {
        "dir": "songgen",
        "cmd": lambda p, o, extra: f"cd {TOOLS}/songgen && python inference.py --text_prompt '{p}' --lyrics '{extra.get('lyrics','')}' --output {o} --mode {extra.get('mode','mixed')}",
        "needs": "SongGen HF weights + XCodec ckpt (Apache)",
    },
    "yue": {
        "dir": "yue", "flag": "WEIGHTS CC-BY-NC 4.0 + creator permission: individual creators MAY monetize; companies need license",
        "cmd": lambda p, o, extra: f"cd {TOOLS}/yue && python infer.py --lyrics '{extra.get('lyrics','')}' --genre '{p}' --output {o}",
        "needs": "YuE/YuE2 HF weights",
    },
    "stable-audio": {
        "dir": "stable-audio", "flag": "weights gated; Stability Community License (commercial OK under $1M/yr)",
        "cmd": lambda p, o, extra: f"cd {TOOLS}/stable-audio && python -c \"from stable_audio_tools import get_pretrained_model\" # see repo; prompt='{p}' dur={extra.get('dur','47s')}",
        "needs": "stabilityai/stable-audio-open-1.0 (gated HF)",
    },
    "magenta": {
        "dir": "magenta",
        "cmd": lambda p, o, extra: f"cd {TOOLS}/magenta && python magenta/models/melody_rnn/melody_rnn_generate.py # primer melody continuation -> MIDI",
        "needs": "Magenta bundles (Apache); render MIDI with soundfont",
    },
}


def main():
    ap = argparse.ArgumentParser(description="Unified music generation dispatcher")
    ap.add_argument("--prompt", "-p", default="", help="style/genre prompt")
    ap.add_argument("--lyrics", "-l", default="", help="lyrics (song engines)")
    ap.add_argument("--out", "-o", default="/tmp/music_out.wav")
    ap.add_argument("--engine", "-e", choices=list(ENGINES))
    ap.add_argument("--mode", default="mixed", help="songgen mixed|dual")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.list or (not args.prompt and not args.lyrics and not args.engine):
        for n, e in ENGINES.items():
            repo = os.path.isdir(os.path.join(TOOLS, e["dir"]))
            flag = f"  !! {e['flag']}" if "flag" in e else ""
            print(f"{n:14} {'Y' if repo else '-':5}  {e['needs']}{flag}")
        return

    order = [args.engine] if args.engine else list(ENGINES)
    for name in order:
        e = ENGINES[name]
        if not os.path.isdir(os.path.join(TOOLS, e["dir"])):
            continue
        extra = {"lyrics": args.lyrics, "mode": args.mode}
        cmd = e["cmd"](args.prompt, args.out, extra)
        print(f"[music_gen] engine={name}")
        if "flag" in e:
            print(f"[music_gen] LICENSE FLAG: {e['flag']}")
        print(f"[music_gen] cmd: {cmd}")
        if args.run:
            sys.exit(subprocess.run(cmd, shell=True).returncode)
        print("[music_gen] dry-run only (use --run)")
        return
    print("[music_gen] no engine repo found")


if __name__ == "__main__":
    main()
