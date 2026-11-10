#!/usr/bin/env python3
"""led3d.py — Cape Jones in-house 3D LED system (Blender 4.x).

The canon room is soaked in violet LED glow (#731AE5). The gag is: he presses
the LED remote and the room color changes. How real studios do color-changing
practical lights: ONE master control drives every LED element (strips, practical
lights, screen glow) so they can never drift out of sync. That is this.

Master state lives on the SCENE as custom properties:
  LED_color       (float vector, RGBA) — the current LED color
  LED_brightness  (float)              — master dimmer, default 1.0

API:
  setup_led_master(color=(0.45,0.10,0.90,1), brightness=1.0)
      create/refresh the scene master props (canon violet default).
  wire_strip_material(mat_name, base_strength=4.0)
      non-destructive: finds the material's Emission node, drivers its Color
      from LED_color and its Strength from LED_brightness * base_strength.
      Use on LEDStripMat and the strip housing materials.
  wire_light(light_name, base_energy=None)
      drivers the light's color from LED_color, energy from
      LED_brightness * base_energy (defaults to current energy).
  apply_preset(name, frame_start=1, frame_end=250)
      keyframes the master props for a full animation:
        purple-pulse, chill-blue, ember-glow, ocean-calm, rainbow-cycle
  gag_press_sequence(colors, frames_per_color=48, frame_start=1)
      the remote gag: abrupt color jumps on each "press" + a final
      rainbow-cycle party tail.

The remote prop (LEDRemote + RemoteBtn_*) stays a dumb prop — the TV lane
keys the master props on press frames; every wired element follows.

Headless verify:
    xvfb-run -a env -u PYTHONPATH blender-4.5 -b --python tools/led-3d/led3d.py -- --verify
"""
import math
import sys

try:
    import bpy
    IN_BLENDER = True
except ImportError:
    IN_BLENDER = False

CANON_VIOLET = (0.451, 0.102, 0.898, 1.0)  # #731AE5

PRESETS = {
    "purple-pulse": {"colors": [CANON_VIOLET], "mode": "pulse"},
    "chill-blue": {"colors": [(0.20, 0.45, 1.0, 1.0)], "mode": "pulse"},
    "ember-glow": {"colors": [(1.0, 0.35, 0.10, 1.0)], "mode": "pulse"},
    "ocean-calm": {"colors": [(0.10, 0.65, 0.85, 1.0)], "mode": "fade"},
    "rainbow-cycle": {"colors": "rainbow", "mode": "cycle"},
}


def setup_led_master(color=CANON_VIOLET, brightness=1.0):
    sc = bpy.context.scene
    sc["LED_color"] = tuple(color)
    sc["LED_brightness"] = float(brightness)
    # UI niceties
    ui = sc.id_properties_ui("LED_color")
    ui.update(subtype="COLOR", description="Master LED color (drives strips + lights)")
    ui2 = sc.id_properties_ui("LED_brightness")
    ui2.update(min=0.0, max=3.0, description="Master LED dimmer")
    return sc


def _drive(target_socket, sc, prop, expr, index=-1):
    fc = target_socket.driver_add("default_value", index) \
        if index >= 0 else target_socket.driver_add("default_value")
    if isinstance(fc, list):
        fc = fc[0]
    drv = fc.driver
    var = drv.variables.new()
    var.name = "led"
    var.targets[0].id_type = "SCENE"
    var.targets[0].id = sc
    var.targets[0].data_path = f'["{prop}"]'
    drv.expression = expr
    return drv


def wire_strip_material(mat_name, base_strength=4.0):
    """Drive a strip material's Emission from the LED master (non-destructive)."""
    sc = setup_led_master() if "LED_color" not in bpy.context.scene else bpy.context.scene
    mat = bpy.data.materials.get(mat_name)
    if mat is None or not mat.use_nodes:
        raise ValueError(f"material '{mat_name}' missing or not node-based")
    emis = next((n for n in mat.node_tree.nodes if n.type == "EMISSION"), None)
    if emis is None:
        raise ValueError(f"material '{mat_name}' has no Emission node")
    _drive(emis.inputs["Color"], sc, "LED_color", "led")
    _drive(emis.inputs["Strength"], sc, "LED_brightness",
           f"led * {base_strength}")
    return mat


def wire_light(light_name, base_energy=None):
    """Drive a light object's color/energy from the LED master."""
    sc = bpy.context.scene
    if "LED_color" not in sc:
        setup_led_master()
    ob = bpy.data.objects.get(light_name)
    if ob is None or ob.type != "LIGHT":
        raise ValueError(f"light object '{light_name}' not found")
    if base_energy is None:
        base_energy = ob.data.energy
    # color is a 3-vector on light data: drive each channel
    try:
        ob.data.driver_remove("color")
    except (TypeError, RuntimeError):
        pass
    for i in range(3):
        fc = ob.data.driver_add("color", i)
        if isinstance(fc, list):
            fc = fc[0]
        drv = fc.driver
        var = drv.variables.new()
        var.name = "led"
        var.targets[0].id_type = "SCENE"
        var.targets[0].id = sc
        var.targets[0].data_path = '["LED_color"]'
        drv.expression = f"led[{i}]"
    fce = ob.data.driver_add("energy")
    if isinstance(fce, list):
        fce = fce[0]
    edrv = fce.driver
    evar = edrv.variables.new()
    evar.name = "led"
    evar.targets[0].id_type = "SCENE"
    evar.targets[0].id = sc
    evar.targets[0].data_path = '["LED_brightness"]'
    edrv.expression = f"led * {base_energy}"
    return ob


