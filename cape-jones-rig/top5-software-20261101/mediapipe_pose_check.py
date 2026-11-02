import math
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
print("mediapipe", mp.__version__)
base = mp_python.BaseOptions(model_asset_path="/home/hatch/workspace/cape-jones-rig/mediapipe-venv-20261101/models/pose_landmarker_heavy.task")
opts = vision.PoseLandmarkerOptions(base_options=base, running_mode=vision.RunningMode.IMAGE, num_poses=1, min_pose_detection_confidence=0.5, min_pose_presence_confidence=0.5, min_tracking_confidence=0.5)
landmarker = vision.PoseLandmarker.create_from_options(opts)
names = ['nose','leye_in','leye','leye_out','reye_in','reye','reye_out','lear','rear','mouth_l','mouth_r','lsho','rsho','lelb','relb','lwri','rwri','lpinky','rpinky','lidx','ridx','lthumb','rthumb','lhip','rhip']
files = [
 "/home/hatch/workspace/cape-jones-rig/side-rig-fixed-20261101/side-bent-correct-grey-20261101.png",
 "/home/hatch/workspace/cape-jones-rig/side-rig-fixed-20261101/side-idle-arms-down-fixed-20261101.png",
 "/home/hatch/workspace/cape-jones-rig/side-rig-fixed-20261101/side-bent-correct-20261101.png",
]
def angle(a,b,c):
    v1=(a.x-b.x, a.y-b.y); v2=(c.x-b.x, c.y-b.y)
    d=(v1[0]*v2[0]+v1[1]*v2[1])/(math.hypot(*v1)*math.hypot(*v2)+1e-9)
    return math.degrees(math.acos(max(-1,min(1,d))))
for f in files:
    print(f"\n=== {f} ===")
    img = mp.Image.create_from_file(f)
    res = landmarker.detect(img)
    print("poses found:", len(res.pose_landmarks))
    if not res.pose_landmarks:
        print("RESULT: NO POSE LANDMARKS DETECTED")
        continue
    lm = res.pose_landmarks[0]
    print(f"RESULT: {len(lm)} landmarks")
    for i,n in enumerate(names):
        p = lm[i]
        print(f"  {n:8s} x={p.x:.4f} y={p.y:.4f} vis={p.visibility:.3f} pres={p.presence:.3f}")
    for side, s,e,w in [('L',11,13,15),('R',12,14,16)]:
        print(f"  elbow-{side}: angle={angle(lm[s],lm[e],lm[w]):.1f}deg elbow_x-shoulder_x={lm[e].x-lm[s].x:+.4f} wrist_x-elbow_x={lm[w].x-lm[e].x:+.4f} elbow_y-shoulder_y={lm[e].y-lm[s].y:+.4f} (image y down)")
    print(f"  facing proxy: nose_x={lm[0].x:.4f} lear_x={lm[7].x:.4f} rear_x={lm[8].x:.4f} lsho_x={lm[11].x:.4f} rsho_x={lm[12].x:.4f}")
