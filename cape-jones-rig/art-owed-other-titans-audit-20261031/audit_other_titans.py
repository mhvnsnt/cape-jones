"""Other Titans mouths pull attempt + production-coordinator owed audit, 2026-10-31.

Reads ONLY local files:
  - robin-eyes-100-20261031/tt-entries.json (970-entry manifest of
    repo mhvnsnt/cn-gigaleak-teen-titans release teen-titans-complete-v1)
  - superhero-mouths-20261031/mouth-library-20261031.json (Robin library, for contrast)
  - shots-endtoend-20261031/shots-endtoend-20261031.json (rim/bleed for CJ-05/06/26)
Makes NO network call, downloads nothing, extracts nothing from the archive.
That is deliberate: the prior local extraction mechanism (authenticated range
reads from the split ZIP) was flagged by a safety check, and no replacement
download path is used here. This script only enumerates, from the local
manifest, exactly which files a parent/root route or Mars-supplied files
would need to provide before any mouth extraction can start.
"""
import csv, json, os
from pathlib import Path

ROOT = Path.home() / "workspace" / "cape-jones-rig"
OUT = ROOT / "art-owed-other-titans-audit-20261031"
MANIFEST = ROOT / "robin-eyes-100-20261031" / "tt-entries.json"

def main():
    entries = json.load(open(MANIFEST))
    names = [(e["name"], e) for e in entries]
    assert len(names) == 970, len(names)

    def has(n, pat):
        return pat.lower() in n.lower()

    # --- Part 1: other Titans expression targets ---
    # Colour EXPRES = the exact analogue of the Robin files the mouth library
    # used (RBEXPRES01..05_CA_DCTTAS.EPS, colour). B&W CAb variants are listed
    # as alternates, not primary targets.
    targets = []
    for char, prefix in [("Cyborg", "CYEXPRES"), ("Starfire", "SFEXPRES"),
                         ("Raven", "RVEXPRES"), ("Beast Boy", "BBEXPRES")]:
        for name, e in names:
            if prefix in name and "EXPRES" in name and "_CA_" in name:
                targets.append({
                    "character": char, "archive_path": name,
                    "file": name.split("/")[-1],
                    "variant": "colour",
                    "uncompressed_bytes": e.get("usize"),
                    "compressed_bytes": e.get("csize"),
                    "local_status": "NOT ON DISC - no source file, no render",
                })
    targets.sort(key=lambda r: (r["character"], r["file"]))
    # Slade: 0 EXPRES sheets exist. Its only face-bearing sheets are the
    # SLA01-03 model/character-art sheets (non-Icon).
    slade_faces = []
    for name, e in names:
        if "Slade" in name and "Icon" not in name:
            slade_faces.append({
                "character": "Slade", "archive_path": name,
                "file": name.split("/")[-1], "variant": "face-sheet (no EXPRES sheet exists)",
                "uncompressed_bytes": e.get("usize"),
                "compressed_bytes": e.get("csize"),
                "local_status": "NOT ON DISC - no source file, no render",
            })
    slade_faces.sort(key=lambda r: r["file"])

    with open(OUT / "other-titans-expression-targets-20261031.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(targets[0].keys()) + ["note"])
        w.writeheader()
        for r in targets:
            w.writerow({**r, "note": "Primary mouth source, colour EXPRES analogue of Robin RBEXPRES"})
        for r in slade_faces:
            w.writerow({**r, "note": "Slade has NO expression sheet; mouth would have to come from a face sheet, unproven"})
    json.dump({"colour_expres_targets": targets, "slade_face_sheet_alternates": slade_faces,
               "counts": {"colour_expres_total": len(targets),
                          "by_character": {c: sum(1 for r in targets if r["character"] == c)
                                           for c in ["Cyborg", "Starfire", "Raven", "Beast Boy"]},
                          "slade_face_sheets": len(slade_faces),
                          "slade_expres_sheets": 0}},
              open(OUT / "other-titans-expression-targets-20261031.json", "w"), indent=1)

    # --- Part 2: owed-items tracker (excludes sibling jobs) ---
    owed = [
        # id, source dir, item, count, unit, status, unblocker
        ("A-01", "shots-endtoend-20261031", "Mars approval of end-to-end shots", 30, "shots", "OWED - decision", "Mars views each shot (0/1 each)"),
        ("A-02", "storyboards-animatic-20261031", "Mars approval of poses/panels/animatic", 72, "files (37 poses + 30 panels + 5 animatic)", "OWED - decision", "Mars views each (0/1 each)"),
        ("A-03", "true-masters-20261031", "Mars approval of true masters", 4, "masters", "OWED - decision", "Mars views each (0/1 each)"),
        ("A-04", "rig-chains-20261031", "Mars approval of chain/successor videos", 9, "videos", "OWED - decision", "Mars views each (0/1 each)"),
        ("A-05", "roomscale-eyes-20261031", "Mars approval: room-scale table + eye verdicts (seated pick RESOLVED 2026-11-01 00:01 CDT: 2.8x LOCKED, 2.3x REJECTED - do not re-ask)", 2, "decisions remaining (seated pick decided)", "OWED - decision (partially resolved)", "Mars approval of table + verdicts 0/1; seated uses locked 2.8x"),
        ("A-06", "storyboards-animatic-20261031", "Room scale lock: 3.0x vs older 2.5x (seated 2.3x)", 1, "decision", "OWED - decision", "Mars confirms which lock supersedes"),
        ("A-07", "rig-chains-20261031", "move-jump-to-shimmy successor re-key", 1, "successor", "BLOCKED - do not build silently", "Mars says re-key (with key sequence) or drop it"),
        ("A-08", "true-masters-20261031", "Single hand-drawn torso-twist sheet", 1, "sheet", "CONDITIONAL - only if Mars rejects twist composite nits", "Mars rejection of composite + artist pass"),
        ("A-09", "roomscale-eyes-20261031", "Canonical room pictures - SUPERSEDED 2026-11-01 00:00 CDT: Mars supplied canonical-room-20261101.jpg (2048x1152); re-measure + CJ-23 chair now in a separate RUNNING workstream", 1, "picture (supplied)", "SUPPLIED - sibling workstream running, NOT owed here", "That workstream's re-measured scale + CJ-23 chair approvals (0/1 each)"),
        ("A-10", "roomscale-eyes-20261031", "Chair-back-at-waist clarification", 1, "clarification", "OWED - decision", "Mars clarifies chair-back position"),
        ("A-11", "roomscale-eyes-20261031", "Full-resolution per-piece inspection (largest-piece + numeric QC done)", 2854, "pieces", "OWED - inspection, not claimed", "A full-res pass, if Mars wants it"),
        ("A-12", "wiring-100-20261031", "Neutral-rim ruling for QC-FAIL shots CJ-05, CJ-06, CJ-26", 3, "shots under 1 ruling", "OWED - decision (ruling sheet built here)", "Mars ruling on neutral key + white/grey rim"),
        ("A-13", "wiring-100-20261031", "Pose-pending tracker rows (apose plate only, pose NOT invented)", 9, "shots: CJ-01, CJ-02, CJ-04, CJ-11, CJ-15, CJ-17, CJ-18, CJ-20, CJ-27", "OWED - tracked, not invented", "Clean pose plates / final renders (CJ-15 + CJ-18 via sibling jobs)"),
        ("A-14", "shots-endtoend-20261031", "Figure-matched lighting lane (per-line shading/tinting + 4 shafts presets, NOT merged into shots)", 1, "workstream", "OWED - separate lane", "That lane's own approval 0/1"),
        ("A-15", "rig-chains-20261031", "Flex 28px dip (no dip parameter in chain builder)", 1, "builder parameter", "NAMED FIX - needs go-ahead, not silently applied", "Mars wants dip applied; builder change + re-render"),
        ("A-16", "rig-chains-20261031", "Per-frame hip-compensation (inbetween dip up to 18px dialects, 13-14px walk/ginyu/jump, <=11px elsewhere)", 1, "pass over 9 videos", "NAMED FIX - needs go-ahead, not silently applied", "Mars wants compensation pass; re-render"),
        ("A-17", "rig-chains-20261031", "Two-figure stand version (successor-pose-dialects uses USER figure only)", 1, "version", "OWED - separate build", "Stand figure keys / Mars go-ahead"),
        ("A-18", "rig-chains-20261031", "Forward-travelling walk with background scroll (current walk is a cycle)", 1, "version", "OWED - separate build", "Background scroll build"),
        ("A-19", "storyboards-animatic-20261031 + wiring-100-20261031", "Final dialogue shots CJ-26/CJ-27 viseme/eye-strip finals", 2, "shots", "OWED - post-episode + sibling-dependent", "Mars dialogue lines (post-episode) + exposure-strip split (sibling)"),
        ("A-20", "wiring-100-20261031 + all lanes", "Post-episode steps: Mars dialogue fill-in, audio pass, dialogue QC, song-tempo choice", 4, "steps", "OWED - post-episode, NOT blockers", "Mars dialogue + tempo choice after episodes"),
        ("A-21", "superhero-mouths-20261031 (cross-ref)", "Wiring pulled Robin mouths into main lip-sync builder as default (PAH GO rebuild here is standalone proof)", 1, "builder swap", "OWED - wiring", "Builder chart swap + re-test"),
    ]
    with open(OUT / "owed-items-audit-20261031.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "source_dir", "item", "count", "unit", "status", "unblocker"])
        w.writerows(owed)
    json.dump(owed, open(OUT / "owed-items-audit-20261031.json", "w"), indent=1)
    print(f"colour EXPRES targets: {len(targets)}")
    print(f"slade face sheets: {len(slade_faces)}")
    print(f"owed rows: {len(owed)}")

if __name__ == "__main__":
    main()
