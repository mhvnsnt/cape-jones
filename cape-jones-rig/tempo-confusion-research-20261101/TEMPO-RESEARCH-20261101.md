# TEMPO CONFUSION — RESEARCH + REVERSE-ENGINEERING, 2026-11-01

## In plain words first — what A, B1, B2, C actually mean

Think of it as two clocks that don't agree. The picture was cut to a slow clock,
the song was written to a fast clock.

- **Picture now: 107 BPM.** One beat = 0.561 seconds = **13.46 frames** at 24fps.
  A step, a punch, a head-turn timed to "one beat" takes about 13-14 frames.
- **Song: 152 BPM.** One beat = 0.395 seconds = **9.47 frames** at 24fps.
  The same "one beat" move takes about 9-10 frames — about 30% faster.
- A bar (4 beats): 107 = 53.8 frames, 152 = 37.9 frames.
- The gap: 152 / 107 = **1.4206x**. Stretching the song down to picture speed
  makes it 1.42x longer. Speeding picture up to song speed makes it 1.42x shorter
  in beat terms.

That is the whole confusion. Nothing is broken, the two sides were just built
to different clocks.

### A — Picture follows song (152)
Keep the song exactly as written. Re-time the visuals so every move lands on
a 152 beat. Cost: visual rework. A 13-14 frame move becomes a 9-10 frame move,
or you add extra inbetweens/holds to fill the new grid. Example, same 24 beats:
107 picture = 323 frames (13.46s), 152 picture = 227 frames (9.47s) — 96 frames
shorter if you keep the same number of beats. The 332-frame animatic holds
24.7 beats at 107, but 35.0 beats at 152 — so at 152 the same animatic would
feel like it has ~10 extra beats of music passing under it unless cuts/moves
are re-timed. This is the "music leads" route: edit the animatic over the
soundtrack first, then fit gestures to the bits (stop-motion / animation
practice, Gasek, Frame-by-Frame Stop Motion).

### B1 — Song follows picture, by stretching (152 -> 107)
Keep the picture exactly as cut. Stretch the song slower, same pitch, 1.42x
longer. Cost: sound artefacts, must be heard first. This is the big one:
industry guidance is that phase-vocoder / granular stretching stays clean
up to about +/-25%; past that, transients smear, drums lose punch, voices
go metallic/robotic and echoey ("phasiness", loss of phase coherence).
1.42x is a 42% stretch — well past the clean zone. That does NOT prove it
sounds bad on THIS song (synthesised music with few vocals stretches better
than speech), which is why B1 can only be judged by listening, never by math.
Demo built in this folder (see below) — DEMO ONLY, not a final.

### B2 — Song follows picture, by re-performing (107)
Keep the picture. Re-record / re-perform the song at 107 BPM, clean, no
stretch artefacts. Cost: a new performance — new session, new takes, new mix,
new -14 LUFS pass. Cleanest sound, most work. This is the film/TV normal
route when a temp track is replaced: tempo-match the temp, then record the
real cue to picture-locked hit points (see Research below).

### C — Neither moves (decouple)
Keep picture at 107 and song at 152, song just plays underneath as a bed.
Cost: you drop the sync claim. Moves will drift in and out of beat — sometimes
landing, sometimes not — and nobody can honestly say "cut to the beat"
anymore. Cheapest, and the standard route when music is atmosphere, not
choreography. What it loses: the dance/fight feeling that comes from moves
landing on beats.

## Research — how real network shows / TV production actually handle this

Sources used in this job (web search, 2026-11-01): music-to-picture workflow
guides, stop-motion music practice, time-stretch DSP literature. No show is
claimed to have used a specific BPM trick unless a source says so — the
methods below are the industry-standard methods, not invented show anecdotes.

1. **Picture lock first, then score to it (the normal TV/film order).**
   Edit to picture lock with a temp track, then the composer/music editor
   tempo-matches the temp and writes/records to locked hit points. The
   temp is a placeholder, the final cue is built to fit the locked picture,
   not the other way round. That is B2 in this show's terms.
   (MusicTech, producing music to picture: import movie, place markers,
   lock markers to SMPTE, not bars/beats.)

2. **Lock markers to SMPTE/time, never to bars/beats.**
   A hit point (a punch lands, a door opens, a cut happens) is a TIME
   (e.g. 00:00:12:10 at 24fps). If you lock it to "bar 3 beat 2" and then
   change tempo, the hit point moves in time and sync breaks. Locked to
   SMPTE, a tempo change moves the bars, the hit point stays put, and you
   can see exactly what has to be re-timed. This is wired into the tempo
   map in this folder.

3. **Music leads (the animation / musical-number order).**
   The other normal order, used for musical numbers and dance: record the
   song first, edit the animatic over the soundtrack to set the tempo for
   the whole piece, then fit the subtler movements and gestures to the
   bits. That is A in this show's terms. (Gasek, "Let the Music Lead":
   first the drawn animatic is edited over the soundtrack, creating a
   general tempo, then the 3D animatic fits movements to the bits.)

