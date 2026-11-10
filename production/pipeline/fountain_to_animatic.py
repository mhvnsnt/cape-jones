#!/usr/bin/env python3
"""fountain_to_animatic.py -- .fountain screenplay -> timed animatic MP4 (title-card cut).

Bridges scriptwriting and boarding: before a single panel is drawn, this turns
a Fountain script into a watchable timing skeleton -- one title card per scene
with the slugline, key action/dialogue, and an estimated duration derived from
word count (~150 wpm dialogue). Drop the result next to build_animatic.py
(which needs real board images) to feel the episode's pacing first.

Self-contained Fountain parser (no dependencies): title page, scene headings,
action, character cues (+ (V.O.)-style extensions), parentheticals, dialogue,
transitions, centered text, sections.

Usage:
  python3 fountain_to_animatic.py script.fountain -o animatic.mp4
  python3 fountain_to_animatic.py script.fountain -o animatic.mp4 --audio voices.mp3
  python3 fountain_to_animatic.py script.fountain -o animatic.mp4 --wpm 130 --fps 24

Pairs with:
  ../script-tools/fountain_to_cues.py  (.fountain -> dialogue cue sheet)
  build_animatic.py                    (board images + timing + audio -> animatic)
"""
import argparse
import math
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, H = 1280, 720
BG = (16, 16, 22)
FG = (235, 235, 240)
DIM = (150, 150, 160)
ACCENT = (255, 176, 32)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def is_scene_heading(line):
    s = line.strip()
    if s.startswith(".") and not s.startswith(".."):
        return True
    return bool(re.match(r"^(INT|EXT|EST|INT\.?/EXT\.?|INT\.?\s*/\s*EXT\.?)[\.\s]", s))


def is_transition(line):
    s = line.strip()
    if s.startswith(">"):
        return True
    return s.endswith("TO:") and s == s.upper() and len(s) < 40


def is_character(line):
    s = line.strip()
    if not s or len(s) > 60:
        return False
    if s.startswith("@"):
        return True
    if not s[0].isupper():
        return False
    core = re.sub(r"\s*\(.*?\)\s*", "", s)
    if not core:
        return False
    letters = [c for c in core if c.isalpha()]
    if not letters:
        return False
    upper = sum(1 for c in letters if c.isupper())
    return upper / len(letters) > 0.7 and not is_scene_heading(s) and not is_transition(s)


def is_parenthetical(line):
    s = line.strip()
    return s.startswith("(") and s.endswith(")")


def parse_fountain(path):
    """Return (title_meta dict, [scene dicts]). Scene: heading, blocks=[(kind,text)]."""
    with open(path, encoding="utf-8-sig") as f:
        raw = f.read()
    lines = raw.split("\n")

    # Title page: Key: value lines at the very top before first blank-line+content
    meta = {}
    i = 0
    while i < len(lines):
        m = re.match(r"^([A-Za-z][A-Za-z0-9 _-]*):\s*(.*)$", lines[i])
        if m and i < 40:
            meta[m.group(1).strip()] = m.group(2).strip()
            i += 1
            continue
        if lines[i].strip() == "" and i < 40:
            i += 1
            continue
        break
    # Only keep title page if we actually saw keys before content
    body = lines[i:]

    scenes = []
    cur = {"heading": "UNTITLED", "blocks": []}
    in_dialogue = False

    def push_scene():
        if cur["blocks"] or cur["heading"] != "UNTITLED":
            scenes.append(cur)

    for line in body:
        s = line.strip()
        if not s:
            in_dialogue = False
            continue
        if s.startswith("#"):
            continue  # section/synopsis marker
        if s.startswith("=") and s.endswith("=") and len(s) > 2:
            continue  # synopsis
        if is_scene_heading(s):
            push_scene()
            cur = {"heading": s.lstrip(".").strip(), "blocks": []}
            in_dialogue = False
        elif is_transition(s):
            cur["blocks"].append(("transition", s.lstrip(">").strip()))
            in_dialogue = False
        elif is_character(s):
            name = s.lstrip("@").strip()
            cur["blocks"].append(("character", name))
            in_dialogue = True
        elif in_dialogue and is_parenthetical(s):
            cur["blocks"].append(("parenthetical", s))
        elif in_dialogue:
            cur["blocks"].append(("dialogue", s))
        else:
            if s.startswith(">") and s.endswith("<"):
                cur["blocks"].append(("centered", s[1:-1].strip()))
            else:
                cur["blocks"].append(("action", s))
                in_dialogue = False
    push_scene()
    # drop the leading empty scene if file started with a heading-less preamble
    if scenes and scenes[0]["heading"] == "UNTITLED" and not scenes[0]["blocks"]:
        scenes.pop(0)
    return meta, scenes


