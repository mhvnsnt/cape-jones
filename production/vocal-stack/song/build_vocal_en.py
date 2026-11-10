#!/usr/bin/env python3
"""English vocal for the Cape Jones dance song (v2 companion to build_vocal.py).
Same repo method as the Japanese take: espeak-ng guide voice (en+f5),
one syllable at a time, each syllable time-fit and pitch-placed onto the
written melody with Rubber Band per rubberband_autotune_v1.py / v19
(hard autotune by construction; formant lift x1.7 decoupled from pitch).
English lines are syllable-adapted to the SAME notes/durations as the
Japanese phrases in song_data.py (counts asserted per phrase).
Outputs (mono 44.1k) into build/vocal_en/: lead_raw.wav, harmony_raw.wav,
octave_raw.wav."""
import json, os, subprocess, wave
import numpy as np
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_data import PHRASES, TOTAL_BARS, BAR_SEC

SR = 44100
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
MORA_DIR, SEG_DIR, VOC_DIR = (os.path.join(WORK, d) for d in ("mora_en", "seg_en", "vocal_en"))
for d in (MORA_DIR, SEG_DIR, VOC_DIR):
    os.makedirs(d, exist_ok=True)
FORMANT_CAP = 1.7
TOTAL_SEC = TOTAL_BARS * BAR_SEC
BEAT = 60.0 / 152.0

# English syllable fragments, one per note, aligned to song_data.PHRASES order.
EN_FRAGS = [
 # verseA
 ["In", "the", "morn", "ing", "yard", "he", "is", "danc", "ing", "all", "a", "lone"],
 ["Cape", "is", "flut", "ter", "ing", "his", "face", "so", "dead", "se", "ri", "ous"],
 ["E", "ven", "if", "the", "whole", "world", "chan", "ges", "he", "nev", "er", "ev", "er", "does"],
 ["On", "ly", "his", "feet", "keep", "the", "beat", "and", "the", "beat", "goes", "all", "day", "long"],
 # chorusA
 ["Cape", "Jones", "dance", "and", "dance", "ev", "ree", "bod", "ee", "come", "and", "dance", "dance"],
 ["And", "when", "the", "co", "lors", "change", "you", "know", "the", "sky", "chan", "ges", "too"],
 ["Cape", "Jones", "spin", "and", "spin", "ev", "ree", "bod", "ee", "come", "and", "spin", "spin"],
 ["To", "mor", "row", "same", "old", "place", "and", "the", "same", "old", "dance", "a", "gain"],
 # verseB
 ["In", "his", "pock", "et", "there's", "a", "lit", "tle", "pet", "and", "it", "beeps", "all", "day"],
 ["Bat", "ter", "eez", "run", "ning", "low", "and", "he", "duz", "unt", "care", "at", "all"],
 ["Be", "fore", "din", "ner", "time", "and", "af", "ter", "din", "ner", "time", "he", "danc", "es"],
 ["The", "same", "old", "step", "the", "dream", "step", "the", "same", "old", "step", "ev", "ree", "day"],
 # bridge
 ["Day", "turns", "in", "to", "night", "and", "the", "night", "turns", "to", "morn", "ing"],
 ["L", "E", "D", "lights", "are", "shi", "ning", "blue", "and", "pink", "and", "green", "to", "night"],
 ["The", "on", "ly", "thing", "that", "chan", "ges", "is", "the", "world"],
 # chorusB (same lines as chorusA)
 ["Cape", "Jones", "dance", "and", "dance", "ev", "ree", "bod", "ee", "come", "and", "dance", "dance"],
 ["And", "when", "the", "co", "lors", "change", "you", "know", "the", "sky", "chan", "ges", "too"],
 ["Cape", "Jones", "spin", "and", "spin", "ev", "ree", "bod", "ee", "come", "and", "spin", "spin"],
 ["To", "mor", "row", "same", "old", "place", "and", "the", "same", "old", "dance", "a", "gain"],
 # outro
 ["He", "is", "al", "ways", "stand", "ing", "right", "here"],
 ["Cape", "Jones", "dance", "ev", "ree", "bod", "ee", "Cape", "Jones", "dance"],
 ["La", "la", "la", "la", "la", "la", "laa"],
]
EN_LINES = [
 "In the morning yard he is dancing all alone",
 "Cape is fluttering, his face so dead serious",
 "Even if the whole world changes, he never, ever does",
 "Only his feet keep the beat, and the beat goes all day long",
 "Cape Jones, dance and dance, everybody come and dance, dance!",
 "And when the colors change, you know the sky changes too",
 "Cape Jones, spin and spin, everybody come and spin, spin!",
 "Tomorrow, same old place, and the same old dance again",
 "In his pocket there's a little pet and it beeps all day",
 "Battery's running low and he doesn't care at all",
 "Before dinner time and after dinner time, he dances",
 "The same old step, the dream step, the same old step every day",
 "Day turns into night and the night turns to morning",
 "L-E-D lights are shining blue and pink and green tonight",
 "The only thing that changes is the world",
 "Cape Jones, dance and dance, everybody come and dance, dance!",
 "And when the colors change, you know the sky changes too",
 "Cape Jones, spin and spin, everybody come and spin, spin!",
 "Tomorrow, same old place, and the same old dance again",
 "He is always standing right here",
 "Cape Jones, dance, everybody, Cape Jones, dance",
 "La la la la la la laa",
]
assert len(EN_FRAGS) == len(PHRASES) == len(EN_LINES)

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

# ---- build the note list (fragment, midi, start_beat, dur_beats, section) ----
notes = []
for p, frags in zip(PHRASES, EN_FRAGS):
    assert len(frags) == len(p["notes"]), (p["section"], p["start_bar"], len(frags), len(p["notes"]))
    t = p["start_bar"] * 4.0
    for frag, (midi, dur) in zip(frags, p["notes"]):
        notes.append(dict(mora=frag, midi=midi, start_beat=t, dur_beats=dur, section=p["section"]))
        t += dur
json.dump(notes, open(os.path.join(WORK, "vocal_notes_en.json"), "w"))

# ---- 1. syllable guide library ----
frags = sorted({n["mora"] for n in notes})
guide = {}
for m in frags:
    safe = m.replace("'", "")
    raw = os.path.join(MORA_DIR, f"{safe}_raw.wav")
    out = os.path.join(MORA_DIR, f"{safe}.wav")
    if not os.path.exists(out):
        run(["espeak-ng", "-v", "en+f5", "-p", "99", "-s", "140", "-w", raw, m])
        run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-ar", str(SR), out])
    x = read_wav(out)
    pk = np.abs(x).max()
    idx = np.where(np.abs(x) > pk * 0.008)[0]
    if len(idx):
        a = max(0, idx[0] - int(0.012 * SR)); b = min(len(x), idx[-1] + int(0.012 * SR))
        x = x[a:b]
    write_wav(out, x)
    guide[m] = (out, measure_f0(x), len(x) / SR)
print("syllable library:", {m: round(guide[m][1]) for m in frags})

def seg_for(mora, target_f, dur):
    safe = mora.replace("'", "")
    key = f"{safe}_{int(round(target_f))}_{int(round(dur * 1000))}"
    out = os.path.join(SEG_DIR, key + ".wav")
    if os.path.exists(out):
        return read_wav(out)
    src, f0, src_dur = guide[mora]
    if f0 <= 0:  # unpitched fragment fallback: nominal 300 Hz
        f0 = 300.0
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
print("EN vocal buffers written; lead peak", float(np.abs(lead).max()))
