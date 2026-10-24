
import bpy, time, resource, os
import numpy as np
SRC = "/kaggle/input/datasets/marsfmmg/cape-bake-scene-20261023/bake_scene.blend"
OUT = "/kaggle/working/scene_capebaked.blend"
print("BAKE opening", SRC, flush=True)
bpy.ops.wm.open_mainfile(filepath=SRC)
sc = bpy.context.scene
cape = bpy.data.objects["CapeJones_Cape"]
cloth = [m for m in cape.modifiers if m.type == 'CLOTH'][0]
cloth.settings.quality = 8
cloth.settings.bending_stiffness = 1.2
cloth.collision_settings.use_self_collision = False
cloth.collision_settings.collision_quality = 2
pc = cloth.point_cache
sc.frame_start, sc.frame_end = 1, 81
pc.frame_start, pc.frame_end = 1, 81
pc.use_disk_cache = False
print(f"BAKE cloth verts={len(cape.data.vertices)} quality={cloth.settings.quality} selfcol={cloth.collision_settings.use_self_collision}", flush=True)
bpy.ops.ptcache.free_bake_all()
t0 = time.time()
bpy.ops.ptcache.bake_all(bake=True)
dt = time.time() - t0
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6
print(f"BAKE 81 frames: {dt:.1f}s ({dt/81:.1f}s/frame) peakRSS={peak:.2f}GB is_baked={pc.is_baked}", flush=True)
assert pc.is_baked, "bake incomplete"
def cape_stats(f):
    sc.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = cape.evaluated_get(dg)
    me = ev.to_mesh()
    arr = np.empty(len(me.vertices) * 3, dtype=np.float64)
    me.vertices.foreach_get("co", arr)
    ev.to_mesh_clear()
    arr = arr.reshape(-1, 3)
    return arr.min(axis=0), arr.max(axis=0), arr.mean(axis=0), bool(np.isnan(arr).any())
for f in (1, 40, 81):
    mn, mx, mean, nan = cape_stats(f)
    print(f"BAKE frame{f}: min={mn.round(3).tolist()} max={mx.round(3).tolist()} mean={mean.round(3).tolist()} NaN={nan}", flush=True)
    assert not nan, f"NaN in cape at frame {f}"
sc.frame_set(40)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print(f"SAVED {OUT} size={os.path.getsize(OUT)}", flush=True)
print("BAKE DONE", flush=True)
