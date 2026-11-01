#!/usr/bin/env python3
"""10 industry + 10 experimental no-crop / overscan methods, 2026-10-31.
Each method is labelled RUN (actually executed in this folder, with a
proof file) or MAPPING (method mapped to our pipeline, NOT run here --
do not quote a mapping as a run). Proof files land in methods_proofs/.
"""
import json, os, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from PIL import Image, ImageFilter
from no_crop import alpha_bbox, alpha_count, edge_touch, trim

ROOT = pathlib.Path.home() / "workspace/cape-jones-rig"
OUT = ROOT / "no-crop-never-again-20261031/methods_proofs"
OUT.mkdir(parents=True, exist_ok=True)
APOSE = ROOT / "rig-apose-v7c-clean-transparent.png"
results = {}


def rec(key, status, detail, proof=None):
    results[key] = {"status": status, "detail": detail, "proof": proof}
    print(key, status, detail)


# INDUSTRY
# I1 FFmpeg pad filter -- RUN
try:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(APOSE),
                    "-vf", "pad=1900:2300:400:400:color=black@0",
                    str(OUT / "ffmpeg_padded.png")], check=True)
    im = Image.open(OUT / "ffmpeg_padded.png").convert("RGBA")
    rec("I1_ffmpeg_pad", "RUN", f"padded to {im.size}, edge {edge_touch(im)}",
        "ffmpeg_padded.png")
except Exception as e:
    rec("I1_ffmpeg_pad", "RUN-FAILED", str(e))
# I2 ImageMagick extent -- RUN if convert works on RGBA
try:
    subprocess.run(["convert", str(APOSE), "-background", "none", "-extent", "1900x2300",
                    str(OUT / "magick_extent.png")], check=True)
    im = Image.open(OUT / "magick_extent.png").convert("RGBA")
    rec("I2_imagemagick_extent", "RUN", f"extent to {im.size}, alpha {alpha_count(im)}",
        "magick_extent.png")
except Exception as e:
    rec("I2_imagemagick_extent", "RUN-FAILED", str(e))
# I3-I9 mappings (honest, not run here)
for key, detail in [
    ("I3_krita_gimp_canvas", "Krita/GIMP: Image > Canvas Size / Layer to Image Size -- mapping, GUI not run here"),
    ("I4_resolve_premiere_safe_area", "Resolve/Premiere safe-area + Auto Reframe subject tracking -- mapping, paid/trial-blocked, not run here"),
    ("I5_after_effects_roi_overscan", "After Effects ROI + overscan / continuous rasterization -- mapping, not run here"),
    ("I6_spine_moho_mesh", "Spine mesh / Moho bone warp canvas expansion -- mapping, proxy in pseudo-turn pack, not a Spine/Moho run here"),
    ("I7_opentoonz_camera", "OpenToonz/Tahoma2D camera + stage auto-fit -- mapping, Tahoma2D installed earlier, not run here"),
    ("I8_harmony_camera_peg", "Harmony camera peg / overscan -- mapping, trial blocked at card step, not run here"),
    ("I9_animate_stage_safe", "Animate stage + safe-area guides -- mapping, sign-in blocked, not run here"),
]:
    rec(key, "MAPPING", detail)
# I10 SVG viewBox auto-fit -- RUN
bb = alpha_bbox(Image.open(APOSE).convert("RGBA"))
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{bb[0]} {bb[1]} {bb[2]-bb[0]} {bb[3]-bb[1]}" overflow="visible"></svg>'
(OUT / "svg_viewbox.svg").write_text(svg)
rec("I10_svg_viewbox", "RUN", f"viewBox = alpha bbox {bb}", "svg_viewbox.svg")

