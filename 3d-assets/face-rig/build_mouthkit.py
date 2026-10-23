#!/usr/bin/env python3
"""
CJ Mouth Kit builder — Telltale-style interchangeable mouths + eye-dart cards.

Builds `cj_mouth_kit.blend` procedurally (Blender 4.0.2, headless via xvfb-run):
- 17 mouth meshes matched to characters/sheets/06-viseme-phoneme-mouth-matrix.jpg
  (resting, A/AH, E/I, O/OO, U, U-wide, M/B/P, E/I-smile, E/O, F, C/D/G/K/N/R/S/T/Y,
  teeth-clench, L/Th, W/Q, Sh/Ch, intense/clenched, gasp/surprise).
- White eye cards + pupil variants + closed lids per sheet 05
  (white eyes default; pupils sometimes-only for emphasis).
- Telltale swap-set: CJ_MouthDriver empty, int property `mouth_index`; drivers show
  exactly one mouth at a time (hide_viewport/hide_render = idx != mouth_index).
- All mouths/eyes parented under CJ_FaceSocket. The face lane parents the socket
  to the head bone and positions it on the face; this kit ships at a plausible
  default measured from the rig (jaw bone head ~(0,-0.068,0.845)).

All geometry is OURS, drawn from OUR sheets. No third-party art.

Usage:
    xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender \
        -b --python build_mouthkit.py -- ./cj_mouth_kit.blend
"""
import bpy
import math
import sys

# ----------------------------------------------------------------------------
# config
# ----------------------------------------------------------------------------
BASE_W = 0.17          # mouth base width (world units, ~ rig scale)
SOCKET_LOC = (0.0, 0.03, 0.80)   # default; face lane re-fits on the head

C_BLACK = (0.02, 0.02, 0.02, 1.0)
C_CAVITY = (0.23, 0.06, 0.06, 1.0)     # dark mouth interior
C_TEETH = (1.0, 1.0, 1.0, 1.0)
C_TONGUE = (0.72, 0.25, 0.32, 1.0)
C_EYEWHITE = (1.0, 1.0, 1.0, 1.0)

# name, style, params. styles: line | open | pucker | f | lth
MOUTHS = [
    ("00_resting",    "line",   dict(w=0.55, h=0.055)),
    ("01_A_AH",       "open",   dict(w=0.60, h=0.50, teeth_u=False, teeth_l=False, tongue=True)),
    ("02_E_I",        "open",   dict(w=0.80, h=0.30, teeth_u=True,  teeth_l=False, tongue=False)),
    ("03_O_OO",       "pucker", dict(r=0.30)),
    ("04_U",          "pucker", dict(r=0.24)),
    ("05_U_wide",     "open",   dict(w=0.60, h=0.78, teeth_u=True,  teeth_l=True,  tongue=True)),
    ("06_M_B_P",      "line",   dict(w=0.55, h=0.045)),
    ("07_E_I_smile",  "open",   dict(w=0.90, h=0.36, teeth_u=True,  teeth_l=True,  tongue=False)),
    ("08_E_O",        "open",   dict(w=0.72, h=0.28, teeth_u=True,  teeth_l=True,  tongue=False)),
    ("09_F",          "f",      dict(w=0.62, h=0.16)),
    ("10_CDGKNRSTY",  "line",   dict(w=0.55, h=0.085)),
    ("11_teeth_clench","open",  dict(w=0.72, h=0.17, teeth_u=True,  teeth_l=True,  tongue=False)),
    ("12_L_Th",       "lth",    dict(w=0.60, h=0.22)),
    ("13_W_Q",        "pucker", dict(r=0.20)),
    ("14_Sh_Ch",      "open",   dict(w=0.45, h=0.26, teeth_u=False, teeth_l=False, tongue=False)),
    ("15_intense",    "open",   dict(w=0.78, h=0.13, teeth_u=True,  teeth_l=True,  tongue=False)),
    ("16_gasp",       "open",   dict(w=0.50, h=0.72, teeth_u=True,  teeth_l=False, tongue=True)),
]

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def wipe():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.materials):
        for x in list(coll):
            coll.remove(x)


def make_mat(name, color):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = 0.9
    return m


