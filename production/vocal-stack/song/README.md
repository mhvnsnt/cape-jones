# Cape Jones Dance — the song (production/vocal-stack/song/)

Anime-intro song for the Cape Jones dance scene, built 2026-10-29 on owner
order, extending the Tamagotchi loop to full length (48 bars, 152 BPM,
C major, 75.8 s): intro → verse A → chorus → verse B → bridge → chorus B →
outro. Japanese lyrics about Cape Jones himself: the deadpan caped hero
dancing in the yard while day/night and LED colors change around him and
the digital pet beeps in his pocket — the world changes, the dance does
not (SHOW-BIBLE-SEED owner text).

## Files
- `lyrics.md` — the lyrics as their own track: Japanese + romaji + English.
- `session.json` — the mixer session/playlist: sections, every stem, the
  lyrics track with timed lines, the vocal and master chains.
- `playlist.m3u` — full mix / vocal stem / instrumental, in order.
- `song-full.mp3`, `song-instrumental.mp3`, `song-vocal-stem.mp3` — mixes.
- `song_data.py` (lyrics + melody data), `compose_song.py` (MIDI/stems,
  compose_v3 conventions), `build_vocal.py` (the sung vocal),
  `mix_song.py` (vocal chain + mix + master). Rebuild order: data →
  compose → FluidSynth stem render → build_vocal → mix_song.

## What sang the vocal (honest)
No Avanna voicebank or VOCALOID5 editor exists in either repo (verified by
full-tree search: no .vsqx/.vpr/.ust files, no installer — the owner's
2.64 GB VOCALOID5 installer lives on his Windows/Mac seat, and the editor
does not run on this Linux box). Avanna is also an English voicebank.

So the Japanese vocal was produced with the repo's own open stack, its
latest generation: a Japanese guide voice (espeak-ng ja+f5, ~345 Hz) sung
mora-by-mora, each mora time-fit and pitch-placed onto the written melody
with Rubber Band per the repo's `rubberband_autotune_v1.py` / v19 method
(hard autotune by construction; formant lift ×1.7 decoupled from pitch —
pass 1 formants move, pass 2 formants preserved), then the Digital Fairy
Avanna bus + the v19 layer recipe (harmony ×0.5, octave HP250+chorus
×0.35, bit-crush parallel, slapback). Pitch verified by measurement:
sustained notes within ~±10 cents of the written melody. When a
Windows/Mac seat runs the real VOCALOID5 + Avanna, the same session
(vocal-melody MIDI + lyrics track) re-voices without re-composing.
