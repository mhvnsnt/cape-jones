# tools/rigging/ — Cape Jones rigging pipeline

Headless Blender 4.0.2 tools for the Cape Jones character rig.
Run with: `xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender -b --python <script.py>`

## Pipeline (in order)

| Script | Input | Output | What it does |
|---|---|---|---|
| `joint_detect.py` | `cape_jones_plain.glb` | `/tmp/cj_joints.json` | Cross-section slice analysis measuring every joint position from the mesh (no eyeballed pivots). |
| `export_verts.py` | GLB | `/tmp/cj_verts.npy` | Exports transformed vertex positions (baked R_z(-90°), feet at z=0). |
| `model_probe.py` | GLB | stdout | Probes model stats (verts, bbox, materials). |
| `blenrig_setup.py` | — | `.rig_tmp/cj_blenrig_raw.blend` | Imports GLB, applies rotation, adds BlenRig 6 biped (`bpy.ops.blenrig.add_biped_rig()` with viewport_toggle monkeypatched), scales rig rest ×0.544. |
| `blenrig_fit.py` | raw blend + joints | `.rig_tmp/cj_blenrig_fit.blend` | Fits 87 BlenRig guides to measured joints. **Note:** full control-rig retarget hits the headless boundary (see RIG-DOCS.md); the deliverable uses the custom deform rig below. |
| `blenrig_warp.py` | raw blend | `.rig_tmp/cj_blenrig_fit.blend` | Alternative: EDIT-mode rest warp (experimental). |
| `build_custom_rig.py` | raw blend + joints | `.rig_tmp/cj_custom_rig.blend` | Builds the 85-bone clean FK/IK deform rig (`CapeJones_Rig`) at measured joints, with driver-driven FK/IK switches, pole targets, wrist-blaster bones. |
| `weight_cage.py` | custom rig blend | `.rig_tmp/cj_weighted.blend` | Fits BlenRig's MDEF cage to character bbox; paints procedural zone weights (stretch vs locked, max 4 influences). |
| `bind_all.py` | weighted blend | `.rig_tmp/cj_bound.blend` | Binds cage→armature (dual-quaternion), character→cage (MeshDeform, precision 5), adds CorrectiveSmooth. |
| `cape_setup.py` | bound blend | `.rig_tmp/cj_cape_sep.blend` | Separates cape (y>0.10, 82,213 verts), sets #000000. |
| `test_poses.py` | cape_sep blend | `test-poses/*.png` | 7-pose Cycles render suite. |

## Licenses
All scripts are original code for this project. BlenRig 6 (used via `production/tools/blenrig6/`) is GPL-3.0.
