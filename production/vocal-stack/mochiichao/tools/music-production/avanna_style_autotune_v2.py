#!/usr/bin/env python3
"""WORLD vocaloid + SMOOTH autotune v2 (Antares + AVANNA blend, NOT chipmunk).
Chipmunk = pitch AND formants shifted up together by the same large ratio.
Hyperpop vocaloid = pitch high, formants shifted LESS than pitch, autotune snapped
with a glide (not instant frame jumps), and no dropped frames.
  - Pitch ratio 2.0 (harvest median 145Hz -> ~290Hz, snapped to D major -> ~293-330Hz)
  - Formant ratio 1.4 (female timbre, not tiny chipmunk vocal tract)
  - Autotune: snap to D major, then 11-frame moving average on log-F0 (~55ms glide,
    Antares retune-speed equivalent, not 0ms hard snap which chopped notes in v8/v9)
  - Unvoiced gaps <200ms interpolated (no silent dropouts inside phrases)
  - Breathiness x0.7 (crisp, not thin)
Usage: python3 avanna_style_autotune_v2.py <in.wav> <out.wav>
"""
import sys, wave, numpy as np, pyworld as pw
SCALE = [0, 2, 4, 5, 7, 9, 11]
def snap(f):
    if f <= 0: return 0.0
    midi = 69 + 12*np.log2(f/440.0); base = int(np.floor(midi)); best, bestd = None, 1e9
    for m in range(base-2, base+3):
        if (m - 2) % 12 in SCALE:
            d = abs(m - midi)
            if d < bestd: best, bestd = m, d
    return 440.0 * 2**((best-69)/12) if best is not None else f

def load(p):
    w = wave.open(p); n = w.getnframes(); sr = w.getframerate(); ch = w.getnchannels()
    d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(float)/32768
    if ch > 1: d = d.reshape(-1, ch).mean(axis=1)
    return d, sr

x, sr = load(sys.argv[1])
f0, t = pw.harvest(x, sr); f0 = pw.stonemask(x, f0, t, sr)
sp = pw.cheaptrick(x, f0, t, sr); ap = pw.d4c(x, f0, t, sr)
# interpolate short unvoiced gaps so WORLD never drops a frame inside a phrase
voiced = f0 > 0
idx = np.arange(len(f0))
f0_fill = np.interp(idx, idx[voiced], f0[voiced]) if voiced.any() else f0
# only interpolate gaps < 40 frames (200ms); longer gaps stay unvoiced (phrase breaks)
f0_work = f0.copy()
last_v, gap = -1, 0
for i, v in enumerate(voiced):
    if v:
        if 0 < gap < 40 and last_v >= 0:
            f0_work[last_v+1:i] = np.linspace(f0[last_v], f0[i], gap+2)[1:-1]
        last_v, gap = i, 0
    else:
        gap += 1
f0_shift = np.where(f0_work > 0, f0_work * 2.0, 0)
f0_snap = np.array([snap(v) for v in f0_shift])
# glide: moving average on log-F0 over voiced frames only (11 frames)
logf = np.where(f0_snap > 0, np.log(f0_snap), 0)
k = 11; ker = np.ones(k)/k
log_smooth = np.convolve(logf, ker, mode="same")
f0_tuned = np.where(f0_snap > 0, np.exp(log_smooth), 0)
# restore true phrase-break silences (gaps >= 40 frames stay 0)
f0_tuned = np.where(f0_work > 0, f0_tuned, 0)
n_freq = sp.shape[1]; sp_new = np.zeros_like(sp)
for i in range(sp.shape[0]):
    src = np.arange(n_freq) / 1.4
    sp_new[i] = np.interp(np.arange(n_freq), src, sp[i], left=sp[i,0], right=sp[i,-1])
y = pw.synthesize(f0_tuned, sp_new, ap * 0.7, sr)
y = np.clip(y, -0.95, 0.95)
w = wave.open(sys.argv[2], "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((y*32767).astype(np.int16).tobytes()); w.close()
print(f"wrote {sys.argv[2]}: {len(y)/sr:.2f}s, pitch x2.0, formant x1.4, autotune D major glide 55ms")
