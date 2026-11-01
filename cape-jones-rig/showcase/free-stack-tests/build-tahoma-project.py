#!/usr/bin/env python3
"""Build a Tahoma2D/OpenToonz project folder for the Cape Jones 24-frame beat-grid test.

Steps (run AFTER Tahoma2D is extracted):
1. Copy the 24 PNG frames into the project inputs/ folder.
2. Write a beat-grid spec + xsheet-style column file (frames 1-24, beat markers 1,7,13,19).
3. If Tahoma2D ships a sample .tnz scene, adapt its structure; otherwise leave the
   scene as an import-ready level folder and record that the GUI open step is owed.
   NEVER claim a Tahoma GUI render that was not actually run and viewed.
"""
import json, os, shutil, sys

SRC_FRAMES = "/home/hatch/workspace/cape-jones-rig/showcase/free-stack-tests/frames-24"
OUT = "/home/hatch/workspace/cape-jones-rig/showcase/free-stack-tests/tahoma-cape-jones-24f"

def main():
    os.makedirs(os.path.join(OUT, "inputs"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "scenes"), exist_ok=True)
    for i in range(1, 25):
        shutil.copy(os.path.join(SRC_FRAMES, f"frame-{i:02d}.png"),
                    os.path.join(OUT, "inputs", f"frame-{i:02d}.png"))
    spec = {
        "project": "cape-jones-24f",
        "fps": 24,
        "frames": 24,
        "beat_markers": [1, 7, 13, 19],
        "columns": [
            {"column": 1, "level": "inputs/frame-##.png", "frames": "1-24",
             "note": "xsheet-style: one level, 24 cells, beat every 6 frames"},
        ],
        "source_plate": "rig-apose-v7c-clean-transparent.png",
        "limb_piece": "cut-limbs-v7c/Arm_Front_Lower.png",
        "status": "level folder ready; GUI scene open + render step recorded separately, not claimed here",
    }
    json.dump(spec, open(os.path.join(OUT, "xsheet-beat-grid-20261031.json"), "w"), indent=2)
    print("Tahoma project folder built:", OUT)
    print("frames copied:", len(os.listdir(os.path.join(OUT, "inputs"))))

if __name__ == "__main__":
    main()
