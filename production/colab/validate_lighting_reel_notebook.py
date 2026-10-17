#!/usr/bin/env python3
"""Static preflight for the Cape Jones lighting-reel Colab notebook.

This intentionally does not import Blender or claim that the .blend file renders.
It catches notebook JSON damage and regressions in the safety guards reviewed in
PR #26 before a human runs the notebook in Colab.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / "production" / "colab" / "cape_jones_lighting_reel_colab.ipynb"

REQUIRED_SNIPPETS = {
    "material lookup": "bpy.data.materials.get",
    "material failure diagnostic": "LEDStripMat",
    "scene light lookup": "RoomLight",
    "segment boundary protection": "SEG - 1",
    "render process status check": "returncode",
    "output existence check": "os.path.exists",
}

FORBIDDEN_SNIPPETS = {
    "account identifier should not be embedded": "drive.google.com/drive/u/",
}


def main() -> int:
    if not NOTEBOOK.is_file():
        print(f"FAIL: notebook not found: {NOTEBOOK}", file=sys.stderr)
        return 2

    try:
        notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: notebook is unreadable or invalid JSON: {exc}", file=sys.stderr)
        return 2

    cells = notebook.get("cells")
    if not isinstance(cells, list):
        print("FAIL: notebook has no valid cells list", file=sys.stderr)
        return 2

    source_parts = []
    for cell in cells:
        if cell.get("cell_type") == "code":
            source = cell.get("source", [])
            source_parts.append("".join(source) if isinstance(source, list) else str(source))
    source = "\n".join(source_parts)

    failures = []
    for label, snippet in REQUIRED_SNIPPETS.items():
        if snippet not in source:
            failures.append(f"missing required guard ({label}): {snippet}")

    for label, snippet in FORBIDDEN_SNIPPETS.items():
        if snippet in source:
            failures.append(f"forbidden content ({label}): {snippet}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    print(f"PASS: notebook JSON valid ({len(cells)} cells)")
    print(f"PASS: {len(REQUIRED_SNIPPETS)} renderer guard markers present")
    print(f"PASS: {len(FORBIDDEN_SNIPPETS)} privacy regression checks passed")
    print("NOTE: static preflight only; Blender/Colab rendering remains unverified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
