#!/usr/bin/env bash
# kaggle-llm-server.sh — serve an LLM on a Kaggle T4 via llama.cpp (MIT).
#
# Usage (inside a Kaggle notebook cell or terminal):
#   bash kaggle-llm-server.sh [GGUF_URL] [PORT]
#
# Defaults: Qwen3.5-class 30B-A3B MoE IQ3_XXS (fits 16GB VRAM with context headroom).
# Override GGUF_URL to serve any other GGUF.
#
# What it does:
#   1. Downloads the prebuilt llama.cpp CUDA binary (release b11696, no compile needed)
#   2. Downloads the GGUF weights (resumable)
#   3. Starts llama-server with an OpenAI-compatible API on $PORT
#
# Test it:
#   curl http://localhost:8080/v1/chat/completions \
#     -H 'Content-Type: application/json' \
#     -d '{"model":"t4-llm","messages":[{"role":"user","content":"Say hi"}],"max_tokens":32}'
#
# Our pipelines talk to it via tools/inference/inference_client.py (no extra deps).
set -euo pipefail

LLAMA_TAG="${LLAMA_TAG:-b11696}"
LLAMA_URL="https://github.com/ggml-org/llama.cpp/releases/download/${LLAMA_TAG}/llama-${LLAMA_TAG}-bin-ubuntu-cuda-12.8-x64.tar.gz"
# Default model: change to any GGUF you prefer. Verified Oct 2026.
GGUF_URL="${1:-https://huggingface.co/unsloth/Qwen3-30B-A3B-GGUF/resolve/main/Qwen3-30B-A3B-UD-IQ3_XXS.gguf}"
PORT="${2:-8080}"
WORKDIR="${WORKDIR:-$HOME/t4-llm}"

mkdir -p "$WORKDIR"
cd "$WORKDIR"

if [ ! -x "$WORKDIR/llama-server" ]; then
  echo "[t4-llm] fetching llama.cpp ${LLAMA_TAG} (CUDA 12.8)..."
  curl -sL --retry 3 -o llama.tgz "$LLAMA_URL"
  tar xzf llama.tgz
  chmod +x "$WORKDIR"/llama-*
fi

GGUF_FILE="$WORKDIR/$(basename "$GGUF_URL")"
if [ ! -f "$GGUF_FILE" ]; then
  echo "[t4-llm] fetching model (resumable)..."
  curl -sL --retry 3 -C - -o "$GGUF_FILE" "$GGUF_URL"
fi

echo "[t4-llm] serving $GGUF_FILE on :$PORT"
exec "$WORKDIR/llama-server" \
  -m "$GGUF_FILE" \
  --host 0.0.0.0 --port "$PORT" \
  -ngl 999 \
  -c 32768 \
  --cont-batching \
  --metrics
