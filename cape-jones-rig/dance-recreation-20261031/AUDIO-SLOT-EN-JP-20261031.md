# Audio slot — English + Japanese versions (same visual cut)

Status: SILENT. No song invented. No audio track in the MP4s.

## Timing grid (shared by both language versions)
- Playback: 48 fps video. Original phrase grid: 24 fps, ~107 BPM,
  beat = 13-14 frames. Beat starts (24fps grid): 1, 15, 28, 42, 56,
  69, 83, 97, 110. At 48fps, beat starts are exactly double:
  2, 30, 56, 84, 112, 138, 166, 194, 220 (frame indices, 1-based
  on the 48fps timeline; Recreation A ends at 217, Recreation B at 215,
  i.e. the phrase tail is the final breath hold — see beat sheet).
- Edit points: beat starts above. Both language versions cut on the
  SAME points. Language is a track swap, never a re-edit.

## Track layout (to be filled when Mars supplies audio)
| Track | Contents | Status |
|---|---|---|
| V1 | Recreation video (A or B), 48fps, silent | DONE |
| A1-EN | English version of the song, full length, same tempo/grid | OWED — Mars-only input |
| A1-JP | Japanese version of the song, full length, same tempo/grid | OWED — Mars-only input |
| A2 | (optional) metronome/beep guide, muted in final | NOT mixed in |

## Swap procedure (when audio arrives)
1. Place EN audio on A1-EN, JP audio on A1-JP, both starting at
   video frame 0 (beat 1 = first downbeat; if the supplied audio has
   a lead-in, offset it so its first downbeat lands on beat 1 and
   record the offset here — do not re-cut the video).
2. Mux two versions from the SAME video file: *_EN.mp4 (V1 + A1-EN),
   *_JP.mp4 (V1 + A1-JP). No frame changes between versions.
3. If EN and JP recordings differ in tempo/length, that is a
   Mars decision (re-time the audio, or accept drift) — do not
   silently stretch the video to fit one language.

## What Mars must supply (one input)
- Song title / which song, AND the English audio file + the Japanese
  audio file, OR his instruction to source them. Until then, these
  videos stay silent and are not presented as finished song videos.
