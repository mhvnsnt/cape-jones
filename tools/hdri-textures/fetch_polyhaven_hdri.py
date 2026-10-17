#!/usr/bin/env python3
"""Fetch a Poly Haven HDRI by slug. Assets are CC0 (verified 2026-10-17 at
https://polyhaven.com/license: commercial use OK, no attribution, redistributable).

Usage: python3 fetch_polyhaven_hdri.py <slug> [1k|2k|4k] [outdir]
Example: python3 fetch_polyhaven_hdri.py kloppenheim_05_puresky 1k ./hdris
"""
import hashlib
import os
import sys
import urllib.request

UA = "cape-jones-3d-tools/1.0 (research fetch)"

def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "kloppenheim_05_puresky"
    res = sys.argv[2] if len(sys.argv) > 2 else "1k"
    outdir = sys.argv[3] if len(sys.argv) > 3 else "."
    os.makedirs(outdir, exist_ok=True)
    url = f"https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/{res}/{slug}_{res}.hdr"
    out = os.path.join(outdir, f"{slug}_{res}.hdr")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r, open(out, "wb") as f:
        data = r.read()
        f.write(data)
    # verify: real Radiance HDR magic bytes
    assert data[:11] == b"#?RADIANCE\n", "not a Radiance HDR file"
    md5 = hashlib.md5(data).hexdigest()
    print(f"OK: {out} ({len(data)} bytes, md5={md5})")
    print("License: CC0 — https://polyhaven.com/license")

if __name__ == "__main__":
    main()
