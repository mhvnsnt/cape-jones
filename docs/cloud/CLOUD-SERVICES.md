# Cloud Services — Master Reference

Every cloud service the owner has or can use. All tied to **fmmg.mars@gmail.com**
unless noted. **Free tiers only — never enter card details without asking.**

Last updated: 2026-10-16

---

## GPU / Compute

### Kaggle (marsfmmg) — PRIMARY GPU
- **What:** Notebook GPU compute
- **Login:** Google sign-in (fmmg.mars@gmail.com)
- **Free tier:** 30 GPU-hours/week, T4 x2 (2x Tesla T4, 16GB each)
- **Limits:** 1 interactive GPU session at a time; weekly quota resets
- **Used for:** Pantera renders, ToonCrafter, Viggle, RIFE — the main workhorse
- **Automation:** `~/workspace/tools/kaggle-queue/kaggle_queue.py` manages a job queue via batch API
- **Status:** ✅ Active, in use

### Google Colab — SECONDARY GPU (parallel)
- **What:** Browser notebook GPU compute
- **Login:** Google sign-in (fmmg.mars@gmail.com) — session confirmed active
- **Free tier:** T4 GPU (16GB), ~12hr max session, ~90min idle disconnect, availability not guaranteed
- **Limits:** No guaranteed GPU; premium GPUs (A100, H100) disabled on free tier
- **Used for:** Lighting gag reel notebook (`production/colab/cape_jones_lighting_reel_colab.ipynb` in cape-jones repo)
- **Why:** Runs in parallel while Kaggle is busy — a second GPU for free
- **Status:** ✅ Account verified, notebook ready — **needs browser to open and Run All**

### Lightning AI (fmmgmars)
- **What:** Cloud IDE + GPU Studios
- **Login:** fmmgmars account, phone verified
- **Credits:** 30.00 displayed BUT billing discrepancy unresolved (Oct 2026) — a $30 order appeared with no matching charge. **Treat as uncertain; may be revoked.**
- **Free tier:** ~22 GPU-hours/month on T4 (if credits hold)
- **Status:** ⚠️ Credits frozen pending owner confirmation — do not spend until he clears it

### Modal (mhvnsnt)
- **What:** Serverless GPU compute (API-driven, no notebooks)
- **Login:** Signed in, $1 of $30/mo free credits available
- **GPUs:** T4/L4/A10G, pay-per-second
- **Client:** Installed at `~/workspace/tools/modal-venv`
- **Status:** ✅ Signed in, minimal credits — useful for quick serverless jobs

### Hugging Face
- **What:** Model hub + Spaces (free GPU demos) + ZeroGPU
- **Login:** Email verified
- **Free tier:** Spaces with shared GPU queue, ZeroGPU serverless inference
- **Status:** ✅ Verified

### Saturn Cloud
- **What:** Cloud notebooks with GPU
- **Login:** Signed in
- **Status:** ⚠️ Billing locked (missing/invalid payment) — backup only, needs card to unlock

### Google Cloud
- **What:** Full GCP (VMs, GPUs, storage)
- **Login:** 2FA completed by owner
- **Free tier:** $300/90-day trial NOT activated
- **Status:** ⚠️ Trial not started — save this for when we need it

---

## Cloud Code Environments

### Aider
- **What:** Open-source AI pair programmer (terminal, Apache 2.0)
- **Setup:** `pip install aider-chat` — config at `~/workspace/tools/aider-config/.aider.conf.yml`
- **Model:** Defaults to Gemini 2.0 Flash (free tier) — set `GEMINI_API_KEY` env var
- **Why:** AI code editing from the terminal, no phone needed
- **Status:** ✅ Config written, ready to install

### GitHub Codespaces
- **What:** Browser-based VS Code, full dev environment in the cloud
- **Login:** GitHub (mhvnsnt) — automatic, no separate signup
- **Free tier:** 120 core-hours/month (60 hrs on 2-core), 15GB storage
- **Limits:** No GPU on free tier; usage blocked at quota without a payment method on file
- **Why:** Full IDE from his phone browser — edit code, run scripts, push commits
- **How:** GitHub repo → Code → Codespaces → Create codespace
- **Status:** ✅ Available — **needs browser to launch first codespace**

