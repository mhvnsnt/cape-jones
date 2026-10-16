#!/usr/bin/env python3
"""kaggle_setup_audio2026.py — one-shot installer + smoke tests for the audio-2026 pull-in.

Target: Kaggle T4 (GPU, internet ON), Google Colab, or the VM.
Installs all eight tools from production/pipeline/audio-2026/README.md, then
smoke-tests each (import / CLI --help / version). Model weights download on
first real use, NOT here — this script stays light.

Usage:
    python3 kaggle_setup_audio2026.py [--skip-cosyvoice] [--skip-diffrhythm]

Owner law: Chatterbox stays the character-voice default. These complement it.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.request

WORK = os.path.expanduser("~/audio-2026")
AUDIO_CPP_VER = "v0.9.2"
AUDIO_CPP_ASSET = f"audio-{AUDIO_CPP_VER}-bin-ubuntu-x64-cuda12.8-colab.tar.gz"
AUDIO_CPP_URL = (f"https://github.com/0xShug0/audio.cpp/releases/download/"
                 f"{AUDIO_CPP_VER}/{AUDIO_CPP_ASSET}")

PASS, FAIL = [], []


def run(cmd, **kw):
    print(f"$ {cmd}")
    r = subprocess.run(cmd, shell=True, **kw)
    return r.returncode == 0


def check(name, ok, note=""):
    (PASS if ok else FAIL).append(name)
    print(("PASS " if ok else "FAIL ") + name + (f" — {note}" if note else ""))


def pip(pkg):
    return run(f"{sys.executable} -m pip install -q {pkg}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-cosyvoice", action="store_true",
                    help="skip CosyVoice (heaviest install)")
    ap.add_argument("--skip-diffrhythm", action="store_true",
                    help="skip DiffRhythm clone+install")
    ap.add_argument("--workdir", default=WORK)
    args = ap.parse_args()
    os.makedirs(args.workdir, exist_ok=True)
    os.chdir(args.workdir)

    print("== GPU check ==")
    has_gpu = shutil.which("nvidia-smi") and run("nvidia-smi -L")
    check("nvidia-smi", bool(has_gpu), "T4 expected on Kaggle; CPU ok for separator/enhance")

    print("== pip installs ==")
    ok = pip("f5-tts==1.1.22")
    check("pip f5-tts==1.1.22", ok)
    ok = pip("audio-separator==0.47.0")
    check("pip audio-separator==0.47.0", ok)
    ok = pip("deepfilternet==0.5.6")
    check("pip deepfilternet==0.5.6", ok)
    ok = pip("resemble-enhance==0.0.1")
    check("pip resemble-enhance==0.0.1", ok)

    if not args.skip_cosyvoice:
        print("== CosyVoice (git, Apache-2.0) ==")
        if not os.path.isdir("CosyVoice"):
            ok = run("git clone --depth=1 https://github.com/FunAudioLLM/CosyVoice.git")
        else:
            ok = True
        ok = ok and pip("./CosyVoice")
        check("CosyVoice install", ok)
    else:
        print("== CosyVoice skipped ==")

    if not args.skip_diffrhythm:
        print("== DiffRhythm (git, Apache-2.0) ==")
        if not os.path.isdir("DiffRhythm"):
            ok = run("git clone --depth=1 https://github.com/ASLP-lab/DiffRhythm.git")
        else:
            ok = True
        ok = ok and pip("./DiffRhythm")
        check("DiffRhythm install", ok)
        print("   NOTE: DiffRhythm-base needs --chunked on <=8GB VRAM; T4 has 16GB.")
    else:
        print("== DiffRhythm skipped ==")

    print("== audio.cpp prebuilt (Apache-2.0, CUDA 12.8 colab build) ==")
    adir = os.path.join(args.workdir, "audio.cpp")
    if not os.path.isdir(adir):
        tgz = os.path.join(args.workdir, AUDIO_CPP_ASSET)
        try:
            print(f"downloading {AUDIO_CPP_URL}")
            urllib.request.urlretrieve(AUDIO_CPP_URL, tgz)
            os.makedirs(adir, exist_ok=True)
            with tarfile.open(tgz) as t:
                t.extractall(adir)
            ok = True
        except Exception as e:  # noqa: BLE001
            print(f"download failed: {e}")
            ok = False
    else:
        ok = True
    check("audio.cpp binary", ok, adir)

    print("== voice-changer (MIT, real-time VC rig) ==")
    if not os.path.isdir("voice-changer"):
        ok = run("git clone --depth=1 --filter=blob:none "
                 "https://github.com/w-okada/voice-changer.git")
    else:
        ok = True
    check("voice-changer clone", ok,
          "run start2.sh / start_docker.sh per repo README; server/MMVCServerSIO.py")

    print("== smoke tests (no model downloads) ==")
    def imp(mod):
        return run(f"{sys.executable} -c \"import {mod}; "
                   f"print('{mod}', getattr({mod}, '__version__', 'ok'))\"",
                   capture_output=True)

    check("import f5_tts", imp("f5_tts"))
    check("audio-separator --help", run("audio-separator --help", capture_output=True))
    check("deepfilternet --help", run("deepfilternet --help", capture_output=True))
    check("resemble-enhance import",
          run(f"{sys.executable} -c \"import resemble_enhance; print('ok')\"",
              capture_output=True))
    if not args.skip_cosyvoice:
        check("import cosyvoice", imp("cosyvoice"))
    if not args.skip_diffrhythm:
        check("DiffRhythm tree", os.path.isdir("DiffRhythm"))
    abin = None
    for root, _, files in os.walk(adir):
        if "audio" in files:
            abin = os.path.join(root, "audio")
            break
    check("audio.cpp binary runs", abin and run(f'"{abin}" --help', capture_output=True),
          abin or "binary not found")

    print()
    print(f"RESULT: {len(PASS)} passed, {len(FAIL)} failed")
    for f in FAIL:
        print(f"  FAILED: {f}")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()