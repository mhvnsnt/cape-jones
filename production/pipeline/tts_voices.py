#!/usr/bin/env python3
"""Unified TTS voice dispatcher for the animation audio pipeline.

Tries engines in priority order (fastest/cheapest first). Weights are NOT
stored locally -- they live on Kaggle/GPU boxes; set the weight root env vars
or pass --weights. Dry-run by default: prints the exact command it WOULD run.
Use --run to execute.

Engines (all commercial-use cleared):
  piper        MIT     ONNX, fastest; great for consistent character voices
  espeak-ng    GPL-3   robot fallback, zero deps
  melotts      MIT     light multilingual (EN + 6 langs)
  matcha-tts   MIT     fast non-autoregressive, pairs with CosyVoice
  styletts2    MIT     style/emotion control
  tortoise     Apache  voice cloning from 3-6s reference, slow but expressive
  f5-tts       MIT*    zero-shot cloning (*weights CC-BY-NC -- flagged)
  gpt-sovits   MIT     singing-capable voice cloning
  cosyvoice    Apache  zero-shot multilingual cloning (Alibaba)
  qwen3-tts    Apache  2026 model, 10 langs, Apache code+weights
  higgs-audio  Apache  conversational multi-speaker (dialogue scenes)
  step-audio   Apache  multilingual, instruction-led vocalization
  sesame-csm   Apache  conversational speech model (Sesame CSM-1B)
  whisperspeech MIT    expressive long-form (Collabora)
  vall-e-x     MIT     cross-lingual voice cloning
  bark         Apache  (already in tools/bark) -- laughter, sighs, non-speech
  kokoro       Apache  (already in tools) -- fast narration
  chatterbox   MIT     (already in tools) -- watermarked clone
  parler-tts   Apache  (already in tools) -- style prompts
  dia          Apache  (already in tools) -- dialogue
  openvoice    MIT     (already in tools) -- tone conversion
"""
import argparse, os, shutil, subprocess, sys

TOOLS = os.path.expanduser("~/workspace/tools")
WROOT = os.environ.get("TTS_WEIGHTS", os.path.join(TOOLS, "post-pipeline", "models"))

