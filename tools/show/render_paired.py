"""Paired fight proof in Jungle Outpost (arena track's jungle-outpost.glb).
NLA choreography (30fps, scene frames):
  Cape:    stance 0..59 | spin-strike 60..81 | stance(recovery, turned away) 82..134
           | hit 135..155 | stance 156..160 | launch 170..184 (frames 0..14 ONLY:
           launch frames 15+ drive the pelvis below ground, measured) + follow
           offset keys (Cape tracks Pantera's lift/slam) | ko 186..225
  Pantera: stance loop 0..160 | approach (object loc) 110..135 | grab 161..195
           | stance (win stand-in) 196..235
  Comeback read: Cape strikes first (spin), ends turned away; Pantera closes,
  lands the blow (Cape stagger), then the chain grab finishes Cape (launch+KO).
  Pantera's grab is a suplex-style throw (attacker goes down with the victim);
  the win stance after it is the edit bridge to him standing over Cape.
Renders: 8 checkframes + realtime chain video frames 161..195.
"""
import bpy, os, sys, math
from mathutils import Vector, Quaternion
OUT = sys.argv[sys.argv.index("--") + 1]
os.makedirs(OUT, exist_ok=True)
bpy.context.scene.render.fps = 30
scn = bpy.context.scene
# --- arena ---
bpy.ops.import_scene.gltf(filepath="/home/hatch/workspace/ep1-fight-anim/jungle-outpost.glb")
arena_objs = [o for o in bpy.data.objects]
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
mn = Vector((1e9,)*3); mx = Vector((-1e9,)*3)
for o in arena_objs:
    if o.type != 'MESH': continue
    e = o.evaluated_get(dg)
    try: me = e.to_mesh()
    except Exception: continue
    for v in me.vertices:
        w = e.matrix_world @ v.co; mn = Vector(map(min, mn, w)); mx = Vector(map(max, mx, w))
    e.to_mesh_clear()
print(f"ARENA bbox min={tuple(round(v,2) for v in mn)} max={tuple(round(v,2) for v in mx)}")
GROUND_Z = mn.z
CX, CY = (mn.x + mx.x) / 2, (mn.y + mx.y) / 2
# --- Cape ---
bpy.ops.import_scene.gltf(filepath="/home/hatch/workspace/scratch/cj-3d/cape-jones-show.glb")
cape = next(o for o in bpy.data.objects if o.type == 'ARMATURE' and o.name == 'CapeJones_Rig')
for o in bpy.data.objects:
    if o.type == 'MESH' and not (o.parent and o.parent.type == 'ARMATURE'):
        o.hide_render = True
# scale cape to 1.8 m tall (measure body mesh)
bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
mn2 = Vector((1e9,)*3); mx2 = Vector((-1e9,)*3)
for o in bpy.data.objects:
    if o.type != 'MESH' or o.name != 'CapeJones_Body': continue
    e = o.evaluated_get(dg); me = e.to_mesh()
    for v in me.vertices:
        w = e.matrix_world @ v.co; mn2 = Vector(map(min, mn2, w)); mx2 = Vector(map(max, mx2, w))
    e.to_mesh_clear()
cape.scale = (1.8 / (mx2.z - mn2.z),) * 3
cape.location = (CX, CY + 0.55, GROUND_Z)
print(f"CAPE scale {cape.scale[0]:.3f} at {tuple(cape.location)}")
# --- Pantera ---
bpy.ops.import_scene.gltf(filepath="/home/hatch/workspace/rig-audit-2026-10-23/main/pantera-leopard-king.glb")
pan = next(o for o in bpy.data.objects if o.type == 'ARMATURE' and o.name == 'Character')
for o in bpy.data.objects:
    if o.type == 'MESH' and not (o.parent and o.parent.type == 'ARMATURE') and o.name not in ('tripo_node_36243c06-de63-4673-8e71-a8c1947476fd',):
        o.hide_render = True
