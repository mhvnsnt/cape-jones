#!/usr/bin/env python3
"""MediaPipe Tasks PoseLandmarker, heavy model, RUN on every gate composite.
Model: pose_landmarker_heavy, float16, from Google mediapipe-models storage.
Cartoon figure: detection is expected to be low — record it honestly, do not
invent keypoints. L/R ankle fallback is the alpha-split measurement in gate-30.
"""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/pose-libs"))
import warnings; warnings.filterwarnings("ignore")
from PIL import Image
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
RIG=os.path.expanduser("~/workspace/cape-jones-rig")
OUT=os.path.join(RIG,"ground-gate-complete-20261031")
gate=json.load(open(os.path.join(OUT,"gate-30-results.json")))
base=vision.PoseLandmarkerOptions(
  base_options=mp_python.BaseOptions(model_asset_path=os.path.expanduser("~/pose-models/pose_landmarker_heavy.task")),
  running_mode=vision.RunningMode.IMAGE, num_poses=1, min_pose_detection_confidence=0.3)
landmarker=vision.PoseLandmarker.create_from_options(base)
NAMES={27:"left_knee",28:"right_knee",29:"left_ankle",30:"right_ankle",31:"left_heel",32:"right_heel",23:"left_hip",24:"right_hip"}
rows=[]
for r in gate:
    path=os.path.join(OUT,r["composite"])
    img=Image.open(path).convert("RGB")
    mpimg=mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(img))
    res=landmarker.detect(mpimg)
    if res.pose_landmarks:
        lm=res.pose_landmarks[0]
        # presence: in tasks API landmarks carry presence? use visibility if present else 1.0
        def conf(i):
            l=lm[i]; return float(getattr(l,"presence", getattr(l,"visibility", 0.0)) or 0.0)
        kps={}
        for i,name in NAMES.items():
            l=lm[i]; kps[name]={"x_px":round(l.x*img.width,1),"y_px":round(l.y*img.height,1),"conf":round(conf(i),3)}
        # overall = mean ankle/heel conf
        oc=round(sum(kps[k]["conf"] for k in ["left_ankle","right_ankle","left_heel","right_heel"])/4,3)
        rows.append({"shot":r["shot"],"detected":True,"overall_ankle_conf":oc,"keypoints":kps})
        print(r["shot"],"DETECTED ankle_conf",oc, kps["left_ankle"], kps["right_ankle"])
    else:
        rows.append({"shot":r["shot"],"detected":False,"overall_ankle_conf":0.0,"keypoints":{}})
        print(r["shot"],"NO DETECTION")
json.dump({"model":"MediaPipe Tasks PoseLandmarker heavy (pose_landmarker_heavy, float16, mediapipe 1.2.0)",
 "min_pose_detection_confidence":0.3,"note":"Cartoon rig figure on grey canvas; detection rate is reported honestly, not used to override alpha L/R feet.",
 "results":rows}, open(os.path.join(OUT,"pose-30-results.json"),"w"), indent=2)
print("detected:",sum(1 for x in rows if x["detected"]),"/",len(rows))
