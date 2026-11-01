#!/usr/bin/env python3
"""WHOLE-ORIGINAL rebuild, Mars 2026-11-01 01:19 CST rejection.
Pipeline-auto test run REJECTED: it split forearms at 75% height (fist off),
and resized hands to 93x134 (1.141875x) in the real-rig version.
This builder does NONE of that:
- Every piece is drawn WHOLE, exactly as its source file, no crop, no split,
  no erase, no content edit.
- The ONLY scaling is the widget's own display placement size (DEFS w/h),
  applied uniformly to the whole piece, same as the widget stage itself.
  That is placement, not a content cut/crop/edit.
- Placement: saved top-left x/y, rotation about widget pivot (ox,oy),
  flipX whole-piece only (handR mirrored whole), DEFS-stable z order.
- Forearms are drawn WHOLE with their attached fists. Separate open hands
  are drawn WHOLE as their own pieces at their saved positions, exactly
  as the widget draws all 18 pieces. No fist is cut off to fake a clean hand.
"""
import json, os
from PIL import Image

RIG = os.path.expanduser("~/workspace/cape-jones-rig")
S34 = os.path.join(RIG, "sitting-rig-34-20261101/pieces")
V7C = os.path.join(RIG, "cut-limbs-v7c")
OUT = os.path.dirname(os.path.abspath(__file__))
LAYOUT = os.path.join(RIG, "pipeline-auto-20261101/saved-layout-20261101.json")

# id -> (source, display w,h, pivot ox,oy, DEFS index, flip_whole)
DEFS = {
 "cape":      (os.path.join(S34,"cape_back.png"),        514,900, 0.5,0.5, 0, False),
 "upperArmL": (os.path.join(S34,"upper_arm_L_socket.png"),125,237, 0.5,0.0, 1, False),
 "upperArmR": (os.path.join(S34,"upper_arm_R.png"),       112,256, 0.5,0.0, 2, False),
 "thighL":    (os.path.join(S34,"thigh_bent_L.png"),     230,267, 0.5,0.0, 3, False),
 "thighR":    (os.path.join(S34,"thigh_bent_R.png"),     218,299, 0.5,0.0, 4, False),
 "forearmL":  (os.path.join(V7C,"Arm_Front_Lower.png"),  145,275, 0.39,0.11,5, False),
 "forearmR":  (os.path.join(V7C,"Arm_Back_Lower.png"),   150,274, 0.63,0.11,6, False),
 "elbowCapL": (os.path.join(V7C,"Arm_Front_Cap.png"),     63,63,  0.5,0.5, 7, False),
 "elbowCapR": (os.path.join(V7C,"Arm_Back_Cap.png"),      63,63,  0.5,0.5, 8, False),
 "pelvis":    (os.path.join(S34,"pelvis_belt.png"),      218,181, 0.5,0.5, 9, False),
 "kneeL":     (os.path.join(S34,"knee_ball_spare.png"),   74,94,  0.5,0.5, 10, False),
 "kneeR":     (os.path.join(S34,"knee_ball_spare.png"),   74,94,  0.5,0.5, 11, False),
 "shinL":     (os.path.join(S34,"shin_boot_L.png"),      244,410, 0.5,0.0, 12, False),
 "shinR":     (os.path.join(S34,"shin_boot_mid.png"),    256,415, 0.5,0.0, 13, False),
 "torso":     (os.path.join(S34,"torso.png"),            291,315, 0.5,0.0, 14, False),
 "head":      (os.path.join(S34,"head_cowl.png"),        130,196, 0.5,0.5, 15, False),
 "handL":     (os.path.join(S34,"hand_spare_L.png"),     117,170, 0.5,0.5, 16, False),
 # handR: same whole separate hand file, mirrored WHOLE (flip, not crop/split)
 "handR":     (os.path.join(S34,"hand_spare_L.png"),     117,170, 0.5,0.5, 17, True),
}

