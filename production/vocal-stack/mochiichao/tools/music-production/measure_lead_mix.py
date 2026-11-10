#!/usr/bin/env python3
"""Measure a vocal lead (pitch median, dropouts) and a mix (RMS, peak, bars,
vocal-band share, fade-in, tail). FFT autocorrelation, never np.correlate on
44.1k audio (that hangs). Usage: measure_lead_mix.py <lead.wav> <mix.wav>"""
import sys, subprocess, numpy as np

def decode(p, mono=True):
    # NOTE: ffmpeg -ac 1 SUMS stereo channels (observed x2 gain); use an explicit
    # 0.5/0.5 pan mix for a true mono average so RMS/peak match volumedetect.
    cmd = ["ffmpeg", "-v", "error", "-i", p, "-af", "pan=mono|c0=0.5*c0+0.5*c1",
           "-ar", "44100", "-f", "f32le", "-"] if mono else \
          ["ffmpeg", "-v", "error", "-i", p, "-ac", "2",
           "-ar", "44100", "-f", "f32le", "-"]
    out = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype=np.float32).astype(float)

def autocorr_pitch(frame, sr, lo=150, hi=800):
    x = frame - frame.mean()
    if np.sqrt(np.mean(x ** 2)) < 0.02:
        return None
    n = 1 << int(np.ceil(np.log2(len(x) * 2)))
    spec = np.fft.rfft(x, n)
    ac = np.fft.irfft(spec * np.conj(spec))[:len(x)]
    if ac[0] <= 0:
        return None
    ac /= ac[0]
    lo_lag, hi_lag = int(sr / hi), int(sr / lo)
    seg = ac[lo_lag:hi_lag]
    if len(seg) == 0:
        return None
    lag = np.argmax(seg) + lo_lag
    return sr / lag

sr = 44100
lead = decode(sys.argv[1])
# phrase windows on the warped timeline (same windows used since v2)
phrases = [(0, 6.51), (7.39, 13.06), (13.95, 19.89), (20.93, 26.45), (27.41, 33.32), (33.77, 35.12), (35.46, 36.89), (37.24, 39.81)]
pitches, drop, total = [], 0, 0
for a, b in phrases:
    s0, s1 = int(a * sr), int(b * sr)
    for k in range(s0, s1, int(0.05 * sr)):
        fr = lead[k:k + int(0.05 * sr)]
        if len(fr) < int(0.05 * sr):
            break
        total += 1
        if np.sqrt(np.mean(fr ** 2)) < 0.01:
            drop += 1
    for k in range(s0, s1, int(0.10 * sr)):
        fr = lead[k:k + int(0.10 * sr)]
        if len(fr) < int(0.10 * sr):
            break
        p = autocorr_pitch(fr, sr)
        if p:
            pitches.append(p)
print(f"LEAD {sys.argv[1]}: dur={len(lead)/sr:.2f}s rms={np.sqrt(np.mean(lead**2)):.4f} "
      f"peak={np.max(np.abs(lead)):.3f} pitch_median={np.median(pitches):.0f}Hz "
      f"(n={len(pitches)}) dropouts={drop}/{total}={100*drop/max(total,1):.1f}% (50ms frames RMS<0.01)")
mixm = decode(sys.argv[2], mono=True)  # mono downmix: time axis stays true
print(f"MIX {sys.argv[2]}: dur={len(mixm)/sr:.3f}s rms={np.sqrt(np.mean(mixm**2)):.4f} "
      f"peak={np.max(np.abs(mixm)):.3f} mean_dB={20*np.log10(np.sqrt(np.mean(mixm**2))):.1f}")
bars = []
for i in range(6):
    s0, s1 = int(i * 4 * 1.714 * sr), int((i + 1) * 4 * 1.714 * sr)
    seg = mixm[s0:s1]
    bars.append(np.sqrt(np.mean(seg ** 2)))
print("bars(4-bar groups):", " ".join(f"{b:.3f}" for b in bars))
spec = np.abs(np.fft.rfft(mixm * np.hanning(len(mixm)))) ** 2
freqs = np.fft.rfftfreq(len(mixm), 1 / sr)
vb = spec[(freqs >= 1000) & (freqs <= 8000)].sum() / spec.sum()
print(f"vocal-band(1-8kHz) share={vb:.3f}")
for a, b, tag in [(0, 1, "fade sec0"), (3, 4, "fade sec3"), (4, 5, "sec4"),
                  (39.8, 40.3, "tail 39.8-40.3")]:
    seg = mixm[int(a * sr):int(b * sr)]
    print(f"{tag}: rms={np.sqrt(np.mean(seg**2)):.3f}")
