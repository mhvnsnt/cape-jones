#!/usr/bin/env python3
"""Assemble the ROUND-3 (tweaked-r3) deliverables from the Kaggle v4 VACE
section clips, mux the recovered song-full-v2-jp.mp3, build the sheet, and
run the PR #269 spec measurements + zoom checks.

Recreated from assemble_v2.py (the v3 tweaked assemble script lived in /tmp
and was lost). Differences vs assemble_v2.py:
- sources: kaggle_out_tweaked_r3/out/sec{N}_{name}/sec{N}_{name}.mp4
- outputs: cj-dance-proof-2d-v2-tweaked-r3.mp4 / -sheet.png (never the
  Oct 31 cj-dance-proof-2d-v2.mp4, never the fallback name)
- extra zoom crops: twist f24 shoulders + legs, cape hem twist
Song rule: song-full-v2-jp.mp3 is present (md5 verified); if it were absent
the output would be -premix, not final.
"""
import numpy as np, cv2
from PIL import Image
import os, sys, subprocess

ROOT = os.path.expanduser('~/workspace/_cj-dance-v2/build')
SRC = os.path.expanduser('~/workspace/_cj-dance-v2/kaggle_out_tweaked_r3/out')
OUTDIR = os.path.expanduser('~/workspace/your_files/cape-jones-dance-proof')
SONGDIR = f'{OUTDIR}/song'
W, H, FPS = 1920, 1080, 24
SEC_F = [260] * 6 + [259]
NAMES = ['sec0_day', 'sec1_magenta', 'sec2_cyan', 'sec3_green',
         'sec4_dusk', 'sec5_night', 'sec6_dayflip']
TAG = '-tweaked-r3'

def read_frames(path):
    cap = cv2.VideoCapture(path)
    frames = []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        frames.append(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))
    cap.release()
    return frames

def main():
    sections = []
    for name in NAMES:
        p = f'{SRC}/{name}/{name}.mp4'
        fr = read_frames(p)
        assert len(fr) >= 49, f'{p}: only {len(fr)} frames'
        print(f'{name}: {len(fr)} frames, {fr[0].shape}')
        sections.append(fr[:49])

    song_v2 = f'{SONGDIR}/song-full-v2-jp.mp3'
    song_v1 = f'{SONGDIR}/song-full.mp3'
    if os.path.exists(song_v2):
        song, final = song_v2, True
    elif os.path.exists(song_v1):
        song, final = song_v1, False
    else:
        song, final = None, False
    suffix = TAG + ('' if final else '-premix')
    video_only = f'{ROOT}/final_video_only{suffix}.mp4'
    proc = subprocess.Popen(['ffmpeg', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                             '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                             '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium',
                             '-pix_fmt', 'yuv420p', video_only], stdin=subprocess.PIPE)
    sheet_frames = []
    for si, sec in enumerate(sections):
        n = SEC_F[si]
        for j in range(n):
            f = sec[j % len(sec)]
            f = cv2.resize(f, (W, H), interpolation=cv2.INTER_CUBIC)
            proc.stdin.write(np.asarray(f, dtype=np.uint8).tobytes())
            if j == 30:
                sheet_frames.append(Image.fromarray(f))
    proc.stdin.close(); proc.wait()

    sheet = Image.new('RGB', (W * 7 // 2, H // 2), (0, 0, 0))
    for i, fr in enumerate(sheet_frames):
        sheet.paste(fr.resize((W // 2, H // 2), Image.LANCZOS), (i * W // 2, 0))
    sheet_path = f'{OUTDIR}/cj-dance-proof-2d-v2-tweaked-r3-sheet.png'
    sheet.save(sheet_path)
    print('SHEET', sheet_path)

    final_mp4 = f'{OUTDIR}/cj-dance-proof-2d-v2{suffix}.mp4'
    if song:
        subprocess.run(['ffmpeg', '-y', '-i', video_only, '-i', song,
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac',
                        '-b:a', '192k', '-shortest', final_mp4], check=True,
                       capture_output=True)
    else:
        os.replace(video_only, final_mp4)
    print('FINAL', final_mp4, 'song:', song, 'song_is_v2_mix:', final)

    # --- PR #269 section 5 measurement: one loop, day section -------------
    loop = [cv2.resize(f, (W, H), interpolation=cv2.INTER_CUBIC) for f in sections[0][:48]]
    small = [cv2.resize(cv2.cvtColor(f, cv2.COLOR_RGB2GRAY), (480, 270)).astype(np.float32) for f in loop]
    med = np.median(np.stack(small), axis=0)
    masks = [np.abs(s - med) > 20 for s in small]
    allt = np.stack(masks)
    ys, xs = np.where(allt.any(axis=0))
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    bw, bh = x1 - x0, y1 - y0
    def travel(ylo, yhi):
        cents = []
        for m in masks:
            band = m[y0 + int(ylo * bh): y0 + int(yhi * bh), x0:x1]
            yy, xx = np.where(band)
            cents.append(xx.mean() if len(xx) else np.nan)
        cents = np.array(cents, dtype=float)
        return (np.nanmax(cents) - np.nanmin(cents)) / bw * 100
    foot = travel(0.82, 1.0)
    torso = travel(0.28, 0.55)
    print(f'MEASURE foot travel {foot:.1f}%  torso travel {torso:.1f}%  ratio {foot / max(torso, 0.01):.2f} (spec: ratio >= 0.5, torso >= 10%)')

    # --- zoom checks: shoulders/cape hem/between-legs on step + twist frames
    def zoom(frame, box, out, size=(880, 880)):
        Image.fromarray(frame).crop(box).resize(size, Image.LANCZOS).save(f'{ROOT}/{out}')
    day = sections[0]
    f_step = cv2.resize(day[5], (W, H), interpolation=cv2.INTER_CUBIC)
    f_twist = cv2.resize(day[26], (W, H), interpolation=cv2.INTER_CUBIC)
    f_twist24 = cv2.resize(day[24], (W, H), interpolation=cv2.INTER_CUBIC)
    zoom(f_step, (620, 60, 1300, 700), 'final_zoom_shoulder_step_r3.png')
    zoom(f_twist, (620, 60, 1300, 700), 'final_zoom_shoulder_twist_r3.png')
    zoom(f_twist24, (620, 60, 1300, 700), 'final_zoom_shoulder_twist24_r3.png')
    zoom(f_step, (700, 620, 1250, 1080), 'final_zoom_legs_step_r3.png', (880, 736))
    zoom(f_twist, (700, 620, 1250, 1080), 'final_zoom_legs_twist_r3.png', (880, 736))
    zoom(f_twist24, (700, 620, 1250, 1080), 'final_zoom_legs_twist24_r3.png', (880, 736))
    # cape hem band on twist frames
    zoom(f_twist, (620, 620, 1300, 1080), 'final_zoom_hem_twist_r3.png', (880, 598))
    zoom(f_twist24, (620, 620, 1300, 1080), 'final_zoom_hem_twist24_r3.png', (880, 598))
    print('zooms saved to build/ (r3)')

if __name__ == '__main__':
    main()
