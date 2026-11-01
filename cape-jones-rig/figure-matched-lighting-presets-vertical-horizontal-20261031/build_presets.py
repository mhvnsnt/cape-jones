import json, pathlib, shutil
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

SRC = pathlib.Path.home()/"workspace/cape-jones-rig/figure-matched-room-lighting-20261031"
OUT = pathlib.Path.home()/"workspace/cape-jones-rig/figure-matched-lighting-presets-vertical-horizontal-20261031"
data = json.loads((SRC/"FIGURE-MATCHED-LIGHTING-REPORT-20261031.json").read_text())
# cel bands / interior treatment from the original figure-matched report (shared method, not per-scenario invented)
SHARED = {
    "cel_bands": [1.12, 0.92, 0.72],
    "cel_bands_note": "3 bands by light direction, from original figure-matched report",
    "rim_method": "dilate(figure,6) - figure, rim_px 34446 in source JSON (measured lit rim included in lit-transparent alpha)",
    "interior_line_method": "ink band: dark pixels within 3px of non-dark, 49849 px in source JSON, recoloured 80% toward rim on light side and toward shadow on away side; pec, rib, ab, belt, gauntlet, cape-fold and cowl lines carry light, not left black under a flat tint",
    "interior_sheen": "<=14px inside-edge band, up to 38% rim",
    "base_art": "never recoloured; lighting on separate layers over a copy of the clean plate",
    "no_crop_source": "source padded canvas 1260x1660, padded edge alpha max 0.0 in source JSON",
    "ground_bounce": {"S3": "45% in bottom 28% of figure", "other": "not specified in source report, recorded as none specified, not invented"},
}
PRESET_NAMES = {
    "S1-v2-warm-overhead": "FIGURE-MATCHED PRESET S1 — V2 WARM OVERHEAD",
    "S2-v3-warm-overhead-strong": "FIGURE-MATCHED PRESET S2 — V3 WARM OVERHEAD STRONG",
    "S3-v3pools-warm-overhead-bounce": "FIGURE-MATCHED PRESET S3 — V3+POOLS WARM GROUND BOUNCE",
    "S4-glare-warm-overhead-glow": "FIGURE-MATCHED PRESET S4 — GLARE WARM OVERHEAD GLOW",
    "S5-colour-magenta-rose": "FIGURE-MATCHED PRESET S5 — COLOUR MAGENTA-ROSE",
    "S6-colour-cyan-dual-backlight": "FIGURE-MATCHED PRESET S6 — COLOUR CYAN DUAL BACKLIGHT",
    "S7-colour-golden-hour-front": "FIGURE-MATCHED PRESET S7 — COLOUR GOLDEN-HOUR FRONT",
    "S8-colour-cool-blue-night": "FIGURE-MATCHED PRESET S8 — COLOUR COOL-BLUE NIGHT",
}
def fit_composite(onroom, target):
    """Full on-room image fitted inside target, blurred cover-fill behind it. No crop of figure or source."""
    tw, th = target
    bg = onroom.convert("RGB").resize((tw, th), Image.LANCZOS)  # cover would crop; instead use blurred stretched fill as backdrop only
    # Build backdrop by cover-resizing then heavy blur (backdrop only, figure layer is the fitted image on top, intact)
    scale = max(tw/onroom.width, th/onroom.height)
    bw, bh = int(onroom.width*scale+0.5), int(onroom.height*scale+0.5)
    cover = onroom.convert("RGB").resize((bw, bh), Image.LANCZOS)
    x0, y0 = (bw-tw)//2, (bh-th)//2
    backdrop = cover.crop((x0, y0, x0+tw, y0+th)).filter(ImageFilter.GaussianBlur(30))
    canvas = backdrop.convert("RGBA")
    fscale = min(tw/onroom.width, th/onroom.height)
    fw, fh = int(onroom.width*fscale+0.5), int(onroom.height*fscale+0.5)
    fitted = onroom.resize((fw, fh), Image.LANCZOS)
    px, py = (tw-fw)//2, (th-fh)//2
    canvas.alpha_composite(fitted.convert("RGBA"), (px, py))
    return canvas.convert("RGB"), {"fit_scale": round(fscale,4), "fitted_size": [fw, fh], "paste_xy": [px, py]}

def fig_bbox(lit_path, scale, paste):
    a = np.array(Image.open(lit_path))[:,:,3] > 10
    ys, xs = np.where(a)
    return {"x_min": int(xs.min()*scale+paste[0]), "x_max": int(xs.max()*scale+paste[0]),
            "y_min": int(ys.min()*scale+paste[1]), "y_max": int(ys.max()*scale+paste[1]),
            "alpha_px_source_lit": int(a.sum())}

