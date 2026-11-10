#!/usr/bin/env python3
"""Unified forced-alignment dispatcher for lip-sync.

Produces word/phoneme timestamps (JSON) that feed the viseme/lip-sync stage
(Rhubarb, OpenFaceFX, LatentSync -- already in tools/).

  whisperx            BSD-2  word-level timestamps via whisper + wav2vec2 align
  whisper-timestamped AGPL   word timestamps (transformers-based)
  mfa                 MIT    Montreal Forced Aligner: phoneme-level (needs
                            pretrained acoustic model, English default)
  aeneas              AGPL   forced aligner (text+audio -> sync map JSON)
  coqui-stt           MPL-2  transcription QC (align output check)
"""
import argparse, os, subprocess, sys

TOOLS = os.path.expanduser("~/workspace/tools")

ENGINES = {
    "whisperx": {
        "dir": "whisperx",
        "cmd": lambda a, t: f"whisperx {a} --model large-v3 --align_model WAV2VEC2_ASR_LARGE_LV60K_960H --output_dir /tmp/align --output_format json",
    },
    "whisper-timestamped": {
        "dir": "whisper-timestamped",
        "cmd": lambda a, t: f"cd {TOOLS}/whisper-timestamped && python -m whisper_timestamped {a} --output /tmp/align.json --accurate",
    },
    "mfa": {
        "dir": "montreal-forced-aligner",
        "cmd": lambda a, t: f"mfa align {os.path.dirname(a) or '.'} english_us_arpa {os.path.basename(t) or 'dict.txt'} /tmp/align_out --output_format json",
    },
    "aeneas": {
        "dir": "aeneas",
        "cmd": lambda a, t: f"python -m aeneas.execute_task {a} {t} \"task_language=eng|os_task_file_format=json|is_text_type=plain\" /tmp/align.json",
    },
}


def main():
    ap = argparse.ArgumentParser(description="Forced alignment for lip-sync")
    ap.add_argument("--audio", "-a", default="", help="dialogue wav")
    ap.add_argument("--text", "-t", default="", help="transcript (txt/dict)")
    ap.add_argument("--engine", "-e", choices=list(ENGINES))
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list or (not args.audio and not args.engine):
        for n, e in ENGINES.items():
            repo = os.path.isdir(os.path.join(TOOLS, e["dir"]))
            print(f"{n:18} {'Y' if repo else '-':5}")
        return
    order = [args.engine] if args.engine else list(ENGINES)
    for name in order:
        e = ENGINES[name]
        if not os.path.isdir(os.path.join(TOOLS, e["dir"])):
            continue
        cmd = e["cmd"](args.audio, args.text)
        print(f"[lipsync_align] engine={name}\n[lipsync_align] cmd: {cmd}")
        if args.run:
            sys.exit(subprocess.run(cmd, shell=True).returncode)
        print("[lipsync_align] dry-run only (use --run)")
        return
    print("[lipsync_align] no engine repo found")


if __name__ == "__main__":
    main()