### Replit
- **What:** Browser IDE with instant hosting
- **Login:** Owner has an account (per prior context)
- **Free tier:** Basic repls, limited compute
- **Why:** Quick prototyping from phone browser
- **Status:** ⚠️ Account exists — **needs browser to verify access**

---

## 3D / Render Services

### SheepIt Render Farm
- **What:** Free community Blender render farm
- **How it works:** Contribute your compute → earn points → spend on your renders
- **Cost:** $0, but you wait in queue
- **Best for:** Non-urgent personal projects (not client/NDA work — your .blend runs on volunteers' machines)
- **Status:** 📋 Documented — **needs browser to create account**

### Colab Blender (DIY)
- **What:** Open-source notebooks that install Blender on Colab GPU
- **Status:** ✅ We built our own (`production/colab/` in cape-jones repo)

---

## AI Services (APIs)

| Service | Login | Free tier | Used for |
|---------|-------|-----------|----------|
| Pollinations.ai | None needed | Free, no signup | Text + image generation (tested working) |
| Groq | `custom.legacy-groq` connector | Free tier, very fast | LLM inference, Aider backend option |
| Google Gemini | `custom.legacy-gemini` connector | Free tier via AI Studio | Image gen/edit, Aider backend |
| Mistral | `custom.legacy-mistral` connector | Free tier | LLM, OCR |
| ElevenLabs | `custom.legacy-elevenlabs` connector | Free tier | Voice/TTS |
| AI Horde | `custom.legacy-ai-horde` connector | Free (crowdsourced) | Image generation |

---

## Storage

### TeraBox (fmmg.mars@gmail.com, Mars FMMG, Premium+)
- **What:** 5TB cloud storage ($0.50/7-day trial, renews 2026-10-20)
- **Used for:** Bulk archives, CN-Gigaleak per-show folders
- **Status:** ✅ Active

### Google Drive (fmmg.mars@gmail.com)
- **What:** 15GB free
- **Used for:** Colab file staging, quick shares
- **Status:** ✅ Active

---

## Colab Pro — Should We Pay?

| Tier | Cost | What you get |
|------|------|--------------|
| Free | $0 | T4, 12hr sessions, 90min idle kill, no guarantees |
| Pro | $9.99/mo | 100 compute units, no idle disconnect, 24hr sessions |
| Pro+ | $49.99/mo | 600 units, background execution |

**Verdict:** Free tier is enough for the lighting reel (one-shot render, not interactive).
Don't pay unless free GPU availability becomes a blocker. **Ask the owner first.**

---

## What Needs a Browser (handoff to parent agent)

These steps require live browser interaction (sign-in, clicking, 2FA):

1. **Colab lighting reel** — Open https://colab.research.google.com/github/mhvnsnt/cape-jones/blob/main/production/colab/cape_jones_lighting_reel_colab.ipynb → Runtime → Change runtime type → T4 GPU → Run All → download MP4 when done
2. **GitHub Codespaces** — Open mhvnsnt/cape-jones → Code → Codespaces → Create codespace → verify it boots
3. **Replit** — Sign in, verify account access, create a test repl
4. **SheepIt** — Create account at sheepit-renderfarm.com if we want community render capacity
5. **Aider** — `pip install aider-chat` can run headless, but the `GEMINI_API_KEY` needs to be obtained from aistudio.google.com (browser)

## What I Did Without a Browser

- ✅ Built the Colab notebook (validated JSON, 6 cells)
- ✅ Pushed `living_room.blend` + notebook to cape-jones repo (PR #23, merged)
- ✅ Wrote Aider config (Gemini free tier default, no auto-commits)
- ✅ This documentation
- ✅ Researched all free tiers and limits (Oct 2026 data)
