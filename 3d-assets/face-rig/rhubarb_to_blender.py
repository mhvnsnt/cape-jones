#!/usr/bin/env python3
"""
rhubarb_to_blender.py — drive the CJ mouth kit from lip-sync data.

Consumes:
  - Rhubarb Lip Sync TSV  (start<TAB>end<TAB>shape, shapes A-H/X)
  - Rhubarb JSON          (mouthCues: [{start, end, value}])
  - Papagayo .dat         (MohoSwitch format, Preston Blair phoneme names)

...and keyframes CJ_MouthDriver["mouth_index"] with CONSTANT interpolation
(Telltale hard-cut swaps — no in-betweening, per the toon spec).

Mapping lives in rhubarb_map.json (shapes -> mouth indices).

Usage (inside Blender, kit linked/appended, driver present):
    blender -b shot.blend --python rhubarb_to_blender.py -- cues.tsv [fps]

Generate cues first:
    ./tools/rhubarb/rhubarb -o cues.tsv -d transcript.txt dialogue.wav
    # or with only basic shapes: --extendedShapes ""
"""
import bpy
import json
import os
import sys

MAP_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rhubarb_map.json")


def load_map():
    with open(MAP_FILE) as f:
        m = json.load(f)
    rmap = {k: v["mouth"] for k, v in m["rhubarb"].items()}
    pmap = {k: v for k, v in m["papagayo_preston_blair"].items() if not k.startswith("_")}
    return rmap, pmap


def parse_tsv(path):
    cues = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                parts = line.split()
            if len(parts) >= 3:
                try:
                    cues.append((float(parts[0]), float(parts[1]), parts[2].strip()))
                except ValueError:
                    continue
    return cues


def parse_rhubarb_json(path):
    with open(path) as f:
        d = json.load(f)
    cues = []
    for c in d.get("mouthCues", d if isinstance(d, list) else []):
        cues.append((float(c["start"]), float(c["end"]), str(c["value"]).strip()))
    return cues


def parse_papagayo_dat(path, pmap):
    # MohoSwitch: word lines "word start end n", then "frame PHONEME, ..." lines.
    cues = []
    phoneme_lines = []
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    for line in lines:
        if line and line[0].isdigit():
            phoneme_lines.append(line)
    for line in phoneme_lines:
        for chunk in line.split(","):
            chunk = chunk.strip()
            if not chunk or " " not in chunk:
                continue
            frame_s, phon = chunk.split(None, 1)
            try:
                cues.append((int(frame_s), int(frame_s) + 1, phon.strip()))
            except ValueError:
                continue
    return cues, True  # True = frame-based


def main():
    argv = sys.argv
    args = argv[argv.index("--") + 1:] if "--" in argv else []
    if not args:
        print("usage: rhubarb_to_blender.py -- cues.(tsv|json|dat) [fps]")
        return
    path = args[0]
    fps = float(args[1]) if len(args) > 1 else 24.0

    rmap, pmap = load_map()
    ext = os.path.splitext(path)[1].lower()
    frame_based = False
    if ext == ".json":
        cues = parse_rhubarb_json(path)
    elif ext == ".dat":
        cues, frame_based = parse_papagayo_dat(path, pmap)
    else:
        cues = parse_tsv(path)
    if not cues:
        print("no cues parsed from", path)
        return

    driver = bpy.data.objects.get("CJ_MouthDriver")
    if driver is None:
        print("CJ_MouthDriver not found — append the mouth kit first")
        return

    # clear old keys on mouth_index
    ad = driver.animation_data
    if ad and ad.action:
        for fc in [fc for fc in ad.action.fcurves if fc.data_path == '["mouth_index"]']:
            ad.action.fcurves.remove(fc)

    keyed = 0
    for start, end, shape in cues:
        if frame_based:
            idx = pmap.get(shape, 0)
            f0, f1 = float(start), float(end)
        else:
            idx = rmap.get(shape, rmap.get("X", 0))
            f0, f1 = start * fps, end * fps
        driver["mouth_index"] = idx
        driver.keyframe_insert(data_path='["mouth_index"]', frame=f0)
        # hold through the cue, then the next cue's key cuts (constant interp)
        keyed += 1

    # constant interpolation: hard Telltale cuts
    ad = driver.animation_data
    for fc in ad.action.fcurves:
        if fc.data_path == '["mouth_index"]':
            for kp in fc.keyframe_points:
                kp.interpolation = 'CONSTANT'

    scene = bpy.context.scene
    scene.render.fps = int(fps)
    print("keyed %d mouth swaps from %s @ %gfps" % (keyed, os.path.basename(path), fps))


if __name__ == "__main__":
    main()
