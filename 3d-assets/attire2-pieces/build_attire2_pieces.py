#!/usr/bin/env python3
"""
CJ Attire-2 piece staging — procedural superhero costume parts (OUR geometry).

Canon (owner 2026-10-17 ~14:47 CDT): Cyborg X = Cape Jones, same person.
Future Attire 2 = female-universe reskin of Cyborg X (Alisa's Tekken model):
Space Ghost style WITHOUT head ears, WHITE eyes, Batgirl-style pieces —
from OUR pulled pieces, NOT any actual 3D Cape Ghost model.

This lane STAGES pieces only. It does NOT build Attire 2. The attire lane
fits/scales/paints these onto Alisa's model later.

Pieces (all separate objects, clean toon geometry, neutral materials —
colors are UNSET; the attire lane paints per the future Attire-2 sheet):
  - CJ_A2_DominoMask   Batgirl-style eye band, earless, open eye slots
                       (white-eye cards from 3d-assets/face-rig sit behind)
  - CJ_A2_Cowl         earless cowl shell, open face (canon: NO head ears)
  - CJ_A2_Cape         single-sheet shoulder-hung cape panel, unposed
                       (matches the cape lane's single-sheet rebuild spec)
  - CJ_A2_Gauntlet_L/R flared forearm gauntlets
  - CJ_A2_Boot_L/R     toon boots (shin + foot)
  - CJ_A2_Belt         utility belt band + pouches
  - CJ_A2_Emblem       blank chest emblem (diamond shield, unpainted)

Built at approximate CJ head scale (head radius ~0.09, eye line z ~0.92
in rig space). Attire lane re-fits.

Usage:
    xvfb-run -a env -u PYTHONPATH ~/workspace/tools/blender/blender-4.0.2-linux-x64/blender \
        -b --python build_attire2_pieces.py -- ./cj_attire2_pieces.blend
"""
import bpy
import math
import sys

OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "./cj_attire2_pieces.blend"

HEAD_R = 0.09
EYE_Z = 0.92


def wipe():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.materials):
        for x in list(coll):
            coll.remove(x)


def mat(name, rgb):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1.0)
    b.inputs["Roughness"].default_value = 0.85
    return m


def finish(ob, material, coll):
    ob.data.materials.append(material)
    try:
        coll.objects.link(ob)
    except RuntimeError:
        pass
    return ob


