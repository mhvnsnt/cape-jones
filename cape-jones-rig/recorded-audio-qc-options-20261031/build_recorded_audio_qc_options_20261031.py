#!/usr/bin/env python3
"""Workstream 3: recorded audio + QC ruling options (2026-10-31).
SYNTHESIZED final mix only — no recorded human voice exists locally, no repo
song audio was pulled in, no script dialogue is invented here.
Music is an ORIGINAL C-major bed (I-V-vi-IV pattern, no lyrics, no vocal),
built at BOTH tempos so Mars can pick without a silent stretch.
Mix target: -14 LUFS integrated, true-peak ceiling -1.5 dB.
Stems are reported solo; only the MIX is normalised to -14.
New dated folder only; nothing overwritten, no repo push.
"""
import json, math, os, re, subprocess, sys
import numpy as np
from scipy.io import wavfile

R = "/home/hatch/workspace/cape-jones-rig"
O = os.path.join(R, "recorded-audio-qc-options-20261031")
SR = 48000

def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12.0)

def env(n, attack=0.01, decay=0.3):
    t = np.arange(n) / SR
    a = np.minimum(1.0, t / max(attack, 1e-4))
    d = np.exp(-t / max(decay, 1e-4))
    return a * d

def tone(freq, dur, amp=0.3, harmonics=((1, 1.0), (2, 0.3), (3, 0.12))):
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for mult, a in harmonics:
        sig += a * np.sin(2 * np.pi * freq * mult * t)
    sig *= env(n, attack=0.01, decay=max(dur * 0.6, 0.2))
    return amp * sig

def noise_burst(dur, amp=0.3, lowpass_steps=8):
    rng = np.random.default_rng(20261031)
    n = int(dur * SR)
    x = rng.standard_normal(n)
    # crude lowpass: cumulative moving average
    k = np.ones(lowpass_steps) / lowpass_steps
    x = np.convolve(x, k, mode="same")
    x = x / (np.max(np.abs(x)) + 1e-9)
    return amp * x * env(n, attack=0.005, decay=dur * 0.5)

def kick(dur=0.22, amp=0.9):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 50 + 70 * np.exp(-t / 0.03)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return amp * np.sin(ph) * np.exp(-t / 0.08)

def add(dst, src, start_sec):
    i = int(start_sec * SR)
    j = min(len(dst), i + len(src))
    if j > i:
        dst[i:j] += src[: j - i]

def stereo(mono, pan=0.0):
    # pan -1 left .. +1 right, equal-power-ish
    l = mono * math.cos((pan + 1) * math.pi / 4)
    r = mono * math.sin((pan + 1) * math.pi / 4)
    # keep centre content present in both: blend
    return np.stack([l + 0.35 * mono, r + 0.35 * mono], axis=1)

def write_wav(path, arr):
    # arr: (n,2) float; normalise only against hard clip, never beyond 0.99
    peak = np.max(np.abs(arr)) if arr.size else 0.0
    if peak > 0.99:
        arr = arr * (0.99 / peak)
    wavfile.write(path, SR, (np.clip(arr, -1, 1) * 32767).astype(np.int16))
    return float(peak)

