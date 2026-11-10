#!/usr/bin/env python3
"""godray_kit.py — Cape Jones in-house god-ray / atmosphere kit (Blender 4.x).

Two-mode system, studied from how the industry does it (fake emissive shafts
for speed + true volumes for realism), written as our own bpy code:

  MODE 1 — build_fake_shaft(): a cone mesh whose VOLUME output is an Emission
  shader with fresnel edge fade + animated noise breakup. Renders ~10x faster
  than a true volume, no fireflies, and the look is directable. A matching Spot
  light (Track To the shaft target) provides the REAL illumination; the cone
  only provides the visible beam. One master custom property `shaft_strength`
  on the control empty drives both.

  MODE 2 — build_true_volume_box(): a box filled with Principled Volume for
  real fog that shadows and responds to every light. Use sparingly (one per
  room max) — expensive.

  PRESETS:
  - window_shafts(): 2-3 fake shafts angled through the living-room window
    (right wall, opening 1.4 x 1.1 at x=3.5, y=1.5, z=1.6 per SCENE-CANON),
    warm daylight color.
  - lamp_haze(): small true-volume box around the floor lamp for glow.

Usage (inside Blender, headless or GUI):
    import godray_kit
    godray_kit.window_shafts()        # living-room window shafts
    godray_kit.build_fake_shaft(...)  # custom shaft
    godray_kit.build_true_volume_box(...)  # real fog box

Headless verify:
    xvfb-run -a env -u PYTHONPATH blender-4.5 -b --python tools/volumetrics/godray_kit.py -- --verify
"""
import math
import os
import sys

try:
    import bpy
    from mathutils import Vector
    IN_BLENDER = True
except ImportError:
    IN_BLENDER = False


# ---------------------------------------------------------------- fake shaft
def _add_driver(socket_or_data, data_path=None, index=-1):
    """driver_add that works on Blender 4.x (returns list) and 3.x."""
    if data_path is None:
        fc = socket_or_data.driver_add("default_value")
    elif index >= 0:
        fc = socket_or_data.driver_add(data_path, index)
    else:
        fc = socket_or_data.driver_add(data_path)
    if isinstance(fc, list):
        fc = fc[0]
    return fc.driver
def _emission_volume_material(name, color, noise_scale=1.5):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)
    emis = nt.nodes.new("ShaderNodeEmission")
    emis.location = (200, 0)
    emis.inputs["Color"].default_value = (*color, 1.0)
    emis.inputs["Strength"].default_value = 2.0
    nt.links.new(emis.outputs["Emission"], out.inputs["Volume"])

    # Fresnel edge fade: beam is bright in the middle, fades at silhouette.
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.location = (-400, 200)
    lw.inputs["Blend"].default_value = 0.35
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.location = (-200, 200)
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 0.65
    ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    nt.links.new(lw.outputs["Fresnel"], ramp.inputs["Fac"])

    # Length fade: brightest near the source, fading to the floor.
    tex = nt.nodes.new("ShaderNodeTexCoord")
    tex.location = (-600, -100)
    grad = nt.nodes.new("ShaderNodeTexGradient")
    grad.location = (-400, -100)
    grad.gradient_type = "LINEAR"
    lramp = nt.nodes.new("ShaderNodeValToRGB")
    lramp.location = (-200, -100)
    lramp.color_ramp.elements[0].position = 0.15
    lramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    lramp.color_ramp.elements[1].position = 0.95
    lramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    nt.links.new(tex.outputs["UV"], grad.inputs["Vector"])
    nt.links.new(grad.outputs["Color"], lramp.inputs["Fac"])

    # Animated noise breakup (dust in the air) — W is driven by frame.
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.location = (-400, -350)
    noise.noise_dimensions = "4D"
    noise.inputs["Scale"].default_value = noise_scale
    noise.inputs["Detail"].default_value = 4.0
    # NOTE (Blender quirk): in a freshly-cleared tree, socket name lookup can
    # fail until the tree updates once. Force-update via the node group call.
    try:
        w_socket = noise.inputs["W"]
    except KeyError:
        w_socket = noise.inputs[1]  # W is input index 1 on 4D noise
    nramp = nt.nodes.new("ShaderNodeValToRGB")
    nramp.location = (-200, -350)
    nramp.color_ramp.elements[0].position = 0.35
    nramp.color_ramp.elements[1].position = 0.75
    nt.links.new(noise.outputs["Fac"], nramp.inputs["Fac"])

    mult1 = nt.nodes.new("ShaderNodeMath")
    mult1.location = (0, 150)
    mult1.operation = "MULTIPLY"
    mult2 = nt.nodes.new("ShaderNodeMath")
    mult2.location = (0, -100)
    mult2.operation = "MULTIPLY"
    nt.links.new(ramp.outputs["Color"], mult1.inputs[0])
    nt.links.new(lramp.outputs["Color"], mult1.inputs[1])
    nt.links.new(mult1.outputs["Value"], mult2.inputs[0])
    nt.links.new(nramp.outputs["Color"], mult2.inputs[1])
    nt.links.new(mult2.outputs["Value"], emis.inputs["Strength"])
    return mat, noise, w_socket