def _clear_led_fcurves():
    sc = bpy.context.scene
    ad = sc.animation_data
    if ad and ad.action:
        for fc in list(ad.action.fcurves):
            if 'LED_' in fc.data_path:
                ad.action.fcurves.remove(fc)


def _key(sc, prop, frame, value):
    sc[prop] = value
    sc.keyframe_insert(data_path=f'["{prop}"]', frame=frame)


def _rainbow(t):
    # HSV rainbow: hue rotates with t in [0,1)
    r = abs(((t * 3 + 0) % 2) - 1)
    g = abs(((t * 3 + 2 / 3) % 2) - 1)
    b = abs(((t * 3 + 4 / 3) % 2) - 1)
    return (r, g, b, 1.0)


def apply_preset(name, frame_start=1, frame_end=250):
    """Keyframe the LED master props for a preset animation."""
    if name not in PRESETS:
        raise ValueError(f"unknown preset {name} (choices: {list(PRESETS)})")
    sc = setup_led_master() if "LED_color" not in bpy.context.scene else bpy.context.scene
    _clear_led_fcurves()
    p = PRESETS[name]
    if p["mode"] == "pulse":
        col = p["colors"][0]
        _key(sc, "LED_color", frame_start, col)
        _key(sc, "LED_color", frame_end, col)
        n = 6
        for i in range(n + 1):
            f = frame_start + (frame_end - frame_start) * i / n
            b = 0.55 + 0.45 * math.sin(math.pi * i / n * 2) ** 2
            _key(sc, "LED_brightness", f, b)
    elif p["mode"] == "fade":
        col = p["colors"][0]
        _key(sc, "LED_color", frame_start, CANON_VIOLET)
        _key(sc, "LED_color", frame_end, col)
        _key(sc, "LED_brightness", frame_start, 1.0)
        _key(sc, "LED_brightness", frame_end, 1.0)
    elif p["mode"] == "cycle":
        n = 24
        for i in range(n + 1):
            f = frame_start + (frame_end - frame_start) * i / n
            _key(sc, "LED_color", f, _rainbow(i / n))
        _key(sc, "LED_brightness", frame_start, 1.0)
        _key(sc, "LED_brightness", frame_end, 1.0)
    # smooth it
    ad = sc.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            if "LED_" in fc.data_path:
                for kp in fc.keyframe_points:
                    kp.interpolation = "BEZIER"
    return sc


def gag_press_sequence(colors, frames_per_color=48, frame_start=1,
                       party_tail_frames=240):
    """The remote gag: jump-cut colors on each press, rainbow party tail."""
    sc = setup_led_master() if "LED_color" not in bpy.context.scene else bpy.context.scene
    _clear_led_fcurves()
    f = frame_start
    for col in colors:
        _key(sc, "LED_color", f, col)
        _key(sc, "LED_brightness", f, 1.0)
        f += frames_per_color
    n = 24
    for i in range(n + 1):
        _key(sc, "LED_color", f + party_tail_frames * i / n,
             _rainbow(i / n))
    _key(sc, "LED_brightness", f + party_tail_frames, 1.0)
    ad = sc.animation_data
    if ad and ad.action:
        for fc in ad.action.fcurves:
            if '["LED_color"]' in fc.data_path:
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"  # jump cuts, like a remote
    return sc


def _verify():
    sc = bpy.context.scene
    setup_led_master()
    assert tuple(sc["LED_color"]) == CANON_VIOLET
    # scratch strip material + light
    mat = bpy.data.materials.new("verify_strip")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    emis = nt.nodes.new("ShaderNodeEmission")
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(emis.outputs["Emission"], out.inputs["Surface"])
    wire_strip_material("verify_strip", base_strength=4.0)
    drv_paths = [d.data_path for d in mat.node_tree.animation_data.drivers]
    assert any("default_value" in p for p in drv_paths), \
        f"strip drivers missing: {drv_paths}"
    bpy.ops.object.light_add(type="POINT", location=(0, 0, 2))
    lamp = bpy.context.active_object
    lamp.name = "verify_led_light"
    lamp.data.energy = 300.0
    wire_light("verify_led_light")
    # evaluate drivers at frame 1 with a known color
    sc["LED_color"] = (1.0, 0.0, 0.0, 1.0)
    sc["LED_brightness"] = 0.5
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    lamp_eval = dg.objects.get("verify_led_light") \
        or lamp.evaluated_get(dg)
    col = tuple(lamp_eval.data.color)
    assert abs(col[0] - 1.0) < 1e-3 and abs(col[1]) < 1e-3, f"driver color wrong: {col}"
    assert abs(lamp_eval.data.energy - 150.0) < 1e-3, \
        f"driver energy wrong: {lamp_eval.data.energy}"
    # preset keyframing
    apply_preset("rainbow-cycle", 1, 49)
    ad = sc.animation_data
    fcs = [fc for fc in ad.action.fcurves if "LED_color" in fc.data_path]
    assert len(fcs) >= 3, "rainbow preset keyed too few curves"
    print("LED3D VERIFY: master props + strip/light drivers + preset keys OK")


if __name__ == "__main__" or "--verify" in sys.argv:
    if IN_BLENDER and "--verify" in sys.argv:
        _verify()
    elif not IN_BLENDER:
        print("led3d: import inside Blender (bpy).")