pan.rotation_mode = 'QUATERNION'
# stand up (Rx-90) then turn around (Rz180) to face +Y toward Cape
q_stand = Quaternion((0.7071067811865476, -0.7071067811865476, 0.0, 0.0))
q_turn = Quaternion((0.0, 0.0, 0.0, 1.0))  # 180deg about Z: (w=cos90=0, x=0,y=0,z=sin90=1)
pan.rotation_quaternion = q_turn @ q_stand
bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
mn3 = Vector((1e9,)*3); mx3 = Vector((-1e9,)*3)
for o in bpy.data.objects:
    if o.type != 'MESH' or 'tripo' not in o.name: continue
    e = o.evaluated_get(dg); me = e.to_mesh()
    for v in me.vertices:
        w = e.matrix_world @ v.co; mn3 = Vector(map(min, mn3, w)); mx3 = Vector(map(max, mx3, w))
    e.to_mesh_clear()
print(f"PANTERA pre-scale bbox min={tuple(round(v,2) for v in mn3)} max={tuple(round(v,2) for v in mx3)}")
# feet to ground: shift so bbox min z == GROUND_Z (after scale, approx via unscaled ratio)
pan.scale = (1.8 / max(mx3.z - mn3.z, 0.01),) * 3
pan.location = (CX, CY - 0.55, GROUND_Z - mn3.z * pan.scale[0])
print(f"PANTERA scale {pan.scale[0]:.3f} at {tuple(pan.location)}")
# --- NLA helper ---
def load_clip(arm, path):
    before = set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [x for x in bpy.data.actions if x not in before]
    assert len(new) == 1, (path, [x.name for x in new])
    for o in [o for o in bpy.data.objects]:
        pass
    return new[0]
def clear_anim(arm):
    if not arm.animation_data: arm.animation_data_create()
    arm.animation_data.action = None
    for tr in list(arm.animation_data.nla_tracks):
        arm.animation_data.nla_tracks.remove(tr)
    arm.animation_data.nla_tracks.new()
def strip(arm, action, start, a0, a1):
    if not arm.animation_data: arm.animation_data_create()
    tr = arm.animation_data.nla_tracks[0]
    st = tr.strips.new(action.name, int(start), action)
    st.action_frame_start = int(a0); st.action_frame_end = int(a1)
    st.extrapolation = 'HOLD'
    return st
def cleanup_clip_objects(before_objs):
    for o in [o for o in bpy.data.objects if o not in before_objs]:
        # keep only armatures' clip objects out; never delete cape/pan/arena/armature mains
        if o.type != 'ARMATURE':
            pass
    # clip imports also create armatures; remove non-main armatures
    for o in list(bpy.data.objects):
        if o.type == 'ARMATURE' and o not in (cape, pan):
            bpy.data.objects.remove(o, do_unlink=True)
C = "/home/hatch/workspace/ep1-fight-anim/clips/cape/"
P = "/home/hatch/workspace/ep1-fight-anim/clips/pantera/"
cape_acts = {}
for nm, fn in (("stance", "ep1_cape_stance.glb"), ("spin", "ep1_cape_strike_light.glb"),
               ("hit", "ep1_cape_hit.glb"), ("launch", "ep1_cape_hit_launch.glb"), ("ko", "ep1_cape_ko.glb")):
    before_objs = set(bpy.data.objects)
    cape_acts[nm] = load_clip(cape, C + fn)
    cleanup_clip_objects(before_objs)
pan_acts = {}
for nm, fn in (("stance", "ep1_pantera_stance.glb"), ("grab", "ep1_pantera_grab.glb")):
    before_objs = set(bpy.data.objects)
    pan_acts[nm] = load_clip(pan, P + fn)
    cleanup_clip_objects(before_objs)
