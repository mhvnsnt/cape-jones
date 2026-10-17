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
    # SCOUT 2026-10-17: FX type variants (palette type_personalities) + per-scene
    # tint (canon: blaster colors are per-scene; core stays white). Tint is
    # threaded as a stored color attribute so shots drive it from the driver
    # empty without touching materials.
    add_group_socket(group, "FXType", "NodeSocketInt", default=0, min_v=0, max_v=3)
    add_group_socket(group, "TintR", "NodeSocketFloat", default=GLOW_AMBER[0], min_v=0.0, max_v=1.0)
    add_group_socket(group, "TintG", "NodeSocketFloat", default=GLOW_AMBER[1], min_v=0.0, max_v=1.0)
    add_group_socket(group, "TintB", "NodeSocketFloat", default=GLOW_AMBER[2], min_v=0.0, max_v=1.0)
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

    # ---- SCOUT 2026-10-17: FX type masks ----
    # 0=energy_beam 1=gauntlet_bolt 2=wave_pulse 3=arc_chain (palette type_personalities)
    fx = gin.outputs["FXType"]
    gt05 = mnode("GREATER_THAN", b=0.5, loc=(-700, -1750))
    links.new(fx, gt05.inputs[0])
    gt15 = mnode("GREATER_THAN", b=1.5, loc=(-700, -1830))
    links.new(fx, gt15.inputs[0])
    gt25 = mnode("GREATER_THAN", b=2.5, loc=(-700, -1910))
    links.new(fx, gt25.inputs[0])

    def one_minus(node, loc):
        s = mnode("SUBTRACT", a=1.0, loc=loc)
        links.new(node.outputs["Value"], s.inputs[1])
        return s

    is_beam = one_minus(gt05, (-550, -1750))
    is_bolt = mnode("MULTIPLY", loc=(-550, -1830))
    links.new(gt05.outputs["Value"], is_bolt.inputs[0])
    links.new(one_minus(gt15, (-550, -1900)).outputs["Value"], is_bolt.inputs[1])
    is_pulse = mnode("MULTIPLY", loc=(-550, -1980))
    links.new(gt15.outputs["Value"], is_pulse.inputs[0])
    links.new(one_minus(gt25, (-550, -2050)).outputs["Value"], is_pulse.inputs[1])
    is_arc = gt25
    beam_or_bolt = mnode("ADD", loc=(-400, -1830))
    links.new(is_beam.outputs["Value"], beam_or_bolt.inputs[0])
    links.new(is_bolt.outputs["Value"], beam_or_bolt.inputs[1])

    def gate(geo_node, mask_out, loc):
        """Scale a part to zero unless its FX-type mask is 1."""
        tr = nodes.new("GeometryNodeTransform")
        tr.location = loc
        links.new(geo_node.outputs[0], tr.inputs["Geometry"])
        cmb = nodes.new("ShaderNodeCombineXYZ")
        cmb.location = (loc[0] - 150, loc[1])
        for i in range(3):
            links.new(mask_out, cmb.inputs[i])
        links.new(cmb.outputs["Vector"], tr.inputs["Scale"])
        return tr

    # ---- SCOUT 2026-10-17: per-scene tint as stored color attribute ----
    tint_cmb = nodes.new("ShaderNodeCombineXYZ")
    tint_cmb.location = (-700, -2150)
    links.new(gin.outputs["TintR"], tint_cmb.inputs[0])
    links.new(gin.outputs["TintG"], tint_cmb.inputs[1])
    links.new(gin.outputs["TintB"], tint_cmb.inputs[2])

    def store_tint(geo_node, loc):
        st = nodes.new("GeometryNodeStoreNamedAttribute")
        st.location = loc
        st.data_type = 'FLOAT_COLOR'
        st.domain = 'POINT'
        st.inputs["Name"].default_value = "CJ_Tint"
        links.new(geo_node.outputs[0], st.inputs["Geometry"])
        links.new(tint_cmb.outputs["Vector"], st.inputs["Value"])
        return st

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

    core_geo = gate(beam_geo(core, 0.0, (-500, -700), 1.0),
                    is_beam.outputs["Value"], (-320, -700))
    shell_geo = gate(beam_geo(shell, 0.0, (-500, -950), 0.7),
                     is_beam.outputs["Value"], (-320, -950))

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
    # SCOUT: tip only exists for the sustained beam type
    tip_g = gate(tip_mv, is_beam.outputs["Value"], (130, -820))

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
    # SCOUT: gauntlet_bolt stretches the burst along the beam axis; burst shows
    # for beam and bolt types only
    bstretch = nodes.new("GeometryNodeTransform")
    bstretch.location = (420, -1200)
    links.new(btr.outputs["Geometry"], bstretch.inputs["Geometry"])
    bsy = mnode("MULTIPLY_ADD", a=2.0, loc=(270, -1350))
    links.new(is_bolt.outputs["Value"], bsy.inputs[1])
    bsy.inputs[2].default_value = 1.0
    bsvec = nodes.new("ShaderNodeCombineXYZ")
    bsvec.location = (270, -1450)
    bsvec.inputs["X"].default_value = 1.0
    bsvec.inputs["Z"].default_value = 1.0
    links.new(bsy.outputs["Value"], bsvec.inputs["Y"])
    links.new(bsvec.outputs["Vector"], bstretch.inputs["Scale"])
    burst_g = gate(bstretch, beam_or_bolt.outputs["Value"], (590, -1200))

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
    spark_tinted = store_tint(spark, (-700, -1720))
    links.new(spark_tinted.outputs["Geometry"], inst.inputs["Instance"])
    sscale = mnode("MULTIPLY", loc=(-350, -1650))
    links.new(gin.outputs["Fire"], sscale.inputs[0])
    links.new(sscale.outputs["Value"], inst.inputs["Scale"])

    # ---- SCOUT 2026-10-17: wave pulse — expanding torus driven by fire ----
    pulse_t = torus(3, 1.0, 0.09)
    pulse_tr = transform(pulse_t, rotation=(0, math.pi / 2, 0), loc=(-500, -2100))
    psc = mnode("MULTIPLY_ADD", a=2.5, loc=(-350, -2250))
    links.new(gin.outputs["Fire"], psc.inputs[0])
    psc.inputs[2].default_value = 0.3
    pvec = nodes.new("ShaderNodeCombineXYZ")
    pvec.location = (-200, -2250)
    for _i in range(3):
        links.new(psc.outputs["Value"], pvec.inputs[_i])
    links.new(pvec.outputs["Vector"], pulse_tr.inputs["Scale"])
    pulse_g = gate(pulse_tr, is_pulse.outputs["Value"], (-50, -2100))

    # ---- SCOUT 2026-10-17: impact flash at beam terminus (sheet 04) ----
    imp = nodes.new("GeometryNodeMeshIcoSphere")
    imp.location = (-850, -2400)
    imp.inputs["Subdivisions"].default_value = 2
    imp.inputs["Radius"].default_value = 0.5
    imp_j = jitter(imp, 0.3, 5, (-200, -2400))
    isc = mnode("MULTIPLY", b=2.2, loc=(-50, -2550))
    links.new(gin.outputs["Fire"], isc.inputs[0])
    ivec = nodes.new("ShaderNodeCombineXYZ")
    ivec.location = (100, -2550)
    for _i in range(3):
        links.new(isc.outputs["Value"], ivec.inputs[_i])
    itr = nodes.new("GeometryNodeTransform")
    itr.location = (250, -2400)
    links.new(imp_j.outputs["Geometry"], itr.inputs["Geometry"])
    links.new(ivec.outputs["Vector"], itr.inputs["Scale"])
    mv2 = nodes.new("GeometryNodeTransform")
    mv2.location = (400, -2400)
    links.new(itr.outputs["Geometry"], mv2.inputs["Geometry"])
    t2 = nodes.new("ShaderNodeCombineXYZ")
    t2.location = (400, -2530)
    t2.inputs["X"].default_value = 0.0
    t2.inputs["Z"].default_value = 0.0
    links.new(beam_len.outputs["Value"], t2.inputs["Y"])
    links.new(t2.outputs["Vector"], mv2.inputs["Translation"])
    impact_g = gate(mv2, is_beam.outputs["Value"], (550, -2400))
    iring = torus(4, 0.8, 0.06)
    iring_tr = transform(iring, rotation=(math.pi / 2, 0, 0), loc=(-500, -2650))
    links.new(ivec.outputs["Vector"], iring_tr.inputs["Scale"])
    mv3 = nodes.new("GeometryNodeTransform")
    mv3.location = (-350, -2650)
    links.new(iring_tr.outputs["Geometry"], mv3.inputs["Geometry"])
    links.new(t2.outputs["Vector"], mv3.inputs["Translation"])
    iring_g = gate(mv3, is_beam.outputs["Value"], (-200, -2650))

    # ---- materials on pieces ----
    mat_core = make_emission_material("CJ_FX_Core", CORE_WHITE, CORE_STRENGTH)
    mat_glow = make_emission_material("CJ_FX_Glow", GLOW_AMBER, GLOW_STRENGTH)
    mat_arc = make_emission_material("CJ_FX_Arc", ARC_CYAN, ARC_STRENGTH)
    # SCOUT 2026-10-17: tintable glow — color comes from the CJ_Tint point
    # attribute (driven per-scene by the driver's tint_r/g/b). Core stays white.
    mat_glow_tint = bpy.data.materials.new("CJ_FX_GlowTint")
    mat_glow_tint.use_nodes = True
    _bsdf = mat_glow_tint.node_tree.nodes.get("Principled BSDF")
    if _bsdf:
        mat_glow_tint.node_tree.nodes.remove(_bsdf)
    _out = mat_glow_tint.node_tree.nodes.get("Material Output")
    _attr = mat_glow_tint.node_tree.nodes.new("ShaderNodeAttribute")
    _attr.attribute_name = "CJ_Tint"
    _em = mat_glow_tint.node_tree.nodes.new("ShaderNodeEmission")
    _em.inputs["Strength"].default_value = GLOW_STRENGTH
    mat_glow_tint.node_tree.links.new(_attr.outputs["Color"], _em.inputs["Color"])
    mat_glow_tint.node_tree.links.new(_em.outputs["Emission"], _out.inputs["Surface"])

    def set_mat(geo_node, mat, out_sock="Geometry"):
        sm = nodes.new("GeometryNodeSetMaterial")
        sm.location = (geo_node.location[0] + 170, geo_node.location[1])
        sm.inputs["Material"].default_value = mat
        links.new(geo_node.outputs[out_sock], sm.inputs["Geometry"])
        return sm

    ring_mats = []
    for i, g in enumerate(ring_geos):
        if i == 2:
            ring_mats.append(set_mat(g, mat_arc))  # cyan arc ring stays fixed
        else:
            ring_mats.append(set_mat(store_tint(g, (g.location[0], g.location[1])),
                                     mat_glow_tint))
    core_m = set_mat(core_geo, mat_core)
    shell_m = set_mat(store_tint(shell_geo, (-150, -950)), mat_glow_tint)
    tip_m = set_mat(tip_g, mat_core)
    burst_m = set_mat(burst_g, mat_core)
    pulse_m = set_mat(store_tint(pulse_g, (120, -2100)), mat_glow_tint)
    impact_m = set_mat(impact_g, mat_core)
    iring_m = set_mat(store_tint(iring_g, (-30, -2650)), mat_glow_tint)
    spark_m = set_mat(inst, mat_glow_tint, out_sock="Instances")

    join = nodes.new("GeometryNodeJoinGeometry")
    join.location = (700, 0)
    for g in ring_mats + [core_m, shell_m, tip_m, burst_m, pulse_m,
                          impact_m, iring_m, spark_m]:
        links.new(g.outputs["Geometry"], join.inputs["Geometry"])
    links.new(join.outputs["Geometry"], gout.inputs["Geometry"])
    return group


