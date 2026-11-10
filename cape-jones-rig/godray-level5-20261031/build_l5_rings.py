"""Side-weighted outer rim rings + apose bleed mask, from L3/apose masks."""
import numpy as np
from PIL import Image
R = '/home/hatch/workspace/cape-jones-rig'
OUT = R + '/godray-level5-20261031'
L3 = R + '/godray-level3-20261031'
def load(p): return Image.open(p).convert('RGBA')
def side_weight(arr):
    W = arr.shape[1]
    w = np.linspace(1.0, 0.35, W, dtype=np.float32)[None, :]
    arr[..., 3] = arr[..., 3] * w
    return arr
def ring(solid_path, mask_path, out_name, weighted):
    solid = np.asarray(load(solid_path), dtype=np.float32)
    mask = np.asarray(load(mask_path), dtype=np.float32)[..., 3] / 255.0
    layer = np.zeros((*mask.shape, 4), dtype=np.float32)
    layer[..., :3] = solid[..., :3]
    layer[..., 3] = mask * 255.0
    if weighted:
        layer = side_weight(layer)
    Image.fromarray(layer.astype(np.uint8)).save(f'{OUT}/{out_name}')
    print('saved', out_name)
from scipy import ndimage
# arms-up outer gold ring, side-weighted
ring(L3 + '/solid-gold.png', L3 + '/mask-outer.png', 'rim-outer-gold-sideweighted-armsup.png', True)
# apose outer gold ring, side-weighted + apose bleed mask (dilate 8 ring)
ring(L3 + '/solid-gold.png', OUT + '/mask-outer-apose.png', 'rim-outer-gold-sideweighted-apose.png', True)
apose = np.asarray(load(R + '/rig-apose-v7c-clean-transparent.png'))[..., 3] > 10
d8 = ndimage.binary_dilation(apose, iterations=8)
bleed = (d8 & ~apose).astype(np.uint8) * 255
layer = np.zeros((*bleed.shape, 4), dtype=np.uint8); layer[..., 3] = bleed
Image.fromarray(layer).save(f'{OUT}/mask-bleed-apose.png'); print('saved mask-bleed-apose.png')
print('RINGS DONE')
