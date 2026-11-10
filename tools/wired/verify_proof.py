#!/usr/bin/env python3
"""Independent proof-clip verification for the EP01 rebuild.

Measures a candidate proof clip WITHOUT trusting the producing
lane's numbers:
  - ffprobe spec (codec, size, fps, frames, duration)
  - mean absolute frame-to-frame difference over ALL consecutive
    frames (native res, grayscale, 0-255 scale). CALIBRATED on
    this exact metric 2026-10-28 (selftest-*.json beside the
    script) — do not mix with the gen lane's sampled-frame RGB
    numbers (floor 1.2 / bundles 19-34 on THAT scale):
      true still (Forest plate):            0.005
      Storyboard Draft 1 excerpt (stills):  0.473  (91.9% pairs near-identical)
      PR #389 Dorowani idle (real motion):  4.50   (3.1% pairs near-identical)
  - fraction of frame pairs that are near-identical (diff < 0.5),
    which exposes held/stills footage even when a few cuts move
  - TIMING PROFILE (added 2026-10-28, THE BAR programme — see
    show/production/animation-method/TIMING-STANDARD.md): the
    hold-length structure of the clip on this same metric.
    A frame pair with diff < 0.5 counts as a HOLD (the drawing
    did not change); a pair at or above it is a CHANGE point.
    From the run-lengths of held spans the profile reports:
      * hold-length distribution (how many spans of each length)
      * effective unique drawings per second (spans / duration)
      * grid fit: what fraction of change boundaries land on
        multiples of 2 and of 3 frames (the 2s and 3s grids)
      * the longest internal hold (a hold that touches neither
        the first nor the last frame — whether the subject was
        *meant* to be moving during it is read off the timing
        chart by a reviewer, never by this script)
      * accent candidates: isolated 1-frame spans bounded by
        changes on both sides (the shape of a 1s accent/smear)
      * sub-threshold drift: pairs that changed but stayed
        under the hold threshold (held drawings do not drift)
      * below-bar signature flags: interpolation_profile
        (continuous per-frame change, no held drawings) and
        uniform_unmodulated_rate (one rate, whole clip, no
        accents) — the two signatures TIMING-STANDARD.md names
        as below the bar
    Hold lengths are FRAMES PER DRAWING at a 24 fps master; the
    profile always also prints effective DRAWINGS PER SECOND
    (3 frames/drawing = 8/sec, 2 = 12/sec, 1 = 24/sec).
    The profile REPORTS measurements only. It never passes or
    fails a clip: the grade is the correct character performing
    the action, judged by the owner/scorer (grading law).
  - sha256 + byte size for the presentation record

Usage: verify_proof.py <clip.mp4> [--json-out result.json]
       [--register scene|credits]
       [--chart chart.json] [--chart-tolerance N]
       [--likeness canon-reference.png]
       [--comparison-sheet sheet.png] [--likeness-runs runs.json]
Exit 0 always (this measures; the gate verdict is the owner's).

CHART CONFORMANCE (Above-the-Floor programme, 2026-10-28):
--chart <chart.json> adds a chart-conformance section. The chart
is a mochiichao/timing-chart/v1 document (segments per character,
accents, line holds, contacts — see the EP01 timing folder). The
checker compares the clip's measured change frames (span starts
on the same HOLD_THRESHOLD metric) against the chart: every
charted ACCENT and CONTACT must be answered by a change frame
within +-tolerance frames (default 2, --chart-tolerance); a
charted line HOLD must contain no change frame strictly inside
its tolerance-trimmed interior; segment-boundary coverage is
reported (what fraction of the chart's drawing-change frames,
union over characters, the clip answers within tolerance, and
how many clip changes the chart does not predict). Deviations
are reported BY FRAME NUMBER. Conformance is a measurement, not
a grade: it never changes the verdict line or the exit code.

HEADLINE OUTPUT (owner's unit rule, 2026-10-28): the profile's
headline is the clip's MEASURED effective NEW DRAWINGS PER
SECOND, with its class printed plainly: at or below ~3/sec is
the FAILED class (the storyboard signature); an interpolation
signature is also FAILED class (its changes are noise, not
authored drawings); below the declared register's floor
(scene 12/sec, credits 8/sec) is BELOW BAR. The headline is
also printed to stderr for humans; the JSON carries it as
timing_profile.headline.

LIKENESS MODE (added 2026-10-28 — the Gap 15 countermeasure;
see the dated correction at Gap 15 in
show/production/animation-method/WHAT-WE-DO-WRONG-ADDENDUM-2.md
and the standing delivery requirement in METHOD-REGISTRY.md):
--likeness <canon-reference.png> measures per-frame similarity
DIAGNOSTICS between the clip's distinct drawings (the span-start
frames of the same HOLD_THRESHOLD span structure the timing
profile computes) and a canon reference image. It exists
because a clip can pass every timing measure while not being
the character at all: the above-floor walk proof measured
10.0 new drawings/sec on a puppet redrawn from geometric
primitives (Gap 15), and the owner rejected it as a character
product. Likeness itself is graded by the owner's eye (grading
law: wrong character = FAIL, full stop); this mode only
quantifies drift so a delivery can state it in numbers up
front. It reports; it never grades; exit stays 0.
Metrics (numpy/PIL only — no metric library is assumed):
  * ssim — sliding-window SSIM (11x11 box filter, standard
    constants) between the reference and each sampled frame,
    both foreground-aligned: each image's foreground bounding
    box is cropped, resized to 96x96, and composited over
    neutral gray, so the measure compares the figure, not
    the stage.
  * color_histogram_l1 / color_histogram_bhattacharyya —
    4x4x4 RGB histograms over foreground pixels only (L1 form:
    0 = identical palette use, 1 = disjoint; Bhattacharyya
    coefficient: 1 = identical, 0 = disjoint).
  * silhouette_iou — intersection-over-union of the aligned
    foreground masks.
  * mean_abs_rgb_diff — 0-255 mean absolute difference of the
    aligned composites (same scale family as the frame-diff
    metric, but reference-vs-frame, not frame-vs-frame).
Foreground heuristic, stated so a reviewer knows exactly what
was measured: the reference by its alpha channel when it has
one, else by distance from its corner colour; a clip frame by
distance from its own corner colour (the proofs sit on a flat
field); any mask row spanning >= 90% of the frame width (a
1-2 px stage line is furniture, not subject) is dropped, and
the largest connected component — the subject — is kept, so
stage lines and stray shadow smears do not enter the frame's
foreground.
Each likeness run appends a RUN RECORD to likeness-runs.json
beside this script (override with --likeness-runs). The record
logs the reference path + sha256 and REQUIRES a side-by-side
comparison sheet: pass --comparison-sheet <sheet.png>; if it
is absent (or the file is not found) the record is still
written but marked INCOMPLETE — a completeness state of the
record, never a grade of the clip. likeness-runs.json is its
own file because timing-profile-runs.json is a keyed object,
not an appendable history; likeness appends are textual, so
every prior run's bytes stay an exact prefix of the file.
"""
import hashlib, json, subprocess, sys
from datetime import datetime
from pathlib import Path

