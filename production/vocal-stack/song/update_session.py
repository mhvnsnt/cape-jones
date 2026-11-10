#!/usr/bin/env python3
"""Update session.json + playlist.m3u in the deliverables song folder for v2."""
import json, os

S = "/home/hatch/workspace/your_files/cape-jones-dance-proof/song"
EN_LINES = [
 "In the morning yard he is dancing all alone",
 "Cape is fluttering, his face so dead serious",
 "Even if the whole world changes, he never, ever does",
 "Only his feet keep the beat, and the beat goes all day long",
 "Cape Jones, dance and dance, everybody come and dance, dance!",
 "And when the colors change, you know the sky changes too",
 "Cape Jones, spin and spin, everybody come and spin, spin!",
 "Tomorrow, same old place, and the same old dance again",
 "In his pocket there's a little pet and it beeps all day",
 "Battery's running low and he doesn't care at all",
 "Before dinner time and after dinner time, he dances",
 "The same old step, the dream step, the same old step every day",
 "Day turns into night and the night turns to morning",
 "L-E-D lights are shining blue and pink and green tonight",
 "The only thing that changes is the world",
 "Cape Jones, dance and dance, everybody come and dance, dance!",
 "And when the colors change, you know the sky changes too",
 "Cape Jones, spin and spin, everybody come and spin, spin!",
 "Tomorrow, same old place, and the same old dance again",
 "He is always standing right here",
 "Cape Jones, dance, everybody, Cape Jones, dance",
 "La la la la la la laa",
]
p = os.path.join(S, "session.json")
s = json.load(open(p))
s["tracks"] += [
 {"name": "full-mix-v2-jp", "type": "mix", "file": "song-full-v2-jp.mp3",
  "note": "v2 remix (same JP vocal take, new balance architecture) — supersedes song-full.mp3"},
 {"name": "full-mix-v2-en", "type": "mix", "file": "song-full-v2-en.mp3",
  "note": "English-sung version, same session/melody, syllable-adapted lyrics, same v2 mix"},
 {"name": "vocal-stem-v2-jp", "type": "stem", "file": "song-vocal-stem-v2-jp.wav",
  "role": "v2 vocal bus (premaster, section gains applied)"},
 {"name": "vocal-stem-v2-en", "type": "stem", "file": "song-vocal-stem-v2-en.wav",
  "role": "v2 English vocal bus (premaster, section gains applied)"},
 {"name": "instrumental-mix-v2", "type": "mix", "file": "song-instrumental-v2.mp3",
  "note": "v2 backing (carved + spectral-ducked stems, section architecture), no vocal"},
 {"name": "excerpt-vocal-entry", "type": "excerpt",
  "file": "excerpt-vocal-entry-v1.mp3 / excerpt-vocal-entry-v2-jp.mp3 / excerpt-vocal-entry-v2-en.mp3",
  "note": "3.0-10.5 s: end of intro into the first sung line — the moment the owner flagged"},
]
assert len(s["lyrics_track"]) == len(EN_LINES)
s["lyrics_track_en"] = [
 {"start_sec": e["start_sec"], "end_sec": e["end_sec"], "section": e["section"],
  "english_sung": line} for e, line in zip(s["lyrics_track"], EN_LINES)]
