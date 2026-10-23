# Aider — AI pair programmer for the terminal

Aider (https://aider.chat) is an open-source CLI tool that edits code in your
git repo based on natural language instructions. Apache 2.0 licensed.

## Install

```bash
pip install aider-chat
# or: python -m pip install aider-install && aider-install
```

## Connect a model (pick one — set as env var)

| Provider | Env var | Free option |
|----------|---------|-------------|
| Google Gemini | `GEMINI_API_KEY` | Free tier available at aistudio.google.com |
| Groq | `GROQ_API_KEY` | Free tier, very fast inference |
| OpenAI | `OPENAI_API_KEY` | Paid |
| Anthropic | `ANTHROPIC_API_KEY` | Paid |
| Ollama (local) | — | Fully free, runs on your machine |

The bundled `.aider.conf.yml` defaults to `gemini/gemini-2.0-flash`
(free tier) with auto-commits OFF.

## Usage

```bash
cd ~/workspace/cape-jones-build/cape-jones
aider                    # uses .aider.conf.yml in this dir
# then type: "add a --dry-run flag to finish.py"
```

Copy `.aider.conf.yml` into any repo root to use the shared config.

## Why this matters for the owner

He does everything from his phone. Aider runs in the terminal on this VM,
so the agents can use it for code edits without him needing a computer.