def ellipse_obj(name, rx, rz, mat, loc=(0, 0, 0), segs=28):
    """Flat filled ellipse curve (XY plane -> rotated to face +Y)."""
    cu = bpy.data.curves.new(name + "_cu", type='CURVE')
    cu.dimensions = '2D'
    cu.fill_mode = 'BOTH'
    sp = cu.splines.new('BEZIER')
    pts = sp.bezier_points
    pts.add(segs - 1)
    k = 0.5522847498  # circle -> bezier handle factor
    for i in range(segs):
        a = 2.0 * math.pi * i / segs
        x, y = rx * math.cos(a), rz * math.sin(a)
        tx, ty = -rx * math.sin(a), rz * math.cos(a)
        p = pts[i]
        p.co = (x, y, 0)
        p.handle_left = (x - tx * k, y - ty * k, 0)
        p.handle_right = (x + tx * k, y + ty * k, 0)
        p.handle_left_type = p.handle_right_type = 'FREE'
    sp.use_cyclic_u = True
    ob = bpy.data.objects.new(name, cu)
    ob.data.materials.append(mat)
    ob.rotation_euler = (math.pi / 2, 0, 0)  # curve XY -> world XZ, faces +Y
    ob.location = loc
    bpy.context.scene.collection.objects.link(ob)
    return ob


def ring_obj(name, r, tube, mat, loc=(0, 0, 0)):
    """Puckered-lip ring: curve circle with bevel (tube)."""
    ob = ellipse_obj(name, r, r, mat, loc=loc)
    ob.data.bevel_depth = tube
    ob.data.bevel_resolution = 2
    ob.data.fill_mode = 'BOTH'
    return ob


def build_mouth(name, style, p, mats):
    holder = bpy.data.objects.new("CJ_Mouth_" + name, None)
    bpy.context.scene.collection.objects.link(holder)
    parts = []

    def add(ob):
        ob.parent = holder
        parts.append(ob)
        return ob

    W = BASE_W
    if style == "line":
        w, h = W * p["w"], W * p["h"]
        add(ellipse_obj("outline", w * 0.62, h * 0.62 + 0.004, mats["black"], loc=(0, -0.002, 0)))
        add(ellipse_obj("line", w * 0.5, h * 0.5, mats["cavity"], loc=(0, 0, 0)))
    elif style == "open":
        w, h = W * p["w"], W * p["h"]
        add(ellipse_obj("outline", w * 0.62, h * 0.62 + 0.004, mats["black"], loc=(0, -0.002, 0)))
        add(ellipse_obj("cavity", w * 0.5, h * 0.5, mats["cavity"], loc=(0, 0, 0)))
        if p.get("tongue"):
            add(ellipse_obj("tongue", w * 0.30, h * 0.16, mats["tongue"], loc=(0, 0.0012, -h * 0.26)))
        if p.get("teeth_u"):
            add(ellipse_obj("teeth_u", w * 0.44, min(h * 0.20, 0.016), mats["teeth"], loc=(0, 0.0018, h * 0.30)))
        if p.get("teeth_l"):
            add(ellipse_obj("teeth_l", w * 0.40, min(h * 0.16, 0.012), mats["teeth"], loc=(0, 0.0018, -h * 0.32)))
    elif style == "pucker":
        r = W * p["r"]
        add(ring_obj("lips", r, 0.007, mats["black"], loc=(0, -0.001, 0)))
        add(ellipse_obj("cavity", r * 0.62, r * 0.62, mats["cavity"], loc=(0, 0.001, 0)))
    elif style == "f":
        w, h = W * p["w"], W * p["h"]
        add(ellipse_obj("outline", w * 0.62, h * 0.62 + 0.004, mats["black"], loc=(0, -0.002, 0)))
        # upper teeth bite over the lower lip line
        add(ellipse_obj("teeth", w * 0.46, 0.014, mats["teeth"], loc=(0, 0.0018, h * 0.18)))
        add(ellipse_obj("line", w * 0.5, 0.006, mats["cavity"], loc=(0, 0.001, -h * 0.28)))
    elif style == "lth":
        w, h = W * p["w"], W * p["h"]
        add(ellipse_obj("outline", w * 0.62, h * 0.62 + 0.004, mats["black"], loc=(0, -0.002, 0)))
        add(ellipse_obj("cavity", w * 0.5, h * 0.5, mats["cavity"], loc=(0, 0, 0)))
        add(ellipse_obj("teeth_u", w * 0.44, 0.013, mats["teeth"], loc=(0, 0.0018, h * 0.28)))
        # tongue tip pokes out between teeth
        add(ellipse_obj("tongue", w * 0.20, 0.010, mats["tongue"], loc=(0, 0.0028, -h * 0.05)))
    return holder