import numpy as np

FLOOR_SLIDESHOW = 0.473   # Storyboard Draft 1 excerpt, this metric
ACCEPTED_BAND = (4.5, 4.5)  # PR #389 Dorowani idle, this metric (single point so far)
HOLD_THRESHOLD = 0.5      # frame-pair diff under this = the drawing held


def ffprobe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,size", "-show_entries",
         "stream=codec_name,width,height,avg_frame_rate,nb_frames",
         "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def frame_diffs(path):
    # Decode to raw gray frames via ffmpeg pipe; stream, don't load all.
    probe = ffprobe(path)
    v = next(s for s in probe["streams"] if "width" in s)
    w, h = v["width"], v["height"]
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf", "format=gray",
         "-f", "rawvideo", "-"],
        stdout=subprocess.PIPE)
    frame_bytes = w * h
    prev, diffs, identical = None, [], 0
    while True:
        buf = proc.stdout.read(frame_bytes)
        if len(buf) < frame_bytes:
            break
        cur = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
        if prev is not None:
            d = float(np.mean(np.abs(cur - prev)))
            diffs.append(d)
            if d < HOLD_THRESHOLD:
                identical += 1
        prev = cur
    proc.wait()
    return diffs, identical


REGISTER_FLOORS = {"scene": 12.0, "credits": 8.0}


