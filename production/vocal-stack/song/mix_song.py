#!/usr/bin/env python3
"""Mix + master the Cape Jones dance song.
Vocal chain = repo stack: digital_fairy_chain (Avanna bus, Pedalboard) ->
build_vocal_mix_v19.sh ffmpeg numbers (HP150, mud cut, presence stack,
de-esser, 4:1 comp, bit-crush parallel, slapback) -> v19 layer recipe
(harmony 0.5, octave HP250+chorus 0.35).
Master = repo pedalboard_master.py chain (HP30 -> comp -18dB 2:1 -> limiter),
then verified on meters and loudness-trimmed (that file's own warning).
Run with the music-pullin venv python (has pedalboard)."""
import os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_data import TOTAL_BARS, BAR_SEC

SR = 44100
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
VOC, WAV = os.path.join(W, "vocal"), os.path.join(W, "wav")
MIX = os.path.join(W, "mix"); os.makedirs(MIX, exist_ok=True)
TOTAL = TOTAL_BARS * BAR_SEC
STACK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocalstack")
sys.path.insert(0, os.path.join(STACK, "show/production/tooling/music-wave/tools"))
import digital_fairy_chain as dfc
from pedalboard import Pedalboard, Chorus, Delay, Reverb
from pedalboard.io import AudioFile

def run(cmd):
    subprocess.run(cmd, check=True)

def load(p):
    with AudioFile(p) as f:
        a = f.read(f.frames); sr = f.samplerate
    return np.ascontiguousarray(a[0], dtype=np.float32), sr  # first channel, mono view

def save(p, mono_or_stereo):
    a = mono_or_stereo
    if a.ndim == 1: a = a.reshape(1, -1)
    with AudioFile(p, "w", SR, a.shape[0]) as f:
        f.write(a.astype(np.float32))

def ff(inp, outp, filt):
    run(["ffmpeg", "-y", "-v", "error", "-i", inp, "-af", filt, "-ar", str(SR), outp])

N = int(TOTAL * SR)
def pad(x):
    y = np.zeros(N, dtype=np.float32); y[:min(N, len(x))] = x[:N]; return y

# ---------- vocal lead: fairy chain (avanna bus) then v19 ffmpeg stack ----------
lead, _ = load(os.path.join(VOC, "lead_raw.wav"))
lead = dfc.build_chain("avanna")(pad(lead).reshape(1, -1), SR)[0]
save(os.path.join(MIX, "lead_fairy.wav"), lead)
ff(os.path.join(MIX, "lead_fairy.wav"), os.path.join(MIX, "lead_proc.wav"),
   "highpass=f=150,equalizer=f=300:width_type=o:width=1.2:g=-5,"
   "equalizer=f=3000:width_type=o:width=1:g=6,equalizer=f=5000:width_type=o:width=1:g=6,"
   "equalizer=f=8000:width_type=o:width=1:g=6,equalizer=f=12000:width_type=s:width=1:g=4,"
   "deesser=i=0.6:f=0.16,acompressor=threshold=0.10:ratio=4:attack=5:release=80:makeup=2")
lead, _ = load(os.path.join(MIX, "lead_proc.wav")); lead = pad(lead)

harm, _ = load(os.path.join(VOC, "harmony_raw.wav"))
harm = dfc.build_chain("human")(pad(harm).reshape(1, -1), SR)[0] * 0.5
octa, _ = load(os.path.join(VOC, "octave_raw.wav"))
octa = pad(octa)
ff(os.path.join(VOC, "octave_raw.wav"), os.path.join(MIX, "oct_ch.wav"),
   "highpass=f=250,chorus=0.5:0.5:25|35:0.4|0.5:5|7:0.5|0.6,volume=0.35")
octa2, _ = load(os.path.join(MIX, "oct_ch.wav"))
octa = pad(octa2)

# bit-crush parallel on the lead (v19 sat layer)
ff(os.path.join(MIX, "lead_proc.wav"), os.path.join(MIX, "lead_sat.wav"),
   "acrusher=level_in=1:level_out=1:bits=10:mix=0.2,volume=0.5")
sat, _ = load(os.path.join(MIX, "lead_sat.wav")); sat = pad(sat)

# stereo vocal bus: lead centre, haas copy right, slapback+verb wet, layers
bus = np.zeros((2, N), dtype=np.float32)
bus[0] += lead; bus[1] += lead
d = int(0.012 * SR); bus[1, d:] += lead[:-d] * 0.30
bus[0] += harm; bus[1] += harm
bus[0] += octa; bus[1] += octa
bus[0] += sat; bus[1] += sat
wet = Pedalboard([Delay(delay_seconds=0.321, feedback=0.18, mix=0.28),
                  Reverb(room_size=0.35, wet_level=0.10, dry_level=0.0)])(bus.copy(), SR)
bus += wet * 0.5
save(os.path.join(MIX, "vocal_bus.wav"), bus)

# ---------- instrumental ----------
def stem(name):
    x, _ = load(os.path.join(WAV, f"stem-{name}.wav"))
    return pad(x if x.ndim == 1 else x)

parts = []
for name, gain in [("arp", 0.85), ("bass", 1.0), ("sparkle", 0.8), ("pad", 0.7), ("drums", 1.0)]:
    with AudioFile(os.path.join(WAV, f"stem-{name}.wav")) as f:
        a = f.read(f.frames)
    st = np.zeros((2, N), dtype=np.float32)
    for ch in range(2):
        src = a[ch] if a.shape[0] > 1 else a[0]
        st[ch, :min(N, len(src))] = src[:N] * gain
    parts.append(st)
# lead stem with ducking under the vocal (v19 melody carve, done as gain here)
with AudioFile(os.path.join(WAV, "stem-lead.wav")) as f:
    a = f.read(f.frames)
ld = np.zeros((2, N), dtype=np.float32)
g = np.ones(N, dtype=np.float32)
v0, v1 = int(4 * BAR_SEC * SR), int(42 * BAR_SEC * SR)
g[v0:v1] = 0.45
for ch in range(2):
    src = a[ch] if a.shape[0] > 1 else a[0]
    ld[ch, :min(N, len(src))] = src[:N] * g[:len(src)]
parts.append(ld)
inst = np.sum(parts, axis=0)
save(os.path.join(MIX, "instrumental.wav"), inst)

# ---------- full mix + master ----------
full = inst * 0.9 + bus * 1.15
save(os.path.join(MIX, "full_premaster.wav"), full)
save(os.path.join(MIX, "instrumental_premaster.wav"), inst)
run([sys.executable, os.path.join(STACK, "tools/music-production/pedalboard_master.py"),
     os.path.join(MIX, "full_premaster.wav"), os.path.join(MIX, "full_mastered.wav")])
run([sys.executable, os.path.join(STACK, "tools/music-production/pedalboard_master.py"),
     os.path.join(MIX, "instrumental_premaster.wav"), os.path.join(MIX, "instrumental_mastered.wav")])
print("mix done")