# Cape strips
clear_anim(cape)
strip(cape, cape_acts["stance"], 0, 0, 59)
strip(cape, cape_acts["spin"], 60, 0, 21)
strip(cape, cape_acts["stance"], 82, 0, 52)
strip(cape, cape_acts["hit"], 135, 0, 20)
strip(cape, cape_acts["stance"], 156, 0, 4)
strip(cape, cape_acts["launch"], 170, 0, 14)
strip(cape, cape_acts["ko"], 186, 0, 39)
# Pantera strips
clear_anim(pan)
strip(pan, pan_acts["stance"], 0, 0, 74)
strip(pan, pan_acts["stance"], 75, 0, 74)
strip(pan, pan_acts["stance"], 150, 0, 10)
strip(pan, pan_acts["grab"], 161, 0, 34)
# win stand-in from STANDING stance frames (30..69): stance frame 0 is a deep
# crouch (hips -0.53), which read as a heap at the 196 cut in v1.
strip(pan, pan_acts["stance"], 196, 30, 69)
# Pantera approach: object location keys (from start toward Cape +Y)
y0 = pan.location.y
pan.location = (CX, y0, pan.location.z)
pan.keyframe_insert(data_path="location", frame=110)
pan.location = (CX, y0 + 0.60, pan.location.z)
pan.keyframe_insert(data_path="location", frame=135)
pan.location = (CX, y0 + 0.60, pan.location.z)
pan.keyframe_insert(data_path="location", frame=235)
# Cape follow offset during the grab: Pantera's grab root travels ~1m +Y and
# lifts to ~1.4m (measured), while Cape's launch clip stays near its start
# point; without this offset the two bodies separate mid-throw (v1 f_0175).
# Offsets are scene-level (armature location), documented choreography aids,
# not source-motion edits. Cape base location (before offsets):
cape_base = cape.location.copy()
cape.location = cape_base
cape.keyframe_insert(data_path="location", frame=169)
cape.location = (cape_base.x, cape_base.y + 0.30, cape_base.z + 0.25)
cape.keyframe_insert(data_path="location", frame=178)
cape.location = (cape_base.x, cape_base.y + 0.45, cape_base.z - 0.05)
cape.keyframe_insert(data_path="location", frame=186)
cape.location = (cape_base.x, cape_base.y + 0.45, cape_base.z - 0.05)
cape.keyframe_insert(data_path="location", frame=235)
# Neutral ground plane at arena ground level: the arena GLB is 140m wide, so
# at fight-camera distance its dressing falls outside the frame / reads as
# void in Workbench; the plane makes foot/ground contact legible without
# faking an arena backdrop (arena-composited beauty proof stays PENDING).
bpy.ops.mesh.primitive_plane_add(size=30, location=(CX, CY, GROUND_Z))
gp = bpy.context.active_object; gp.name = "proof_ground"
# camera: side view from +X
camd = bpy.data.cameras.new("proof_cam"); camd.lens = 35
cam = bpy.data.objects.new("proof_cam", camd); scn.collection.objects.link(cam)
cam.location = (CX + 4.5, CY, GROUND_Z + 1.6)
look = Vector((CX, CY, GROUND_Z + 1.0)); cam.rotation_euler = (look - cam.location).to_track_quat('-Z', 'Y').to_euler()
scn.camera = cam
scn.render.engine = 'BLENDER_WORKBENCH'
scn.display.shading.type = 'SOLID'; scn.display.shading.color_type = 'MATERIAL'; scn.display.shading.show_cavity = True
scn.render.resolution_x, scn.render.resolution_y = 640, 360
scn.render.image_settings.file_format = 'PNG'
frames = sorted(set([0, 60, 81, 135, 150, 161, 170, 176, 180, 185, 186, 196, 210, 235] + list(range(170, 196))))
for f in frames:
    scn.frame_set(f); scn.render.filepath = os.path.join(OUT, f"f_{f:04d}.png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED paired", f, flush=True)
print("PAIRED DONE")
