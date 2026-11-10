#!/usr/bin/env python3
"""Room-at-2.5x Blender proof — Cycles CPU, textured planes, orthographic camera.
Canvas 1168x1060 (locked-sheet frame). Background plane: desk-painted canvas
(desk painting + floor extension, prep file). Character plane: grey-keyed apose
alpha PNG (prep file). Character height set to 950px by construction:
apose char = 1041px of 1500px plate; plane scaled 950/1041 = 0.9126.
Feet target canvas y=985 from top (on the floor band); plane centre computed
from plate geometry (feet 543px below plate centre, char centre +11.5px right
of plate centre). Emission shaders (shadeless) so colours are the plate colours.
Run: blender --background --python blender_room_proof_20261031.py -- <bg.png> <char.png> <out.png> <out.blend>
"""
import sys, os
import bpy

def main():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]
    bg_path, char_path, out_png, out_blend = [os.path.abspath(a) for a in argv[:4]]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 32
    scene.cycles.use_denoising = False
    scene.render.resolution_x = 1168
    scene.render.resolution_y = 1060
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.filepath = out_png
    scene.view_settings.view_transform = 'Standard'
    scene.display_settings.display_device = 'sRGB'
    world = bpy.data.worlds.new("World")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
    scene.world = world

    def plane(name, w, h, x, y, z, img_path, use_alpha):
        bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, z))
        ob = bpy.context.active_object
        ob.name = name
        ob.dimensions = (w, h, 0)
        mat = bpy.data.materials.new(name + "_mat")
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(img_path)
        tex.interpolation = 'Linear'
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Strength"].default_value = 1.0
        nt.links.new(tex.outputs["Color"], em.inputs["Color"])
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        if use_alpha:
            tr = nt.nodes.new("ShaderNodeBsdfTransparent")
            mix = nt.nodes.new("ShaderNodeMixShader")
            nt.links.new(tex.outputs["Alpha"], mix.inputs["Fac"])
            nt.links.new(tr.outputs["BSDF"], mix.inputs[1])
            nt.links.new(em.outputs["Emission"], mix.inputs[2])
            nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
        else:
            nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
        ob.data.materials.append(mat)
        # UV: default plane UVs already map 0..1; ensure correct orientation
        return ob

    # Background plane fills frame: 11.68 x 10.60 world units = 100 px/unit.
    plane("BG_plane", 11.68, 10.60, 0, 0, 0, bg_path, False)
    # Character plane: plate 11.0 x 15.0 scaled 0.9126 -> char height 9.50 units = 950px.
    s = 950 / 1041
    plane("Char_plane", 11.0 * s, 15.0 * s, 0.105, 0.405, 0.1, char_path, True)

    bpy.ops.object.camera_add(location=(0, 0, 10))
    cam = bpy.context.active_object
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = 11.68
    cam.rotation_euler = (0, 0, 0)
    scene.camera = cam
    bpy.ops.wm.save_as_mainfile(filepath=out_blend)
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED {out_png} exists={os.path.exists(out_png)}")

if __name__ == "__main__":
    main()
