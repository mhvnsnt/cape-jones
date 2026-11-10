# Audio Map — Gumball "The Words" (GB214), Sc057 + Sc059

*Production science, study A of 3. Measured 2026-11-02 from the production
FLA/SWF files. Terms: a **frame** is one scene frame at 25 fps. **dBFS** is
level against digital maximum. Data behind this document:
`data/audio-frame-rms.csv` (level for every frame), `data/audio-events.csv`
(labeled events), `data/movement-math.json` (all numbers), and the recovered
tracks in `audio/`.*

---

## 1. What audio actually exists in the production files

Each scene's FLA holds **exactly one sound object** — a per-shot working mix.
There are no stems, no separate dialogue/music/SFX files, and no event sounds
anywhere in either file. The dissection:

| Layer of the file | Sc057 | Sc059 |
|---|---|---|
| Sound item in the FLA library | `GB214_WORDS_057.aiff` | `GB214_WORDS_059.aif` |
| Original format | 44,100 Hz, 16-bit, **mono** | 44,100 Hz, 16-bit, **mono** |
| Length | 349,264 samples = 7.920 s = **198 frames exactly** | 185,212 samples = 4.200 s = **105 frames exactly** |
| Where it came from (path stored in the FLA) | `N:/08_ANIMATION/03_SHOT BREAKDOWNS/MONO AIFFS/GB214_WORDS_057.aiff` | `./03_SHOT BREAKDOWNS/MONO AIFFS/GB214_WORDS_059.aif` |
| In the scene | one `audio` layer, one keyframe, full shot length | one `audio` layer, one keyframe, full shot length |
| In the published SWF | 1 stream-sound header (MP3, 11,025 Hz) + **198 stream blocks — one per frame** | same, **105 blocks** |
| Event sounds (DefineSound / StartSound) | **0** | **0** |
| Second track in the file | the approved **layout movie** (FLV, 1280×720, stereo 44.1 kHz audio in its metadata; stored in Flash's internal media format — its audio could not be decoded with the tools on hand) | same |

Three facts worth learning from:

1. **The track is cut to the shot, to the sample.** 349,264 samples is 198
   frames at 25 fps (within 8 samples). The sound department didn't hand
   animation "the episode audio" — they cut one mono AIFF **per shot** (the
   folder is literally called *SHOT BREAKDOWNS / MONO AIFFS*) and the
   animator animated to that.
2. **Mono is deliberate.** A mono breakdown is all an animator needs for
   timing, it survives any playback setup, and it keeps the pre-mix cheap.
   The stereo/spatial mix is a post-production job (see §5).
3. **The FLA's track is high quality; the SWF's is not.** The FLA stores the
   44.1 kHz original. Flash's publish step compresses the stream sound to
   11,025 Hz MP3 for the SWF — fine for review copies, which is all the SWF
   ever was.

## 2. The beat — measured, not assumed

Tempo analysis (autocorrelation of the onset envelope, cross-checked with a
grid fit) gives the same answer in both shots:

| | Sc057 | Sc059 |
|---|---|---|
| Tempo | 111.7 BPM | 112.3 BPM |
| **Working number** | **≈112 BPM → one beat = 13.4 frames at 25 fps** | same song, same tempo |
| Phrase structure | a two-hit figure — strong hit, second hit ~6 frames later — repeating every **54 frames (4 beats, 2.16 s)** | accents once per beat through the twist |
| Beat grid phase (frame of beat 1) | ≈ frame 3.7, then every 13.4 | ≈ frame 3.3, then every 13.4 |

**The two shots' tracks are not phase-continuous.** If Sc059's track were the
same uncut song continuing from Sc057, its beat grid would land at phase
≈6.7; measured is ≈3.3. Conclusion: each shot's AIFF was cut independently
from the episode's music, starting at that shot's own frame 0. (The two shots
are also not necessarily adjacent in the finished episode.) This is normal
per-shot breakdown practice — and it means **sync is always local to the
shot**, which is exactly how the files are built.

**The in-file beat layers are counting aids, not the lock.** Sc059's puppet
has a `beat` layer with 14-frame spans (nominal 107 BPM). Measured against
the real audio grid, that layer sits ~6 frames (about half a beat) off and
drifts ~0.6 frames per beat, because 14.0 ≠ the true 13.4. It tracks the
off-beat side of the pulse — close enough to count against the layout movie,
not frame-accurate against the final track. Masami's library puppet carries a
`BEAT` layer on 10–11-frame spans (~143 BPM) that matches **neither** grid —
a leftover from when the GB200 series library puppet was built, not this
scene's tempo. The true sync lives in the pose keyframes themselves (§3).

## 3. Sync map — where the sound and the animation shake hands

Frame precision. Animation events are from `MOVEMENT-MATH.md`; audio events
from `data/audio-events.csv`.

**Sc059 — the twist is fired by the track:**

| Frame | What happens |
|---|---|
| 43 | The `twist` layer's first active keyframe. The strongest-class audio accent lands at **frame 43.4** — the move starts *on* the hit, within half a frame. |
| 43–56 | The bed pulls back under the twist (frame RMS falls from ~−12 to −31.5 dBFS at frame 53) — the accent at 43 is staged by the dip behind it. |
| 56.9 | Next beat accent (13.5 frames later) — twist is mid-run, keyed on twos. |
| 63.7 | Half-beat syncopation. |
| 70.2 | Strongest onset in the scene — third beat accent of the twist's first half. |
| 97 | The twist layer ends (last 2-frame keyframe) and exits on an 11-frame hold. No audio accent here — the exit is the animator's, not the track's. |

**Sc057 — phrase hits structure the strut:**

| Frame | What happens |
|---|---|
| 37.5 / 43.6 | First two-hit phrase figure (strongest onset in the scene = 37.5). Darwin is in his stride cycle, keyed on twos throughout — no pose is held for the hit; the *music* phrases, the body doesn't stop for it. |
| 89–91 | The track nearly drops out (frame RMS −28.0, **−33.9**, −24.2 dBFS)… |
| 91.5 / 92 / 97.6 | …and slams back (−10.4 dBFS) into the second phrase figure at 91.5/97.6. The hole before the hit is the staging trick: the accent reads bigger because the floor fell out first. |
| 126–131 | A second, softer sag (−21 → −26 dBFS) before the level recovers at 132. |
| 145.5 / 146 / 151.6 | Third phrase figure; frame 146 is the loudest single frame of the shot (−9.9 dBFS). |
| 184.9 | Late off-beat hit — then the track is cut mid-phrase at the out-point. The shot ends before the figure resolves; the resolution belongs to the next shot's track, not this file. |

**Footsteps:** there is no separate footstep track and no per-step SFX hits —
the onset pattern is musical (phrase figures + grid accents), not foley.
Darwin's steps are carried by the beat, not by planted sound effects. In the
finished episode, any foley was added in post; in the animator's file, the
music *is* the footstep track.

## 4. Level and shape — a working mix, deliberately not a master

| | Sc057 | Sc059 |
|---|---|---|
| Peak | 0.0 dBFS | 0.0 dBFS |
| RMS | −16.5 dBFS | −14.4 dBFS |
| Integrated loudness (BS.1770) | −16.6 LUFS | −15.1 LUFS |
| True peak | **+2.11 dBTP** (over) | +0.02 dBTP |
| Loudness range (LRA) | 0.4 LU | 1.6 LU |
| Energy under 250 Hz | 59% | 46% |
| Energy 250 Hz–4 kHz | 35% | 53% |
| Spectral centroid | 4,171 Hz | 2,941 Hz |
| Pitched (tonal) frames | 41% | 80% |

Read: both tracks are **hot and flat** — normalized to full scale, almost no
loudness range, running at a constant working level. Sc057 is bass-led (the
strut's thump); Sc059 is mid-forward and far more tonal (80% pitched frames,
almost nothing above 4 kHz) — a closer, duller bed for the close-up. None of
this is a broadcast master, and it isn't supposed to be: for comparison, a
finished show must land at **−24 LKFS (ATSC A/85, US) / −23 LUFS (EBU R128,
EU)** with true peak at **−2 / −1 dBTP**. These files sit ~7–8 LU hot with
true-peak overs. Final loudness is set in post-production, on the full mix,
with dialogue/music/effects stems — none of which exist at the animation
stage. The animator's track only has to be *timed* right and *feel* right.

## 5. How a sound department actually lays this out (the industry reading)

The standard TV-animation sound workflow, and where these files sit in it:

1. **Voices first.** Dialogue is recorded before animation; animators time
   mouths and acting to the recorded track. (Universal practice for US/EU TV
   animation — the reverse, post-sync, is the dubbing workflow.)
2. **Animatic.** The editor cuts storyboard panels against the voice track
   and temporary music/effects (a *scratch track*). For Gumball, creator Ben
   Bocquelet's published account names editor Richard Overall as managing
   the animatic and the voice recording, with composer Ben Lockett starting
   the music at the same stage.
3. **Shot breakdowns to animation.** Sound/editorial cuts the track **per
   shot** and ships it to the animators — *this is the stage our files are
   from*, proven by the `03_SHOT BREAKDOWNS/MONO AIFFS` folder, the
   frame-exact lengths, and the mono working format.
4. **Animation keys to the track.** Accents become animation events (the
   twist at frame 43). Music-driven scenes may also get a **bar sheet** —
   the musical equivalent of a dope sheet; the in-puppet `beat` layers in
   these files are that function, kept inside the FLA.
5. **Post-production sound.** Final score, sound effects, Foley, and the
   full mix (dialogue/music/effects stems) are built against the finished
   picture, then mastered to the delivery loudness spec. For Gumball,
   post-production was handled in London (Fitzrovia, per Bocquelet's
   account) after animation at Boulder Media (Dublin) and Studio SOI
   (backgrounds/3D).

**Cape Jones takeaway:** our pipeline already matches the shape — finished
songs (the EN/JP dance mixes are final and approved) before dance animation,
dialogue handled in post by design (owner's method: record lines after, lip
sync with MouthSwap). What this scene adds: **cut the audio per shot, to the
exact frame count, before the shot is animated** — and treat that mono track
as a timing document, not a master.

## 6. Files in this study

- `audio/GB214_WORDS_057_track.wav`, `audio/GB214_WORDS_059_track.wav` — the
  per-shot tracks, recovered bit-exact from the FLAs' internal media stores
  (the original 44.1 kHz 16-bit mono PCM) and wrapped as WAV. These are the
  only separable audio objects in the production files — the "stem" is the
  shot track itself.
- `data/audio-frame-rms.csv` — RMS level for every frame of both tracks.
- `data/audio-events.csv` — every labeled event used in §3.
