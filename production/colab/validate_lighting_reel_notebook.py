#!/usr/bin/env python3
"""Static preflight for the Cape Jones lighting-reel Colab notebook.

This intentionally does not import Blender or claim that the .blend file renders.
It catches notebook JSON damage and regressions in the safety guards reviewed in
PR #26 before a human runs the notebook in Colab.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / "production" / "colab" / "cape_jones_lighting_reel_colab.ipynb"
LED_CONTROLLER = ROOT / "production" / "pipeline" / "led_controller.py"

REQUIRED_SNIPPETS = {
    "material lookup": "bpy.data.materials.get",
    "material failure diagnostic": "Lighting reel setup failed",
    "scene light lookup": "bpy.data.objects.get",
    "segment boundary protection": "SEG - 1",
    "shell pipeline failure propagation": "pipefail",
    "output existence and size verification": "os.path.getsize(output) == 0",
    "metadata probe failure propagation": "check=True",
}

FORBIDDEN_SNIPPETS = {
    "account-specific Drive URL should not be embedded": "drive.google.com/drive/u/",
}


def assigned_value(tree: ast.AST, name: str) -> ast.AST | None:
    """Return the value node assigned to a top-level variable, without executing it."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in node.targets
        ):
            return node.value
    return None


def main() -> int:
    if not LED_CONTROLLER.is_file():
        print(f"FAIL: canonical LED controller not found: {LED_CONTROLLER}", file=sys.stderr)
        return 2

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
            cell_source = cell.get("source", [])
            source_parts.append(
                "".join(cell_source) if isinstance(cell_source, list) else str(cell_source)
            )
    source = "\n".join(source_parts)

    failures = []
    for label, snippet in REQUIRED_SNIPPETS.items():
        if snippet not in source:
            failures.append(f"missing required guard ({label}): {snippet}")

    for label, snippet in FORBIDDEN_SNIPPETS.items():
        if snippet in source:
            failures.append(f"forbidden content ({label}): {snippet}")

    # Parse the canonical controller and the embedded Blender script as syntax
    # trees. Never import or execute either file during static validation.
    try:
        controller_tree = ast.parse(LED_CONTROLLER.read_text(encoding="utf-8"))
        canonical_node = assigned_value(controller_tree, "PRESETS")
        if not isinstance(canonical_node, ast.Dict):
            raise ValueError("controller PRESETS must be a literal dictionary")
        canonical_names = {
            key.value for key in canonical_node.keys if isinstance(key, ast.Constant)
            and isinstance(key.value, str)
        }

        blender_script = next(
            (part for part in source_parts if "PRESETS = [" in part), None
        )
        if blender_script is None:
            raise ValueError("embedded Blender render script or PRESETS list not found")
        # The first line is the Jupyter %%writefile cell magic, not Python syntax.
        script_lines = blender_script.splitlines()
        if script_lines and script_lines[0].startswith("%%writefile"):
            script_lines = script_lines[1:]
        script_tree = ast.parse("\n".join(script_lines))
        subset_node = assigned_value(script_tree, "PRESETS")
        if not isinstance(subset_node, ast.List):
            raise ValueError("embedded render PRESETS must be a literal list")
        subset_names = {
            item.elts[0].value
            for item in subset_node.elts
            if isinstance(item, ast.Tuple) and item.elts
            and isinstance(item.elts[0], ast.Constant)
            and isinstance(item.elts[0].value, str)
        }
        if not subset_names:
            raise ValueError("could not extract any named render presets")
        unknown_names = sorted(subset_names - canonical_names)
        if unknown_names:
            failures.append(
                "render preset names missing from canonical LED controller: "
                + ", ".join(unknown_names)
            )
        if len(canonical_names) != 15:
            failures.append(
                f"expected 15 canonical LED presets, found {len(canonical_names)}"
            )
    except (OSError, SyntaxError, ValueError) as exc:
        failures.append(f"could not validate canonical preset alignment: {exc}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    print(f"PASS: notebook JSON valid ({len(cells)} cells)")
    print(f"PASS: {len(REQUIRED_SNIPPETS)} renderer guard markers present")
    print(f"PASS: {len(FORBIDDEN_SNIPPETS)} privacy regression checks passed")
    print("PASS: embedded preview preset names match the 15-preset canonical controller")
    print("NOTE: static preflight only; Blender/Colab rendering remains unverified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
