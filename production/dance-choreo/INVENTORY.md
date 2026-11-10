# Dance-source inventory — pro cartoon holdings (2026-10-31)

Method: every candidate archive was listed without full download where
possible (HTTP range requests against GitHub release assets reading zip
central directories), every FLA in the Gumball production archive was
range-extracted and parsed (XFL DOMDocument + LIBRARY XML), and candidate
scenes were rendered frame-by-frame from their production SWFs with
JPEXS FFDec 26.3.0 and eyeballed.

## The one-line answer

The only rig dance in the holdings is **Darwin's hallway dance in
Gumball "The Words" (GB214), Sc057 + Sc059** — extracted, see `README.md`.
No Richard dance and no Scooby dance exist in extractable form in what
is held.

## Inventory

| Show | Source held | Format | Dance? | Extractable? |
|---|---|---|---|---|
| Gumball | CN-Leaks-001-gumball.zip — 61 production FLAs: 11 puppets + scene files for GB202 Remote, GB204 Phone, GB206 Job, GB209 Banana, GB211 Treasure, GB214 Words, GB218 Flakers, GB219 Watch, GB2215 Apology, GB222 Bumpkin (+ Foster's turnarounds) | FLA = XFL zip (25 fps) + companion SWF exports | **YES — Darwin, "The Words" Sc057 (wide, 198 f) + Sc059 (close-up twist, 105 f)** | **YES — extracted to JSON** |
| Gumball | Puppet SWFs/FLAs (Gumball, Nicole, Richard, Anais, Darwin, Hector, Carrie, Penny, Tobias, Ocho) | XFL / SWF | No — pose libraries + model-sheet turnarounds. Richard puppet SWF verified by FFDec dump: 1 main frame @24 fps, 147 shapes, 0 sprites; the 145-frame export in the S2 zip is a model-sheet presentation | n/a (no performance) |
| Gumball | Gumball_S2_Rigs.zip (686 MB, same release) | zip of the same rig set | No (subset of the above) | n/a |
| Gumball | Gumball Flash.rar parts (release `gumball-flash-v1`, ~1.7 GB) | RAR | Unlisted — same S2-era source family as CN-Leaks-001 | Not listed this pass |
| Gumball | Full leak 43.52 GB (draft `gumball-leak-v1`, 86 parts) | **RAR5** | **Unknown — likely more episodes (S1/S3+)** | Needs sequential RAR5 header walk across parts; not done |
| Scooby-Doo! Mystery Inc | Complete archive (GitHub `cn-gigaleak-scooby-doo-mystery-inc`) | Model packs, production art, PSD/TIF/PDF, scripts, storyboards — **0 .fla** | Chase-song material exists only as ep. 607 act D song **animatic .mov** (baked video) | **No — baked pixels / no rigs held** |
| Foster's Home | CN dot-com Flash animations: Berry, Bloo, Cheese, Coco, Ivan, Uncle Pockets, Wilt (FLA + SWF pairs) | FLA = pre-CS5 OLE binary; SWF = main-timeline shape animation, 1,618–2,190 f @24 fps | Not verified — long character reels, no dance identified yet | Heavier route: SWF PlaceObject tag parsing; not done |
| Foster's Home | TV-show turnarounds (in CN-Leaks-001) + Frankie puppet FLA | XFL / binary FLA | No — turnarounds/model sheets | n/a |
| Smiling Friends | Charlie + Pim rig FLAs (release `tv-gigaleak-fla-v1`, cartoon-vault) | FLA = XFL zip | No — rigs only; scene timelines empty | n/a (no performance) |
| Darwin (Gumball) | Standalone XFL puppet (local, from GB200 CS5 FLA) | XFL | No — puppet structure (front/back/flopped views, head comps) | n/a |
| Regular Show | Regular Show.zip in ~180 × 100 MB parts (draft `regular-show-cnleaks-v1`) | zip (unlisted) | Unknown | Not listed this pass (18.9 GB) |
| Chowder etc. | Unsorted FLAs in cartoon-vault `tv-gigaleak-fla-v1` (BOSS_*, ch_max, ch_ruby, yyo_spl_act_flipflopfoo) | FLA (binary/XFL unexamined) | Unknown | Not examined this pass |
| Rick and Morty | Toon Boom files (.tpl/.tvg thumbnails only on this VM) | Toon Boom | Unknown | No Toon Boom on VM — not extractable here |
| Ed Edd n Eddy / Grim / KND / others | Gigaleak archives complete on GitHub | Model packs / art archives | No rig material in extractable form (per parts census) | No |

## Scenes examined visually (rendered from production SWFs)

| Scene | What it is | Dance? |
|---|---|---|
| GB214 Sc057 | Darwin dance-strut down hallway, class watching | **YES — extracted** |
| GB214 Sc059 | Close-up of the same sequence; Darwin twist on the beat | **YES — extracted** |
| GB206 Sc019 | Gumball + Darwin amazed close-up (money) | No |
| GB206 Sc119 | Nicole angry close-up | No |
| GB202 Sc144 | Kids run in; Richard tackles them for the remote | No |
| GB202 Sc108 | GB + Darwin run cycles (school) | No (run cycles) |
| GB219 Sc111 | Gumball + Darwin faces squished on glass (KeyAnim) | No |
| GB214 Sc099 | Darwin's angry classroom rant | No |
| GB222 Sc090 | Kids + Anais looking up at giant bumpkin (KeyAnim, held) | No |
| GB200 DAD puppet | Richard model-sheet turnaround + expressions | No |

## Structural scan (all 71 CN-Leaks-001 FLAs)

- Symbol-name scan for dance/danse/boogie/groove/disco/twist: one hit —
  `darwin twist` (Sc059).
- Layer-name scan for dance/twist/beat/groove/song across every symbol
  timeline: hits only in Sc057 + Sc059 (`twist`, `beat`/`BEAT` layers).
- Named cycles that do exist elsewhere: `gb run cycle`, `dar run cycle`,
  `Panic Run Cycle`, walk cycles — locomotion, not dance.
