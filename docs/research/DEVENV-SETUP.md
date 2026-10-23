# Dev Environment Setup — Colab + Aider + Free IDEs

**For the Cape Jones pipeline. Owner: fmmg.mars@gmail.com (phone-only — everything
computer-side runs through agents).**

All free tier. No card details. Ever.

---

## 1. Google Colab — Backup/Parallel GPU Lane

Colab is our **second GPU** alongside Kaggle (30h/wk). Use it when:
- Kaggle quota is running low
- You want two jobs running in parallel (one on Kaggle, one on Colab)
- Kaggle is having issues

### Setup (one time)

1. Go to https://colab.research.google.com
2. Sign in with **fmmg.mars@gmail.com** (owner's Google — blanket permission on file)
3. Upload a notebook from `production/colab/` (File → Upload notebook)
4. **Runtime → Change runtime type → T4 GPU** → Save
5. **Runtime → Run all**

### Available notebooks (`production/colab/`)

| Notebook | What | Generator |
|----------|------|-----------|
| `cape_jones_tooncrafter_colab.ipynb` | ToonCrafter cartoon interpolation (106f→211f @ 24fps) | `gen_tooncrafter_colab.py` |
| `cape_jones_viggle_colab.ipynb` | Viggle-Animate AI body replacement | `gen_viggle_colab.py` |
| `cape_jones_lighting_reel_colab.ipynb` | Lighting gag reel (Blender) | — (static) |

To regenerate: `python3 production/colab/gen_tooncrafter_colab.py`

### Colab vs Kaggle

| | Kaggle | Colab |
|---|---|---|
| GPU | T4 x2 (16GB) | T4 (16GB) |
| Free hours | 30h/week | ~4h/session (unreliable) |
| Model cache | Kaggle datasets (persistent) | Re-download each session (or Drive cache) |
| Output saving | `save_outputs.py` → dataset versions | `files.download()` — **download immediately** |
| Best for | Long runs, queue automation | Quick parallel runs |

### ⚠️ Colab gotchas

- **Sessions time out.** Download outputs via `files.download()` the moment they're
  ready. Don't rely on files persisting.
- **No dataset cache.** Model weights (~10GB ToonCrafter, ~25GB Viggle) download
  every session. Optional: uncomment the Drive-cache lines in the notebook to
  persist weights in Google Drive across sessions.
- **GPU not guaranteed.** Free tier may give you no GPU during peak. If
  `!nvidia-smi` shows nothing, try again later or use Kaggle.

---

## 2. Aider — AI Pair Programmer (Terminal)

Aider edits code in your git repo from natural language. Apache-2.0.

**Installed at:** `~/workspace/tools/aider-venv/bin/aider` (v0.86.2)

### Quick verify

```bash
~/workspace/tools/aider-venv/bin/aider --version
# → aider 0.86.2
```

### Usage

```bash
cd ~/workspace/cape-jones
~/workspace/tools/aider-venv/bin/aider
# then type: "add a --dry-run flag to finish.py"
```

The repo's `.aider.conf.yml` sets:
- Model: `gemini/gemini-2.0-flash` (free tier)
- Auto-commits: OFF (you review before committing)

### Connect a model

| Provider | Env var | Free? |
|----------|---------|-------|
| Google Gemini | `GEMINI_API_KEY` | ✅ Free tier at aistudio.google.com |
| Groq | `GROQ_API_KEY` | ✅ Free tier, very fast |
| Ollama (local) | — | ✅ Fully free, no key needed |

Get a Gemini key: https://aistudio.google.com → Get API key (free).
Then: `export GEMINI_API_KEY=your-key-here`

### Why Aider matters here

The owner is phone-only. Aider runs in the terminal on this VM, so agents
can use it for code edits without him needing a computer. It's the
"AI pair programmer" for the pipeline scripts.

**Note (2026-10-16 research):** OpenCode (189k stars, MIT) has overtaken Aider
(48k, slowing). Gemini CLI gives 1000 free req/day on just a Google login.
Both are documented in `docs/research/CLOUD-RESEARCH.md`. Aider stays as the
git-native option; evaluate OpenCode/Gemini CLI for future work.

---

## 3. Free IDEs — Browser-Based Development

The owner does everything from his phone. A browser IDE means he can view
(and eventually edit) code from the Android app.

### code-server (installed, recommended)

**What:** Full VS Code in the browser. MIT licensed. ~70k stars.

**Installed at:** `/usr/bin/code-server` (v4.141.0, verified 2026-10-16)

**Start it:**
```bash
/usr/bin/code-server --bind-addr 0.0.0.0:8080 ~/workspace/cape-jones
# Set a password on first run when prompted
```

**Access:** `http://<vm-ip>:8080` in any browser (including phone).

**As a service** (auto-start):
```bash
# Create systemd user service (run once)
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/code-server.service << 'EOF'
[Unit]
Description=code-server
After=network.target

[Service]
ExecStart=/usr/bin/code-server --bind-addr 127.0.0.1:8080 %h/workspace/cape-jones
Restart=always

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable --now code-server
```

### Alternatives (documented, not installed)

| Tool | License | Why not installed |
|------|---------|-------------------|
| OpenVSCode Server | MIT | Higher RAM (~500MB-1GB); code-server is lighter |
| Coder | AGPL-3.0 | 2-4 day setup; overkill for single-user |
| Gitpod/Ona | Proprietary | 3 parallel envs free; zero setup if needed later |
| GitHub Codespaces | Proprietary | 60h/month free; needs browser action to launch |

See `docs/research/CLOUD-RESEARCH.md` for the full ranked comparison.

---

## 4. GPU Landscape — Where Things Run

| Service | GPU | Free | Best for |
|---------|-----|------|----------|
| **Kaggle** | T4 x2 | 30h/week | Primary. Queue-automated. |
| **Colab** | T4 | ~4h/session | Backup/parallel. Unreliable for long runs. |
| Lightning AI | T4/A100/H100 | 15 credits/mo | Third GPU. Real terminal. A100 access. |

**Current pipeline routing:**
- ToonCrafter → Kaggle primary, Colab backup
- Viggle → Kaggle primary, Colab backup
- Blender renders → Kaggle (v4 pipeline)

---

## Quick Reference

```bash
# Colab notebooks
ls ~/workspace/cape-jones/production/colab/*.ipynb

# Regenerate Colab notebooks
python3 ~/workspace/cape-jones/production/colab/gen_tooncrafter_colab.py
python3 ~/workspace/cape-jones/production/colab/gen_viggle_colab.py

# Aider
~/workspace/tools/aider-venv/bin/aider --version
cd ~/workspace/cape-jones && ~/workspace/tools/aider-venv/bin/aider

# code-server
/usr/bin/code-server --version
/usr/bin/code-server --bind-addr 0.0.0.0:8080 ~/workspace/cape-jones
```

---

*Last updated: 2026-10-16. Research: `docs/research/CLOUD-RESEARCH.md`.*
