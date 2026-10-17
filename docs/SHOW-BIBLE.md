# CAPE JONES — Show Bible

*This document EXPANDS docs/SHOW-BIBLE-SEED.md (it does not replace it). The seed names the lead and the rename; this bible builds the show from the owner's recipe.*

Owner recipe (2026-10-14, verbatim): "Gumball repo and files + Teen titans repo and files + superman and open source hero files and public domain stuff we pulled in, plus space ghost repo + johnny bravo show bible = Cape Jones"

## 1. Series Overview

**Logline:** A washed-up cosmic cape-hero keeps "saving" a town that never asked him to, and fails upward every time because he cannot stop performing the hero part.

**Comedic engine** (from the Johnny Bravo show-bible template — `animation-techniques/steal-like-artist/show-starter-kits/johnny-bravo-style/show-bible-template.md`): the protagonist's flaw generates every episode. Cape Jones's flaw: he needs an audience more than he needs a rescue. Every episode = Jones wants glory → attempts a heroic feat → succeeds at the wrong thing (or fails at the right thing) → gets the credit anyway → tag undercuts him.

**Format:** 11-minute episodes (from `Gumball_Bible_text.pdf`: "THE 36X11 MINUTES SERIES" — the Gumball bible's proven unit), animated sitcom following misadventures. 2D-first production with Gumball-style mixed media where it pays off (see §5).

**Tone:** Gumball's formula (from `Gumball_Bible_text.pdf`): totally normal family/sitcom setup, "simple everyday issues we've all been through" — chased by a rampaging T-Rex, sleeping rough when a robot steals his identity — played straight. Cape Jones plays cosmic stakes with sitcom smallness: universe-ending threats, handled like a parking dispute.

**Action spine:** Teen Titans (2003) — the recipe's action ingredient. Team-dynamic action-adventure beats under the comedy: real threats, real stakes, cartoon solutions. (Source repo `mhvnsnt/cn-gigaleak-teen-titans` is README-only as of 2026-10-15 — tone notes land when the files do; see docs/ASSET-INVENTORY.md gaps.)

## 2. The Lead — CAPE JONES

Full bible: `characters/cape-jones.md`. Design sheet: `characters/design-sheet.png` (full-body, white void).

- **Body gag** (Johnny Bravo style-bible rule — "one exaggeration, committed fully"): the cape. It is enormous, dramatic, and has opinions. It billows in rooms with no wind. It gets caught in doors. It is the most competent character on the show.
- **Want:** to be watched being heroic.
- **Flaw:** performs heroism instead of doing it.
- **Silhouette-first** (Johnny Bravo style-bible): white armored suit + black mask with glowing yellow eyes + huge navy cape with crimson lining + gold power bands. Reads instantly. Likeness anchors: mask shape, cape volume, gold wrist bands.
- **CURRENT palette (owner 2026-10-17 — supersedes the old navy/crimson/gold):** suit pure white **#FFFFFF** (stays blown out, no gradients), cowl & logo deep violet **#3E1473**, skin **#E5B28C**, cape & shadows absolute black **#000000**, rim light 2–4px (situational — see §5A), blaster FX white core **#FFFFFF** + **#FFB300** outer glow. The old navy/crimson/gold look and `design-sheet.png`'s yellow-cape/red-bands are ALTERNATE colorways — logged in `characters/cape-jones.md`, never used until he says so.

## 2A. Pupil Canon (owner 2026-10-17)

**Base = "Cape Ghost":** Space Ghost minus the ears and proprietary mask bits — cowled mask, chin showing, **white eyes**. That's WHY donor-parts works (his words: the proprietary pieces are shaved off; everything else is sculpted and adapted ONTO him; result must be 100% Cape Jones).

**Pupil rules:**
- White eyes are the DEFAULT.
- SOMETIMES he gains cartoony irises/pupils for emphasis — not every time.
- Plenty of big campy acting happens pupil-less. Pupils = occasional emphasis spice.
- Cartoony pupils only — never realistic.
- Rig needs a pupil toggle; per-shot animator choice.
- Spec: `characters/sheets/05-expression-eye-dart-matrix.jpg`.

## 2B. Wardrobe Canon (owner 2026-10-17)

Alternate colorways stay LOGGED — we may log more, but do NOT use them until he says so. Story logic: people think his look is a superhero costume, but these are just his CLOTHES. One day he might change clothes — same outfit, different colorway. The 3D outfit is built as a recolorable system (material slots per colorway). Log: `characters/cape-jones.md` §"Alternate colorways".

## 3. Supporting Cast (4–6, per the Johnny Bravo template)

Cast is locked by owner only — slots below are production placeholders, not canon:

| Slot | Role | Notes |
|---|---|---|
| 1 | The Straight-Man Sidekick | Sees every failure clearly; never believed. |
| 2 | The Rival Hero | Actually competent; gets no credit. |
| 3 | The Fan | A kid who thinks Jones hung the moon; the show's heart. |
| 4 | The Nemesis | Petty, small-time; Jones inflates him into an arch-villain. |
| 5 | The Cape | (Not a joke slot — the cape gets physical-comedy sequences.) |
| 6 | The Authority | Mayor/chief who keeps hiring Jones because the paperwork is easier. |

## 4. World

**Setting:** A mid-size town that treats cosmic events as municipal problems (Gumball's Elmore principle — "Welcome to The Amazing World of Gumball, where normal just got a little weird" — from `Gumball_Bible_text.pdf`). Alien invasions get a parade permit. The hero's headquarters is a decommissioned water tower.

**Source art:** Space Ghost Coast to Coast production materials — `mhvnsnt/cn-gigaleak-space-ghost` → "Space Ghost C2C" → CHARACTER SHEETS (`SGSpaceGhostCC.eps`, `SGBrakCC.eps`, `SGMoltarCC.eps`, `SGZorakCC.eps`), BACKGROUNDS, PRODUCTION ART, LOGOS, LOG LINES. Study-only per repo notes.

## 5. Visual Style

- **Base construction:** classic Hanna-Barbera humanoid (Johnny Bravo style-bible — `style-bible.md`): standard humanoid construction, clean medium-weight outlines, smooth confident arcs, flat limited palette, silhouette-first.
- **Mixed media:** Gumball's signature (from `Gumball_Bible_text.pdf`: "COMBINES 2D AND 3D ANIMATION IN A LIVE-ACTION SETTING") — 2D character animation over photographic/3D environments for hero shots and establishing shots; `COMPGUIDE_CHARACTERS.PDF` (16pp) is the compositing reference.
- **Colour:** `AWG_Colour_Palettes_001.pdf` — palette discipline; Cape Jones hero palette: white / black / navy / crimson / gold.
- **Rig source:** Gumball S2 Flash puppet rigs (local: `workspace/toon-mash-studio/animation-study/gumball-s2-rigs/`) are the pose-library reference for physical comedy timing.

## 5A. Signature Visual Device — Dynamic Colored Lighting (owner 2026-10-17)

*"Like how texture effects in Chowder"* — Chowder made patterned textures its signature visual language; **this show makes dynamic colored lighting its signature.**

- **The blast's light BECOMES the scene lighting while it's firing:** it creates the rim light on him, throws color into the environment, and drives the color grade of the shot.
- **The sheet's blaster colors are just EXAMPLES for when he's firing that color.** Every blaster type/color gets its own lighting personality that takes over the scene while it fires.
- **Same rules in 2D and 3D:** 3D = real lights (dedicated environment-driven rim/fill rig keyed to the blaster color — see `docs/lighting/DYNAMIC-RIM-BLASTER-LIGHTING.md`); 2D = composited equivalent.
- **BUILD:** dynamic blaster-lighting rig — blaster color drives real 3D scene light (rim + spill + grade shift), 2D gets the composited equivalent. Core show identity.

## 5B. Rim Light = Situational (owner 2026-10-17)

Motivated by the scene, not fixed:
- **In space / dark void:** blue/cyan rim flying around (sheets 09–10).
- **In LED scenes:** the LED lighting itself creates the rim.
- **While a blaster fires:** the blast's color IS the rim (§5A).
- Same job everywhere: black cape stays visible in dark settings. 3D = real environment-driven rim/fill rig; 2D = drawn/composited rim. Both versions go hard in their own way.
- The suit NEVER takes the tint — environment color applies to rim lights and glow only.

## 6. Premises (first 8)

Formula (Johnny Bravo template): [Jones wants X] + [attempts Y] + [fails due to own flaw] + [tag].

1. Jones wants a parade → "stops" a meteor (it was already burning up) → the town parades the meteor → tag: the cape gets the key to the city.
2. Jones wants a nemesis → inflates a parking-ticket villain into an arch-foe → the villain leans in → tag: they do a podcast together.
3. Jones wants a sidekick → holds auditions → picks the only applicant who boos him → tag: the kid is right about everything.
4. Jones wants merch → the cape gets its own action figure → Jones's figure is the accessory → tag: cape outsells him 40:1.
5. Jones wants a day off → a real threat shows up → the town handles it without him → tag: he takes credit in the group photo.
6. Jones wants a catchphrase → every attempt is taken → settles on one in another language he can't pronounce → tag: it means "plumber."
7. Jones wants the rival's respect → challenges him to a hero-duel → loses theatrically → tag: the crowd loved the theater.
8. Jones wants to retire → nobody notices for a week → tag: the cape kept working.

## 7. Production

- Pose library required before animation (Johnny Bravo template §5). Source: Gumball S2 rigs + Space Ghost character sheets.
- Physical-comedy timing guide: cape-first. The cape leads every gag; the body follows a beat late.
- Design sheet law: every character render ships with a VOID WHITE version; full arm reach with margin at frame edges.
- Asset gaps are tracked honestly in `docs/ASSET-INVENTORY.md` — nothing ships on fabricated sources.

## 8. LED Remote Gag (canon — owner 2026-10-17, applies to 2D AND 3D)

**The rule:** the LED remote works EVERYWHERE, logic be damned. No LED lights set up? Doesn't matter — he hits the remote and the world's lighting changes anyway. The remote prop + "remote changes the world lighting" rig must work in both the 2D and 3D pipelines (version-agnostic gags).

**Canon scenes:**
1. **THE CLUB:** he's sitting in the club, everybody's dancing, and he's just got the LED remote — changing the club's lights with it.
2. **THE FOREST:** he's standing outside in the forest, broad daylight — takes out the remote, starts cycling through LED colors, and the actual daylight changes with it.
3. **THE PARKING LOT** (owner's favorite): night, standing in a parking lot — takes out the remote without a word, hits it, and the whole night lighting shifts to that broken-streetlight purple (the messed-up sodium light color). He goes: "ah, that's better."

---
*Show bible v1 — built from the owner's recipe, 2026-10-15. Tone/direction: set by owner; this is the production expansion.*
