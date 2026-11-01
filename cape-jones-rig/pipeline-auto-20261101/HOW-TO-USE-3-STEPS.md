# How to use the one pipeline — 3 steps
1. Drag in Cape Jones Rig Drag. Tap Save Positions. (Until the autosave repair lands, this tap is still required — leaving without tapping loses unsaved changes.)
2. Rebuild with one command, or tell Muse "rebuild from saved":
   `python3 pipeline_auto.py --layout saved-layout-20261101.json --fist off --real-hand --out poses/real-rig-YYYYMMDD.png`
   Literal widget-faithful version (fists on, display hands): `--fist on` and no `--real-hand`.
3. Check the gates file. If ground gate says NOT planted, drag the feet down in the widget, save, re-run step 2. Nothing else to type, no manual numbers, no second hand, no crop.
