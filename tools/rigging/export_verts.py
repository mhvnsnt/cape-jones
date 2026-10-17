"""Export Cape Jones verts to npy for fast numpy joint analysis (one Blender run)."""
import bpy, os
import numpy as np
from mathutils import Matrix
from math import radians

bpy.ops.wm.read_factory_settings(use_empty=True)
f = os.path.expanduser('~/workspace/cj-rev2-scratch/cape_jones_plain.glb')
bpy.ops.import_scene.gltf(filepath=f)
ob = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
n = len(ob.data.vertices)
v = np.empty(n * 3, dtype=np.float64)
ob.data.vertices.foreach_get('co', v)
v = v.reshape(n, 3)
# Bake R_z(-90): (x,y,z) -> (y,-x,z): character faces -Y, L=+X (matches BlenRig)
R = np.array([[0., 1., 0.], [-1., 0., 0.], [0., 0., 1.]])
v = v @ R.T
# Feet at z=0: translate so min z = 0
v[:, 2] -= v[:, 2].min()
np.save('/tmp/cj_verts.npy', v.astype(np.float32))
print('SAVED', v.shape, 'zrange', v[:, 2].min(), v[:, 2].max(), 'height', v[:, 2].max() - v[:, 2].min())
