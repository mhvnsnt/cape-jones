# Gaussian Splatting for Cape Jones — 20261031

Approval: 0/1. No repo push. No original overwritten. 3D-SIDE-READY ONLY:
the current show focus is the 2D side. This does NOT turn the 2D work into a
3D project. It is a tool for the 3D side later, and an extra turn/depth tool
now. Mars already has FLA pieces to actually animate a turn — splatting is
an extra tool, NOT the only turn route, and NOT a replacement for those pieces.

## Plain explanation
Gaussian Splatting (3DGS) does not build a character out of triangles.
It builds a scene out of many soft 3D blobs — Gaussians. Each blob has a
position (x, y, z), a size/shape (scale, stretched in a direction), a colour,
and an opacity. To make a picture, each blob is projected ("splatted") onto
the screen as a soft ellipse, the blobs are sorted by depth, and they are
blended front-to-back. Move the camera and the same blobs re-project, so you
get a new view without re-drawing the character. That is why it matters for
Cape: novel views, depth, and turning around — if you have real multi-view
data. A single front plate alone cannot invent a back.

## What actually ran here (honest)
Source: rig-apose-v7c-clean-transparent.png (1100x1500), base art untouched.
Builder: build_splats.py (CPU, PIL + numpy + scipy, no GPU).
Gaussians: 5,846, stride 8 over solid alpha, sigma 3.2, opacity 0.85,
perspective focal 900, depth-sorted far-to-near alpha compositing.
Depth is a SYNTHETIC bulge proxy: distance-transform depth, max 81.9 px,
toward camera. It is NOT a true multi-view reconstruction, NOT a scanned
back, NOT a measured depth map. Turn views below are therefore a
depth-bulge rotation — they squeeze and shift like a turn, they do NOT show
a true back view. A true back still needs Mars's FLA back pieces.
Measurements: plate alpha 373,846 px; front splat alpha 250,408 px;
alpha IoU 0.647. The gap is sampling (stride 8 leaves holes) — this is a
splat-point proof, NOT a clean-plate replacement. Do not ship it as a plate.
Torch/CUDA: ABSENT on this VM (no torch module, no gsplat module, no GPU).
Vendor CUDA libraries below are therefore mappings, not runs. No paid GPU
run was made, none is claimed.

## Industry standard — 5
I1. Original 3DGS — Kerbl, Kopanas, Leimkuehler, Drettakis, SIGGRAPH 2023,
"3D Gaussian Splatting for Real-Time Radiance Field Rendering". Core:
anisotropic Gaussians, adaptive density control, differentiable tile
rasterizer, real-time novel views. RAN (CPU re-implementation of the core:
projection + depth sort + alpha blend, build_splats.py). Cape help: the
reference model every other item below extends.
I2. gsplat — Nerfstudio, open-source CUDA rasterizer with Python bindings
(Apache-2.0), up to 4x less training memory / ~15% less training time vs
the reference, plus MCMC densification and anti-aliasing options.
MAPPING ONLY: needs CUDA GPU + PyTorch 2.7+, neither present here.
Cape help: the production rasterizer to use on a Mars-approved free GPU
run (Kaggle/Colab) for a real trained splat, not this CPU proxy.
I3. Nerfstudio splatfacto — the 3DGS method inside the Nerfstudio
framework (UC Berkeley / NVIDIA community), gsplat-backed, 60+ fps
rendering, minutes-to-hours training. MAPPING ONLY, same GPU reason.
Cape help: the full training/viewer pipeline around gsplat — data,
training, export, viewer — when a real multi-view Cape set exists.
I4. PLY / .splat export + web splat viewers — the standard interchange
for Gaussian scenes (position, scale, colour, opacity per point).
RAN: cape-gaussians-20261031.ply, 5,846 vertices, header re-read and
verified; Blender 5.2.3 headless load RAN, cape-gaussians-blender-20261031.blend
with 5,846 vertices. Cape help: a Cape splat can be handed to any viewer
or to Blender without re-training.
I5. Blender 3DGS import / point-cloud route — load a Gaussian point set
into Blender as points/geometry, then render or composite from it.
RAN as a point cloud (blend above); a true Gaussian-shader render inside
Blender (splat ellipses, not points) is NOT run — that is a separate
Blender shader pass, still owed. Cape help: puts a splat into the existing
Blender 5.2.3 pipeline used for shafts/shading.