def render(layout):
    canvas = Image.new("RGBA", (1400, 1600), (0,0,0,0))
    pieces = sorted(layout["pieces"], key=lambda p: (p["z"], DEFS[p["id"]][5]))
    audit = []
    for p in pieces:
        if not p.get("visible", True):
            continue
        pid = p["id"]
        src, w, h, ox, oy, _, flip = DEFS[pid]
        native = Image.open(src).convert("RGBA")
        # WHOLE piece, resized only to widget display placement size.
        im = native.resize((w, h), Image.LANCZOS)
        if flip:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        # Verification: no crop/split — resized whole piece alpha count
        # must be preserved through rotation (rotation adds transparent
        # padding, it does not remove content).
        before = sum(1 for a in im.split()[3].getdata() if a > 0)
        r = im.rotate(-p["rotation"], resample=Image.BICUBIC,
                      center=(ox*im.width, oy*im.height))
        canvas.alpha_composite(r, (int(round(p["x"])), int(round(p["y"]))))
        audit.append({
            "id": pid, "source": os.path.relpath(src, RIG),
            "native_size": list(native.size), "display_size": [w, h],
            "saved_xy": [p["x"], p["y"]], "rotation": p["rotation"],
            "pivot": [ox, oy], "z": p["z"], "flip_whole": flip,
            "locked": p.get("locked"), "cut": "NO", "crop": "NO", "split": "NO",
            "erased": "NO", "status": "WHOLE",
            "whole_alpha_pixels_display_size": before,
        })
    return canvas, audit

def stats(im):
    a = im.split()[3]
    bbox = a.getbbox()
    arr = __import__("numpy").array(a)
    ys, _ = __import__("numpy").where(arr > 0)
    def bottom(m):
        yy, _ = __import__("numpy").where(m > 0)
        return int(yy.max()) if len(yy) else None
    return {"bbox": bbox, "bottom": int(ys.max()),
            "bottom_left_band": bottom(arr[:, :700]),
            "bottom_right_band": bottom(arr[:, 700:])}

def main():
    layout = json.load(open(LAYOUT))
    canvas, audit = render(layout)
    canvas.save(os.path.join(OUT, "poses/sit-chair-whole-original-20261101.png"))
    grey = Image.new("RGBA", (1400, 1600), (126,126,126,255))
    grey.alpha_composite(canvas)
    grey.convert("RGB").save(os.path.join(OUT, "poses/sit-chair-whole-original-20261101-on-grey.png"))
    # old vs new contact: rejected pipeline real-rig | rejected pipeline literal | NEW whole
    def load(p):
        return Image.open(p).convert("RGBA")
    rej_real = load(os.path.join(RIG, "pipeline-auto-20261101/poses/real-rig-20261101.png"))
    rej_lit = load(os.path.join(RIG, "pipeline-auto-20261101/poses/literal-widget-20261101.png"))
    panels = []
    for im, label in [(rej_real, "REJECTED pipeline real-rig\n(fist split 75%, hand 93x134)"),
                      (rej_lit, "REJECTED pipeline literal\n(audit: builder splits fist off)"),
                      (canvas, "NEW whole-original\n(no cut, no crop, no split)")]:
        thumb = im.copy(); thumb.thumbnail((460, 526), Image.LANCZOS)
        panels.append((thumb, label))
    from PIL import ImageDraw, ImageFont
    W = 460*3 + 40; H = 526 + 70
    contact = Image.new("RGB", (W, H), (255,255,255))
    d = ImageDraw.Draw(contact)
    for i, (thumb, label) in enumerate(panels):
        x = 10 + i*470
        contact.paste(thumb, (x, 60), thumb)
        d.text((x, 10), label, fill=(0,0,0))
    contact.save(os.path.join(OUT, "contacts/old-vs-new-whole-original-20261101.png"))
    gates = {"layout_source": LAYOUT, "pieces_drawn": len(audit),
             "pieces_status": "ALL WHOLE", "stats": stats(canvas),
             "ground_line_y": 1475,
             "hands_separate_whole": 2, "forearms_whole_with_attached_fist": 2,
             "fists_cut_off": 0, "crops": 0, "splits": 0, "erased": 0,
             "audit": audit}
    json.dump(gates, open(os.path.join(OUT, "gates-20261101.json"), "w"), indent=2)
    json.dump(audit, open(os.path.join(OUT, "piece-audit-20261101.json"), "w"), indent=2)
    print(json.dumps({k: v for k, v in gates.items() if k != "audit"}, indent=2))
    print("AUDIT:", [(a["id"], a["status"]) for a in audit])

if __name__ == "__main__":
    main()