def build_tempo(bpm, outdir):
    beat = 60.0 / bpm
    bars = 8
    total = bars * 4 * beat
    n = int(total * SR)
    music = np.zeros(n)
    sfx = np.zeros(n)
    amb = np.zeros(n)
    beep = np.zeros(n)
    # ---- ambience: brown noise, low ----
    rng = np.random.default_rng(7)
    white = rng.standard_normal(n)
    brown = np.cumsum(white)
    brown = brown - np.mean(brown)
    brown = brown / (np.max(np.abs(brown)) + 1e-9)
    amb += 0.5 * brown
    # ---- music: C major, chords C G Am F | C G F C ----
    chords = [
        [60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 65],
        [60, 64, 67], [55, 59, 62], [53, 57, 65], [60, 64, 67],
    ]
    melody = [64, 67, 69, 67, 65, 64, 62, 60,
              64, 67, 69, 72, 71, 67, 64, 60,
              64, 67, 69, 67, 65, 64, 62, 60,
              67, 69, 72, 71, 67, 64, 62, 60]
    for bar, chord in enumerate(chords):
        t0 = bar * 4 * beat
        for note in chord:
            add(music, tone(midi(note), 4 * beat, amp=0.10), t0)
        # bass on beats 1 and 3
        for b in (0, 2):
            add(music, tone(midi(chord[0] - 12), beat * 0.9, amp=0.28,
                           harmonics=((1, 1.0), (2, 0.15))), t0 + b * beat)
        # kick every beat, hat on off-beats
        for b in range(4):
            add(music, kick(amp=0.55), t0 + b * beat)
            add(music, noise_burst(0.05, amp=0.06, lowpass_steps=2),
                t0 + b * beat + beat / 2)
        for b in range(4):
            add(music, tone(midi(melody[bar * 4 + b]), beat * 0.85, amp=0.16),
                t0 + b * beat)
    # ---- sfx cues, placed by bar/beat (same musical position both tempos) ----
    add(sfx, tone(120, 0.35, amp=0.7, harmonics=((1, 1.0),)), 0.0)          # punch thump bar1 b1
    add(sfx, noise_burst(0.30, amp=0.55), 0.0)
    add(sfx, noise_burst(0.50, amp=0.35, lowpass_steps=16), 4 * beat)       # whoosh bar2 b1
    add(sfx, noise_burst(0.08, amp=0.45, lowpass_steps=3), 8 * beat)        # step bar3 b1
    add(sfx, noise_burst(0.08, amp=0.40, lowpass_steps=3), 10 * beat)       # step bar3 b3
    for k, f in enumerate((300, 400, 500, 600)):                           # jump rise bar4
        add(sfx, tone(f, beat * 0.9, amp=0.22), 12 * beat + k * beat)
    for bar in range(4, 8):                                                # dance accents bars5-8
        add(sfx, tone(110, 0.25, amp=0.45, harmonics=((1, 1.0),)), bar * 4 * beat)
        add(beep, tone(880, 0.07, amp=0.30, harmonics=((1, 1.0),)), bar * 4 * beat)
        for b in range(1, 4):
            add(beep, tone(880, 0.05, amp=0.18, harmonics=((1, 1.0),)),
                bar * 4 * beat + b * beat)
    stems = {
        "dialogue": np.zeros((n, 2)),  # SILENCE placeholder — no recorded dialogue
        "sfx": stereo(sfx, 0.0),
        "music": stereo(music, 0.0),
        "ambience": stereo(amb, 0.0),
        "device_beep_metronome": stereo(beep, 0.0),
    }
    os.makedirs(outdir, exist_ok=True)
    peaks = {}
    for name, arr in stems.items():
        peaks[name] = write_wav(os.path.join(outdir, f"stem-{name}.wav"), arr)
    mix = (0.55 * stems["music"] + 0.80 * stems["sfx"] + 0.12 * stems["ambience"]
           + 0.25 * stems["device_beep_metronome"])
    raw_path = os.path.join(outdir, "mix-raw.wav")
    write_wav(raw_path, mix)
    return {"bpm": bpm, "beat_sec": beat, "duration_sec": total,
            "stem_peaks": peaks, "raw_path": raw_path, "outdir": outdir}

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def measure_ebur128(path):
    r = run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=framelog=quiet",
             "-f", "null", "-"])
    txt = r.stderr
    m = re.search(r"Integrated loudness:\s*I:\s*(-?[\d.]+)\s*LUFS", txt)
    tp = re.search(r"True peak:\s*Peak:\s*(-?[\d.]+)\s*dBFS", txt)
    lra = re.search(r"Loudness range:\s*LRA:\s*([\d.]+)\s*LU", txt)
    if m is None:
        # fallback: loudnorm print
        r2 = run(["ffmpeg", "-hide_banner", "-i", path, "-af",
                  "loudnorm=print_format=json", "-f", "null", "-"])
        j = re.search(r"\{.*\}", r2.stderr, re.S)
        d = json.loads(j.group(0)) if j else {}
        return {"integrated_lufs": float(d.get("input_i", "nan")),
                "true_peak_db": float(d.get("input_tp", "nan")),
                "lra_lu": float(d.get("input_lra", "nan")), "method": "loudnorm-fallback"}
    return {"integrated_lufs": float(m.group(1)),
            "true_peak_db": float(tp.group(1)) if tp else float("nan"),
            "lra_lu": float(lra.group(1)) if lra else float("nan"),
            "method": "ebur128"}

