"""Cape Jones — Blaster VFX geometry-nodes build.

Reference implementation for docs/blaster/BLASTER-VFX-SPEC.md.
Builds headless: the CJ_BlasterFX geometry-node group, canon materials
(white core #FFFFFF / #FFB300 glow / cyan arcs), a driver empty with
charge/fire/recoil custom props, a dummy gauntlet for proof renders,
and saves 3d-assets/blaster-vfx/blaster_fx.blend.

Palette comes from blaster_palette.json (single source of truth).

Run headless:
    xvfb-run -a env -u PYTHONPATH <blender> -b --python build_blasterfx.py -- <out.blend>

Canon sources: characters/sheets/03-color-lighting-vfx-key.jpg,
characters/sheets/04-action-flight-vfx-reference.jpg.
Palette locked 2026-10-17 ~10:24 CDT: blaster core #FFFFFF, outer glow #FFB300.
Rim refinement 2026-10-17 ~10:35: rim is situational/motivated — NOT part of this FX.
Blaster lighting concept 2026-10-17 ~10:36: the blast's light becomes the scene lighting.
"""
import bpy
import json
import math
import sys
import os

# ---------------------------------------------------------------- palette
PALETTE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "blaster_palette.json")
with open(PALETTE_PATH) as _pf:
    _PAL = json.load(_pf)

CORE_WHITE = tuple(_PAL["core_blast"]["rgba"])
GLOW_AMBER = tuple(_PAL["outer_glow"]["rgba"])
ARC_CYAN = tuple(_PAL["arc_cyan"]["rgba"])
CUFF_WHITE = tuple(_PAL["cuff_white"]["rgba"])
CORE_STRENGTH = _PAL["core_blast"]["emission_strength"]
GLOW_STRENGTH = _PAL["outer_glow"]["emission_strength"]
ARC_STRENGTH = _PAL["arc_cyan"]["emission_strength"]

OUT_BLEND = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "/tmp/blaster_fx.blend"


