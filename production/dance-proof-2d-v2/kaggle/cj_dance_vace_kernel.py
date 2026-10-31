# Cape Jones dance v2 - Wan2.1 VACE redraw on Kaggle T4 x2.
# Method (owner correction 2026-10-29): NO hand-rotated cutout final. The
# cutout composite is only the DRIVING video; VACE redraws the character
# region (white mask) holding the likeness of the sheet reference, at
# QUALITY settings in the class of the accel A/B's winning baseline20
# (full steps, cfg 5, full fp32 VAE decode - NOT the rejected dmd4/tae
# fast setup). Structure is unchanged: same simple dance loop, same
# sections; VACE cleans the frames, it does not add motion.
# HONESTY CONTRACT: never writes a clip it did not render; failures are
# recorded in manifest["failed"].
import gc, json, os, time, hashlib, glob, traceback, subprocess, sys
from pathlib import Path
T0 = time.time()
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "git+https://github.com/huggingface/diffusers",
                "transformers>=4.49", "accelerate", "ftfy", "imageio[ffmpeg]", "safetensors"], check=False)
import torch, numpy as np
from PIL import Image
import imageio.v2 as imageio
import diffusers
from diffusers import WanVACEPipeline, AutoencoderKLWan
from diffusers.utils import export_to_video

inp = Path(glob.glob("/kaggle/input/**/batch.json", recursive=True)[0]).parent
B = json.loads((inp / "batch.json").read_text())
ROOT = Path("/kaggle/working/out"); ROOT.mkdir(parents=True, exist_ok=True)
FPS, W, H, NF = 16, 832, 480, 49
MODEL = "Wan-AI/Wan2.1-VACE-1.3B-diffusers"
STEPS, CFG = B.get("steps", 30), B.get("cfg", 5.0)
env = {"gpu": torch.cuda.get_device_name(0), "n_gpu": torch.cuda.device_count(),
       "diffusers": diffusers.__version__, "torch": torch.__version__,
       "install_s": round(time.time() - T0, 1), "model": MODEL, "steps": STEPS, "cfg": CFG}
print("ENV", env, flush=True)

def read_frames(path, n=NF):
    rd = imageio.get_reader(str(path))
    frames = []
    for i, fr in enumerate(rd):
        if i >= n: break
        frames.append(Image.fromarray(np.asarray(fr)[:, :, :3].astype(np.uint8)).convert("RGB"))
    rd.close()
    return frames

tl = time.time()
vae = AutoencoderKLWan.from_pretrained(MODEL, subfolder="vae", torch_dtype=torch.float32)
pipe = WanVACEPipeline.from_pretrained(MODEL, vae=vae, torch_dtype=torch.float16)
pipe.vae.enable_tiling()
TWO = torch.cuda.device_count() > 1
if TWO:
    TE = pipe.text_encoder.to("cuda:1"); pipe.text_encoder = None
else:
    TE = pipe.text_encoder
pipe.transformer.to("cuda:0"); pipe.vae.to("cuda:0")
load_s = round(time.time() - tl, 1)
refs = [Image.open(inp / r).convert("RGB") for r in B.get("references", [B["reference"]])]

man = {"env": env, "load_s": load_s, "clips": {}, "failed": {}}
for sec in B["sections"]:
    sid = sec["id"]
    try:
        torch.cuda.reset_peak_memory_stats(); ts = time.time()
        video = read_frames(inp / sec["video"])
        mask = read_frames(inp / sec["mask"])
        mask = [m.point(lambda p: 255 if p > 127 else 0) for m in mask]
        assert len(video) == NF and len(mask) == NF, f"frame count {len(video)}/{len(mask)}"
        dev = "cuda:1" if TWO else "cuda:0"
        pipe.text_encoder = TE
        with torch.no_grad():
            pe, ne = pipe.encode_prompt(prompt=B["prompt"], negative_prompt=B["negative"],
                                        do_classifier_free_guidance=CFG > 1, device=torch.device(dev))
        pipe.text_encoder = None
        pe = pe.to("cuda:0"); ne = ne.to("cuda:0") if ne is not None else None
        with torch.no_grad():
            out = pipe(video=video, mask=mask, reference_images=refs,
                       prompt_embeds=pe, negative_prompt_embeds=ne,
                       height=H, width=W, num_frames=NF,
                       num_inference_steps=STEPS, guidance_scale=CFG,
                       generator=torch.Generator("cpu").manual_seed(42 + sec["index"]))
        frames = [np.asarray(f) for f in out.frames[0]]
        frames = [(f * 255).clip(0, 255).astype("uint8") if f.dtype != np.uint8 else f for f in frames]
        gc.collect(); torch.cuda.empty_cache()
        wall = time.time() - ts
        OUT = ROOT / sid; OUT.mkdir(exist_ok=True)
        mp4 = OUT / f"{sid}.mp4"
        export_to_video([f / 255.0 for f in frames], str(mp4), fps=FPS)
        for i in (0, 24, 48): Image.fromarray(frames[i]).save(OUT / f"{sid}.f{i}.png")
        # likeness/continuity proxy vs the driving frames (whole frame)
        drv = read_frames(inp / sec["video"])
        prox = {}
        for i in (0, 24, 48):
            x = np.asarray(drv[i]).astype(np.float32); y = frames[i].astype(np.float32)
            mse = ((x - y) ** 2).mean()
            gx, gy = x.mean(2).ravel(), y.mean(2).ravel()
            prox[f"f{i}"] = {"psnr_vs_driving": round(float(10 * np.log10(255 ** 2 / max(mse, 1e-6))), 2),
                             "gray_corr_vs_driving": round(float(np.corrcoef(gx, gy)[0, 1]), 4)}
        man["clips"][sid] = {"sha256": hashlib.sha256(mp4.read_bytes()).hexdigest(), "frames": len(frames),
                             "wall_s": round(wall, 1), "peak_vram_gb": round(torch.cuda.max_memory_allocated() / 1e9, 2),
                             "vs_driving": prox}
        print("OK", sid, man["clips"][sid], flush=True)
    except Exception as e:
        man["failed"][sid] = traceback.format_exc()[-3000:]
        print("FAIL", sid, e, flush=True)
man["total_wall_s"] = round(time.time() - T0, 1)
(ROOT / "manifest.json").write_text(json.dumps(man, indent=1))
print("DONE", json.dumps({k: man[k] for k in ("load_s", "total_wall_s")}), "clips:", list(man["clips"]), "failed:", list(man["failed"]))
