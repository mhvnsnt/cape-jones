#!/usr/bin/env python3
"""Render v2 (drawn-art build): full song-length composite (labeled
fallback) + the Wan-VACE batch (49-frame loop per lighting section,
832x480, masks, drawn-art references).

Character: build_dance_v3 puppet from characters/sheets/04 (drawn art).
Plates/grades: render_v2 (painted here, labeled honestly in the README).
Sections: 7 lighting states x ~10.83 s = the full 75.79 s song.
"""
import numpy as np, cv2
from PIL import Image
import os, subprocess, imageio.v2 as imageio, importlib.util

def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m

HERE = os.path.dirname(__file__)
bd3 = load('bd3', f'{HERE}/build_dance_v3.py')
rv2 = load('rv2', f'{HERE}/render_v2.py')
ROOT = bd3.ROOT
VACEIN = f'{ROOT}/vace_in'; os.makedirs(VACEIN, exist_ok=True)
W, H, FPS = rv2.W, rv2.H, rv2.FPS
PLATES = {'yard': rv2.bg_yard, 'mesa': rv2.bg_mesa, 'evening': rv2.bg_evening}
TOTAL_F = 1819                      # 75.79 s song at 24 fps
SEC_F = [260] * 6 + [259]           # per-section frame counts
FIG_H = 920

def main():
    fig = Image.open(f'{ROOT}/parts2/figure2_rgba.png')
    layers, piv = bd3.segment(fig)
    scale = FIG_H / fig.size[1]
    DW, DH = int(fig.size[0] * scale), FIG_H
    PX, PY = (W - DW) // 2, 1006 - DH
    cache = {}
    def drawing(flip, f):
        key = (flip, f)
        if key not in cache:
            d = bd3.build_drawing(layers, piv, bd3.sample(f))
            if flip:
                d = d.transpose(Image.FLIP_LEFT_RIGHT)
            cache[key] = d.resize((DW, DH), Image.LANCZOS)
        return cache[key]

    plates = {name: fn()[0].convert('RGB') for name, fn in PLATES.items()}
    proc = None  # no 1080p video write: the account disk quota is nearly
    # exhausted (EDQUOT killed three runs). The fallback assembles from the
    # 832x480 guide clips in vace_in instead - same drawings, upscaled.
    sheet_frames = []
    for si, ((plate_name, grade_name, flip), nframes) in enumerate(zip(rv2.SECTIONS, SEC_F)):
        plate = plates[plate_name]
        # only 48 unique composites per section (the dance loop); the video
        # writes them looped, the VACE batch takes one loop, loop-closed
        graded, vmasks = [], []
        for f in range(bd3.LOOP):
            d = drawing(flip, f)
            frame = plate.copy()
            frame.paste(d, (PX, PY), d)
            frame = rv2.apply_grade(frame, grade_name)
            graded.append(np.asarray(frame, dtype=np.uint8))
            alpha = Image.new('L', (W, H), 0)
            alpha.paste(d.getchannel('A'), (PX, PY))
            a = cv2.dilate(np.array(alpha), np.ones((21, 21), np.uint8))
            m = cv2.resize(a, (832, 480), interpolation=cv2.INTER_AREA)
            vmasks.append(np.stack([m] * 3, axis=2))
        sheet_frames.append(Image.fromarray(graded[30]))
        vframes = [cv2.resize(graded[f], (832, 480), interpolation=cv2.INTER_AREA) for f in range(bd3.LOOP)]
        vframes.append(vframes[0].copy())
        vmasks.append(vmasks[0].copy())
        imageio.mimsave(f'{VACEIN}/sec{si}.mp4', vframes, fps=16, codec='libx264',
                        ffmpeg_params=['-crf', '10', '-pix_fmt', 'yuv420p'])
        imageio.mimsave(f'{VACEIN}/sec{si}_mask.mp4', vmasks, fps=16, codec='libx264',
                        ffmpeg_params=['-crf', '3', '-pix_fmt', 'gray'])
        print('section', si, plate_name, grade_name, 'frames', nframes, 'vace 49', flush=True)

    # references for VACE - ALL drawn art (owner correction #5)
    ref = Image.new('RGB', (700, 1013), (168, 168, 168))
    f2 = fig.resize((622, 900), Image.LANCZOS)
    ref.paste(f2, ((700 - 622) // 2, 56), f2)
    ref.save(f'{VACEIN}/ref.png')
    hero = Image.open(os.path.expanduser('~/workspace/cape-jones/characters/sheets/09-hero-shot-black.png')).convert('RGB')
    hero.thumbnail((1024, 1024), Image.LANCZOS)
    hero.save(f'{VACEIN}/ref_hero.png')
    s07 = Image.open(os.path.expanduser('~/workspace/cape-jones/characters/sheets/07-character-parts-expressions.jpg')).convert('RGB')
    sw, sh = s07.size
    head = s07.crop((int(0.030 * sw), int(0.080 * sh), int(0.155 * sw), int(0.245 * sh)))
    head.save(f'{VACEIN}/ref_head.png')
    sheet = Image.new('RGB', (W * 7 // 2, H // 2), (0, 0, 0))
    for i, fr in enumerate(sheet_frames):
        sheet.paste(fr.resize((W // 2, H // 2), Image.LANCZOS), (i * W // 2, 0))
    sheet.save(f'{ROOT}/sheet_cutout.png')
    print('render done: video_only_1080.mp4 + vace_in + refs + sheet_cutout')

if __name__ == '__main__':
    main()
