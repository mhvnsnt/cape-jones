import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import importlib.util
spec = importlib.util.spec_from_file_location("cg", os.path.join(os.path.dirname(__file__), "convert_grok_sheets.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
from pathlib import Path
shard, nshards = int(sys.argv[1]), int(sys.argv[2])
files = sorted([p for p in mod.SRC.rglob("*") if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png")])
todo = []
for src in files:
    rel = src.relative_to(mod.SRC)
    if rel.parts[0] == "backgrounds":
        continue
    dst = mod.OUT/(rel.parts[0] if len(rel.parts) > 1 else "root")/(src.stem + ".png")
    if dst.exists():
        continue
    todo.append((src, rel, dst))
todo = todo[shard::nshards]
print(f"shard {shard} todo {len(todo)}", flush=True)
for src, rel, dst in todo:
    try:
        m = mod.convert(src, dst)
        print("converted", rel, f"{m['alpha_frac']:.3f}", flush=True)
    except Exception as e:
        print("FAILED", rel, e, flush=True)
