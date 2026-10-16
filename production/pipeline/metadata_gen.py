#!/usr/bin/env python3
"""
metadata_gen.py — Title/description/tags generator for show episodes.

Reads a small show config + episode info, emits a YouTube-ready metadata JSON
sidecar (consumed by youtube_upload.py) plus chapter markers from a beat list.

Usage:
    python3 metadata_gen.py --show cape-jones --ep 1 --title "Pilot Title" \
        --beats beats_ep01.json --out EP01_meta.json
    python3 metadata_gen.py --show cape-jones --ep 1 --title "Pilot Title" --out EP01_meta.json

beats JSON: [{"t": "0:00", "label": "Cold open"}, {"t": "0:42", "label": "Title card"}, ...]
"""
import argparse
import json
import os

SHOWS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shows.json")


def load_shows():
    if os.path.exists(SHOWS_FILE):
        with open(SHOWS_FILE) as f:
            return json.load(f)
    return {}


HOOK_TEMPLATES = [
    "{title} | {show} EP{ep:02d}",
    "{show} EP{ep:02d} — {title}",
    "{title} — {show} (EP{ep:02d}) FULL EPISODE",
]

DESC_TEMPLATE = """{hook}

{synopsis}

🎬 {show} — Episode {ep}: "{title}"
{credits}

⏱️ CHAPTERS
{chapters}

🔔 New episodes every {schedule}. Subscribe for more 2D animated chaos.

{hashtags}
"""


def build_hashtags(tags, extra=()):
    base = [t for t in tags if t]
    return " ".join("#" + t.replace(" ", "").replace("-", "") for t in (base + list(extra)))


def fmt_chapters(beats):
    if not beats:
        return "00:00 Start"
    return "\n".join(f"{b['t']} {b['label']}" for b in beats)


def main():
    ap = argparse.ArgumentParser(description="Generate YouTube metadata sidecar for an episode.")
    ap.add_argument("--show", required=True, help="Show key in shows.json")
    ap.add_argument("--ep", type=int, required=True)
    ap.add_argument("--title", required=True, help="Episode title")
    ap.add_argument("--synopsis", default="", help="1-2 sentence episode synopsis")
    ap.add_argument("--beats", help="JSON file of chapter beats")
    ap.add_argument("--tags", help="Comma-separated extra tags")
    ap.add_argument("--hook", type=int, default=0, help="Title template index")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    shows = load_shows()
    show = shows.get(args.show, {})
    sname = show.get("name", args.show)
    tags = list(show.get("tags", [])) + (args.tags.split(",") if args.tags else [])
    tags = [t.strip() for t in tags if t.strip()]

    beats = []
    if args.beats:
        with open(args.beats) as f:
            beats = json.load(f)

    title = HOOK_TEMPLATES[args.hook % len(HOOK_TEMPLATES)].format(
        title=args.title, show=sname, ep=args.ep)[:100]
    description = DESC_TEMPLATE.format(
        hook=args.synopsis or args.title,
        synopsis=args.synopsis,
        show=sname, ep=args.ep, title=args.title,
        credits=show.get("credits", ""),
        chapters=fmt_chapters(beats),
        schedule=show.get("schedule", "week"),
        hashtags=build_hashtags(tags[:15]),
    ).strip()

    meta = {
        "show": args.show,
        "episode": args.ep,
        "title": title,
        "description": description,
        "tags": tags[:500],
        "chapters": beats,
    }
    with open(args.out, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"wrote {args.out}\ntitle: {title}\n{len(tags)} tags, {len(beats)} chapters")


if __name__ == "__main__":
    main()
