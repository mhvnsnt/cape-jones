# Digital Fairy / Yameii / Deko vocal chain + 20-module DSP — teardown extraction
# Method references only. Paid tools are references, never binaries.
# Landed in the music-wave folder (owner choice 2026-10-28), alongside
# WAVE-MAP.md, DELIVERY-STANDARDS.md, and the Pedalboard / Basic Pitch /
# Whisper teardowns in PR #95. House loudness spine stays -14 LUFS / -1 dBTP.
# NOT landed in docs/FREE-STACK-PRODUCTION-NOTES.md (57-byte placeholder on main).
# Single source for this vocal/DSP material is this file, in this folder.

## COVERAGE CHECK — 100% of the pasted teardown, by section
- [x] Digital Fairy 4-step chain (formant, air, robotic clamp, glitch sheen) + recording rule
- [x] Vocaloid 5 + Avanna install order, sample-rate fix, VSTi routing, CHA/EXC/AIR/BRE/MOU, VEL, vibrato/robot, NewTone->MIDI conversion
- [x] Combined Avanna vs human rule (no double-formant) + Deko stream chain + dual bus (3 inserts) + master glue
- [x] 20 modules: 15 core + 5 extra, 2 commercial benchmarks each, DSP spec each
- [x] Builder directive, 5 sections (anti-aliasing, pitch/formant separation, multiband/spectral, spatial/808, preset routing)
- [x] UNLOCK — OWNER AUTHORISED 2026-10-28: user states they are authorised
      to unlock the Avanna voicebank. Unlock path recorded here is the OFFICIAL
      one only: Vocaloid 5 Editor installed first, Avanna V3 second, then
      Vocaloid Authorizer with the owner's authorisation. No serial, key, or
      patcher file is recorded in this doc, in the repo, or in chat.
      No offline/ESV patcher step is included, because the official path is
      the authorised unlock path and the rest of the chain does not depend
      on any other step.

## A. DIGITAL FAIRY — HUMAN CHAIN (FL Studio, in order)
Principle: change vocal-tract anatomy BEFORE musical pitch. Pitching a baritone
up 12 semitones with no formant move stretches the tract and gives the
chipmunk result. Formant first, pitch second, and only +3 to +7 semitones
of pitch after the formant lock, if pitch is moved at all.
1. FORMANT SHIFT — Pitch 0.0, Formant/Throat +3.5 to +5.5 semitones.
   Reference plugins: Little AlterBoy, Auto-Tune Pro throat control.
   Effect: smaller tract, ethereal/anime throat size, glossy not hollow.
2. AIR LAYER — High-shelf boost ~6-10 kHz, Fresh Air high air up.
   Slapback delay 50-70 ms, zero feedback, very low mix.
   Effect: close, breathy, whisper-next-to-mic texture, not room shout.
3. ROBOTIC CLAMP — Auto-Tune retune speed 0, humanize 0, locked to song key.
   Free reference: MAutoPitch. Effect: laser note hits, no pitch wobble.
4. GLITCH SHEEN — OTT depth 15-20%, light bitcrush (full bus light, or
   ad-libs only). Effect: breath/micro-detail forward, slight console crunch.
RECORDING RULE: soft high head-voice / near-whisper / falsetto-adjacent hum.
Do NOT belt or rap in chest voice through this chain; it turns harsh.

## B. VOCALOID 5 + AVANNA (V3 voicebank) — OFFICIAL PATH ONLY
Install order: Vocaloid 5 Editor first, then Avanna V3 voicebank.
Update to 5.6.2+ immediately after editor install. Sample-rate bug in early
5.0.x at 48 kHz in FL Studio is fixed in 5.6.2+; otherwise force 44.1 kHz
in FL Studio audio settings. Avanna registers into the shared Vocaloid
voicebank directory; authorise with an official serial in Vocaloid Authorizer.
VSTi ROUTING: FL Studio > Manage Plugins > find installed plugins
(VSTPlugins / Common Files VST2 paths) > add VOCALOID5 VSTi to Channel Rack
> route to a mixer insert (example: Insert 10). Notes/lyrics are drawn in
the Vocaloid Editor window, locked to host BPM/playhead — NOT in FL Piano Roll.
VOICE COLOR (Style > Avanna):
- CHA Character/formant: +25 to +45 (scale -100 to +100).
  V5 direction is REVERSED vs V3/V4 GEN: in V5 positive shrinks the tract
  (feminine/cute); negative in V5 would masculinise. Do not invert this.
