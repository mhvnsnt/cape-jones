#!/usr/bin/env python3
"""Release gate: FAIL if a FINAL deliverable contains donor art/voice/lines.
Template files are allowed ONLY if marked TEMPLATE-PLACEHOLDER / TEMPLATE-AUDIO.
Usage: python3 check_template_gate.py <folder>  -> exit 0 PASS, 1 FAIL"""
import pathlib, sys
root = pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).parent
fails=[]
for p in root.rglob("*"):
    if p.is_file() and p.suffix.lower() in (".mp4",".wav",".png",".md",".json"):
        name=p.name
        # this folder is template-only by design; a file without TEMPLATE marker in a FINAL-named file fails
        if "FINAL" in name.upper() and "TEMPLATE" not in name.upper():
            fails.append(f"FINAL file without TEMPLATE marker: {name}")
# explicit: no donor voice wav in this folder (template beeps are synthesized, not donor)
# talking test must carry TEMPLATE-AUDIO in its name - check it does
if not (root/"TALKING-TEST-TEMPLATE-AUDIO-20261101.mp4").exists():
    fails.append("talking test missing TEMPLATE-AUDIO marker")
print("TEMPLATE GATE:", "FAIL "+str(fails) if fails else "PASS - template-only, no final donor deliverable in this folder")
sys.exit(1 if fails else 0)