def timing_profile(diffs, duration_s, register=None):
    """Hold-run structure of the clip from its frame-pair diffs.

    diffs[i] is the change between frame i and frame i+1 (0-based).
    A run (span) is a maximal set of consecutive frames joined by
    sub-threshold diffs; its length is its frame count.
    """
    n_frames = len(diffs) + 1
    spans = []            # (start_frame, length)
    start, length = 0, 1
    for i, d in enumerate(diffs):
        if d < HOLD_THRESHOLD:
            length += 1
        else:
            spans.append((start, length))
            start, length = i + 1, 1
    spans.append((start, length))

    def bucket(n):
        if n <= 6:
            return str(n)
        if n <= 11:
            return "7-11"
        if n <= 23:
            return "12-23"
        return "24+"

    hist = {}
    for _, ln in spans:
        hist[bucket(ln)] = hist.get(bucket(ln), 0) + 1
    hist = {k: hist[k] for k in sorted(hist, key=lambda x: (len(x), x))}

    def grid_fit(g):
        bounds = [s for s, _ in spans if s > 0]
        if not bounds:
            return None
        on = sum(1 for s in bounds if s % g == 0)
        return round(on / len(bounds), 4)

    def grid_fit_best_phase(g):
        # A clip may start mid-cycle, so its boundaries can sit on
        # the grid at a constant phase offset. Report the modal
        # offset and the fraction of boundaries that share it —
        # that fraction is the grid-consistency measure; the
        # absolute fit above is reported alongside, not instead.
        bounds = [s for s, _ in spans if s > 0]
        if not bounds:
            return None, None
        offs = {}
        for s in bounds:
            offs[s % g] = offs.get(s % g, 0) + 1
        best = max(offs, key=lambda k: offs[k])
        return best, round(offs[best] / len(bounds), 4)

    internal = [(s, ln) for s, ln in spans if s > 0 and s + ln < n_frames]
    longest_internal = max(internal, key=lambda t: t[1]) if internal else (None, 0)
    longest = max(spans, key=lambda t: t[1]) if spans else (0, 0)

    accents = [s for s, ln in spans
               if ln == 1 and 0 < s and s + ln < n_frames][:50]

    changed = [d for d in diffs if d >= HOLD_THRESHOLD]
    drift = [d for d in diffs if 0.0 < d < HOLD_THRESHOLD]

    # Pacing metrics (THE BAR programme, owner pacing verdict
    # 2026-10-28): retention is a production criterion. A near-
    # static run is a maximal span of frames joined by sub-
    # threshold pairs — the same spans as above, read as pacing.
    change_idx = [i for i, d in enumerate(diffs) if d >= HOLD_THRESHOLD]
    if duration_s:
        change_per_10s = round(len(change_idx) / duration_s * 10, 2)
    else:
        change_per_10s = None
    # Minimum change events in any rolling 10-second window
    # (windows stepped 1 second; only when the clip is >= 10 s).
    min_window = None
    win = 240  # 10 s of frame pairs at 24 fps
    if len(diffs) >= win:
        counts = []
        starts = list(range(0, len(diffs) - win + 1, 24))
        for st in starts:
            counts.append(sum(1 for i in change_idx if st <= i < st + win))
        min_window = min(counts) if counts else None
    pacing = {
        "longest_near_static_run_frames": longest[1],
        "longest_near_static_run_seconds": round(longest[1] / 24.0, 2),
        "longest_near_static_run_at_frame": longest[0],
        "change_events_total": len(change_idx),
        "change_events_per_10s": change_per_10s,
        "min_change_events_in_any_10s_window": min_window,
        "note": "Pacing measurements only. Whether a long near-static run is a "
                "charted dramatic hold or dead air is read against the timing "
                "chart by a reviewer (TIMING-STANDARD.md, pacing section).",
    }

    # Below-bar signatures (THE BAR programme, owner correction
    # 2026-10-28). These are measured signatures, named so a
    # reviewer sees them at a glance — they are not a verdict.
    # Units, always: hold lengths are FRAMES PER DRAWING at a
    # 24 fps master; the rate that matters on screen is new
    # drawings per second (3 frames/drawing = 8 drawings/sec,
    # 2 = 12/sec, 1 = 24/sec — full animation, the most work).
    n_spans = max(len(spans), 1)
    one_frame_share = sum(1 for _, ln in spans if ln == 1) / n_spans
    modal_len, modal_count = (0, 0)
    for _, ln in spans:
        c = sum(1 for _, l2 in spans if l2 == ln)
        if c > modal_count:
            modal_len, modal_count = ln, c
    modal_share = modal_count / n_spans
    near_identical_frac = (sum(1 for d in diffs if d < HOLD_THRESHOLD)
                           / len(diffs)) if diffs else 0.0
    flags = {
        "interpolation_profile": bool(one_frame_share >= 0.8
                                      and near_identical_frac < 0.3),
        "interpolation_profile_basis": {
            "one_frame_span_share": round(one_frame_share, 4),
            "near_identical_frac": round(near_identical_frac, 4)},
        "uniform_unmodulated_rate": bool(duration_s and duration_s >= 4.0
                                         and near_identical_frac >= 0.3
                                         and modal_share >= 0.95
                                         and not accents),
        "uniform_unmodulated_basis": {
            "modal_hold_frames_per_drawing": modal_len,
            "modal_span_share": round(modal_share, 4),
            "accent_candidates": len(accents)},
        "note": "A flag names a below-bar SIGNATURE (see TIMING-STANDARD.md): "
                "interpolation_profile = continuous per-frame change with no "
                "held drawings (the v1 signature); uniform_unmodulated_rate = "
                "held material at one rate for its whole length with no "
                "accent (a plain cycle LOOP under 4 s does not raise it — "
                "uniformity is judged at scene/instance scale). The grade "
                "of a clip remains the owner's/scorer's call.",
    }
    # HEADLINE (owner's unit rule, 2026-10-28): the headline number
    # for a clip is its MEASURED effective NEW DRAWINGS PER SECOND
    # — distinct authored drawings/sec from the span structure,
    # not frame-diff noise. Classes, printed plainly:
    #   * at or below ~3/sec  -> FAILED class (storyboard signature)
    #   * interpolation signature -> FAILED class (its per-frame
    #     changes are interpolation noise, not authored drawings,
    #     however high the raw change count runs)
    #   * below the declared register's floor -> BELOW BAR
    # Floors: scene body 12/sec in moving passages; credits (ED /
    # chibi register) 8/sec. Action accents run at 24/sec.
    eff_rate = (len(spans) / duration_s) if duration_s else None
    if flags["interpolation_profile"]:
        headline_class = ("FAILED class - interpolation signature: the "
                          "frame changes are interpolation noise, not "
                          "authored drawings")
    elif eff_rate is not None and eff_rate <= 3.0:
        headline_class = ("FAILED class - storyboard signature: at or "
                          "below ~3 new drawings per second")
    elif register in REGISTER_FLOORS:
        floor = REGISTER_FLOORS[register]
        if eff_rate is not None and eff_rate < floor:
            headline_class = ("BELOW BAR - under the %s floor of %g new "
                              "drawings per second" % (register, floor))
        else:
            headline_class = ("at or above the %s rate floor (%g new "
                              "drawings/sec) - rate only; grading is the "
                              "reviewer's call" % (register, floor))
    else:
        headline_class = ("no register declared - FAILED-class checks "
                          "applied; no floor verdict")
    headline = {
        "effective_new_drawings_per_second": round(eff_rate, 3) if eff_rate is not None else None,
        "register": register,
        "register_floor_new_drawings_per_second": REGISTER_FLOORS.get(register),
        "class": headline_class,
        "note": "Headline unit is NEW DRAWINGS PER SECOND (the owner's "
                "unit). A low figure is a failure signature, never an "
                "achievement or a style (TIMING-STANDARD.md).",
    }

    return {
        "headline": headline,
        "threshold": HOLD_THRESHOLD,
        "frames": n_frames,
        "spans_unique_drawings": len(spans),
        "effective_drawings_per_second": round(len(spans) / duration_s, 3) if duration_s else None,
        "hold_length_distribution": hist,
        "grid_fit_boundaries_on_2s": grid_fit(2),
        "grid_fit_boundaries_on_3s": grid_fit(3),
        "grid_fit_3s_best_phase_offset": grid_fit_best_phase(3)[0],
        "grid_fit_3s_best_phase_frac": grid_fit_best_phase(3)[1],
        "grid_fit_2s_best_phase_offset": grid_fit_best_phase(2)[0],
        "grid_fit_2s_best_phase_frac": grid_fit_best_phase(2)[1],
        "longest_hold_frames": longest[1],
        "longest_hold_at_frame": longest[0],
        "longest_hold_seconds": round(longest[1] / 24.0, 3),
        "longest_internal_hold_frames": longest_internal[1],
        "longest_internal_hold_at_frame": longest_internal[0],
        "accent_candidates_1f_spans": len([1 for s, ln in spans
                                           if ln == 1 and 0 < s and s + ln < n_frames]),
        "accent_candidate_frames": accents,
        "subthreshold_drift_pairs": len(drift),
        "subthreshold_drift_frac": round(len(drift) / len(diffs), 4) if diffs else 0,
        "median_diff_on_change_pairs": round(float(np.median(changed)), 3) if changed else 0,
        "below_bar_signatures": flags,
        "pacing": pacing,
        "note": "Measurements only — no verdict. Whether a long internal hold is a "
                "composed hold or a freeze is read against the timing chart by a reviewer.",
    }



