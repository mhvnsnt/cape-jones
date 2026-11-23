#!/usr/bin/env python3
"""Derive the Rig Jones 2 (V3) keys from the V2 mixed keys.
Bone mapping (V2 -> V3):
  armR -> upperArmR (same target); forearmR = armR + elbow bend.
    The raise swings the arm DOWN-negative (rest -90, full raise -259);
    the forearm lags by up to +12 deg so the elbow bends slightly.
  handR/handL -> same targets (relative rotation, same convention).
  legR/legL -> thighR/thighL (same targets); shin = leg (straight).
  cape: follows the TORSO (hangs), never the arm. Sway trails the arm's
    MOTION only: proportional to arm angular velocity, capped +/-1.5 deg
    (neck x0.5, mid x1.0, tip x1.5), so it trails while the arm moves
    and settles straight when the arm holds.
Slot schedule (new in V3):
  handR/handL: V2 hand names ("Hand_6_Relaxed" -> "Relaxed", "Hand_7_Grip").
  mouth: Closed f1-120, Open f121-168 (raise+click), Open f169-205 (gag),
         Closed f206-312, Smile f313-379 (lower), Open f380-428 (nod),
         Closed f429-480.
  eyes: "Pupils" when V2 pupils is true, else "Normal".
  remote: V2 remote bool. forearmR/L: "Standard".
Also writes v3_test_keys.json — the 120f short test (arm raise + close-up
+ wide, slot cycling on camera):
  f1-24   wide rest: hands Relaxed, mouth Closed, eyes Normal.
  f25-48  arm raise, camera medium: handR Fist->Open->Point->Grip (6f each),
          mouth Open.
  f49-72  close-up: mouth Closed->Open->Shout->Smile (6f each),
          eyes Normal->Pupils at f61.
  f73-96  arm lower, camera medium: handL Point->Open->Fist (8f each),
          handR Grip + remote from f85.
  f97-120 wide settle: hands Relaxed, mouth Closed, eyes Normal.
"""
import json

WD = "/home/hatch/workspace/_cape-jones-parking-lot-2d"
V3 = f"{WD}/v3-swap-system"

HAND_NAMES = ["Fist", "FistBack", "Open", "Point", "Point2", "Relaxed", "Grip"]


def hand_variant(v2name):
    # "Hand_6_Relaxed" -> "Relaxed"
    return v2name.split("_", 2)[2]


def mouth_for_frame(f):
    if f <= 120:
        return "Closed"
    if f <= 205:
        return "Open"
    if f <= 312:
        return "Closed"
    if f <= 379:
        return "Smile"
    if f <= 428:
        return "Open"
    return "Closed"


def elbow_bend(arm_target):
    # raise amount 0..1 as the arm swings from -90 down to -259
    raise_amt = max(0.0, min(1.0, (-90.0 - arm_target) / 170.0))
    return 12.0 * raise_amt


def map_keys(v2keys):
    out = []
    for rec in v2keys:
        b = rec["bones"]
        nb = {
            "pelvis": b["pelvis"], "torso": b["torso"], "neck": b["neck"],
            "head": b["head"],
            "upperArmR": b["armR"],
            "forearmR": b["armR"] + elbow_bend(b["armR"]),
            "handR": b["handR"],
            "upperArmL": b["armL"],
            "forearmL": b["armL"] + elbow_bend(b["armL"]),
            "handL": b["handL"],
            "thighR": b["legR"], "shinR": b["legR"],
            "thighL": b["legL"], "shinL": b["legL"],
            "capeNeck": -90.0, "capeMid": -90.0, "capeTip": -90.0,
        }
        sw = rec["swaps"]
        out.append({
            "frame": rec["frame"], "bones": nb, "root": rec["root"],
            "camera": rec["camera"],
            "slots": {
                "handR": hand_variant(sw["handR"]),
                "handL": hand_variant(sw["handL"]),
                "mouth": mouth_for_frame(rec["frame"]),
                "eyes": "Pupils" if sw["pupils"] else "Normal",
                "remote": bool(sw["remote"]),
                "forearmR": "Standard", "forearmL": "Standard",
            },
        })
    # Cape: follows the TORSO (hangs), never the arm. The old mapping
    # copied V2's spring (capeTop/capeTip), which swung the whole cape
    # -20 deg with the arm raise — the "cape lifts with the arm" the
    # owner rejected. Now the cape only trails the arm's MOTION: sway is
    # proportional to arm angular velocity, capped at +/-3 deg, so the
    # cape trails while the arm moves and settles straight when it
    # holds. Neck (pinned at the shoulders) moves least, tip most.
    # Lean compensation (added 2026-11-23): the cape chain is parented
    # to the torso, so without it the whole cape swings RIGIDLY with a
    # torso lean — during the hero-shift lean (+/-3 deg) the tip swung
    # 0.82 from the top. A hanging cape does not do that: the top is
    # pinned at the shoulders and follows the lean, the rest hangs
    # straight down. So the lean is compensated progressively down the
    # chain (neck 0, mid 1/2, tip full) and the tip hangs vertical.
    for i, rec in enumerate(out):
        if i == 0:
            vel = 0.0
        else:
            df = rec["frame"] - out[i - 1]["frame"]
            vel = (rec["bones"]["upperArmR"]
                   - out[i - 1]["bones"]["upperArmR"]) / max(1, df)
        sway = max(-1.5, min(1.5, vel * 0.45))
        lean = rec["bones"]["torso"] - 90.0
        rec["bones"]["capeNeck"] = -90.0 + sway * 0.5
        rec["bones"]["capeMid"] = -90.0 + sway - lean * 0.5
        rec["bones"]["capeTip"] = -90.0 + sway * 1.5 - lean
    return out


