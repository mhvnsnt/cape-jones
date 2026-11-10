"""Debug: where are the chair and character, and are they render-visible?"""
import bpy
scn = bpy.context.scene
for name in ("recliner_base", "recliner_backrest", "CapeJones_Body", "CapeJones_Rig",
             "CapeJones_Cape", "BodyProxy", "Floor"):
    o = bpy.data.objects.get(name)
    if o is None:
        print(f"{name}: MISSING"); continue
    print(f"{name}: loc=({o.location.x:.2f},{o.location.y:.2f},{o.location.z:.2f}) "
          f"hide_viewport={o.hide_viewport} hide_render={o.hide_render} "
          f"hide_get={o.hide_get()}")
# all mesh objects near the seat location
print("--- objects within 2m of (3.05,2.067,0.5):")
for o in bpy.data.objects:
    if o.type == 'MESH':
        d = ((o.location.x-3.05)**2 + (o.location.y-2.067)**2 + (o.location.z-0.5)**2) ** 0.5
        if d < 2.0:
            print(f"  {o.name}: loc=({o.location.x:.2f},{o.location.y:.2f},{o.location.z:.2f}) hr={o.hide_render}")
print("DONE")
