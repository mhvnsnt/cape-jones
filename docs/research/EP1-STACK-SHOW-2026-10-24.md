# EP1 Open-Source Stacking Research — Show-Facing + Shared Pipeline — 2026-10-24

**Shared-pipeline rule (owner scope clarification, 2026-10-24).** This stack
serves BOTH the game and the show — one shared pipeline, not a show-only
fork. The game-facing wiring lives in western-heart
(`docs/research/EP1-STACK-RESEARCH-2026-10-24.md` and
`docs/research/ANATOMY-STACK-WIRING-2026-10-24.md`, plus the enforceable
gate `tools/anatomy/stack_layers.json` +
`tools/anatomy/validate_stack_layers.py`). This document is the show-facing
half of the SAME pipeline: it says how each piece feeds show production,
and where the game and the show share one asset, one rig check, or one
render setup instead of maintaining two versions. Show is the current
focus; game wiring is not out of scope — it is the other half of this
work, reported separately to the coordinator.

**In-show naming rule (non-negotiable).** Inside Episode 1, the game
appears under its in-universe title **IMMORTAL QOMBAT** — never
"Western Heart". That rule governs show-facing docs, on-screen text,
dialogue, credits as seen in the episode, and assets. "Western Heart" is
only the out-of-universe repository/project name and appears in this
document solely where it identifies the game repo that shares the pipeline
(e.g. file paths). If any show-facing asset in this PR used the wrong
name, that would be a defect — none does: this PR contains no on-screen
text, dialogue, or in-episode credits, only production docs and a render
job template.

**Honesty rule.** No farm was run, no render was measured, and no
third-party asset was bundled in this PR. Flamenco is a pointer for the
render-pipeline track (which owns numbers); the job file here is a
template to adapt, not a submission tested against a live Manager. SKEL
findings are a checklist applied to our own rigs, not SKEL assets.

## 1. Shared pipeline map (one asset, two outputs)

| Shared piece | Game output | Show output | Single source of truth |
|---|---|---|---|
| Anatomy layers (`wh.anatomy-layers/2`, analytic SDF primitives) | X-ray on KO blows; creation-suite deep morphing | Fight-presentation anatomy shots in IMMORTAL QOMBAT sequences; dissection-style presentation where the episode calls for it | The fighter's `anatomy-layers.json` in the game repo. The show reads the same layer groups — it does not maintain a parallel anatomy model. |
| Rig + joint audit (SKEL checklist, §3) | Fighter rigs that bend without bones poking through skin | Show rigs (Cape, Pantera) that hold up in close-up fight shots | One checklist, applied to both rig sets; fixes land in our own rigging. |
| Render setup (Flamenco, §4) | — (game runtime does not use Flamenco) | Ep 1 Blender frames, chunked across workers | The job template in this PR, owned for numbers by the render track. |
| Dataset provenance (allow/block list) | Which atlas meshes may ship in the game | Which atlas geometry may appear in show frames, and what credit it needs | `tools/anatomy/stack_layers.json` in the game repo; show credits copy its attribution strings verbatim when atlas geometry is ever shown. |
| Purdue fracture core (MIT) | Destructible props / finisher VFX | Over-the-top impact VFX in show fight shots, rendered from the same technique | MIT shader core in `tools/`; game and show each bake their own shots from it. |

If a future change forks any row above into a game version and a show
version, that fork needs an explicit owner decision — the default is one
pipeline.

## 2. Piece-by-piece show use (licenses from the game-facing doc)

Full verdicts, license sources, and the sources-read list are in the
game-facing research doc; this section states only the show consequence.
Nothing here re-verdicts a license.

- **Purdue Dissectible Anatomy — methods-only for show VFX.** The
  splat/SDF anatomy layer has no public code, so no show shot can "use
  Purdue's code". What the show CAN use: the same methods the game uses
  (PBD particles, no fixed connectivity, SDF boolean cuts, shell-only
  splat rendering) implemented from the published methods for
  dissection-style or interior-reveal shots, plus the MIT voxel-fracture
  core for destructible-impact VFX. Both are production techniques, not
  story claims, and neither invents canon.
- **Human Atlas datasets — credit-gated for show frames.** BodyParts3D
  4.0 (CC BY 4.0) and HRA 3D organs (CC BY 4.0) may appear in show frames
  with their exact attribution strings (see the game repo's stack map);
  Z-Anatomy (CC BY-SA 4.0) geometry must not appear in shipped show
  frames either — the share-alike problem does not disappear because the
  output is video. If a show frame ever uses atlas geometry, its credit
  line goes in the episode credits from the same attribution strings the
  game uses. No atlas geometry is used in any frame by this PR.
- **Somakine — reference + viewer pattern for show presentation.**
  Somakine's MIT viewer patterns (layer toggles, exploded layouts,
  occlusion-aware picking, demand-driven loading) are the reference for
  how anatomy-presentation shots are staged (which layer is visible when,
  how a structure is isolated on screen). Its BodyParts3D data pack is
  CC BY 4.0, same credit rule as above. No Somakine code is embedded in
  show assets by this PR.
