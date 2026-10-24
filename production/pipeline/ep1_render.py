"""ep1_render.py — Episode 1 show-clip renderer with per-frame timing.

Renders a WH cast GLB playing a SHOW clip (anims/show/<char>/<clip>.glb)
inside Cape's living room (3d-assets/living_room.blend), one frame at a
time, so every frame gets an honest wall-clock timing and so frame ranges
can be split across machines/processes (the farm story: chunked ranges).

Derived from shared/cast/render_show_clip_in_room.py (the 2026-10-23
moving-proof script) with two changes, both documented:
  1. Per-frame loop instead of bpy.ops.render.render(animation=True), so
     timings.json records real seconds/frame and --start/--end chunks work.
  2. scene.render.fps = 30 is set BEFORE importing the clip GLB. The glTF
     importer maps clip times to frames at the *current* scene fps; the
     proof session's scratch variant found this matters (30 fps clip
     imported at the wrong fps plays fast).

Usage (headless, Blender 4.2+):
  blender -b 3d-assets/living_room.blend --python ep1_render.py -- \\
      <model.glb> <clip.glb> <rotate_y_deg> <out_dir> '[x,y,z]' \\
      --start 1 --end 6 --engine BLENDER_EEVEE_NEXT --preset eevee_preview \\
      --res 640 360

Presets (values match the repo's proven configs where they exist):
  eevee_preview — proof settings: TAA 24 (render_show_clip_in_room.py)
  eevee_show    — the living-room .blend's own beauty setting: TAA 64
  cycles_preview— proof's Cycles variant: 12 spp, denoising on
  cycles_show   — production/pipeline/cycles_speed_config.py "animation"
                  (16 spp, adaptive 0.05) + tools/scene-render
                  living_room bounces (diffuse 4, volume 2, step 2.0)
  cycles_hero   — cycles_speed_config "hero" (32 spp, adaptive 0.03) +
                  living_room_hero bounces (diffuse 5, volume 3, step 1.0)

Output: <out_dir>/f_%04d.png per frame + <out_dir>/timings.json
  [{"frame": n, "seconds": s, "engine": ..., "preset": ...,
    "res": "WxH", "samples": ...}, ...]
Show clips only (ANIM-GATE: SHOW context). Never saves the .blend.
Room lighting/colours untouched (canon violet LED wash).
"""
import bpy
import json
import math
import mathutils
import os
import sys
import time

PRESETS = {
    "eevee_preview": {"engine": "BLENDER_EEVEE_NEXT", "taa": 24},
    "eevee_show": {"engine": "BLENDER_EEVEE_NEXT", "taa": 64},
    "cycles_preview": {"engine": "CYCLES", "samples": 12,
                       "adaptive": False, "threshold": 0.0,
                       "diffuse": 2, "volume": 1, "step_rate": 1.0},
    "cycles_show": {"engine": "CYCLES", "samples": 16,
                    "adaptive": True, "threshold": 0.05,
                    "diffuse": 4, "volume": 2, "step_rate": 2.0},
    "cycles_hero": {"engine": "CYCLES", "samples": 32,
                    "adaptive": True, "threshold": 0.03,
                    "diffuse": 5, "volume": 3, "step_rate": 1.0},
}


def parse_args(argv):
    a = argv[argv.index("--") + 1:]
    pos = [x for x in a if not x.startswith("--")]
    kw = {}
    i = 0
    while i < len(a):
        if a[i].startswith("--") and i + 1 < len(a) and not a[i + 1].startswith("--"):
            kw[a[i][2:]] = a[i + 1]
            i += 2
        elif a[i].startswith("--"):
            kw[a[i][2:]] = True
            i += 1
        else:
            i += 1
    return pos, kw


