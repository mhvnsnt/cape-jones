#!/usr/bin/env python3
"""
podcast_feed.py — RSS 2.0 + iTunes podcast feed generator for a show.

Takes a JSON manifest of episodes (video/audio files already hosted at public
URLs) and emits a valid podcast RSS feed. Useful for distributing a show as a
video podcast feed (RSS readers, Podcast Addict, etc.).

Usage:
    python3 podcast_feed.py feed.json --out feed.xml

feed.json:
{
  "title": "Cape Jones",
  "description": "2D animated series ...",
  "link": "https://example.com/cape-jones",
  "image": "https://example.com/cover.jpg",
  "language": "en-us",
  "author": "Real",
  "category": "TV & Film",
  "explicit": false,
  "episodes": [
    {"title": "EP01 — Pilot", "description": "...", "url": "https://.../ep01.mp4",
     "size": 12345678, "type": "video/mp4", "date": "2026-10-20", "duration": "5:00",
     "guid": "cape-jones-ep01"}
  ]
}
"""
import argparse
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

ITUNES = "http://www.itunes.com/dtds/podcast-1.0.dtd"


def feed(manifest):
    rss = ET.Element("rss", version="2.0")
    rss.set("xmlns:itunes", ITUNES)
    ch = ET.SubElement(rss, "channel")
    for tag, key in [("title", "title"), ("description", "description"),
                     ("link", "link"), ("language", "language")]:
        ET.SubElement(ch, tag).text = manifest.get(key, "")
    ET.SubElement(ch, "itunes:author").text = manifest.get("author", "")
    ET.SubElement(ch, "itunes:explicit").text = (
        "yes" if manifest.get("explicit") else "no")
    if manifest.get("image"):
        ET.SubElement(ch, "itunes:image", href=manifest["image"])
    ET.SubElement(ch, "itunes:category", text=manifest.get("category", "TV & Film"))
    for ep in manifest.get("episodes", []):
        item = ET.SubElement(ch, "item")
        ET.SubElement(item, "title").text = ep["title"]
        ET.SubElement(item, "description").text = ep.get("description", "")
        ET.SubElement(item, "guid").text = ep.get("guid", ep["url"])
        ET.SubElement(item, "pubDate").text = ep.get("date", "")
        ET.SubElement(item, "enclosure", url=ep["url"],
                      length=str(ep.get("size", 0)), type=ep.get("type", "video/mp4"))
        ET.SubElement(item, "itunes:duration").text = ep.get("duration", "")
        ET.SubElement(item, "itunes:explicit").text = (
            "yes" if ep.get("explicit", manifest.get("explicit")) else "no")
    return minidom.parseString(ET.tostring(rss)).toprettyxml(indent="  ")


def main():
    ap = argparse.ArgumentParser(description="Generate a podcast RSS feed from a manifest.")
    ap.add_argument("manifest", help="feed.json manifest")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    with open(args.manifest) as f:
        manifest = json.load(f)
    with open(args.out, "w") as f:
        f.write(feed(manifest))
    print(f"wrote {args.out} ({len(manifest.get('episodes', []))} episodes)")


if __name__ == "__main__":
    main()