def chart_conformance(diffs, chart, tolerance=2):
    """Compare a clip's measured change frames against a timing chart.

    diffs[i] is the change between frame i and i+1 (0-based), the
    same series timing_profile() reads. A change frame is the start
    frame of a held span after the first (the frame a new drawing
    lands on). Chart frames are 0-based in the clip's own window.
    Returns measurements + deviations by frame number; no verdict.
    """
    spans = []
    start = 0
    for i, d in enumerate(diffs):
        if d >= HOLD_THRESHOLD:
            spans.append((start, i + 1 - start))
            start = i + 1
    spans.append((start, len(diffs) + 1 - start))
    change_frames = sorted(s for s, _ in spans if s > 0)

    def nearest(frame):
        if not change_frames:
            return None
        return min(change_frames, key=lambda c: abs(c - frame))

    def answered(frame):
        # An event charted at frame 0 is landed by construction:
        # the clip opens on that drawing, so no change frame can
        # or must answer it.
        if frame == 0:
            return True, 0
        n = nearest(frame)
        return (n is not None and abs(n - frame) <= tolerance), n

    deviations = []
    accent_rows = []
    for a in chart.get("accents", []):
        f = a["frame"]
        ok, n = answered(f)
        accent_rows.append({"chart_frame": f, "label": a.get("label", ""),
                            "nearest_change_frame": n, "answered": ok})
        if not ok:
            deviations.append({"type": "accent", "chart_frame": f,
                               "nearest_change_frame": n,
                               "detail": "no change frame within +-%d frames of the charted accent" % tolerance})
    contact_rows = []
    for c in chart.get("contacts", []):
        f = c["frame"]
        ok, n = answered(f)
        contact_rows.append({"chart_frame": f, "character": c.get("character", ""),
                             "nearest_change_frame": n, "answered": ok})
        if not ok:
            deviations.append({"type": "contact", "chart_frame": f,
                               "character": c.get("character", ""),
                               "nearest_change_frame": n,
                               "detail": "no change frame within +-%d frames of the charted contact" % tolerance})
    hold_rows = []
    for h in chart.get("holds", []):
        st, ln = h["start"], h["frames"]
        lo, hi = st + tolerance, st + ln - tolerance
        inside = [c for c in change_frames if lo < c < hi]
        hold_rows.append({"chart_start": st, "chart_frames": ln,
                          "label": h.get("label", ""),
                          "changes_inside": inside, "clear": not inside})
        for c in inside:
            deviations.append({"type": "hold", "chart_start": st,
                               "chart_frames": ln, "change_frame": c,
                               "detail": "change frame inside a charted line hold"})
    expected = set()
    for _name, segs in (chart.get("characters") or {}).items():
        for sg in segs:
            if sg["start"] > 0:
                expected.add(sg["start"])
    answered = 0
    for f in expected:
        n = nearest(f)
        if n is not None and abs(n - f) <= tolerance:
            answered += 1
    uncharted = [c for c in change_frames
                 if all(abs(c - f) > tolerance for f in expected)]
    return {
        "chart_id": chart.get("id"),
        "chart_format": chart.get("format"),
        "tolerance_frames": tolerance,
        "clip_frames": len(diffs) + 1,
        "chart_duration_frames": chart.get("duration_frames"),
        "duration_match": chart.get("duration_frames") == len(diffs) + 1,
        "clip_change_frames": change_frames,
        "accents": accent_rows,
        "contacts": contact_rows,
        "holds": hold_rows,
        "segment_boundary_coverage": {
            "chart_change_frames_expected": len(expected),
            "answered_within_tolerance": answered,
            "fraction": round(answered / len(expected), 4) if expected else None,
            "uncharted_clip_changes": uncharted,
        },
        "deviations": deviations,
        "deviation_count": len(deviations),
        "note": "Conformance measurements only — deviations are reported "
                "by frame number for a reviewer; this section does not "
                "grade the clip (TIMING-STANDARD.md).",
    }

