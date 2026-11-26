# CAPE JONES — MASTER SHOW CANON (binding law)

**Source:** Owner decision, Nov 5, 2026 (Producerbot chat). Owner: Marquis (mhvnsnt).
**Status:** Binding. Required reading for every agent working in this repo (see root `AGENTS.md`).
**Scope note:** This overrides the Oct 23, 2026 note that Cape Jones 2D was not Grok Bot's job, for the purpose of this repo: **Cape Jones 2D is in scope.**

Do not invent canon beyond what is written here. Anything not stated below is an open owner decision, not a fact.

## 1. Cape Jones is the master show

- Cape Jones is the master's master show.
- Cape Jones is the **TEST GROUND for every pipeline**: 2D, 3D, game, software, animation, and show.
- Everything else converges into Cape Jones as parody / in-universe versions inside the Cape Jones multiverse.
- Other games and shows appear in Cape Jones show style.

## 2. In-universe mapping (only what the owner has stated)

| In Cape Jones | Real-world project |
|---|---|
| Immortal Qombat | Western Heart |
| Mochiichao handheld game + Mochiichao-related segments (Cape Jones show style) | Mochiichao — ties into the rest of the owner's games, shows, and repos |

No other game-to-segment mappings are canon yet. Do not create them without an owner decision; log the request instead.

## 3. Single-pipeline rule

- Get **ONE** production pipeline perfected, hardened, and consistently reliable **in Cape Jones first**.
- That one hardened pipeline in this repo is the **template** for every other project. Reuse it across all other games, shows, and repos instead of building parallel pipelines.

## 4. Tools: put what the owner has to use

The owner has Toon Boom Harmony and other paid, free, and production-level show tools and material, including work with Adult Swim and other networks. Agents must put the tools the owner actually has legitimate access to into use, not leave them sitting unused.

- Use licensed / owned / subscription tools (Toon Boom Harmony — it runs on Linux: Harmony 27 has a native GNU/Linux build; find the install with `production/harmony/find_harmony.sh` and never write "Linux unsupported").
- Use the open-source tools already vendored that can actually run (Natron, Glaxnimate, Pencil2D, etc.).
- Document anything present-but-unused: what it is, where it is, why it is not in the pipeline yet, and what would unblock it.
- This law does not authorize pulling in leaked materials; tooling means licensed, owned, subscription, or open-source tools.

## Related docs

- `docs/SHOW-PRODUCTION-STATUS.md` — REQUIRED: what is actually true about the 2D show right now (read before claiming episode/Harmony progress).
- `docs/SHOW-BIBLE.md` — show bible (this canon sits above it).
- `docs/HANDOFF-CAPE-JONES-X-WESTERN-HEART.md` — Cape Jones 3D x Western Heart ("Immortal Qombat") tie-in.
- `docs/production/CAPE-JONES-PRODUCTION-MODEL.md` — production model.

## 5. Owner decisions — 2026-11-09

