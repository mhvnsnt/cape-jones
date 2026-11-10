#!/usr/bin/env python3
"""v2 final mixes: v1 files are KEPT (not overwritten, not deleted) and marked
SUPERSEDED — v1 hit -14.0 LUFS but true peak -0.80/-0.90 dB, over the -1.5 dB
ceiling, because a plain makeup-gain step was applied after loudnorm.
v2 chain (standard mix-bus processing, stated plainly):
  raw mix -> acompressor(threshold -20 dB, ratio 4, attack 5 ms, release 120 ms)
          -> alimiter(limit 0.84) -> linear makeup gain to -14 LUFS.
Verification: ebur128 summary for integrated LUFS, loudnorm input_tp for
true peak. Acceptance: |I - (-14)| <= 0.3 LU AND TP <= -1.5 dB.
"""
import json, os, re, subprocess

O = "/home/hatch/workspace/cape-jones-rig/recorded-audio-qc-options-20261031"

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def meas(path):
    r = run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=framelog=quiet",
             "-f", "null", "-"])
    m = re.search(r"Integrated loudness:\s*\n\s*I:\s*(-?[\d.]+)\s*LUFS", r.stderr)
    lra = re.search(r"Loudness range:\s*\n\s*LRA:\s*([\d.]+)\s*LU", r.stderr)
    r2 = run(["ffmpeg", "-hide_banner", "-i", path, "-af",
              "loudnorm=print_format=json", "-f", "null", "-"])
    j = re.search(r"\{.*\}", r2.stderr, re.S)
    ln = json.loads(j.group(0)) if j else {}
    return {"integrated_lufs_ebur128": float(m.group(1)) if m else None,
            "integrated_lufs_loudnorm": float(ln["input_i"]) if "input_i" in ln else None,
            "true_peak_db_loudnorm": float(ln["input_tp"]) if "input_tp" in ln else None,
            "lra_lu": float(lra.group(1)) if lra else None}

def build_v2(bpm, sub):
    raw = os.path.join(O, sub, "mix-raw.wav")
    comp = f"/tmp/v2-comp-{bpm}.wav"
    r = run(["ffmpeg", "-hide_banner", "-y", "-i", raw, "-af",
             "acompressor=threshold=-20dB:ratio=4:attack=5:release=120,"
             "alimiter=limit=0.84:level=false", "-c:a", "pcm_s16le", comp])
    assert r.returncode == 0, r.stderr[-400:]
    m0 = meas(comp)
    gain = -14.0 - m0["integrated_lufs_ebur128"]
    final = os.path.join(O, f"final-mix-{bpm}bpm-minus14lufs-v2-20261031.wav")
    r = run(["ffmpeg", "-hide_banner", "-y", "-i", comp, "-af",
             f"volume={gain:.2f}dB", "-c:a", "pcm_s16le", final])
    assert r.returncode == 0, r.stderr[-400:]
    ver = meas(final)
    print(bpm, "comp", m0, "gain", round(gain, 2), "final", ver)
    return {"chain": "acompressor threshold=-20dB ratio=4 attack=5ms release=120ms -> "
                     "alimiter limit=0.84 -> linear makeup gain",
            "makeup_gain_db": round(gain, 2), "pre_gain_measure": m0,
            "final_measure": ver,
            "final_file": final,
            "accept": (ver["integrated_lufs_ebur128"] is not None
                       and abs(ver["integrated_lufs_ebur128"] + 14) <= 0.3
                       and ver["true_peak_db_loudnorm"] is not None
                       and ver["true_peak_db_loudnorm"] <= -1.5)}

out = {}
for bpm, sub in ((107, "stems-107bpm"), (152, "stems-152bpm")):
    stems = {}
    for name in ("dialogue", "sfx", "music", "ambience", "device_beep_metronome"):
        p = os.path.join(O, sub, f"stem-{name}.wav")
        stems[name] = ({"integrated_lufs": None, "true_peak_db": None,
                        "note": "SILENCE placeholder — no recorded dialogue; "
                                "Space Ghost workflow: Mars fills dialogue AFTER "
                                "episodes are built, so this stem is empty by design "
                                "at this stage, not a missing episode blocker."}
                       if name == "dialogue" else meas(p))
    out[str(bpm)] = {"bpm": bpm, "stems": stems, "mix_v2": build_v2(bpm, sub),
                     "mix_v1_superseded": {
                         "file": os.path.join(
                             O, f"final-mix-{bpm}bpm-minus14lufs-20261031.wav"),
                         "reason": "SUPERSEDED by v2: v1 integrated -14.0 LUFS but "
                                   "true peak -0.80 (107) / -0.90 (152) dB, over the "
                                   "-1.5 dB ceiling. Kept on disk, not deleted, not "
                                   "used as the delivery."}}
    # durations via ffprobe
    r = run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "csv=p=0", out[str(bpm)]["mix_v2"]["final_file"]])
    out[str(bpm)]["duration_sec"] = float(r.stdout.strip())
json.dump(out, open(os.path.join(O, "lufs-measurements-v2-20261031.json"), "w"), indent=1)
print("V2 DONE")
