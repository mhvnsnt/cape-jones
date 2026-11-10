#!/usr/bin/env python3
"""Mix v2 for the Cape Jones dance song (JP + EN) — the balance fix.
Owner complaint on v1: 'as soon as the lyrics vocals drop then the beat is
almost unhearable.' Measured root cause (measure_v1.py): the v1 vocal bus
sat +11 to +15 dB over the whole instrumental while singing (hit-song
median is ~0 dB), and inside the delivered master the beat's 40-250 Hz
body fell ~8 dB from the intro into the vocal sections — the hot vocal
ate the shared master compressor/limiter budget and pumped the beat down.

V2 architecture (research: hyperpop/digicore + anisong practice, and the
repo's own VOCAL-CHAIN teardown module 14 / section F.3):
  1. LEVELS FIRST: per-section vocal<->instrumental offsets solved to
     genre targets (vocal ~level with the beat broadband; verses +0.5 dB,
     choruses 0, bridge +1, outro +1) instead of one hot global gain.
  2. STATIC CARVE: -2 dB @ 3 kHz on the square lead + arp (the vocal's
     presence band), sparkle trimmed (its energy is 99% inside 2-5 kHz).
  3. SPECTRAL DUCK (TrackSpacer-style, custom STFT): the vocal key dips
     ONLY the clashing bins of arp / lead / sparkle, Mid channel only
     (stereo width untouched), max ~4 dB, fast attack / ~150 ms release.
     Drums and bass are NEVER ducked — the beat's body stays put.
  4. STEREO: vocal lead focused centre (Haas 0.30 -> 0.18), layers wide;
     arp widened (+2 dB side) so its energy leaves the vocal's centre.
  5. SECTION ARCHITECTURE on the instrumental bus (intro 0, verses -0.5,
     choruses 0, bridge -2, outro -1 dB) for contrast without pumping.
  6. MASTER: unchanged house chain (pedalboard_master.py HP30 -> comp
     -18 dB 2:1 -> limiter -1) then loudnorm to the locked house spine
     -14 LUFS / -1 dBTP, verified on meters afterwards.
The vocal chain itself is v1's, note for note (Digital Fairy Avanna bus ->
v19 ffmpeg stack -> layers): the owner approved the voice; only its
placement in the mix was wrong.
Usage: mix_v2.py jp|en   (run with the music-pullin venv python)"""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_data import TOTAL_BARS, BAR_SEC, SECTIONS

LANG = sys.argv[1] if len(sys.argv) > 1 else "jp"
SR = 44100
BASE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(BASE, "build")
VOC = os.path.join(W, "vocal" if LANG == "jp" else "vocal_en")
WAV = os.path.join(W, "wav")
OUT = os.path.join(W, "mix2", LANG); os.makedirs(OUT, exist_ok=True)
STACK = os.path.join(BASE, "vocalstack")
sys.path.insert(0, os.path.join(STACK, "show/production/tooling/music-wave/tools"))
import digital_fairy_chain as dfc
from pedalboard import Pedalboard, Chorus, Delay, Reverb, PeakFilter
from pedalboard.io import AudioFile

TOTAL = TOTAL_BARS * BAR_SEC
N = int(TOTAL * SR)
SEC = [(name, a * BAR_SEC, b * BAR_SEC) for name, a, b in SECTIONS]

def run(cmd):
    subprocess.run(cmd, check=True)

def load(p):
    with AudioFile(p) as f:
        return np.ascontiguousarray(f.read(f.frames), dtype=np.float32)

def save(p, a):
    if a.ndim == 1: a = a.reshape(1, -1)
    with AudioFile(p, "w", SR, a.shape[0]) as f:
        f.write(a.astype(np.float32))

def ff(inp, outp, filt):
    run(["ffmpeg", "-y", "-v", "error", "-i", inp, "-af", filt, "-ar", str(SR), outp])

def pad2(x):
    y = np.zeros((x.shape[0], N), dtype=np.float32)
    y[:, :min(N, x.shape[1])] = x[:, :N]
    return y

def pad1(x):
    y = np.zeros(N, dtype=np.float32); y[:min(N, len(x))] = x[:N]; return y

def rms_db(x, a, b):
    seg = x[:, int(a * SR):int(b * SR)]
    return 10 * np.log10(float(np.mean(seg.astype(np.float64) ** 2)) + 1e-20)

