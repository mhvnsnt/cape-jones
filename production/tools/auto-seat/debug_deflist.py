"""Write full deform bone list to file."""
import bpy
rig = bpy.data.objects.get("CapeJones_Rig")
deform = sorted([b.name for b in rig.data.bones if b.use_deform])
with open("/tmp/deform_bones.txt", "w") as f:
    f.write(f"Total: {len(deform)}\n")
    for name in deform:
        f.write(name + "\n")
print("WROTE", flush=True)