def build_fake_shaft(name, source, target, radius_top=0.12, radius_bottom=0.55,
                      color=(1.0, 0.93, 0.78), strength=2.0, collection=None):
    """Build a fake god-ray shaft from `source` (lamp pos) to `target`."""
    src, tgt = Vector(source), Vector(target)
    direction = tgt - src
    length = direction.length

    bpy.ops.mesh.primitive_cone_add(
        vertices=32, radius1=radius_bottom, radius2=radius_top,
        depth=length,
        location=tuple((src + tgt) / 2))
    cone = bpy.context.active_object
    cone.name = name
    # Cone local +Z runs bottom(radius1)->top(radius2); aim -Z along beam.
    cone.rotation_euler = (0, 0, 0)
    d = direction.normalized()
    quat = Vector((0, 0, -1)).rotation_difference(d)
    cone.rotation_mode = "QUATERNION"
    cone.rotation_quaternion = quat

    # No shadow casting, no diffuse bounce contribution — the Spot does that.
    cone.visible_shadow = False
    cone.visible_diffuse = False
    cone.visible_glossy = False
    cone.visible_transmission = False

    mat, noise_node, w_socket = _emission_volume_material(name + "_mat", color)
    cone.data.materials.append(mat)

    # Matching real Spot light, aimed at the target.
    bpy.ops.object.light_add(type="SPOT", location=tuple(src))
    spot = bpy.context.active_object
    spot.name = name + "_spot"
    spot.data.energy = 400.0
    spot.data.color = color
    spot.data.spot_size = 2 * math.atan(radius_bottom / max(length, 1e-3))
    spot.data.spot_blend = 0.6
    spot.data.shadow_soft_size = 0.15
    tgt_empty = bpy.data.objects.new(name + "_target", None)
    (collection or bpy.context.scene.collection).objects.link(tgt_empty)
    tgt_empty.location = tuple(tgt)
    tgt_empty.empty_display_size = 0.1
    con = spot.constraints.new("TRACK_TO")
    con.target = tgt_empty
    con.track_axis = "TRACK_NEGATIVE_Z"
    con.up_axis = "UP_Y"

    # Master control: one empty, one custom prop, drives everything.
    ctrl = bpy.data.objects.new(name + "_ctrl", None)
    (collection or bpy.context.scene.collection).objects.link(ctrl)
    ctrl.location = tuple(src)
    ctrl["shaft_strength"] = strength
    emis_node = mat.node_tree.nodes.get("Emission")
    drv = _add_driver(emis_node.inputs["Strength"])
    var = drv.variables.new()
    var.name = "s"
    var.targets[0].id = ctrl
    var.targets[0].data_path = '["shaft_strength"]'
    drv.expression = "s"
    sdrv = _add_driver(spot.data, "energy")
    svar = sdrv.variables.new()
    svar.name = "s"
    svar.targets[0].id = ctrl
    svar.targets[0].data_path = '["shaft_strength"]'
    sdrv.expression = "s * 200"

    # Animate the noise W with the frame number (drifting dust).
    wdrv = _add_driver(w_socket)
    wdrv.expression = "frame * 0.02"

    if collection is not None:
        for o in (cone, spot, ctrl):
            if o.name not in collection.objects:
                collection.objects.link(o)
    return {"cone": cone, "spot": spot, "ctrl": ctrl,
            "target": tgt_empty, "material": mat}


