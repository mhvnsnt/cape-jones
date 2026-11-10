# QLoRA fine-tuning on a T4 (Colab / Kaggle) — runbook

**Primary: Unsloth** (Apache-2.0) — 2–5x faster than stock transformers on consumer GPUs,
~half the VRAM. **Reproducible: Axolotl** (Apache-2.0) YAML configs. Reference numbers
(2026): Llama-3 8B QLoRA r=16 on 50k examples ≈ 12h on a T4; gpt-oss-20b QLoRA ≈ 14GB VRAM;
Qwen3-30B-A3B MoE QLoRA workable via Unsloth's split-LoRA formulation.

## 1. Unsloth on a free Colab T4

Runtime → Change runtime type → **T4 GPU**.

```python
# install
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps xformers trl peft accelerate bitsandbytes
```

```python
from unsloth import FastLanguageModel
import torch

MAX_SEQ = 2048  # raise to 4096 on 8B if it fits; watch nvidia-smi
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-8B-bnb-4bit",   # 4-bit base; swap for your model
    max_seq_length=MAX_SEQ,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,                       # 64 to close the last quality gap (costs VRAM)
    target_modules=["q_proj","k_proj","v_proj","o_proj",
                    "gate_proj","up_proj","down_proj"],
    lora_alpha=16,
    lora_dropout=0,             # 0 = the Unsloth-recommended stable setting
    bias="none",
    use_gradient_checkpointing="unsloth",
)

from trl import SFTTrainer
from transformers import TrainingArguments

trainer = SFTTrainer(
    model=model, tokenizer=tokenizer,
    train_dataset=dataset,      # your HF dataset: {"text": ...} or chat format
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        max_steps=300,          # scale to your data; ~1-3 epochs typical
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),  # T4: False -> fp16 path
        optim="adamw_8bit",
        logging_steps=10,
        output_dir="qlora-out",
    ),
)
trainer.train()
model.save_pretrained("lora-adapter")   # 10-100MB — commit THIS to the repo
```

Merge/export for serving:
```python
model.save_pretrained_merged("merged-16bit", tokenizer, save_method="merged_16bit")
# then quantize to GGUF with llama.cpp for llama-server/Ollama deployment
```

## 2. Axolotl (reproducible pipeline runs)

```yaml
# axolotl-qwen3-8b-qlora.yml
base_model: unsloth/Qwen3-8B-bnb-4bit
load_in_4bit: true
adapter: qlora
lora_r: 16
lora_alpha: 16
lora_dropout: 0.0
sequence_len: 2048
sample_packing: true
gradient_accumulation_steps: 4
micro_batch_size: 2
num_epochs: 2
learning_rate: 0.0002
optimizer: adamw_bnb_8bit
datasets:
  - path: <your-dataset>
    type: chat_template
output_dir: ./qlora-out
```
```bash
axolotl train axolotl-qwen3-8b-qlora.yml
```

## 3. FLUX art-style LoRA on the Kaggle T4 — Ostris ai-toolkit (MIT)

```bash
git clone --filter=blob:none https://github.com/ostris/ai-toolkit.git
cd ai-toolkit && git submodule update --init --recursive
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```
Use the `config/examples/train_lora_flux_24gb.yaml` example as a base, then set the
low-VRAM options the toolkit documents for 16GB: `quantize: true` on the base model,
`gradient_checkpointing: true`, `optimizer: adamw8bit`, sample resolution 512–768,
`batch_size: 1`. 20–50 style images is enough for a character/show style LoRA.
Output is a `.safetensors` LoRA (tens of MB) — drops into ComfyUI's `models/loras/`
and works with the GGUF FLUX workflow via a standard `LoraLoader` node.

## 4. Character voice models (RVC) on T4

RVC training needs ~10min of clean, single-speaker audio per character and a T4 is
plenty. Train per-character RVC v2 models on Kaggle, export the `.pth`, and serve
alongside the Chatterbox TTS already in our pipeline (see TRACK-B-AUDIO-PULL.md):
TTS generates the line → RVC converts timbre to the character voice.
Keep datasets and trained weights on TeraBox/GitHub releases (they're small);
never commit raw voice audio of real people without consent.

## 5. T4 VRAM cheat-sheet

| Job | Fits? | Notes |
|---|---|---|
| 8B QLoRA r=16, 2k ctx | yes, comfortable | the default fine-tune |
| 8B QLoRA r=64, 4k ctx | yes, tight | monitor nvidia-smi |
| gpt-oss-20b QLoRA | yes (~14GB) | per Unsloth's guide |
| 30B-A3B MoE QLoRA | yes | needs Unsloth MoE build or Axolotl `quantize_moe_experts` |
| 70B QLoRA | no | needs 2x T4 / bigger card |
| FLUX LoRA (ai-toolkit) | yes | quantized base + 8bit optimizer |
| RVC v2 voice | yes | batch size 4–8 typical |
