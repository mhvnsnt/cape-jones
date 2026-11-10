from PIL import Image, ImageDraw
D = '/home/hatch/workspace/cape-jones-rig/forearm-fist-v5-correction-20261031/'
src = Image.open('/home/hatch/workspace/user/files/1000179204_34_scne.jpg').convert('RGBA')
left = Image.open(D + 'fist-left-v5-20261031.png')
right = Image.open(D + 'fist-right-v5-20261031.png')
up2 = Image.open(D + 'forearm-v5-arm2-uppercut-20261031.png')
up1 = Image.open(D + 'forearm-v5-arm1-uppercut-20261031.png')
fwd2 = Image.open(D + 'forearm-v5-arm2-forward-punch-flipped-20261031.png')
fwd1 = Image.open(D + 'forearm-v5-arm1-forward-punch-flipped-20261031.png')
W, H = 1600, 960
sheet = Image.new('RGB', (W, H), (128, 128, 128))
dr = ImageDraw.Draw(sheet)


def paste(img, x, y, maxw, maxh):
    im = img.copy()
    im.thumbnail((maxw, maxh), Image.LANCZOS)
    sheet.paste(im, (x, y), im)
    return im.size


dr.text((20, 10), 'SOURCE (Mars upload, beige bg)', fill=(0, 0, 0))
paste(src, 20, 40, 380, 260)
dr.text((440, 10), 'CUT-OUT LEFT (original, knuckles top)', fill=(0, 0, 0))
paste(left, 440, 40, 300, 270)
dr.text((780, 10), 'CUT-OUT RIGHT (original, knuckles top)', fill=(0, 0, 0))
paste(right, 780, 40, 300, 270)
dr.text((1120, 10), 'UPPERCUT Arm2 (old rotated set, saved)', fill=(0, 0, 0))
paste(up2, 1120, 40, 320, 300)
dr.text((20, 360), 'UPPERCUT Arm1 (old rotated set, saved)', fill=(0, 0, 0))
paste(up1, 20, 390, 320, 300)
dr.text((380, 360), 'FORWARD PUNCH Arm2 (FLIPPED: right fist, unrotated, thumb left)', fill=(0, 0, 0))
paste(fwd2, 380, 390, 320, 300)
dr.text((740, 360), 'FORWARD PUNCH Arm1 (FLIPPED: left fist, unrotated, thumb right)', fill=(0, 0, 0))
paste(fwd1, 740, 390, 320, 300)
dr.text((1080, 390), 'Correction 2026-10-31 17:29 CDT:', fill=(0, 0, 0))
dr.text((1080, 420), 'rotated 180 = upside down for forward punch,', fill=(0, 0, 0))
dr.text((1080, 450), 'saved as UPPERCUT. Forward punch = original', fill=(0, 0, 0))
dr.text((1080, 480), 'orientation, knuckles top, NOT rotated.', fill=(0, 0, 0))
dr.text((1080, 510), 'Pulled + cut out + fitted. NOT generated,', fill=(0, 0, 0))
dr.text((1080, 540), 'NOT hand-drawn vector.', fill=(0, 0, 0))
dr.text((20, 720), 'FORWARD vs UPPERCUT side-by-side (Arm2):', fill=(0, 0, 0))
paste(fwd2, 20, 750, 220, 200)
paste(up2, 260, 750, 220, 200)
dr.text((500, 760), 'LEFT: forward (knuckles top, original). RIGHT: uppercut (rotated 180, knuckles at strike edge).', fill=(0, 0, 0))
dr.text((500, 790), 'Original v5 seated files untouched; uppercut copies are byte-identical to them (md5 verified).', fill=(0, 0, 0))
sheet.save(D + 'proof-v5-correction-forward-vs-uppercut-20261031.png')
print(sheet.size)
