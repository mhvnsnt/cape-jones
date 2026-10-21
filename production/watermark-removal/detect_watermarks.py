import cv2, numpy as np

def glyph_mask(tmpl_path, thresh):
    t = cv2.imread(tmpl_path)
    g = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY).astype(np.float32)
    bg = cv2.GaussianBlur(g, (0, 0), 6)
    return (g - bg) > thresh

LEFT_MASK = glyph_mask('/home/hatch/workspace/viggle-inputs/wm-proper/wm_template_left.png', 60)
RIGHT_MASK = glyph_mask('/home/hatch/workspace/viggle-inputs/wm-proper/rbox-140.png', 40)
print(f"left glyph px: {LEFT_MASK.sum()}, right glyph px: {RIGHT_MASK.sum()}")
LEFT_BOX = (15, 935)    # 300x90
RIGHT_BOX = (720, 1355) # 300x90

def detect(frame, box, mask):
    x, y = box
    h, w = mask.shape
    roi = frame[y:y+h, x:x+w].astype(np.int32)
    if roi.shape[0] != h or roi.shape[1] != w:
        return -1, -1
    mn = roi.min(axis=2); mx = roi.max(axis=2)
    white = (mn > 170) & ((mx - mn) < 45)
    return white[mask].mean(), white.mean()

cap = cv2.VideoCapture('/home/hatch/workspace/viggle-inputs/cape-jones-episode-v4.mp4')
tests = [
    (45, 'R', 'present'), (50, 'R', 'present'), (140, 'R', 'present'), (155, 'R', 'present'), (78, 'R', 'present'),
    (10, 'R', 'absent'), (30, 'R', 'absent'), (110, 'R', 'absent'), (160, 'R', 'absent'), (95, 'R', 'absent'),
    (70, 'L', 'present'), (89, 'L', 'present'), (147, 'L', 'present'),
    (10, 'L', 'absent'), (30, 'L', 'absent'), (120, 'L', 'absent'), (155, 'L', 'absent'), (50, 'L', 'SUIT'),
    (160, 'L', 'absent'), (45, 'L', 'absent'),
]
for t, which, exp in tests:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ret, frame = cap.read()
    if not ret:
        print(f"t={t} {which}: NO FRAME"); continue
    if which == 'L':
        s, f = detect(frame, LEFT_BOX, LEFT_MASK)
    else:
        s, f = detect(frame, RIGHT_BOX, RIGHT_MASK)
    print(f"t={t} {which}: glyph_score={s:.3f} box_white_frac={f:.3f}  (expected {exp})")
cap.release()
