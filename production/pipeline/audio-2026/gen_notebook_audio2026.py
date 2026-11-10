#!/usr/bin/env python3
"""Generate cape_jones_audio2026_kaggle.ipynb — Kaggle T4 installer + smoke tests
for the audio-2026 pull-in (F5-TTS, CosyVoice 3, audio.cpp, DiffRhythm,
voice-changer, audio-separator, DeepFilterNet, resemble-enhance).

Pattern matches production/kaggle/gen_notebook.py: edit THIS generator, not the .ipynb.

Research: docs/research/AUDIO-VOICE-MUSIC-2026.md
Wiring: production/pipeline/audio-2026/
"""
import json

BRANCH = "audio-voice-2026"
RAW = (f"https://raw.githubusercontent.com/mhvnsnt/cape-jones/"
       f"{BRANCH}/production/pipeline/audio-2026")


def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def code(src):
    return {"cell_type": "code", "metadata": {},
            "execution_count": None, "outputs": [], "source": src}


cells = [
    md("""# Cape Jones — audio-2026 pull-in on Kaggle T4

Installs + smoke-tests the eight 2026-10-16 audio/voice/music tools
(F5-TTS, CosyVoice 3, audio.cpp, DiffRhythm, voice-changer, audio-separator,
DeepFilterNet, resemble-enhance).

**Before running:** Settings (right panel) → **Accelerator: GPU T4 x2**, **Internet: ON**.
Then **Run All**.

Owner law: **Chatterbox stays the character-voice default.** These complement it.
Research: `docs/research/AUDIO-VOICE-MUSIC-2026.md`.
"""),
    code("""# Cell 1 — GPU check
import subprocess
out = subprocess.run(["nvidia-smi", "-L"], capture_output=True, text=True)
print(out.stdout or out.stderr)
assert "Tesla T4" in out.stdout, "expected Tesla T4"
print("GPU OK")"""),
    code(f"""# Cell 2 — fetch the installer from the repo branch
import urllib.request, os
os.makedirs("/kaggle/working/audio-2026", exist_ok=True)
url = "{RAW}/kaggle_setup_audio2026.py"
dst = "/kaggle/working/audio-2026/kaggle_setup_audio2026.py"
urllib.request.urlretrieve(url, dst)
print("fetched", dst, os.path.getsize(dst), "bytes")"""),
    code("""# Cell 3 — run installer + smoke tests (model weights download on first real use, not here)
import subprocess, sys
r = subprocess.run([sys.executable, "/kaggle/working/audio-2026/kaggle_setup_audio2026.py"])
print("installer exit:", r.returncode)
assert r.returncode == 0, "installer reported failures — see output above"
print("ALL AUDIO-2026 SMOKE TESTS PASSED")"""),
    md("""## Next: real synthesis tests (weights download on first use)

Run these after the installer passes. Each downloads its model on first call.

```python
# F5-TTS zero-shot (reference clip -> cloned voice)
# f5-tts_infer-cli --model F5TTS_v1_Base --ref_audio ref.wav --ref_text "hello" \\
#     --gen_text "Cape Jones line here." --output f5_test.wav

# audio-separator: split a mix into stems
# audio-separator mix.wav --model_filename UVR-MDX-NET-Voc_FT.onnx

# DeepFilterNet: de-reverb + denoise a phone recording
# deepfilternet --noisy-audio phone_line.wav --output clean_line.wav

# resemble-enhance: neural polish
# python -m resemble_enhance.inference --input clean_line.wav --output final_line.wav

# DiffRhythm: lyrics + style -> full song (add --chunked if VRAM < 8GB)
# cd ~/audio-2026/DiffRhythm && python infer.py --lrc lyrics.lrc --chunked
```
"""),
]

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    },
    "cells": cells,
}

if __name__ == "__main__":
    out = "cape_jones_audio2026_kaggle.ipynb"
    with open(out, "w") as f:
        json.dump(nb, f, indent=1)
    print(f"wrote {out} ({len(cells)} cells)")