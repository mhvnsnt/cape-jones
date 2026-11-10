# CapeJones_Sitting — Harmony import pack (skeleton)
1. In Harmony 27 Premium (activated, Windows/Mac): File > New Scene, 24 fps.
2. Import each piece in nodes.csv as a bitmap drawing (whole piece, no crop),
   create its peg, set pivot to pivot_ox/pivot_oy, set saved x/y/rotation.
   Verify cape/pelvis/head pivots (assumed centre) via Show Attribute Information.
3. Import palette/cape-jones-palette.csv via the palette editor, verify RGB
   against CAPE-JONES-HARMONY-BRIDGE-20261101.md before first render.
4. Run scripts/cape_jones_import_stub.js from Harmony's scripting interface.
   It is UNTESTED until activation — check its log against nodes.csv.
5. Save the rig as a Template (.tpl) in your CapeJones library. Do NOT
   overwrite the original default sitting pose; save new poses as new versions.
