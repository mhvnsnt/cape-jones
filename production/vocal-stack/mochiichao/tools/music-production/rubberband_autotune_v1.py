#!/usr/bin/env python3
"""Rubberband autotune + feminine shift v1 (V19 lead) — NO WORLD resynthesis.

Why this exists: v18's robotic/muddy formants came from WORLD's spectral-envelope
warp stacked across layers (envelope resampled by 1/1.5 on every layer, plus a
20ms-glide WORLD main lead, plus rubberband re-processing WORLD output). This
script keeps Mars's actual performance and does every pitch operation with
Rubber Band (the pro phase-vocoder pitch shifter used in DAWs), which does not
resynthesize the voice from a spectral model, so it cannot invent the robotic
artifacts WORLD's envelope warp does.

Chain:
  1. F0 estimation ONLY with pyworld harvest + stonemask (no synthesis).
  2. Autotune by note segments: smoothed F0 -> snapped D-major note per segment;
     each segment is pitch-shifted with rubberband (formant preserved) by
     snapped/median ratio, 25ms raised-cosine crossfades at segment edges.
     Segments <60ms merge into the previous note; notes already within
     25 cents of the scale are left untouched (natural vibrato kept).
  3. Feminine shift, decoupled from pitch (the AVANNA separation, done with
     rubberband instead of WORLD):
       pass 1: pitch x2.0, formant SHIFTED  -> pitch x2.0, formants x2.0
       pass 2: pitch x1.4, formant PRESERVED -> pitch x2.8 total, formants stay x2.0
     Pitch x2.8 from a 145 Hz harvest median targets ~400 Hz perceived.
     Formant/pitch ratio = 2.0/2.8 = 0.71, the SAME separation as v11
     (pitch 2.0, formant 1.4) which Mars judged the least chipmunk direction.
     First attempt used formants x1.4 with pitch x2.8 (ratio 0.5): measured
     lead spectrum was 94.5% in 300-1000 Hz, 2.7% in 1-8 kHz — the male
     envelope stayed low and the mix measured muddier than v18. Formants x2.0
     moves the envelope up with the pitch while keeping the 0.71 separation,
     so brightness comes back without going full chipmunk (ratio 1.0).
Usage: python3 rubberband_autotune_v1.py <in.wav> <out.wav>
"""
import sys, wave, subprocess, os, numpy as np, pyworld as pw

SCALE_PC = {2, 4, 6, 7, 9, 11, 1}  # D major: D E F# G A B C#
SR = 44100

def snap_midi(m):
    base = int(np.floor(m))
    best, bestd = None, 1e9
    for cand in range(base - 2, base + 3):
        if cand % 12 in SCALE_PC:
            d = abs(cand - m)
            if d < bestd:
                best, bestd = cand, d
    return best

def load(p):
    w = wave.open(p); n = w.getnframes(); sr = w.getframerate(); ch = w.getnchannels()
    d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(float) / 32768
    if ch > 1:
        d = d.reshape(-1, ch).mean(axis=1)
    return d, sr

def save(p, y, sr):
    y = np.clip(y, -0.95, 0.95)
    w = wave.open(p, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((y * 32767).astype(np.int16).tobytes()); w.close()

def rubberband_shift(x, sr, ratio, formant, tmp):
    inp, outp = tmp + ".in.wav", tmp + ".out.wav"
    save(inp, x, sr)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", inp, "-af",
                    f"rubberband=pitch={ratio:.5f}:formant={formant}:pitchq=quality",
                    outp], check=True)
    y, _ = load(outp)
    os.remove(inp); os.remove(outp)
    return y

x, sr = load(sys.argv[1])
assert sr == SR, sr
f0, t = pw.harvest(x, sr)
f0 = pw.stonemask(x, f0, t, sr)
voiced = f0 > 0
# median filter (5 frames) on voiced F0, then interpolate gaps < 40 frames (200ms)
f0m = f0.copy()
for i in range(2, len(f0) - 2):
    if voiced[i]:
        win = f0[max(0, i - 2):i + 3]
        win = win[win > 0]
        if len(win):
            f0m[i] = np.median(win)
idx = np.arange(len(f0))
f0w = f0m.copy()
last_v, gap = -1, 0
for i, v in enumerate(voiced):
    if v:
        if 0 < gap < 40 and last_v >= 0:
            f0w[last_v + 1:i] = np.linspace(f0m[last_v], f0m[i], gap + 2)[1:-1]
        last_v, gap = i, 0
    else:
        gap += 1
# smooth log-F0 (7-frame moving average, ~35ms) -> midi track
logf = np.where(f0w > 0, np.log(np.maximum(f0w, 1e-6)), 0.0)
ker = np.ones(7) / 7
logs = np.convolve(logf, ker, mode="same")
midi = np.where(f0w > 0, 69 + 12 * np.log2(np.exp(logs) / 440.0), np.nan)
snapped = np.array([snap_midi(m) if np.isfinite(m) else -1 for m in midi])
# segment into runs of the same snapped note
segs = []
i = 0
while i < len(snapped):
    if snapped[i] < 0:
        i += 1
        continue
    j = i
    while j < len(snapped) and snapped[j] == snapped[i]:
        j += 1
    segs.append([i, j, snapped[i]])
    i = j
# merge short segments (<12 frames = 60ms) into previous segment
merged = []
for s in segs:
    if merged and (s[1] - s[0]) < 12:
        merged[-1][1] = s[1]
    else:
        merged.append(s)
print(f"segments: {len(merged)}")
out = x.copy()
xf = int(0.025 * sr)  # 25ms crossfade
nshift = 0
for (a, b, note) in merged:
    if b - a < 8:
        continue
    med = np.nanmedian(midi[a:b])
    if not np.isfinite(med):
        continue
    if abs(med - note) < 0.25:
        continue
    ratio = 2 ** ((note - med) / 12.0)
    s0 = max(0, int(t[a] * sr) - xf)
    s1 = min(len(x), int(t[b - 1] * sr) + xf)
    seg = x[s0:s1]
    shifted = rubberband_shift(seg, sr, ratio, "preserved", "/tmp/rb_seg")
    # trim handles (rubberband preserves duration)
    if len(shifted) < len(seg):
        shifted = np.pad(shifted, (0, len(seg) - len(shifted)))
    shifted = shifted[:len(seg)]
    # raised-cosine crossfades at both edges against current output
    region = out[s0:s1].copy()
    n = len(seg)
    fade = np.ones(n)
    k = min(xf, n // 2)
    if k > 0:
        ramp = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, k))
        fade[:k] = ramp
        fade[-k:] = 1 - ramp
    out[s0:s1] = region * (1 - fade) + shifted * fade
    nshift += 1
print(f"segments shifted: {nshift}")
save("/tmp/rb_autotuned.wav", out, sr)
# feminine shift, two passes (pitch x2.8 total, formants x1.4)
p1 = rubberband_shift(out, sr, 2.0, "shifted", "/tmp/rb_p1")
p2 = rubberband_shift(p1, sr, 1.4, "preserved", "/tmp/rb_p2")
save(sys.argv[2], p2, sr)
print(f"wrote {sys.argv[2]}: {len(p2)/sr:.2f}s")
