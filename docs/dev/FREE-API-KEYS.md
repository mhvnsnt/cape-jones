# FREE-API-KEYS — free-tier API keys for the Cape Jones lanes

**Researched:** 2026-10-16. **Method:** every free-tier number below was checked
against a live 2026 source (provider docs, rate-limit pages, or a free-API
directory re-verified in the last ~2 weeks). Sources are linked per row. Limits
change — re-verify against the provider's own page before building on them.

**Hard rules (owner laws, not suggestions):**
- Free tiers ONLY. No spending, no credit cards. If a service asks for a card, STOP and report — do not pay.
- Keys go through the **secure vault flow ONLY**. NEVER in chat, files, logs, code, or commits.
- Env audit (this VM): 2026-10-16 — **every key below was MISSING**. 2026-10-17 —
  **four keys are now LIVE** in `~/.config/cape-jones/api-keys.env` (chmod 600,
  gitignored, values never in repo/chat/logs): `GEMINI_API_KEY` ✅ (verified via
  Gemini models list; hit free-tier `quota exceeded` after a few calls),
  `MISTRAL_API_KEY` ✅ (200 on api.mistral.ai/v1/models),
  `OPENROUTER_API_KEY` ✅ (200 on /v1/models; free `:free` models respond),
  `HF_TOKEN` ✅ (whoami-v2: user Dmn52, token "Bannon agents"). **Still missing:
  `GROQ_API_KEY`** — not in the file as of 2026-10-17; needs the key re-delivered.
  (Presence only — values are never printed.)
- The repo's stored `custom.legacy-gemini` connector is a **surrogate-only**
  credential for one-turn image edits — it is NOT retrievable as a raw API key
  and cannot feed aider/Cline (established in `docs/dev/AIDER.md`).
- Related prior research (do NOT redo): `docs/research/FREE-3D-TOOLS.md` —
  Meshy free (100 credits/mo, ~3–5 textured models, CC BY 4.0, attribution
  required — non-commercial), Tripo Studio free (200 credits/mo but **public
  + non-commercial — BLOCKED for shipped work**), self-hosted TripoSR
  (winner, MIT, unlimited, no signup). Pollinations anonymous tier (no key).

## Master table