def _span_starts(diffs):
    """Start frame of each held span — the clip's distinct
    drawings — under the same HOLD_THRESHOLD rule the timing
    profile uses. These are the frames likeness mode samples."""
    starts, start = [], 0
    for i, d in enumerate(diffs):
        if d >= HOLD_THRESHOLD:
            starts.append(start)
            start = i + 1
    starts.append(start)
    return starts


def _foreground_mask(rgb, alpha=None):
    """Boolean foreground mask. With alpha: alpha > 8. Without:
    pixels differing from the corner colour by more than 24 in
    any channel (the flat-field heuristic stated in the module
    docstring)."""
    if alpha is not None:
        return alpha > 8
    corners = np.stack([rgb[0, 0], rgb[0, -1], rgb[-1, 0], rgb[-1, -1]])
    corner = np.median(corners.astype(np.float32), axis=0)
    return np.abs(rgb.astype(np.float32) - corner).max(axis=2) > 24


def _drop_stage_lines(mask, frac=0.90):
    """Drop mask rows spanning >= frac of the frame width —
    a thin full-width stage line is furniture, not subject."""
    wide = mask.mean(axis=1) >= frac
    if not wide.any():
        return mask
    out = mask.copy()
    out[wide, :] = False
    return out


def _largest_component(mask):
    """Largest 4-connected component of a boolean mask
    (run-length two-pass labelling, numpy only)."""
    parent = [0]

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    runs = []
    prev = []
    next_lab = 0
    for y in range(mask.shape[0]):
        d = np.diff(np.concatenate(([0], mask[y].view(np.int8), [0])))
        starts = np.nonzero(d == 1)[0]
        ends = np.nonzero(d == -1)[0] - 1
        cur = []
        for x0, x1 in zip(starts.tolist(), ends.tolist()):
            next_lab += 1
            parent.append(next_lab)
            for (_, px0, px1, plab) in prev:
                if px0 <= x1 and x0 <= px1:
                    ra, rb = find(next_lab), find(plab)
                    if ra != rb:
                        parent[max(ra, rb)] = min(ra, rb)
            cur.append((y, x0, x1, next_lab))
            runs.append((y, x0, x1, next_lab))
        prev = cur
    if not runs:
        return mask
    lab = np.zeros(mask.shape, dtype=np.int32)
    for (y, x0, x1, l) in runs:
        lab[y, x0:x1 + 1] = find(l)
    counts = np.bincount(lab.ravel())
    counts[0] = 0
    return lab == int(np.argmax(counts))