def main():
    wipe()
    piece_coll = bpy.data.collections.new("CJ_Attire2_Pieces")
    bpy.context.scene.collection.children.link(piece_coll)

    m_dark = mat("CJ_A2_Dark", (0.08, 0.08, 0.10))      # placeholder dark
    m_gray = mat("CJ_A2_Gray", (0.45, 0.45, 0.48))      # placeholder gray
    m_gold = mat("CJ_A2_Gold", (0.85, 0.62, 0.15))      # placeholder accent

    # ---- domino mask: curved band (front arc of a torus), open eye slots ----
    bpy.ops.mesh.primitive_torus_add(
        major_radius=HEAD_R * 1.04, minor_radius=0.016,
        major_segments=40, minor_segments=12,
        location=(0, 0, EYE_Z))
    band = bpy.context.active_object
    band.name = "CJ_A2_DominoMask"
    # keep the front arc across the face, drop the back half
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    import bmesh
    bm = bmesh.from_edit_mesh(band.data)
    for v in bm.verts:
        if v.co.y < 0.01:  # behind the face plane -> remove
            v.select = True
    bmesh.update_edit_mesh(band.data)
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    band.scale = (1.0, 1.0, 1.5)  # taller band
    bpy.ops.object.transform_apply(scale=True)
    finish(band, m_dark, piece_coll)
    # eye-slot rims (gold): two small flattened tori where the white eyes sit
    for sx in (-1, 1):
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.027, minor_radius=0.006,
            major_segments=20, minor_segments=8,
            location=(sx * 0.043, 0.080, EYE_Z), rotation=(math.pi / 2, 0, 0))
        rim = bpy.context.active_object
        rim.name = "CJ_A2_EyeRim_%s" % ("L" if sx < 0 else "R")
        rim.scale = (1.25, 0.8, 1.0)
        bpy.ops.object.transform_apply(scale=True)
        finish(rim, m_gold, piece_coll)

    # ---- earless cowl: sphere shell, open face ----
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=32, ring_count=20, radius=HEAD_R * 1.12,
        location=(0, -0.008, EYE_Z + 0.015))
    cowl = bpy.context.active_object
    cowl.name = "CJ_A2_Cowl"
    cowl.scale = (1.0, 1.05, 1.18)
    bpy.ops.object.transform_apply(scale=True)
    # open the face: delete verts in front (y > 0.03) and below eye line front
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    me = cowl.data
    import bmesh
    bm = bmesh.from_edit_mesh(me)
    for v in bm.verts:
        w = cowl.matrix_world @ v.co
        if w.y > 0.035 and w.z < EYE_Z + 0.045:
            v.select = True
    bmesh.update_edit_mesh(me)
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')
    # solidify-lite: no modifier kept (staging) — note in PULL-LOG
    finish(cowl, m_dark, piece_coll)

    # ---- cape: single flat sheet, tapered, shoulder-hung ----
    import bmesh
    me = bpy.data.meshes.new("CJ_A2_CapeMesh")
    bm = bmesh.new()
    rows, cols = 8, 6
    top_w, bot_w, length = 0.16, 0.30, 0.55
    verts = []
    for r in range(rows):
        t = r / (rows - 1)
        w = top_w + (bot_w - top_w) * t
        z = (EYE_Z - 0.06) - length * t
        y = -HEAD_R * 1.05 - 0.02 * t
        row = []
        for c in range(cols):
            s = c / (cols - 1) - 0.5
            v = bm.verts.new((s * w, y, z))
            row.append(v)
        verts.append(row)
    for r in range(rows - 1):
        for c in range(cols - 1):
            bm.faces.new((verts[r][c], verts[r][c + 1],
                          verts[r + 1][c + 1], verts[r + 1][c]))
    bm.to_mesh(me)
    bm.free()
    cape = bpy.data.objects.new("CJ_A2_Cape", me)
    bpy.context.scene.collection.objects.link(cape)
    finish(cape, m_dark, piece_coll)

    # ---- gauntlets: flared forearm cylinders ----
    for sx, tag in ((-1, "L"), (1, "R")):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=20, radius=0.045, depth=0.22,
            location=(sx * 0.21, 0, 0.45))
        g = bpy.context.active_object
        g.name = "CJ_A2_Gauntlet_%s" % tag
        # flare the top: scale top verts
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bm = bmesh.from_edit_mesh(g.data)
        for v in bm.verts:
            if v.co.z > 0.09:
                v.co.x *= 1.35
                v.co.y *= 1.35
        bmesh.update_edit_mesh(g.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        finish(g, m_gray, piece_coll)

    # ---- boots: shin cylinder + foot box ----
    for sx, tag in ((-1, "L"), (1, "R")):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16, radius=0.05, depth=0.30,
            location=(sx * 0.09, 0, 0.17))
        b = bpy.context.active_object
        b.name = "CJ_A2_Boot_%s" % tag
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(b.data)
        for v in bm.verts:
            if v.co.z < -0.13:
                v.co.y += 0.09  # foot forward
                v.co.z = -0.15
        bmesh.update_edit_mesh(b.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        finish(b, m_dark, piece_coll)

    # ---- belt: band + pouches ----
    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.13, minor_radius=0.022,
        major_segments=28, minor_segments=10,
        location=(0, 0, 0.52))
    belt = bpy.context.active_object
    belt.name = "CJ_A2_Belt"
    finish(belt, m_gold, piece_coll)
    for i, px in enumerate((-0.07, -0.024, 0.024, 0.07)):
        bpy.ops.mesh.primitive_cube_add(size=0.045, location=(px, 0.125, 0.52))
        p = bpy.context.active_object
        p.name = "CJ_A2_Pouch_%d" % i
        p.scale = (1.0, 0.6, 1.2)
        bpy.ops.object.transform_apply(scale=True)
        finish(p, m_dark, piece_coll)

    # ---- emblem blank: diamond shield ----
    bpy.ops.mesh.primitive_cube_add(size=0.09, location=(0, 0.10, 0.68),
                                    rotation=(0, 0, math.pi / 4))
    emb = bpy.context.active_object
    emb.name = "CJ_A2_Emblem"
    emb.scale = (1.0, 0.25, 1.3)
    bpy.ops.object.transform_apply(scale=True)
    finish(emb, m_gold, piece_coll)

    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print("SAVED", OUT, "| pieces:",
          len(piece_coll.objects))


if __name__ == "__main__":
    main()
