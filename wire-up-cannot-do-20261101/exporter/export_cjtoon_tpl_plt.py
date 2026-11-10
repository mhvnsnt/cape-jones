"""OWN .tpl / .plt exporter prototype for Cape Jones Toon.
Own code, written from public Toon Boom documentation only:
- A Harmony template is a mini-scene: a folder with elements, palette-library,
  and a scene file (.xstage, XML), per docs.toonboom.com Harmony 24 Advanced,
  'About the File Structure in Harmony Stand Alone'.
- A palette is an individual *.plt file stored in palette-library, per
  Harmony 21 Advanced Palette Operations docs.
- Drawings in Harmony are normally .tvg vector files; this prototype does NOT
  claim to write .tvg. It writes bitmap PNG drawings (Harmony's bitmap import
  path) and labels that plainly. Until a real Harmony binary opens this
  package, it is a PROTOTYPE, not a verified Harmony import.
- No Toon Boom code was copied, no binary was used, no licence was bypassed.
What it exports today (verified by validate_tpl.py, round-trip):
  CapeJonesToon.tpl  = zip of a mini-scene folder containing:
    CapeJonesToon.xstage  (XML: resolution 1100x1500, 24fps, pegs, elements,
                           timings for the 48-frame clip, palette list)
    elements/<layer>/drawing-1.png  (whole/joint-cut Cape Jones PNGs)
    palette-library/CapeJones.plt  (prototype palette, see format note below)
    palette-library/CapeJones.plt.json (machine-readable colour list, same colours)
    PALETTE_LIST, scene.elementTable, README-PROTOTYPE.txt
Palette format note: Toon Boom does not publish a .plt binary spec in its
public docs. Our .plt is therefore a plain-text, line-based palette:
  first line: # CJTOON-PLT-PROTOTYPE-1 (not a Toon Boom format claim)
  then: name R G B A per colour, sampled from the actual Cape Jones PNGs.
  Harmony reading this exact file is UNVERIFIED and must be tested in real
  Harmony before anyone claims import works. The .json companion is the
  machine-readable copy that our own tools round-trip today.
Usage: python3 export_cjtoon_tpl_plt.py [--out DIR]
"""
import os, sys, json, zipfile, shutil
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from PIL import Image
from collections import Counter

ROOT = os.path.expanduser("~/workspace/cape-jones-rig")
OUT = sys.argv[sys.argv.index("--out")+1] if "--out" in sys.argv else os.path.join(ROOT, "wire-up-cannot-do-20261101/exporter")
STAGE = os.path.join(OUT, "CapeJonesToon-scene")
LAYERS = [
    ("CapeBack", "sliced/Cape_Back_Main.png"),
    ("LegBack", "cut-limbs-v7/Leg_Back_Upper.png"),
    ("LegFront", "cut-limbs-v7/Leg_Front_Upper.png"),
    ("ArmBack", "cut-limbs-v7/Arm_Back_Upper.png"),
    ("Pelvis", "sliced/Pelvis.png"),
    ("Torso", "sliced/Torso_Chest.png"),
    ("CapeCollar", "sliced/Cape_Collar.png"),
    ("Neck", "sliced/Neck.png"),
    ("Head", "sliced/Head_Front.png"),
    ("ArmFront", "cut-limbs-v7/Arm_Front_Upper.png"),
]
PEGS = [
    ("Root", None), ("Pelvis-P", "Root"), ("Torso-P", "Pelvis-P"),
    ("Neck-P", "Torso-P"), ("Head-P", "Neck-P"),
    ("Cape-P", "Root"), ("CapeCollar-P", "Torso-P"),
    ("Arm1-Upper-P", "Torso-P"), ("Arm1-Forearm-P", "Arm1-Upper-P"),
    ("Arm1-Hand-P", "Arm1-Forearm-P"),
    ("Arm2-Upper-P", "Torso-P"), ("Arm2-Forearm-P", "Arm2-Upper-P"),
    ("Arm2-Hand-P", "Arm2-Forearm-P"),
    ("Leg1-Thigh-P", "Pelvis-P"), ("Leg1-Knee-P", "Leg1-Thigh-P"),
    ("Leg2-Thigh-P", "Pelvis-P"), ("Leg2-Knee-P", "Leg2-Thigh-P"),
]

