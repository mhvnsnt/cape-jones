#!/usr/bin/env python3
"""Mastering stage with Spotify's Pedalboard (open-source DSP, no DAW needed).
Chain: HighpassFilter 30Hz -> Compressor (gentle glue) -> Limiter (-1 dB true-peak-ish ceiling).
This is the LAST stage only: it does not mix, it masters. Input: a rendered mix WAV.
Usage: python3 pedalboard_master.py <in.wav> <out.wav>
"""
import sys
from pedalboard import Pedalboard, HighpassFilter, Compressor, Limiter
from pedalboard.io import AudioFile
with AudioFile(sys.argv[1]) as f:
    audio = f.read(f.frames); sr = f.samplerate; ch = f.num_channels
board = Pedalboard([HighpassFilter(cutoff_frequency_hz=30.0),
                    Compressor(threshold_db=-18.0, ratio=2.0, attack_ms=10.0, release_ms=120.0),
                    Limiter(threshold_db=-1.0, release_ms=50.0)])
out = board(audio, sr)
with AudioFile(sys.argv[2], 'w', sr, ch) as f:
    f.write(out)
print(f"mastered {sys.argv[1]} -> {sys.argv[2]} (HP30 + comp 2:1 + limiter -1dB)")

# MEASURED WARNING (2026-10-26, v16 test): the Limiter-only pass on this mix
# measured HOTTER than the input (mean -12.6 -> -10.6 dB, peak 0.0 dBFS, LUFS
# -8.2, tail 0.145 -> 0.229) — the comp version also lifted the tail cut.
# So for loop tracks, master with the ffmpeg chain's own limiter (0.89) and
# VERIFY peak/LUFS/tail after any Pedalboard pass before shipping it.
# Do not ship a Pedalboard-mastered file on meters alone.
