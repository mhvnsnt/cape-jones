"""Batch B contact sheets + measurements (PIL only, no Blender).
Run after all Blender stages finish. Reads renders in this folder and
writes contacts + measurements-20261101.json + FK gif/mp4.
Render-pixel mappings (measured from camera setups):
- side 100% (1400x1600, centre y 6.65, ortho 14): x_r = 700+(cx-700)*1.1428,
  y_r = (13.65-(1450-py)/100)*114.2857.
- back 50% (700x800, centre y 6.88, ortho 14): x_r = 350+(cx-700)*0.5714,
  y_r = (13.88-(1540-py)/100)*57.1429.
"""
import os, json, subprocess
from PIL import Image, ImageDraw

OUT = os.path.expanduser('~/workspace/cape-jones-rig/batch-b-side-rig-next-20261101')
CJ = os.path.expanduser('~/workspace/cape-jones-rig')
GREY = (170, 170, 170)

def side_xy(cx, py):
    return (700 + (cx - 700) * 1.1428, (13.65 - (1450 - py) / 100.0) * 114.2857)

def back_xy(cx, py):
    return (350 + (cx - 700) * 0.5714, (13.88 - (1540 - py) / 100.0) * 57.1429)

def crop_side(path, cx0, py0, cx1, py1):
    im = Image.open(path).convert('RGB')
    x0, y0 = side_xy(cx0, py0); x1, y1 = side_xy(cx1, py1)
    return im.crop((int(x0), int(y0), int(x1), int(y1)))

def side50_xy(cx, py):
    # side 50% (700x800, same camera as 100%): half the 100% factors
    return (350 + (cx - 700) * 0.5714, (13.65 - (1450 - py) / 100.0) * 57.1429)

def crop_side50(path, cx0, py0, cx1, py1):
    im = Image.open(path).convert('RGB')
    x0, y0 = side50_xy(cx0, py0); x1, y1 = side50_xy(cx1, py1)
    return im.crop((int(x0), int(y0), int(x1), int(y1)))

def crop_back(path, cx0, py0, cx1, py1):
    im = Image.open(path).convert('RGB')
    x0, y0 = back_xy(cx0, py0); x1, y1 = back_xy(cx1, py1)
    return im.crop((int(x0), int(y0), int(x1), int(y1)))

def label_sheet(cells, cols, cell_w, cell_h, labels, out, bg=(40, 40, 40)):
    """cells: list of PIL images (already sized cell_w x cell_h or smaller,
    centred); labels: one per cell, drawn above."""
    rows = (len(cells) + cols - 1) // cols
    W = cols * cell_w + (cols + 1) * 10
    H = rows * (cell_h + 26) + 10
    sheet = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(sheet)
    for i, (im, lab) in enumerate(zip(cells, labels)):
        r, c = divmod(i, cols)
        x = 10 + c * (cell_w + 10); y = 10 + r * (cell_h + 26)
        d.text((x + 2, y), lab, fill=(255, 255, 0))
        sheet.paste(im, (x, y + 26))
    sheet.save(out)
    print('SHEET', out, sheet.size)

def fit(im, w, h):
    im2 = im.copy(); im2.thumbnail((w, h), Image.LANCZOS)
    canvas = Image.new('RGB', (w, h), GREY)
    canvas.paste(im2, ((w - im2.width) // 2, (h - im2.height) // 2))
    return canvas

# --- neck-gap before/after: head/neck crops from wrist-fix bent render
# (before) and batch-b bent render (after). Same crop box both.
before = crop_side(os.path.join(CJ, 'side-rig-wrist-fix-20261101', 'side-bent-wrist-fix-grey-20261101.png'),
                   540, 60, 790, 500)
after = crop_side(os.path.join(OUT, 'side-open-hand-bent-20261101.png'),
                  540, 60, 790, 500)
bw, bh = before.size
before2 = before.resize((bw * 2, bh * 2), Image.LANCZOS)
after2 = after.resize((bw * 2, bh * 2), Image.LANCZOS)
label_sheet([before2, after2], 2, before2.width, before2.height,
            ['BEFORE wrist-fix: neck centre (663,367)',
             'AFTER batch-b: neck centre (663,357) up 10, neck z behind head'],
            os.path.join(OUT, 'neck-gap-before-after-20261101.png'))

# --- FK gif/mp4 from frames-fk (side, 100% frames)
frames = sorted(os.path.join(OUT, 'frames-fk', f)
                for f in os.listdir(os.path.join(OUT, 'frames-fk')) if f.endswith('.png'))
if frames:
    ims = [Image.open(f).convert('RGB') for f in frames]
    small = [im.resize((700, 800), Image.LANCZOS) for im in ims]
    small[0].save(os.path.join(OUT, 'side-fk-chain-20261101.gif'), save_all=True,
                  append_images=small[1:], duration=170, loop=0)
    with open(os.path.join(OUT, 'frames-fk', 'concat.txt'), 'w') as fh:
        for f in frames:
            fh.write("file '%s'\n" % f)
    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-r', '6',
                    '-i', os.path.join(OUT, 'frames-fk', 'concat.txt'),
                    '-vf', 'scale=700:800', '-pix_fmt', 'yuv420p',
                    os.path.join(OUT, 'side-fk-chain-20261101.mp4')],
                   check=True, capture_output=True)
    print('FK gif/mp4 from', len(frames), 'frames')

