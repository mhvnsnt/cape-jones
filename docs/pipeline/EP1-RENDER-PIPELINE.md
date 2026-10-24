# EP1 RENDER PIPELINE — Track D report (2026-10-24)

## Owner instruction (verbatim quote)

> "Yeah let's get all the missing pieces in... so we can aim for like 6 minutes or longer"

Owner authorized getting all missing pieces in for a 6+ minute episode.
This track covers the render-pipeline missing piece: making 6+ minutes
renderable, with measured numbers.

## 0. Baseline — what was already true

- Shipped moving proof: `shared/cast/proof/cape_idle_in_cape_room_v1.md`
  (2026-10-23) — Cape idling in the living room, 61 frames @ 30 fps,
  640x360, Eevee (Blender 4.2.0), via
  `shared/cast/render_show_clip_in_room.py`. Binding gate 940/940 fcurves.
- Prior session's Cycles test on the same scene family
  (`~/workspace/scratch/cj-3d/proof/render_cycles.log`, Cycles CPU,
  12 samples, 640x360): frames finished at ~39–46 s/frame (frame 1: 42.6 s,
  frame 3: 42.1 s, frame 5: 46.4 s, frame 7: 42.6 s, frame 9: 39.3 s).
  That log is the source of the "20–50 s/frame" problem statement — it
  checks out against a real log, and this track re-measures it fresh below.
- Correction to the brief: the brief said "21 frames" for the proof. The
  shipped proof video is 61 frames; the "21 frames" are the step-6 Cycles
  stills (f_0001…f_0121) from the same session's Cycles runs. Both exist;
  neither changes the math.

## 1. Test machine (measured, 2026-10-24)

- 2 vCPU, 7.7 GB RAM, NO GPU. Blender 4.2.0 Cycles device list: only
  `CPU | AMD EPYC 9D25 126-Core Processor`, compute type NONE. No
  nvidia-smi, no CUDA/OPTIX/HIP/Metal device. Cycles GPU is therefore
  NOT an option on this VM — measured, not assumed.
- /tmp is a 512 MB tmpfs and was 100% full at test time (a 471 MB
  blender-dl tarball from another lane). Render scratch MUST live in
  ~/workspace, never /tmp. This also broke an early test run's file
  writes (0-byte outputs) before the cause was found.
