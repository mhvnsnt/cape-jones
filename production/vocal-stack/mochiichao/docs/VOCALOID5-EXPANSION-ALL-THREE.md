# Vocaloid 5 expansion — all three lanes, plus everything else reverse-engineered

Owner instruction 2026-10-28: all of it, plus anything else that can be
reverse-engineered, into this full stack, straight from the Mochi Chao repo
work, so music can start being produced for the shows, the repos, and the
games. This file is the expansion draft, in the local consolidation folder.
It is NOT yet appended to docs/FREE-STACK-PRODUCTION-NOTES.md on main,
because main is an orphan single-file commit (93114e0d) — see INDEX.md.
Append it to the notes file once a clean repo base is chosen, do not
overwrite the notes file with it.

Paid tools remain method references only. The 2.64 GB owned Vocaloid 5
installer is NOT in this folder, NOT in the repo, and NOT downloaded here.

## A. Full Voice Color / control set (Vocaloid 5)

Already landed (teardown, Yameii-style, do not redo):
- CHA +25 to +45, EXC +35 to +50, AIR/BRE +15 to +25, MOU +20 to +40
- VEL 95 to 115, consonant speed not volume
- CHA direction reversed in V5 vs V3/V4: positive shrinks the tract

Full set, by function (not by range, unless the range is the landed set):
- Velocity (VEL): length of the consonant. Increase = consonant shorter,
  decrease = consonant longer. This is why VEL 95-115 gives trap timing:
  it shortens consonants, it does not turn the volume up.
- Dynamics (DYN): volume / expression of the synthesized voice, drawn as
  a curve. This is the volume lane. Do not use VEL as a volume control.
- Pitch Bend (PIT) / Pitch Bend Sensitivity (PBS): PIT is a continuous
  pitch adjustment; PBS sets how far a full PIT swing moves pitch, in
  semitones. Standard MIDI bend range is -8192 to +8191, with a full swing
  at PBS 12 = 1 octave. Vibrato type, position, amount, and frequency are
  separate from PIT, and are set per note.
- Gender Factor / Character (GEN / CHA): formant structure, vocal-tract
  size. Raising = feminine / smaller tract, lowering = masculine / larger
  tract. In V5 this is the Character control in Voice Color.
- Brightness (BRI): brightness of pronunciation, high-range harmonics.
- Clearness (CLE): clearness of pronunciation, high harmonics.
- Portamento Timing (POR): where pitch changes between notes, the slide
  position, not just whether a slide happens.
- Breathiness (BRE): breath mixed into pronunciation and vowel tone.
- Air (AIR): breath mixed into pronunciation. AIR and BRE are related but
  not the same lane: BRE affects vowel tone as well, AIR is breath amount.
- Exciter (EXC): tone of the voice, muffled to bright.
- Mouth Opening (MOU): diction / mouth opening level of pronunciation.
- Voice Color stacking rule (critical edge): Voice Color provides an
  OFFSET to the control parameter that can also be edited in the musical
  editor. So a Voice Color CHA offset PLUS an editor CHA curve PLUS an
  external formant shifter can stack three times. That is the same
  double-formant trap as the landed rule, at a larger scale. For Yameii:
  pick ONE formant authority per bus (inside Vocaloid, or external),
  and leave the others at neutral.
- Vocaloid 5 total, from Yamaha's V5 release material: 13 control
  parameters for adjusting vocals, including 3 new/improved ones in V5
  (Exciter, Air, Breathiness). Do NOT import Vocaloid 6 ranges here:
  the V6 manual lists CHARACTER -64 to +63 and MOUTH -127 to 0, which
  are NOT the landed V5 Yameii ranges above.

## B. FL Studio VSTi integration, expanded

Already landed:
- Editor first, then Avanna V3; update to 5.6.2+ fixes the 48 kHz FL Studio
  crash, otherwise force 44.1 kHz in FL Studio.
- VSTi in FL Channel Rack, routed to a mixer insert; notes/lyrics drawn
  in the Vocaloid Editor window, locked to host BPM/playhead.

Expansion, from V5 external-functionality material:
- V5 supports VST, AU, and external MIDI input. That is the host route:
  Vocaloid as a plug-in in the DAW, not only as a standalone editor.
  Standalone still works for rendering a WAV and importing it, which is
  the fallback if a host route misbehaves.