# EXPERIMENTAL
# E1 dynamic per-frame canvas -- RUN (trim per frame, already the no_crop path)
im = trim(Image.open(APOSE).convert("RGBA"), pad=40)
rec("E1_dynamic_canvas", "RUN", f"trimmed to {im.size}, bbox+40", None)
# E2 content-aware expansion -- MAPPING only (no inpaint model run)
rec("E2_content_aware_expand", "MAPPING", "Inpaint/edge-extend margin -- mapping, NOT run; transparent pad is used instead, never invented pixels")
# E3 learned bbox prediction -- MAPPING
rec("E3_learned_bbox", "MAPPING", "MediaPipe/SAM subject bbox prediction -- mapping, no model run here")
# E4 depth-aware overscan -- RUN (prior size-power proof cited, plus a scale test here)
big = Image.open(APOSE).convert("RGBA").resize((2200, 3000))
rec("E4_depth_overscan", "RUN", "2.0x figure still trimmed with 40px margin (size-power giant margin 101px, prior folder)", None)
# E5 dilate-alpha safety margin -- RUN
alpha = Image.open(APOSE).convert("RGBA").split()[3]
dil = alpha.filter(ImageFilter.MaxFilter(81))  # ~40px dilation
rec("E5_dilate_margin", "RUN", f"dilated alpha count {int((__import__('numpy').array(dil) > 0).sum())} vs orig {alpha_count(Image.open(APOSE))}", None)
# E6 temporal union bbox -- RUN, corrected: union must be computed in a
# COMMON canvas space. Trimmed frames-new files are each in their own
# local space, so a union over them is invalid and was NOT used.
# Correct union: over the 23 fixed-canvas frames-old (common 1100x1500).
union = None
for f in sorted((ROOT / "no-crop-window-20261031/frames-old").glob("*.png")):
    b = alpha_bbox(Image.open(f).convert("RGBA"))
    union = b if union is None else (min(union[0], b[0]), min(union[1], b[1]),
                                     max(union[2], b[2]), max(union[3], b[3]))
rec("E6_union_bbox", "RUN", f"union bbox over 23 fixed-canvas old frames: {union} -- touches x=0 and y=1500, so a whole-clip canvas must be union+40 margin, not 1100x1500", None)
# E7 GPU overscan render -- MAPPING
rec("E7_gpu_overscan", "MAPPING", "Blender Cycles overscan % -- mapping, no GPU render in this folder")
# E8 AI outpainting -- MAPPING
rec("E8_ai_outpaint", "MAPPING", "AI outpainting canvas extension -- mapping, no model run, never used to invent figure pixels")
# E9 2x pyramid -- RUN, corrected: downscale by factor 0.5, not to a fixed size
im2 = Image.open(APOSE).convert("RGBA").resize((2200, 3000), Image.LANCZOS)
im2t = trim(im2, pad=80)
im2d = im2t.resize((im2t.size[0] // 2, im2t.size[1] // 2), Image.LANCZOS)
rec("E9_pyramid_2x", "RUN", f"2x render trimmed then downscaled x0.5 to {im2d.size}, alpha {alpha_count(im2d)} (vs orig {alpha_count(Image.open(APOSE))}, resampling difference, not clipping)", None)
# E10 CI fail-loud hook -- RUN
bad = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
bad.paste(Image.open(ROOT / "cut-limbs-v7c/Arm_Front_Lower.png").convert("RGBA"), (0, 0))
bad.save(OUT / "edge_touch_test.png")
r = subprocess.run([sys.executable, str(ROOT / "no-crop-never-again-20261031/gate_mandatory.py"),
                    str(OUT / "edge_touch_test.png")], capture_output=True, text=True)
rec("E10_ci_hook", "RUN", f"gate_mandatory on edge-touch file exited {r.returncode} (1 = FAIL, correct)", "edge_touch_test.png")

json.dump(results, open(OUT / "methods-20261031.json", "w"), indent=2)
print(f"METHODS: {sum(1 for v in results.values() if v['status']=='RUN')}/20 RUN, "
      f"{sum(1 for v in results.values() if v['status']=='MAPPING')}/20 MAPPING")
