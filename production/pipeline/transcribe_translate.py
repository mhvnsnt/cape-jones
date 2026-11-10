#!/usr/bin/env python3
"""
transcribe_translate.py — Whisper-based transcription + translation pipeline.

1. Transcribes dialogue/audio to SRT with word-level timestamps (faster-whisper).
2. Translates the SRT into target languages using a LOCAL engine
   (Argos Translate — no API keys, works offline) or LibreTranslate (self-hosted).
3. Multi-language SRT manager: shift/scale timings, merge language tracks,
   split for dubbing cues.

Usage:
    pip install faster-whisper argostranslate srt
    python3 transcribe_translate.py EP01_dialogue.wav --source en --targets es fr
    python3 transcribe_translate.py EP01_dialogue.wav --targets es --shift +0.5
    python3 transcribe_translate.py EP01.en.srt --targets es fr --no-transcribe

Output: EP01.en.srt, EP01.es.srt, EP01.fr.srt (+ .vtt copies if --vtt).
"""
import argparse
import os
import sys

try:
    import srt
except ImportError:
    sys.exit("pip install srt")


def transcribe(audio, source_lang, model="large-v3", device="auto"):
    from faster_whisper import WhisperModel
    compute = "int8" if device in ("auto", "cpu") else "float16"
    print(f"[whisper] loading {model} on {device} ...")
    model_obj = WhisperModel(model, device=device, compute_type=compute)
    segments, info = model_obj.transcribe(audio, language=source_lang,
                                          word_timestamps=True, vad_filter=True)
    subs = []
    for i, seg in enumerate(segments, 1):
        from datetime import timedelta
        subs.append(srt.Subtitle(
            index=i,
            start=timedelta(seconds=seg.start),
            end=timedelta(seconds=seg.end),
            content=seg.text.strip()))
    print(f"[whisper] detected language {info.language} "
          f"({info.language_probability:.0%}), {len(subs)} cues")
    return subs


def translate_subs(subs, src, dst, engine="argos"):
    if engine == "argos":
        try:
            import argostranslate.package, argostranslate.translate
        except ImportError:
            sys.exit(
                "[argos] argostranslate not installed in this venv.\n"
                "  Install it (needs ~1GB for the stanza+torch stack, CPU-only is fine):\n"
                "    venv/bin/pip install --index-url https://download.pytorch.org/whl/cpu torch\n"
                "    venv/bin/pip install argostranslate\n"
                "  Or use --engine libre with a self-hosted LibreTranslate server instead."
            )
        installed = [str(p) for p in argostranslate.translate.get_installed_languages()]
        argostranslate.package.update_package_index()
        avail = argostranslate.package.get_available_packages()
        pkg = next((p for p in avail if p.from_code == src and p.to_code == dst), None)
        if pkg is None:
            sys.exit(f"[argos] no package {src}->{dst}. "
                     f"Install with: argospm install translate-{src}_{dst}")
        argostranslate.package.install_from_path(pkg.download())
        out = []
        for s in subs:
            s2 = srt.Subtitle(index=s.index, start=s.start, end=s.end,
                              content=argostranslate.translate.translate(s.content, src, dst))
            out.append(s2)
        return out
    elif engine == "libre":
        import requests
        url = os.environ.get("LIBRETRANSLATE_URL", "http://localhost:5000")
        out = []
        for s in subs:
            r = requests.post(f"{url}/translate",
                              data={"q": s.content, "source": src, "target": dst,
                                    "format": "text"}, timeout=60)
            r.raise_for_status()
            text = r.json()["translatedText"]
            out.append(srt.Subtitle(index=s.index, start=s.start, end=s.end, content=text))
        return out
    else:
        sys.exit(f"unknown engine {engine}")


def shift_subs(subs, seconds):
    from datetime import timedelta
    delta = timedelta(seconds=seconds)
    for s in subs:
        s.start += delta
        s.end += delta
    return subs


def scale_subs(subs, factor):
    from datetime import timedelta
    for s in subs:
        s.start = timedelta(seconds=s.start.total_seconds() * factor)
        s.end = timedelta(seconds=s.end.total_seconds() * factor)
    return subs


def to_vtt(path):
    with open(path) as f:
        subs = list(srt.parse(f.read()))
    lines = ["WEBVTT", ""]
    for s in subs:
        fmt = lambda td: (f"{int(td.total_seconds()//3600):02d}:"
                          f"{int(td.total_seconds()%3600//60):02d}:"
                          f"{int(td.total_seconds()%60):02d}."
                          f"{int(td.microseconds//1000):03d}")
        lines += [f"{fmt(s.start)} --> {fmt(s.end)}", s.content, ""]
    vtt = path.rsplit(".", 1)[0] + ".vtt"
    with open(vtt, "w") as f:
        f.write("\n".join(lines))
    return vtt


def main():
    ap = argparse.ArgumentParser(description="Transcribe + translate dialogue to multi-language SRTs.")
    ap.add_argument("input", help="Audio file (transcribes) or .srt (skips transcription)")
    ap.add_argument("--source", default="en", help="Source language code")
    ap.add_argument("--targets", nargs="+", default=["es"], help="Target language codes")
    ap.add_argument("--engine", default="argos", choices=["argos", "libre"],
                    help="argos = local offline; libre = self-hosted LibreTranslate server")
    ap.add_argument("--model", default="large-v3", help="faster-whisper model")
    ap.add_argument("--device", default="auto")
    ap.add_argument("--no-transcribe", action="store_true")
    ap.add_argument("--shift", type=float, default=0.0, help="Shift all cues by N seconds")
    ap.add_argument("--scale", type=float, default=1.0, help="Scale all timings by factor")
    ap.add_argument("--vtt", action="store_true", help="Also write .vtt copies")
    args = ap.parse_args()

    stem = os.path.splitext(args.input)[0]
    if args.input.endswith(".srt") or args.no_transcribe:
        with open(args.input) as f:
            subs = list(srt.parse(f.read()))
        print(f"[srt] loaded {len(subs)} cues from {args.input}")
    else:
        subs = transcribe(args.input, args.source, args.model, args.device)

    if args.shift:
        subs = shift_subs(subs, args.shift)
    if args.scale != 1.0:
        subs = scale_subs(subs, args.scale)

    src_path = f"{stem}.{args.source}.srt"
    with open(src_path, "w") as f:
        f.write(srt.compose(subs))
    print(f"[srt] wrote {src_path}")
    made = [src_path]
    if args.vtt:
        made.append(to_vtt(src_path))

    for lang in args.targets:
        if lang == args.source:
            continue
        print(f"[translate] {args.source} -> {lang} via {args.engine} ...")
        tsubs = translate_subs(subs, args.source, lang, args.engine)
        path = f"{stem}.{lang}.srt"
        with open(path, "w") as f:
            f.write(srt.compose(tsubs))
        print(f"[srt] wrote {path} ({len(tsubs)} cues)")
        made.append(path)
        if args.vtt:
            made.append(to_vtt(path))

    print("DONE:", ", ".join(made))


if __name__ == "__main__":
    main()
