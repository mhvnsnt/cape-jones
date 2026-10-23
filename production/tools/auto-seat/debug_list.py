"""List all body-like objects and their locations."""
import bpy
for o in bpy.data.objects:
    if 'body' in o.name.lower() or 'capejones' in o.name.lower():
        print(f"{o.name}: type={o.type} loc=({o.location.x:.2f},{o.location.y:.2f},{o.location.z:.2f}) hr={o.hide_render}", flush=True)
print("DONE", flush=True)
