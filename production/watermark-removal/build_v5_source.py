import cv2, numpy as np, subprocess, sys

V3 = '/home/hatch/workspace/viggle-inputs/cape-jones-episode-v3.mp4'
V4 = '/home/hatch/workspace/viggle-inputs/cape-jones-episode-v4.mp4'
OUT = '/home/hatch/workspace/viggle-inputs/cape-jones-episode-v5.mp4'
TMP = '/home/hatch/workspace/viggle-inputs/v5-novid.mp4'

# affine magenta fit (BGR), from magenta_fit.py at t=83.1/83.2
A = np.array([0.729, 1.30, 0.59], dtype=np.float32)
B = np.array([42.9, -54.8, 83.3], dtype=np.float32)

# blur corner region in v4
CX1, CY1, CX2, CY2 = 755, 1735, 1080, 1920
FEATHER = 16
# feather alpha for corner patch: 1 inside, ramping to 0 at top/left outer edges
ch, cw = CY2 - CY1, CX2 - CX1
alpha = np.ones((ch, cw), dtype=np.float32)
ramp_y = np.linspace(0, 1, FEATHER, dtype=np.float32)
ramp_x = np.linspace(0, 1, FEATHER, dtype=np.float32)
alpha[:FEATHER, :] *= ramp_y[:, None]
alpha[:, :FEATHER] *= ramp_x[None, :]
alpha = alpha[:, :, None]

cap3 = cv2.VideoCapture(V3)
cap4 = cv2.VideoCapture(V4)
fps = cap3.get(cv2.CAP_PROP_FPS)
W = int(cap3.get(cv2.CAP_PROP_FRAME_WIDTH)); H = int(cap3.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f'fps={fps} {W}x{H}', flush=True)

WIN_START, WIN_END = 83.0, 83.5  # seconds
writer = cv2.VideoWriter(TMP, cv2.VideoWriter_fourcc(*'mp4v'), fps, (W, H))
i = 0
lifted = 0
while True:
    r3, f3 = cap3.read()
    r4, f4 = cap4.read()
    if not r3:
        break
    t = i / fps
    out = f3
    if r4 and WIN_START <= t < WIN_END:
        # does v4 hold magenta here vs v3?
        m3 = f3.reshape(-1, 3).mean(axis=0)
        m4 = f4.reshape(-1, 3).mean(axis=0)
        if (m4[2] - m4[1]) - (m3[2] - m3[1]) > 15:
            cand = f4.astype(np.float32)
            corner3 = f3[CY1:CY2, CX1:CX2].astype(np.float32)
            graded_corner = np.clip(corner3 * A + B, 0, 255)
            cand[CY1:CY2, CX1:CX2] = graded_corner * alpha + cand[CY1:CY2, CX1:CX2] * (1 - alpha)
            out = cand.astype(np.uint8)
            lifted += 1
    writer.write(out)
    i += 1
    if i % 500 == 0:
        print(f'{i} frames, lifted={lifted}', flush=True)
cap3.release(); cap4.release(); writer.release()
print(f'video done: {i} frames, {lifted} lifted', flush=True)

r = subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', TMP, '-i', V3,
                    '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-preset', 'medium',
                    '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', OUT],
                   capture_output=True, text=True)
print('mux rc:', r.returncode, r.stderr[-200:] if r.returncode else 'ok', flush=True)
