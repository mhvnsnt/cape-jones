"""Check occluders between camera and character."""
import bpy
for name in ("shelf", "Shelf", "bookcase"):
    for o in bpy.data.objects:
        if name.lower() in o.name.lower():
            print(f"{o.name}: loc=({o.location.x:.2f},{o.location.y:.2f},{o.location.z:.2f})", flush=True)
# camera at (1.35,2.067,0.85), char at (3.06,1.97,0.52)
# check what's at x~2-3, y~2
for o in bpy.data.objects:
    if o.type == 'MESH' and 2.0 < o.location.x < 3.5 and 1.5 < o.location.y < 2.5:
        print(f"  {o.name}: ({o.location.x:.2f},{o.location.y:.2f},{o.location.z:.2f})", flush=True)
print("DONE", flush=True)
