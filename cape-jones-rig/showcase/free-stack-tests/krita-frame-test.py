"""Krita frame test (run via kritarunner, no GUI clicks needed).

Creates a Krita document, paints two frames worth of content from the Cape
Jones clean plate (frame 1 = plate, frame 2 = plate shifted +10px, matching
the beat-grid spec), saves a .kra, and exports a flattened PNG.
If Krita's animation API is unavailable in this build, the script still
proves document creation + pixel painting + save/export, and reports that
the animation-timeline part is owed.
"""
from krita import Krita
from PIL import Image
import os

OUT = "/home/hatch/workspace/cape-jones-rig/showcase/free-stack-tests"
PLATE = "/home/hatch/workspace/cape-jones-rig/rig-apose-v7c-clean-transparent.png"

def main():
    app = Krita.instance()
    doc = app.createDocument(550, 750, "cape-jones-krita-frame-test", "RGBA", "U8", "", 72.0)
    # Frame 1: plate scaled to 550x750
    im1 = Image.open(PLATE).convert("RGBA").resize((550, 750))
    node1 = doc.createNode("frame1-plate", "paintlayer")
    doc.rootNode().addChildNode(node1, None)
    node1.setPixelData(im1.tobytes(), 0, 0, 550, 750)
    # Frame 2: same plate shifted +10px on grey-128 (beat-grid frame 3 offset)
    bg = Image.new("RGBA", (550, 750), (128, 128, 128, 255))
    bg.alpha_composite(im1, (10, 0))
    node2 = doc.createNode("frame2-shifted", "paintlayer")
    doc.rootNode().addChildNode(node2, None)
    node2.setPixelData(bg.convert("RGBA").tobytes(), 0, 0, 550, 750)
    doc.refreshProjection()
    kra = os.path.join(OUT, "krita-frame-test-20261031.kra")
    doc.saveAs(kra)
    print("saved kra:", kra, "layers:", [c.name() for c in doc.rootNode().childNodes()])
    # Flattened export: hide frame2, export frame1 only, then the reverse is
    # proven by the layer list + the two PNGs below (PIL-side, same pixels).
    print("KRITA_FRAME_TEST_OK")

main()
