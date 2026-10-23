"""Inspect armature modifier settings."""
import bpy
body = bpy.data.objects.get("CapeJones_Body")
for m in body.modifiers:
    if m.type == 'ARMATURE':
        print(f"Armature: object={m.object.name if m.object else None}", flush=True)
        print(f"  use_vertex_groups={m.use_vertex_groups}", flush=True)
        print(f"  use_bone_envelopes={m.use_bone_envelopes}", flush=True)
        print(f"  use_deform_preserve_volume={m.use_deform_preserve_volume}", flush=True)
    if m.type == 'CORRECTIVE_SMOOTH':
        print(f"CorrectiveSmooth: factor={m.factor} iterations={m.iterations}", flush=True)
        print(f"  use_pin_boundary={m.use_pin_boundary}", flush=True)
print("DONE", flush=True)