s["v2_remix"] = {
 "date": "2026-10-29",
 "owner_complaint": "as soon as the lyrics vocals drop then the beat is almost unhearable",
 "measured_v1_problem": {
   "vocal_bus_minus_instrumental_LUFS_while_singing": "+11.3 to +14.8 dB (hit-song median is ~0 dB)",
   "beat_body_40_250Hz_drop_intro_to_verseA_in_delivered_master_dB": 7.8,
   "mechanism": "the over-hot vocal bus ate the shared master compressor/limiter budget, "
                "so the beat was pumped down exactly when the vocal entered; the tinkle-bell "
                "sparkle also sits 99% inside the vocal's 2-5 kHz presence band"},
 "architecture": [
   "per-section vocal gains solved to LUFS targets (verses +1.0, choruses +0.5, bridge +1.5, outro +1.5)",
   "static carve -2 dB @ 3 kHz on square lead + arp; sparkle trimmed 0.8 -> 0.7",
   "TrackSpacer-style spectral ducking (custom STFT, Mid channel only): vocal key dips only "
   "clashing bins of arp/lead/sparkle, max ~4 dB, fast attack / ~150 ms release; drums+bass never ducked",
   "stereo: vocal lead centre-focused (Haas 0.30 -> 0.18), arp widened +2 dB side",
   "instrumental section gains: intro 0, verses -0.5, choruses 0, bridge -2, outro -1 dB",
   "master unchanged: pedalboard_master house chain + loudnorm to the locked -14 LUFS / -1 dBTP spine"],
 "measured_v2_jp": {"LUFS": -14.2, "TP": -1.3, "beat_body_drop_intro_to_verseA_dB": 0.5,
                    "offsets_LUFS": {"verseA": 1.0, "chorusA": 0.5, "verseB": 1.0, "bridge": 1.5, "chorusB": 0.5, "outro": 1.5}},
 "measured_v2_en": {"LUFS": -14.3, "TP": -1.4, "beat_body_drop_intro_to_verseA_dB": 0.2,
                    "offsets_LUFS": {"verseA": 0.9, "chorusA": 0.7, "verseB": 1.1, "bridge": 1.9, "chorusB": 0.8, "outro": 0.2}},
 "english_vocal_note": "Sung with the same repo v19 method as the JP take: espeak-ng en+f5 guide voice, "
                       "one syllable at a time, Rubber Band pitch placement on the same written melody, "
                       "formant lift x1.7, then the same Digital Fairy Avanna bus + v19 layers. "
                       "English lines were syllable-adapted to the JP note grid (counts asserted in "
                       "build_vocal_en.py). Avanna herself still cannot sing here (English Vocaloid "
                       "voicebank; editor lives on the owner's Windows/Mac seat).",
 "scripts": ["measure_v1.py", "mix_v2.py", "build_vocal_en.py", "verify_v2.py"],
 "notes_file": "MIX-NOTES.md",
}
json.dump(s, open(p, "w"), ensure_ascii=False, indent=2)

pl = """#EXTM3U
# Cape Jones dance song — playlist / mixer order (v2 first, v1 kept below)
#EXTINF:76,Cape Jones Dance v2 - full mix (Japanese)
song-full-v2-jp.mp3
#EXTINF:76,Cape Jones Dance v2 - full mix (English)
song-full-v2-en.mp3
#EXTINF:76,Cape Jones Dance v2 - vocal stem (Japanese)
song-vocal-stem-v2-jp.wav
#EXTINF:76,Cape Jones Dance v2 - vocal stem (English)
song-vocal-stem-v2-en.wav
#EXTINF:76,Cape Jones Dance v2 - instrumental
song-instrumental-v2.mp3
#EXTINF:8,Cape Jones Dance - vocal entry excerpt v1 (before)
excerpt-vocal-entry-v1.mp3
#EXTINF:8,Cape Jones Dance - vocal entry excerpt v2 JP (after)
excerpt-vocal-entry-v2-jp.mp3
#EXTINF:8,Cape Jones Dance - vocal entry excerpt v2 EN (after)
excerpt-vocal-entry-v2-en.mp3
#EXTINF:76,Cape Jones Dance v1 - full mix
song-full.mp3
#EXTINF:76,Cape Jones Dance v1 - vocal stem
song-vocal-stem.wav
#EXTINF:76,Cape Jones Dance v1 - instrumental
song-instrumental.mp3
"""
open(os.path.join(S, "playlist.m3u"), "w").write(pl)
print("session.json + playlist.m3u updated")
