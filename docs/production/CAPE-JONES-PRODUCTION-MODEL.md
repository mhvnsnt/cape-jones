# Cape Jones Production Model

Owner law, set 2026-10-29. This is the standing production rule for the Cape Jones show.

## 1. The model

Cape Jones is made like an Adult Swim show. Space Ghost Coast to Coast and Home Movies are the reference points.

The animation stays simple on purpose. Few frames. Few angles. Long held poses. Plain cuts.

The entertainment does not come from movement. It comes from lighting, segments, writing, comedy, editing, voice and sound. That is where the work goes.

Cape Jones is not made like Pokemon. Pokemon-grade production means hundreds of shots and thousands of drawings per episode. That is a different model with a different budget. We do not chase it.

The cheapness is part of the show. We do not hide it. We make it funny.

## 2. The spec

Animation targets for an 11 minute episode:

- The timeline is 24 fps. Dialogue and ordinary business are animated on threes and fours. That is 8 or 6 new poses per second.
- Held poses run 1 to 5 seconds or longer. A frozen face held in silence is a tool, not a mistake.
- Twos (12 poses per second) are reserved for one or two big moments per episode. Ones are never the default.
- New poses per episode stay in the low hundreds. The pose library comes first. A new pose is approved only when a joke cannot land without it.
- Cuts per episode: about 40 to 80. Most cuts are the wide of the set, a close on speaker A, a close on speaker B, and a reaction hold.
- Typical shot length is 5 to 15 seconds. Cut fast only for a specific gag.
- Camera angles: 2 to 3 locked angles per location, for the whole series. One wide, one close, one reverse or reaction. A new angle costs a new background and a new pose set. Treat it like buying furniture.
- Sets: 2 to 4 standing sets per episode, built once and reused across the series. Change the mood instead of the architecture: day, night, lights off, one prop swapped.
- Every character has a named pose library: neutral talk, point, shrug, head turn, blink, mouth sets, one signature gesture.
- Nobody walks. A character appears in the next position on a cut, or bobs and slides if the move has to be seen. Big actions happen as cutaway and cut back. Effects like a zap or an explosion are one reusable clip, used the same way every time.
- A new pose must be reusable in at least 3 episodes.
- In dialogue, only the mouth and the blink move. A brow raise or a head tilt is the big acting choice.

Decision rule: if a scene needs a new location, a new angle, a walk, a fight, or a transformation shown on screen, rewrite the scene. Move the event into dialogue, sound, a cutaway, a title card, or a reusable clip. If a scene is funny as audio alone, it is ready to produce.

## 3. Why this model

Pokemon, per OLM producer Hiroyuki Kato in AWN: over 300 shots and 4,000 to 5,000 individual drawings per episode. That volume buys a new layout and new angles on nearly every cut.

Space Ghost Coast to Coast, episode 1: animator C. Martin Croker needed only 5 new pieces of animation. The rest came from the existing footage library (Mental Floss). The show still ran for years.

The gap between those two numbers is the whole decision. We spend on writing, voices, editing, lighting and sound instead of drawings.

## 4. The non-animation checklist, and where each part already lives

Writing first, pictures last. Record the episode. Edit the sound into a funny radio play. Only then put pictures under it. If it is not funny with your eyes closed, more animation will not save it.

- Lighting and mood. Looks and grades live in docs/lighting/ (COLOR-GRADES.md, LED-CONTROLLER.md, RENDER-LOOKS.md). Tooling lives in tools/lighting/. The LED engine lives in production/pipeline/: led_controller.py, led_scene_assembler.py, LED-SCENE-ASSEMBLER.md. Status: wired and in use. This is the gag engine. A lighting change on a held frame is an act break, a menace, or a punchline at zero drawing cost.
- Voice. The Wizard Gang voice pipe (repo mhvnsnt/wizard-gang-voice-pipe, Chatterbox) is proven and carries over. In this repo: production/pipeline/tts_voices.py, tts_voices_2026.py, voice_convert.py. Cast for contrast and timing. Record loose. Keep the accidents.
- Segment structure. An 11 minute episode is 2 to 3 bits, not one thin plot: a cold open in the standing set, one long dialogue set piece, one escalation with a reusable effect, an abrupt ending. Reference research sits in repo mhvnsnt/mystery-coast-ghosted, docs/research/: SGC2C-PRODUCTION.md, HB-LIMITED-ANIMATION.md, CAPE-JONES-TRANSFER.md. Fold-in to this repo is pending. See the gaps below.
- Writing and gags. Scripts live in docs/story/ (EP01-IMMORTAL-QOMBAT-SHOOTING-SCRIPT.md). The Fountain pipeline is production/pipeline/fountain_to_animatic.py and fountain_to_beats.py. Gag mechanics live in repo mhvnsnt/God-Molecule-Show-Studio, docs/research/wave2/JOKE-MECHANICS.md. Build in a retroscripting pass: outline the scene, record more than needed, let actors overlap and go off script, then mine the edit for jokes.
- Editing. Editing is a creative job here, not a finishing step. The tools are the pause left in, the answer moved to a different question, the reaction held one beat too long. Tooling: the ffmpeg chains in production/pipeline/ (ffmpeg-animation-filters.sh, trackA-ffmpeg-fx-chains.sh) and finish.py.
- Sound and music. Docs: docs/soundtracks/SOUNDTRACKS.md. Generators: production/pipeline/music_gen.py and sfx_gen.py. Sound is the action in this model: room tone, signature effects for every reusable action, stingers, deliberate silence. Music is a character, not a background.
- Sets and poses. The standing living room set is 3d-assets/living-room/ (SCENE-CANON.md, INTEGRATION.md, and its own lighting rig). The named sitting pose library is 3d-assets/cape-jones-rig/SITTING-POSE-LIBRARY.md.
- Title cards. docs/story/ep01-title-card/ holds the EP01 card, the generator make-title-card.py, and the animated card. Cards cover scene changes, so we never need establishing shots.

## 5. Gaps, named as build items

1. Bumper library. No bumper or interstitial library exists yet. Build one: short written jokes as white text on black cards, Adult Swim style. The card writer is a writer on the episode.
2. Shot and angle library. There is no named shot or camera-angle library. Catalog the locked angles by name, the way Space Ghost reused its desk shots, so every episode pulls shots by name.
3. Research fold-in. The production research in mhvnsnt/mystery-coast-ghosted docs/research/ (SGC2C-PRODUCTION.md, HB-LIMITED-ANIMATION.md, CAPE-JONES-TRANSFER.md) needs folding into this repo's docs.
4. Show bible tone. docs/SHOW-BIBLE-SEED.md has tone sections that are still TBD. They are the owner's call. No agent fills them in. This doc points at them and leaves them alone.

## Sources

- AWN, OLM Asia Launches New Pokemon Animation Series with the Help of Celsys' Clip Studio Paint. Producer Hiroyuki Kato: over 300 shots, 4,000 to 5,000 drawings per episode. https://www.awn.com/animationworld/olm-asia-launches-new-pok-mon-animation-series-help-celsys-clip-studio-paint
- Mental Floss, 15 Things You Might Not Know About Space Ghost Coast to Coast. Five new pieces of animation for episode 1, plus budget and production notes. https://www.mentalfloss.com/entertainment/tv/15-things-you-might-not-know-about-space-ghost-coast-coast
- Full research: Pokemon vs. Adult Swim production models, 2026-10-29 (AWN, Mental Floss, Creative Loafing, Nerdist, and the Home Movies and Squigglevision production accounts).