def add_driver(target, data_path, expression, sources, index=-1):
    """target: ID object or modifier; data_path: RNA path; sources: {var: (id_obj, data_path)}.
    index: for array properties (e.g. light color), the channel to drive."""
    if index >= 0:
        d = target.driver_add(data_path, index).driver
    else:
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
    # SCOUT 2026-10-17: fx_type (0=energy_beam 1=gauntlet_bolt 2=wave_pulse
    # 3=arc_chain) + per-scene tint (canon: blaster colors are per-scene)
    drv["fx_type"] = 0
    drv["tint_r"] = GLOW_AMBER[0]
    drv["tint_g"] = GLOW_AMBER[1]
    drv["tint_b"] = GLOW_AMBER[2]

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
    for key, val in (("Charge", 1.0), ("Fire", 1.0), ("Seed", 7), ("BeamLength", 6.0),
                     ("FXType", 0), ("TintR", GLOW_AMBER[0]),
                     ("TintG", GLOW_AMBER[1]), ("TintB", GLOW_AMBER[2])):
        if key in idents:
            mod[idents[key]] = val
    print("MOD-KEYS:", sorted(mod.keys()))
    add_driver(mod, '["%s"]' % idents["Charge"], "charge", {"charge": (drv, '["charge"]')})
    add_driver(mod, '["%s"]' % idents["Fire"], "fire", {"fire": (drv, '["fire"]')})
    # SCOUT: drive the new sockets from the driver empty
    for _key, _prop in (("FXType", "fx_type"), ("TintR", "tint_r"),
                        ("TintG", "tint_g"), ("TintB", "tint_b")):
        if _key in idents:
            add_driver(mod, '["%s"]' % idents[_key], _prop,
                       {_prop: (drv, '["%s"]' % _prop)})

    # cast light: amber point at the muzzle; energy = charge*200 + fire*1500
    bpy.ops.object.light_add(type="POINT", location=(0, 1.2, 0.6))
    lamp = bpy.context.active_object
    lamp.name = "CJ_BlasterLight"
    lamp.data.color = GLOW_AMBER[:3]
    add_driver(lamp.data, "energy", "charge*200 + fire*1500",
               {"charge": (drv, '["charge"]'), "fire": (drv, '["fire"]')})
    # SCOUT: blast light follows the per-scene tint (canon: while firing, the
    # blast light BECOMES the scene lighting)
    for _i, _p in enumerate(("tint_r", "tint_g", "tint_b")):
        add_driver(lamp.data, "color", _p, {_p: (drv, '["%s"]' % _p)}, index=_i)

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
    # SCOUT: blast rim takes the per-scene tint too
    for _i, _p in enumerate(("tint_r", "tint_g", "tint_b")):
        add_driver(blast_rim.data, "color", _p, {_p: (drv, '["%s"]' % _p)}, index=_i)

    # SCOUT 2026-10-17: appendable blast-light rig (links into shot files;
    # the shot's own CJ_BlasterDriver feeds it — rig file itself never edited)
    rig_coll = bpy.data.collections.new("CJ_BlastLightRig")
    sc.collection.children.link(rig_coll)
    for _o in (lamp, rim, blast_rim):
        rig_coll.objects.link(_o)
        sc.collection.objects.unlink(_o)

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