v2 = json.load(open(f"{WD}/rig/mixed_keys.json"))
v3keys = map_keys(v2["keys"])
json.dump({"frames": 480, "name": "v3", "outdir": "v3-frames", "keys": v3keys},
          open(f"{V3}/v3_keys.json", "w"))
print("v3_keys.json:", len(v3keys), "keyframes")


# ---- short test keys (120f, explicit, on twos) --------------------------
def key(frame, armR=-90.0, armL=-90.0, cape=-90.0, cam=None,
        handR="Relaxed", handL="Relaxed", mouth="Closed", eyes="Normal",
        remote=False, head=90.0):
    return {"frame": frame,
            "bones": {"pelvis": 90, "torso": 90.0, "neck": 90, "head": head,
                      "upperArmR": armR, "forearmR": armR + elbow_bend(armR),
                      "handR": -90, "upperArmL": armL,
                      "forearmL": armL + elbow_bend(armL), "handL": -90,
                      "thighR": -90, "shinR": -90, "thighL": -90, "shinL": -90,
                      "capeNeck": cape, "capeMid": cape, "capeTip": cape},
            "root": [0.0, 0.0],
            "camera": cam or {"ortho": 71.0, "x": 0.0, "y": 10.08},
            "slots": {"handR": handR, "handL": handL, "mouth": mouth,
                      "eyes": eyes, "remote": remote,
                      "forearmR": "Standard", "forearmL": "Standard"}}


WIDE = {"ortho": 71.0, "x": 0.0, "y": 10.08}
MED = {"ortho": 34.0, "x": -0.5, "y": 8.6}
MED2 = {"ortho": 34.0, "x": 0.5, "y": 8.6}
CLOSE = {"ortho": 26.0, "x": 0.0, "y": 9.6}
test = []
# f1-24 wide rest
for f in range(1, 25, 2):
    test.append(key(f))
# f25-48 arm raise, handR cycles, mouth Open
for i, f in enumerate(range(25, 49, 2)):
    arm = -90.0 + (-250.0 + 90.0) * (i / 11.0)
    hr = ["Fist", "Open", "Point", "Grip"][min(3, i // 3)]
    test.append(key(f, armR=arm,
                    cam=MED, handR=hr, mouth="Open"))
# f49-72 close-up, mouth cycles, eyes -> Pupils at f61
for i, f in enumerate(range(49, 73, 2)):
    mo = ["Closed", "Open", "Shout", "Smile"][min(3, i // 3)]
    ey = "Pupils" if f >= 61 else "Normal"
    test.append(key(f, armR=-250.0, cam=CLOSE, handR="Grip",
                    mouth=mo, eyes=ey, head=94.0))
# f73-96 arm lower, handL cycles, remote from f85
for i, f in enumerate(range(73, 97, 2)):
    arm = -250.0 + (250.0 - 90.0) * (i / 11.0)
    hl = ["Point", "Open", "Fist"][min(2, i // 4)]
    test.append(key(f, armR=arm,
                    cam=MED2, handR="Grip", handL=hl, mouth="Open",
                    remote=(f >= 85)))
# f97-120 wide settle
for f in range(97, 121, 2):
    test.append(key(f))
# Cape: same rule as the full cut — hangs from the torso, trails the
# arm's motion only (velocity-proportional sway, +/-1.5 deg max),
# with progressive lean compensation (neck 0, mid 1/2, tip full) so
# the tip hangs vertical when the torso leans.
for i, rec in enumerate(test):
    if i == 0:
        vel = 0.0
    else:
        df = rec["frame"] - test[i - 1]["frame"]
        vel = (rec["bones"]["upperArmR"]
               - test[i - 1]["bones"]["upperArmR"]) / max(1, df)
    sway = max(-1.5, min(1.5, vel * 0.45))
    lean = rec["bones"]["torso"] - 90.0
    rec["bones"]["capeNeck"] = -90.0 + sway * 0.5
    rec["bones"]["capeMid"] = -90.0 + sway - lean * 0.5
    rec["bones"]["capeTip"] = -90.0 + sway * 1.5 - lean
json.dump({"frames": 120, "name": "v3-test", "outdir": "v3-test-frames",
           "keys": test}, open(f"{V3}/v3_test_keys.json", "w"))
print("v3_test_keys.json:", len(test), "keyframes")
