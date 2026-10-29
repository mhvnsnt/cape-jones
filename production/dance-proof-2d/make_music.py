#!/usr/bin/env python3
"""Tamagotchi-style chiptune loop, synthesized with numpy. 21 s, square-wave
lead + triangle bass + tick hats. Cute, loopy, digital-pet energy."""
import numpy as np, wave, os

SR = 22050
DUR = 21.0
BPM = 142
BEAT = 60.0 / BPM
EIGHTH = BEAT / 2
N = int(SR * DUR)
out = np.zeros(N, np.float32)

def note_freq(midi): return 440.0 * 2 ** ((midi - 69) / 12.0)

def add_square(midi, t0, dur, vol, detune_cents=0.0):
    f = note_freq(midi) * 2 ** (detune_cents / 1200.0)
    i0, i1 = int(t0 * SR), min(N, int((t0 + dur) * SR))
    if i1 <= i0: return
    t = np.arange(i1 - i0) / SR
    ph = (t * f) % 1.0
    w = np.where(ph < 0.5, 1.0, -1.0)
    env = np.minimum(1.0, t / 0.006) * (0.72 + 0.28 * np.exp(-t * 6.0))
    out[i0:i1] += vol * w * env

def add_tri(midi, t0, dur, vol):
    f = note_freq(midi)
    i0, i1 = int(t0 * SR), min(N, int((t0 + dur) * SR))
    if i1 <= i0: return
    t = np.arange(i1 - i0) / SR
    ph = (t * f) % 1.0
    w = 2 * np.abs(2 * ph - 1) - 1
    env = np.minimum(1.0, t / 0.01) * np.exp(-t * 1.2)
    out[i0:i1] += vol * w * env

def add_tick(t0, vol=0.05):
    i0, i1 = int(t0 * SR), min(N, int((t0 + 0.03) * SR))
    if i1 <= i0: return
    rng = np.random.default_rng(int(t0 * 1000) + 7)
    out[i0:i1] += vol * rng.standard_normal(i1 - i0) * np.exp(-np.arange(i1 - i0) / SR * 260)

# lead melody: 2-bar loop, 8ths. C major, bouncy.
MEL = [72, 76, 79, 76, 81, 79, 76, 74,
       72, 76, 79, 76, 74, 76, 72,  0,
       74, 76, 79, 76, 81, 79, 76, 74,
       76, 74, 72, 74, 72,  0, 67, 71]
# bass roots per bar (2 bars): C G | C G ... with F in bar 2 of each pair
BASS = [48, 55, 48, 55, 53, 55, 48, 55]
steps_per_bar = 16
total_steps = int(DUR / EIGHTH)
for s in range(total_steps):
    t0 = s * EIGHTH
    m = MEL[s % len(MEL)]
    if m: add_square(m, t0, EIGHTH * 0.92, 0.16)
    if m: add_square(m, t0, EIGHTH * 0.92, 0.05, detune_cents=7)
    add_tick(t0, 0.035 if s % 2 == 0 else 0.02)
for b in range(int(DUR / BEAT)):
    t0 = b * BEAT
    root = BASS[(b // 2) % len(BASS)] if b % 2 == 0 else BASS[(b // 2) % len(BASS)]
    add_tri(root, t0, BEAT * 0.95, 0.20)
    add_tri(root + 12, t0 + BEAT / 2, BEAT * 0.4, 0.07)   # little bloop off-beat

out *= 0.9 / max(1e-6, np.abs(out).max())
# click-free ends
fade = int(SR * 0.03)
out[:fade] *= np.linspace(0, 1, fade); out[-fade:] *= np.linspace(1, 0, fade)
pcm = (out * 32767).astype(np.int16)
path = os.path.expanduser('~/workspace/_cj-dance-2d/build/chiptune.wav')
with wave.open(path, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('wrote', path, f'{len(pcm)/SR:.2f}s')
