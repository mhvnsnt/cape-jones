#!/usr/bin/env python3
"""TOOL 4 — FLA/XFL + JSFL library reader (rank #4).
An XFL file is a ZIP: DOMDocument.xml holds the timeline, LIBRARY holds
symbols. A binary .fla cannot be parsed here (needs Animate); this tool
says so plainly instead of faking it. It also reads our existing .jsfl
rig builders, which ARE the library metadata for this rig (STACK order
= layer order, PIVOTS = registration points).
Usage:
  tool4_xfl_jsfl.py xfl <file.xfl>   -> symbols + timeline layers
  tool4_xfl_jsfl.py jsfl <file.jsfl> -> STACK + PIVOTS parsed
  tool4_xfl_jsfl.py make-test-xfl <out.xfl>  -> synthetic XFL from sliced/
"""
import sys, os, json, zipfile, re
import xml.etree.ElementTree as ET

def parse_xfl(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        dom_name = next((n for n in names if n.endswith("DOMDocument.xml")), None)
        if not dom_name:
            return {"tool": "xfl_jsfl", "error": "no DOMDocument.xml in this archive — not an XFL"}
        root = ET.fromstring(z.read(dom_name))
        symbols, layers = [], []
        for el in root.iter():
            tag = el.tag.split("}")[-1]
            if tag == "DOMSymbolItem":
                symbols.append({"name": el.get("name"), "itemID": el.get("itemID")})
            if tag == "DOMLayer":
                layers.append(el.get("name"))
        return {"tool": "xfl_jsfl", "file": path, "entries": len(names),
                "symbols": symbols, "timeline_layers": layers}

def parse_jsfl(path):
    txt = open(path).read()
    stack = re.search(r"var STACK = \[(.*?)\];", txt, re.S)
    pivots = re.search(r"var PIVOTS = \{(.*?)\n  \};", txt, re.S)
    files = re.findall(r'"([^"]+\.png)"', stack.group(1)) if stack else []
    return {"tool": "xfl_jsfl", "file": path, "stack_layer_order_bottom_to_top": files,
            "pivots_found": bool(pivots),
            "note": "STACK in the .jsfl is bottom-to-top; Animate timeline lists top first"}

def make_test_xfl(out):
    import io
    tmpl = sorted(f for f in os.listdir(os.path.expanduser("~/workspace/cape-jones-rig/sliced"))
                  if f.endswith(".png"))
    symbols = "".join(
        f'<DOMSymbolItem xmlns="http://ns.adobe.com/xfl/2008/" name="{t[:-4]}" itemID="{i:08x}"/>'
        for i, t in enumerate(tmpl))
    dom = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<DOMDocument xmlns="http://ns.adobe.com/xfl/2008/" width="1920" height="1080" frameRate="24">'
           '<timelines><DOMTimeline name="Scene 1"><layers>'
           '<DOMLayer name="CapeJonesRig" color="#FF0000" current="true" isSelected="true"/>'
           '</layers></DOMTimeline></timelines>'
           f'<symbols>{symbols}</symbols></DOMDocument>')
    with zipfile.ZipFile(out, "w") as z:
        z.writestr("DOMDocument.xml", dom)
        z.writestr("LIBRARY/placeholder.txt", "synthetic test XFL built from sliced/ names only")
    return {"tool": "xfl_jsfl", "test_xfl": out, "symbols_written": len(tmpl)}

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "xfl":
        print(json.dumps(parse_xfl(sys.argv[2]), indent=2))
    elif cmd == "jsfl":
        print(json.dumps(parse_jsfl(sys.argv[2]), indent=2))
    elif cmd == "make-test-xfl":
        print(json.dumps(make_test_xfl(sys.argv[2]), indent=2))
    else:
        print("usage: xfl|jsfl|make-test-xfl", file=sys.stderr); sys.exit(2)
