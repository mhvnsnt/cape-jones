# DELIVERY STANDARDS — loudness teardown (Dolby & the broadcast/podcast targets)

Not code: this is the standards layer the show's audio is judged against
when it leaves the building. The house mastering spine is FFmpeg loudnorm
at **−14 LUFS integrated / −1 dBTP true peak**, locked by the owner.
**This document does not change that target.** Anything below that would
alter a deliverable is written as a *proposal flagged for an owner
decision*, never applied silently.

## The measurement language (ITU-R BS.1770)

- **LUFS** (Loudness Units Full Scale) = BS.1770 K-weighted integrated
  loudness — a perceptual average over the whole programme, not a peak
  meter. All standards below are BS.1770 numbers; "Dolby" enters because
  Dolby's tooling (and the broadcast chains built on it, e.g. Dolby Digital
  metadata / dialnorm) is how the broadcast standards are enforced in
  practice.
- **True peak (dBTP)** = inter-sample peak; lossy encoders can push peaks
  ~1–2 dB above sample peak, which is why ceilings sit at −1 or −2 dBTP.
- **LRA** (loudness range) = how dynamic the programme is; streaming
  platforms normalize integrated loudness but generally leave LRA alone.

## The targets, by destination (published specs)

| Destination | Integrated | True peak | Source family |
|---|---|---|---|
| **House master (locked)** | **−14 LUFS** | **−1 dBTP** | Owner law; UNIFIED-PIPELINE spine |
| YouTube / most social video | −14 LUFS (normalized) | ≤ −1 dBTP recommended | Platform loudness normalization |
| Spotify / Apple Music / podcast feeds | −14 LUFS (Apple Podcasts spec −16 LUFS stereo is the older podcast convention; Apple Music normalizes ≈ −14) | −1 dBTP | Platform specs |
| Twitch | ≈ −14 LUFS class normalization | — | Platform practice |
| US broadcast (ATSC A/85, CALM Act) | −24 LKFS ±2 | −2 dBTP (typical) | FCC/ATSC |
| EU broadcast (EBU R128) | −23 LUFS ±0.5 | −1 dBTP max | EBU |
| Cinema (Dolby rooms) | No LUFS master target — calibrated room (85 dBC reference), dialogue-anchored mixes | — | Dolby theatre calibration |

Reading of the table: **the locked −14/−1 house master is exactly the
streaming/social delivery spec.** One master serves YouTube, the feeds,
and social with zero rework — the destinations the show actually ships to
first. Broadcast and cinema are *different masters*, not louder/quieter
copies: they are dialogue-anchored and ~9–10 LU lower.

## Where the house stands (measured, not assumed)

EP01's 20 finished beds were all measured at the house settings and land
at **−14 ±1 LUFS, TP ≤ −0.9 dBTP** (BEDS.md, `~/workspace/ep01-finish/`),
with two scripted exceptions that are *content*, not defects: S3 at
−40 LUFS (deliberate near-silence scene) and the ST stinger at −51.85 LUFS
(deliberate absence, exempt by design). Any delivery gate must carry those
exemptions as data (scene-flagged), or it will "repair" the show's two
quietest decisions into noise.

## Proposals — OWNER DECISIONS, not applied

1. **Broadcast variant master (only if a broadcast sale ever happens):**
   a −23 LUFS (EBU) / −24 LKFS (ATSC) dialogue-anchored re-mix is a
   separate deliverable from the episode stems, not a re-normalize of the
   −14 master. *Proposal: keep as a standing note; build nothing until a
   destination exists.*
2. **Podcast/audio-only feed variant:** if episodes ever ship audio-only,
   Apple Podcasts' long-standing convention is −16 LUFS stereo. *Proposal:
   a one-flag loudnorm variant in the bed tool when/if the feed launches —
   owner call.*
3. **Gate data (no target change):** encode the deliberate-absence
   exemptions (S3/ST class) in the audio gate as named scene flags so the
   −14 ±1 check stops hand-waving them. This changes bookkeeping only;
   recommended, still flagged here rather than applied to the gate by this
   wave (the gate lives outside this package's home).

## What this wave changed

Nothing about the locked target. The spine was already right for the
show's real destinations; the teardown's product is this map, the
exemption warning, and the two flagged proposals above.
