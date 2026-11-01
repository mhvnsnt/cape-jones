"""Blender fast path: EEVEE, 1 sample, 550x375, 48 frames, timed.
Reuses the existing .blend scene by opening it and changing render settings.
Own code, no Toon Boom code."""
import bpy, time, os, json
OUT="/home/hatch/workspace/cape-jones-rig/wire-up-cannot-do-20261101/renders/blender_fast"
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cape-jones-rig/blender523-toon-20261101/cape_jones_toon_blender523.blend")
s=bpy.context.scene
s.render.engine='BLENDER_EEVEE'
try: s.eevee.taa_render_samples=1
except Exception as e: print("eevee samples set failed", e)
s.render.resolution_x=550; s.render.resolution_y=375
s.frame_start=1; s.frame_end=48; s.render.fps=24
s.render.image_settings.file_format='PNG'
s.render.filepath=os.path.join(OUT,"frame_")
t0=time.time()
bpy.ops.render.render(animation=True)
t1=time.time()
n=len([f for f in os.listdir(OUT) if f.endswith(".png")])
print("BLENDER_FAST_DONE", json.dumps({"frames":n,"total_s":round(t1-t0,2),"per_frame_s":round((t1-t0)/max(n,1),3)}))
