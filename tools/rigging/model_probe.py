"""Probe Cape Jones GLB: dims, materials, verts. Headless."""
import bpy, os, sys
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
f = os.path.expanduser('~/workspace/cj-rev2-scratch/cape_jones_plain.glb')
bpy.ops.import_scene.gltf(filepath=f)
ob = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
xs=[c.x for c in bb]; ys=[c.y for c in bb]; zs=[c.z for c in bb]
print('VERTS', len(ob.data.vertices), 'FACES', len(ob.data.polygons))
print('H %.4f W %.4f D %.4f' % (max(zs)-min(zs), max(xs)-min(xs), max(ys)-min(ys)))
print('ZMIN %.4f ZMAX %.4f YMIN %.4f YMAX %.4f XMIN %.4f XMAX %.4f' % (min(zs), max(zs), min(ys), max(ys), min(xs), max(xs)))
for m in ob.data.materials:
    if m and m.use_nodes:
        bsdf = next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'), None)
        c = tuple(bsdf.inputs['Base Color'].default_value) if bsdf else None
        print('MAT', m.name, 'basecolor', [round(v,3) for v in c] if c else None)
