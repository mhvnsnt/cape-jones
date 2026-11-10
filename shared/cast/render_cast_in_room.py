"""Proof render: place a western-heart cast GLB in the Cape Jones living room (rest pose, no fight anims touched).
blender -b 3d-assets/living_room.blend -P shared/cast/render_cast_in_room.py -- <glb> <rotate_y_deg> <out_prefix>
Never saves the .blend (living_room.blend stays untouched)."""
import bpy, sys, math, json, mathutils
def bbox(objs):
    dg = bpy.context.evaluated_depsgraph_get(); mins = mathutils.Vector((1e9,)*3); maxs = -mins
    for o in objs:
        if o.type != 'MESH': continue
        e = o.evaluated_get(dg); me = e.to_mesh()
        for v in me.vertices:
            w = e.matrix_world @ v.co; mins = mathutils.Vector(map(min, mins, w)); maxs = mathutils.Vector(map(max, maxs, w))
        e.to_mesh_clear()
    return mins, maxs
a = sys.argv[sys.argv.index("--")+1:]
glb, rot, out = a[0], float(a[1]), a[2]
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=glb)
new = [o for o in bpy.data.objects if o not in before]
# GLB strays (e.g. pantera's unparented 'Icosphere' helper) are hidden in THIS render only; GLB is not edited
strays = [o for o in new if o.type == 'MESH' and not (o.parent and o.parent.type == 'ARMATURE')]
for o in strays: o.hide_render = True; o.hide_viewport = True
new = [o for o in new if o not in strays]
roots = [o for o in new if o.parent is None]
# scale to 1.8 m tall, stand on floor, on the rug area facing the TV-room camera
mins, maxs = bbox(new)
h = maxs.z - mins.z
s = 1.8 / h if h > 0 else 1
floor = min((o.matrix_world @ mathutils.Vector(c)).z for o in bpy.data.objects if o.type=='MESH' and o not in new and 'floor' in o.name.lower() for c in o.bound_box) if any('floor' in o.name.lower() for o in bpy.data.objects if o not in new) else 0.0
target = mathutils.Vector(json.loads(a[3])) if len(a) > 3 else mathutils.Vector((0, 0, 0))
for r in roots:
    r.scale = [v*s for v in r.scale]
    r.rotation_mode = 'XYZ'; r.rotation_euler.z += math.radians(rot)
bpy.context.view_layer.update()
mins, maxs = bbox(new)
ctr = (mins + maxs) / 2
off = mathutils.Vector((target.x - ctr.x, target.y - ctr.y, target.z - mins.z))
for r in roots: r.location += off
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 48
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
info = {"glb": glb, "height_m_before_scale": h, "scale": s, "placed_at": list(off), "camera": sc.camera.name if sc.camera else None,
        "objects": [o.name for o in new][:20], "hidden_strays": [o.name for o in strays]}
print("CASTINFO", json.dumps(info))
sc.render.filepath = out + "_scene_cam.png"; bpy.ops.render.render(write_still=True)
# second view: close camera aimed at the character
cam = bpy.data.objects.new("castProofCam", bpy.data.cameras.new("castProofCam")); sc.collection.objects.link(cam)
look = mathutils.Vector((target.x, target.y, target.z + 0.95))
cam.location = look + mathutils.Vector((-0.8, -5.0, 0.0)) if len(a) < 5 else mathutils.Vector(json.loads(a[4]))
cam.rotation_euler = (look - cam.location).to_track_quat('-Z', 'Y').to_euler()
sc.camera = cam; sc.render.filepath = out + "_close.png"; bpy.ops.render.render(write_still=True)