# ------------------------------------------------------------- true volume
def build_true_volume_box(name, center, size, density=0.05,
                          color=(0.9, 0.9, 0.95), anisotropy=0.3,
                          collection=None):
    """A box of real Principled Volume fog. One per room max — expensive."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=tuple(center))
    box = bpy.context.active_object
    box.name = name
    box.dimensions = tuple(size)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    box.visible_shadow = False
    box.display_type = "WIRE"

    mat = bpy.data.materials.new(name + "_mat")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    pv = nt.nodes.new("ShaderNodeVolumePrincipled")
    pv.inputs["Density"].default_value = density
    pv.inputs["Color"].default_value = (*color, 1.0)
    pv.inputs["Anisotropy"].default_value = anisotropy
    nt.links.new(pv.outputs["Volume"], out.inputs["Volume"])
    box.data.materials.append(mat)

    box["fog_density"] = density
    drv = _add_driver(pv.inputs["Density"])
    var = drv.variables.new()
    var.name = "d"
    var.targets[0].id = box
    var.targets[0].data_path = '["fog_density"]'
    drv.expression = "d"
    if collection is not None:
        try:
            collection.objects.link(box)
        except RuntimeError:
            pass
    return {"box": box, "material": mat}


# ----------------------------------------------------------------- presets
def window_shafts(strength=2.0):
    """Living-room window shafts: warm beams through the right-wall window.

    Window per SCENE-CANON: right wall x=3.5, opening 1.4 x 1.1 centered at
    (3.5, 1.5, 1.6). Beams angle down-left into the room toward the rug.
    """
    col = bpy.data.collections.new("VOL_window_shafts")
    bpy.context.scene.collection.children.link(col)
    results = []
    beams = [
        ((3.45, 1.15, 2.05), (1.4, 0.9, 0.02), 0.10, 0.42),
        ((3.45, 1.50, 2.10), (1.1, 1.5, 0.02), 0.12, 0.50),
        ((3.45, 1.85, 2.05), (1.4, 2.1, 0.02), 0.10, 0.42),
    ]
    for i, (src, tgt, r1, r2) in enumerate(beams):
        results.append(build_fake_shaft(
            f"window_shaft_{i}", src, tgt, radius_top=r1,
            radius_bottom=r2, color=(1.0, 0.94, 0.80),
            strength=strength, collection=col))
    return results


def lamp_haze(density=0.08):
    """Small true-volume box around the floor lamp for a soft glow."""
    col = bpy.data.collections.new("VOL_lamp_haze")
    bpy.context.scene.collection.children.link(col)
    return build_true_volume_box(
        "lamp_haze", center=(3.0, 2.5, 1.0), size=(0.8, 0.8, 1.6),
        density=density, color=(1.0, 0.9, 0.7), collection=col)


# ------------------------------------------------------------------ verify
def _verify():
    col = bpy.data.collections.new("VOL_verify")
    bpy.context.scene.collection.children.link(col)
    r = build_fake_shaft("verify_shaft", (0, 0, 3), (2, 0, 0),
                         collection=col)
    assert r["cone"].type == "MESH"
    assert r["spot"].data.type == "SPOT"
    assert "shaft_strength" in r["ctrl"]
    assert r["material"].node_tree.nodes.get("Emission") is not None
    assert r["cone"].visible_shadow is False
    v = build_true_volume_box("verify_fog", (0, 0, 1), (1, 1, 1),
                              collection=col)
    assert v["box"].data.materials[0].node_tree.nodes.get(
        "Principled Volume") is not None
    print("GODRAY_KIT VERIFY: fake shaft + true volume OK")
    # 32px compile check of both volume shaders
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 1
    sc.render.resolution_x = 32
    sc.render.resolution_y = 32
    sc.render.filepath = "/tmp/godray_verify.png"
    bpy.ops.render.render(write_still=True)
    assert os.path.exists("/tmp/godray_verify.png")
    print("GODRAY_KIT VERIFY: 32px volume-shader compile render OK")


if __name__ == "__main__" or "--verify" in sys.argv:
    if IN_BLENDER and "--verify" in sys.argv:
        _verify()
    elif not IN_BLENDER:
        print("godray_kit: import inside Blender (bpy).")
