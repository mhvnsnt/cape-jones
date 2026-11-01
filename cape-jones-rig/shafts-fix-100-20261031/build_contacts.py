"""Contacts for shafts-fix-100: final contact (v4b shafts, v4b+figure,
Glare composite, per-shot sample) + per-shot contact grid (30 shots,
5 per row x 6 rows, downscaled)."""
import os, json
from PIL import Image, ImageDraw
BASE = os.path.dirname(os.path.abspath(__file__))
SHAFTS = os.path.join(BASE, 'shafts-eevee-v4-fullres-20261031.png')
FIG = '/home/hatch/workspace/cape-jones-rig/shafts-environmental-depth-lighting-upgrade-20261031/figure-only-plate-20261031.png'
import numpy as np

def mask_behind(shafts_img, fig_img):
    s = np.asarray(shafts_img.convert('RGB')).astype(float)
    f = np.asarray(fig_img.convert('RGBA')).astype(float)
    a = f[:, :, 3:4] / 255.0
    return Image.fromarray((s * (1 - a) + f[:, :, :3] * a).astype(np.uint8))

def tile(images, labels, cols, tw, th, bg=(40, 40, 40)):
    rows = (len(images) + cols - 1) // cols
    out = Image.new('RGB', (cols * tw, rows * (th + 28)), bg)
    d = ImageDraw.Draw(out)
    for i, (im, lab) in enumerate(zip(images, labels)):
        r, c = divmod(i, cols)
        x, y = c * tw, r * (th + 28)
        out.paste(im.resize((tw, th)), (x, y))
        d.text((x + 6, y + th + 6), lab, fill=(255, 255, 0))
    return out

def main():
    shafts = Image.open(SHAFTS).convert('RGB')
    fig = Image.open(FIG).convert('RGBA')
    comp = mask_behind(shafts, fig)
    comp.save(os.path.join(BASE, 'composite-shafts-v4-figure-20261031.png'))
    glare_path = os.path.join(BASE, 'methods', 'I4-glare-v4.png')
    glare = Image.open(glare_path).convert('RGB') if os.path.exists(glare_path) else shafts
    # per-shot samples: first 4
    rows = json.load(open(os.path.join(BASE, 'per-shot-table-20261031.json'))) if os.path.exists(os.path.join(BASE, 'per-shot-table-20261031.json')) else []
    samples = []
    labels = []
    for r in rows[:4]:
        samples.append(Image.open(os.path.join(BASE, 'per-shot', r['file'])).convert('RGB'))
        labels.append(r['shot_id'] + ' shafts')
    imgs = [shafts, comp, glare] + samples
    labs = ['V4 Eevee shafts only', 'V4 Eevee + figure', 'V4 Glare'] + labels
    tile(imgs, labs, 3, 360, 490).save(os.path.join(BASE, 'final-contact-20261031.png'))
    # per-shot grid
    if rows:
        allimgs = [Image.open(os.path.join(BASE, 'per-shot', r['file'])).convert('RGB') for r in rows]
        alllabs = [r['shot_id'] for r in rows]
        tile(allimgs, alllabs, 5, 300, 408).save(os.path.join(BASE, 'per-shot-contact-20261031.png'))
    print('contacts done', len(rows))

if __name__ == '__main__':
    main()