- **Sitting rig read-only (owner 2026-11-02):** the sitting rig stays saved exactly as sitting position, never changed into standing rig; build a new separate standing rig. Bent legs intentional; real defect = arms/upper body stiff at shoulders/biceps.
- **Natural idle — arms down, feet grounded, arms alive (owner 2026-11-07 18:06 CST, permanent no-H-pose rule, to EVERYTHING):** in ALL natural idle poses/starts — STANDING and SITTING — arms hang DOWN naturally; half-T/'H pose' NEVER occurs naturally, ONLY when owner explicitly directs it. Feet stay planted, gravity works. Arms-down is idle, NOT freeze — arms swing/move MORE, driven by body motion.
- **V6 idle-gate verdict VOID (owner 2026-11-09):** V6 landed 2026-11-08 (PR #388) but its idle gate verdict is VOID — owner rejected cj-idle-proofs-v6.png ("those all have arms biceps up in H pose"); zoomed crops confirm upper arms held OUT from torso, elbows cocked away. Diagnosis (PR #394, merged 2026-11-10): the gate measured the upperarm bone vs world-down ONLY, never elbow-vs-torso. First fix iteration FAILED the new gate. **Owner ordered the V6 dance render STOPPED** (2026-11-09 ~12:14 CST), 1,711 of 1,824 frames PRESERVED; restart only after the real arms fix passes parent zoom-verification. Finisher lane redispatched with ELBOW-POSITION-FIRST solver objective; no bone-number-only gates for pose claims ever again.
- **2D dance decision MADE (owner 2026-11-09 ~14:53 CST, twice — widget tap + typed):** RETRY THE 2D VACE PASS WITH TWEAKED/DIFFERENT SETTINGS, Kaggle sign-in refreshed if needed (working auth = the 2026-11-02 named access token; never a legacy key). This closes the decision pending since 2026-10-31 (tweaked retry / keep fallback / focus 3D) and the retire-vs-park question on the daily cj-vace-kaggle-retry job: the job's premise is spent — retire it once the tweaked push lands. Tweaked-retry lane launched 2026-11-09; the failed Oct 31 assembly stays untouched as evidence; new output gets new filenames; zoom-verification (cape one piece in twist frames, torso travel ≥10%) before any delivery.
- **Hallway parody — owner verdict + STOP ORDER (2026-11-09):** Cape Jones is NOT THE RIGHT SIZE in the parody (owner's eye over the lane's measured-track claim). Do NOT keep working on the parody — it stays as-is, banked in cape-jones `production/dance-choreo/parody/` (PR #372, verified on main 2026-11-09). The Gumball scene material gets used LATER for more than Darwin replacement ("not just replace Darwin but will do other stuff"). Same day he ordered the full 43.5 GB Gumball leak (86 RAR5 parts, draft release gumball-leak-v1 on mhvnsnt/cn-gigaleak-gumball) mirrored INTO cape-jones in full — "get it all into the repo all 50 gigs of it."

## 6. Owner decisions — 2026-11-21

- **SHOW DNA (owner 2026-11-21):** Aqua Teen Hunger Force + JoJo's Bizarre Adventure + Space Ghost + Metalocalypse. JoJo is in it only for universe languages taken from it — not a JoJo mix otherwise. Really about Cape Jones doing nothing, mundane bullshit. Owner says they "kind of already have it out" (show bible / pilot material exists in the repo).
- **$UPEREGO studies → Cape Jones (owner 2026-11-21):** the $UPEREGO formula matches how he already planned Cape Jones, with their own languages, gags, etc. built on top of it. Full studies: `docs/SUPERIOR-TURBINATE-STUDY.md` (PR #416), `docs/SUPERIOR-TURBINATE-DEEP-STUDY.md` (PR #417), `docs/SUPERIOR-TURBINATE-FEELING-STUDY.md` (PR #418).
- **$UPEREGO blueprint for Cape Jones (owner 2026-11-21, from the $UPEREGO studies):** universe languages = voices in his head; Cape = the moral voice (most competent); Fan = audience surrogate who takes him seriously; lighting = feeling language; music = Metalocalypse layer with Real as Carmen; 'Ask Cape Jones' = Advice Corner; water tower = Discord. Thesis: 'the world is a dim orange streetlight, he fixes the light, it's better. Not saved — better.' Test short: THE PARKING LOT LED remote scene (owner's favorite); build ordered 2026-11-21 ~20:53 EST (see `docs/SHOW-PRODUCTION-STATUS.md`).

## 7. Owner decisions — 2026-11-22

- **WHITE GLOVES + GLOVE GAG (owner 2026-11-22 ~07:34–07:35 EST):** Jones wears all-white gloves in every normal/wide shot. The ungloved hand close-up is a DELIBERATE comedic beat only — hand lifts slowly, Jones out of focus in the back, he clicks, next frame cuts to normal/wide and the gloves are back on with no explanation. Bare hand appears ONLY inside the gag beat; gloves on in every normal/wide shot.
- **SHOW ORDER (owner 2026-11-22 ~08:13 EST):** Cape Jones is the #1 show to blow up — the most built-out, the simplest, perfect it first; once Cape Jones is perfected it makes Dream Girl easier to perfect, and Dream Girl follows second. People already like and support Dream Girl and want to be part of it. Cape Jones is the test ground whose pipeline Dream Girl inherits.

## 8. Owner decisions — 2026-11-26

- **PURPLE LOT V2 — REJECTED BY OWNER (2026-11-26 ~09:14 CST):** worse than before — square crops around the shoulders, hands invisible from the forearm, and the rig was swapped without being asked. VERIFIED TRUE by parent own-eyes on the merged frames: f0001/f0313 show arms ending in a flat cut at the elbow (no forearms/hands visible) and hard square box edges at the shoulders. WHY: the V2 brief ordered a NEW COA rig build from the sheets and the lane re-cut all 44 parts as rectangular boxes with make_part.py (tight boxes + flood-fill) — exactly the square-crop hand tooling his Oct 31 standing rule bans (`cape-jones-rig/CLEAN-CUT-NOTES.md`: "No square-crop hand tooling. Every slice, every time, uses slice_clean.py..."). The clean-sliced rig ALREADY existed in the repo (`cape-jones-rig/sliced-clean-20261031`, packs A–G, dance-proven CJ-09/10/11, wrist-attach rules) and the brief never told the lane to use it. The coordinator passed the defects as "nits" and the parent delivered it as done — both misses. What survives: choreography/timeline, backgrounds, gag staging, pupil button, palette. NEXT: rebuild the cut on the clean-sliced rig, pending his call. V2 as merged stays on main as the rejected cut; do not present it as the standard.
- **COLAB 3D RENDER — RESUME STARTED, BLOCKED ON SIGN-IN (2026-11-26 ~09:14–09:18 CST):** owner tapped "Resume the Colab render from ~frame 338". Cloud browser task started (browser-task:8ccc11aa) but could NOT sign in as marquiswhitacre — Google never offered "Tap Yes on your phone or tablet" in the cloud browser (only password, passkey, and "Try another way" → phone-number checks → outright rejection). No password was tried; nothing rendered; nothing paid. The Nov 22 runtime is dead after 4 days idle, so frames 1–337 are almost certainly gone — do not claim a resume from 338 unless frames are actually on disk. Do NOT retry cloud sign-in blindly (repeat rejections risk lockout). Unblock: he signs in as marquiswhitacre on his own phone (a device Google recognizes), then the resume is retried from there — or switch to JANCTION (approved backup) instead.
