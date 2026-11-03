# The Bumpkin — Sc089: top-shot tableau — Nicole, Anais and Darwin flat on the ground (KeyAnim)

**Episode:** GB222 "The Bumpkin" (Season 2) · **Scene:** Sc089 · **Frames:** 177 @ 25fps · **Source:** GB222Bumpkin_Sc089_KeyAnim_V008.fla (63,909,731 bytes — the largest FLA in the batch)

## Story / beat
The camera looks straight down at a grey ground plate. Nicole, Anais and Darwin lie flat in a diagonal row — Nicole centre, Anais lower-left, Darwin right — and stay there for 177 frames, talking. Anais speaks through the first half (mouth comp working f23–89), Darwin answers in the second (f111–155), and Nicole's reactions take over at the end: her look shifts sideways at f133 and turns worried by f177 while Darwin glances up.

## Cast
- **Nicole** — GB200_MOM_ORIGINAL_PUPPET_V001 (281 kf) on its own scene layer named for the puppet. Centre of the tableau; mostly reaction.
- **Anais** — GB200_ANAIS_ORIGINAL_PUPPET_V001 (309 kf). Lower-left; first speaker.
- **Darwin** — GB200_DRW_ORIGINAL_PUPPET_v001 (278 kf). Right; second speaker.
- No Gumball: this is a Watterson scene built entirely without him.

## Construction
- One locked background: GB222_BUMPKIN_Sc089_LO_BG.jpg (bitmap plate, frames 0–177) — a grey mottled ground texture read from directly overhead.
- Dead-simple stack: three puppet layers (one per character, named for their puppet symbols) over a white shape layer and the background, plus audio, framecounter, fieldguide and the 'layout mov' reference layer.
- The 63.9 MB FLA parses to only 15 animated symbols: the bulk is library head/face-comp depth, not scene complexity. The parse completed cleanly (no OOM).

## Techniques (tags + evidence)
- **multi-character-staging** — three characters staged in one held overhead shot for 177 frames, each on its own scene layer over a single ground plate (manual, layers + sheet).
- **face-comp-driven** — face comps 3,206 kf vs body puppets 868 kf; Anais mouth comp 457 kf is the largest symbol (auto).
- **layout-mov-reference** — scene carries a 'layout mov' reference-video layer (auto).
- KeyAnim state: heads are finished colour comps; every body below the neck renders as red rough construction lines in all 177 frames (sheet).

## What Cape Jones steals from this scene
- The overhead tableau: lay the cast flat under a top camera and a dialogue scene needs no staging moves at all — heads in a row, mouths and eye-lines do the blocking.
- Speaker rotation by face comp: Anais → Darwin → Nicole's reactions. In a held shot, who talks is who moves; plan the comp budgets accordingly.
- A scene can be carried entirely by the 'B' cast: no lead character, no problem — three reacting heads are a complete scene.

## Media status
- Contact sheet: done (177 frames). Video: done, production audio muxed from the SWF sound asset. Frames rendered: 177/177.
- Render history: two FFDec attempts (172/177 cached by the first attempt's timeout, completed by the second).

## Gaps / honesty
- The red rough bodies are the file's KeyAnim state, not a render fault: the SWF exports heads clean and bodies rough, and the sheet documents it as-is.
- The scenes index describes Sc089 as a 'giant-scale sequence'; nothing in this file's placements or the render supports a giant-scale gag — the characters are large in frame because the overhead camera is close. Recorded as a correction to the index note.
