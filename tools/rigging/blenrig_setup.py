"""BlenRig 6 headless rig driver for Cape Jones — STEP 1: setup + import + add biped.
Run: xvfb-run -a env -u PYTHONPATH blender -b --python blenrig_setup.py
Outputs: /tmp/cj_bones.json (bone names + parents + deform flags)
"""
import bpy, os, sys, json, zipfile, shutil
from mathutils import Vector

BLENDER = os.path.expanduser('~/workspace/tools/blender/blender-4.0.2-linux-x64/blender')
ADDON_DIR = os.path.expanduser('~/workspace/cj-rig-wt/production/tools/blenrig6')
MODEL = os.path.expanduser('~/workspace/cj-rev2-scratch/cape_jones_plain.glb')

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene

# ---- install + enable blenrig6 ----
zip_path = '/tmp/blenrig6_install.zip'
if os.path.exists(zip_path):
    os.remove(zip_path)
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(ADDON_DIR):
        for fn in files:
            if fn.endswith('.pyc') or '__pycache__' in root:
                continue
            full = os.path.join(root, fn)
            z.write(full, os.path.join('blenrig6', os.path.relpath(full, ADDON_DIR)))
try:
    bpy.ops.preferences.addon_install(filepath=zip_path)
except Exception as e:
    print('addon_install note:', e)
bpy.ops.preferences.addon_enable(module='blenrig6')
print('ADDON ENABLED:', bpy.context.preferences.addons.get('blenrig6') is not None)

# ---- import model ----
bpy.ops.import_scene.gltf(filepath=MODEL)
char = [o for o in scn.objects if o.type == 'MESH'][0]
char.name = 'CapeJones_Body'
print('CHAR:', char.name, len(char.data.vertices), 'verts')
# Bake R_z(-90): (x,y,z)->(y,-x,z) so the character faces -Y, L=+X (BlenRig
# convention); then feet at z=0. Rotation+translation only -- scale untouched.
import numpy as np
n = len(char.data.vertices)
v = np.empty(n * 3)
char.data.vertices.foreach_get('co', v)
v = v.reshape(n, 3)
R = np.array([[0., 1., 0.], [-1., 0., 0.], [0., 0., 1.]])
v = (v @ R.T)
v[:, 2] -= v[:, 2].min()
char.data.vertices.foreach_set('co', v.reshape(-1))
char.data.update()
print('CHAR TRANSFORMED: faces -Y, feet at z=0')

# ---- add blenrig biped (headless-safe: patch the screen-dependent viewport_toggle) ----
from blenrig6.blenrig_biped import ops_blenrig_biped_add as addmod
addmod.Operator_BlenRig5_Add_Biped.viewport_toggle = lambda self, context: None
bpy.ops.object.select_all(action='DESELECT')
r = bpy.ops.blenrig.add_biped_rig()
print('ADD BIPED RESULT:', r)
# find + select the armature
arm = None
for ob in bpy.data.objects:
    if ob.type == 'ARMATURE':
        for k, v in ob.data.items():
            if k == 'rig_name' and 'BlenRig_' in str(v):
                arm = ob
                break
print('ARMATURE:', arm.name if arm else None)
if arm is None:
    raise RuntimeError('no blenrig armature found after import')
arm.select_set(True)
scn.view_layers[0].objects.active = arm
bpy.context.view_layer.objects.active = arm
scn.blenrig_guide.arm_obj = arm
for ob in bpy.data.objects:
    if 'BlenRigMdefCage' in ob.name:
        for mod in ob.modifiers:
            if mod.type == 'ARMATURE' and mod.object == arm:
                scn.blenrig_guide.mdef_cage_obj = ob
                print('MDEF CAGE:', ob.name)
    if 'BlenRigMDefHeadWeightsModel' in ob.name:
        scn.blenrig_guide.mdef_head_weights_transfer_obj = ob
    if 'BlenRigMDefHandsWeightsModel' in ob.name:
        scn.blenrig_guide.mdef_hands_weights_transfer_obj = ob

# ---- dump bone inventory ----
bpy.ops.object.mode_set(mode='EDIT')
bones = []
for b in arm.data.edit_bones:
    bones.append({
        'name': b.name,
        'parent': b.parent.name if b.parent else None,
        'head': [round(v, 4) for v in b.head],
        'tail': [round(v, 4) for v in b.tail],
        'deform': b.use_deform,
    })
bpy.ops.object.mode_set(mode='OBJECT')
with open('/tmp/cj_bones.json', 'w') as f:
    json.dump(bones, f, indent=1)
print('BONES:', len(bones))
print('DEFORM BONES:', sum(1 for b in bones if b['deform']))
# save checkpoint blend
import shutil
os.makedirs(os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp'), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.expanduser('~/workspace/cj-rig-wt/.rig_tmp/cj_blenrig_raw.blend'))
if os.path.exists(zip_path):
    os.remove(zip_path)
print('SETUP DONE')
