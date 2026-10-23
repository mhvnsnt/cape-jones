#!/usr/bin/env python3
"""Gentle line art cleanup for hand-drawn animation frames.
Only smooths noise and fills pinhole gaps in lines. NEVER recolors fills.
- Bilateral filter: smooths flat areas, preserves edges (keeps all colors)
- Tiny morphological close on THIN structures only (not large fills)
Usage: cleanup_lines.py input.png output.png
"""
import cv2
import numpy as np
import sys

def cleanup_frame(img):
    # Step 1: Edge-preserving denoise. Keeps every color, just kills grain.
    smoothed = cv2.bilateralFilter(img, 7, 50, 50)

    # Step 2: Find THIN dark lines only (not large dark fills like the cowl/cape).
    # Use adaptive threshold to find dark pixels, then EXCLUDE large connected
    # components (those are fills, not lines).
    gray = cv2.cvtColor(smoothed, cv2.COLOR_BGR2GRAY)
    _, dark = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

    # Connected components: kill anything bigger than a line
    # (a line at 1080p is rarely more than ~4000 px in one blob)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(dark, connectivity=8)
    thin_lines = np.zeros_like(dark)
    for i in range(1, n):
        area = stats[i, cv2.CC_STAT_AREA]
        if area < 4000:  # thin line, not a fill
            thin_lines[labels == i] = 255

    # Tiny close to fill pinhole gaps in the thin lines only
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    closed_lines = cv2.morphologyEx(thin_lines, cv2.MORPH_CLOSE, kernel)

    # Composite: original smoothed image, but paint closed thin lines
    # back in pure black for crispness
    result = smoothed.copy()
    result[closed_lines.astype(bool)] = (10, 10, 10)
    return result

if __name__ == "__main__":
    inp, outp = sys.argv[1], sys.argv[2]
    img = cv2.imread(inp)
    if img is None:
        print(f"Cannot read {inp}", file=sys.stderr)
        sys.exit(1)
    cv2.imwrite(outp, cleanup_frame(img))
    print(f"Cleaned {inp} -> {outp}")
