"""Check bone deform flags."""
import bpy
rig = bpy.data.objects.get("CapeJones_Rig")
for name in ("root", "pelvis", "thigh_fk_L", "spine_fk_1"):
    b = rig.data.bones.get(name)
    if b:
        print(f"{name}: use_deform={b.use_deform} inherit_scale={b.inherit_scale}", flush=True)
print("DONE", flush=True)