- Host lock rule: the Vocaloid window follows the host BPM and playhead.
  If the host tempo changes, the Vocaloid part follows the host, it does
  not keep its own tempo. Render / freeze the vocal to WAV before
  changing tempo or sample rate mid-project, or the part will re-time.
- Sample-rate rule, restated with the mechanism: Vocaloid's internal
  operating specification is 44.1 kHz. Pasted / imported audio is
  converted to 44.1 kHz / 16-bit in later Vocaloid versions. That is why
  forcing 44.1 kHz in FL Studio is the safe workaround below 5.6.2, and
  why a 48 kHz project can sound pitched / timed wrong if the host and
  the plug-in disagree, even when it does not crash.
- Channel Rack / mixer discipline for Mochi Chao: one Vocaloid channel
  per voice part (Avanna lead, human digi, etc.), each routed to its own
  mixer insert, so the Deko dual-bus chains stay separate. Do not put
  Avanna and the human digi bus on the same insert, or the formant,
  OTT, and vocoder stages will cross-contaminate.
- Historical note, NOT a V5 limitation: very old Vocaloid (V2 era)
  ReWire did not work properly with FL Studio, and old VSTi hosts that
  did not send NRPNs could not drive it. Do not apply that to V5 VSTi,
  which is a different plug-in generation. If a V5 VSTi problem appears,
  check sample rate, plug-in format (VST3 vs VST2 in FL), and mixer
  routing first, not the old ReWire note.
- NewTone to Vocaloid route, already landed, restated as a production
  step: record the human flow, correct in NewTone, send to Piano Roll,
  export MIDI, drag the MIDI into the Vocaloid Editor. The MIDI carries
  pitch and timing; lyrics and Voice Color still have to be entered /
  tuned inside Vocaloid. MIDI alone does not carry CHA/EXC/AIR/MOU.

## C. Formant / velocity edge cases

These are the failure modes the landed ranges are protecting against.
They are qualitative edges from the landed teardown, not new invented
numbers:

- Chipmunk trap: pitch +12 semitones with formant at 0. The tract
  stretches, the voice sounds hollow, thin, and cartoonish. Fix is
  formant-first: formant +3.5 to +5.5 at pitch 0, then pitch only
  +3 to +7 if moved at all.
- Double-formant trap: CHA raised inside Vocaloid + Little AlterBoy /
  Auto-Tune Throat formant on the same bus. The tract gets shrunk twice.
  Omit the external shifter on the Avanna bus when CHA is already raised.
- VEL too low on fast lyrics: consonants get longer, syllables smear,
  trap timing collapses. VEL too high: consonants get clipped, lyrics
  become unintelligible, especially on fricatives and plosives. The
  landed 95-115 band is the trap-timing band, not a universal setting
  for ballads or spoken lines.
- Vibrato / pitch transition edge: 0-10% gives the robotic, laser-beam
  Yameii clamp (with zero-speed Auto-Tune, humanize 0). Raising vibrato
  and pitch transition re-introduces human wobble, which is correct for
  a human-sounding lead and wrong for the robotic digicore clamp.
  Choose per part, not per project.
- Air / slapback edge: 6-10 kHz shelf + 50-70 ms slapback, zero feedback,
  very low mix gives close, breathy, whisper-in-ear texture. More
  feedback or a longer delay turns it into a room echo and loses the
  hyperpop intimacy. OTT 15-20% (human) / 20% (Avanna bus) pulls breath
  and digital artefacts forward; more OTT pulls noise forward too.
- Recording edge, already landed and repeated because it decides the
  chain: soft head-voice / near-whisper, do not belt. A belted take
  through a formant-raised, OTT-heavy chain sounds harsh and messy,
  no matter how correct the plug-in settings are.

## D. Everything else reverse-engineered in V5 (production stack)

From Yamaha's V5 release material, all method references:
- Style function: around 100 singing styles, including lead vocals,
  background vocals, and robotic vocals. Apply a style, then tune
  Voice Color and control curves on top of it, not instead of it.
  A style is a starting point, not a finished vocal.
