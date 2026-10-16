#!/usr/bin/env python3
"""fountain_to_beats.py — Fountain screenplay -> beat sheet (JSON + Markdown).

Parses a .fountain file into a per-scene beat breakdown:
slugline, location, beats (action/dialogue), speakers, estimated duration.

    python3 fountain_to_beats.py script.fountain [--wpm 150] [--out beats/]

Outputs <basename>_beats.json and <basename>_beats.md next to --out (or cwd).
Under 200 lines, stdlib only.
"""
import argparse, json, os, re, sys

SLUG_RE = re.compile(r"^(INT|EXT|EST|INT\.?/|EXT\.?/|I/E)[\.\s]", re.I)
TRANS_RE = re.compile(r"^\s*(CUT TO|SMASH CUT|DISSOLVE|FADE (IN|OUT)|MATCH CUT|JUMP CUT)[:.]?\s*$", re.I)
CENTER_RE = re.compile(r"^\s*>.*<\s*$")


def parse_fountain(text):
    scenes, cur = [], None

    def new_scene(slug):
        return {"slugline": slug, "location": slug, "beats": [], "speakers": [],
                "duration_est_s": 0.0}

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if SLUG_RE.match(line.strip()) or line.strip().startswith(".") and len(line.strip()) > 2:
            if cur:
                scenes.append(cur)
            cur = new_scene(line.strip().lstrip("."))
            continue
        if cur is None:
            continue  # title page lines before first slugline
        s = line.strip()
        if TRANS_RE.match(s) or TRANS_RE.match(s.lstrip(">")) or CENTER_RE.match(line):
            continue
        if s.startswith("!"):
            cur["beats"].append({"type": "action", "text": s[1:].strip()})
        elif s.startswith("#"):
            continue  # section/synopsis markers
        elif s.startswith(">") and not s.endswith("<"):
            sp = s[1:].strip()
            cur["beats"].append({"type": "dialogue", "speaker": sp, "text": ""})
            if sp and sp not in cur["speakers"]:
                cur["speakers"].append(sp)
        elif s.startswith("@"):
            sp = s[1:].strip()
            cur["beats"].append({"type": "dialogue", "speaker": sp, "text": ""})
            if sp and sp not in cur["speakers"]:
                cur["speakers"].append(sp)
        elif cur["beats"] and cur["beats"][-1]["type"] == "dialogue" and not cur["beats"][-1]["text"]:
            cur["beats"][-1]["text"] = s
        elif s.isupper() and len(s) < 40 and not s.endswith("."):
            # probable character cue
            cur["beats"].append({"type": "dialogue", "speaker": s, "text": ""})
            if s not in cur["speakers"]:
                cur["speakers"].append(s)
        else:
            cur["beats"].append({"type": "action", "text": s})
    if cur:
        scenes.append(cur)
    return scenes


def estimate(scenes, wpm):
    words_total = 0
    for sc in scenes:
        words = sum(len(b.get("text", "").split()) for b in sc["beats"])
        words_total += words
        # dialogue ~ reading pace, action ~ 2x pacing, plus 5s per scene pad
        sc["duration_est_s"] = round(words / wpm * 60 * 1.25 + 5, 1)
        sc["word_count"] = words
    return words_total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fountain", help=".fountain input file")
    ap.add_argument("--wpm", type=float, default=150)
    ap.add_argument("--out", default=".", help="output dir")
    args = ap.parse_args()
    with open(args.fountain, encoding="utf-8") as f:
        text = f.read()
    scenes = parse_fountain(text)
    total_words = estimate(scenes, args.wpm)
    base = os.path.splitext(os.path.basename(args.fountain))[0]
    os.makedirs(args.out, exist_ok=True)
    total = round(sum(s["duration_est_s"] for s in scenes), 1)

    jpath = os.path.join(args.out, base + "_beats.json")
    with open(jpath, "w", encoding="utf-8") as f:
        json.dump({"source": args.fountain, "scenes": len(scenes),
                   "total_words": total_words, "total_est_s": total,
                   "beats": scenes}, f, indent=2, ensure_ascii=False)

    mpath = os.path.join(args.out, base + "_beats.md")
    with open(mpath, "w", encoding="utf-8") as f:
        f.write(f"# Beat sheet: {base}\n{len(scenes)} scenes, ~{total:.0f}s est. "
                f"(@{args.wpm:g} wpm), {total_words} words\n\n")
        for i, sc in enumerate(scenes, 1):
            f.write(f"## {i}. {sc['slugline']} — {sc['duration_est_s']}s\n")
            if sc["speakers"]:
                f.write("Speakers: " + ", ".join(sc["speakers"]) + "\n")
            for j, b in enumerate(sc["beats"], 1):
                if b["type"] == "action":
                    f.write(f"- beat {j} (action): {b['text'][:140]}\n")
                else:
                    f.write(f"- beat {j} ({b['speaker']}): {b['text'][:140]}\n")
            f.write("\n")
    print(f"scenes={len(scenes)} words={total_words} est={total:.1f}s")
    print("json:", jpath)
    print("md:", mpath)


if __name__ == "__main__":
    sys.exit(main())