def section_curve(gains, ramp=0.15):
    """gains: {section_name: dB}. Returns per-sample linear gain with
    raised-cosine ramps centred on section boundaries."""
    gdb = np.zeros(N, dtype=np.float32)
    for name, a, b in SEC:
        gdb[int(a * SR):int(b * SR)] = gains[name]
    g = 10 ** (gdb / 20)
    r = int(ramp * SR)
    for name, a, b in SEC[1:]:
        s = int(a * SR)
        lo, hi = max(0, s - r // 2), min(N, s + r // 2)
        if hi > lo:
            t = (np.linspace(0, 1, hi - lo) - 0.5) * np.pi
            wgt = 0.5 + 0.5 * np.sin(t)  # smoothstep-ish
            g[lo:hi] = g[lo] * (1 - wgt) + g[hi - 1] * wgt if hi - lo > 1 else g[lo:hi]
    return g

# ================= vocal (v1 chain, unchanged) =================
lead, _ = (lambda a: (a[0], None))(load(os.path.join(VOC, "lead_raw.wav")))
lead = dfc.build_chain("avanna")(pad1(lead).reshape(1, -1), SR)[0]
save(os.path.join(OUT, "lead_fairy.wav"), lead)
ff(os.path.join(OUT, "lead_fairy.wav"), os.path.join(OUT, "lead_proc.wav"),
   "highpass=f=150,equalizer=f=300:width_type=o:width=1.2:g=-5,"
   "equalizer=f=3000:width_type=o:width=1:g=6,equalizer=f=5000:width_type=o:width=1:g=6,"
   "equalizer=f=8000:width_type=o:width=1:g=6,equalizer=f=12000:width_type=s:width=1:g=4,"
   "deesser=i=0.6:f=0.16,acompressor=threshold=0.10:ratio=4:attack=5:release=80:makeup=2")
lead = pad1(load(os.path.join(OUT, "lead_proc.wav"))[0])
KEY = lead.copy()  # processed lead = ducking key

harm = load(os.path.join(VOC, "harmony_raw.wav"))[0]
harm = dfc.build_chain("human")(pad1(harm).reshape(1, -1), SR)[0] * 0.5
ff(os.path.join(VOC, "octave_raw.wav"), os.path.join(OUT, "oct_ch.wav"),
   "highpass=f=250,chorus=0.5:0.5:25|35:0.4|0.5:5|7:0.5|0.6,volume=0.35")
octa = pad1(load(os.path.join(OUT, "oct_ch.wav"))[0])
ff(os.path.join(OUT, "lead_proc.wav"), os.path.join(OUT, "lead_sat.wav"),
   "acrusher=level_in=1:level_out=1:bits=10:mix=0.2,volume=0.5")
sat = pad1(load(os.path.join(OUT, "lead_sat.wav"))[0])

bus = np.zeros((2, N), dtype=np.float32)
bus[0] += lead; bus[1] += lead
d = int(0.012 * SR); bus[1, d:] += lead[:-d] * 0.18  # narrower Haas than v1
for layer in (harm, octa, sat):
    bus[0] += layer; bus[1] += layer
wet = Pedalboard([Delay(delay_seconds=0.321, feedback=0.18, mix=0.28),
                  Reverb(room_size=0.35, wet_level=0.10, dry_level=0.0)])(bus.copy(), SR)
bus += wet * 0.5

# ================= spectral ducking (TrackSpacer-style, Mid only) =================
NFFT, HOP = 2048, 512
WIN = np.hanning(NFFT).astype(np.float32)
FREQS = np.fft.rfftfreq(NFFT, 1 / SR)

def stft(x):
    xp = np.concatenate([np.zeros(NFFT // 2, np.float32), x, np.zeros(NFFT, np.float32)])
    nfr = 1 + (len(xp) - NFFT) // HOP
    idx = np.arange(NFFT)[None, :] + HOP * np.arange(nfr)[:, None]
    return np.fft.rfft(xp[idx] * WIN, axis=1).T  # (freq, time) complex64

def istft(X, length):
    nfr = X.shape[1]
    out = np.zeros(HOP * (nfr - 1) + NFFT, dtype=np.float32)
    norm = np.zeros_like(out)
    frames = np.fft.irfft(X.T, NFFT, axis=1) * WIN
    for t in range(nfr):
        s = t * HOP
        out[s:s + NFFT] += frames[t]
        norm[s:s + NFFT] += WIN ** 2
    nz = norm > 1e-8
    out[nz] /= norm[nz]
    return out[NFFT // 2:NFFT // 2 + length]

def spectral_duck(stereo, key, max_duck_db, lo=900.0, hi=6500.0, ratio=0.4):
    mid = (stereo[0] + stereo[1]) * 0.5
    side = (stereo[0] - stereo[1]) * 0.5
    T = stft(mid); K = stft(key)
    nf = min(T.shape[1], K.shape[1]); T, K = T[:, :nf], K[:, :nf]
    v_db = 20 * np.log10(np.abs(K) + 1e-6)
    t_db = 20 * np.log10(np.abs(T) + 1e-6)
    duck = np.clip(ratio * np.maximum(v_db - t_db, 0.0), 0.0, max_duck_db)
    band = (FREQS >= lo) & (FREQS <= hi)
    duck[~band, :] = 0.0
    # frequency smoothing (5-bin moving average)
    ker = np.ones(5, dtype=np.float32) / 5
    duck = np.apply_along_axis(lambda c: np.convolve(c, ker, mode="same"), 0, duck)
    duck[~band, :] = 0.0
    # time smoothing: fast attack, ~150 ms release (hop = 11.6 ms)
    for t in range(1, nf):
        a = np.where(duck[:, t] > duck[:, t - 1], 0.65, 0.07)
        duck[:, t] = duck[:, t - 1] + a * (duck[:, t] - duck[:, t - 1])
    gain = (10 ** (-duck / 20)).astype(np.float32)
    mid2 = istft(T * gain, len(mid))
    return np.stack([mid2 + side, mid2 - side]).astype(np.float32)

# roundtrip sanity: silence key must return the target ~unchanged
_probe = np.stack([np.sin(2 * np.pi * 440 * np.arange(N) / SR),
                   np.sin(2 * np.pi * 440 * np.arange(N) / SR)]).astype(np.float32) * 0.2
_rt = spectral_duck(_probe, np.zeros(N, np.float32), 4.0)
_err = float(np.sqrt(np.mean((_rt - _probe) ** 2)) / np.sqrt(np.mean(_probe ** 2)))
print(f"ducker roundtrip rel err (silent key): {_err:.4f}")
assert _err < 0.05, "STFT roundtrip broken"
del _probe, _rt

# ================= instrumental =================
def stem(name):
    return pad2(load(os.path.join(WAV, f"stem-{name}.wav")))

carve = Pedalboard([PeakFilter(cutoff_frequency_hz=3000.0, gain_db=-2.0, q=0.7)])

def widen(x, side_db):
    mid = (x[0] + x[1]) * 0.5; side = (x[0] - x[1]) * 0.5 * (10 ** (side_db / 20))
    return np.stack([mid + side, mid - side]).astype(np.float32)

arp = stem("arp") * 0.85
arp = carve(arp, SR)
arp = widen(arp, 2.0)
arp = spectral_duck(arp, KEY, 4.0)

lead_stem = stem("lead") * 0.9
lead_stem = carve(lead_stem, SR)
lead_stem = spectral_duck(lead_stem, KEY, 4.5)

sparkle = stem("sparkle") * 0.7
sparkle = spectral_duck(sparkle, KEY, 4.0)

inst = arp + lead_stem + sparkle + stem("pad") * 0.7 + stem("bass") * 1.0 + stem("drums") * 1.05
INST_GAINS = {"intro": 0.0, "verseA": -0.5, "chorusA": 0.0, "verseB": -0.5,
              "bridge": -2.0, "chorusB": 0.0, "outro": -1.0}
g = section_curve(INST_GAINS)
inst = inst * g[None, :]

# ================= solve vocal section gains to genre targets =================
# Targets are LUFS offsets (vocal minus instrumental, while singing).
# The solver works in plain RMS; BIAS is the LUFS-minus-RMS offset measured
# on the v2 JP first pass (K-weighting favours the presence-heavy vocal and
# discounts the low-heavy backing): verseA +2.6, chorusA +2.6, verseB +2.0,
# bridge +2.3, chorusB +2.5, outro +3.8.
TARGET = {"verseA": 1.0, "chorusA": 0.5, "verseB": 1.0, "bridge": 1.5, "chorusB": 0.5, "outro": 1.5}
BIAS = {"verseA": 2.6, "chorusA": 2.6, "verseB": 2.0, "bridge": 2.3, "chorusB": 2.5, "outro": 3.8}
vgains = {"intro": 0.0}
for name, a, b in SEC:
    if name == "intro":
        continue
    off = rms_db(bus, a, b) - rms_db(inst, a, b)
    vgains[name] = float(np.clip(TARGET[name] - BIAS[name] - off, -24.0, 8.0))
print("vocal section gains (dB):", {k: round(v, 1) for k, v in vgains.items()})
gv = section_curve(vgains, ramp=0.2)
bus = bus * gv[None, :]
print("post-gain offsets vocal-inst (RMS dB):",
      {name: round(rms_db(bus, a, b) - rms_db(inst, a, b), 1) for name, a, b in SEC if name != "intro"})

save(os.path.join(OUT, "vocal_bus.wav"), bus)
save(os.path.join(OUT, "instrumental.wav"), inst)
full = inst + bus
full *= 0.89 / max(float(np.abs(full).max()), 1e-6)
save(os.path.join(OUT, "full_premaster.wav"), full)
for _f in ("lead_fairy.wav", "lead_proc.wav", "lead_sat.wav", "oct_ch.wav"):
    _p = os.path.join(OUT, _f)
    if os.path.exists(_p):
        os.remove(_p)

# ================= master: house chain + loudnorm to -14 LUFS / -1 dBTP =================
def master(inp, mastered):
    run([sys.executable, os.path.join(STACK, "tools/music-production/pedalboard_master.py"), inp, mastered])

def loudnorm_json(path):
    err = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "loudnorm=print_format=json",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    return json.loads(err[err.index("{"):err.rindex("}") + 1])

def finalize(mastered, out_mp3):
    m = loudnorm_json(mastered)
    off = -14.0 - float(m["input_i"])
    tmp = mastered.replace(".wav", "_ln.wav")
    if float(m["input_tp"]) + off <= -1.1:
        af = (f"loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
              f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={off:.2f}:linear=true")
    else:
        af = "loudnorm=I=-14:TP=-1.0:LRA=11"
    run(["ffmpeg", "-y", "-v", "error", "-i", mastered, "-af", af, "-ar", str(SR), tmp])
    v = loudnorm_json(tmp)
    if abs(float(v["input_i"]) + 14.0) > 0.35:  # trim pass: exact gain + true ceiling
        g = -14.0 - float(v["input_i"])
        tmp2 = tmp.replace(".wav", "_t.wav")
        run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-ar", str(SR),
             "-af", f"volume={g:.2f}dB,alimiter=limit=0.87:level=false:attack=0.5:release=20", tmp2])
        v2 = loudnorm_json(tmp2)
        if abs(float(v2["input_i"]) + 14.0) < abs(float(v["input_i"]) + 14.0) and float(v2["input_tp"]) <= -0.95:
            os.replace(tmp2, tmp); v = v2
        else:
            os.remove(tmp2)
    print(f"finalize {os.path.basename(out_mp3)}: LUFS={v['input_i']} TP={v['input_tp']}")
    run(["ffmpeg", "-y", "-v", "error", "-i", tmp, "-codec:a", "libmp3lame", "-b:a", "192k", out_mp3])
    os.remove(tmp)
    return None

master(os.path.join(OUT, "full_premaster.wav"), os.path.join(OUT, "full_mastered.wav"))
master(os.path.join(OUT, "instrumental.wav"), os.path.join(OUT, "instrumental_mastered.wav"))
finalize(os.path.join(OUT, "full_mastered.wav"), os.path.join(OUT, f"song-full-v2-{LANG}.mp3"))
finalize(os.path.join(OUT, "instrumental_mastered.wav"), os.path.join(OUT, "song-instrumental-v2.mp3"))
for _f in ("full_premaster.wav", "full_mastered.wav", "instrumental_mastered.wav"):
    _p = os.path.join(OUT, _f)
    if os.path.exists(_p):
        os.remove(_p)
print("mix v2 done:", LANG)