def build_eyes(mats):
    holder = bpy.data.objects.new("CJ_Eyes", None)
    bpy.context.scene.collection.objects.link(holder)
    eye_w, eye_h = 0.058, 0.030
    eye_z, eye_y, eye_x = 0.105, 0.035, 0.088

    def white_side(sx, tag):
        parts = []
        g = bpy.data.objects.new(tag, None)
        bpy.context.scene.collection.objects.link(g)
        g.parent = holder
        o = ellipse_obj("white", eye_w * 0.62, eye_h * 0.62 + 0.003, mats["black"],
                        loc=(sx * eye_x, eye_y - 0.002, eye_z))
        o.parent = g
        w = ellipse_obj("white_in", eye_w * 0.5, eye_h * 0.5, mats["eye"],
                        loc=(sx * eye_x, eye_y, eye_z))
        w.parent = g
        p = ellipse_obj("pupil", 0.016, 0.020, mats["black"],
                        loc=(sx * eye_x, eye_y + 0.004, eye_z))
        p.parent = g
        return g, p

    gl, pl = white_side(-1, "CJ_Eye_L")
    gr, pr = white_side(1, "CJ_Eye_R")
    # closed lids (lash lines)
    cl = bpy.data.objects.new("CJ_Eye_Closed", None)
    bpy.context.scene.collection.objects.link(cl)
    cl.parent = holder
    for sx in (-1, 1):
        l = ellipse_obj("lash", eye_w * 0.55, 0.006, mats["black"],
                        loc=(sx * eye_x, eye_y + 0.002, eye_z - 0.004))
        l.parent = cl
    return holder, [pl, pr], cl


def add_hide_driver(obj, driver_id, prop, index):
    for dp in ("hide_viewport", "hide_render"):
        d = obj.driver_add(dp).driver
        d.type = 'SCRIPTED'
        v = d.variables.new()
        v.name = "idx"
        v.type = 'SINGLE_PROP'
        v.targets[0].id = driver_id
        v.targets[0].data_path = '["%s"]' % prop
        d.expression = "idx != %d" % index


def int_prop(ob, name, default, minv, maxv, desc):
    ob[name] = default
    ui = ob.id_properties_ui(name)
    ui.update(min=minv, max=maxv, description=desc)


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------
def main():
    argv = sys.argv
    out = argv[argv.index("--") + 1] if "--" in argv else "./cj_mouth_kit.blend"

    wipe()
    mats = {
        "black": make_mat("CJ_Mouth_Black", C_BLACK),
        "cavity": make_mat("CJ_Mouth_Cavity", C_CAVITY),
        "teeth": make_mat("CJ_Mouth_Teeth", C_TEETH),
        "tongue": make_mat("CJ_Mouth_Tongue", C_TONGUE),
        "eye": make_mat("CJ_Eye_White", C_EYEWHITE),
    }

    socket = bpy.data.objects.new("CJ_FaceSocket", None)
    socket.location = SOCKET_LOC
    bpy.context.scene.collection.objects.link(socket)

    driver = bpy.data.objects.new("CJ_MouthDriver", None)
    bpy.context.scene.collection.objects.link(driver)
    driver.parent = socket
    int_prop(driver, "mouth_index", 0, 0, len(MOUTHS) - 1,
             "Telltale swap-set: which mouth is visible (see rhubarb_map.json)")

    for i, (name, style, p) in enumerate(MOUTHS):
        holder = build_mouth(name, style, p, mats)
        holder.parent = socket
        add_hide_driver(holder, driver, "mouth_index", i)
    eye_driver = bpy.data.objects.new("CJ_EyeDriver", None)
    bpy.context.scene.collection.objects.link(eye_driver)
    eye_driver.parent = socket
    int_prop(eye_driver, "eye_index", 0, 0, 2,
             "0=white only (default, sheet 05), 1=white+pupils (emphasis), 2=closed")
    eyes, pupils, closed = build_eyes(mats)
    eyes.parent = socket
    # eye visibility: white groups show on 0 and 1; pupils only on 1; closed only on 2
    for child in list(eyes.children):
        if child is closed:
            for dp in ("hide_viewport", "hide_render"):
                d = child.driver_add(dp).driver
                d.type = 'SCRIPTED'
                v = d.variables.new(); v.name = "idx"; v.type = 'SINGLE_PROP'
                v.targets[0].id = eye_driver; v.targets[0].data_path = '["eye_index"]'
                d.expression = "idx != 2"
        else:
            # white eye groups: visible on 0 and 1
            for dp in ("hide_viewport", "hide_render"):
                d = child.driver_add(dp).driver
                d.type = 'SCRIPTED'
                v = d.variables.new(); v.name = "idx"; v.type = 'SINGLE_PROP'
                v.targets[0].id = eye_driver; v.targets[0].data_path = '["eye_index"]'
                d.expression = "idx == 2"
            # pupils: only on 1
            for p in child.children:
                if "pupil" in p.name:
                    for dp in ("hide_viewport", "hide_render"):
                        d = p.driver_add(dp).driver
                        d.type = 'SCRIPTED'
                        v = d.variables.new(); v.name = "idx"; v.type = 'SINGLE_PROP'
                        v.targets[0].id = eye_driver; v.targets[0].data_path = '["eye_index"]'
                        d.expression = "idx != 1"

    bpy.ops.wm.save_as_mainfile(filepath=out)
    print("SAVED", out, "| mouths:", len(MOUTHS))


if __name__ == "__main__":
    main()