def sample_palette(paths, n=12):
    cnt = Counter()
    for p in paths:
        im = Image.open(p).convert("RGBA")
        im.thumbnail((200, 200))
        for px in im.getdata():
            if px[3] > 200:
                cnt[px] += 1
    # keep distinct, non-grey-dominant colours: take top colours, dedupe by rounding
    colours = []
    for (r, g, b, a), _ in cnt.most_common(200):
        key = (r//16*16, g//16*16, b//16*16)
        if key not in [c[:3] for c in colours]:
            colours.append((r, g, b, a))
        if len(colours) >= n:
            break
    # Names are generic on purpose: the sampler returns the most frequent
    # opaque colours, and assigning semantic names by order would mislabel
    # them (e.g. white labelled purple). Real semantic colours in this set:
    # 254,254,254 = suit white, 0,0,0 = outline, 90,39,114 = cowl purple.
    return [(f"Colour{i+1:02d}", c) for i, c in enumerate(colours)]

def main():
    if os.path.exists(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(os.path.join(STAGE, "elements"), exist_ok=True)
    os.makedirs(os.path.join(STAGE, "palette-library"), exist_ok=True)
    os.makedirs(os.path.join(STAGE, "frames"), exist_ok=True)
    element_files = []
    for layer, rel in LAYERS:
        src = os.path.join(ROOT, rel)
        d = os.path.join(STAGE, "elements", layer)
        os.makedirs(d, exist_ok=True)
        dst = os.path.join(d, "drawing-1.png")
        shutil.copyfile(src, dst)
        element_files.append((layer, dst))
    palette = sample_palette([os.path.join(ROOT, rel) for _, rel in LAYERS])
    with open(os.path.join(STAGE, "palette-library", "CapeJones.plt"), "w") as f:
        f.write("# CJTOON-PLT-PROTOTYPE-1\n")
        f.write("# Prototype palette only. Toon Boom .plt binary format is not\n")
        f.write("# publicly specified; Harmony reading this file is UNVERIFIED.\n")
        for name, (r, g, b, a) in palette:
            f.write(f"{name} {r} {g} {b} {a}\n")
    with open(os.path.join(STAGE, "palette-library", "CapeJones.plt.json"), "w") as f:
        json.dump([{"name": n, "rgba": list(c)} for n, c in palette], f, indent=1)
    with open(os.path.join(STAGE, "PALETTE_LIST"), "w") as f:
        f.write("palette-library/CapeJones.plt\n")
    with open(os.path.join(STAGE, "scene.elementTable"), "w") as f:
        for layer, _ in element_files:
            f.write(f"{layer}\n")
    # .xstage XML, own structure mirroring documented scene fields
    scene = Element("xstage", {"version": "prototype-1", "name": "CapeJonesToon",
                               "resolution": "1100x1500", "fps": "24", "frames": "48"})
    SubElement(scene, "note").text = ("PROTOTYPE ONLY. Built from public docs, not from "
        "Toon Boom code. Harmony import is UNVERIFIED until a real Harmony binary opens it.")
    pegs_el = SubElement(scene, "pegs")
    for name, parent in PEGS:
        SubElement(pegs_el, "peg", {"name": name, "parent": parent or ""})
    els = SubElement(scene, "elements")
    for layer, _ in element_files:
        SubElement(els, "element", {"name": layer, "drawing": f"elements/{layer}/drawing-1.png"})
    timings = SubElement(scene, "timings")
    for frame in range(1, 49):
        SubElement(timings, "frame", {"number": str(frame), "exposure": "drawing-1"})
    pal = SubElement(scene, "palettes")
    SubElement(pal, "palette", {"file": "palette-library/CapeJones.plt"})
    xml = minidom.parseString(tostring(scene)).toprettyxml(indent="  ")
    with open(os.path.join(STAGE, "CapeJonesToon.xstage"), "w") as f:
        f.write(xml)
    with open(os.path.join(STAGE, "README-PROTOTYPE.txt"), "w") as f:
        f.write("Cape Jones Toon template prototype, 2026-11-01.\n"
                "This is a mini-scene folder (template = mini-scene, per public docs).\n"
                "Bitmap PNG drawings, NOT .tvg vectors. Palette .plt is a prototype\n"
                "text format, NOT a verified Toon Boom binary. Do NOT claim Harmony\n"
                "import works until a real Harmony binary opens it and renders it.\n")
    tpl = os.path.join(OUT, "CapeJonesToon.tpl")
    with zipfile.ZipFile(tpl, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(STAGE):
            for fn in files:
                full = os.path.join(root, fn)
                z.write(full, os.path.relpath(full, STAGE))
    print(json.dumps({"tpl": tpl, "tpl_bytes": os.path.getsize(tpl),
                      "layers": len(element_files), "palette_colours": len(palette),
                      "palette": palette}, indent=1))

if __name__ == "__main__":
    main()