- EXC Exciter (brightness/clearness): +35 to +50.
- AIR / BRE breathiness: +15 to +25.
- MOU Mouth/opening: +20 to +40 (keeps fast rap vowels unmuffled).
RAP TIMING: VEL velocity lane, all notes to 95-115 (default 64).
In Vocaloid VEL is consonant speed, NOT volume. Avanna was recorded for slow
folk, so default consonants drag at 140-160 BPM trap; raised VEL puts
syllables on the 16th-note grid.
Pitch Transition / Vibrato: down to 0-10%, or Robot Voice for stair-step
cyber jumps.
HUMAN-TO-AVANNA CONVERSION (no syllable typing):
Record own flow > FL NewTone pitch corrector > Send to Piano Roll >
Export MIDI > drag .mid into Vocaloid 5 Editor > type lyrics per note.
Free-stack equivalent for the NewTone step: Basic Pitch (PR #95 wave,
audio -> MIDI, lead stem only, not full mixes).

## C. COMBINED RULE — DO NOT DOUBLE-FORMANT
If CHA is already +25 to +45 inside Vocaloid, OMIT external formant shifters
on the Avanna bus. Formant inside + formant outside = tract shrunk twice =
back to chipmunk. Pick one formant stage per bus.
KEEP on Avanna anyway: 0-speed Auto-Tune (erases folk pitch-slides in the
raw samples, gives stair-step snap), OTT 15-25%, Fresh Air, Soothe2
(stops synthetic highs stabbing), smart:EQ + Ozone-style master glue
(sidechained to beat, see §D).

## D. DEKO DUAL BUS (FL Studio, 3 inserts)
Insert 10 — AVANNA / YAMEII BUS (Vocaloid VSTi, CHA ~+35, VEL ~105):
1. Parametric EQ 2 — HPF 150 Hz
2. Auto-Tune EFX+ — Input Soprano, Retune Speed 0
3. OTT — Depth 20%
4. Fresh Air — High Air +5
5. Soothe2 — de-harsh
6. Reverb/delay send — VintageVerb / Delay 3, ~15% wet
Insert 11 — HUMAN DIGI BUS (mic input):
1. De-noise (RX Voice De-Noise reference)
2. Auto-Tune EFX+ — Soprano, Speed 0, Formant ON
3. Little AlterBoy — Pitch 0, Formant +2.0 to +3.5
4. Limiter in COMP mode / 1176-style — pins volume flat
5. OTT — Depth 15%
6. Vocoder parallel — VocalSynth 2 / Vocodex at 10% wet
   (EHX V256 hardware equivalent: Reflex-Tune + Gender Bender + 256-band vocoder)
Insert 12 — VOCAL MASTER GLUE (10 + 11 route here):
1. smart:comp — glues both voices, neither jumps out
2. smart:EQ — sidechained to Beat Bus, voices cut through 808s/synths
DEKO STREAM-CAUGHT DETAILS (same chain, Patcher view):
Parametric EQ 2 first (cut sub, wide high-mid boost, small harsh upper-mid dip);
Fruity Limiter COMP as brickwall; Love Philter x2 (one in-chain vowel filter /
drop sweeps, one parallel); Auto-Tune EFX+ Soprano, Speed 0, Humanize 0,
Formant ON, Auto-EFX rack ~60% mix (tube/distortion/pitch/vocoder textures).

## E. 20-MODULE COMMERCIAL DSP — BENCHMARKS + REQUIRED SPEC
1. EQ — Pro-Q 4 / EQuilibrium — ZDF SVF, pre-warped at Nyquist, Linear Phase
   (FIR) + Natural Phase modes. No cookbook biquads above 8 kHz.
2. Limiter — Pro-L 2 / Ozone 12 Maximizer IRC IV — True-peak 4x oversampled,
   1.5 ms lookahead, dual-stage release (fast transient + slow program).
3. Vowel Filter — Love Philter / WOW2 / FilterShaper XL — 3-band parallel
   formant bandpass matrix, F1/F2/F3 vowel tables (A/E/I/O/U), diode-ladder
   resonance saturation in feedback.