def _bbox(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def _aligned_composite(rgb, mask, size=96):
    """Crop to the foreground bounding box, resize to size x
    size, composite over neutral gray. Returns (composite float
    array, aligned boolean mask) or (None, None)."""
    from PIL import Image
    bb = _bbox(mask)
    if bb is None:
        return None, None
    x0, y0, x1, y1 = bb
    img = (Image.fromarray(rgb).crop((x0, y0, x1, y1))
           .resize((size, size), Image.BILINEAR))
    msk = (Image.fromarray((mask * 255).astype(np.uint8))
           .crop((x0, y0, x1, y1)).resize((size, size), Image.NEAREST))
    m = (np.asarray(msk) > 127).astype(np.float32)
    comp = (np.asarray(img).astype(np.float32) * m[:, :, None]
            + 128.0 * (1.0 - m[:, :, None]))
    return comp, m > 0.5


def _box_mean(a, win):
    """Uniform (box) filter via cumulative sums, edge-padded."""
    r = win // 2
    p = np.pad(a, r, mode="edge")
    c = np.pad(np.cumsum(np.cumsum(p, axis=0), axis=1), ((1, 0), (1, 0)))
    H, W = a.shape
    return (c[win:win + H, win:win + W] - c[0:H, win:win + W]
            - c[win:win + H, 0:W] + c[0:H, 0:W]) / float(win * win)


def _ssim(a, b, win=11):
    """Sliding-window SSIM between two same-size grayscale
    float arrays (0-255 scale), standard constants; the mean is
    taken over the valid interior of the SSIM map."""
    C1, C2 = (0.01 * 255.0) ** 2, (0.03 * 255.0) ** 2
    mu_a, mu_b = _box_mean(a, win), _box_mean(b, win)
    va = _box_mean(a * a, win) - mu_a ** 2
    vb = _box_mean(b * b, win) - mu_b ** 2
    cov = _box_mean(a * b, win) - mu_a * mu_b
    m = ((2 * mu_a * mu_b + C1) * (2 * cov + C2)
         / ((mu_a ** 2 + mu_b ** 2 + C1) * (va + vb + C2)))
    r = win // 2
    if m.shape[0] > win and m.shape[1] > win:
        return float(m[r:-r, r:-r].mean())
    return float(m.mean())


def _color_hist(rgb, mask, bins=4):
    """Normalised bins^3 RGB histogram over foreground pixels."""
    px = rgb[mask]
    if len(px) == 0:
        return np.zeros(bins ** 3)
    idx = (px.astype(np.int32) * bins // 256).clip(0, bins - 1)
    code = (idx[:, 0] * bins + idx[:, 1]) * bins + idx[:, 2]
    h = np.bincount(code, minlength=bins ** 3).astype(np.float64)
    return h / h.sum()


def likeness_profile(clip, diffs, ref_path, comparison_sheet=None):
    """Per-frame similarity diagnostics of a clip's distinct
    drawings against a canon reference image. Diagnostics only
    — see the module docstring's LIKENESS MODE section."""
    from PIL import Image
    ref_path = Path(ref_path)
    ref_bytes = ref_path.read_bytes()
    ref_img = Image.open(ref_path)
    has_alpha = (ref_img.mode in ("RGBA", "LA")
                 or (ref_img.mode == "P" and "transparency" in ref_img.info))
    ref_rgba = np.asarray(ref_img.convert("RGBA"))
    ref_rgb = ref_rgba[:, :, :3]
    ref_mask = _foreground_mask(ref_rgb, ref_rgba[:, :, 3] if has_alpha else None)
    ref_comp, ref_amask = _aligned_composite(ref_rgb, ref_mask)
    ref_hist = _color_hist(ref_rgb, ref_mask)
    ref_gray = ref_comp.mean(axis=2)

    starts = _span_starts(diffs)
    probe = ffprobe(clip)
    v = next(s for s in probe["streams"] if "width" in s)
    w, h = v["width"], v["height"]
    want = set(starts)
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(clip), "-vf", "format=rgb24",
         "-f", "rawvideo", "-"],
        stdout=subprocess.PIPE)
    frame_bytes = w * h * 3
    rows, idx = [], 0
    while True:
        buf = proc.stdout.read(frame_bytes)
        if len(buf) < frame_bytes:
            break
        if idx in want:
            rgb = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 3)
            mask = _largest_component(
                _drop_stage_lines(_foreground_mask(rgb)))
            comp, amask = _aligned_composite(rgb, mask)
            if comp is not None:
                fh = _color_hist(rgb, mask)
                union = int(np.logical_or(ref_amask, amask).sum())
                rows.append({
                    "frame": idx,
                    "ssim": round(_ssim(ref_gray, comp.mean(axis=2)), 4),
                    "color_histogram_l1": round(
                        0.5 * float(np.abs(ref_hist - fh).sum()), 4),
                    "color_histogram_bhattacharyya": round(
                        float(np.sqrt(ref_hist * fh).sum()), 4),
                    "silhouette_iou": round(
                        float(np.logical_and(ref_amask, amask).sum())
                        / max(union, 1), 4),
                    "mean_abs_rgb_diff": round(
                        float(np.abs(ref_comp - comp).mean()), 3),
                })
        idx += 1
    proc.wait()

    def summ(key):
        vals = [r[key] for r in rows]
        if not vals:
            return None
        return {"min": round(min(vals), 4),
                "median": round(float(np.median(vals)), 4),
                "max": round(max(vals), 4)}

    sheet = None
    if comparison_sheet:
        sp = Path(comparison_sheet)
        sheet = {"path": str(sp), "present": bool(sp.exists())}
        if sp.exists():
            sb = sp.read_bytes()
            sheet.update({"bytes": len(sb),
                          "sha256": hashlib.sha256(sb).hexdigest()})
    complete = bool(sheet and sheet["present"])
    return {
        "reference": {"path": str(ref_path), "bytes": len(ref_bytes),
                      "sha256": hashlib.sha256(ref_bytes).hexdigest()},
        "sampled_frames": starts,
        "frames_evaluated": len(rows),
        "per_frame": rows,
        "summary": {k: summ(k) for k in (
            "ssim", "color_histogram_l1", "color_histogram_bhattacharyya",
            "silhouette_iou", "mean_abs_rgb_diff")},
        "comparison_sheet": sheet,
        "record_status": (
            "COMPLETE" if complete else
            "INCOMPLETE - no comparison sheet recorded (pass "
            "--comparison-sheet <sheet.png>); the sheet must sit "
            "beside this record for the delivery requirement in "
            "METHOD-REGISTRY.md to be met. A completeness state "
            "of the record, not a grade of the clip."),
        "note": "Similarity DIAGNOSTICS only: they quantify drift "
                "against the canon reference; they never grade the "
                "clip. The grade is the correct character performing "
                "the action, judged by the owner/scorer (grading "
                "law). Alignment is by foreground bounding box, so "
                "read the numbers as a drift measure, not a "
                "likeness verdict.",
    }


