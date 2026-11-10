"""
Set the LED remote rig preset on an OPEN blend (headless render automation).
Usage:
    blender -b rigged.blend --python set_led_preset.py -- <preset 0..3> [env 0..1] [out.blend]

Authoritative setter: writes rig["preset"]/rig["environment"] AND the driven
colors directly (RoomLight, LEDStripMat emission, RimLight) from the preset
table — deterministic in background mode, no viewport needed. The drivers
installed by apply_lighting_rig.py agree with these values for interactive use.
"""
import bpy
import sys

PRESETS = {
    0: ("DEFAULT",            (0.45, 0.10, 0.90)),   # violet #731AE5 — canon
    1: ("RED",                (1.00, 0.00, 0.00)),   # remote red
    2: ("BLUE",               (0.00, 0.00, 1.00)),   # remote blue
    3: ("BROKEN_STREETLIGHT", (0.643, 0.283, 0.643)),  # parking-lot gag purple
}
SPACE_CYAN = (0.0, 1.0, 1.0)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    preset = int(argv[0]) if len(argv) > 0 else 0
    env = int(argv[1]) if len(argv) > 1 else 0
    out = argv[2] if len(argv) > 2 else None
    assert preset in PRESETS, f"preset must be 0..3, got {preset}"
    assert env in (0, 1), f"env must be 0..1, got {env}"

    rig = bpy.data.objects.get("LED_RemoteRig")
    assert rig, "LED_RemoteRig not found — run apply_lighting_rig.py first"
    rig["preset"] = preset
    rig["environment"] = env
    color = PRESETS[preset][1]
    rim_color = SPACE_CYAN if env == 1 else color

    room = bpy.data.objects.get("RoomLight")
    assert room, "RoomLight not found"
    room.data.color = color

    led = bpy.data.materials.get("LEDStripMat")
    assert led, "LEDStripMat not found"
    led.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (*color, 1.0)

    rim = bpy.data.objects.get("RimLight")
    rim_c = None
    if rim:
        rim.data.color = rim_color
        rim_c = tuple(round(c, 3) for c in rim.data.color)

    # tag + frame_set: ID-prop assignment doesn't tag the depsgraph headless,
    # so drivers would otherwise keep stale values
    rig.update_tag()
    bpy.context.scene.frame_set(bpy.context.scene.frame_current)
    bpy.context.view_layer.update()
    rc = tuple(round(c, 3) for c in room.data.color)
    assert all(abs(a - b) < 1e-3 for a, b in zip(rc, color)), \
        f"color write failed: {rc} != {color}"
    print(f"set_led_preset: preset={preset} ({PRESETS[preset][0]}) env={env} "
          f"RoomLight={rc} RimLight={rim_c}")
    if out:
        bpy.ops.wm.save_as_mainfile(filepath=out)
        print(f"saved {out}")


main()
