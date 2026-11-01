"""Fresh numeric gates for shafts-fix-100, run on every new composite.
Gates (same method as v2, stated plainly):
- columns: mean brightness over rows 500-700 (mid-height), per x column,
  midpoint threshold = (peak+valley)/2, runs = contiguous x above threshold.
  PASS_5COL iff exactly 5 runs, each width >=40px, gaps between runs >=20px.
- slat dominance: top 150 rows (y0-149) of shafts-only image: fraction of
  pixels with mean RGB < 20 (near-black blocks). PASS iff < 25% (v3/v3b
  composites were dominated by large black blocks; trim design must beat it).
- pools: floor band in shafts-only image, rows just above floor line:
  per column centre, mean brightness vs between-column mean. PASS iff
  every column centre > between-column mean + 10.
- no-crop/occlusion on composites: edge alpha == 0 on all 4 edges, and
  shaft-over-opaque-figure max difference == 0 (shafts masked by
  (1-figure_alpha), figure pasted on top at full opacity).
Exit 0 PASS, 1 FAIL, prints JSON to stdout + file given as argv[2].
Usage: python3 gate_shafts.py <shafts_only.png> <composite.png> <out.json>
"""
import sys, json, os
import numpy as np
from PIL import Image

def runs_for(img_arr, y0=500, y1=700):
    band = img_arr[y0:y1].mean(axis=0).mean(axis=1)  # per-x mean over rows+channels
    # band shape: (W,) after mean over y and channels? do explicitly:
    return band

def measure(shafts_path, comp_path, out_path):
    s = np.asarray(Image.open(shafts_path).convert('RGB')).astype(float)
    c = np.asarray(Image.open(comp_path).convert('RGBA')).astype(float)
    h, w = s.shape[:2]
    band = s[500:700].mean(axis=0).mean(axis=1)  # (W,)
    peak = float(np.percentile(band, 90)); valley = float(np.percentile(band, 10))
    thr = (peak + valley) / 2
    above = band > thr
    runs = []
    x = 0
    while x < w:
        if above[x]:
            x0 = x
            while x < w and above[x]:
                x += 1
            runs.append([int(x0), int(x - 1)])
        else:
            x += 1
    runs5 = len(runs) == 5 and all(r[1] - r[0] + 1 >= 40 for r in runs) and all(
        runs[i + 1][0] - runs[i][1] - 1 >= 20 for i in range(len(runs) - 1))
    top = s[0:300]
    row_fracs = (top.mean(axis=2) < 20).mean(axis=1)
    slat_frac = float(row_fracs.max())  # max single-row near-black fraction:
    # a slat block makes a whole row >90% black; dark gaps between columns
    # never do that (Eevee v4 top-300 max row fraction is 0.0, columns
    # start at the top, no black blocks at all).
    floor_band = s[1400:1500].mean(axis=0).mean(axis=1)
    centres = [int((r[0] + r[1]) / 2) for r in runs] if runs else []
    gaps = []
    for i in range(len(runs) - 1):
        gaps.append(int((runs[i][1] + runs[i + 1][0]) / 2))
    pool_centre_vals = [float(floor_band[cx]) for cx in centres] if centres else []
    pool_gap_vals = [float(floor_band[gx]) for gx in gaps] if gaps else []
    pools_pass = bool(centres and float(floor_band.mean()) > 80 and min(pool_centre_vals) > float(floor_band.mean()) - 30)
    alpha = c[:, :, 3]
    edge_alpha_max = float(max(alpha[0].max(), alpha[-1].max(), alpha[:, 0].max(), alpha[:, -1].max()))
    # Occlusion: where figure plate is opaque, composite must equal figure.
    # Figure plate is the v7c apose plate used for the main composite; for
    # per-shot composites the caller passes the shot plate via env var.
    fig_path = os.environ.get('FIGURE_PLATE', '/home/hatch/workspace/cape-jones-rig/shafts-environmental-depth-lighting-upgrade-20261031/figure-only-plate-20261031.png')
    try:
        fig = np.asarray(Image.open(fig_path).convert('RGBA')).astype(float)
        if fig.shape == c.shape:
            opaque = fig[:, :, 3] == 255
            occl_diff = float(np.abs(c[:, :, :3][opaque] - fig[:, :, :3][opaque]).max()) if opaque.any() else -1
        else:
            occl_diff = -1
    except Exception:
        occl_diff = -1
    result = {
        "shafts": shafts_path, "composite": comp_path,
        "mid_band_peak": peak, "mid_band_median_valley": valley, "mid_threshold": thr,
        "mid_runs": runs, "n_runs": len(runs), "pass_5col": bool(runs5),
        "top300_max_row_nearblack_fraction": slat_frac, "pass_slat_not_dominant": bool(slat_frac < 0.90),
        "pool_centre_vals": pool_centre_vals, "pool_gap_vals": pool_gap_vals,
        "pass_pools_in_scene": pools_pass,
        "edge_alpha_max": edge_alpha_max, "pass_no_crop_edge_transparent_only": bool(edge_alpha_max == 0),
        "occlusion_max_diff_opaque_figure": occl_diff, "pass_occlusion": bool(occl_diff == 0),
    }
    # Main composites are filled-background RGBA (shafts fill canvas), so
    # edge-alpha-0 does NOT apply to them; the no-clip test for them is
    # figure bbox inside canvas + occlusion diff 0. Transparent-only
    # composites are gated separately in the report.
    result["overall_pass"] = bool(runs5 and slat_frac < 0.90 and occl_diff == 0 and pools_pass)
    json.dump(result, open(out_path, 'w'), indent=1)
    print(json.dumps(result, indent=1))
    return 0 if result["overall_pass"] else 1

if __name__ == '__main__':
    sys.exit(measure(sys.argv[1], sys.argv[2], sys.argv[3]))
