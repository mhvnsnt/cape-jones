"""
Cape Jones living room — LED remote lighting rig + volumetrics.
LANE 4: LIGHTING + GOD RAYS (owner directive 2026-10-17 ~20:51 CDT).

Applies to an OPEN living_room.blend (integration lane runs this; never hand-edit):
    blender -b 3d-assets/living_room.blend --python 3d-assets/living-room/lighting/apply_lighting_rig.py

WHAT IT DOES (additive only — locked canon defaults are NOT changed):
  1. Creates control Empty `LED_RemoteRig` with drivable properties:
       preset      int   0..3  0=DEFAULT violet #731AE5 (canon), 1=RED, 2=BLUE,
                              3=BROKEN_STREETLIGHT purple (parking-lot gag)
       environment int   0..1  0=ROOM, 1=SPACE (rim color source)
       vol_density float 0..0.2  room volume scatter density (0 = god rays off)
       rim_energy  float 0..500  rim/fill light energy
  2. Drivers (no addons, no registered functions — plain scripted expressions):
       RoomLight.color + LEDStripMat emission color <- preset
       RimLight.color <- environment==SPACE ? cyan : preset color
       VolumeBox density <- vol_density ; RimLight energy <- rim_energy
  3. Volumetric rig:
       VolumeBox_Room  : room-sized Principled Volume (subtle scatter)
       LampCone_Floor  : warm SPOT under the floor-lamp shade
       LampCone_Table  : warm SPOT under the table-lamp shade
       WindowShaft     : cool SPOT just inside the window -> visible god-ray shaft
       RimLight        : SPOT rim/fill on the recliner subject zone
  4. Render/volume guidance lives in LIGHTING-RIG.md (CPU vs Colab GPU tables).

Canon grounding (SCENE-CANON.md, owner-locked 2026-10-16 — untouched by this script):
  RoomLight  POINT  (0.45,0.10,0.90) energy 300 @ (0,0,2.4)
  Sun        SUN    white 1.5 @ (2,-4,5)
  HallLight  POINT  (1.0,0.914,0.588) energy 60 @ (-2.6,4.4,2.2)
  LED strips #731AE5 emission 4.0 | world (0.051) | Cycles 960x540@50% 24 samples
LED remote gag canon (SHOW-BIBLE.md section 8): remote changes world lighting anywhere;
  THE PARKING LOT gag = broken-streetlight purple ("ah, that's better.")
"""

import bpy
from mathutils import Vector
from math import radians

# ---------------------------------------------------------------- presets
# Linear RGB values as stored in the blend (canon values copied exactly).
PRESETS = {
    0: ("DEFAULT",      (0.45, 0.10, 0.90)),   # violet #731AE5 — canon, RoomLight/LED exact
    1: ("RED",          (1.00, 0.00, 0.00)),   # remote BtnMat_0 #FF0000
    2: ("BLUE",         (0.00, 0.00, 1.00)),   # remote BtnMat_2 #0000FF
    3: ("BROKEN_STREETLIGHT",
                        (0.643, 0.283, 0.643)),  # ~#A448A4: 65% canon violet + 35% sodium
}                                              # orange — the messed-up sodium lamp color
SPACE_CYAN = (0.0, 1.0, 1.0)                   # remote BtnMat_5 #00FFFF — rim in SPACE env


def _ternary(vals):
    """Build a driver expression selecting vals[i] by the `preset` variable."""
    expr = f"{vals[3]}"
    for i in (2, 1, 0):
        expr = f"({vals[i]} if preset=={i} else {expr})"
    return expr


PRESET_R = _ternary([f"{v[1][0]:.3f}" for v in PRESETS.values()])
PRESET_G = _ternary([f"{v[1][1]:.3f}" for v in PRESETS.values()])
PRESET_B = _ternary([f"{v[1][2]:.3f}" for v in PRESETS.values()])
# Rim: cyan in SPACE, otherwise the LED preset color.
RIM_R = f"(0.0 if env==1 else {PRESET_R})"
RIM_G = f"(1.0 if env==1 else {PRESET_G})"
RIM_B = f"(1.0 if env==1 else {PRESET_B})"


def get_rig():
    rig = bpy.data.objects.get("LED_RemoteRig")
    if rig is None:
        rig = bpy.data.objects.new("LED_RemoteRig", None)
        bpy.context.scene.collection.objects.link(rig)
        rig.empty_display_type = 'SPHERE'
        rig.empty_display_size = 0.25
    rig["preset"] = 0
    rig["environment"] = 0
    rig["vol_density"] = 0.015
    rig["rim_energy"] = 60.0
    rig.id_properties_ui("preset").update(min=0, max=3,
        description="0 DEFAULT violet #731AE5 | 1 RED | 2 BLUE | 3 BROKEN_STREETLIGHT purple")
    rig.id_properties_ui("environment").update(min=0, max=1,
        description="0 ROOM (rim = LED color) | 1 SPACE (rim = cyan)")
    rig.id_properties_ui("vol_density").update(min=0.0, max=0.2,
        description="Room volume scatter density — 0 disables god rays")
    rig.id_properties_ui("rim_energy").update(min=0.0, max=500.0,
        description="RimLight energy")
    return rig


def add_driver_var(drv, name, rig, data_path):
    var = drv.variables.new()
    var.name = name
    var.type = 'SINGLE_PROP'
    tgt = var.targets[0]
    tgt.id = rig
    tgt.data_path = data_path
    return var


