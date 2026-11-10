#!/usr/bin/env python3
"""House Pedalboard chains (Spotify Pedalboard, GPL-3.0 — used as a pipeline
tool; see TEARDOWN-pedalboard.md).

Usage: pedalboard_chain.py <in.wav> <out.wav> [--chain voice|bed]

voice: HPF 80 Hz -> presence peak +3 dB @ 3 kHz -> compressor 3:1 @ -18 dB
       -> limiter ceiling -1 dB. For Chatterbox/Kokoro/casting voice lines.
bed:   low shelf +1.5 dB @ 120 Hz -> glue compressor 2:1 @ -20 dB
       -> limiter ceiling -1 dB. For music beds before the loudnorm spine.
Prints in/out peak and RMS so the run is self-recording.
"""
import argparse
import numpy as np
from pedalboard import (Pedalboard, Compressor, Gain, HighpassFilter,
                        Limiter, LowShelfFilter, PeakFilter)
from pedalboard.io import AudioFile


def build_chain(name):
    if name == "voice":
        return Pedalboard([
            HighpassFilter(cutoff_frequency_hz=80.0),
            PeakFilter(cutoff_frequency_hz=3000.0, gain_db=3.0, q=0.8),
            Compressor(threshold_db=-18.0, ratio=3.0, attack_ms=10.0,
                       release_ms=120.0),
            Limiter(threshold_db=-1.0, release_ms=100.0),
        ])
    return Pedalboard([
        LowShelfFilter(cutoff_frequency_hz=120.0, gain_db=1.5, q=0.7),
        Compressor(threshold_db=-20.0, ratio=2.0, attack_ms=20.0,
                   release_ms=200.0),
        Limiter(threshold_db=-1.0, release_ms=100.0),
        Gain(gain_db=0.0),
    ])


def stats(audio):
    peak = float(np.max(np.abs(audio))) if audio.size else 0.0
    rms = float(np.sqrt(np.mean(audio ** 2))) if audio.size else 0.0
    return peak, rms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--chain", default="voice", choices=["voice", "bed"])
    a = ap.parse_args()
    with AudioFile(a.src) as f:
        audio = f.read(f.frames)
        sr = f.samplerate
    ip, ir = stats(audio)
    out = build_chain(a.chain)(audio, sr)
    op, orr = stats(out)
    with AudioFile(a.dst, "w", sr, out.shape[0]) as f:
        f.write(out)
    print(f"chain={a.chain} sr={sr} frames={audio.shape[1]}")
    print(f"in : peak={ip:.4f} rms={ir:.4f}")
    print(f"out: peak={op:.4f} rms={orr:.4f}")
    print(f"wrote {a.dst}")


if __name__ == "__main__":
    main()
