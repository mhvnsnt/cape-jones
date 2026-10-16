#!/usr/bin/env python3
"""
vs-anime-cleanup.vpy — VapourSynth cleanup chain for SCANNED HAND-DRAWN art.
Uses the pulled track-2 libraries:
  ~/workspace/tools/kagefunc/kagefunc.py   (adaptive_grain, retinex_edgemask, hybriddenoise)
  ~/workspace/tools/lvsfunc/lvsfunc        (deblock / misc helpers — imported if present)

What it does:
  1. Source via ffms2 (override with VS_SOURCE_PLUGIN=lsmas|ffms2)
  2. Light denoise tuned to keep pencil lines  (kagefunc.hybriddenoise)
  3. Banding removal on gradients              (f3kdb, if installed)
  4. Line-art mask -> darken/strengthen lines   (kagefunc.retinex_edgemask)
  5. Fine adaptive film grain for the final     (kagefunc.adaptive_grain)

Env:
  VS_INPUT   input file (required)
  VS_DENOISE 0/1 (default 1)      VS_DEBAND 0/1 (default 1)
  VS_LINEDARK 0..64 (default 18)  VS_GRAIN 0.0..1.0 (default 0.15)
"""
import os
import sys
import vapoursynth as vs

core = vs.core

sys.path.insert(0, os.path.expanduser("~/workspace/tools"))
import kagefunc as kgf  # noqa: E402

try:
    import lvsfunc as lvf  # noqa: E402
    HAVE_LVS = True
except Exception:
    HAVE_LVS = False

INPUT = os.environ["VS_INPUT"]  # KeyError with a clear message if missing
DENOISE = os.environ.get("VS_DENOISE", "1") == "1"
DEBAND = os.environ.get("VS_DEBAND", "1") == "1"
LINEDARK = int(os.environ.get("VS_LINEDARK", "18"))
GRAIN = float(os.environ.get("VS_GRAIN", "0.15"))

src_plugin = os.environ.get("VS_SOURCE_PLUGIN", "ffms2").lower()
if src_plugin == "lsmas":
    clip = core.lsmas.LWLibavSource(INPUT)
else:
    clip = core.ffms2.Source(INPUT)

# Work in 16-bit for the cleanup chain, finish at 10-bit.
clip = core.resize.Bicubic(clip, format=vs.YUV420P16, dither_type="error_diffusion")

if DENOISE:
    clip = kgf.hybriddenoise(clip, knl=0.5, sigma=2, radius1=1)

if DEBAND:
    try:
        clip = core.f3kdb.Deband(clip, range=15, y=32, cb=32, cr=32,
                                 grainy=0, grainc=0, output_depth=16)
    except vs.Error:
        sys.stderr.write("WARN: f3kdb not installed, skipping deband\n")

if LINEDARK > 0:
    # Line mask from retinex edge detection, then pull masked luma down.
    mask = kgf.retinex_edgemask(clip, sigma=1)
    mask = core.std.Binarize(mask, threshold=38000).std.Maximum()
    dark = core.std.Expr([clip],
                         expr=[f"x {LINEDARK * 256} - 0 max", "", ""])
    clip = core.std.MaskedMerge(clip, dark, mask)

if GRAIN > 0:
    clip = kgf.adaptive_grain(clip, strength=GRAIN, static=False, luma_scaling=12)

clip = core.resize.Bicubic(clip, format=vs.YUV420P10)
clip.set_output()