def drive_rgb(target, data_path, exprs, rig, extra_vars=()):
    """Drive a 3-channel color property with per-channel expressions."""
    for idx, expr in enumerate(exprs):
        fc = target.driver_add(data_path, idx)
        drv = fc.driver
        drv.type = 'SCRIPTED'
        add_driver_var(drv, "preset", rig, '["preset"]')
        for vname, vpath in extra_vars:
            add_driver_var(drv, vname, rig, vpath)
        drv.expression = expr
        # fail loud: an invalid expression silently keeps the base value
        assert drv.is_valid, f"driver expression invalid: {expr!r}"


def drive_float(target, data_path, rig, prop):
    fc = target.driver_add(data_path)
    drv = fc.driver
    drv.type = 'SCRIPTED'
    add_driver_var(drv, "p", rig, f'["{prop}"]')
    drv.expression = "p"
    assert drv.is_valid, f"driver expression invalid for {data_path}"


def aim_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def make_spot(name, location, target, color, energy, size_deg, blend=0.4):
    data = bpy.data.lights.new(name, 'SPOT')
    data.color = color
    data.energy = energy
    data.spot_size = radians(size_deg)
    data.spot_blend = blend
    data.use_shadow = True
    data.shadow_soft_size = 0.15
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = location
    aim_at(obj, target)
    return obj


def get_volume_mat():
    mat = bpy.data.materials.get("VolumeMat_Room")
    if mat is None:
        mat = bpy.data.materials.new("VolumeMat_Room")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.name = "Principled Volume"
    vol.inputs["Density"].default_value = 0.015
    vol.inputs["Anisotropy"].default_value = 0.7
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(vol.outputs["Volume"], out.inputs["Volume"])
    return mat


def main():
    rig = get_rig()
    scene = bpy.context.scene
    coll = scene.collection

    # --- existing canon lights: drive COLOR ONLY (energy/position untouched) ---
    room = bpy.data.objects.get("RoomLight")
    assert room and room.data.type == 'POINT', "RoomLight POINT light not found — canon broken?"
    drive_rgb(room.data, "color", (PRESET_R, PRESET_G, PRESET_B), rig)

    led = bpy.data.materials.get("LEDStripMat")
    assert led, "LEDStripMat not found — canon broken?"
    princ = led.node_tree.nodes.get("Principled BSDF")
    assert princ, "LEDStripMat has no Principled BSDF — canon broken?"
    drive_rgb(princ.inputs["Emission Color"], "default_value",
              (PRESET_R, PRESET_G, PRESET_B), rig)

    # --- room volume box (subtle scatter; camera stays outside it) ---
    vbox = bpy.data.objects.get("VolumeBox_Room")
    if vbox is None:
        mesh = bpy.data.meshes.new("VolumeBox_Room_Mesh")
        mesh.from_pydata(
            [(-3.5, -3, 0), (3.5, -3, 0), (3.5, 3, 0), (-3.5, 3, 0),
             (-3.5, -3, 3), (3.5, -3, 3), (3.5, 3, 3), (-3.5, 3, 3)],
            [], [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
                 (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)])
        mesh.update()
        vbox = bpy.data.objects.new("VolumeBox_Room", mesh)
        coll.objects.link(vbox)
        vbox.display_type = 'WIRE'
    vbox.data.materials.clear()
    vmat = get_volume_mat()
    vbox.data.materials.append(vmat)
    drive_float(vmat.node_tree.nodes["Principled Volume"].inputs["Density"],
                "default_value", rig, "vol_density")

    # --- lamp cone spots (warm, from the real lamp positions) ---
    for lamp_name, rig_name, energy, size in (
            ("lampRoundFloor(Clone)", "LampCone_Floor", 30.0, 60.0),
            ("lampSquareTable(Clone)", "LampCone_Table", 18.0, 55.0)):
        lamp = bpy.data.objects.get(lamp_name)
        if lamp is None:
            print(f"WARN: {lamp_name} not found, skipping {rig_name}")
            continue
        if rig_name not in bpy.data.objects:
            loc = (lamp.location.x, lamp.location.y, lamp.location.z + 0.10)
            make_spot(rig_name, loc, (lamp.location.x, lamp.location.y, 0.0),
                      (1.0, 0.914, 0.588), energy, size)

    # --- window god-ray shaft (cool spot just inside the window plane) ---
    if "WindowShaft" not in bpy.data.objects:
        make_spot("WindowShaft", (3.80, 1.50, 2.00), (-1.20, -0.20, 0.0),
                  (0.85, 0.92, 1.00), 120.0, 38.0, blend=0.55)

    # --- rim/fill on the recliner subject zone (color = env-driven) ---
    rim = bpy.data.objects.get("RimLight")
    if rim is None:
        rim = make_spot("RimLight", (2.60, 3.40, 2.60), (3.14, 1.20, 0.50),
                        PRESETS[0][1], 60.0, 42.0, blend=0.5)
    drive_rgb(rim.data, "color", (RIM_R, RIM_G, RIM_B), rig,
              extra_vars=(("env", '["environment"]'),))
    drive_float(rim.data, "energy", rig, "rim_energy")

    # --- sanity: drivers must evaluate; preset 0 must reproduce canon exactly ---
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    rc = room.evaluated_get(dg).data.color
    assert all(abs(a - b) < 1e-4 for a, b in zip(rc, PRESETS[0][1])), \
        f"preset 0 drifted from canon: {tuple(rc)}"
    print("apply_lighting_rig: OK — rig live, preset 0 == canon "
          f"RoomLight {tuple(round(c,3) for c in rc)}")

main()
