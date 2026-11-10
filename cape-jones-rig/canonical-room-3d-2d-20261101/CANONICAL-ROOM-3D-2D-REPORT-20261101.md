# Canonical room — 3D source found + new 2D version from it (2026-11-01)

Correction recorded: canonical room SOURCE is the actual 3D room in repo mhvnsnt/cape-jones,
NOT only the 2D picture sent 2026-11-01 00:00 CDT. That 2D picture is a 2D version/rendering
of that 3D room. Mars sent 00:19 CDT: 4 3D renders + 2 2D images, saved in this folder.

## 1. 3D room found in repo — VERIFIED via GitHub API + Blender (approval 0/1 separately)

- Repo: mhvnsnt/cape-jones, public, default branch main, repo size 4,027,599 KB (API, 2026-11-01).
- Main file: `3d-assets/living_room.blend`
  - API size 92,300,171 bytes, blob SHA c537475db64c33c5c36fa308ba16adb921e7df16
  - Local checkout md5 3ff6c792a93ecb7ee2fb70a4abd437f1 (git checkout, not API blob)
  - Download URL: https://raw.githubusercontent.com/mhvnsnt/cape-jones/main/3d-assets/living_room.blend
- Scene docs in repo: `3d-assets/living-room/SCENE-CANON.md` (owner-approved 2026-10-16,
  "single source of truth"), `3d-assets/living-room/INTEGRATION.md` (assembly 2026-10-18,
  PRs #123 recliner, #129 TV, #132 lighting, #131 sit targets, #126 research),
  `3d-assets/living_room_layout.json` (room 7.0 x 6.0 m, validated, 8 items),
  `3d-assets/living-room/furniture_positions.json` (position_1 DEFAULT backs-against-wall,
  position_2 TV/shelf facing chair).
- Subfolders: renders/ (5 integration renders), tv/, recliner/ (recliner_rigged.blend 947,444 bytes),
  lighting/, sit-targets/, props/ (notes only).
- Blender 5.2.3 LTS inspection, local checkout (first attempt crashed on the missing linked
  recliner library; after fetching recliner_rigged.blend it loaded clean, exit 0):
  - Scene "Scene", 129 objects, 2 collections (Collection, Recliner), render engine CYCLES
  - Camera: MainCam at (0, -4.6, 1.7), active camera
  - Lights: RoomLight POINT 300 violet (0.45, 0.10, 0.90), Sun 1.5 white, HallLight 60,
    LampCone_Floor 30, LampCone_Table 18, RimLight 60 violet, TV_Glow 14, WindowShaft 160
  - Key objects: Floor, Ceiling, cabinetTelevision(Clone) (-0.9, 2.6, 0), crt_tv + crt_screen,
    antenna_0/1, box_a/b/c/d, monster_body/eyes/feet (TV-stand monster toy),
    bookcaseClosed(Clone) (-2.95, -1.8, 0) = position_2 placement in this blend,
    loungeChairRelax(Clone) (2.653, 2.312, 0) hide_render=True (static mesh hidden;
    linked recliner_rig parts at same location are the visible chair),
    loungeDesignSofa(Clone) (-2.9, -0.6, 0) blue sofa, tableCoffee, rugRound(Clone),
    lampRoundFloor(Clone) (3.0, 2.5, 0), lampSquareTable(Clone), side_table,
    okayest_hero_mug, LED_Back (0, 2.9, 2.75), LED_Left, LED_Right, window_unit (3.5, 1.5, 1.6)
    + win_* frame/mullions, ext_sun (5.3, -0.1, 2.6), poster_backing/paper/text (-1.7, 2.925, 1.9),
    ghost_* poster objects (0.5, 2.925, 1.9), shrimp_body/tail (-1.7, 2.9, 1.78),
    door jambs/lintel, hallway objects, CapeJones_Body/Cape/Rig at origin (character in blend).
  - Materials: WallMat, FloorMat, carpet (chair), carpet.001 (rug), carpetBlue (sofa),
    carpetDarker (rug ring), wood/wood.001-003, metal/metal.001-003, lamp/lamp.001,
    LEDStripMat, tvScreenMat, skyMat, RemoteMat, BtnMat_0-5.
- Canon palette (SCENE-CANON.md, hex from Principled BSDF): walls WallMat #D1C7B8 warm bone,
  floor FloorMat #735238 dark warm brown, chair/rug carpet #F15E57 coral pink, rug ring
  #9B4C49, sofa carpetBlue #5B84DD, wood #E59964 warm oak, metal #BDD2D6 cool silver,
  lamp shades #FFE996 warm amber, LED emission #731AE5 violet-purple strength 4.0.
  The purple/pink look in Mars's sent renders is that violet RoomLight 300 wash over
  bone/brown surfaces, NOT a different wall paint in the canon doc. State this plainly:
  canon doc colour != sent-render apparent colour, because of the violet light.
- Blender render done here (Cycles CPU, 480x270, 24 samples, MainCam):
  work/blender-render-maincam.png — matches Mars's 3d-view-2 almost exactly
  (TV left, coffee table + lamp centre, black cape silhouette foreground, rug right edge).
  One Cycles warning: "Failed to load 1 image file" — a TV image-sequence frame not in
  the sparse checkout; TV screen renders pink/blank, same as view-2. Not a room failure.

## 2. Comparison — repo 3D room vs Mars's sent views (item by item)

| Item | Repo 3D blend | Mars 3D views (1-4) | Mars 2D full / chair closeup |
|---|---|---|---|
| Two-wall corner, ceiling | Yes, 7.0x6.0m, walls 3.0m high, Ceiling at z=3.0 | Yes, same corner in view-3 | Yes, same corner |
| Neon tubes, both walls | LED_Back/Left/Right meshes at z=2.75, emission #731AE5 | Yes, long pink-magenta tubes, view-3 | Yes, two glowing tubes |
| Posters, left wall | poster (shrimp/FRY EM UP, -1.7, back wall) + ghost poster (0.5) | Yes, left poster + centre pink poster | Left poster text "PET OM UP" + pink creature poster — text differs from FRY EM UP canon; 2D renames/re-stages it |
| Blue hanging mask | NO named mask object in the 129-object list | Yes, blue mask hanging in view-3/4 | Yes, blue mask — appears in sent renders but has no named object in living_room.blend; either baked into a mesh or added after this blend save. NOT invented here. |
| CRT TV + stand + antennae | crt_tv, crt_screen, antenna_0/1, cabinetTelevision | Yes, views 2/3/4 | Yes, TV on wooden stand |
| TV-stand shelves: VCR, boxes, monster toy | box_a-d, monster_body/eyes/feet | Yes, view-4 shows VCR + boxes + blue ball | Yes, VCR + boxes + blue ball |
| Floor lamp, corner | lampRoundFloor (3.0, 2.5, 0) | Yes, view-1 | Yes, thin floor lamp in corner |
| Window, right wall | window_unit (3.5, 1.5, 1.6), ext_sun, skyMat | Yes, 4-pane window, sunset sun | Yes, 4-pane window, large orange sun, teal sky |
| Window view content | Layout says trees/sky (AFTER furniture); blend has ext_sun + skyMat | Sunset sun in views | Sunset sun — sunset staging is in the sent renders/2D, not in the SCENE-CANON trees/sky text |
| Blue side table + mug | side_table, okayest_hero_mug | Yes, view-1/3 | Yes, blue side table + cup |
| Pink chair | Recliner, coral #F15E57, 0.49m wide, at (2.653, 2.312, 0), facing -x toward TV | Yes, small pink recliner on rug, view-1 | Large pink wingback with wooden scroll arms — ENLARGED/STYLISED vs the blend recliner; not 1:1 scale |
| Round rug | rugRound, coral field + darker ring | Yes, large round pink rug, view-1 | Rug is NOT prominent in 2D full (floor mostly bare); 3D view-1 rug is the reference |
| Coffee table + lamp | tableCoffee, lampSquareTable | Yes, view-2 | Yes, pink coffee table + lamp, foreground centre |
| Blue sofa | loungeDesignSofa (-2.9, -0.6, 0) | Not in sent views (camera side) | Not in 2D full |
| Doorway / hallway | door jambs/lintel + hallway objects | View-2/4 show doorway at left edge | Not in 2D full |
| Character | CapeJones_Body/Cape/Rig in blend; INTEGRATION says sitter placed, scale 0.925 | View-1 seated, view-4 T-pose arms out | Seated in wingback, hands together; foreground partial figure bottom-right |
| 2D full vs 00:00 picture | — | — | Same scene, both 2048x1152, DIFFERENT md5 (2d-full 4d19819e…, 00:00 picture 04e3078f…): re-encode/variant, NOT byte-identical |

## 3. NEW 2D version from the 3D source (approval 0/1 separately)

- File: canonical-room-2d-from-3d-20261101.png, 2048x1152, generated with the media
  generation pipeline (best generative method on this VM), from Mars's 3D views as
  reference (wide view-3 + chair view-1), NOT a copy of his 2D upload, NOT hand-drawn PIL.
  PIL was not used as production here.
- It is an EMPTY room background plate (no character), so it can sit behind any pose.
  Layout matches the 3D room: two-wall corner, darker purple ceiling, pink-purple floor,
  two neon tubes, left-wall posters + blue mask, CRT + oak stand + VCR/boxes/blue ball,
  right-wall 4-pane sunset window, corner floor lamp, blue side table + steaming cup,
  pink wingback chair on round pink rug with darker ring, foreground pink coffee table + lamp.
- Viewed by this job before delivery. Honest differences from Mars's 2D full:
  chair is smaller (closer to the blend recliner) than his large 2D wingback;
  poster animals are simplified (left poster animal reads pig-like, not capybara);
  window sunset sits lower with clouds; no seated figure, no foreground partial figure.
  Those are generative simplifications, not canon changes.
- Originals untouched. No repo push by this job. Work scratch (partial git clone of the
  repo, ~662 MB with .git objects) was deleted after inspection — the .blend lives in
  the repo, regenerable, and must not be landed as a duplicate.
- Still owed: Mars's approval 0/1 for (a) 3D-source identification above, (b) new 2D
  version; a seated-figure composite on this new 2D plate if he wants one (not built here).
