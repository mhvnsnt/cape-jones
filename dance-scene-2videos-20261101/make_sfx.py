#!/usr/bin/env python3
"""Synthesised original SFX, NOT copyrighted show audio, NOT a song.
Generated with numpy: footsteps (filtered noise bursts), bounce thumps (low sine),
whoosh (noise sweep envelope), finger snap (short high noise + 2kHz burst).
Beat grid: 107 BPM visual, beat = 60/107 = 0.5607s. Cuts at frames:
cut1 0-432, cut2 432-936, cut3 936-1364, cut4 1364-1796, hold 1796-1819 @24fps.
"""
import numpy as np, sys
from scipy.io import wavfile
SR = 44100; DUR = 75.789
BEAT = 60/107
def burst(t0, dur, kind):
    n = int(dur*SR); i0 = int(t0*SR)
    if i0+n > len(buf): n = len(buf)-i0
    if n <= 0: return
    t = np.arange(n)/SR
    if kind == 'step':
        x = np.random.randn(n); x = np.convolve(x, np.ones(20)/20, mode='same')
        env = np.exp(-t*30); y = x*env*0.5
    elif kind == 'thump':
        y = np.sin(2*np.pi*70*t)*np.exp(-t*18)*0.8
    elif kind == 'whoosh':
        x = np.random.randn(n); x = np.convolve(x, np.ones(50)/50, mode='same')
        env = np.sin(np.pi*np.arange(n)/n)**2; y = x*env*0.7
    elif kind == 'snap':
        x = np.random.randn(n); x = np.diff(np.concatenate([[0],x]))
        y = (x*0.6 + np.sin(2*np.pi*2000*t)*np.exp(-t*120)*0.4)
    else: return
    buf[i0:i0+n] += y

def make(path, video):
    global buf
    buf = np.zeros(int(DUR*SR))
    # footsteps + thumps on every beat, all cuts
    t = 0.0
    while t < DUR:
        burst(t, 0.08, 'step'); burst(t, 0.15, 'thump'); t += BEAT
    if video == 'V1':
        # cut2 Richard bounce: extra thump every beat already, add stronger thump at half-beats in cut2
        t = 432/24
        while t < 936/24:
            burst(t, 0.12, 'thump'); t += BEAT/2
        # cut3 Scooby stepping: extra steps at half-beats
        t = 936/24
        while t < 1364/24:
            burst(t, 0.08, 'step'); t += BEAT/2
        # cut4 Johnny punch/snap: whoosh every 2 beats, snap every 4 beats
        t = 1364/24; k = 0
        while t < 1796/24:
            burst(t, 0.30, 'whoosh')
            if k % 2 == 0: burst(t, 0.03, 'snap')
            t += BEAT*2; k += 1
    else:
        # V2: cut2 pose-swap snaps every beat, cut4 kick whoosh every 2 beats
        t = 432/24
        while t < 936/24:
            burst(t, 0.03, 'snap'); t += BEAT
        t = 1364/24
        while t < 1796/24:
            burst(t, 0.30, 'whoosh'); t += BEAT*2
    # normalise SFX to peak 0.35, stereo (same both channels, steps alternate pan slightly via simple gain)
    m = np.max(np.abs(buf)) or 1
    buf = buf/m*0.35
    stereo = np.stack([buf, buf], axis=1)
    wavfile.write(path, SR, (stereo*32767).astype(np.int16))
    print(path, "peak", float(np.max(np.abs(buf))))

if __name__ == '__main__':
    make(sys.argv[1], sys.argv[2])
