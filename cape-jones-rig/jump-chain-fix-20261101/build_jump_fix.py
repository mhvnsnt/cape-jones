"""Jump chain fix, 2026-11-01. Reuses rig-chains build_chains.py verbatim except:
- JUMP takeoff + tuck-apex keys get top=("L","R"), so both arm chains are drawn
  AFTER head/torso (figure() top_arms path). All other keys unchanged, angles unchanged.
- Outputs go to this folder, not rig-chains-20261031 (original untouched).
No frames, motions, or keys are cut: the rebuilt chain has the same 62 frames.
"""
import sys, os, json
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig/rig-chains-20261031")
import build_chains as bc
OUT = "/home/hatch/workspace/cape-jones-rig/jump-chain-fix-20261101"
bc.OUT = OUT
bc.FR = os.path.join(OUT, "frames")
keys = bc.JUMP_KEYS
for k in keys:
    if k["name"] in ("jump takeoff", "jump tuck apex"):
        k["top"] = ("L", "R")
    print(k["name"], "top=", k["top"])
frames, meta, masters = bc.build("chain-jump-fixed", keys, n_inb=7, label="AIRBORNE",
    flight="flight line: crouch 0px->takeoff 30px->tuck apex 100px->land 0px")
n = bc.save_video("chain-jump-fixed", frames, meta, masters)
print("BUILT", n)
json.dump(meta, open(os.path.join(OUT, "chain-jump-fixed-xsheet-20261101.json"), "w"), indent=1)
