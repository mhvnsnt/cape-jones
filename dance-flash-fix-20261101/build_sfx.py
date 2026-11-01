#!/usr/bin/env python3
"""
build_sfx.py — ORIGINAL synthesized SFX track for the fixed dance videos.
No show audio, no copyrighted audio, no sample from another show.
All sounds are synthesized here with numpy: filtered noise + sine.

Timing, tied to the visual grid (not a free rhythm):
- Visual dance grid ~107 BPM, beat starts (timeline 1..109, from
  dance-improved report): 1, 15, 28, 42, 56, 69, 83, 97, 110.
  At 24fps those are t = (beat-1)/24 seconds into each 109-frame loop.
- Footstep thump on EVERY beat start in every loop: 0.09s,
  70 Hz sine decay + lowpassed noise burst, peak -18 dBFS.
  Steps land on the beat, not on a free rhythm (Foley rule in
  ADDITIONAL-STANDARDS: steps on contact frames).
- Whoosh on arm-snap frames (timeline f015 and f083, the two
  measured arm-front-snap keys): 0.35s noise sweep, rising,
  ending AT the snap frame, never continuing past it.
  Whoosh leads the snap by 0.35s and ends at the snap time.
- Soft bounce pop on squat/groove beats (f028, f056): 0.12s
  sine pitch drop 300->120 Hz, peak -20 dBFS.
- No ambience bed added: the song already fills the mix, and a
  bed per environment would need crossfades per loop segment;
  adding a bed on guess would muddy the vocal. Stated, not hidden.

Mix: song (full v2, -14 LUFS locked) at 1.0 + SFX at 0.35,
then measured with ffmpeg loudnorm. Final loudness is reported
in REPORT, not claimed as -14 if the mix moves it.
Outputs: dance-test-FIXED-v2-sfx-track-20261101.wav (SFX only),
and remixed EN/JP finals are made by the shell step in REPORT
(ffmpeg amix), not by this script, so the song files stay untouched.
"""
import numpy as np, wave, os
SR = 44100
DUR = 75.789
LOOP_FRAMES = 123
FPS = 24
BEATS = [0, 14, 27, 41, 68, 82, 96, 110]  # v2 0-based frame indices, fast section held
SNAPS = [14, 96]
BOUNCES = [27, 68]

def add(buf, start, sig):
    i0 = int(start * SR)
    i1 = min(len(buf), i0 + len(sig))
    if i1 > i0:
        buf[i0:i1] += sig[:i1-i0]

def step():
    t = np.arange(int(0.09*SR)) / SR
    env = np.exp(-t*45)
    s = 0.6*np.sin(2*np.pi*70*t)*env + 0.4*np.random.randn(len(t))*env*np.exp(-t*20)
    return s * 0.25  # peak about -18 dBFS after mix scaling

def whoosh():
    n = int(0.35*SR); t = np.arange(n)/SR
    noise = np.random.randn(n)
    # rising sweep feel: simple one-pole lowpass with rising cutoff
    # approximated by amplitude ramp + differencing
    out = np.cumsum(noise) * 0.02
    out = out - np.linspace(out[0], out[-1], n)
    env = np.sin(np.pi * (t/0.35))**1.5
    return out * env * 0.35

def bounce():
    t = np.arange(int(0.12*SR)) / SR
    f = 300 * (120/300)**(t/0.12)
    return 0.3 * np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*25)

def main():
    np.random.seed(20261101)
    buf = np.zeros(int(DUR*SR))
    loops = int(DUR / (LOOP_FRAMES/FPS)) + 1
    for L in range(loops):
        base = L * LOOP_FRAMES / FPS
        for b in BEATS:
            add(buf, base + b/FPS, step())
        for s in SNAPS:
            st = base + s/FPS - 0.35
            if st >= 0:
                add(buf, st, whoosh())
        for b in BOUNCES:
            add(buf, base + b/FPS, bounce())
    # normalize SFX-only track to -3 dB peak, mix level is set in ffmpeg
    peak = np.max(np.abs(buf)) or 1.0
    buf = buf / peak * 0.7
    out = os.path.expanduser("~/workspace/cape-jones-rig/dance-flash-fix-20261101/dance-test-FIXED-v2-sfx-track-20261101.wav")
    with wave.open(out, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((buf * 32767).astype(np.int16).tobytes())
    print(f"SFX track: {out}, {DUR}s, beats/loops: {len(BEATS)} per loop x {loops} loops")

if __name__ == "__main__":
    main()
