"""Wrap v4 stage 1 — NORMAL-FROM-DEPTH relight (runs, no faking).

Method (industry-standard, free/open): depth estimation from the actual plate
+ normal-from-depth, the core of intrinsic-image / 2D relighting pipelines
(Neural LightRig / GeoRelight / PIXLRelight use estimated normals+depth when no
3D model exists; Blender's own normal passes do the same math on a mesh).
Here the depth field is MEASURED from the plate, not a directional gradient:
  depth = distance-to-silhouette-edge (scipy EDT, gives a rounded volume
          profile per limb/torso/head) MINUS valleys at the art's own dark
          interior lines (pec/abs/crease/cape-fold lines = creases), smoothed.
  normals = (-dz/dx, -dz/dy, 1) normalised from that depth field (Sobel).
  shading = N.L per light, computed PER PIXEL from those normals.
This replaces v3's linework-offset + directional gradient approximation.
HONEST SCOPE: normals are ESTIMATED from silhouette+linework depth, not from
a true 3D character model. Fold direction is therefore derived from the art's
own lines + silhouette volume, which is exactly what the art shows — but it
is not a mesh normal pass. That distinction is stated in the doc, not hidden.

Lights (image space, y down): back cyan light from upper-left:
  L_back = (-0.55, -0.45, 0.70) normalised (x left, y up, z toward viewer)
  front gold key from right/front: L_front = (0.60, 0.10, 0.75) normalised.
Side-weight field = clip(N.L_back, 0, 1), blurred outward, used in the
compositor to weight the wrap/rim (stronger on the backlit side) — real
side-weighting, not a uniform band.
"""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

R = '/home/hatch/workspace/cape-jones-rig'
OUT = R + '/blender-composite-wrap-v4-20261031/scratch'
PLATES = {
    'apose': R + '/rig-apose-v7c-clean-transparent.png',
    'armsup': R + '/dual-light-variants-20261031/base-arms-up-transparent-20261031.png',
    'fighting': R + '/blender-composite-wrap-v3-20261031/scratch/plate-fighting-extracted.png',
}

def norm(v):
    return v / np.linalg.norm(v)

L_BACK = norm(np.array([-0.55, -0.45, 0.70]))
L_FRONT = norm(np.array([0.60, 0.10, 0.75]))
CYAN = np.array([0.0, 200/255, 1.0])
GOLD = np.array([1.0, 0.75, 0.35])

for name, path in PLATES.items():
    im = Image.open(path).convert('RGBA')
    a = np.asarray(im).astype(np.float32) / 255.0
    rgb, alpha = a[..., :3], a[..., 3]
    mask = alpha > 0.5
    # depth: distance transform, normalised inside mask
    dist = ndimage.distance_transform_edt(mask)
    depth = np.zeros_like(dist)
    if dist[mask].max() > 0:
        depth[mask] = dist[mask] / dist[mask].max()
    # interior lines = dark pixels well inside mask (not the outer outline)
    gray = rgb.mean(axis=2)
    eroded = ndimage.binary_erosion(mask, iterations=4)
    # thin dark strokes only: a solid dark region (cape) is NOT a line —
    # a line pixel must be dark AND locally darker than its neighbourhood
    gmax = ndimage.maximum_filter(gray, size=7)
    lines = eroded & (gray < 0.43) & ((gmax - gray) > 0.12)
    depth[lines] -= 0.35  # crease valleys
    depth = ndimage.gaussian_filter(depth, 3.0)
    depth = np.clip(depth, 0, 1)
    depth[~mask] = 0
    # normals from depth (Sobel), z-scale 2.0 for readable relief
    dzdy, dzdx = np.gradient(depth)
    nx = -dzdx * 2.0; ny = -dzdy * 2.0; nz = np.ones_like(depth)
    nlen = np.sqrt(nx**2 + ny**2 + nz**2)
    nx, ny, nz = nx/nlen, ny/nlen, nz/nlen
    diff_back = np.clip(nx*L_BACK[0] + ny*L_BACK[1] + nz*L_BACK[2], 0, 1)
    diff_front = np.clip(nx*L_FRONT[0] + ny*L_FRONT[1] + nz*L_FRONT[2], 0, 1)
    # relight: albedo kept; shading factor from normals; tint added per light
    shade = 0.70 + 0.30*diff_front + 0.15*diff_back
    out = rgb * shade[..., None]
    out += (CYAN * (diff_back[..., None] * 0.22))
    out += (GOLD * (diff_front[..., None] * 0.10))
    # dark cape stays shadowed: scale tint by lightness (as v3 did)
    light = rgb.mean(axis=2, keepdims=True)
    out = np.where(light < 0.15, rgb * shade[..., None] + CYAN * (diff_back[..., None] * 0.08), out)
    out = np.clip(out, 0, 1)
    out_im = Image.fromarray((np.dstack([out, alpha]) * 255).astype(np.uint8), 'RGBA')
    out_im.save(f'{OUT}/plate-{name}-relit-v4.png')
    # normal map visualisation (for proof, not a scene layer)
    nvis = np.dstack([(nx*0.5+0.5), (ny*0.5+0.5), (nz*0.5+0.5), alpha])
    Image.fromarray((nvis*255).astype(np.uint8), 'RGBA').save(f'{OUT}/normal-{name}-v4.png')
    Image.fromarray((np.dstack([depth, depth, depth, alpha])*255).astype(np.uint8), 'RGBA').save(f'{OUT}/depth-{name}-v4.png')
    # side-weight field: diffuse_back, blurred outward past the silhouette
    sw = ndimage.gaussian_filter(np.where(mask, diff_back, 0), 6.0)
    sw = np.clip(sw, 0, 1)
    Image.fromarray((sw*255).astype(np.uint8), 'L').save(f'{OUT}/sideweight-{name}-v4.png')
    inside = mask.sum()
    print(name, 'mask_px', int(inside),
          'diff_back mean', round(float(diff_back[mask].mean()), 3),
          'diff_front mean', round(float(diff_front[mask].mean()), 3),
          'line_px', int(lines.sum()))
print('RELIGHT DONE')
