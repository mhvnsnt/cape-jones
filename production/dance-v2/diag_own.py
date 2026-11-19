#!/usr/bin/env python3
import numpy as np
from PIL import Image
import os, importlib.util
spec = importlib.util.spec_from_file_location('bd3', os.path.join(os.path.dirname(__file__), 'build_dance_v3.py'))
bd3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(bd3)
P = os.path.expanduser('~/workspace/_cj-dance-v2/build/parts2')
fig = Image.open(f'{P}/figure2_rgba.png')
layers, piv = bd3.segment(fig)
cols = {'cape': (160, 0, 200), 'leg_r': (0, 200, 0), 'leg_l': (0, 120, 255),
        'torso': (255, 200, 0), 'sock_l': (255, 120, 0), 'sock_r': (255, 60, 120),
        'arm_l': (255, 0, 0), 'arm_r': (200, 0, 0), 'head': (0, 255, 255)}
w, h = fig.size
m = np.zeros((h, w, 3), np.uint8)
for k, c in cols.items():
    a = np.array(layers[k].getchannel('A')) > 0
    m[a] = c
Image.fromarray(m).save(f'{P}/ownership.png')
# neutral drawing on sky for reference
d = bd3.build_drawing(layers, piv, bd3.sample(0))
bg = Image.new('RGBA', fig.size, (110, 190, 245, 255)); bg.alpha_composite(d)
bg.convert('RGB').save(f'{P}/neutral_check.png')
print('ownership + neutral saved')
