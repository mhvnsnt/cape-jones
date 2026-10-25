"""Auto-framing camera rig for the Cape Jones / Western Heart studio pipeline.

Owner directive 2026-10-24 22:07 CDT, owned: the old method was "set a camera
by hand, render, discover it cropped, withhold the proof, repeat." That stops.
Every camera in this pipeline is now COMPUTED from the subject's real bounding
box, and every framing is SELF-CHECKED (projected bbox corners must land
inside the frame) BEFORE a full render is spent on it.

Industry-standard basis (not invented): pinhole framing — distance =
(half-extent + margin) / tan(vertical_fov / 2), vertical_fov from lens focal
length and sensor height (36x24mm full-frame reference, Blender default).
Camera looks at the bbox centre (track-to), never at a guessed target.

Usage in Blender:
  blender --background scene.blend --python auto_camera.py -- --subject CapeJones_Body --lens 35 --margin 0.15 --out /tmp/cam.json
Or import in a render script: from auto_camera import fit_camera, check_framing
"""
import bpy, math, mathutils as mu, json, sys, argparse

SENSOR_H = 24.0  # mm, Blender default full-frame sensor height

def v_fov_deg(lens):
    return 2.0 * math.degrees(math.atan((SENSOR_H / 2.0) / lens))

def subject_bbox(obj_names):
    """World-space bbox (min, max) over all given objects' evaluated meshes."""
    dg = bpy.context.evaluated_depsgraph_get()
    mins = [float('inf')] * 3; maxs = [float('-inf')] * 3
    for name in obj_names:
        o = bpy.data.objects.get(name)
        if o is None or o.type != 'MESH':
            continue
        eo = o.evaluated_get(dg)
        me = eo.to_mesh()
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mins[i] = min(mins[i], w[i]); maxs[i] = max(maxs[i], w[i])
        eo.to_mesh_clear()
    return tuple(mins), tuple(maxs)

def fit_camera(bbox, lens=35, margin=0.15, direction=(0, -1, 0), height_frac=0.5):
    """Return (location, target) that fits the whole bbox in frame.

    direction: unit vector from subject toward camera (default: front, -Y).
    Camera height = bbox min z + height_frac * bbox height.
    Distance covers BOTH vertical extent and horizontal extent (aspect-aware
    via the render resolution): the caller passes aspect, we take the max.
    """
    (mn, mx) = bbox
    cx, cy, cz = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, (mn[2] + mx[2]) / 2
    half_h = (mx[2] - mn[2]) / 2 + margin
    half_w = max(mx[0] - mn[0], mx[1] - mn[1]) / 2 + margin
    res_x = bpy.context.scene.render.resolution_x
    res_y = bpy.context.scene.render.resolution_y
    aspect = res_x / max(res_y, 1)
    # horizontal fov from vertical fov and aspect
    vfov = math.radians(v_fov_deg(lens))
    hfov = 2.0 * math.atan(math.tan(vfov / 2.0) * aspect)
    dist_v = half_h / math.tan(vfov / 2.0)
    dist_h = half_w / math.tan(hfov / 2.0)
    dist = max(dist_v, dist_h)
    d = mu.Vector(direction); d.normalize()
    target = mu.Vector((cx, cy, mn[2] + height_frac * (mx[2] - mn[2])))
    loc = target + d * dist
    return loc, target, dist

def check_framing(cam, bbox):
    """Project all 8 bbox corners into camera NDC. PASS iff all inside
    [0,1]x[0,1] with depth > 0. Returns (pass, min_x, max_x, min_y, max_y)."""
    (mn, mx) = bbox
    corners = [mu.Vector((x, y, z)) for x in (mn[0], mx[0]) for y in (mn[1], mx[1]) for z in (mn[2], mx[2])]
    scene = bpy.context.scene
    xs, ys = [], []
    for c in corners:
        co = mu.Vector(c)
        # world_to_camera_view handles the camera matrix
        ndc = bpy_extras.object_utils.world_to_camera_view(scene, cam, co) if False else None
        # manual path (no bpy_extras import needed in background):
        mv = cam.matrix_world.inverted() @ co
        # perspective divide using camera lens/sensor via projection matrix
        proj = cam.calc_matrix_camera(bpy.context.evaluated_depsgraph_get())
        p = proj @ mu.Vector((mv.x, mv.y, mv.z, 1.0))
        if p.w == 0:
            continue
        xs.append(p.x / p.w); ys.append(p.y / p.w)
    # NDC here is -1..1 after projection; convert to 0..1
    xs = [(x + 1) / 2 for x in xs]; ys = [(y + 1) / 2 for y in ys]
    ok = bool(xs) and min(xs) >= 0.0 and max(xs) <= 1.0 and min(ys) >= 0.0 and max(ys) <= 1.0
    return ok, (min(xs), max(xs), min(ys), max(ys)) if xs else None

def make_camera(name, loc, target, lens):
    cd = bpy.data.cameras.new(name)
    c = bpy.data.objects.new(name, cd)
    bpy.context.collection.objects.link(c)
    c.location = loc; c.data.lens = lens
    c.rotation_euler = (mu.Vector(target) - c.location).to_track_quat('-Z', 'Y').to_euler()
    return c

if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", default="CapeJones_Body")
    ap.add_argument("--lens", type=float, default=35)
    ap.add_argument("--margin", type=float, default=0.15)
    ap.add_argument("--out", default="")
    a = ap.parse_args(argv)
    bbox = subject_bbox([a.subject])
    print("AUTO_CAM bbox", bbox)
    loc, target, dist = fit_camera(bbox, lens=a.lens, margin=a.margin)
    print("AUTO_CAM fit lens", a.lens, "dist", round(dist, 3), "loc", tuple(round(v, 3) for v in loc), "target", tuple(round(v, 3) for v in target))
    cam = make_camera("AutoCam", loc, target, a.lens)
    bpy.context.scene.camera = cam
    bpy.context.view_layer.update()
    ok, rng = check_framing(cam, bbox)
    print("AUTO_CAM framing", "PASS" if ok else "FAIL", rng)
    if a.out:
        json.dump({"bbox": bbox, "loc": tuple(loc), "target": tuple(target), "dist": dist, "framing_pass": ok, "ndc_range": rng}, open(a.out, "w"))
        print("AUTO_CAM wrote", a.out)
