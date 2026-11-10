"""Fist v5 CORRECTION (Mars, 2026-10-31 17:29 CDT): the 180-rotated seated
v5 fists are UPSIDE DOWN for a forward punch -- that orientation is saved
as the UPPERCUT set. For the forward punch, seat the cut-out fists in their
ORIGINAL orientation (knuckles top, as in Mars's uploaded source), NO 180
rotation. Thumb-left rule, unrotated: the RIGHT source fist has its thumb
detail on the left side, so Arm2 = right fist; Arm1 = left fist (thumb right).
No shapes redrawn, no vector polygons -- pulled + cut out + fitted only."""
from PIL import Image

base_dir = '/home/hatch/workspace/cape-jones-rig/'
src_dir = base_dir + 'forearm-fist-v5-20261031/'
out_dir = base_dir + 'forearm-fist-v5-correction-20261031/'


def seat(forearm_path, fist_path, forearm_offset, fist_centre_x, fist_top_y,
         out_name, fist_w=170, cut_y=88):
    fore = Image.open(base_dir + forearm_path).convert('RGBA')
    px = fore.load()
    for y in range(cut_y, fore.size[1]):
        for x in range(fore.size[0]):
            px[x, y] = (0, 0, 0, 0)
    fist = Image.open(src_dir + fist_path).convert('RGBA')
    # NO rotation -- original orientation, knuckles top, as uploaded.
    fh = int(fist.size[1] * fist_w / fist.size[0])
    fist = fist.resize((fist_w, fh), Image.LANCZOS)
    canvas = Image.new('RGBA', (320, 300), (0, 0, 0, 0))
    canvas.alpha_composite(fore, forearm_offset)
    canvas.alpha_composite(fist, (fist_centre_x - fist_w // 2, fist_top_y))
    canvas.save(out_dir + out_name)
    print(out_name, 'fist', fist.size, 'top', fist_top_y,
          'bottom', fist_top_y + fh)


# Arm2: RIGHT source fist -> thumb on the left side, unrotated.
seat('forearm-fist-v3-20261031/forearm-v3-arm2-standard-clean-20261031.png',
     'fist-right-v5-20261031.png', (35, 0), 205, 65,
     'forearm-v5-arm2-forward-punch-flipped-20261031.png')
# Arm1: LEFT source fist -> thumb on the right side, unrotated.
seat('forearm-fist-v3-20261031/forearm-v3-arm1-clean-20261031.png',
     'fist-left-v5-20261031.png', (40, 0), 165, 65,
     'forearm-v5-arm1-forward-punch-flipped-20261031.png')