def append_likeness_run(record, runs_path):
    """Append one run record to a likeness-runs.json (a JSON
    array). The append is textual — the new record is inserted
    before the closing bracket — so every prior run's bytes
    stay an exact prefix of the file."""
    text = json.dumps(record, indent=2)
    indented = "\n".join("  " + ln for ln in text.splitlines())
    p = Path(runs_path)
    if p.exists():
        core = p.read_bytes().decode().rstrip()
        assert core.endswith("]"), "likeness runs file is not a JSON array"
        p.write_text(core[:-1].rstrip() + ",\n" + indented + "\n]\n")
    else:
        p.write_text("[\n" + indented + "\n]\n")


def main():
    clip = Path(sys.argv[1])
    assert clip.exists(), f"no such file: {clip}"
    data = clip.read_bytes()
    diffs, identical = frame_diffs(clip)
    mean_diff = sum(diffs) / len(diffs) if diffs else 0.0
    probe = ffprobe(clip)
    duration = float(probe["format"]["duration"])
    result = {
        "clip": str(clip),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "ffprobe": probe,
        "frame_pairs": len(diffs),
        "mean_frame_diff": round(mean_diff, 3),
        "median_frame_diff": round(float(np.median(diffs)), 3) if diffs else 0,
        "near_identical_pairs": identical,
        "near_identical_frac": round(identical / len(diffs), 4) if diffs else 0,
        "timing_profile": timing_profile(
            diffs, duration,
            register=(sys.argv[sys.argv.index("--register") + 1]
                      if "--register" in sys.argv else None)),
        "references": {
            "slideshow_floor": FLOOR_SLIDESHOW,
            "accepted_bundle_band": ACCEPTED_BAND,
        },
        "reads_as_real_motion": mean_diff > 2.0 and identical / max(len(diffs), 1) < 0.5,
        "verdict": "MEASURED — owner viewing decides; this script promotes nothing",
    }
    if "--chart" in sys.argv:
        _chart_path = sys.argv[sys.argv.index("--chart") + 1]
        _tol = (int(sys.argv[sys.argv.index("--chart-tolerance") + 1])
                if "--chart-tolerance" in sys.argv else 2)
        with open(_chart_path) as _fh:
            _chart_doc = json.load(_fh)
        _conf = chart_conformance(diffs, _chart_doc, tolerance=_tol)
        result["chart_conformance"] = _conf
        print("CHART CONFORMANCE: %d deviation(s) against %s "
              "(accents %d/%d, contacts %d/%d, holds %d/%d clear, "
              "boundary coverage %s)"
              % (_conf["deviation_count"], _conf["chart_id"],
                 sum(1 for a in _conf["accents"] if a["answered"]),
                 len(_conf["accents"]),
                 sum(1 for c in _conf["contacts"] if c["answered"]),
                 len(_conf["contacts"]),
                 sum(1 for h in _conf["holds"] if h["clear"]),
                 len(_conf["holds"]),
                 _conf["segment_boundary_coverage"]["fraction"]),
              file=sys.stderr)
    if "--likeness" in sys.argv:
        _ref = sys.argv[sys.argv.index("--likeness") + 1]
        _sheet = (sys.argv[sys.argv.index("--comparison-sheet") + 1]
                  if "--comparison-sheet" in sys.argv else None)
        _lik = likeness_profile(clip, diffs, _ref, _sheet)
        result["likeness"] = _lik
        _runs = (sys.argv[sys.argv.index("--likeness-runs") + 1]
                 if "--likeness-runs" in sys.argv
                 else str(Path(__file__).with_name("likeness-runs.json")))
        append_likeness_run({
            "recorded_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "clip": str(clip), "clip_bytes": len(data),
            "clip_sha256": result["sha256"],
            "reference": _lik["reference"],
            "comparison_sheet": _lik["comparison_sheet"],
            "frames_evaluated": _lik["frames_evaluated"],
            "sampled_frames": _lik["sampled_frames"],
            "summary": _lik["summary"],
            "record_status": _lik["record_status"],
            "note": _lik["note"],
        }, _runs)
        _s = _lik["summary"]
        print("LIKENESS (diagnostics, not a grade): median SSIM %s, "
              "median colour-histogram L1 %s, median silhouette IoU %s "
              "over %d sampled drawings vs %s; run record %s -> %s"
              % (_s["ssim"]["median"], _s["color_histogram_l1"]["median"],
                 _s["silhouette_iou"]["median"], _lik["frames_evaluated"],
                 Path(_ref).name, _lik["record_status"], _runs),
              file=sys.stderr)
    _h = result["timing_profile"]["headline"]
    print("HEADLINE: %s new drawings/sec - %s"
          % (_h["effective_new_drawings_per_second"], _h["class"]),
          file=sys.stderr)
    print(json.dumps(result, indent=2))
    if "--json-out" in sys.argv:
        out = sys.argv[sys.argv.index("--json-out") + 1]
        Path(out).write_text(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
