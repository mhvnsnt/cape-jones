"""Find deform bones (use_deform=True)."""
import bpy
rig = bpy.data.objects.get("CapeJones_Rig")
deform = [b.name for b in rig.data.bones if b.use_deform]
print(f"Total bones: {len(rig.data.bones)}, Deform bones: {len(deform)}", flush=True)
# group by prefix
for name in sorted(deform)[:40]:
    print(f"  {name}", flush=True)
print("DONE", flush=True)