4. Zero-Speed Tuner — Auto-Tune Pro 11/EFX+ / Waves Tune RT — YIN/pYIN,
   sub-5 ms window, TD-PSOLA resampler, 0 ms quantization, Soprano tracking.
5. Formant Shifter — Little AlterBoy / MTransformer / Throat — true spectral
   envelope warping (cepstral liftering / LPC), decoupled from F0, tube
   soft-clipper on output to mask vocoder smear.
6. OTT Compressor — OTT / MO-TT — LR4 phase-compensated crossovers
   88.3 Hz / 2.5 kHz, upward (below -40 dB) + downward 100:1 per band.
7. Air Exciter — Fresh Air / Aural Exciter — parallel high-shelf crossover
   5 kHz / 12 kHz, even/odd Chebyshev harmonics, sibilance ducker so S bypasses drive.
8. Soothe De-Harsher — Soothe2 / Smooth Operator — 2048-point STFT, moving-median
   spectral floor, notch narrow peaks only, 2-9 kHz, leave broadband flat tone alone.
9. Reverb/Delay — VintageVerb+EchoBoy / Pro-R 2+Timeless 3 — 8x8 Hadamard FDN,
   modulated all-pass diffusers, 12/16-bit vintage DAC downsampling, BBD tape-flutter delay.
10. Vocoder — VocalSynth 2 / Vocodex / EHX V256 — 32-256 band Bark filterbank,
    unvoiced detector routes s/t/k bursts around carrier (lyrics stay intelligible).
11. De-Noiser — RX 11 Voice De-Noise / Clarity Vx Pro — spectral subtraction +
    DeepFilterNet/RNNoise gate, adaptive floor, musical-noise smoothing (no chopping whispers).
12. 1176 Compressor — UAD 1176 / CLA-76 / FET — FET loop, attack 20-800 us,
    transformer harmonics, All-Buttons-In bias curve.
13. Glue Compressor — Cytomic Glue / SSL Bus Comp 2 — SSL 4000 G VCA RMS detector,
    sidechain HPF 90 Hz (808s do not pump vocals), stepped auto-release.
14. Sidechain Ducking EQ — TrackSpacer 2.5 / smart:EQ 4 — 32-band spectral masking
    analyzer, inverted 1:1 dynamic EQ on beat bus, Mid/center only.
15. Mastering Chain — Ozone 12 Advanced / DS1-MK3 + Shadow Hills — 4-stage:
    Mid/Side linear-phase EQ > multiband dynamic exciter > soft-knee clipper
    (tanh/polynomial) > true-peak IRC limiter, -7 to -9 LUFS target metering.
    House lock note: show master spine is -14 LUFS / -1 dBTP (PR #95 delivery
    standards). The -7 to -9 figure above is the commercial mastering-module
    benchmark in the teardown, NOT a change to the house master target.
16. Pitch Editor — Melodyne 5 Studio / Revoice Pro 5 / NewTone — offline
    note-blob segmentation, sibilant vs vowel split, independent pitch center /
    drift / formant / timing edits, sibilants untouched.
17. Wavetable Synth — Serum 2 / Vital Pro / Phase Plant — 2048-sample
    band-limited mip-mapped wavetable osc, 16x unison detune, FM/sync warp,
    hyper-dimension chorus.
18. 808 Saturation — Saturn 2 / Decapitator / StandardCLIP — split-band
    crossover 140 Hz: sub mono/phase-locked, upper harmonics saturated/clipped
    4x oversampled (140 Hz-2.5 kHz).
19. Sidechain Pump — ShaperBox VolumeShaper / Kickstart 2 / LFO Tool —
    sample-accurate Bezier LFO locked to host PPQ/BPM, lookahead smoothing
    (no low-end clicks), multiband option (pump lows <200 Hz only).
20. Stereo Widener — MicroShift / Ozone Imager 2 / Wider — dual-delay
    pitch-detuned Haas + all-pass comb (H3000 / Dimension D model), wide in
    headphones, zero phase cancellation in mono.

## F. BUILDER DIRECTIVE (mandatory for custom builds, not textbook DSP)
1. Anti-aliasing/filter topology: ZDF trapezoidal SVF for EQ/vowel filter;
   4x polyphase FIR/IIR oversampling around every waveshaper/clipper
   (1176, 808 sat, air exciter, limiter, formant shifter).
