#!/usr/bin/env python3
"""AVANNA-style vocaloid transform for Mars's own voice (open-source, repo-safe).
Uses WORLD vocoder (pyworld): decomposes voice into F0 / spectral envelope (formants)
 / aperiodicity (breathiness), then shifts each independently — the exact trick that
makes a human voice sound like a pitched-up, crisp, futuristic female vocaloid voice:
  - F0 x1.682 (+9 semitones, neptune-babii median target ~350 Hz from Mars raw ~210 Hz)
  - Spectral envelope (formants) shifted up by the same ratio (female timbre, not just pitch)
  - Aperiodicity reduced (less breathiness = crisper, more synthetic consonants, AVANNA trait)
  - No AVANNA voicebank is used, copied, or shipped: this transforms Mars's own recording.
Usage: python3 avanna_style.py <in.wav> <out.wav> [f0_ratio] [breath_scale]
"""
import sys, wave, numpy as np, pyworld as pw

def load(p):
    w = wave.open(p); n = w.getnframes(); sr = w.getframerate(); ch = w.getnchannels()
    d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(float) / 32768
    if ch > 1: d = d.reshape(-1, ch).mean(axis=1)
    return d, sr

def main(inp, out, f0_ratio=1.682, breath_scale=0.5):
    x, sr = load(inp)
    f0, t = pw.harvest(x, sr)
    f0 = pw.stonemask(x, f0, t, sr)
    sp = pw.cheaptrick(x, f0, t, sr)
    ap = pw.d4c(x, f0, t, sr)
    # F0 shift (pitch), formant shift via spectral envelope resampling on freq axis
    f0_new = np.where(f0 > 0, f0 * f0_ratio, 0)
    # shift spectral envelope: interpolate each frame's envelope to higher frequencies
    n_freq = sp.shape[1]
    sp_new = np.zeros_like(sp)
    for i in range(sp.shape[0]):
        src_idx = np.arange(n_freq) / f0_ratio
        sp_new[i] = np.interp(np.arange(n_freq), src_idx, sp[i], left=sp[i,0], right=sp[i,-1])
    ap_new = ap * breath_scale
    y = pw.synthesize(f0_new, sp_new, ap_new, sr)
    y = np.clip(y, -0.95, 0.95)
    w = wave.open(out, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((y * 32767).astype(np.int16).tobytes()); w.close()
    print(f"wrote {out}: {len(y)/sr:.2f}s, f0 x{f0_ratio}, breath x{breath_scale}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2],
         float(sys.argv[3]) if len(sys.argv) > 3 else 1.682,
         float(sys.argv[4]) if len(sys.argv) > 4 else 0.5)