def loudnorm_measure(path):
    r = run(["ffmpeg", "-hide_banner", "-i", path, "-af",
             "loudnorm=print_format=json", "-f", "null", "-"])
    j = re.search(r"\{.*\}", r.stderr, re.S)
    return json.loads(j.group(0)) if j else {}

def normalise_to_minus14(raw_path, final_path):
    meas = loudnorm_measure(raw_path)
    cur = raw_path
    steps = [{"stage": "raw", "measured": meas}]
    for i in range(3):
        m = loudnorm_measure(cur)
        filt = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:"
                f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
                f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
        out = final_path if i == 0 else final_path.replace(".wav", f"-pass{i}.wav")
        r = run(["ffmpeg", "-hide_banner", "-y", "-i", cur, "-af", filt, out])
        if r.returncode != 0:
            raise RuntimeError(f"loudnorm failed: {r.stderr[-500:]}")
        ver = measure_ebur128(out)
        steps.append({"stage": f"loudnorm-pass{i}", "measured_before": m, "verify": ver})
        cur = out
        if abs(ver["integrated_lufs"] - (-14)) <= 0.3 and ver["true_peak_db"] <= -1.0:
            break
        # small linear gain correction, only if peak headroom allows
        gain = -14 - ver["integrated_lufs"]
        if ver["true_peak_db"] + gain > -1.0:
            break
        corr = out.replace(".wav", "-gaincorr.wav")
        r = run(["ffmpeg", "-hide_banner", "-y", "-i", out, "-af",
                 f"volume={gain:.2f}dB", corr])
        ver2 = measure_ebur128(corr)
        steps.append({"stage": "gain-correction", "gain_db": round(gain, 2), "verify": ver2})
        cur = corr
        if abs(ver2["integrated_lufs"] - (-14)) <= 0.3:
            break
    # final file must be exactly final_path
    if cur != final_path:
        run(["ffmpeg", "-hide_banner", "-y", "-i", cur, "-c:a", "pcm_s16le", final_path])
    final_ver = measure_ebur128(final_path)
    return final_ver, steps

def main():
    results = {}
    for bpm, sub in ((107, "stems-107bpm"), (152, "stems-152bpm")):
        outdir = os.path.join(O, sub)
        info = build_tempo(bpm, outdir)
        # stem solo measurements
        stem_meas = {}
        for name in ("dialogue", "sfx", "music", "ambience", "device_beep_metronome"):
            p = os.path.join(outdir, f"stem-{name}.wav")
            if name == "dialogue":
                stem_meas[name] = {"integrated_lufs": None, "note": "SILENCE placeholder — no recorded dialogue; ebur128 has no loudness to measure (-inf)"}
            else:
                stem_meas[name] = measure_ebur128(p)
        final_path = os.path.join(O, f"final-mix-{bpm}bpm-minus14lufs-20261031.wav")
        final_ver, steps = normalise_to_minus14(info["raw_path"], final_path)
        # also keep raw mix beside stems for audit
        run(["cp", info["raw_path"], os.path.join(outdir, "mix-raw.wav")])
        results[str(bpm)] = {"bpm": bpm, "duration_sec": round(info["duration_sec"], 4),
                             "beat_sec": round(info["beat_sec"], 4),
                             "beat_frames_24fps": round(info["beat_sec"] * 24, 2),
                             "stems": stem_meas, "stem_peaks": info["stem_peaks"],
                             "mix_final": final_ver, "mix_file": final_path,
                             "normalisation_steps": steps}
        print(f"{bpm} BPM: dur {info['duration_sec']:.2f}s mix {final_ver}")
    json.dump(results, open(os.path.join(O, "lufs-measurements-20261031.json"), "w"), indent=1)
    print("DONE")

if __name__ == "__main__":
    main()