## Experimental — 5
E1. 4D Gaussian Splatting (dynamic / deformation-field 4DGS) — Gaussians
gain a time parameter, so the same set moves over time. RAN as a
time-parameter proxy: splat-4d-breathing-20261031.gif, 8 frames, gentle
y-scale pulse. Cape help: moving splats for motion, not just a still
turn — but a true trained 4DGS needs video/multi-view, not one plate.
E2. Mip-Splatting (Yu et al. 2024) — 3D smoothing + 2D mip filter to stop
aliasing when a splat is viewed far away or at low resolution. RAN as a
filter proxy: splat-mip-minus20-20261031.png, sigma x1.6. Cape help:
cleaner distant / small splat renders; the paper's exact 3D+2D filter
pair is a mapping on top of this proxy, not a separate trained run.
E3. Scaffold-GS (Lu et al., CVPR 2024) — structured anchors: a sparse
anchor grid predicts nearby Gaussians, view-adaptive and compact.
RAN as an anchor-count proxy: 1,949 anchors of 5,846 (every 3rd),
splat-scaffold-anchors-20261031.png. Cape help: fewer stored splats for
the same figure — the anchor-prediction network itself is a mapping.
E4. 2DGS (Huang et al. 2024) — surfels: Gaussians flattened into oriented
disks, with depth/normal consistency, for view-consistent surfaces and
clean mesh extraction. RAN as a flattening proxy: splat-2dgs-flattened-20261031.png,
sigma x1.6 / y0.55. Cape help: a splat that behaves like a surface, so a
Cape turn reads as a body surface rather than a cloud.
E5. Animatable Gaussian avatars (Animatable Gaussians; HumanGS-style
feed-forward SMPL-X Gaussian avatars; skinned Gaussian avatars) —
Gaussians attached to a body model and driven by linear-blend skinning,
so a pose change moves the splats. MAPPING + PARTIAL PROXY: no SMPL
body model for Cape exists here, and no multi-view avatar was trained;
the proxy principle is demonstrated by the turn sequence (group rotation
of the whole Gaussian set) and by the 4D time parameter. Cape help: the
long-term route to a poseable 3D Cape — it needs a Cape body rig and
multi-view data first, and it does NOT replace the 2D rig or the FLA turn.

## Files (all viewed by the builder agent; contact + front checked)
- splat-contact-20261031.png — front, turn -35, turn +35, 2DGS, mip
- splat-front-20261031.png, splat-turn-minus35-20261031.png,
  splat-turn-plus35-20261031.png, splat-2dgs-flattened-20261031.png,
  splat-mip-minus20-20261031.png, splat-scaffold-anchors-20261031.png
- splat-turn-sequence-20261031.gif (9 frames, -40 to +40 and back)
- splat-4d-breathing-20261031.gif (8 frames)
- splat-depth-proxy-20261031.png (bulge depth, synthetic, labelled)
- cape-gaussians-20261031.ply (5,846), cape-gaussians-blender-20261031.blend
- build_splats.py, measurements-20261031.json

## Still owed
Approval 0/1. True multi-view Cape capture (front + side + back plates
from Mars's FLA pieces, or a Mars-approved free GPU training run) 0/1;
real gsplat / splatfacto CUDA training run 0/1 (needs Mars-approved free
GPU run, never paid); true Blender Gaussian-shader render 0/1; per-pose
splat application beyond apose 0/1; a true back view from splats alone
is NOT owed as a claim — it is impossible from one front plate, and the
FLA back pieces are the route to it.
