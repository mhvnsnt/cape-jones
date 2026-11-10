# SOURCES AND METHODS — Space Ghost Workflow, 2026-10-31

Public sources only. URLs below are copied verbatim from web search results
returned during this workstream. No SGC2C script dialogue, character, name,
or logo is reproduced here — only production-method facts, per the standing
show-building barred list.

## A. Space Ghost Coast to Coast — picture-first production

Claim: SGC2C was built by re-editing / tracing over existing 1960s
Hanna-Barbera *Space Ghost* footage the channel already owned, on a low
budget, reorganised into a talk show with crudely animated lips delivering
new dialogue; continuity errors and limited, jerky movement became the
signature.

- https://diffsense.com/why-space-ghost-coast-to-coast-still-feels-like-a-fever-dream-1zrh
  ("built on the cheap, using recycled animation cells"; "they just traced
  over the old frames"; "mouth flaps and the occasional power band blast").
- https://www.cracked.com/article_37137_space-ghost-coast-to-coast-how-a-hanna-barbera-talk-show-started-an-entire-comedy-counter-culture.html
  ("hastily editing footage from the original Hanna-Barbera series and
  reorganizing it into a talk show with crudely animated lips delivering
  the new dialogue").
- https://medium.com/@jsbegy/the-anti-televisual-politics-and-aesthetics-of-space-ghost-coast-to-coast-a40555df4e37
  (same Kelly quote on hasty editing + crudely animated lips; long silent
  stares as expressive despite crude animation).

Claim: celebrity interviews were filmed separately, largely
improvisationally, then combined / re-cut with the cartoon dialogue, often
producing results opposed to the original questions' context.

- https://grantland.com/hollywood-prospectus/the-phantom-fame-space-ghost-coast-to-coast-secretly-tvs-most-influential-show/?ex_cid=story-twitter
  ("Interviews with the celebrities involved were filmed separately, in
  largely improvisational fashion, then combined with the cartoon
  characters' dialogue").
- https://diffsense.com/why-space-ghost-coast-to-coast-still-feels-like-a-fever-dream-1zrh
  (team flew to New York / Los Angeles, sat a celebrity in front of a green
  screen, talked to a puppet or producer, then chopped the footage up in
  Atlanta and re-edited the questions).

Claim: format and origin — Mike Lazzo / Ghost Planet Industries (later
Williams Street), Cartoon Network's first original series and first animated
talk show, 1994 launch, ~12-minute episodes, host at desk with Zorak as
bandleader and Moltar as director, guest on a monitor screen.

- https://williamsstreet.fandom.com/wiki/Space_Ghost_Coast_to_Coast
  (low-cost method: re-edit owned property, superimpose over live-action
  sequences; satirical talk-show concept; original run April 15, 1994 –
  May 31, 2008 across runs).
- https://www.cracked.com/article_37137_space-ghost-coast-to-coast-how-a-hanna-barbera-talk-show-started-an-entire-comedy-counter-culture.html
  (Lazzo launched Ghost Planet Industries, later Williams Street; 11 p.m.
  Friday launch; talk-show format with celebrity guests).

## B. Standard dialogue-after-picture / ADR / post-sync practice

Claim: ADR (Automatic/Additional Dialogue Replacement, UK: post-synchronisation
/ post-sync, also "looping") is re-recording dialogue in a controlled studio
after filming, with the actor watching picture, to replace unusable production
sound or to change lines for clarity, diction, or timing.

- https://krotos.studio/blog/adr-film
  (ADR workflow: locked picture reference with handles + line list with
  scene/shot/timecode/character/emotion/breaths/lip beats; markers at first
  frame of each line; multiple takes; best-take selection; stems delivery).
- https://www.liquisearch.com/dubbing_filmmaking/automated_dialogue_replacement__post-sync
  (definition, post-sync naming, ADR supervisor review, animation note:
  dialogue recorded to a pre-edited version; ADR needed when cast cannot all
  be present at once).
- https://voiceoverla.com/adr-101/
  (looping with 3-pop cue, mic placement, ambience/reverb matching, select
  take on the spot, alternates saved as backup).
- https://github.com/kmgrassi/popcornready/blob/HEAD/docs/research/voiceover-adr-data-models.md
  (cueing aids: beeps, countdowns, streamers, line text; deterministic
  references: SMPTE timecode, clip boundaries, handles, metadata; stems and
  Music-and-Effects packages conformed to final picture).

## C. The inverted standard (documented to avoid it)

Claim: standard feature-animation textbooks say dialogue is recorded FIRST
and animation timed to it (animatic from recorded dialogue, syllable timing,
then animation, with final lip sync last) — and at least one practitioner
source notes this textbook order often fails in practice because actors
struggle to visualise the scene. Either way, it is the OPPOSITE order from
Mars's locked Space Ghost order, and is therefore marked INVERTED (SG-12),
not used.

- https://en.wikibooks.org/wiki/Movie_Making_Manual%2FCharacter_Animation
  (textbook order: record dialogue → animatic with dialogue + temp score →
  syllable timing → animation → edit → ADR session reacting to picture →
  final lip-sync animation last).
- https://saturation.io/film-crew-positions/animatic-editor
  (animatic = storyboard panels + scratch dialogue + temp music + SFX as a
  rough moving blueprint; lip-sync timing via mouth-chart phoneme panels
  synced to scratch dialogue — the scratch/temp concept reused here as SG-04,
  with the difference that in this workflow the scratch is replaced AFTER
  picture lock, not before animation).

## D. Cape Jones facts used (local files, not web sources)

- Shot specs + rim/bleed/LUT per shot:
  `clean-100-20261031/shots/shot-specs-30-20261031.md` (30/30 shots).
- QC flags CJ-05/06/26 (rim, neutral exception / grey rim, NOT dual-light):
  `gap-close-tv-20261031/qc-cj01-cj30-20261031.md`.
- Song tempo + options: `mars-sweep-G-20261031/REPORT-20261031.md`
  (152 BPM, C major, 48 bars, 75.8 s; options (a)/(b)/(c); no silent stretch).
- Visual dance grid ~107 BPM, 24 fps, beat 13–14 frames:
  `dance-improved-20261031/BEAT-SHEET.md`.
- Standing rules applied, not changed: version-lock + image-cache
  (new dated filenames, never overwrite Mars-seen files), rim-color rule
  (±20°, dual-light exception only with both sources named), show-building
  method (reference + transformation; barred list), delivery at −14 LUFS
  with audio as LINK, never in chat.

## E. What was NOT verified here

- No SGC2C episode was watched frame-by-frame in this workstream; claims
  rest on the public sources above, not on first-hand viewing.
- No song audio file was found on local disk in this workstream (consistent
  with the sweep-G report); the 152 BPM figure is task-supplied via that
  report, not re-verified from audio here.
- No dialogue line, tempo choice, or rim ruling was verified or decided —
  all three remain Mars's post-episode steps.