| Service | Free tier (numbers, as of 2026-10-16) | Signup URL | OAuth options | Env var | Status |
|---|---|---|---|---|---|
| Google AI Studio (Gemini API) | **Flash-family free:** per-model limits shown in AI Studio (Google stopped publishing tables mid-2026). Reported: Flash 10–15 RPM, ~250K TPM, 250–1,500 RPD; Pro models effectively paid. **Free-tier prompts may train Google models.** No card. [src](https://dev.to/unicodefawn/free-llm-api-tiers-in-2026-the-actual-rate-limits-and-why-they-keep-changing-32d6) | https://aistudio.google.com/apikey | Google (only) | `GEMINI_API_KEY` (aider also accepts `GOOGLE_API_KEY`) | NEED-BROWSER |
| Groq | **30 RPM, 1,000 RPD, 8K TPM, 200K TPD** per model on `openai/gpt-oss-120b`, `gpt-oss-20b`, `qwen/qwen3.8-27b` (limits are per-org, not per-key). Whisper: 20 RPM / 2,000 RPD / 7,200 audio-sec/hr. No card. No training use. **Best free fallback for coding agents.** [src](https://klymentiev.com/blog/groq-pricing) | https://console.groq.com/keys | Google or GitHub | `GROQ_API_KEY` | NEED-BROWSER |
| OpenRouter | **`:free` models: 20 RPM, 50 RPD** (rises to 1,000 RPD only after $10 lifetime credit purchase — **do not buy**). 25+ free models, OpenAI-compatible. Provider may log prompts. No card. [src](https://openrouter.ai/docs/api-reference/limits) | https://openrouter.ai/settings/keys | GitHub or Google | `OPENROUTER_API_KEY` | NEED-BROWSER |
| Mistral (La Plateforme) | **Free Experiment tier:** ~1 req/sec, 500K TPM, up to ~1B tokens/month per model incl. Codestral. **Phone verification required. Free tier is NON-commercial and trains on your data (opt-out in console).** No card. [src](https://cabina.ai/blog/mistral-api-pricing/) | https://console.mistral.ai/api-keys | email + phone | `MISTRAL_API_KEY` | NEED-BROWSER (+ phone) |
| Hugging Face | Free users: **$0.10/month Inference Providers credits** (rate-limit free tier retired in 2026). Token needed for private repos + routed inference. Fine-grained token scope must include **"Make calls to Inference Providers"**. No card. [src](https://github.com/IdoY12/awesome-free-ai-apis/blob/HEAD/docs/providers/huggingface-inference-providers-image.md) | https://huggingface.co/settings/tokens | GitHub or Google | `HF_TOKEN` (fallback `HUGGINGFACE_HUB_TOKEN`) | NEED-BROWSER |
| Pollinations | Anonymous tier, **no key, no signup** — already wired in prior lanes. | n/a | n/a | none | HAVE (no key) |
| Cohere | Trial key: **1,000 calls/month, 20 RPM, non-commercial**, eval use. No card. | https://dashboard.cohere.com/api-keys | email or Google | `COHERE_API_KEY` | NEED-BROWSER (low priority) |
| NVIDIA NIM | Phone verification, **up to 40 RPM, no published RPD**, prototyping-only, no card. Models: Nemotron, Kimi, DeepSeek, Llama. | https://build.nvidia.com | NVIDIA account | `NVIDIA_API_KEY` | NEED-BROWSER (low priority) |
| Z.ai (GLM Flash) | GLM-4.5/4.6/4.7-Flash free, ~1 req/sec, ~1,000 RPD. No card, registration only. | https://z.ai/manage-apikey/apikey-list | Google or GitHub | `ZAI_API_KEY` | NEED-BROWSER (low priority) |
| Replicate | **Free limited runs on public models without card; beyond that = card + pay-per-second.** No permanent free tier. (Acquired by Cloudflare.) | https://replicate.com | GitHub | `REPLICATE_API_TOKEN` | NEED-BROWSER (free-runs only) |
| fal.ai | **No permanent free tier.** ~$10 one-time dev credits on signup; pay-per-use after. No published card requirement. | https://fal.ai | GitHub or Google | `FAL_KEY` | NEED-BROWSER (credits run out) |
| DeepInfra | ❌ **BLOCKED — card required.** Official pricing: "you have to add a card or pre-pay or you won't be able to use our services." [src](https://www.apipod.ai/alternatives/deepinfra) | — | — | `DEEPINFRA_API_TOKEN` | blocked-no-card |
| Cerebras | ❌ **BLOCKED — card required.** Trial is $5 one-time credit behind a verified payment method, expiring 30 days; no permanent free tier since 2026-08. [src](https://mvalentsev.github.io/awesome-free-ai-coding/providers/cerebras-free/) | — | — | `CEREBRAS_API_KEY` | blocked-no-card |
| OpenAI / Anthropic | ❌ No permanent free API tier (trial credits only, card needed). | — | — | `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` | blocked-no-free-tier |

## Which keys feed which tools

| Tool | Keys it reads (env vars, verified 2026-10-16) |
|---|---|
| Aider | `GEMINI_API_KEY` (default model in `.aider.conf.yml` is `gemini-exp`, free with usage limits), `OPENROUTER_API_KEY`, `GROQ_API_KEY`, `MISTRAL_API_KEY`, `DEEPINFRA_API_TOKEN`, `GOOGLE_API_KEY`, or `--api-key <provider>=<key>`. Also supports a `.env` file (env vars override). |
| Cline (VS Code ext) | Reads `OPENROUTER_API_KEY` natively; per-provider keys in extension settings (Gemini: AI Studio key; Mistral: La Plateforme key). |
| OpenRouter CLI/HTTP | `OPENROUTER_API_KEY` + `Authorization: Bearer` on `https://openrouter.ai/api/v1`. |
| HF inference (TripoSR/TRELLIS pulls) | `HF_TOKEN` — public models work without a key; a token with the right scope raises quotas and unlocks private repos. |

## Key request list (for the parent browser lane)

**Sign-in fallback law:** Google first (`fmmg.mars@gmail.com`), then GitHub OAuth (`mhvnsnt`).
Each key is created in the live browser; the VALUE goes through the secure
vault flow only and lands as the named env var. Never paste it into chat.

1. **AI Studio** → https://aistudio.google.com/apikey → "Get API key" →
   Google sign-in (fmmg.mars@gmail.com) → copy key → store via vault as
   **`GEMINI_API_KEY`**. *(Unblocks aider default + Cline. Highest value.)*
2. **Groq** → https://console.groq.com/keys → Google or GitHub OAuth →
   create key → store as **`GROQ_API_KEY`**. *(Best free coding-agent fallback.)*
3. **OpenRouter** → https://openrouter.ai/settings/keys → GitHub or Google
   OAuth → create key → store as **`OPENROUTER_API_KEY`**. *(50 free req/day —
   light use only; **do not buy the $10 credit** to raise the cap.)*
4. **Mistral** → https://console.mistral.ai/api-keys → email signup +
   **phone verification** (owner's phone) → create key → store as
   **`MISTRAL_API_KEY`**. *(Codestral for code; free tier is non-commercial.)*
5. **Hugging Face** → https://huggingface.co/settings/tokens → Google or
   GitHub OAuth → new fine-grained token with **"Make calls to Inference
   Providers"** scope → store as **`HF_TOKEN`**.
6. (optional) **Replicate** → https://replicate.com → GitHub OAuth →
   token → **`REPLICATE_API_TOKEN`** — free test runs only, no card.
7. (optional) **fal.ai** → https://fal.ai → GitHub or Google OAuth →
   key → **`FAL_KEY`** — one-time $10 credit; expires when spent.

**Blocked, do not attempt:** Cerebras and DeepInfra (card required),
OpenAI/Anthropic (no free API tier), OpenRouter credit purchase (spending).

## Post-vault wiring (no values anywhere)

Once each key is in the vault and exported in the agent env:

```bash
# verify WITHOUT printing values (presence only)
for v in GEMINI_API_KEY GROQ_API_KEY OPENROUTER_API_KEY MISTRAL_API_KEY HF_TOKEN; do
  [ -n "${!v}" ] && echo "$v: PRESENT" || echo "$v: MISSING"
done

# aider smoke tests (one tiny call each, then check the diff)
aider --model gemini-exp --message "reply with the single word ok" --yes-always
aider --model openrouter/deepseek/deepseek-chat --message "reply with the single word ok" --yes-always

# OpenRouter raw HTTP check (prints only status, not the key)
curl -s -o /dev/null -w "%{http_code}" https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"

# HF scope check (token permission lives under "Permissions")
curl -s https://huggingface.co/api/whoami -H "Authorization: Bearer $HF_TOKEN" | grep -o '"auth":[^,]*'
```

## Changelog

- 2026-10-17 — Lane `docs/wireup-ai-agents-20261017`: keys live —
  GEMINI/MISTRAL/OPENROUTER/HF wired into `~/.config/cape-jones/api-keys.env`;
  aider LIVE (real edit via `gemini/gemini-3-flash-preview`; note `gemini-exp`
  alias is dead — 404, use explicit model); Cline LIVE (real response via
  OpenRouter `cohere/north-mini-code:free`); Copilot CLI 1.0.98 installed but
  BLOCKED (prior PAT auth expired; stored gh PAT lacks Copilot Requests scope —
  needs owner `copilot login` device flow). GROQ_API_KEY still missing from
  the key file. Docs updated: AIDER.md, CLINE.md.
- 2026-10-16 — Lane `setup/free-api-keys-20261016`: full env audit (all keys
  MISSING on this VM), 2026-source free-tier research for Gemini/Groq/OpenRouter/
  Mistral/HF/DeepInfra/Cerebras/Replicate/fal.ai, plus key request list for the
  parent browser lane. Headless key creation was NOT possible for any service —
  every provider needs browser OAuth signup, so nothing was wired up locally.
