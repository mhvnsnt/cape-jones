"""Tool 2: FK pivot rotate, large-temp method. Never PIL rotate(expand=False) in place.
Rotate a piece about a named pivot (in native piece coords) by PIL angle degrees
(counter-clockwise positive, as PIL defines). Uses a 3x canvas so nothing clips,
then trims to alpha bbox and returns (image, new_pivot_in_trimmed_coords)."""
from PIL import Image
import sys
def rotate_about_pivot(im, pivot, angle_deg):
    w,h = im.size
    scale = 3
    canvas = Image.new('RGBA', (w*scale, h*scale), (0,0,0,0))
    canvas.paste(im, (w, h))
    cx, cy = w + pivot[0], h + pivot[1]
    # PIL rotate is about canvas centre; translate so pivot is centre, rotate, translate back
    # Simpler robust method: rotate whole large canvas about its centre after shifting
    # Use affine via rotate on a canvas where pivot is at centre:
    big = Image.new('RGBA', (w*scale, h*scale), (0,0,0,0))
    big.paste(im, (w + (w*scale//2 - cx), h + (h*scale//2 - cy)))
    rot = big.rotate(angle_deg, resample=Image.BICUBIC, expand=False)
    # pivot is now at canvas centre
    bbox = rot.getchannel('A').getbbox()
    if bbox is None:
        raise ValueError('rotated image empty')
    trimmed = rot.crop(bbox)
    new_pivot = (w*scale//2 - bbox[0], h*scale//2 - bbox[1])
    return trimmed, new_pivot
if __name__ == '__main__':
    from PIL import Image as I
    im = I.open(sys.argv[1]); px,py = int(sys.argv[2]), int(sys.argv[3]); ang=float(sys.argv[4])
    out,piv = rotate_about_pivot(im,(px,py),ang)
    out.save(sys.argv[5]); print(f"OK size={out.size} new_pivot={piv}")
