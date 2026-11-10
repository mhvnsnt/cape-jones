"""Check ray visibility."""
import bpy
body = bpy.data.objects.get("CapeJones_Body")
vis = body.visible_camera if hasattr(body, 'visible_camera') else 'N/A'
print(f"visible_camera attr: {vis}", flush=True)
# Cycles visibility is on the object
print(f"hide_render={body.hide_render}", flush=True)
# check cycles settings
c = body.cycles if hasattr(body, 'cycles') else None
if c:
    print(f"cycles.is_holdout={c.is_holdout}", flush=True)
print("DONE", flush=True)
