import json, os, shutil, sys, time
from gradio_client import Client, handle_file
import httpx as _hx

BASE = os.path.expanduser("~/workspace/_cj-dance-v2")
batch = json.load(open(f"{BASE}/dataset/batch.json"))
src_dir = f"{BASE}/build/vace_in"
out_dir = f"{BASE}/altgpu_out"
os.makedirs(out_dir, exist_ok=True)
only = sys.argv[1:] or [f"sec{i}" for i in range(7)]

client = Client("fffiloni/Wan2.1-VACE-1.3B", httpx_kwargs={"timeout": _hx.Timeout(3600.0, connect=120.0)})
print("connected", flush=True)
for sec in only:
    dst = f"{out_dir}/{sec}.mp4"
    if os.path.exists(dst) and os.path.getsize(dst) > 10000:
        print(sec, "already done, skip", flush=True); continue
    meta = [s for s in batch["sections"] if s["video"] == f"{sec}.mp4"][0]
    t0 = time.time()
    result = client.predict(
        output_gallery=[],
        src_video={"video": handle_file(f"{src_dir}/{meta['video']}"), "subtitles": None},
        src_mask={"video": handle_file(f"{src_dir}/{meta['mask']}"), "subtitles": None},
        src_ref_image_1=handle_file(f"{src_dir}/ref.png"),
        src_ref_image_2=handle_file(f"{src_dir}/ref_hero.png"),
        src_ref_image_3=handle_file(f"{src_dir}/ref_head.png"),
        prompt=batch["prompt"],
        negative_prompt=batch["negative"],
        shift_scale=16.0,
        sample_steps=batch["steps"],
        context_scale=1.0,
        guide_scale=float(batch["cfg"]),
        infer_seed=2025,
        output_height="480",
        output_width="832",
        frame_rate="16",
        num_frames="49",
        api_name="/generate",
    )
    # result: gallery list of dicts; find the video entry
    print(sec, "raw result:", json.dumps(result, default=str)[:500], flush=True)
    vid = None
    items = result if isinstance(result, list) else [result]
    for it in items:
        v = (it or {}).get("video") if isinstance(it, dict) else None
        if v and v.get("path"):
            vid = v["path"]; break
        im = (it or {}).get("image") if isinstance(it, dict) else None
        if im and im.get("path") and im["path"].endswith(".mp4"):
            vid = im["path"]; break
    if not vid:
        print(sec, "NO VIDEO IN RESULT", flush=True); continue
    shutil.copy(vid, dst)
    print(sec, "SAVED", dst, os.path.getsize(dst), f"{time.time()-t0:.0f}s", flush=True)
print("ALL DONE", flush=True)