- **LearnAnatomy3D — techniques only.** Its part-index texture,
  persistent clipping plane, stencil body-volume mask, and two-pass
  streaming are staging/rendering techniques for anatomy shots (see the
  game-facing wiring spec §5). No LearnAnatomy3D geometry or code enters
  show production through this path.
- **SKEL — checklist only (§3).** No SKEL/SMPL model, mesh, or parameter
  ships in the show or the game. The MPG research-only license bars
  commercial incorporation and distribution; the show is commercial
  production, so the bar applies here too.
- **Flamenco — the show's render farm (§4).** GPLv3+, tool-only. Running
  it as separate Manager/Worker processes to render `.blend` files does
  not GPL the episode or its frames. No Flamenco code is copied into
  show or game runtime by this PR.

## 3. SKEL-informed rig-quality checklist (show rigs)

Apply to every show rig (Cape, Pantera, and any fighter appearing in Ep 1)
before its shots are rendered, and record pass/fail per rig in the shot's
production notes. A failed check is fixed in our own rigging — never by
importing SKEL parameters, meshes, or joint data. This is the same
checklist as the game-facing doc §5, stated here for show rigs:

1. **Joint centers:** knees, elbows, shoulders sit at true anatomical
   centers, not at simplified joint guesses. Check in a neutral pose
   against the skeleton layer, not against the skin silhouette alone.
2. **Scapula slide:** the shoulder blade slides on the ribcage as the
   arm raises; it is not rigidly parented to the torso. Check at arm
   raise extremes — a frozen scapula reads as broken in close-up.
3. **Forearm twist:** pronation/supination twists along the forearm
   axis; the forearm does not rotate as a rigid stick. Check with the
   hand rotating while the elbow stays fixed.
4. **Knee hinge:** flexion is a clean hinge axis; at full bend the mesh
   does not collapse and no bone pokes through the skin. Check at the
   deepest crouch / kick-chamber poses the episode uses.
5. **Bones inside surface:** at every extreme pose used in the episode,
   every bone stays inside the skin mesh. Check the full pose range, not
   just the neutral pose.
6. **Realistic ranges:** joint limits match anatomical ranges, so
   retargeted motion does not produce impossible poses on screen.

Status for this PR: checklist specified, not yet run against any show
rig — running it is shot-production work, and its results belong in shot
notes, not in this research doc. Do not report any rig as "SKEL-verified":
SKEL was not run, and its assets were not used.

## 4. Flamenco render-farm pointer (render track owns numbers)

Flamenco (Blender Studio's render-farm manager, GPLv3+) is the evaluated
stack piece for Ep 1 Blender rendering. From the project docs (see the
game-facing research doc §6 for sources): Manager holds the queue and web
dashboard and splits jobs into tasks; Workers poll, launch Blender in the
background, and report progress; jobs are frame ranges cut into chunks;
idle workers take the next chunk; failed tasks retry on another worker,
and a worker is blocklisted for a job after three failures on it; job
types are JavaScript; any Blender render engine works, including
progressive Cycles (frames split by sample count, then merged).

**Job shape for Ep 1 (template in `EP1-FLAMENCO-JOB.example.json`).**
One job per shot; the template carries placeholders the render track
fills in — it is NOT a submission tested against a live Manager, and its
field names must be adapted to the render track's Flamenco version before
use:

- Shot identity + `.blend` path + output path (shared storage every
  worker can reach — file sharing must already be set up before any job
  runs; Flamenco does not move your `.blend` for you).
- Frame range + chunk size (chunking is how fast machines end up doing
  more work; the render track picks the size from its measurements, not
  from this doc).
- Render engine + output format + resolution placeholders.
- Pre-submission gates, in order: (1) bake all simulations centrally
  (cloth, smoke, any dynamics — un-baked sims diverge across workers);
  (2) identical Blender + add-on versions on every node; (3) packed
  textures/assets or absolute shared paths; (4) a short test chunk
  rendered and viewed before the full range is committed.

**What this track does NOT do:** stand up a farm, measure throughput,
pick chunk sizes, or choose worker machines. That is the separate
render-pipeline track's measurement work, deliberately not duplicated
here. If that track finds Flamenco unsuitable, this pointer is replaced
by its findings — the job template is disposable, the episode is not
blocked on it.

## 5. What is still open (show side)

- Running the §3 checklist against Cape/Pantera show rigs and recording
  results in shot notes (shot-production work).
- Render-track decisions: farm machines, chunk sizes, throughput numbers,
  and the adapted job submission (see §4).
- Any episode credit lines for atlas geometry, if and only if a show
  frame ever uses BodyParts3D/HRA geometry (copy attribution strings
  verbatim from the game repo's stack map).
- In-show naming audit at picture lock: confirm no show-facing asset
  calls the in-show game anything but IMMORTAL QOMBAT.
