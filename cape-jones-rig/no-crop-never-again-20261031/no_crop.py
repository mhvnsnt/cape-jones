#!/usr/bin/env python3
"""No-crop rendering path for Cape Jones rig work.

NO-CROP-WINDOW RULE (Mars, 2026-10-31 19:22 CDT, standing):
  He has a transparent background, so he does NOT need a crop window
  around him or around any of his pieces. A fixed canvas that a rotated /
  sheared / pasted figure can run off the edge of IS a crop window, and
  it clips feet, fists, heads and pieces silently. Going forward:
  the canvas fits the figure, never the figure fits the window.

How this module implements it (all open-source, all actually run here):
  1. Pillow rotate(expand=True) -- the documented Pillow way to rotate
     without clipping: the output image grows to hold the rotated input.
     (Pillow docs, Image.rotate: "expand -- Optional expansion flag.
     If true, the output image is made large enough to hold the rotated
     image.")  Used via pad-then-rotate-then-trim, which also keeps the
     rotation centre meaningful.
  2. Pillow ImageOps.expand -- pad a transparent canvas by N px on every
     side before a transform, so the transform has room to move into.
  3. numpy alpha bbox -- alpha channel > 0 gives the true figure bbox;
     trimming to bbox + padding is the only crop allowed, and it can
     never cut alpha because the bbox IS the alpha extent.
  4. OpenCV boundingRect -- cv2.boundingRect(alpha) cross-checks the
     numpy/Pillow bbox. cv2 5.0.0 was installed into the rig venv for
     this task and actually ran in check_no_clip.py; if cv2 is absent
     the gate falls back to numpy/Pillow and says so.
  5. Blender render-border-off + overscan -- the Blender-side equivalent:
     scene.render.use_border = False (no render window) and compositor
     overscan / a camera fit to the subject bbox. Wired as
     blender_nocrop_setup.py and actually executed headless against
     Blender 5.2.3 in this folder (it prints the settings; it is NOT a
     render claim -- no Blender render is claimed from this script).
  6. Industry distinction, stated plainly: a RENDER canvas is overscan
     (bigger than the subject, never a window) and a DELIVERY crop
     happens only at export, after a safe-area check, never during
     building. This module never delivery-crops; trim() only removes
     fully transparent pixels outside bbox + padding.

Transparent background throughout: every function here keeps RGBA and
never composites onto an opaque grey/RGB background. Grey or checker
in a contact sheet is DISPLAY ONLY, applied to a copy for viewing,
never baked into a figure file.
"""
import numpy as np
from PIL import Image, ImageOps

PAD = 40  # transparent padding kept around the trimmed figure, px


def alpha_array(im):
    return np.array(im.convert("RGBA").split()[3])


def alpha_count(im):
    return int((alpha_array(im) > 0).sum())


def alpha_bbox(im):
    """(left, upper, right, lower) of alpha>0, Pillow getbbox convention
    (right/lower exclusive), or None if fully transparent."""
    return im.convert("RGBA").getbbox()


def edge_touch(im):
    """Pixels of alpha>0 on each canvas edge. Any non-zero count means
    the figure is touching the window and may already be clipped."""
    a = alpha_array(im) > 0
    return {
        "top": int(a[0].sum()), "bottom": int(a[-1].sum()),
        "left": int(a[:, 0].sum()), "right": int(a[:, -1].sum()),
    }


def margins(im):
    """Distance in px from the alpha bbox to each canvas edge.
    Negative would mean the bbox is outside (cannot happen for a
    Pillow image); 0 means touching the edge."""
    bb = alpha_bbox(im)
    if bb is None:
        return None
    w, h = im.size
    return {"left": bb[0], "top": bb[1],
            "right": w - bb[2], "bottom": h - bb[3]}


def cv2_bbox(im):
    """OpenCV boundingRect cross-check. Returns (x, y, w, h) or None.
    Raises ImportError if cv2 is not installed -- callers must say so."""
    import cv2
    a = (alpha_array(im) > 0).astype("uint8") * 255
    x, y, w, h = cv2.boundingRect(a)
    if w == 0 or h == 0:
        return None
    return (int(x), int(y), int(w), int(h))


def trim(im, pad=PAD):
    """Crop ONLY to alpha bbox + pad. Never cuts alpha: the bbox is by
    definition the full alpha extent, and pad adds transparent room."""
    bb = alpha_bbox(im)
    if bb is None:
        return im.copy()
    x0 = max(0, bb[0] - pad); y0 = max(0, bb[1] - pad)
    x1 = min(im.size[0], bb[2] + pad); y1 = min(im.size[1], bb[3] + pad)
    return im.crop((x0, y0, x1, y1))