def main():
    pos, kw = parse_args(sys.argv)
    model, clip, rot, out = pos[0], pos[1], float(pos[2]), pos[3]
    target = mathutils.Vector(json.loads(pos[4])) if len(pos) > 4 \
        else mathutils.Vector((1.2, 0.9, 0))
    preset_name = kw.get("preset", "eevee_preview")
    preset = PRESETS[preset_name]
    engine = kw.get("engine", preset["engine"])
    if "res" in kw and "x" in str(kw["res"]):
        res_x, res_y = map(int, str(kw["res"]).split("x"))
    else:
        res_x = int(kw.get("res_x", 640))
        res_y = int(kw.get("res_y", 360))

    sc = bpy.context.scene
    sc.render.fps = 30  # BEFORE clip import: glTF times -> frames at this fps

    def imp(p):
        b = set(bpy.data.objects)
        acts = set(bpy.data.actions)
        bpy.ops.import_scene.gltf(filepath=p)
        return ([o for o in bpy.data.objects if o not in b],
                [x for x in bpy.data.actions if x not in acts])

    new, _ = imp(model)
    arm = next(o for o in new if o.type == "ARMATURE")
    for o in new:
        if o.type == "MESH" and not (o.parent and o.parent.type == "ARMATURE"):
            o.hide_render = True
    # Hide the room's own rest-pose Cape figure, like the proof did.
    for _n in ("CapeJones_Rig", "CapeJones_Body", "CapeJones_Cape"):
        _o = bpy.data.objects.get(_n)
        if _o:
            _o.hide_viewport = True
            _o.hide_render = True
    cnew, cacts = imp(clip)
    act = cacts[0]
    bones = {b.name for b in arm.data.bones}
    paths = [fc.data_path for fc in act.fcurves]
    bound = sum(1 for p in paths
                if p.startswith('pose.bones["') and p.split('"')[1] in bones)
    for o in cnew:
        bpy.data.objects.remove(o, do_unlink=True)
    print("BINDING", json.dumps({"clip": clip, "action": act.name,
                                 "bound_fcurves": bound,
                                 "total_fcurves": len(paths)}), flush=True)
    if bound < 8:
        raise SystemExit("binding gate: <8 bound tracks")
    arm.animation_data_create()
    arm.animation_data.action = act

    f0, f1 = map(int, act.frame_range)
    start = int(kw.get("start", f0))
    end = int(kw.get("end", min(f1, start + 5)))
    step = int(kw.get("step", 1))

    roots = [o for o in new if o.parent is None]
    dg = bpy.context.evaluated_depsgraph_get()

    def bbox():
        dg.update()
        mn = mathutils.Vector((1e9,) * 3)
        mx = -mn
        for o in new:
            if o.type != "MESH" or o.hide_render:
                continue
            e = o.evaluated_get(dg)
            me = e.to_mesh()
            for v in me.vertices:
                w = e.matrix_world @ v.co
                mn = mathutils.Vector(map(min, mn, w))
                mx = mathutils.Vector(map(max, mx, w))
            e.to_mesh_clear()
        return mn, mx

    mn, mx = bbox()
    s = 1.8 / (mx.z - mn.z)
    for r in roots:
        r.scale = [v * s for v in r.scale]
        r.rotation_mode = "XYZ"
        r.rotation_euler.z += math.radians(rot)
    bpy.context.view_layer.update()
    mn, mx = bbox()
    c = (mn + mx) / 2
    for r in roots:
        r.location += mathutils.Vector(
            (target.x - c.x, target.y - c.y, target.z - mn.z))

    cam = bpy.data.objects.new("showProofCam", bpy.data.cameras.new("showProofCam"))
    sc.collection.objects.link(cam)
    look = target + mathutils.Vector((0, 0, 0.95))
    cam.location = look + mathutils.Vector((-0.6, -4.6, 0.25))
    cam.data.lens = 35
    cam.rotation_euler = (look - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam

    sc.render.engine = engine
    sc.render.resolution_x, sc.render.resolution_y = res_x, res_y
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    samples = None
    if engine == "CYCLES":
        c = sc.cycles
        c.device = "CPU"
        c.samples = preset["samples"]
        samples = preset["samples"]
        c.use_adaptive_sampling = preset["adaptive"]
        if preset["adaptive"]:
            c.adaptive_threshold = preset["threshold"]
            c.adaptive_min_samples = 8
        c.use_denoising = True
        c.denoiser = "OPENIMAGEDENOISE"
        c.denoising_input_passes = "RGB_ALBEDO_NORMAL"
        c.max_bounces = 8
        c.diffuse_bounces = preset["diffuse"]
        c.glossy_bounces = 3
        c.transmission_bounces = 2
        c.volume_bounces = preset["volume"]
        c.transparent_max_bounces = 8
        c.volume_step_rate = preset["step_rate"]
        c.volume_max_steps = 256
        c.caustics_reflective = False
        c.caustics_refractive = False
        sc.render.use_persistent_data = True
    else:
        sc.eevee.taa_render_samples = preset["taa"]
        samples = preset["taa"]

    print("EP1_RENDER", json.dumps({
        "engine": engine, "preset": preset_name, "samples": samples,
        "res": f"{res_x}x{res_y}", "frames": f"{start}-{end} step {step}",
        "model": os.path.basename(model), "clip": os.path.basename(clip)}),
        flush=True)

    os.makedirs(out, exist_ok=True)
    timings = []
    frame = start
    while frame <= end:
        sc.frame_set(frame)
        sc.render.filepath = os.path.join(out, f"f_{frame:04d}.png")
        t0 = time.perf_counter()
        bpy.ops.render.render(write_still=True)
        dt = time.perf_counter() - t0
        rec = {"frame": frame, "seconds": round(dt, 2), "engine": engine,
               "preset": preset_name, "res": f"{res_x}x{res_y}",
               "samples": samples}
        timings.append(rec)
        print("FRAME_TIME", json.dumps(rec), flush=True)
        # Persist after EVERY frame: a killed run still yields its timings.
        _tmp = os.path.join(out, "timings.json.tmp")
        with open(_tmp, "w") as f:
            json.dump(timings, f, indent=2)
        os.replace(_tmp, os.path.join(out, "timings.json"))
        frame += step
    if timings:
        avg = sum(t["seconds"] for t in timings) / len(timings)
        print(f"EP1_RENDER DONE frames={len(timings)} avg_s_per_frame={avg:.2f} "
              f"per_minute_s={avg * 1440:.0f} per_6min_h={avg * 8640 / 3600:.2f}",
              flush=True)


main()
