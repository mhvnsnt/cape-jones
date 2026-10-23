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
  3. F5-TTS    (SWivid/F5-TTS, MIT) — fast zero-shot TTS, bulk ADR/dubbing
  4. CosyVoice3 (FunAudioLLM, Apache-2.0) — cross-lingual clone (EN<->JA),
                                       instruction emotion ("say it angry")
  5. Kokoro    (tools/kokoro-venv)  — CPU-fast, 82M params
  6. Bark      (suno-ai/bark)       — non-verbal sounds (laughs, sighs)
  7. espeak-ng (system fallback)    — always works, robotic temp track

Owner law: Chatterbox stays the character-voice default; F5-TTS/CosyVoice3 complement it.

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
        "f5tts": _has_module("f5_tts"),          # pip install f5-tts (MIT)
        "cosyvoice": _has_module("cosyvoice"),   # FunAudioLLM/CosyVoice (Apache-2.0)
        "kokoro": os.path.isdir(os.path.join(TOOLS, "kokoro-venv")),
        "bark": os.path.isdir(os.path.join(TOOLS, "bark")),
        "espeak": shutil.which("espeak-ng") is not None,
    }
    return checks.get(name, False)


def _has_module(mod):
    import importlib.util
    return importlib.util.find_spec(mod) is not None


ENGINES = ["dia2", "chatterbox", "f5tts", "cosyvoice", "kokoro", "bark", "espeak"]


def list_engines():
    print("TTS engines (availability on this machine):")
    for e in ENGINES:
        mark = "OK " if engine_available(e) else " -- "
        print(f"  [{mark}] {e}")


def pick_engine(preferred):
    order = ENGINES
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
                    choices=["auto"] + ENGINES,
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
        elif engine == "f5tts":
            print(f"  [{i}] f5tts: {line['line'][:40]}", file=sys.stderr)
            synth_f5tts(line, wav)
        elif engine == "cosyvoice":
            print(f"  [{i}] cosyvoice: {line['line'][:40]}", file=sys.stderr)
            synth_cosyvoice(line, wav)

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


def synth_f5tts(line, out_wav):
    """F5-TTS zero-shot (SWivid, MIT). Fast — best for bulk ADR/dubbing.

    Needs a reference clip: line["ref_audio"] + line["ref_text"].
    Model F5TTS_v1_Base downloads from HF on first use.
    """
    ref_audio = line.get("ref_audio")
    ref_text = line.get("ref_text", "")
    if not ref_audio:
        sys.exit("ERROR: f5tts needs line['ref_audio'] (+ line['ref_text']) "
                 "for zero-shot cloning")
    code = (
        "from f5_tts.api import F5TTS; "
        "f5 = F5TTS(); "
        f"f5.infer(ref_file={ref_audio!r}, ref_text={ref_text!r}, "
        f"gen_text={line['line']!r}, file_wave={out_wav!r})"
    )
    r = subprocess.run([sys.executable, "-c", code],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ERROR: f5tts failed:\n{r.stderr[-800:]}")


def synth_cosyvoice(line, out_wav):
    """CosyVoice3 zero-shot / instruct (FunAudioLLM, Apache-2.0).

    line["ref_audio"] + line["ref_text"]: zero-shot clone (cross-lingual OK).
    line["instruct"]: natural-language direction, e.g. "say it angry, fast"
        (uses inference_instruct2). Model dir: FunAudioLLM/Fun-CosyVoice3-0.5B-2512
        (download once from HF/ModelScope to pretrained_models/).
    """
    import soundfile as sf
    from cosyvoice.cli.cosyvoice import CosyVoice3
    model_dir = os.environ.get("COSYVOICE3_MODEL",
                               "pretrained_models/Fun-CosyVoice3-0.5B-2512")
    if not os.path.isdir(model_dir):
        sys.exit(f"ERROR: CosyVoice3 model not found at {model_dir}. "
                 "Download FunAudioLLM/Fun-CosyVoice3-0.5B-2512 first "
                 "(or set COSYVOICE3_MODEL).")
    cv = CosyVoice3(model_dir, load_jit=False, load_trt=False, fp16=True)
    ref_audio = line.get("ref_audio")
    ref_text = line.get("ref_text", "")
    instruct = line.get("instruct")
    if instruct and ref_audio:
        out = cv.inference_instruct2(line["line"], instruct, ref_audio, stream=False)
    elif ref_audio:
        out = cv.inference_zero_shot(line["line"], ref_text, ref_audio, stream=False)
    else:
        sys.exit("ERROR: cosyvoice needs line['ref_audio'] (+ line['ref_text'])")
    audio = out["tts_speech"].numpy().flatten()
    sf.write(out_wav, audio, cv.sample_rate)


if __name__ == "__main__":
    main()