4. **Mickey Mousing / cutting to the beat.**
   When action is timed to land exactly on musical beats — the classic
   cartoon / music-video technique — the beat grid IS the timing chart.
   Cuts, impacts and steps sit on beats, holds sit between them. If you
   decouple (C), you lose Mickey Mousing by definition: the grid and the
   action no longer share a clock.

5. **Time-stretch only inside its clean zone, otherwise re-perform.**
   Phase-vocoder stretching (Audacity's lib-time-and-pitch, Ableton
   Complex Pro, and similar) keeps pitch while changing duration, but
   above ~25% the trade-offs bite: pre-echo and smearing on transients,
   metallic/phasy vocals, flattened dynamics, ghost notes blurring.
   WSOLA (time-domain overlap-add) is kinder to single voices but worse
   on dense polyphonic music. A 42% stretch is outside the clean zone for
   either family, so B1 is a listen-first decision, never a math decision.
   Small shifts (e.g. 124 -> 110 BPM, ~13%) are routinely inaudible;
   152 -> 107 (42%) is not in that class.

6. **Temp-track trap.**
   If a temp track sets the audience's expectation, replacing it with a
   differently-tempoed final cue feels wrong even if it is technically
   in sync. That is why the decision is made at picture-lock / spotting
   time, not after the mix — and why this show's decision is post-episode
   by design (Space Ghost workflow: episodes first, dialogue/audio after),
   not a blocker now.

## Reverse-engineering — what each option does to THIS show, measured

- Existing mixes (both -14.0 LUFS PASS, v2): 107 BPM = 17.94s = 430.6 frames
  at 24fps; 152 BPM = 12.63s = 303.1 frames. Ratio 17.94/12.63 = 1.420 — exactly
  the 152/107 ratio, confirming both mixes are the same musical content at
  two tempos, not two different songs.
- Stretch demo built here: 152 v2 mix through ffmpeg atempo=0.70395
  (107/152) -> **17.94s**, matching the native 107 mix length to 0.01s.
  Loudnorm measure on the demo: input -14.21 LUFS, true peak -2.89 dBTP
  (same peak as the 152 source). That measures loudness, NOT artefact
  quality — artefacts are judged by ear, which is why the demo exists.
- Animatic: 332 frames = 13.83s = 24.7 beats at 107, 35.0 beats at 152.
- Re-time cost, A: every 1-beat move 13.46f -> 9.47f (-3.99f, -29.6%);
  every 4-beat bar 53.8f -> 37.9f (-15.9f). Holds and inbetweens must be
  re-counted, not just sped up, or motion reads rushed.
- Re-time cost, B1: zero picture work, all risk in sound. 42% stretch.
- Re-time cost, B2: zero picture work, one new performance + mix + LUFS pass.
- Re-time cost, C: zero work on either side, sync claim dropped.

## 5 industry-standard things wired 100% in this folder

1. **Beat-grid timing chart** — beat-grid-chart-20261101.png +
   beat-grid-107-vs-152-20261101.csv (33 beats, 0-32, frame + time at both
   tempos). Use: lay any shot's key frames on this grid, see instantly
   which beats they land on at 107 vs 152.
2. **Tempo map** — tempo-map-20261101.json. Beat/bar lengths, stretch
   factors, existing-mix durations, animatic beats, and the SMPTE-lock rule.
   Use: the single source of truth for any re-time job; hit points go in
   here as times, never as bar numbers alone.
3. **Re-time calculator** — retime-calculator-20261101.csv/.json +
   build_tempo_tools.py (re-runnable). Converts beats<->frames<->seconds
   at 107 and 152, both directions. Use: "this move is 2 beats" -> frames
   at either tempo, no hand math.
4. **Stretch demo + A/B listen sheet** — stretch-demo-152-to-107-DEMO-20261101.wav
   (ffmpeg atempo 0.70395, 17.94s, -14.21 LUFS measured) + A/B-LISTEN-20261101.md.
   Use: listen to demo vs native 107 mix, same length, judge B1 by ear.
   DEMO ONLY — not a final, not a mix, not approved.
5. **Sync-decision template** — SYNC-DECISION-TEMPLATE-20261101.md.
   One page per option (A / B1 / B2 / C): what moves, what it costs, what
   it loses, what must be heard/seen first, decision line left BLANK for Mars.
   Use: fill it in when the post-episode decision is made, file it with the
   episode, so the choice is recorded, not re-argued.

## Approval
Tempo pick: **0/1, still owed, NOT made here.** This job explains the choice
and wires the tools to judge it. It does not pick A, B1, B2, or C for Mars.
Post-episode, not a blocker.
