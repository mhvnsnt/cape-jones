# === Patch ToonCrafter for FP16 execution (fits T4 VRAM) ===
# v5 (2026-10-17): Non-fatal patch. If the upstream anchor is missing or
# the patch is already applied, log and continue instead of asserting.
# The official README's 12GB figure assumes fp16 execution. Stock inference.py
# loads weights into an fp32 model — load_state_dict casts fp16->fp32, so
# weights alone can push past 16GB on a T4. We patch run_inference() to
# half() the model right after checkpoint load.
import os
p = "/kaggle/working/ToonCrafter/scripts/evaluation/inference.py"
if not os.path.exists(p):
    print(f"WARNING: {p} not found — skipping FP16 patch")
else:
    src = open(p).read()
    old = "    model = load_model_checkpoint(model, args.ckpt_path)\n    model.eval()"
    new = ("    model = load_model_checkpoint(model, args.ckpt_path)\n"
           "    model = model.half()  # v5: FP16 execution -> ~12GB VRAM on T4\n"
           "    model.eval()")
    if "model = model.half()" in src:
        print("FP16 patch already applied — skipping")
    elif old in src:
        open(p, "w").write(src.replace(old, new))
        print("FP16 execution patch applied to inference.py")
    else:
        print("WARNING: PATCH ANCHOR NOT FOUND — upstream inference.py changed.")
        print("         Continuing without the half() patch. Watch VRAM.")
        print("         You may need to update the anchor string in this cell.")
