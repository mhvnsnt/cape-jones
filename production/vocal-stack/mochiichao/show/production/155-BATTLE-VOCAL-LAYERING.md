# #155 — BATTLE VOCAL LAYERING → cries, in chorus, without ever becoming speech

**Seat in the doctrine:** creatures speak in cries —
only cries, ever (the voice law). #2 built the synth
(37 classic base cries differentiated by (base, pitch,
length) triples; per-species cry blocks in the sheet
schema), #95 built the variation engine with its
identity-floor rule, and #84 bound a place's sounds to
its roster. Battle is where cries stack: two combatants,
a Garden crowd, a show scene with six creatures in frame.
Layering is where a cry system can quietly break its own
law — stack enough voices and the ear starts hearing
crowds, choruses, almost-words. This spec is the layering
grammar that keeps stacked cries *cries*.

**What was studied.** Vocal layering in the publicly
documented record: game audio practice layers creature
sounds by *priority and thinning* (the featured voice
plays whole; background voices are fewer, quieter, and
never simultaneous at full weight), and chorus effects
come from offset and spread, never from synchronised
identical voices (which read as one loud voice, or as a
chant). Animation sound design adds the show rule: in a
multi-creature scene, one creature *speaks* at a time
even when the sound is wordless — the mix directs the
ear the way the camera directs the eye. The kit taken:
priority classes, a simultaneity budget, and offsets —
all parameterised over the cry records that already
exist.

## Native spec — layering grammar over #2/#95/#84 (records ride the #51 SFX classes)

- **Priority classes** (closed): `featured` (the acting
  creature — full cry, unmodified params except #95's
  jitter), `answer` (the opposing/responding creature —
  full cry, sequenced *after*, never under, the featured
  cry's attack portion), `chorus` (background individuals
  of present species — thinned: at most one cry per
  species per beat, params at the species' base with
  #95 jitter, level under the featured pair). A layer
  stack names its members by class; a sound not in a
  class is not in the stack.
- **The identity floor binds the stack.** #95's rule —
  jitter clamps to under half the distance to the nearest
  sibling species' pitch offset — applies per layer, so
  no chorus member can drift across a species boundary
  no matter how the layers sum. Layering may never make
  one species audible as another; if a proposed stack
  would, the stack is wrong, not the rule.
- **Simultaneity budget.** At most two full-weight cries
  overlap at any instant (featured + at most one other),
  and chorus entries enter on offsets, never on the
  featured cry's onset. The budget is what keeps a
  six-creature scene a scene instead of a wall — and it
  is also the voice law's enforcement at mix level:
  nothing in the grammar can produce the call-and-
  response *cadence of conversation* at full weight,
  because answers are sequenced, bounded, and thinned
  by construction.
- **Battle sequence joins.** The battle presentation
  reads the stack at its existing beats: intro (#10's
  INTRO — entrants cry in fixture order), move
  performance (#9's animscript cue points may carry a
  vocal cue referencing the performer's cry record —
  the cue is a reference, the params stay #2's), damage/
  faint beats, and the living-field ambience (#10's
  read-only LIVING_FIELD: chorus class only, and —
  per the battle doctrine — the layering is
  presentation: it reads battle state, it never writes
  it).
- **Show mirror.** Episode mixes use the same classes
  and budget (the show's cry work already runs on the
  synth — this gives its battle and crowd scenes the
  grammar the game uses), under the subtitle law as
  usual: cries are not subtitled; comprehension is
  #136's staged reads, in the Ranger's face, not in
  captions of creature sound.

## Open slots (nothing invented)

Chorus thinning ratios and level offsets (mix values —
production measurements, OPEN) · whether `answer` may
ever overlap on a *finishing* beat (a double-KO tableau
is the arguable case — recorded as a question for the
audio lane, not settled) · per-species chorus behaviour
for species whose profile (#152) is `colony` (a colony
species' chorus may be denser — the profile says; the
interaction is specified, the values are not).

---

**Landing citation — List 32 (2026-10-27).**

#313 ghost spectacle (`battle/313-GHOST-SPECTACLE.md`) reads this file's vocal floor as one of its staging seats (presence before form; closeness, not size, is that family's climax). The citation is reciprocal with #313's spec; no vocal rule in this file changes.