- Blender 4.2.0 (the proof's version) used for all fresh measurements,
  same scene files as the proof: living_room.blend (92,300,171 bytes —
  matches repo main size exactly) and idle.glb (145,732 bytes — matches
  anims/show/cape-jones/idle.glb exactly). Binding gate re-verified:
  940/940 on every fresh run.
- Contention caveat (read this before using the numbers): this VM is
  shared with other lanes running Blender jobs. Today's Cycles numbers
  were measured while 1–3 other Blender processes were active, so they
  are realistic "shared VM" rates, not clean single-job benchmarks. The
  prior session's quiet-VM rate (~42 s/frame) is the other end of the
  range. Episode math below uses the measured rates; the range matters
  and is stated wherever it changes a conclusion.
- GAP FOUND: the proof's model file `3d-assets/cape-jones-rig/cape-jones-show.glb`
  is NOT on repo main at that path (contents API 404; code search finds
  only doc references). All fresh tests used the proof session's scratch
  copy (123,063,288 bytes, ~/workspace/scratch/cj-3d/cape-jones-show.glb).
  The pipeline cannot be re-run from main alone until that GLB is
  committed (or its real path documented). Flagged for the coordinator —
  not something this track can fix by inventing a model.

## 2. Fresh measurements (same scene, this VM, Blender 4.2.0)

Method: `production/pipeline/ep1_render.py` (this PR) — per-frame loop
with wall-clock timing persisted to timings.json after EVERY frame, so
a killed run still yields data. Camera, placement, scale and lighting
are identical to the proof script; only the render loop and an
fps-before-import fix differ (see script header).

All figures at 24 fps unless noted: 1 minute = 1,440 frames,
6 minutes = 8,640 frames. "Per 6 min" = measured s/frame × 8,640,
EXTRAPOLATED from the measured rate (labelled as such everywhere).

| Candidate (preset, res) | Measured s/frame | Frames | Per 1 min | Per 6 min (1 machine) |
|---|---|---|---|---|
| Cycles preview, 12 spp, 640x360 — TODAY, contended | 167.75 / 150.20 / 151.34 (avg 156.43) | 3 | 62.6 h | 375.4 h = 15.6 days |
| Cycles preview, 12 spp, 640x360 — PRIOR session, quiet VM | ~39–46 (avg ~42) | ~5 (log) | 16.8 h | 100.8 h = 4.2 days |
| Cycles show, 16 spp adaptive 0.05 + OIDN + living-room bounces, 640x360 — TODAY, contended | 216.34 / 182.31 / 189.36 (avg 196.00) | 3 | 78.4 h | 470.4 h = 19.6 days |
| Cycles show, 16 spp adaptive 0.05 + OIDN, 1920x1080 — TODAY | 819.12 | 1 | 327.7 h | 1,965.9 h = 81.9 days |
| Eevee preview, TAA 24, 640x360 — TODAY | 289.36 | 1 clean (+1 rough, see §3c) | 115.7 h | 694.5 h = 28.9 days |
| Eevee preview, TAA 24, 1920x1080 | EXTRAPOLATED ×9 pixels from 289.36 = ~2,604 | 0 (not run) | ~1,042 h | ~6,250 h = 260 days |
| Cycles show, 1920x1080 → 720p scale | EXTRAPOLATED ×0.444 pixels from 819.12 = ~364 | 0 (not run) | ~145 h | ~873 h = 36.4 days |
| Cycles hero, 32 spp — NOT measured | (would be ~2× show rate by samples; not claimed) | 0 | — | — |

Split test (real, today): 2 concurrent Cycles-preview 640x360 processes,
1 frame each, finished in 174 s wall total (110.36 s + 110.68 s render
each, imports overlapped). Per-frame cost did NOT drop — on a 2-core
box, two Blenders share the same 2 cores. Splitting only pays when the
workers are on DIFFERENT machines.

At 30 fps instead of 24 fps, multiply all frame counts by 1.25
(6 min = 10,800 frames): Cycles show 1080p single-machine = 2,457 h =
102.4 days. Render at 24 fps unless the owner explicitly wants 30.

## 3. Candidate verdicts

### (a) Cycles CPU at final-quality settings
The show preset (16 spp adaptive + OIDN, living-room bounces) is the
quality anchor: 819.12 s/frame measured at 1080p. It looks right (see
§3c visual check) and it is the preset the repo's own speed research
already validated. But on one machine it is 82 days for 6 minutes at
1080p. Cycles CPU is viable ONLY with a farm (§4). At 360p the same
preset is 196 s/frame contended — still 19.6 days for 6 minutes.
There is no Cycles-CPU-on-one-VM path to 6 minutes. Full stop.

### (b) Cycles GPU on this VM
NOT AVAILABLE. Device list shows CPU only (see §1). Any GPU number for
this VM would be invented. GPU rendering requires a different machine
(see (f) and §4).

### (c) Eevee at show quality
Measured, and the result kills the obvious hope: on THIS GPU-less VM,
Eevee preview at 640x360 took 289.36 s/frame — SLOWER than Cycles
preview (156 s contended / ~42 s quiet) on the same scene. Eevee runs
on software GL (llvmpipe) here, and it is also fragile: two further
Eevee attempts died mid-run (exit 134 libEGL abort; exit 137 SIGKILL
twice, under shared-VM memory pressure), while Cycles runs completed.
An earlier Eevee frame did complete (run 1, ≤5.1 min wall including
import — consistent with ~289 s), so Eevee CAN render here, but it is
neither fast nor reliable here.
Visual check (viewed, not claimed): the Eevee frame holds the show's
look — same purple LED wash, same room, same Cape. Against the Cycles
frame of the same scene, Eevee is visibly grainier with flatter shadows
and harsher light edges, but nothing breaks: no missing geometry, no
wrong colors, no lost cape. The 1080p Cycles frame was also viewed:
clean, detailed, purple wash intact, soft shadows, TV glow, lamp pools.
Eevee is NOT rejected for looks — it is rejected on this hardware for
speed and stability. Eevee only becomes the fast path on a machine WITH
a real GPU, which this project does not currently have. Do NOT plan the
episode around Eevee on this VM.
(The cape in these tests is the baked/idle clip mesh; cloth motion is
NOT a differentiator here — that stays with the cloth-collision track.)

### (d) Flamenco 3.9.3 (Blender's official farm manager, GPL, free)
Verified live on this VM, 2026-10-24:
- Downloaded flamenco-3.9.3-linux-amd64.tar.gz from the official
  download page; Manager and Worker binaries run (version 3.9.3).
- Manager serves its web UI on :8080 (/app/, HTTP 200).
- One Worker registered and signed on: name "htch-runtime",
  uuid 9ada828d-93e2-4c0f-8a53-bc59e60ea636, status awake.
- The Worker reported "Blender could not be found" until the Manager's
  `blender` variable points at a real binary — the delivered
  `flamenco-manager.ep1.yaml` sets it (placeholder path to replace).
- The Manager serves its Blender add-on at /flamenco-addon.zip
  (HTTP 200, 735,422 bytes, 131 entries — downloaded and inspected:
  real add-on with job_submission.py, job_types.py, manager API).
- NOT yet exercised end-to-end: no job was dispatched through Flamenco
  on this VM. Job submission needs (i) shared storage at one identical
  path on manager + workers, (ii) the `blender` variable set, (iii) the
  add-on installed in Blender. Those are setup steps, not blockers —
  but until a job actually renders through it, Flamenco is "installed
  and handshake-verified", NOT "proven rendering".
- What Flamenco does and does not do: it distributes FRAMES across
  machines. It does NOT make one frame faster. Farm wall-clock =
  single-machine wall-clock ÷ worker count (minus overhead). With ONE
  worker it buys nothing. Its default task_timeout is 10 min per task,
  so chunks must be sized to finish inside the timeout (delivered
  config raises it to 30 min; chunk guidance: Cycles-show 1080p at
  819 s/frame = max 2 frames per 30-min task, 1 is safest; Cycles-show
  360p at ~196 s = ~9 frames per 30-min task).

### (e) Frame-range chunking (no new software)
`production/pipeline/ep1_render_chunk.sh`: one invocation = one frame
range = one farm task / one Kaggle kernel / one manual run. This works
today with zero installs and is how the episode MUST be split regardless
of which farm runs it: a 6-minute episode at 24 fps is 8,640 frames,
and no single machine on this project renders that in one go. The
split test (§2) proves the mechanism; it also proves the limit: on this
2-core VM, splitting across processes gains ~nothing. The gain comes
from additional machines.

### (f) Kaggle T4 lane (existing, documented, free)
Repo doc: docs/pipeline/KAGGLE-GPU-SETUP.md. Status from that doc:
- GPU presence PROVEN 2026-10-16: 2× Tesla T4 (15,360 MiB each),
  Cycles OPTIX devices listed. Blender 5.2.2 installed in 27.3 s.
- The actual Cycles render test was BLOCKED: kernel v4 was cancelled by
  an external party ~1 min after push, before rendering. Re-push was
  awaiting parent go-ahead and the doc says do not re-push blindly.
- Consequence: NO measured T4 seconds/frame exists anywhere in the repo.
  Any T4 number in a plan today is an estimate, and this report does not
  present one as measured.
- Quota arithmetic (ASSUMED 10× GPU speedup — an assumption, NOT a
  measurement, shown only to test feasibility): Cycles-show 1080p at
  ~82 s/frame = 197 GPU-hours per 6-minute episode vs the 30 GPU-hour/
  week shared quota = ~6.6 weeks of quota for one episode. At 720p
  (~36 s/frame assumed) = ~87 GPU-hours = ~2.9 weeks. Conclusion: even
  under an optimistic speedup assumption, the FREE Kaggle tier alone
  cannot carry a 6-minute 1080p episode in one week. Kaggle is a
  supplement (measurement runs, hero shots, tests), not the episode
  engine, unless the owner pays for more GPU or accepts multi-week
  quota spend. A real T4 measurement run is still worth doing — it
  replaces the assumed 10× with a number.

## 4. Recommendation

1. ENGINE: Cycles show preset (16 spp adaptive 0.05 + OIDN +
   living-room bounces) — the repo's own validated preset, visually
   confirmed at 1080p. Not Eevee (slower + fragile here), not Cycles
   preview for finals (noisier, and only ~1.25× cheaper than show at
   360p while giving up the denoiser/bounce quality).
2. RESOLUTION + FPS: 1920x1080 at 24 fps IF a farm exists (see 3).
   Fallback if no farm materializes: 1280x720 at 24 fps (extrapolated
   ~364 s/frame, 873 h single-machine — still needs a farm, but a
   smaller one). Do not choose 30 fps without a reason: +25% frames.
3. FARM: Flamenco 3.9.3 (free, handshake-verified) on real machines,
   chunks via ep1_render_chunk.sh. Farm wall-clock for 6 min at
   Cycles-show 1080p (measured 819.12 s/frame, before overhead):
   10 workers → ~197 h ≈ 8.2 days; 20 workers → ~98 h ≈ 4.1 days;
   50 workers → ~39 h ≈ 1.6 days. At 720p: 10 workers → ~87 h ≈
   3.6 days; 20 workers → ~44 h ≈ 1.8 days. Add ~10–20% overhead in
   planning. The binding constraint is WORKER COUNT, not software.
4. KAGGLE: run the T4 measurement (needs go-ahead, §6 item 2) to get a
   real GPU number, and use Kaggle for tests/hero shots. Do not plan
   the episode on free-tier quota alone (§3f).
5. SEQUENCE: lock 24 fps + resolution (owner call) → commit the missing
   model GLB → stand up Manager + shared storage → dispatch one small
   Flamenco job end-to-end as proof → then chunk the episode.

## 5. What it costs / setup steps

- Software cost: $0 (Blender, Flamenco, chunk scripts — all free).
- Machines: the only real cost. One VM = 82 days (1080p) — not viable.
  10–20 real worker machines (or equivalent rented GPU/CPU time) =
  days, per §4. No purchase is identified as required by this track;
  paid GPU time is an owner decision if owned machines fall short.
- Setup steps (Flamenco path): (1) pick a Manager host; (2) mount
  shared storage at ONE identical path on every worker; (3) install
  Blender 4.2.0 (same version everywhere) + copy
  production/pipeline/ep1_render.py + chunk script under shared
  storage; (4) install flamenco-manager.ep1.yaml with real
  SHARED_STORAGE + BLENDER_BIN values; (5) install the add-on from
  http://<manager>:8080/flamenco-addon.zip in Blender; (6) submit one
  1–2 frame test job; (7) split the episode with the chunk script and
  submit per-chunk tasks inside the task timeout (§3d).
- Per-chunk sizing rule: chunk_seconds ≤ task_timeout. At 30 min
  timeout: Cycles-show 1080p → 1–2 frames/chunk; Cycles-show 360p →
  ≤9 frames/chunk; Cycles-preview 360p → ≤11 frames/chunk (at
  contended rates; fewer if contention is worse).

## 6. Delivered in this PR
- production/pipeline/ep1_render.py — chunked show-clip renderer with
  presets (eevee_preview/show, cycles_preview/show/hero) + per-frame
  timings.json (persisted after every frame). Derived from
  shared/cast/render_show_clip_in_room.py; changes documented in its
  header (per-frame loop; fps set before clip import).
- production/pipeline/ep1_render_chunk.sh — one chunk = one farm task.
- production/pipeline/flamenco-manager.ep1.yaml — Flamenco manager
  config for EP1 (placeholders marked SHARED_STORAGE / BLENDER_BIN).
- This report: docs/pipeline/EP1-RENDER-PIPELINE.md.
- Test frames + logs are NOT in git (PNGs are large). They live in the
  worker workspace at ~/workspace/trackd/out/ (cycles_preview_360/,
  cycles_show_360/, cycles_show_1080/, eevee_retry_360/, split_a/,
  split_b/ + matching .log files and timings.json). The numbers in §2
  are the durable record; the coordinator can publish frames from
  there if the owner wants to see them.

## 7. OWNER-NEEDED (only the owner/coordinator can supply)
1. Machines: how many real machines (or cloud/GPU hours) will render?
   The farm math in §4 shows the worker count needed for each target.
2. Kaggle go-ahead: permission to spend shared 30 GPU-hr/week quota on
   a T4 measurement run (the doc's standing rule: never re-push blindly;
   coordinate, never kill another lane's kernel).
3. Show-quality call: 24 vs 30 fps, and 1080p vs 720p. Both change frame
   count and per-frame cost multiplicatively (see §2).
4. The missing model file: commit 3d-assets/cape-jones-rig/cape-jones-show.glb
   (or document its real path) so the pipeline runs from main alone.
5. Flamenco farm home: a machine to host the Manager + shared storage
   path identical on all workers (NAS/SMB mount), if Flamenco is chosen.

## 8. PENDING (open after this track)
- End-to-end Flamenco job dispatch (needs §7 items 1+5).
- Measured T4 seconds/frame (needs §7 item 2).
- Measured 720p rate (currently extrapolated from 1080p by pixel ratio)
  and measured hero-preset rate (currently unmeasured; not claimed).
- Eevee steady-state at 1080p (not run — 360p rate + fragility already
  disqualify it on this hardware; re-test only on a GPU machine).
- Cloth-motion rendering: this track renders the baked/idle clip; the
  cloth-collision track owns whether the cape sim survives at render time.