def wipe():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_emission_material(name, color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        mat.node_tree.nodes.remove(bsdf)
    out = mat.node_tree.nodes.get("Material Output")
    em = mat.node_tree.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = color
    em.inputs["Strength"].default_value = strength
    mat.node_tree.links.new(em.outputs["Emission"], out.inputs["Surface"])
    return mat


def add_group_socket(group, name, socket_type, default=None, min_v=None, max_v=None):
    """Blender 4.0+: use the new interface API, fall back to the old one."""
    if hasattr(group, "interface"):
        sock = group.interface.new_socket(name=name, socket_type=socket_type, in_out="INPUT")
        if default is not None:
            sock.default_value = default
        if min_v is not None:
            sock.min_value = min_v
        if max_v is not None:
            sock.max_value = max_v
        return sock
    sock = group.inputs.new(socket_type, name)
    if default is not None:
        sock.default_value = default
    return sock


def build_blaster_group():
    group = bpy.data.node_groups.new("CJ_BlasterFX", "GeometryNodeTree")

    add_group_socket(group, "Charge", "NodeSocketFloat", default=0.0, min_v=0.0, max_v=1.0)
    add_group_socket(group, "Fire", "NodeSocketFloat", default=0.0, min_v=0.0, max_v=1.0)
    add_group_socket(group, "Seed", "NodeSocketInt", default=0)
    add_group_socket(group, "BeamLength", "NodeSocketFloat", default=6.0, min_v=0.5, max_v=20.0)
    if hasattr(group, "interface"):
        out_sock = group.interface.new_socket(name="Geometry", socket_type="NodeSocketGeometry", in_out="OUTPUT")
    else:
        group.outputs.new("NodeSocketGeometry", "Geometry")

    nodes = group.nodes
    links = group.links
    gin = nodes.new("NodeGroupInput")
    gin.location = (-900, 0)
    gout = nodes.new("NodeGroupOutput")
    gout.location = (900, 0)
    time = nodes.new("GeometryNodeInputSceneTime")
    time.location = (-900, -300)

    def torus(ring_i, major, minor):
        # Blender 4.0 has no torus primitive (4.1+): curve circle -> curve-to-mesh
        c = nodes.new("GeometryNodeCurvePrimitiveCircle")
        c.location = (-820, 420 - ring_i * 260)
        c.inputs["Resolution"].default_value = 64
        c.inputs["Radius"].default_value = major
        p = nodes.new("GeometryNodeCurvePrimitiveCircle")
        p.location = (-820, 280 - ring_i * 260)
        p.inputs["Resolution"].default_value = 12
        p.inputs["Radius"].default_value = minor
        ctm = nodes.new("GeometryNodeCurveToMesh")
        ctm.location = (-640, 420 - ring_i * 260)
        links.new(c.outputs["Curve"], ctm.inputs["Curve"])
        links.new(p.outputs["Curve"], ctm.inputs["Profile Curve"])
        ctm.inputs["Fill Caps"].default_value = True
        return ctm

    def mnode(op, a=None, b=None, loc=(0, 0)):
        m = nodes.new("ShaderNodeMath")
        m.operation = op
        m.location = loc
        if a is not None:
            m.inputs[0].default_value = a
        if b is not None:
            m.inputs[1].default_value = b
        return m

    def transform(geo_node, translation=None, rotation=None, scale=None, loc=(0, 0)):
        tr = nodes.new("GeometryNodeTransform")
        tr.location = loc
        links.new(geo_node.outputs["Mesh"], tr.inputs["Geometry"])
        if translation is not None:
            tr.inputs["Translation"].default_value = translation
        if rotation is not None:
            tr.inputs["Rotation"].default_value = rotation
        if scale is not None:
            if isinstance(scale, (int, float)):
                tr.inputs["Scale"].default_value = (scale, scale, scale)
            else:
                tr.inputs["Scale"].default_value = scale
        return tr

    # ---- charge rings: 3 tori around the gauntlet axis (X axis here) ----
    # pulse = 1 + 0.15 * sin(time * 12)
    sin_t = mnode("SINE", loc=(-700, -500))
    links.new(time.outputs["Seconds"], sin_t.inputs[0])
    freq = mnode("MULTIPLY", b=12.0, loc=(-850, -500))
    links.new(time.outputs["Seconds"], freq.inputs[0])
    links.new(freq.outputs["Value"], sin_t.inputs[0])
    pulse = mnode("MULTIPLY_ADD", b=0.15, loc=(-550, -500))
    links.new(sin_t.outputs["Value"], pulse.inputs[0])
    pulse.inputs[2].default_value = 1.0

    charge_scale = mnode("MULTIPLY", loc=(-400, -200))
    links.new(gin.outputs["Charge"], charge_scale.inputs[0])
    links.new(pulse.outputs["Value"], charge_scale.inputs[1])

    ring_geos = []
    for i, (major, minor) in enumerate([(0.55, 0.06), (0.75, 0.045), (0.95, 0.035)]):
        t = torus(i, major, minor)
        # orient torus around X axis (gauntlet axis)
        tr = transform(t, rotation=(0, math.pi / 2, 0), loc=(-500, 420 - i * 260))
        sc = mnode("MULTIPLY", b=1.0, loc=(-300, 420 - i * 260))
        links.new(charge_scale.outputs["Value"], sc.inputs[0])
        vec = nodes.new("ShaderNodeCombineXYZ")
        vec.location = (-150, 420 - i * 260)
        links.new(sc.outputs["Value"], vec.inputs["X"])
        links.new(sc.outputs["Value"], vec.inputs["Y"])
        links.new(sc.outputs["Value"], vec.inputs["Z"])
        tr2 = nodes.new("GeometryNodeTransform")
        tr2.location = (0, 420 - i * 260)
        links.new(tr.outputs["Geometry"], tr2.inputs["Geometry"])
        links.new(vec.outputs["Vector"], tr2.inputs["Scale"])
        ring_geos.append(tr2)

    # ---- shared: per-vertex random jitter (4.0 GN has no texture nodes;
    # per-vertex Random Value gives the jagged starburst / zigzag look) ----
    def jitter(ico_node, amt, seed_off, loc):
        pos = nodes.new("GeometryNodeInputPosition")
        pos.location = (loc[0] - 300, loc[1] + 60)
        rv = nodes.new("FunctionNodeRandomValue")
        rv.location = (loc[0] - 150, loc[1])
        rv.data_type = "FLOAT_VECTOR"
        rv.inputs["Min"].default_value = (-amt, -amt, -amt)
        rv.inputs["Max"].default_value = (amt, amt, amt)
        links.new(pos.outputs["Position"], rv.inputs["ID"])
        sp = nodes.new("GeometryNodeSetPosition")
        sp.location = loc
        links.new(ico_node.outputs["Mesh"], sp.inputs["Geometry"])
        links.new(rv.outputs["Value"], sp.inputs["Offset"])
        return sp

    # ---- beam: white core + amber shell along +Y ----
    beam_len = mnode("MULTIPLY", loc=(-400, -620))
    links.new(gin.outputs["Fire"], beam_len.inputs[0])
    links.new(gin.outputs["BeamLength"], beam_len.inputs[1])

    core = nodes.new("GeometryNodeMeshCylinder")
    core.location = (-700, -700)
    core.inputs["Vertices"].default_value = 24
    core.inputs["Radius"].default_value = 0.14
    core.inputs["Depth"].default_value = 1.0
    shell = nodes.new("GeometryNodeMeshCylinder")
    shell.location = (-700, -950)
    shell.inputs["Vertices"].default_value = 24
    shell.inputs["Radius"].default_value = 0.26
    shell.inputs["Depth"].default_value = 1.0

    def beam_geo(cyl, y_off, loc, len_factor=1.0):
        # cylinder axis is Z; rotate to Y, scale Z->length, offset so base at gauntlet
        tr = nodes.new("GeometryNodeTransform")
        tr.location = loc
        links.new(cyl.outputs["Mesh"], tr.inputs["Geometry"])
        tr.inputs["Rotation"].default_value = (math.pi / 2, 0, 0)
        scl = nodes.new("ShaderNodeCombineXYZ")
        scl.location = (loc[0] - 150, loc[1])
        scl.inputs["X"].default_value = 1.0
        scl.inputs["Z"].default_value = 1.0
        blen = mnode("MULTIPLY", b=len_factor, loc=(loc[0] - 280, loc[1]))
        links.new(beam_len.outputs["Value"], blen.inputs[0])
        links.new(blen.outputs["Value"], scl.inputs["Y"])
        links.new(scl.outputs["Vector"], tr.inputs["Scale"])
        mv = nodes.new("GeometryNodeTransform")
        mv.location = (loc[0] + 150, loc[1])
        links.new(tr.outputs["Geometry"], mv.inputs["Geometry"])
        half = mnode("MULTIPLY", b=0.5 * len_factor, loc=(loc[0] + 150, loc[1] - 120))
        links.new(beam_len.outputs["Value"], half.inputs[0])
        # translation needs a vector: combine (0, half, y_off)
        tvec = nodes.new("ShaderNodeCombineXYZ")
        tvec.location = (loc[0] + 150, loc[1] - 200)
        tvec.inputs["X"].default_value = 0.0
        tvec.inputs["Z"].default_value = y_off
        links.new(half.outputs["Value"], tvec.inputs["Y"])
        links.new(tvec.outputs["Vector"], mv.inputs["Translation"])
        return mv

    core_geo = beam_geo(core, 0.0, (-500, -700), 1.0)
    shell_geo = beam_geo(shell, 0.0, (-500, -950), 0.7)

    # ---- beam tip: jagged zigzag leading edge (sheet 04) at the beam's end ----
    tip = nodes.new("GeometryNodeMeshIcoSphere")
    tip.location = (-850, -820)
    tip.inputs["Subdivisions"].default_value = 2
    tip.inputs["Radius"].default_value = 0.28
    tip_sp = jitter(tip, 0.22, 1, (-200, -820))
    tip_mv = nodes.new("GeometryNodeTransform")
    tip_mv.location = (-50, -820)
    links.new(tip_sp.outputs["Geometry"], tip_mv.inputs["Geometry"])
    tip_vec = nodes.new("ShaderNodeCombineXYZ")
    tip_vec.location = (-50, -950)
    tip_vec.inputs["X"].default_value = 0.0
    tip_vec.inputs["Z"].default_value = 0.0
    links.new(beam_len.outputs["Value"], tip_vec.inputs["Y"])
    links.new(tip_vec.outputs["Vector"], tip_mv.inputs["Translation"])

    # ---- burst flash: random-displaced icosphere at muzzle (jagged starburst) ----
    ico = nodes.new("GeometryNodeMeshIcoSphere")
    ico.location = (-850, -1200)
    ico.inputs["Subdivisions"].default_value = 3
    ico.inputs["Radius"].default_value = 0.5
    setpos = jitter(ico, 0.35, 0, (-200, -1200))
    bscale = mnode("MULTIPLY", b=1.6, loc=(-50, -1350))
    links.new(gin.outputs["Fire"], bscale.inputs[0])
    bvec = nodes.new("ShaderNodeCombineXYZ")
    bvec.location = (100, -1350)
    links.new(bscale.outputs["Value"], bvec.inputs["X"])
    links.new(bscale.outputs["Value"], bvec.inputs["Y"])
    links.new(bscale.outputs["Value"], bvec.inputs["Z"])
    btr = nodes.new("GeometryNodeTransform")
    btr.location = (250, -1200)
    links.new(setpos.outputs["Geometry"], btr.inputs["Geometry"])
    links.new(bvec.outputs["Vector"], btr.inputs["Scale"])
    btr.inputs["Translation"].default_value = (0, 0.4, 0)

    # ---- sparks: points in a small volume at the muzzle, instanced ----
    pts = nodes.new("GeometryNodeDistributePointsInVolume")
    pts.location = (-700, -1500)
    pts.inputs["Density"].default_value = 60.0
    ball = nodes.new("GeometryNodeMeshIcoSphere")
    ball.location = (-850, -1550)
    ball.inputs["Subdivisions"].default_value = 1
    ball.inputs["Radius"].default_value = 0.7
    m2v = nodes.new("GeometryNodeMeshToVolume")
    m2v.location = (-700, -1600)
    links.new(ball.outputs["Mesh"], m2v.inputs["Mesh"])
    links.new(m2v.outputs["Volume"], pts.inputs["Volume"])
    spark = nodes.new("GeometryNodeMeshIcoSphere")
    spark.location = (-700, -1650)
    spark.inputs["Subdivisions"].default_value = 0
    spark.inputs["Radius"].default_value = 0.05
    inst = nodes.new("GeometryNodeInstanceOnPoints")
    inst.location = (-500, -1500)
    links.new(pts.outputs["Points"], inst.inputs["Points"])
    links.new(spark.outputs["Mesh"], inst.inputs["Instance"])
    sscale = mnode("MULTIPLY", loc=(-350, -1650))
    links.new(gin.outputs["Fire"], sscale.inputs[0])
    links.new(sscale.outputs["Value"], inst.inputs["Scale"])

    # ---- materials on pieces ----
    mat_core = make_emission_material("CJ_FX_Core", CORE_WHITE, CORE_STRENGTH)
    mat_glow = make_emission_material("CJ_FX_Glow", GLOW_AMBER, GLOW_STRENGTH)
    mat_arc = make_emission_material("CJ_FX_Arc", ARC_CYAN, ARC_STRENGTH)

    def set_mat(geo_node, mat, out_sock="Geometry"):
        sm = nodes.new("GeometryNodeSetMaterial")
        sm.location = (geo_node.location[0] + 170, geo_node.location[1])
        sm.inputs["Material"].default_value = mat
        links.new(geo_node.outputs[out_sock], sm.inputs["Geometry"])
        return sm

    ring_mats = [set_mat(g, mat_arc if i == 2 else mat_glow) for i, g in enumerate(ring_geos)]
    core_m = set_mat(core_geo, mat_core)
    shell_m = set_mat(shell_geo, mat_glow)
    tip_m = set_mat(tip_mv, mat_core)
    burst_m = set_mat(btr, mat_core)
    spark_m = set_mat(inst, mat_glow, out_sock="Instances")

    join = nodes.new("GeometryNodeJoinGeometry")
    join.location = (700, 0)
    for g in ring_mats + [core_m, shell_m, tip_m, burst_m, spark_m]:
        links.new(g.outputs["Geometry"], join.inputs["Geometry"])
    links.new(join.outputs["Geometry"], gout.inputs["Geometry"])
    return group


def add_driver(target, data_path, expression, sources):
    """target: ID object or modifier; data_path: RNA path; sources: {var: (id_obj, data_path)}."""
    d = target.driver_add(data_path).driver
    d.type = "SCRIPTED"
    for var, (src_id, src_path) in sources.items():
        v = d.variables.new()
        v.name = var
        v.type = "SINGLE_PROP"
        v.targets[0].id = src_id
        v.targets[0].data_path = src_path
    d.expression = expression
    return d


def build_scene(group):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 16
    sc.render.resolution_x = 640
    sc.render.resolution_y = 360
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False

    world = bpy.data.worlds.new("CJ_DarkVoid")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.008, 0.008, 0.015, 1.0)
    sc.world = world

    # dummy gauntlet: forearm cylinder + white cuff + fist, aimed +Y
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=2.2, location=(0, -1.1, 0))
    arm = bpy.context.active_object
    arm.name = "CJ_DummyForearm"
    cuff_mat = bpy.data.materials.new("CJ_CuffWhite")
    cuff_mat.use_nodes = True
    cuff_mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = CUFF_WHITE
    arm.data.materials.append(cuff_mat)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(0, 0.15, 0))
    fist = bpy.context.active_object
    fist.name = "CJ_DummyFist"
    fist.data.materials.append(cuff_mat)

    # driver empty: charge / fire / recoil custom props (the animator's 3 knobs)
    bpy.ops.object.empty_add(location=(0, 0, 0))
    drv = bpy.context.active_object
    drv.name = "CJ_BlasterDriver"
    drv["charge"] = 1.0
    drv["fire"] = 1.0
    drv["recoil"] = 0.0

    fx = bpy.data.objects.new("CJ_BlasterFX", bpy.data.meshes.new("CJ_BlasterFXMesh"))
    bpy.context.collection.objects.link(fx)
    mod = fx.modifiers.new("BlasterFX", "NODES")
    mod.node_group = group
    # map socket name -> identifier, set proof values, then drive Charge/Fire
    idents = {}
    tree = mod.node_group.interface if hasattr(mod.node_group, "interface") else None
    items = tree.items_tree if tree is not None else mod.node_group.inputs
    for inp in items:
        idents[inp.name] = inp.identifier
    print("SOCKET-IDENTS:", idents)
    for key, val in (("Charge", 1.0), ("Fire", 1.0), ("Seed", 7), ("BeamLength", 6.0)):
        if key in idents:
            mod[idents[key]] = val
    print("MOD-KEYS:", sorted(mod.keys()))
    add_driver(mod, '["%s"]' % idents["Charge"], "charge", {"charge": (drv, '["charge"]')})
    add_driver(mod, '["%s"]' % idents["Fire"], "fire", {"fire": (drv, '["fire"]')})

    # cast light: amber point at the muzzle; energy = charge*200 + fire*1500
    bpy.ops.object.light_add(type="POINT", location=(0, 1.2, 0.6))
    lamp = bpy.context.active_object
    lamp.name = "CJ_BlasterLight"
    lamp.data.color = GLOW_AMBER[:3]
    add_driver(lamp.data, "energy", "charge*200 + fire*1500",
               {"charge": (drv, '["charge"]'), "fire": (drv, '["fire"]')})

    # motivated rim rig (10:35 refinement): space setting -> cyan-blue rim...
    bpy.ops.object.light_add(type="AREA", location=(-2.5, 0.5, 1.5))
    rim = bpy.context.active_object
    rim.name = "CJ_RimLight_Space"
    rim.data.color = (0.13, 0.83, 0.93)
    # ...that yields to the blaster during FIRE (10:36 lighting concept)
    add_driver(rim.data, "energy", "(1-fire)*300 + 20", {"fire": (drv, '["fire"]')})

    # blast-color rim: takes over the scene while firing (the signature device)
    bpy.ops.object.light_add(type="AREA", location=(-2.5, 0.5, 1.5))
    blast_rim = bpy.context.active_object
    blast_rim.name = "CJ_RimLight_Blast"
    blast_rim.data.color = GLOW_AMBER[:3]
    blast_rim.rotation_euler = (math.pi / 2, 0, math.pi / 3)
    add_driver(blast_rim.data, "energy", "fire*1200", {"fire": (drv, '["fire"]')})

    bpy.ops.object.empty_add(location=(0, 2.2, 0))
    look = bpy.context.active_object
    look.name = "CJ_LookTarget"

    cam_data = bpy.data.cameras.new("CJ_Cam")
    cam = bpy.data.objects.new("CJ_Cam", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = (8.5, -1.5, 3.2)
    tt = cam.constraints.new("TRACK_TO")
    tt.target = look
    tt.track_axis = "TRACK_NEGATIVE_Z"
    tt.up_axis = "UP_Y"
    sc.camera = cam

    sc.render.filepath = os.path.join(os.path.dirname(OUT_BLEND), "proof", "blaster_fire_proof.png")
    return sc


def main():
    wipe()
    group = build_blaster_group()
    sc = build_scene(group)
    bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
    print("SAVED:", OUT_BLEND)
    print("GROUP-NODES:", len(group.nodes))
    bpy.ops.render.render(write_still=True)
    print("RENDERED:", sc.render.filepath)


if __name__ == "__main__":
    main()
