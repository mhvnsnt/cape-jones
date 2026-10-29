#!/usr/bin/env python3
"""House Basic Pitch entry point (Spotify Basic Pitch, Apache-2.0).

Usage: transcribe_midi.py <in.wav> <out_dir>
Writes <stem>.mid + <stem>_note_events.csv into out_dir and prints the
note count, pitch range and duration so the run is self-recording.
Best on a single source (lead stem, hum, solo line) — see
TEARDOWN-basic-pitch.md.
"""
import os
import sys

from basic_pitch import ICASSP_2022_MODEL_PATH
from basic_pitch.inference import predict_and_save


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    predict_and_save(
        [src], out_dir, save_midi=True, sonify_midi=False,
        save_model_outputs=False, save_notes=True,
        model_or_model_path=ICASSP_2022_MODEL_PATH,
    )
    import pretty_midi
    stem = os.path.splitext(os.path.basename(src))[0]
    mid = os.path.join(out_dir, stem + "_basic_pitch.mid")
    pm = pretty_midi.PrettyMIDI(mid)
    notes = [n for inst in pm.instruments for n in inst.notes]
    if notes:
        pitches = [n.pitch for n in notes]
        print(f"notes={len(notes)} pitch_min={min(pitches)} "
              f"pitch_max={max(pitches)} duration_s={pm.get_end_time():.2f}")
    else:
        print("notes=0")
    print(f"wrote {mid}")


if __name__ == "__main__":
    main()
