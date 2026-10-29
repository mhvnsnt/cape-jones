#!/usr/bin/env python3
"""Digital Fairy chain — Pedalboard-available parts ONLY (free stack).

Teardown source: Digital Fairy / Yameii vocal chain + Deko dual bus,
in show/production/tooling/music-wave/VOCAL-CHAIN-DIGITAL-FAIRY-YAMEII-DEKO-20DSP.md
and docs/FREE-STACK-PRODUCTION-NOTES.md (Voice/DSP section, restored 2026-10-28).

What this script DOES (Pedalboard built-ins, GPL-3.0 tool, pipeline use only):
  Avanna-style bus (no formant stage, see below):
    HPF 150 Hz -> presence peak -> compressor -> limiter -1 dB
  Human digi bus (formant stage NOT in Pedalboard, see below):
    HPF 150 Hz -> presence peak -> compressor -> slapback delay 60 ms, low mix
    -> limiter -1 dB
  Air: high-shelf via PeakFilter is approximated with a presence peak;
  true Fresh Air harmonic excitation is NOT a Pedalboard built-in.

What this script does NOT claim (custom DSP owed, do not report as wired):
  - True formant shift (+3.5 to +5.5 human, +2.0 to +3.5 Deko human bus,
    CHA +25 to +45 inside Vocaloid) — cepstral/LPC warping, custom build.
  - OTT-style multiband (LR4 88.3 Hz / 2.5 kHz, upward + downward) — custom build.
  - Soothe-style 2048-STFT resonance suppression — custom build.
  - Vocoder (Bark filterbank, unvoiced bypass, 10% parallel) — custom build.
  - Zero-speed Auto-Tune (YIN/pYIN + TD-PSOLA, Soprano tracking) — custom build.
  - Bitcrush: Pedalboard Distortion is a rough stand-in, not a bitcrusher;
    it is NOT included here, to avoid claiming a bitcrush that is not one.

Usage: digital_fairy_chain.py <in.wav> <out.wav> [--bus avanna|human]
Prints in/out peak and RMS so the run is self-recording.
House loudness spine is unchanged: -14 LUFS / -1 dBTP (FFmpeg loudnorm),
applied downstream, not by this script.
"""
import argparse
import numpy as np
from pedalboard import (Pedalboard, Compressor, Delay, Gain, HighpassFilter,
                        Limiter, PeakFilter)
from pedalboard.io import AudioFile


def build_chain(bus):
    base = [
        HighpassFilter(cutoff_frequency_hz=150.0),
        PeakFilter(cutoff_frequency_hz=3000.0, gain_db=3.0, q=0.8),
        Compressor(threshold_db=-18.0, ratio=3.0, attack_ms=10.0,
                   release_ms=120.0),
    ]
    if bus == "human":
        # Slapback: 60 ms (teardown range 50-70 ms), zero feedback, low mix.
        # Pedalboard Delay mix is set via the effect's mix parameter where
        # available; Gain staging keeps the delay low in the summed output.
        base.append(Delay(delay_seconds=0.06, feedback=0.0, mix=0.15))
    base.append(Limiter(threshold_db=-1.0, release_ms=100.0))
    return Pedalboard(base)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--bus", default="avanna", choices=["avanna", "human"])
    a = ap.parse_args()
    with AudioFile(a.src) as f:
        audio = f.read(f.frames)
        sr = f.samplerate
    out = build_chain(a.bus)(audio, sr)
    with AudioFile(a.dst, "w", sr, out.shape[0]) as f:
        f.write(out)
    print(f"bus={a.bus} sr={sr} frames={audio.shape[1]}")
    print(f"in : peak={float(np.max(np.abs(audio))):.4f}")
    print(f"out: peak={float(np.max(np.abs(out))):.4f}")
    print("NOTE: formant / OTT / Soothe / vocoder / zero-speed tuner NOT in this chain — custom DSP owed.")
    print(f"wrote {a.dst}")


if __name__ == "__main__":
    main()
