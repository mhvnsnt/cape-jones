"""Eevee free-GPU notebook builder + local simplified Eevee attempt script.
This file writes:
- build_eevee_v4.py: Eevee version of the separate-volume scene, half-res
  550x750, volumetric tile 8, samples 1, for a local xvfb attempt. If it
  times out, that is measured, not hidden.
- shafts-eevee-free-gpu.ipynb: a ready-to-run notebook for Kaggle free GPU
  (first, Mars FMMG fmmg.mars@gmail.com only — if Kaggle rejects that login,
  STOP and report, do NOT try another account) then Colab free GPU.
  The notebook downloads Blender 5.2.3, runs build_cycles_v4_separate.py
  and the Eevee variant on GPU, and saves outputs. It needs a Mars
  sign-in step in the browser — a subagent cannot sign in, so execution
  on Kaggle/Colab is the one step that must be handed to the parent/
  Mars, with this exact notebook file. No paid run, no credentials in
  the notebook, no Cloudflare/Backblaze claimed as GPU (they are
  storage/CDN, not compute; they are NOT used as GPU here).
"""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
eevee = r'''
import bpy, math, random
random.seed(31)
OUT = '/home/hatch/workspace/cape-jones-rig/shafts-fix-100-20261031/shafts-eevee-v4-20261031.png'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_EEVEE'
try:
    sc.eevee.use_volumetric_shadows = False
    sc.eevee.volumetric_tile_size = '8'
    sc.eevee.taa_render_samples = 1
    print("EEVEE_SETTINGS_OK")
except Exception as e:
    print("EEVEE_SETTINGS_FAIL", e)
sc.render.resolution_x = 550; sc.render.resolution_y = 750
sc.render.resolution_percentage = 100
sc.render.film_transparent = False; sc.render.filepath = OUT
w = bpy.data.worlds.new("W"); w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.012, 0.03, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
sc.world = w
bpy.ops.object.camera_add(location=(0, -15, 3.2), rotation=(math.radians(90), 0, 0))
sc.camera = bpy.context.object
COLS = [-3.0, -1.5, 0.0, 1.5, 3.0]
for i, gx in enumerate(COLS):
    bpy.ops.mesh.primitive_cube_add(size=2, location=(gx, 0, 3.0))
    vol = bpy.context.object; vol.name = f"VolumeCol_{i}"; vol.scale = (0.55, 3.0, 4.5)
    mat = bpy.data.materials.new(f"VolCol_{i}"); mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    pv = nt.nodes.new("ShaderNodeVolumePrincipled")
    pv.inputs["Density"].default_value = 0.35; pv.inputs["Anisotropy"].default_value = 0.7
    pv.inputs["Color"].default_value = (1.0, 0.85, 0.55, 1)
    outn = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(pv.outputs[0], outn.inputs["Volume"])
    vol.data.materials.append(mat)
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -1.5))
floor = bpy.context.object; floor.name = "FloorPools"
fm = bpy.data.materials.new("FloorMat"); fm.use_nodes = True
fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.25, 0.22, 0.18, 1)
floor.data.materials.append(fm)
for i, gx in enumerate(COLS):
    bpy.ops.object.empty_add(location=(gx, 0, -1.5)); target = bpy.context.object
    bpy.ops.object.light_add(type='SPOT', location=(gx, 0, 9.0))
    s = bpy.context.object; s.data.energy = 10000; s.data.color = (1.0, 0.88, 0.62)
    s.data.spot_size = math.radians(18); s.data.spot_blend = 0.3
    c = s.constraints.new('TRACK_TO'); c.target = target; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
bpy.ops.render.render(write_still=True)
print("EEVEE_V4_DONE", OUT)
'''
open(os.path.join(BASE, 'build_eevee_v4.py'), 'w').write(eevee)
nb = {
 "cells": [
  {"cell_type": "markdown", "metadata": {}, "source": ["# Shafts v4 — free GPU render (Kaggle first, then Colab)\n", "FREE ONLY. No paid run. Kaggle: sign in as Mars FMMG fmmg.mars@gmail.com ONLY — if Kaggle rejects that login, STOP and report, do NOT try another account. Colab free GPU second. Cloudflare/Backblaze are storage/CDN, NOT GPU, and are not used as compute here.\n", "This notebook downloads Blender 5.2.3, copies build_cycles_v4_separate.py and build_eevee_v4.py (same folder as this notebook in the repo), renders both, and lists the output PNGs."]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["import os, subprocess, sys, urllib.request, tarfile\n", "url='https://download.blender.org/release/Blender5.2/blender-5.2.3-linux-x64.tar.xz'\n", "urllib.request.urlretrieve(url, 'blender.tar.xz')\n", "import shutil\n", "shutil.unpack_archive('blender.tar.xz', '.')\n", "print('blender ready')\n", "!nvidia-smi -L 2>/dev/null || echo 'no nvidia-smi (CPU fallback still renders Cycles; Eevee needs GPU/GL)'\n"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["!./blender-5.2.3-linux-x64/blender --background --python build_cycles_v4_separate.py 2>&1 | tail -5\n", "!ls -lh shafts-only-cycles-v4-separate-20261031.png\n"]},
  {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": ["!./blender-5.2.3-linux-x64/blender --background --python build_eevee_v4.py 2>&1 | tail -5\n", "!ls -lh shafts-eevee-v4-20261031.png\n"]},
 ],
 "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python", "version": "3.10"}},
 "nbformat": 4, "nbformat_minor": 5}
json.dump(nb, open(os.path.join(BASE, 'shafts-eevee-free-gpu.ipynb'), 'w'), indent=1)
print("wrote eevee script + notebook")