# --- sitting trials contact (3 x 700x800 renders)
cells, labels = [], []
for tag, lab in [('A-splay', 'S-A splay crouch (TRIAL, not chosen)'),
                 ('B-foreshorten', 'S-B rotX foreshorten sit (TRIAL)'),
                 ('C-drop', 'S-C rotX sit + hip drop, feet at ground (TRIAL)')]:
    p = os.path.join(OUT, 'back-sitting-trial-v2-%s-20261101.png' % tag)
    cells.append(fit(Image.open(p).convert('RGB'), 440, 500))
    labels.append(lab)
label_sheet(cells, 3, 440, 500, labels,
            os.path.join(OUT, 'back-sitting-trials-20261101.png'))

# --- knee trials contact 3x3 (options A/B/C x angles 0/30/60)
cells, labels = [], []
for opt in ['A', 'B', 'C']:
    for ang in [0, 30, 60]:
        p = os.path.join(OUT, 'knee-trial-%s-%02d-20261101.png' % (opt, ang))
        cells.append(fit(Image.open(p).convert('RGB'), 440, 500))
        labels.append('opt %s %d deg' % (opt, ang))
label_sheet(cells, 3, 440, 500, labels,
            os.path.join(OUT, 'back-knee-pivot-trials-20261101.png'))

# --- belt trials contact: waist crops from 50% back renders + split pieces
cells, labels = [], []
for tag, lab in [('0-fused', 'B0 fused belt+pelvis (control)'),
                 ('1-split', 'B1 split belt layer + pelvis layer'),
                 ('2-row7', 'B2 Row7_10 overlay at waist (buckle shows)')]:
    p = os.path.join(OUT, 'belt-trial-%s-20261101.png' % tag)
    cr = crop_back(p, 520, 720, 880, 1050)
    cells.append(fit(cr.resize((cr.width * 2, cr.height * 2), Image.LANCZOS), 440, 330))
    labels.append(lab)
cells.append(fit(Image.open(os.path.join(OUT, 'belt-split-belt-20261101.png')).convert('RGB'), 440, 330))
labels.append('split belt piece alone (rows 0-47 + side rects to 56)')
cells.append(fit(Image.open(os.path.join(OUT, 'belt-split-pelvis-20261101.png')).convert('RGB'), 440, 330))
labels.append('split pelvis piece alone (below outline)')
label_sheet(cells, 3, 440, 330, labels,
            os.path.join(OUT, 'belt-trials-contact-20261101.png'))
# belt split pieces proof sheet (same crops, kept as separate proof file)
label_sheet(cells[3:], 2, 440, 330, labels[3:],
            os.path.join(OUT, 'belt-split-pieces-20261101.png'))

# --- palm trials contact: hand crops, ArmFront (+ P3 ArmBack)
cells, labels = [], []
specs = [('0-fused', 'ArmFront', 'P0 fused only (control)'),
         ('1-row5', 'ArmFront', 'P1 Row5_15 121x121 on ArmFront'),
         ('2-hand10', 'ArmFront', 'P2 Hand_10 161x110 on ArmFront'),
         ('3-both', 'ArmFront', 'P3 ArmFront = Row5_15'),
         ('3-both', 'ArmBack', 'P3 ArmBack = Hand_10')]
for tag, arm, lab in specs:
    p = os.path.join(OUT, 'palm-trial-%s-20261101.png' % tag)
    if arm == 'ArmFront':
        cr = crop_back(p, 700, 880, 880, 1150)
    else:
        cr = crop_back(p, 510, 880, 690, 1150)
    cr = cr.resize((cr.width * 3, cr.height * 3), Image.LANCZOS)
    cells.append(fit(cr, 440, 380))
    labels.append(lab)
label_sheet(cells, 3, 440, 380, labels,
            os.path.join(OUT, 'palm-trials-contact-20261101.png'))

# --- side belt trial waist crop (from 50% side render: 700x800, use 50% mapping)
cr = crop_side50(os.path.join(OUT, 'side-belt-row7-trial-20261101.png'), 540, 680, 880, 940)
cr.save(os.path.join(OUT, 'side-belt-row7-waist-crop-20261101.png'))
print('side belt waist crop', cr.size)
print('CONTACTS DONE')
