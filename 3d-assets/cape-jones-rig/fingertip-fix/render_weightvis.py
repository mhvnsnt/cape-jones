# Visualize fingertip weights as vertex colors (no posing needed)
# RED = high forearm influence (BAD), BLUE = correct tip-bone influence (GOOD)
import bpy, sys
import numpy as np
blend, outdir, mode, tag = sys.argv[-4], sys.argv[-3], sys.argv[-2], sys.argv[-1]
# mode: 'bad' colors by forearm weight, 'good' colors by tip-bone weight
bpy.ops.wm.open_mainfile(filepath=blend)
mesh = max((o for o in bpy.data.objects if o.type=='MESH'), key=lambda o: len(o.data.vertices))
n = len(mesh.data.vertices)

# create vertex color layer
if "WeightVis" not in mesh.data.color_attributes:
    mesh.data.color_attributes.new(name="WeightVis", type='FLOAT_COLOR', domain='POINT')
ca = mesh.data.color_attributes["WeightVis"]

forearm_vgs = [mesh.vertex_groups.get(x) for x in ('forearm_L','forearm_R')]
tip_names = [b for b in mesh.vertex_groups.keys() if b.endswith('_3_L') or b.name.endswith('_3_R')] if False else \
    [vg.name for vg in mesh.vertex_groups if vg.name.endswith('_3_L') or vg.name.endswith('_3_R') or vg.name in ('finger_thumb_2_L','finger_thumb_2_R')]
tip_vgs = [mesh.vertex_groups.get(x) for x in tip_names]

colors = np.zeros((n,4), dtype=np.float32)
colors[:,3] = 1.0
for i in range(n):
    v = mesh.data.vertices[i]
    if mode == 'bad':
        w = 0.0
        for vg in forearm_vgs:
            if vg:
                try: w = max(w, vg.weight(i))
                except: pass
        # red intensity = forearm weight (only meaningful on fingers)
        colors[i,0] = min(1.0, w*3.0)
        colors[i,1] = colors[i,2] = 0.15
    else:
        w = 0.0
        for vg in tip_vgs:
            if vg:
                try: w = max(w, vg.weight(i))
                except: pass
        colors[i,2] = min(1.0, w*1.5)
        colors[i,0] = colors[i,1] = 0.15

ca.data.foreach_set('color', colors.ravel())
# use vertex colors in workbench
for mat in bpy.data.materials:
    mat.use_nodes = False
import mathutils
target = mathutils.Vector((-0.45, -0.04, 0.70))
cam_pos = mathutils.Vector((-0.45, -0.25, 0.80))
cam_data = bpy.data.cameras.new("C"); cam_data.lens=45
cam = bpy.data.objects.new("C", cam_data)
bpy.context.collection.objects.link(cam)
cam.location=cam_pos
cam.rotation_euler=((target-cam_pos).normalized().to_track_quat('-Z','Y')).to_euler()
bpy.context.scene.camera=cam
s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH'; s.display.shading.light='FLAT'
s.display.shading.color_type='VERTEX'
s.render.resolution_x=640; s.render.resolution_y=480; s.render.resolution_percentage=100
for ob in bpy.data.objects:
    for m in ob.modifiers:
        if m.type=='SUBSURF': m.render_levels=0; m.levels=0
        if m.type in ('CLOTH','CORRECTIVE_SMOOTH'): m.show_viewport=False; m.show_render=False
s.render.filepath=outdir+"/weightvis_%s_%s.png" % (mode, tag)
bpy.ops.render.render(write_still=True)
print("RENDERED", s.render.filepath, flush=True)
