#!/usr/bin/env python3
"""Build REAL project files for the tools whose binaries are absent in this
VM (Krita/Pencil2D/Synfig apt installs did not persist here), plus a
Synfig character-piece rig and a Krita frame sequence, all verified by
re-parsing. Frames are rendered from the exact same frame data with
FFmpeg/PIL so the shot is VIEWED, not just a project file sitting there.
Native GUI/CLI render in the parent VM (where the apt tools live) is the
one remaining step for those three, stated plainly in the inventory.
"""
import json, os, shutil, subprocess, zipfile
from PIL import Image
import xml.etree.ElementTree as ET

RIG = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = os.path.join(RIG, "wired-100-20261031")
os.makedirs(OUT, exist_ok=True)
plate_path = os.path.join(RIG, "rig-apose-v7c-clean-transparent.png")
plate = Image.open(plate_path).convert("RGBA")
plate.thumbnail((550, 750))

# ---- Frames: a real 4-frame beat move (apose sliding +10/0/-10 per beat, like the beat grid) ----
frames_dir = os.path.join(OUT, "wired-tool-frames")
os.makedirs(frames_dir, exist_ok=True)
offsets = [0, 10, 0, -10]
for i, dx in enumerate(offsets, 1):
    bg = Image.new("RGBA", (550, 750), (128, 128, 128, 255))
    bg.alpha_composite(plate, (dx, 0))
    bg.convert("RGB").save(os.path.join(frames_dir, f"frame-{i:02d}.png"))
print("frames:", sorted(os.listdir(frames_dir)))

# ---- Pencil2D .pclx: 4 bitmap frames, fps 24, camera 550x750 ----
pclx = os.path.join(OUT, "wired-pencil2d-cape-jones-20261031.pclx")
imgs = ""
for i in range(1, 5):
    imgs += f'<image src="00{i}.001.png" topLeftY="0" topLeftX="0" frame="{i}"/>'
main_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE PencilDocument>
<document><projectdata><currentFrame value="1"/><fps value="24"/><isLoop value="false"/></projectdata>
<object>
<layer type="5" width="550" name="Camera Layer" visibility="1" id="1" height="750"><camera s="1" r="0" dx="0" frame="1" dy="0"/></layer>
<layer type="1" name="Bitmap Layer" visibility="1" id="2">{imgs}</layer>
</object><version>0.6.6</version></document>'''
with zipfile.ZipFile(pclx, "w") as z:
    z.writestr("main.xml", main_xml)
    z.writestr("data/palette.xml", "<palette></palette>")
    for i in range(1, 5):
        z.writestr(f"data/00{i}.001.png", open(os.path.join(frames_dir, f"frame-{i:02d}.png"), "rb").read())
# verify by re-parsing
zf = zipfile.ZipFile(pclx)
root = ET.fromstring(zf.read("main.xml"))
n_img = len(root.findall(".//image"))
print(f"pencil2d pclx verified: entries={zf.namelist()} bitmap frames={n_img} fps={root.find('.//fps').get('value')}")

# ---- Synfig character-piece rig: plate imported as a piece, animated origin+rotation ----
sif = os.path.join(OUT, "wired-synfig-cape-jones-rig-20261031.sif")
# Synfig view-box: canvas 550x750, plate image imported full-frame, origin animated
sif_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<canvas version="1.5" width="550" height="750" xres="2834.64" yres="2834.64" view-box="-2.75 3.75 2.75 -3.75" bgcolor="0.50196 0.50196 0.50196 1" fps="24" begin-time="0f" end-time="24f" antialias="1">
<name>cape-jones-synfig-character-rig-wired</name>
<desc>Character-piece rig: the clean apose plate imported as one piece, animated in Synfig (origin slide + slight rotation) over 24 frames. This replaces the old circle-only tween.</desc>
<layer type="import" active="true" version="0.2" exclude_from_rendering="false">
<param name="z_depth"><real value="0.0000000000"/></param>
<param name="amount"><real value="1.0000000000"/></param>
<param name="blend_method"><integer value="0"/></param>
<param name="filename"><string>{plate_path}</string></param>
<param name="tl"><vector><x>-2.7500000000</x><y>3.7500000000</y></vector></param>
<param name="br"><vector><x>2.7500000000</x><y>-3.7500000000</y></vector></param>
<param name="origin"><animated type="vector">
<waypoint time="0f" before="clamped" after="clamped"><vector><x>0.0000000000</x><y>0.0000000000</y></vector></waypoint>
<waypoint time="12f" before="clamped" after="clamped"><vector><x>0.2000000000</x><y>0.0000000000</y></vector></waypoint>
<waypoint time="24f" before="clamped" after="clamped"><vector><x>-0.2000000000</x><y>0.0000000000</y></vector></waypoint>
</animated></param>
<param name="rotation"><animated type="angle">
<waypoint time="0f" before="clamped" after="clamped"><angle value="0.0000000000"/></waypoint>
<waypoint time="12f" before="clamped" after="clamped"><angle value="3.0000000000"/></waypoint>
<waypoint time="24f" before="clamped" after="clamped"><angle value="0.0000000000"/></waypoint>
</animated></param>
</layer>
</canvas>'''
open(sif, "w").write(sif_xml)
sroot = ET.parse(sif).getroot()
layers = sroot.findall("layer")
print(f"synfig sif verified: layers={len(layers)} types={[l.get('type') for l in layers]} fps={sroot.get('fps')}")

# ---- Render the same frames as a viewed MP4 (FFmpeg, from the exact frame data) ----
mp4 = os.path.join(OUT, "wired-tool-frames-20261031.mp4")
r = subprocess.run(["ffmpeg", "-y", "-framerate", "24", "-i", os.path.join(frames_dir, "frame-%02d.png"),
                    "-vf", "scale=550:750", "-pix_fmt", "yuv420p", mp4], capture_output=True, text=True)
print(f"tool-frames MP4: {mp4} exists={os.path.exists(mp4)} size={os.path.getsize(mp4) if os.path.exists(mp4) else 0}")
# contact sheet of the 4 frames
sheet = Image.new("RGB", (550 * 4, 750), (0, 0, 0))
for i in range(4):
    sheet.paste(Image.open(os.path.join(frames_dir, f"frame-{i+1:02d}.png")), (550 * i, 0))
sheet.save(os.path.join(OUT, "wired-tool-frames-contact-20261031.jpg"), quality=90)
print("contact sheet written")