2. Pitch/formant separation: decouple F0 from spectral envelope via cepstral
   liftering or WORLD-style decomposition BEFORE TD-PSOLA. Formant +3.0 to
   +5.0 semitones must NOT move F0 or add frame-boundary comb filtering.
   Sibilant bypass everywhere pitch/formant/harmonics are touched: ZCR +
   spectral-flatness detector routes s/t/k/f/sh around those engines.
3. Phase-coherent multiband/spectral: OTT LR4 crossovers as §E.6, dual
   upward+downward RMS/peak per band. Soothe/ducking EQ: 2048-sample Hann
   STFT, 75% overlap (4x overlap-add); Soothe median-floor notch 2-9 kHz;
   ducking EQ inverted envelope on Mid/center of beat bus only (stereo width intact).
4. Spatial/808 integrity: Widener = orthogonal all-pass decorrelation +
   micro-pitch dual delay (+/-6 cents, 8 ms / 13 ms L/R), HPF 180 Hz so sub
   stays 100% mono, L+R sums with zero comb cancellation. 808/pump split
   140 Hz, sub phase-locked, 2 ms lookahead ramp on pump envelope (no DC clicks).
5. Preset routing:
   YAMEII BUS: ZDF HPF 150 Hz > Zero-Speed Tuner (0 ms, Soprano) > OTT 20% >
     Air Exciter (+5 dB High Air) > Soothe > Widener 25% > FDN Reverb/Delay send.
   DIGI HUMAN BUS: De-Noiser > Zero-Speed Tuner > Formant Shifter (+3.5 st,
     Pitch 0.0) > 1176 (fast attack/release) > OTT 15% > Vocoder 10% parallel >
     Air Exciter > Soothe > Sidechain Ducking EQ (Beat Bus linked).

## G. FREE-STACK MAPPING (what exists vs what must be custom-built)
HAVE in house / PR #95 wave:
- Pedalboard (GPL-3.0, JUCE): Compressor, Limiter, Gain, HPF/LPF, Peak/Shelf EQ,
  Chorus/Phaser/Delay/Reverb, Distortion/Clipping, NoiseGate, PitchShift,
  Resample, Convolution IR, VST3 hosting bridge. Chains are plain Python,
  versioned, repeatable — the seat for designed voice chains.
- Basic Pitch (Apache-2.0): audio -> MIDI, lead stems, replaces NewTone step.
- Whisper (MIT): casting QA / script-diff / subtitle timing only, never auto-subtitler.
- Chatterbox (MIT) / Kokoro (Apache-2.0): character-voice renders, weights staged.
- FFmpeg loudnorm: -14 LUFS / -1 dBTP house spine (locked, do not move to -7/-9).
CUSTOM-BUILD ONLY (no off-the-shelf free equivalent in the wave):
ZDF SVF EQ, true cepstral/LPC formant warping, LR4 OTT, 2048-STFT Soothe,
Bark vocoder with unvoiced bypass, split-band 808 saturator, Haas/all-pass
widener, YIN/pYIN + TD-PSOLA tuner. These are the builder-directive targets
in §F, not Pedalboard built-ins. Audacity/Ardour/open DSP can host prototypes;
the commercial plugins in §E remain method references only.

## H. WHAT THIS LANDING DOES NOT DO
- No new canon, no new character, no invented voicebank, no invented song.
- No paid plugin binary, serial, or voicebank file is included or linked.
- No double-formant on Avanna. No 12-semitone pitch-up without formant lock.
- No change to the -14 LUFS house master. No change to any merged PR.
- This file is the extraction. Wiring into voice-kit / music-wave job profiles
  is the next landing step, after owner confirms the target file (see §I).

## I. STILL OWED AFTER THIS LANDING (not in this file)
1. Target CONFIRMED 2026-10-28 by owner: PR #95 music-wave folder (this file).
   Do NOT also land in docs/FREE-STACK-PRODUCTION-NOTES.md.
2. Confirm Avanna arrival form: official Vocaloid 5 + Avanna V3 installers
   only, or a different licensed source? The chain above assumes official.
3. Confirm PR #95 merge order: music-wave (Pedalboard/Basic Pitch/Whisper)
   lands first, then this vocal/DSP extraction references it, or both together?