- Drag-and-drop song creation: over 2,000 preset phrases and audio
  clips. Use these as phrase starters and reference timing, not as
  final lyrics for Mochi Chao characters.
- Attack & Release effects: icon-selected vocal techniques, sampled
  from actual singers, applied by selecting an icon and copy/pasting
  it onto notes. This is how vibrato and other hard-to-draw techniques
  are applied without hand-drawing every curve.
- Emotion Tool: visualises singing style while showing the waveform;
  mouse control of vocal strength, speed, phoneme length, and related
  settings while watching the waveform.
- 11 kinds of audio effects in the standard V5 package, for complete
  vocal tracks inside one application, before the external DAW chain.
- Voicebanks in V5 Standard: 4 banks — Amy (English female, contemporary,
  R&B to pop), Chris (English male, R&B, soft bass to powerful high
  tones), Kaori (Japanese female, soulful, long sustains), Ken
  (Japanese male, sharp, clear, light, J-pop). Premium adds VY1, VY2,
  CYBER Songman II, CYBER Diva II.
- Compatibility: Vocaloid 3 and 4 voicebanks work in the V5 Editor
  without modification, which is why Avanna V3 loads in V5. Vocaloid
  4.5 Editor for Cubase was included as support software for Cubase.
- Production mapping for Mochi Chao (shows / repos / games):
  - Lead / show songs: Avanna bus (Vocaloid lead) + Deko dual-bus
    glue, rendered to WAV, then mixed in FL Studio.
  - Game voice lines: human digi bus for human characters, Chatterbox /
    voice-kit pipeline for other characters per the repo's standing
    voice rules. Cape Jones is the exception: the owner voices ALL
    Cape lines himself, never synthesized. Do NOT put Cape lines
    through Vocaloid, Chatterbox, or any other synth voice.
  - Beds / menus / arenas: the music-wave chains (Pedalboard voice/bed,
    Digital Fairy chain, loudnorm spine -14 LUFS / -1 dBTP) stay as
    the house spine. The -7 to -9 LUFS mastering benchmark is NOT
    a change to that spine.
  - Free-stack equivalents where they exist: Pedalboard, Basic Pitch
    (replaces NewTone for lead stems), Whisper (QA only), plus
    custom DSP builds still owed (ZDF EQ, true formant warping,
    LR4 OTT, STFT Soothe, Bark vocoder, split-band 808, widener,
    YIN tuner).

## E. Next production / music styles — awaiting owner list

Owner will add more production styles and music styles next. None are
invented here. When that list arrives, each style gets: (1) its vocal
chain variant (which bus, which Voice Color band), (2) its instrumental
stack (which free-stack / custom DSP modules), (3) its house loudness
and routing (which mixer insert, which rotation: show / game / menu /
arena), and (4) its source (teardown, manual, or owner direction).
Until then, this file covers Vocaloid 5, Digital Fairy / Yameii, and
Deko, and nothing else is claimed as a style.

## Sources (public, method references only)

- Yamaha Vocaloid 5 press release / feature overview (Style ~100,
  2,000+ phrases, Attack & Release, Emotion Tool, 11 effects, 4+4
  voicebanks, VST/AU/external MIDI, V3/V4 compatibility, 13 parameters
  including Exciter/Air/Breathiness).
- Vocaloid control-parameter descriptions (VEL = consonant length,
  DYN = volume, PIT/PBS = pitch bend, GEN/CHA = formant, BRI, CLE,
  POR, BRE, AIR, EXC, MOU; Voice Color as an offset to editor curves).
- Landed teardown in FREE-STACK-PRODUCTION-NOTES.md and
  VOCAL-CHAIN-DIGITAL-FAIRY-YAMEII-DEKO-20DSP.md (Yameii ranges,
  48 kHz / 5.6.2+ bug, Channel Rack / mixer insert, NewTone->MIDI,
  double-formant rule, chipmunk trap).
- Gaps still named: exact V5 (not V6) numeric ranges for every
  parameter beyond the landed Yameii set; exact names of the 11 V5
  audio effects; exact FL Studio VST3 vs VST2 behaviour for V5 in
  the user's FL version; live Vocaloid session re-measurement.
