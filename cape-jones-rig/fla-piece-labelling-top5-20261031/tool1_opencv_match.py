#!/usr/bin/env python3
"""TOOL 1 — OpenCV shape matching (rank #1).
Compares a piece's alpha silhouette against the 31 already-labelled
sliced/ templates using cv2.matchShapes (Hu-moment distance, lower=better),
tested in both orientations (a mirrored limb is a real mislabel risk).
Usage: tool1_opencv_match.py <piece.png>  -> JSON on stdout.
"""
import sys, os, json
import cv2
import numpy as np
from PIL import Image

TEMPLATES_DIR = os.path.expanduser("~/workspace/cape-jones-rig/sliced")

def contour_of(path):
    im = Image.open(path).convert("RGBA")
    a = np.array(im)[:, :, 3]
    _, bw = cv2.threshold(a, 10, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return None, im.size
    return max(cnts, key=cv2.contourArea), im.size

def match(piece):
    pc, psize = contour_of(piece)
    if pc is None:
        return {"tool": "opencv_shape", "best": None, "confidence": 0.0, "reason": "no opaque pixels"}
    results = []
    for tf in sorted(os.listdir(TEMPLATES_DIR)):
        if not tf.endswith(".png"):
            continue
        tc, tsize = contour_of(os.path.join(TEMPLATES_DIR, tf))
        if tc is None:
            continue
        d = cv2.matchShapes(pc, tc, cv2.CONTOURS_MATCH_I1, 0.0)
        # mirrored template (flip the contour image, not the file)
        tim = Image.open(os.path.join(TEMPLATES_DIR, tf)).convert("RGBA")
        tim = tim.transpose(Image.FLIP_LEFT_RIGHT)
        arr = np.array(tim)[:, :, 3]
        _, bw = cv2.threshold(arr, 10, 255, cv2.THRESH_BINARY)
        cnts, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        dm = cv2.matchShapes(pc, max(cnts, key=cv2.contourArea), cv2.CONTOURS_MATCH_I1, 0.0) if cnts else 9.9
        best_d, mirror = (d, False) if d <= dm else (dm, True)
        results.append({"template": tf, "distance": round(float(best_d), 4),
                        "mirrored": mirror, "template_size": tsize})
    results.sort(key=lambda r: r["distance"])
    best = results[0]
    # confidence from distance: <0.15 high, <0.35 medium, else low
    conf = 0.9 if best["distance"] < 0.15 else (0.6 if best["distance"] < 0.35 else 0.3)
    return {"tool": "opencv_shape", "best": best["template"], "mirrored": best["mirrored"],
            "distance": best["distance"], "confidence": conf,
            "second": results[1] if len(results) > 1 else None,
            "piece_size": psize,
            "reason": f"Hu-moment shape distance {best['distance']} to {best['template']}"
                        + (" (mirrored)" if best["mirrored"] else "")}

if __name__ == "__main__":
    print(json.dumps(match(sys.argv[1]), indent=2))