def scene_duration(scene, wpm):
    words = 0
    for kind, text in scene["blocks"]:
        n = len(text.split())
        if kind == "dialogue":
            words += n
        elif kind == "action":
            words += n * 0.35  # action reads faster / gets less screen time
    return max(2.0, words / (wpm / 60.0) + 1.0)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def render_card(scene, idx, n, duration, meta):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    fb, fr, fs = font(FONT_BOLD, 54), font(FONT_REG, 30), font(FONT_REG, 24)

    # top bar
    d.rectangle([0, 0, W, 130], fill=(24, 24, 32))
    d.rectangle([0, 130, W, 134], fill=ACCENT)
    d.text((48, 26), f"SCENE {idx + 1}/{n}", font=font(FONT_BOLD, 28), fill=ACCENT)
    d.text((48, 62), scene["heading"][:64], font=fb, fill=FG)
    d.text((W - 48 - d.textlength(f"{duration:.1f}s", font=fr), 62),
           f"{duration:.1f}s", font=fr, fill=DIM)

    y = 180
    shown = 0
    for kind, text in scene["blocks"]:
        if shown >= 8 or y > H - 90:
            break
        if kind == "character":
            y += 10
            d.text((80, y), text.upper(), font=font(FONT_BOLD, 30), fill=ACCENT)
            y += 44
        elif kind == "dialogue":
            for ln in wrap(d, text, fr, W - 220)[:2]:
                d.text((110, y), ln, font=fr, fill=FG)
                y += 38
            shown += 1
        elif kind == "action":
            for ln in wrap(d, text, fr, W - 160)[:3]:
                d.text((80, y), ln, font=fr, fill=(200, 200, 208))
                y += 38
            shown += 1
        elif kind == "parenthetical":
            d.text((110, y), text, font=fs, fill=DIM)
            y += 32
        elif kind == "transition":
            d.text((W - 80 - d.textlength(text, font=fs), y), text, font=fs, fill=DIM)
            y += 36
    # footer
    title = meta.get("Title", "")
    if title:
        d.text((48, H - 56), title[:80], font=fs, fill=DIM)
    d.text((W - 48 - d.textlength("fountain_to_animatic", font=fs), H - 56),
           "fountain_to_animatic", font=fs, fill=(90, 90, 100))
    return img


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAILED: {' '.join(cmd)}\n{r.stderr[-2000:]}", file=sys.stderr)
        sys.exit(1)
    return r


def main():
    ap = argparse.ArgumentParser(description=".fountain -> timed title-card animatic MP4")
    ap.add_argument("script", help=".fountain file")
    ap.add_argument("-o", "--out", required=True, help="output mp4")
    ap.add_argument("--audio", help="voice/music track laid under the animatic")
    ap.add_argument("--wpm", type=float, default=150, help="dialogue words per minute")
    ap.add_argument("--fps", type=float, default=24)
    ap.add_argument("--size", default="1280x720")
    ap.add_argument("--keep-cards", help="directory to keep per-scene card PNGs")
    args = ap.parse_args()

    global W, H
    W, H = map(int, args.size.split("x"))

    meta, scenes = parse_fountain(args.script)
    if not scenes:
        print("No scenes found in script.", file=sys.stderr)
        sys.exit(1)

    tmp = tempfile.mkdtemp(prefix="fountain_animatic_")
    cards_dir = args.keep_cards or tmp
    os.makedirs(cards_dir, exist_ok=True)

    durations = [scene_duration(s, args.wpm) for s in scenes]
    total = sum(durations)
    print(f"{len(scenes)} scenes, est. total {total:.1f}s @ {args.wpm} wpm")

    segs = []
    for i, (scene, dur) in enumerate(zip(scenes, durations)):
        card = render_card(scene, i, len(scenes), dur, meta)
        path = os.path.join(cards_dir, f"card_{i:03d}.png")
        card.save(path)
        seg = os.path.join(tmp, f"seg_{i:03d}.mp4")
        run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(args.fps),
             "-i", path, "-t", f"{dur:.2f}", "-vf", f"scale={W}:{H}",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(args.fps), seg])
        segs.append(seg)

    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")
    video = os.path.join(tmp, "video.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", video])

    if args.audio:
        # pad/trim audio to animatic length
        run(["ffmpeg", "-y", "-v", "error", "-i", video, "-i", args.audio,
             "-filter_complex",
             f"[1:a]apad=whole_dur={total:.2f},atrim=0:{total:.2f}[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy",
             "-c:a", "aac", "-b:a", "160k", "-shortest", args.out])
    else:
        run(["ffmpeg", "-y", "-v", "error", "-i", video, "-c", "copy", args.out])

    print(f"Wrote {args.out} ({total:.1f}s)")
    if not args.keep_cards:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
