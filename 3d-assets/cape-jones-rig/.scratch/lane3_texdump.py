"""Lane 3: dump the body color texture to PNG and view it."""
import bpy
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/cape_jones_rigged_w5r_idle.blend")
for img in bpy.data.images:
    print("IMAGE:", img.name, "size:", img.size[0], "x", img.size[1], "has_data:", img.has_data,
          "filepath:", img.filepath, "packed:", img.packed_file is not None)
    if img.name.startswith("Color_2cad"):
        img.filepath_raw = "/home/hatch/workspace/cj-hands-work/3d-assets/cape-jones-rig/.scratch/body_color_tex.png"
        img.file_format = "PNG"
        try:
            img.save()
            print("SAVED body_color_tex.png")
        except Exception as e:
            print("SAVE FAIL:", e)
