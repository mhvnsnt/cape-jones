#!/usr/bin/env python3
"""TOOL 2 — Colour + proportion nearest-neighbour classifier (rank #3).
NOT a downloaded CLIP model: a local, auditable feature vector trained on
the 31 already-labelled sliced/ templates — aspect ratio, fill ratio,
opaque-pixel colour histogram (8-bin RGB), and silhouette centroid.
A piece is proposed the label of its nearest template(s) in that space.
This is deliberately complementary to Tool 1 (colour/proportion, not shape).
Usage: tool2_embedding_knn.py <piece.png> -> JSON on stdout.
"""
import sys, os, json
import numpy as np
from PIL import Image

TEMPLATES_DIR = os.path.expanduser("~/workspace/cape-jones-rig/sliced")

def features(path):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im).astype(float)
    a = arr[:, :, 3] / 255.0
    opaque = a > 0.04
    if opaque.sum() == 0:
        return None
    h, w = a.shape
    rgb = arr[:, :, :3][opaque]
    hist = []
    for c in range(3):
        hist.extend(np.histogram(rgb[:, c], bins=4, range=(0, 256))[0] / max(1, len(rgb)))
    ys, xs = np.where(opaque)
    feat = [w / h, opaque.mean(),
            (xs.mean() / w), (ys.mean() / h)] + hist
    return np.array(feat, dtype=float)

def classify(piece):
    pf = features(piece)
    if pf is None:
        return {"tool": "embedding_knn", "best": None, "confidence": 0.0, "reason": "no opaque pixels"}
    rows = []
    for tf in sorted(os.listdir(TEMPLATES_DIR)):
        if not tf.endswith(".png"):
            continue
        tf_feat = features(os.path.join(TEMPLATES_DIR, tf))
        if tf_feat is None:
            continue
        # normalise feature scales: aspect/fill/centroid ~0-2, hist sums to 3
        d = float(np.linalg.norm((pf - tf_feat) * np.array([1, 1, 1, 1] + [0.5] * 12)))
        rows.append({"template": tf, "distance": round(d, 4)})
    rows.sort(key=lambda r: r["distance"])
    best = rows[0]
    conf = 0.9 if best["distance"] < 0.5 else (0.6 if best["distance"] < 1.0 else 0.3)
    return {"tool": "embedding_knn", "best": best["template"], "distance": best["distance"],
            "confidence": conf, "second": rows[1] if len(rows) > 1 else None,
            "reason": f"nearest template in colour+proportion space, distance {best['distance']}"}

if __name__ == "__main__":
    print(json.dumps(classify(sys.argv[1]), indent=2))
