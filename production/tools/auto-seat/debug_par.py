"""Check deform bone parents."""
import bpy
rig = bpy.data.objects.get("CapeJones_Rig")
for name in ("pelvis", "spine_1", "thigh_L", "upperarm_L"):
    b = rig.data.bones.get(name)
    if b:
        par = b.parent.name if b.parent else None
        print(f"{name}: parent={par} deform={b.use_deform}", flush=True)
# check if there's a deform root
roots = [b.name for b in rig.data.bones if b.parent is None]
print(f"root bones: {roots}", flush=True)
print("DONE", flush=True)