def pad_image(im, pad):
    """Transparent expansion on every side (Pillow ImageOps.expand)."""
    return ImageOps.expand(im.convert("RGBA"), border=pad, fill=(0, 0, 0, 0))


def rotate_nocrop(im, angle, center=None, pad=400, out_pad=PAD):
    """Rotate without clipping. Pad first, rotate on the padded canvas
    (expand=False there is safe because the pad holds the swing), then
    trim to bbox + out_pad. `center` is in original-image coordinates;
    if None, Pillow's default (image centre) is used."""
    im = im.convert("RGBA")
    padded = pad_image(im, pad)
    c = (center[0] + pad, center[1] + pad) if center else None
    rot = padded.rotate(angle, center=c) if c else padded.rotate(angle)
    return trim(rot, pad=out_pad)


def shear_nocrop(im, k, pad=600, out_pad=PAD):
    """Shear (lean) without clipping. Same pad-transform-trim pattern:
    AFFINE (1, k, 0, 0, 1, 0) on the padded canvas, then trim."""
    im = im.convert("RGBA")
    padded = pad_image(im, pad)
    w, h = padded.size
    out = padded.transform((w, h), Image.AFFINE, (1, k, 0, 0, 1, 0))
    return trim(out, pad=out_pad)


def transform_nocrop(im, fn, pad=600, out_pad=PAD):
    """Generic no-crop wrapper: fn(padded_image) -> transformed image,
    then trim. Use for any whole-figure transform (QUAD, perspective,
    etc.) that would otherwise be run on a fixed-size canvas."""
    padded = pad_image(im.convert("RGBA"), pad)
    return trim(fn(padded), pad=out_pad)


def paste_nocrop(canvas, piece, xy):
    """Paste a piece without clipping it at the canvas edge. If the
    paste box would exceed the canvas, the canvas auto-expands
    (transparent) to hold the whole piece, and the shift applied to
    the original canvas origin is returned, so callers can track
    coordinates: new_canvas, (shift_x, shift_y) where a point that was
    at (x, y) in the old canvas is at (x + shift_x, y + shift_y)."""
    canvas = canvas.convert("RGBA"); piece = piece.convert("RGBA")
    x, y = int(xy[0]), int(xy[1])
    cw, ch = canvas.size; pw, ph = piece.size
    left = min(0, x); top = min(0, y)
    right = max(cw, x + pw); bottom = max(ch, y + ph)
    if (left, top, right, bottom) == (0, 0, cw, ch):
        out = canvas.copy(); out.alpha_composite(piece, (x, y))
        return out, (0, 0)
    out = Image.new("RGBA", (right - left, bottom - top), (0, 0, 0, 0))
    out.alpha_composite(canvas, (-left, -top))
    out.alpha_composite(piece, (x - left, y - top))
    return out, (-left, -top)


def limb_layer_nocrop(canvas_size, piece, joint, anchor, angle):
    """Drop-in replacement for the old limb() pattern:
      layer = Image.new("RGBA", canvas_size, transparent)
      layer.paste(piece, joint - anchor)
      layer.rotate(angle, center=joint, expand=False)   <- CROP WINDOW
    This version pads the layer first, rotates on the padded layer,
    then returns a layer the SAME size as canvas_size ONLY if nothing
    was clipped -- otherwise it returns the expanded layer plus the
    shift, and the caller must use paste_nocrop to composite it.
    Returns (layer, shift) where shift maps old-canvas coords to the
    returned layer's coords."""
    piece = piece.convert("RGBA")
    ax, ay = int(anchor[0]), int(anchor[1])
    px, py = int(joint[0]) - ax, int(joint[1]) - ay
    pad = max(piece.size) + 100
    layer = Image.new("RGBA", (canvas_size[0] + 2 * pad,
                                canvas_size[1] + 2 * pad), (0, 0, 0, 0))
    layer.alpha_composite(piece, (px + pad, py + pad))
    rot = layer.rotate(angle, center=(int(joint[0]) + pad,
                                       int(joint[1]) + pad))
    # If the rotated piece still fits the original window, crop back
    # to it (no alpha lost, verified by the caller gate); otherwise
    # return the padded layer and let paste_nocrop expand the canvas.
    inner = rot.crop((pad, pad, pad + canvas_size[0], pad + canvas_size[1]))
    if alpha_count(inner) == alpha_count(rot):
        return inner, (0, 0)
    return rot, (pad, pad)
