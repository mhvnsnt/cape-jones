#!/usr/bin/env python3
"""
dialogue_pipeline.py — script-to-speaking-character pipeline.

Takes a dialogue script and produces:
  1. Per-line WAV audio via the best available TTS engine
  2. Timing/viseme data for lip sync

The script format (JSON):
  [
    {"character": "CAPE JONES", "voice": "deep-hero", "emotion": "bored",
     "line": "What the fuck, man?"},
    {"character": "NARRATOR", "voice": "narrator", "emotion": "deadpan",
     "line": "Meanwhile, at the beach."}
  ]

TTS engine priority (first available wins):
  1. Dia2      (nari-labs/Dia)      — multi-speaker dialogue, [S1]/[S2] tags, emotion
  2. Chatterbox (already in tools/) — voice cloning + emotion, 23 languages
  3. Kokoro    (tools/kokoro-venv)  — CPU-fast, 82M params
  4. Bark      (suno-ai/bark)       — non-verbal sounds (laughs, sighs)
  5. espeak-ng (system fallback)    — always works, robotic temp track

Lip sync handoff:
  - writes per-line timing JSON compatible with tools/lipsync/
  - OpenFaceFX / Rhubarb consume the WAV + transcript -> visemes

Usage:
  python3 dialogue_pipeline.py script.json out_dir/ --engine auto
  python3 dialogue_pipeline.py script.json out_dir/ --engine chatterbox
  python3 dialogue_pipeline.py script.json out_dir/ --list-engines

GPU note: Dia2/Chatterbox/Bark want GPU (Kaggle T4). Kokoro + espeak run on CPU.
For full-quality dialogue, run this on Kaggle with --engine dia2.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

TOOLS = os.path.expanduser("~/workspace/tools")


def engine_available(name):
    checks = {
        "dia2": os.path.isdir(os.path.join(TOOLS, "Dia")),
        "chatterbox": os.path.isdir(os.path.join(TOOLS, "chatterbox")),
        "kokoro": os.path.isdir(os.path.join(TOOLS, "kokoro-venv")),
        "bark": os.path.isdir(os.path.join(TOOLS, "bark")),
        "espeak": shutil.which("espeak-ng") is not None,
    }
    return checks.get(name, False)


def list_engines():
    print("TTS engines (availability on this machine):")
    for e in ["dia2", "chatterbox", "kokoro", "bark", "espeak"]:
        mark = "OK " if engine_available(e) else " -- "
        print(f"  [{mark}] {e}")


def pick_engine(preferred):
    order = ["dia2", "chatterbox", "kokoro", "bark", "espeak"]
    if preferred != "auto":
        if not engine_available(preferred):
            sys.exit(f"ERROR: engine '{preferred}' not available. "
                     f"Use --list-engines.")
        return preferred
    for e in order:
        if engine_available(e):
            return e
    sys.exit("ERROR: no TTS engine available (install espeak-ng at minimum)")


def synth_espeak(line, out_wav, voice="en", speed=175):
    subprocess.run(
        ["espeak-ng", "-v", voice, "-s", str(speed), "-w", out_wav, line["line"]],
        check=True, capture_output=True)
    return out_wav


def get_duration(wav):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", wav],
        capture_output=True, text=True)
    return float(out.stdout.strip())


def main():
    ap = argparse.ArgumentParser(description="dialogue script -> voiced lines")
    ap.add_argument("script", nargs="?", help="dialogue JSON file")
    ap.add_argument("out_dir", nargs="?", help="output directory for wavs + timing")
    ap.add_argument("--engine", default="auto",
                    choices=["auto", "dia2", "chatterbox", "kokoro", "bark", "espeak"],
                    help="TTS engine (default: auto = best available)")
    ap.add_argument("--list-engines", action="store_true")
    ns = ap.parse_args()

    if ns.list_engines:
        list_engines()
        return

    if not ns.script or not ns.out_dir:
        ap.error("script and out_dir required (unless --list-engines)")

    with open(ns.script) as f:
        lines = json.load(f)
    os.makedirs(ns.out_dir, exist_ok=True)

    engine = pick_engine(ns.engine)
    print(f"engine: {engine}", file=sys.stderr)

    timing = []
    t = 0.0
    for i, line in enumerate(lines):
        wav = os.path.join(ns.out_dir, f"line_{i:03d}.wav")

        if engine == "espeak":
            synth_espeak(line, wav)
        elif engine == "kokoro":
            # kokoro-venv inference (torch required)
            print(f"  [{i}] kokoro: {line['line'][:40]}", file=sys.stderr)
            synth_kokoro(line, wav)
        elif engine == "chatterbox":
            print(f"  [{i}] chatterbox: {line['line'][:40]}", file=sys.stderr)
            synth_chatterbox(line, wav)
        elif engine == "dia2":
            print(f"  [{i}] dia2: {line['line'][:40]}", file=sys.stderr)
            synth_dia2(line, wav)
        elif engine == "bark":
            print(f"  [{i}] bark: {line['line'][:40]}", file=sys.stderr)
            synth_bark(line, wav)

        dur = get_duration(wav)
        timing.append({
            "index": i,
            "character": line.get("character", ""),
            "voice": line.get("voice", ""),
            "emotion": line.get("emotion", ""),
            "line": line["line"],
            "wav": os.path.basename(wav),
            "start": round(t, 3),
            "duration": round(dur, 3),
        })
        t += dur + 0.25  # 250ms gap between lines

    timing_path = os.path.join(ns.out_dir, "timing.json")
    with open(timing_path, "w") as f:
        json.dump(timing, f, indent=2)
    print(f"wrote {len(lines)} lines + timing.json -> {ns.out_dir}")
    print(f"total dialogue: {t:.1f}s")
    print("next: feed wavs + timing.json to tools/lipsync/ for visemes")


def synth_kokoro(line, out_wav):
    """Kokoro TTS via the kokoro-venv."""
    code = (
        "import sys, soundfile as sf; "
        "from kokoro import KPipeline; "
        f"pipe = KPipeline(lang_code='a'); "
        f"gen = pipe({line['line']!r}, voice={line.get('voice','af_heart')!r}); "
        "audio = next(gen)[2]; "
        f"sf.write({out_wav!r}, audio, 24000)"
    )
    venv_py = os.path.join(TOOLS, "kokoro-venv", "bin", "python")
    r = subprocess.run([venv_py, "-c", code], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ERROR: kokoro failed:\n{r.stderr[-800:]}")


def synth_chatterbox(line, out_wav):
    """Chatterbox TTS (Resemble AI, MIT). GPU recommended."""
    code = (
        "import torchaudio; "
        "from chatterbox.tts import ChatterboxTTS; "
        "model = ChatterboxTTS.from_pretrained(device='cuda'); "
        f"wav = model.generate({line['line']!r}); "
        f"torchaudio.save({out_wav!r}, wav, model.sr)"
    )
    r = subprocess.run([sys.executable, "-c", code],
                       capture_output=True, text=True,
                       cwd=os.path.join(TOOLS, "chatterbox"))
    if r.returncode != 0:
        sys.exit(f"ERROR: chatterbox failed:\n{r.stderr[-800:]}")


def synth_dia2(line, out_wav):
    """Dia2 dialogue TTS (Nari Labs, Apache-2.0). GPU required."""
    spk = line.get("speaker_tag", "[S1]")
    text = f"{spk} {line['line']}"
    code = (
        "import soundfile as sf; "
        "from dia.model import Dia; "
        "model = Dia.from_pretrained('nari-labs/Dia-1.6B-0626'); "
        f"out = model.generate({text!r}); "
        f"sf.write({out_wav!r}, out, 44100)"
    )
    r = subprocess.run([sys.executable, "-c", code],
                       capture_output=True, text=True,
                       cwd=os.path.join(TOOLS, "Dia"))
    if r.returncode != 0:
        sys.exit(f"ERROR: dia2 failed:\n{r.stderr[-800:]}")


def synth_bark(line, out_wav):
    """Bark TTS (suno-ai, MIT). Good for non-verbal sounds."""
    code = (
        "import numpy as np; from scipy.io.wavfile import write as wav_write; "
        "from bark import SAMPLE_RATE, generate_audio, preload_models; "
        "preload_models(); "
        f"audio = generate_audio({line['line']!r}); "
        f"wav_write({out_wav!r}, SAMPLE_RATE, (audio*32767).astype(np.int16))"
    )
    r = subprocess.run([sys.executable, "-c", code],
                       capture_output=True, text=True,
                       cwd=os.path.join(TOOLS, "bark"))
    if r.returncode != 0:
        sys.exit(f"ERROR: bark failed:\n{r.stderr[-800:]}")


if __name__ == "__main__":
    main()
