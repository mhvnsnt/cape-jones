"""Render frame 1 of a single-preset CapeGP .blend to a PNG (transparent).

Usage inside Blender 5.2.3:
  blender -b --python blender_render.py -- --blend IN.blend --out OUT.png
"""
import bpy, sys, argparse
def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--blend", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    bpy.ops.wm.open_mainfile(filepath=args.blend)
    sc = bpy.context.scene
    sc.frame_set(1)
    sc.render.filepath = args.out
    bpy.ops.render.render(write_still=True)
    print("COLORED INVISIBLE RENDERED", args.out)
main()
