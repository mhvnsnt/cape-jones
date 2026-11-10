#!/usr/bin/env python3
"""Fetch an ambientCG PBR material set. Downloadable assets are CC0
(ambientcg.com: free for personal/commercial use, no attribution).

Usage: python3 fetch_ambientcg.py <AssetId> [1K|2K] [JPG|PNG] [outdir]
Example: python3 fetch_ambientcg.py Wood096 1K JPG ./textures
"""
import os
import sys
import urllib.request
import zipfile

UA = "cape-jones-3d-tools/1.0 (research fetch)"

def main():
    asset = sys.argv[1] if len(sys.argv) > 1 else "Wood096"
    res = sys.argv[2] if len(sys.argv) > 2 else "1K"
    fmt = sys.argv[3] if len(sys.argv) > 3 else "JPG"
    outdir = sys.argv[4] if len(sys.argv) > 4 else "."
    os.makedirs(outdir, exist_ok=True)
    url = f"https://ambientcg.com/get?file={asset}_{res}-{fmt}.zip"
    zpath = os.path.join(outdir, f"{asset}_{res}-{fmt}.zip")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r, open(zpath, "wb") as f:
        f.write(r.read())
    with zipfile.ZipFile(zpath) as z:
        names = z.namelist()
    assert any(n.endswith((".jpg", ".png")) for n in names), "no image maps in zip"
    print(f"OK: {zpath}")
    for n in names:
        print("  -", n)
    print("License: CC0 — https://ambientcg.com/")

if __name__ == "__main__":
    main()
