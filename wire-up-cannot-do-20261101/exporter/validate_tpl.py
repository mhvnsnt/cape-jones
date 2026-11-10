"""Round-trip validator for our own .tpl prototype. Own code.
Unzips, parses the .xstage XML, checks every element drawing exists,
checks palette .plt and .plt.json agree, checks timings cover 48 frames.
This proves OUR package is self-consistent. It does NOT prove Harmony
can open it - only a real Harmony binary can prove that."""
import zipfile, json, sys, os
from xml.etree import ElementTree as ET
tpl = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    "~/workspace/cape-jones-rig/wire-up-cannot-do-20261101/exporter/CapeJonesToon.tpl")
tmp = "/tmp/cjtoon_tpl_check"
import shutil
if os.path.exists(tmp): shutil.rmtree(tmp)
os.makedirs(tmp)
with zipfile.ZipFile(tpl) as z:
    names = z.namelist(); z.extractall(tmp)
root = ET.parse(os.path.join(tmp, "CapeJonesToon.xstage")).getroot()
els = [e.get("name") for e in root.find("elements")]
missing = [f"elements/{n}/drawing-1.png" for n in els
           if not os.path.exists(os.path.join(tmp, f"elements/{n}/drawing-1.png"))]
frames = len(root.find("timings"))
plt_lines = [l for l in open(os.path.join(tmp, "palette-library/CapeJones.plt")).read().splitlines()
             if l and not l.startswith("#")]
plt_json = json.load(open(os.path.join(tmp, "palette-library/CapeJones.plt.json")))
ok = (not missing and frames == 48 and len(plt_lines) == len(plt_json)
      and all(f"{c['name']} {c['rgba'][0]} {c['rgba'][1]} {c['rgba'][2]} {c['rgba'][3]}" in plt_lines
              for c in plt_json))
print(json.dumps({"tpl": tpl, "files": len(names), "elements": els,
                  "missing_drawings": missing, "timing_frames": frames,
                  "palette_lines": len(plt_lines), "palette_json": len(plt_json),
                  "self_consistent": ok}, indent=1))
sys.exit(0 if ok else 1)
