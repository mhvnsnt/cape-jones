import cv2, numpy as np

# Fit per-channel affine transform: v4_frame = a * v3_frame + b, using the paired frame at t=83.1
# (same edit frame in both files; v3 = grade released, v4 = magenta held)
V3 = '/home/hatch/workspace/viggle-inputs/cape-jones-episode-v3.mp4'
V4 = '/home/hatch/workspace/viggle-inputs/cape-jones-episode-v4.mp4'

def frame_at(path, ms):
    cap = cv2.VideoCapture(path)
    cap.set(cv2.CAP_PROP_POS_MSEC, ms)
    ret, f = cap.read()
    cap.release()
    return f.astype(np.float32) if ret else None

a_list, b_list = [], []
for t in (83100, 83200):
    x = frame_at(V3, t)   # ungraded (BGR)
    y = frame_at(V4, t)   # magenta-graded (BGR)
    if x is None or y is None:
        print(f"t={t}: missing frame"); continue
    a = np.zeros(3); b = np.zeros(3)
    for c in range(3):
        xs = x[:, :, c].ravel(); ys = y[:, :, c].ravel()
        A = np.vstack([xs, np.ones_like(xs)]).T
        coef, *_ = np.linalg.lstsq(A, ys, rcond=None)
        a[c], b[c] = coef
    a_list.append(a); b_list.append(b)
    print(f"t={t}: a={np.round(a,3)} b={np.round(b,1)}")
    # verification: apply to x, compare to y
    pred = np.clip(x * a + b, 0, 255)
    err = np.abs(pred - y).mean()
    print(f"   mean abs error of fit: {err:.2f} (per-pixel, 0-255 scale)")

if a_list:
    np.savez('/home/hatch/workspace/viggle-inputs/wm-proper/magenta_transform.npz',
             a=np.mean(a_list, axis=0), b=np.mean(b_list, axis=0))
    print("saved mean transform: a=", np.round(np.mean(a_list, axis=0), 3), " b=", np.round(np.mean(b_list, axis=0), 1))
