"""Living-room proof renders (Workbench): Cape seated + channel-flip, and portal flight.
Uses the ROOM GLB (stages/cape-house/living-room.glb -- the authoritative stage;
SIT-TARGETS.md describes it). The living_room.blend is NOT used: its built-in
Cape body does not follow a posed rig (evaluated bbox stays at origin) and its
Recliner collection is empty, so proofs against it render no character.
Imports the Cape model GLB and uses the IMPORTED rig/body (fresh armature),
seats Cape at the recliner via iterative pelvis-head placement
(target = butt_target + lift), renders checkframes.
"""
import bpy, os, sys
from mathutils import Vector
MODE = sys.argv[sys.argv.index("--") + 1]  # 'flip' or 'flight'
OUT = f"/home/hatch/workspace/ep1-fight-anim/proof/room2_{MODE}"
os.makedirs(OUT, exist_ok=True)
scn = bpy.context.scene
scn.render.fps = 30
# room GLB
bpy.ops.import_scene.gltf(filepath="/home/hatch/workspace/scratch/cj-3d/repo/stages/cape-house/living-room.glb")
for o in bpy.data.objects:
    if o.type == 'MESH' and any(k in o.name.lower() for k in ('chair', 'recliner', 'lounge')):
        mw = o.matrix_world
        vs = [mw @ v.co for v in o.data.vertices]
        xs=[v.x for v in vs]; ys=[v.y for v in vs]; zs=[v.z for v in vs]
        print(f"ROOM CHAIR {o.name} bbox x[{min(xs):.2f},{max(xs):.2f}] y[{min(ys):.2f},{max(ys):.2f}] z[{min(zs):.2f},{max(zs):.2f}]")
# cape model (use the IMPORTED armature, not any pre-existing one)
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath="/home/hatch/workspace/scratch/cj-3d/cape-jones-show.glb")
rig = next(o for o in bpy.data.objects if o.type == 'ARMATURE' and o not in before)
print("USING imported rig:", rig.name)
CLIP = {"flip": "/home/hatch/workspace/ep1-fight-anim/clips/cape/ep1_cape_channel_flip.glb",
        "flight": "/home/hatch/workspace/ep1-fight-anim/clips/cape/ep1_cape_portal_flight.glb"}[MODE]
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=CLIP)
clip_arm = next(o for o in bpy.data.objects if o.type == 'ARMATURE' and o not in before)
act = clip_arm.animation_data.action
bpy.data.objects.remove(clip_arm, do_unlink=True)
if not rig.animation_data: rig.animation_data_create()
rig.animation_data.action = act
rig.rotation_mode = 'XYZ'
rig.rotation_euler = (0, 0, -1.5708)  # Rz(-90): clip -Y -> room -X (faces TV)
TARGET = Vector((3.120, 2.067, 0.42))
rig.location = (3.0, 2.067, 0)
for _ in range(3):
    scn.frame_set(0); bpy.context.view_layer.update()
    pb = rig.pose.bones['pelvis']
    head_w = rig.matrix_world @ (pb.matrix @ Vector(pb.bone.head_local))
    rig.location += TARGET - head_w
    print(f"SEAT adjust: head was {tuple(round(v,3) for v in head_w)} loc now {tuple(round(v,3) for v in rig.location)}")
if MODE == 'flight':
    for o in bpy.data.objects:
        if o.name == 'TV_Glow' and hasattr(o.data, 'energy'):
            print("TV_GLOW base energy:", o.data.energy); o.data.energy *= 4.0
camd = bpy.data.cameras.new("proof_cam"); camd.lens = 35
cam = bpy.data.objects.new("proof_cam", camd); scn.collection.objects.link(cam)
if MODE == 'flip':
    # South profile view: the low front camera's sightline is blocked by the
    # coffee table (legs occluded, "floating torso" misread in v1). From the
    # south, the seated figure + pointing arm + legs are all visible.
    cam.location = (2.6, 0.6, 1.4)
    look = Vector((3.12, 2.067, 0.55))
    FRAMES = [0, 20, 45, 120]
else:
    cam.location = (1.5, -0.8, 1.9)
    look = Vector((1.5, 2.067, 0.9))
    FRAMES = [0, 25, 60, 95, 115]
cam.rotation_euler = (look - cam.location).to_track_quat('-Z', 'Z').to_euler()
bpy.context.view_layer.update()
scn.camera = cam
scn.render.engine = 'BLENDER_WORKBENCH'
scn.display.shading.type = 'SOLID'; scn.display.shading.color_type = 'MATERIAL'; scn.display.shading.show_cavity = True
scn.render.resolution_x, scn.render.resolution_y = 640, 360
scn.render.image_settings.file_format = 'PNG'
for f in FRAMES:
    scn.frame_set(f); scn.render.filepath = os.path.join(OUT, f"f_{f:04d}.png")
    bpy.ops.render.render(write_still=True)
    print("RENDERED room2", MODE, f, flush=True)
print("ROOM2 DONE", MODE)
