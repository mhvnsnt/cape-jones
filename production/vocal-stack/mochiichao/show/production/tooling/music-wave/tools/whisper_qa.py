#!/usr/bin/env python3
"""House Whisper QA seat (OpenAI Whisper, MIT — code and weights).

Usage: whisper_qa.py <in.wav> [--model base] [--expect "the script line"]

Transcribes, prints text, segment table, and mean no_speech_prob (the
hallucination gate: non-speech audio must score high no-speech and its
"text" must be discarded). With --expect, prints word error rate against
the expected line — the casting/TTS render check described in
TEARDOWN-whisper.md.
"""
import argparse
import re

import whisper


def wer(ref, hyp):
    r = re.findall(r"[a-z0-9']+", ref.lower())
    h = re.findall(r"[a-z0-9']+", hyp.lower())
    if not r:
        return float("nan")
    d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        d[i][0] = i
    for j in range(len(h) + 1):
        d[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                          d[i - 1][j - 1] + (r[i - 1] != h[j - 1]))
    return d[len(r)][len(h)] / len(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--model", default="base")
    ap.add_argument("--expect", default=None)
    a = ap.parse_args()
    model = whisper.load_model(a.model)
    res = model.transcribe(a.src)
    text = res["text"].strip()
    print(f"language={res['language']} segments={len(res['segments'])}")
    for s in res["segments"]:
        print(f"[{s['start']:6.2f}-{s['end']:6.2f}] "
              f"no_speech={s['no_speech_prob']:.3f} :: {s['text'].strip()}")
    if res["segments"]:
        mean_ns = sum(s["no_speech_prob"] for s in res["segments"]) / len(res["segments"])
        print(f"mean_no_speech_prob={mean_ns:.3f}")
    print(f"text: {text}")
    if a.expect:
        print(f"expected: {a.expect}")
        print(f"wer={wer(a.expect, text):.3f}")


if __name__ == "__main__":
    main()