ENGINES = {
    "piper": {
        "dir": "piper", "check": "piper-tts",
        "cmd": lambda t, o, v: f"piper-tts --model {v} --output_file {o} --text '{t}'",
        "needs": "onnx voice file (.onnx + .onnx.json)",
    },
    "espeak-ng": {
        "dir": "espeak-ng", "check": "espeak-ng",
        "cmd": lambda t, o, v: f"espeak-ng -v {v or 'en-us'} -w {o} '{t}'",
        "needs": "nothing (system voices)",
    },
    "kitten-tts": {
        "dir": "kitten-tts", "check": None, "flag": "code Apache-2.0; v2 models under Stellon Labs Community License -- check model terms",
        "cmd": lambda t, o, v: f"cd {TOOLS}/kitten-tts && python -c \"from kittentts import KittenTTS; m=KittenTTS(); m.generate('{t}', '{o}')\"",
        "needs": "KittenTTS model (<25MB, CPU)",
    },
    "melotts": {
        "dir": "melotts", "check": "melotts",
        "cmd": lambda t, o, v: f"python -m melo.api '{t}' --output_path {o} --language {v or 'EN'}",
        "needs": "MeloTTS HF weights",
    },
    "matcha-tts": {
        "dir": "matcha-tts", "check": None,
        "cmd": lambda t, o, v: f"cd {TOOLS}/matcha-tts && python matcha/cli.py --text '{t}' --output_folder {os.path.dirname(o)}",
        "needs": "Matcha-TTS checkpoint",
    },
    "styletts2": {
        "dir": "StyleTTS2", "check": None,
        "cmd": lambda t, o, v: f"cd {TOOLS}/StyleTTS2 && python inference.py --text '{t}' --output_wav {o}",
        "needs": "StyleTTS2 checkpoint",
    },
    "tortoise": {
        "dir": "tortoise-tts", "check": None,
        "cmd": lambda t, o, v: f"cd {TOOLS}/tortoise-tts && python tortoise/do_tts.py --text '{t}' --voice {v or 'random'} --output_path {o}",
        "needs": "Tortoise HF weights + voice sample dir",
    },
    "f5-tts": {
        "dir": "f5-tts", "check": None, "flag": "WEIGHTS CC-BY-NC -- non-commercial only",
        "cmd": lambda t, o, v: f"cd {TOOLS}/f5-tts && python inference-cli.py --text '{t}' --ref_audio {v} --output {o}",
        "needs": "F5-TTS checkpoint (CC-BY-NC)",
    },
    "gpt-sovits": {
        "dir": "gpt-sovits", "check": None,
        "cmd": lambda t, o, v: f"cd {TOOLS}/gpt-sovits && python tools/infer_cli.py --text '{t}' --output {o}",
        "needs": "GPT-SoVITS v4 checkpoints + ref audio",
    },
    "cosyvoice": {
        "dir": "cosyvoice", "check": None,
        "cmd": lambda t, o, v: f"cd {TOOLS}/cosyvoice && python -c \"from cosyvoice.cli.cosyvoice import AutoModel\" # see cosyvoice/ for zero_shot API",
        "needs": "CosyVoice2-0.5B (Apache) + Matcha-TTS submodule",
    },
    "qwen3-tts": {
        "dir": "qwen3-tts", "check": None,
        "cmd": lambda t, o, v: f"cd {TOOLS}/qwen3-tts && python run.py --text '{t}' --out {o}",
        "needs": "Qwen3-TTS HF weights (Apache)",
    },
    "higgs-audio": {
        "dir": "higgs-audio", "check": None,
        "cmd": lambda t, o, v: f"cd {TOOLS}/higgs-audio && python examples/generation.py --text '{t}' --out {o}",
        "needs": "Higgs Audio v2 HF weights (Apache)",
    },
    "step-audio": {
        "dir": "step-audio", "check": None,
        "cmd": lambda t, o, v: f"cd {TOOLS}/step-audio && python app.py --text '{t}' # see repo for CLI",
        "needs": "Step-Audio HF weights (Apache)",
    },
    "sesame-csm": {
        "dir": "sesame-csm", "check": None,
        "cmd": lambda t, o, v: f"cd {TOOLS}/sesame-csm && python -c \"from generator import load_csm_1b\" # see repo",
        "needs": "CSM-1B HF weights (Apache)",
    },
    "whisperspeech": {
        "dir": "whisperspeech", "check": None,
        "cmd": lambda t, o, v: f"cd {TOOLS}/whisperspeech && python -c \"import whisperspeech\" # see notebooks",
        "needs": "WhisperSpeech HF weights (MIT)",
    },
    "vall-e-x": {
        "dir": "vall-e-x", "check": None,
        "cmd": lambda t, o, v: f"cd {TOOLS}/vall-e-x && python utils/generation.py --text '{t}'",
        "needs": "VALL-E-X checkpoint + ref audio",
    },
}

PRIORITY = ["piper", "kokoro", "melotts", "espeak-ng"]  # fast ones first


def available(name):
    e = ENGINES[name]
    repo = os.path.isdir(os.path.join(TOOLS, e["dir"]))
    exe = True
    if e["check"]:
        exe = shutil.which(e["check"]) is not None
    return repo, exe


def main():
    ap = argparse.ArgumentParser(description="Unified TTS dispatcher")
    ap.add_argument("--text", "-t", help="text to speak")
    ap.add_argument("--out", "-o", default="/tmp/tts_out.wav", help="output wav")
    ap.add_argument("--engine", "-e", choices=list(ENGINES), help="force engine")
    ap.add_argument("--voice", "-v", default="", help="voice/ref-audio/onnx model path")
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

    order = [args.engine] if args.engine else PRIORITY + [n for n in ENGINES if n not in PRIORITY]
    for name in order:
        repo, exe = available(name)
        if not repo:
            continue
        e = ENGINES[name]
        cmd = e["cmd"](args.text or "test", args.out, args.voice)
        print(f"[tts_voices] engine={name} repo={'ok' if repo else 'missing'} cli={'ok' if exe else 'missing'}")
        if "flag" in e:
            print(f"[tts_voices] LICENSE FLAG: {e['flag']}")
        print(f"[tts_voices] cmd: {cmd}")
        if args.run:
            r = subprocess.run(cmd, shell=True)
            sys.exit(r.returncode)
        else:
            print("[tts_voices] dry-run only (use --run to execute)")
        return
    print("[tts_voices] no engine repo found under ~/workspace/tools/")


if __name__ == "__main__":
    main()
