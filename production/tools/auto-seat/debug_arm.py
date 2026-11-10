"""Check armature modifier and bone hierarchy."""
import bpy
body = bpy.data.objects.get("CapeJones_Body")
rig = bpy.data.objects.get("CapeJones_Rig")
print("Body modifiers:", flush=True)
for m in body.modifiers:
    print(f"  {m.type}: {m.name} -> {m.object.name if hasattr(m,'object') and m.object else None}", flush=True)
print("Rig root bones:", flush=True)
for b in rig.data.bones:
    if b.parent is None:
        print(f"  {b.name}", flush=True)
pelvis = rig.data.bones.get("pelvis")
if pelvis:
    chain = []
    b = pelvis
    while b:
        chain.append(b.name)
        b = b.parent
    print(f"pelvis chain: {' -> '.join(chain)}", flush=True)
print("DONE", flush=True)
