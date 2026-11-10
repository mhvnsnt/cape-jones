#!/usr/bin/env python3
"""
merch_qr.py — QR code generator for merch / show links.

Generates print-ready QR codes (PNG + SVG) for merch cards, posters, and
video end-cards. Uses the `segno` library (BSD-3-Clause, cloned in
../merch/segno). Install with: pip install segno

Usage:
    python3 merch_qr.py --out qr_out
    # edits the LINKS dict below, or pass --link "Label=https://..." pairs

Example:
    python3 merch_qr.py --out qr_out \
        --link "Merch Store=https://printful.com/..." \
        --link "Tip Page=http://localhost:3000/tip"
"""
import argparse
import os
import re
import sys

# Edit these for the show's actual links
LINKS = {
    "Merch Store": "https://example.com/merch",
    "Tip Page": "https://example.com/tip",
    "Discord": "https://discord.gg/example",
    "Latest Episode": "https://youtube.com/@example",
}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="qr_out", help="output directory")
    ap.add_argument("--link", action="append", default=[],
                    help='"Label=https://..." (repeatable)')
    ap.add_argument("--scale", type=int, default=10,
                    help="modules per pixel multiplier (default 10)")
    ap.add_argument("--border", type=int, default=4,
                    help="quiet-zone border in modules (default 4)")
    args = ap.parse_args()

    try:
        import segno
    except ImportError:
        sys.exit("segno not installed: pip install segno "
                 "(or see ../merch/segno)")

    links = dict(LINKS)
    for item in args.link:
        if "=" not in item:
            sys.exit(f'bad --link {item!r}; use "Label=https://..."')
        label, url = item.split("=", 1)
        links[label.strip()] = url.strip()

    os.makedirs(args.out, exist_ok=True)
    for label, url in links.items():
        name = slug(label)
        qr = segno.make(url, error="h")  # high error correction: survives logos
        qr.save(os.path.join(args.out, f"{name}.png"),
                scale=args.scale, border=args.border)
        qr.save(os.path.join(args.out, f"{name}.svg"),
                scale=args.scale, border=args.border)
        print(f"{label:>20} -> {name}.png / {name}.svg")

    print(f"\nDone: {len(links)} QR codes in {args.out}/")


if __name__ == "__main__":
    main()
