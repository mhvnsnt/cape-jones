#!/usr/bin/env python3
"""
obs_scene_json.py — generate an OBS scene-collection JSON with overlay slots.

Builds a ready-to-import OBS scene collection containing browser-source
slots wired to a self-hosted overlay server (e.g. Fanfare in
../streaming/fanfare, or Overlayr). Import via OBS:
    Scene Collection -> Import, select the generated .json

Usage:
    python3 obs_scene_json.py --base http://localhost:3000 --out show_scenes.json

Creates scenes:
    SHOW LIVE   — alerts + chat + goal + event ticker browser sources
    SHOW BRB    — fullscreen BRB text + alerts
    SHOW ENDING — ending slate + goal

Overlay URLs assume Fanfare paths (/overlay/alertbox etc.). Pass --urls
overrides as "name=url" to point at anything else.
"""
import argparse
import json

W, H = 1920, 1080

# Fanfare (../streaming/fanfare) overlay paths; override with --url name=url
DEFAULT_URLS = {
    "Alerts": "/overlay/alertbox",
    "Chat": "/overlay/chatbox?max=12",
    "Goal": "/overlay/goal",
    "Events": "/overlay/eventlist?max=10",
}


def browser_source(name, url, x, y, w, h):
    return {
        "name": name,
        "id": "browser_source",
        "versioned_id": "browser_source",
        "settings": {
            "url": url,
            "width": w,
            "height": h,
            "fps": 30,
            "shutdown": False,
            "reroute_audio": False,
        },
        "mixers": 255,
        "sync": 0,
        "flags": 0,
        "volume": 1.0,
        "enabled": True,
        "pos": {"x": float(x), "y": float(y)},
        "scale": {"x": 1.0, "y": 1.0},
        "crop": {"top": 0, "right": 0, "bottom": 0, "left": 0},
    }


def text_source(name, text, x, y, size):
    return {
        "name": name,
        "id": "text_gdiplus_v2",
        "versioned_id": "text_gdiplus_v2",
        "settings": {"text": text, "font": {"size": size},
                     "color1": 4294967295, "bk_color": 0, "bk_opacity": 0},
        "mixers": 255,
        "sync": 0,
        "flags": 0,
        "volume": 1.0,
        "enabled": True,
        "pos": {"x": float(x), "y": float(y)},
        "scale": {"x": 1.0, "y": 1.0},
        "crop": {"top": 0, "right": 0, "bottom": 0, "left": 0},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://localhost:3000",
                    help="overlay server base URL")
    ap.add_argument("--out", default="show_scenes.json")
    ap.add_argument("--url", action="append", default=[],
                    help='"Alerts=/overlay/alertbox" style overrides')
    args = ap.parse_args()

    urls = {k: args.base + v for k, v in DEFAULT_URLS.items()}
    for item in args.url:
        name, path = item.split("=", 1)
        urls[name.strip()] = path.strip()

    scenes = [
        {"name": "SHOW LIVE", "settings": {"items": [
            browser_source("Alerts", urls["Alerts"], 560, 740, 800, 300),
            browser_source("Chat", urls["Chat"], 1480, 80, 400, 900),
            browser_source("Goal", urls["Goal"], 60, 60, 500, 120),
            browser_source("Events", urls["Events"], 60, 200, 400, 300),
        ]}},
        {"name": "SHOW BRB", "settings": {"items": [
            text_source("BRB Text", "BE RIGHT BACK", 640, 480, 96),
            browser_source("Alerts", urls["Alerts"], 560, 740, 800, 300),
        ]}},
        {"name": "SHOW ENDING", "settings": {"items": [
            text_source("Thanks Text", "THANKS FOR WATCHING", 560, 480, 72),
            browser_source("Goal", urls["Goal"], 710, 600, 500, 120),
        ]}},
    ]

    collection = {
        "name": "Show Stream",
        "current_scene": "SHOW LIVE",
        "current_program_scene": "SHOW LIVE",
        "scene_order": [{"name": s["name"]} for s in scenes],
        "sources": scenes,
        "transitions": [],
        "transition_duration": 300,
    }

    with open(args.out, "w") as f:
        json.dump(collection, f, indent=2)
    print(f"Wrote {args.out} ({len(scenes)} scenes)")
    print("Import: OBS -> Scene Collection -> Import")


if __name__ == "__main__":
    main()
