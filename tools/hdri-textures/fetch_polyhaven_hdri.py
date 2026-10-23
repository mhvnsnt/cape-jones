#!/usr/bin/env python3
"""Fetch Poly Haven HDRIs (CC0). Assets verified CC0 2026-10-17 at
https://polyhaven.com/license: commercial use OK, no attribution, redistributable.

Usage:
  python3 fetch_polyhaven_hdri.py <slug> [1k|2k|4k] [outdir]
  python3 fetch_polyhaven_hdri.py --indoor --res 1k   # suggested indoor set

Example: python3 fetch_polyhaven_hdri.py kloppenheim_05_puresky 1k ./hdris

Resolution + integrity now come from the free Poly Haven API
(https://api.polyhaven.com/files/{slug}, no key): the script asserts the
downloaded bytes match the API's published md5 + size, and skips re-download
when the local file already matches. Falls back to the direct CDN URL pattern
if the API is unreachable.
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.request

UA = {"User-Agent": "cape-jones-3d-tools/1.0 (research fetch)"}
API = "https://api.polyhaven.com/files/{}"

# Suggested indoor/studio HDRIs for the living room (window daylight fill,
# lamp reflections). Curated 2026-10-17.
INDOOR_SUGGESTIONS = [
    "studio_small_03",
    "studio_small_09",
    "leburb",
    "brown_photostudio_02",
]


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def api_meta(slug):
    """Return the API's file record for `slug`, or None if unreachable."""
    try:
        req = urllib.request.Request(API.format(slug), headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except Exception as e:
        print(f"API lookup failed for {slug} ({e}); using CDN pattern",
              file=sys.stderr)
        return None


def resolve(meta, slug, res):
    """Pick the download entry for `res` (or nearest available)."""
    hdri = meta.get("hdri", {})
    order = [res] + [r for r in ("1k", "2k", "4k", "8k") if r != res]
    for r in order:
        if r in hdri and "hdr" in hdri[r]:
            return hdri[r]["hdr"], r
    raise RuntimeError(f"no .hdr download in API response for {slug}")


def fetch(slug, res="1k", outdir="."):
    os.makedirs(outdir, exist_ok=True)
    meta = api_meta(slug)
    if meta:
        entry, used_res = resolve(meta, slug, res)
        url, want_md5, want_size = (entry["url"], entry.get("md5"),
                                   entry.get("size"))
    else:
        url = (f"https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/"
               f"{res}/{slug}_{res}.hdr")
        want_md5, want_size, used_res = None, None, res
    out = os.path.join(outdir, f"{slug}_{used_res}.hdr")
    if os.path.exists(out) and want_md5 and md5_of(out) == want_md5:
        print(f"SKIP (md5 match): {out}")
        return out
    print(f"GET {url}")
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=600) as r, open(out, "wb") as f:
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    with open(out, "rb") as f:
        magic = f.read(11)
    assert magic == b"#?RADIANCE\n", f"{out}: not a Radiance HDR file"
    if want_md5:
        got = md5_of(out)
        assert got == want_md5, f"md5 mismatch: {got} != {want_md5}"
    if want_size:
        assert os.path.getsize(out) == want_size, "size mismatch"
    md5short = f", md5={want_md5[:12]}..." if want_md5 else ""
    print(f"OK: {out} ({os.path.getsize(out)} bytes{md5short})")
    print("License: CC0 — https://polyhaven.com/license")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?", default="kloppenheim_05_puresky")
    ap.add_argument("rest", nargs="*",
                    help="[res] [outdir] — old positional form still works")
    ap.add_argument("--res", default=None, choices=["1k", "2k", "4k", "8k"])
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--indoor", action="store_true",
                    help="fetch the suggested indoor/studio set")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    res, outdir = a.res or "1k", a.outdir or "."
    for r in a.rest:  # backward compat: fetch_polyhaven_hdri.py slug 2k ./hdris
        if r in ("1k", "2k", "4k", "8k") and a.res is None:
            res = r
        elif a.outdir is None:
            outdir = r
    slugs = [a.slug]
    if a.indoor:
        slugs = INDOOR_SUGGESTIONS
    if a.limit:
        slugs = slugs[:a.limit]
    for s in slugs:
        try:
            fetch(s, res=res, outdir=outdir)
        except Exception as e:
            print(f"FAILED {s}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
