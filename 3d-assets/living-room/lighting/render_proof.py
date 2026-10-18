"""
Headless proof renderer for the lighting rig (verification only — never saved).
Usage:
    blender -b rigged.blend --python render_proof.py -- <preset> <camera> <out.png> [samples] [env]

Render settings are set IN-MEMORY ONLY (the .blend is never re-saved by this
script): Cycles, 960x540@50% (canon), OpenImageDenoise on, volume bounces 0.
Pass samples=24 for canon-exact, higher for cleaner volumetrics.
"""
import bpy
import sys

PRESET_COLORS = {
    0: (0.45, 0.10, 0.90),    # DEFAULT violet #731AE5 — canon
    1: (1.0, 0.0, 0.0),       # RED
    2: (0.0, 0.0, 1.0),       # BLUE
    3: (0.643, 0.283, 0.643),  # BROKEN_STREETLIGHT purple
}
SPACE_CYAN = (0.0, 1.0, 1.0)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    preset = int(argv[0]) if len(argv) > 0 else 0
    camera = argv[1] if len(argv) > 1 else "MainCam"
    out = argv[2] if len(argv) > 2 else "/tmp/proof.png"
    samples = int(argv[3]) if len(argv) > 3 else 32
    env = int(argv[4]) if len(argv) > 4 else 0
    assert preset in PRESET_COLORS

    rig = bpy.data.objects.get("LED_RemoteRig")
    assert rig, "LED_RemoteRig not found — run apply_lighting_rig.py first"
    rig["preset"] = preset
    rig["environment"] = env
    color = PRESET_COLORS[preset]
    bpy.data.objects["RoomLight"].data.color = color
    led = bpy.data.materials["LEDStripMat"]
    led.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (*color, 1.0)
    rim = bpy.data.objects.get("RimLight")
    if rim:
        rim.data.color = SPACE_CYAN if env == 1 else color

    cam = bpy.data.objects.get(camera)
    assert cam and cam.type == 'CAMERA', f"camera {camera} not found"
    bpy.context.scene.camera = cam

    s = bpy.context.scene
    r = s.render
    r.engine = 'CYCLES'
    r.resolution_x, r.resolution_y, r.resolution_percentage = 960, 540, 50
    r.film_transparent = False
    r.image_settings.file_format = 'PNG'
    s.cycles.samples = samples
    s.cycles.use_denoising = True
    s.cycles.denoiser = 'OPENIMAGEDENOISE'
    s.cycles.volume_bounces = 0  # single-scatter god rays: fast, reads on camera
    try:
        s.cycles.device = 'CPU'
    except Exception:
        pass

    bpy.context.view_layer.update()
    r.filepath = out
    bpy.ops.render.render(write_still=True)
    print(f"render_proof: preset={preset} env={env} camera={camera} "
          f"samples={samples} -> {out}")


main()
