# Cape layer correction — Mars, 2026-10-31 10:13 CDT (v1 -> v2)

V1 problem, in Mars's words: Cape_Back_Main was up too high, and the
cape / collar / torso layering was wrong.
V2 fixes, exactly as given:
1. Cape_Back_Main LOWERED: top at the shoulders. In the v2 assembly
   canvas (1100x1500) that is top y=410, torso top y=400, bottom y=1201
   (80% of canvas height, behind the legs to lower shin). V1 was top
   y=180, behind the head.
2. Cape_Collar OVER Cape_Back_Main.
3. Torso_Chest OVER Cape_Collar.

New layer order, bottom to top (v2, assembly-preview-v2-20261031.png):
1 Cape_Back_Main
2 Leg_Back
3 Leg_Front
4 Arm_Back (screen-left)
5 Arm_Front (screen-right)
6 Pelvis
7 Cape_Collar
8 Torso_Chest
9 Belt_Overlay
10 Neck
11 Head_Front
Head_Profile, hand swaps, mouth/eye swaps: not in this preview, unchanged.
V1 file assembly-preview.png is NOT overwritten (checkpoint rule).
JSFL v2: build-cape-jones-rig-v2.jsfl with the same STACK order.
Note, flagged not guessed: with Torso over Collar, the collar now only
peeks at the shoulders (two small black caps beside the neck). If Mars
wants more collar visible as a drape, that is a position/size change to
the collar piece itself, not a layer-order change — ask, do not invent.
