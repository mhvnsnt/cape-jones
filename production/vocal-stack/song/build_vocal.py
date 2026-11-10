#!/usr/bin/env python3
"""Build the sung vocal for the Cape Jones dance song.
Method = the Mochiichao repo's own vocal stack, latest generation:
  - rubberband_autotune_v1.py / build_vocal_mix_v19.sh: NO WORLD resynthesis on
    the lead; per-note-segment Rubber Band pitch work, feminine shift decoupled
    from pitch (pass 1 formants move, pass 2 formants preserved).
Guide singer: espeak-ng Japanese (ja+f5 variant, pitch 99) — one mora at a time,
each mora time-fit to its note, then pitch-shifted to the exact melody note
(hard autotune by construction). Avanna/VOCALOID5 itself cannot run on this
Linux box (Windows/Mac licensed editor; the repo holds the method + chains,
not the installer or any voicebank) — this is the repo's documented
open-stack equivalent of the Avanna sound (see avanna_style.py header).
Outputs (mono 44.1k): lead_raw.wav, harmony_raw.wav, octave_raw.wav."""
import json, os, subprocess, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_data import KANA, TOTAL_BARS, BAR_SEC

SR = 44100
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
MORA_DIR, SEG_DIR, VOC_DIR = (os.path.join(WORK, d) for d in ("mora", "seg", "vocal"))
for d in (MORA_DIR, SEG_DIR, VOC_DIR):
    os.makedirs(d, exist_ok=True)
FORMANT_CAP = 1.7
TOTAL_SEC = TOTAL_BARS * BAR_SEC
BEAT = 60.0 / 152.0

def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def read_wav(p):
    w = wave.open(p); sr = w.getframerate(); n = w.getnframes(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    if ch > 1: x = x.reshape(-1, ch).mean(axis=1)
    assert sr == SR, (p, sr)
    return x

def write_wav(p, x):
    x = np.clip(x, -0.98, 0.98)
    w = wave.open(p, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()

def measure_f0(x):
    win = int(0.05 * SR)
    if len(x) < win: return 0.0
    ests = []
    hop = int(0.02 * SR)
    for s in range(0, len(x) - win, hop):
        seg = x[s:s + win]
        if np.sqrt((seg ** 2).mean()) < 0.05: continue
        seg = seg * np.hanning(win)
        ac = np.correlate(seg, seg, 'full')[win - 1:]
        lo, hi = int(SR / 600), int(SR / 150)
        ests.append(SR / (lo + int(np.argmax(ac[lo:hi]))))
    return float(np.median(ests)) if ests else 0.0

# ---- 1. mora library ----
notes = json.load(open(os.path.join(WORK, 'vocal_notes.json')))
morae = sorted({n["mora"] for n in notes if n["mora"] != "xtu"})
guide = {}
for m in morae:
    raw = os.path.join(MORA_DIR, f"{m}_raw.wav")
    out = os.path.join(MORA_DIR, f"{m}.wav")
    if not os.path.exists(out):
        run(["espeak-ng", "-v", "ja+f5", "-p", "99", "-s", "140", "-w", raw, KANA[m]])
        run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-ar", str(SR), out])
    x = read_wav(out)
    # trim to -42 dB of peak with 12 ms margins
    pk = np.abs(x).max()
    idx = np.where(np.abs(x) > pk * 0.008)[0]
    if len(idx):
        a = max(0, idx[0] - int(0.012 * SR)); b = min(len(x), idx[-1] + int(0.012 * SR))
        x = x[a:b]
    write_wav(out, x)
    guide[m] = (out, measure_f0(x), len(x) / SR)
print("mora library:", {m: round(guide[m][1]) for m in morae})

def seg_for(mora, target_f, dur):
    """Processed mora segment at (freq, duration), cached."""
    key = f"{mora}_{int(round(target_f))}_{int(round(dur * 1000))}"
    out = os.path.join(SEG_DIR, key + ".wav")
    if os.path.exists(out):
        return read_wav(out)
    src, f0, src_dur = guide[mora]
    tmp1 = os.path.join(SEG_DIR, key + "_t.wav")
    run(["rubberband", "-t", f"{dur / src_dur:.4f}", "-c", "6", src, tmp1])
    r = target_f / f0
    cur = tmp1
    r1 = min(r, FORMANT_CAP)
    if abs(r1 - 1.0) > 0.01:
        tmp2 = os.path.join(SEG_DIR, key + "_p1.wav")
        run(["rubberband", "-f", f"{r1:.4f}", "-c", "6", cur, tmp2]); cur = tmp2
    r2 = r / r1
    if abs(r2 - 1.0) > 0.01:
        tmp3 = os.path.join(SEG_DIR, key + "_p2.wav")
        run(["rubberband", "-f", f"{r2:.4f}", "-F", "-c", "6", cur, tmp3]); cur = tmp3
    x = read_wav(cur)
    write_wav(out, x)
    return x

def place(buf, x, start_sec, fade=0.010):
    s = int(start_sec * SR); e = min(len(buf), s + len(x))
    if e <= s: return
    x = x[:e - s].copy()
    n = min(int(fade * SR), len(x) // 2)
    if n > 0:
        x[:n] *= np.linspace(0, 1, n); x[-n:] *= np.linspace(1, 0, n)
    buf[s:e] += x

SCALE = [0, 2, 4, 5, 7, 9, 11]
def third_up(midi):
    deg = SCALE.index(midi % 12); octv, _ = divmod(midi, 12)
    nd = deg + 2
    return (octv + nd // 7) * 12 + SCALE[nd % 7]

lead = np.zeros(int(TOTAL_SEC * SR), dtype=np.float32)
harm = np.zeros_like(lead); octa = np.zeros_like(lead)
freq = lambda m: 440.0 * 2 ** ((m - 69) / 12)
for n in notes:
    st = n["start_beat"] * BEAT; dur = n["dur_beats"] * BEAT
    if n["mora"] == "xtu":
        continue  # glottal stop = a cut of silence, the note still takes its time
    x = seg_for(n["mora"], freq(n["midi"]), dur * 1.03)
    place(lead, x, st)
    if n["section"] in ("chorusB", "outro"):
        place(harm, seg_for(n["mora"], freq(third_up(n["midi"])), dur * 1.03), st)
        place(octa, seg_for(n["mora"], freq(n["midi"]) * 2, dur * 1.03), st)
for buf in (lead, harm, octa):
    pk = float(np.abs(buf).max())
    if pk > 0.89:
        buf *= 0.89 / pk
write_wav(os.path.join(VOC_DIR, "lead_raw.wav"), lead)
write_wav(os.path.join(VOC_DIR, "harmony_raw.wav"), harm)
write_wav(os.path.join(VOC_DIR, "octave_raw.wav"), octa)
print("vocal buffers written; lead peak", float(np.abs(lead).max()))