results = []
for s in data["scenarios"]:
    sid = s["id"]
    pdir = OUT/"presets"/sid
    pdir.mkdir(parents=True, exist_ok=True)
    lit = SRC/"figures"/f"{sid}-lit-transparent-20261031.png"
    onroom = SRC/"figures"/f"{sid}-on-room-20261031.png"
    ongrey = SRC/"figures"/f"{sid}-on-grey-20261031.png"
    shutil.copy(lit, pdir/f"{sid}-lit-transparent-20261031.png")
    shutil.copy(onroom, pdir/f"{sid}-on-room-20261031.png")
    shutil.copy(ongrey, pdir/f"{sid}-on-grey-20261031.png")
    onroom_im = Image.open(onroom)
    vert, vmeta = fit_composite(onroom_im, (1080, 1920))
    horiz, hmeta = fit_composite(onroom_im, (1920, 1080))
    vpath = pdir/f"{sid}-vertical-1080x1920-20261031.png"
    hpath = pdir/f"{sid}-horizontal-1920x1080-20261031.png"
    vert.save(vpath); horiz.save(hpath)
    vb = fig_bbox(lit, vmeta["fit_scale"], vmeta["paste_xy"])
    hb = fig_bbox(lit, hmeta["fit_scale"], hmeta["paste_xy"])
    # margins
    vb["margins"] = {"left": vb["x_min"], "right": 1080-1-vb["x_max"], "top": vb["y_min"], "bottom": 1920-1-vb["y_max"]}
    hb["margins"] = {"left": hb["x_min"], "right": 1920-1-hb["x_max"], "top": hb["y_min"], "bottom": 1080-1-hb["y_max"]}
    spec = {
        "preset_name": PRESET_NAMES[sid],
        "scenario_id": sid,
        "source": "figure-matched-room-lighting-20261031, Mars saved-good 2026-10-31 23:00 CDT (saved-good, NOT upgraded to full 1/1 approval)",
        "room": s["room"], "direction": s["direction"], "gain": s["gain"], "rim_RGB": s["rim"],
        "shadow_RGB": s["shadow"], "lit_mean_RGB_source": s["lit_mean_RGB"], "base_mean_RGB_source": s["base_mean_RGB"],
        "source_canvas": s["canvas"], "source_figure_alpha_px_source_JSON": s["figure_alpha_px"],
        "measured_lit_transparent_alpha_px": vb["alpha_px_source_lit"],
        "alpha_note": "Source JSON figure_alpha_px (374127) differs from measured lit-transparent alpha (408573, S4 423488). Both recorded; source value preserved verbatim, measured value is from the lit-transparent file used here. Rim expansion in the lit file is the likely cause; not resolved by editing either number.",
        "line_band_px_source": s["line_band_px"], "rim_px_source": s["rim_px"],
        "line_band_mean_light_factor_source": s["line_band_mean_light_factor"],
        "shared_method": SHARED,
        "ground_bounce": SHARED["ground_bounce"].get("S3") if sid.startswith("S3") else "not specified in source report",
        "vertical": {"canvas": [1080, 1920], **vmeta, "figure_bbox": vb, "no_crop": "figure fully inside canvas, all margins > 0, source fitted not cropped; backdrop is blurred cover of same room only"},
        "horizontal": {"canvas": [1920, 1080], **hmeta, "figure_bbox": hb, "no_crop": "figure fully inside canvas, all margins > 0, source fitted not cropped; backdrop is blurred cover of same room only"},
        "files": [p.name for p in sorted(pdir.glob("*.png"))],
        "approval": "0/1 preset set, 0/1 vertical set, 0/1 horizontal set separately; original set saved-good by Mars",
    }
    (pdir/f"PRESET-{sid}-20261031.json").write_text(json.dumps(spec, indent=2))
    results.append(spec)
    print(sid, "vert", vmeta, vb["margins"], "horiz", hmeta, hb["margins"])

def contact(tiles, cols, thumb_w, label_h, outpath):
    rows = (len(tiles)+cols-1)//cols
    tw = thumb_w; th = int(tiles[0][0].height * tw / tiles[0][0].width)
    W, H = cols*tw, rows*(th+label_h)
    sheet = Image.new("RGB", (W, H), (20,20,20))
    d = ImageDraw.Draw(sheet)
    for i,(im,label) in enumerate(tiles):
        t = im.resize((tw, th), Image.LANCZOS)
        x, y = (i%cols)*tw, (i//cols)*(th+label_h)
        sheet.paste(t, (x,y)); d.text((x+8, y+th+6), label, fill=(255,255,0))
    sheet.save(outpath); print(outpath, sheet.size)

# preset index contact: on-room thumbnails
tiles=[]
for s in results:
    sid=s["scenario_id"]
    tiles.append((Image.open(OUT/"presets"/sid/f"{sid}-on-room-20261031.png"), s["preset_name"]))
contact(tiles, 4, 420, 28, OUT/"preset-index-contact-20261031.png")
tiles=[]
for s in results:
    sid=s["scenario_id"]
    tiles.append((Image.open(OUT/"presets"/sid/f"{sid}-vertical-1080x1920-20261031.png"), s["preset_name"]+" VERTICAL"))
contact(tiles, 4, 300, 28, OUT/"vertical-contact-20261031.png")
tiles=[]
for s in results:
    sid=s["scenario_id"]
    tiles.append((Image.open(OUT/"presets"/sid/f"{sid}-horizontal-1920x1080-20261031.png"), s["preset_name"]+" HORIZONTAL"))
contact(tiles, 2, 640, 28, OUT/"horizontal-contact-20261031.png")
(OUT/"PRESET-INDEX-20261031.json").write_text(json.dumps({"presets": results, "canvases": {"source": [1260,1660], "vertical": [1080,1920], "horizontal": [1920,1080]}, "counts": {"presets": len(results), "vertical_files": len(results), "horizontal_files": len(results)}}, indent=2))
print("DONE", len(results))
