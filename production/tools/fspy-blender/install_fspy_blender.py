#!/usr/bin/env python3
"""Install the vendored fSpy-Blender add-on into a Blender installation.

Builds a zip of the sibling fspy_blender/ package and copies it into the
Blender addons directory, then prints the enable step.

Usage:
    install_fspy_blender.py --blender /path/to/blender-install
    install_fspy_blender.py --blender ~/workspace/tools/blender/blender-4.0.2-linux-x64 --dry-run

The --blender path is the Blender install dir (the one containing the
`blender` executable). The script resolves the versioned addons dir from the
executable's own version string (e.g. 4.0/scripts/addons).
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ADDON_SRC = os.path.join(HERE, "fspy_blender")


def blender_version(blender_dir):
    exe = os.path.join(blender_dir, "blender")
    if not os.path.isfile(exe):
        raise SystemExit(f"no blender executable at {exe}")
    out = subprocess.run([exe, "--version"], capture_output=True, text=True,
                         timeout=60).stdout
    m = re.search(r"Blender (\d+)\.(\d+)", out)
    if not m:
        raise SystemExit(f"could not parse version from: {out.strip()}")
    return f"{m.group(1)}.{m.group(2)}"


def build_zip(dest_dir):
    zip_path = os.path.join(dest_dir, "fSpy-Blender.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(ADDON_SRC):
            for f in files:
                if f.endswith((".pyc", ".pyo")) or "__pycache__" in root:
                    continue
                full = os.path.join(root, f)
                arc = os.path.join("fspy_blender",
                                   os.path.relpath(full, ADDON_SRC))
                zf.write(full, arc)
    return zip_path


def main():
    ap = argparse.ArgumentParser(
        description="Install vendored fSpy-Blender add-on into Blender.")
    ap.add_argument("--blender", required=True,
                    help="Blender install dir (contains the blender executable)")
    ap.add_argument("--dry-run", action="store_true",
                    help="build the zip and print the target dir, do not copy")
    args = ap.parse_args()

    if not os.path.isdir(ADDON_SRC):
        raise SystemExit(f"addon source missing: {ADDON_SRC}")

    blender_dir = os.path.expanduser(args.blender)
    version = blender_version(blender_dir)
    addons_dir = os.path.join(blender_dir, version, "scripts", "addons")
    print(f"Blender {version} -> addons dir: {addons_dir}")

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = build_zip(tmp)
        print(f"built {zip_path} ({os.path.getsize(zip_path)} bytes)")
        if args.dry_run:
            print("dry-run: not copying")
            return 0
        os.makedirs(addons_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(addons_dir)
        print(f"installed fspy_blender into {addons_dir}")

    print("Next: Blender -> Edit -> Preferences -> Add-ons -> "
          "enable 'Import-Export: fSpy importer'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
