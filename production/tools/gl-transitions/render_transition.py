#!/usr/bin/env python3
"""Render a gl-transitions GLSL transition between two images to MP4, headless.

Uses headless Chromium (Playwright, SwiftShader WebGL) to render each frame
of a transition from the vendored ``transitions/*.glsl`` collection, then
encodes the frames to H.264 MP4 with ffmpeg.

Examples:
  render_transition.py --list
  render_transition.py --from a.png --to b.png --transition fade --out fade.mp4
  render_transition.py --from a.png --to b.png --transition undulatingBurnOut \\
      --duration 2.0 --fps 24 --width 1280 --height 720 --out burn.mp4

Transition parameters: each .glsl file declares its own uniforms with
defaults in trailing comments (e.g. ``uniform float strength; // = 0.5``).
Defaults are applied automatically; override any of them with
``--param name=value`` (repeatable).

Requires: playwright + a Chromium build (``pip install playwright`` then
``playwright install chromium``), ffmpeg with libx264.
"""

import argparse
import functools
import http.server
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
TRANSITIONS_DIR = os.path.join(HERE, "transitions")

UNIFORM_RE = re.compile(
    r"^\s*uniform\s+(\w+)\s+(\w+)\s*;(?:\s*//\s*=\s*(.+?)\s*)?$"
)
STD_UNIFORMS = {"from", "to", "progress", "ratio"}


def list_transitions():
    names = sorted(
        f[:-5] for f in os.listdir(TRANSITIONS_DIR) if f.endswith(".glsl")
    )
    return names


def parse_transition(name):
    """Split a .glsl transition into custom uniforms and the shader body."""
    path = os.path.join(TRANSITIONS_DIR, name + ".glsl")
    if not os.path.isfile(path):
        raise SystemExit(
            f"unknown transition {name!r} (see --list); file not found: {path}"
        )
    uniforms = {}  # name -> (type, default_str_or_None)
    body_lines = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            m = UNIFORM_RE.match(line)
            if m:
                utype, uname, default = m.group(1), m.group(2), m.group(3)
                if uname not in STD_UNIFORMS:
                    uniforms[uname] = (utype, default)
                continue
            body_lines.append(line)
    return uniforms, "".join(body_lines)


def _parse_vec(value, n):
    value = value.strip()
    m = re.match(r"vec\d\s*\((.+)\)", value)
    inner = m.group(1) if m else value
    parts = [float(p.strip()) for p in inner.split(",")]
    if len(parts) == 1:
        parts = parts * n
    if len(parts) != n:
        raise ValueError(f"cannot parse {value!r} as vec{n}")
    return parts


def coerce_value(utype, raw):
    raw = raw.strip()
    if utype == "float":
        return float(raw)
    if utype == "int":
        return int(float(raw))
    if utype == "bool":
        return 1 if raw.lower() in ("true", "1") else 0
    if utype == "vec2":
        return _parse_vec(raw, 2)
    if utype == "vec3":
        return _parse_vec(raw, 3)
    if utype == "vec4":
        return _parse_vec(raw, 4)
    if utype == "sampler2D":
        return None  # bound to the generated extra texture
    raise ValueError(f"unsupported uniform type {utype!r}")


VERT_SRC = """
attribute vec2 a_pos;
void main(){ gl_Position = vec4(a_pos, 0.0, 1.0); }
"""


def build_frag_src(body, uniforms, width, height):
    decls = []
    for uname, (utype, _default) in uniforms.items():
        decls.append(f"uniform {utype} {uname};")
    uniform_block = "\n".join(decls)
    return (
        "precision mediump float;\n"
        "uniform sampler2D from;\n"
        "uniform sampler2D to;\n"
        "uniform float progress;\n"
        "uniform float ratio;\n"
        + uniform_block
        + "\n"
        "vec4 getFromColor(vec2 uv){ return texture2D(from, uv); }\n"
        "vec4 getToColor(vec2 uv){ return texture2D(to, uv); }\n"
        + body
        + "\nvoid main(){\n"
        f"  vec2 uv = gl_FragCoord.xy / vec2({width}.0, {height}.0);\n"
        "  gl_FragColor = transition(uv);\n"
        "}\n"
    )


PAGE_TMPL = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
html,body{margin:0;padding:0;background:#000;overflow:hidden}
canvas{display:block;width:__W__px;height:__H__px}
#error{color:#f66;font-family:monospace;white-space:pre-wrap;padding:20px}
</style></head>
<body>
<canvas id="c" width="__W__" height="__H__"></canvas>
<div id="error"></div>
<script>
"use strict";
const W = __W__, H = __H__;
const VERT_SRC = __VERT__;
const FRAG_SRC = __FRAG__;
const UNIFORMS = __UNIFORMS__;
const FROM_URL = __FROM_URL__;
const TO_URL = __TO_URL__;
const EXTRA_SAMPLERS = __EXTRA__;

function fail(msg){
  document.getElementById('error').textContent = 'RENDER_ERROR: ' + msg;
  window.__error = msg;
}

function compile(gl, type, src){
  const sh = gl.createShader(type);
  gl.shaderSource(sh, src);
  gl.compileShader(sh);
  if(!gl.getShaderParameter(sh, gl.COMPILE_STATUS)){
    fail('shader compile: ' + gl.getShaderInfoLog(sh));
    return null;
  }
  return sh;
}

function makeNoiseTexture(gl){
  // Deterministic SMOOTH pseudo-random RGBA texture for transitions that need
  // an extra sampler (e.g. displacementMap, luma). White noise would shred
  // the image; instead we stamp small random noise and upscale with bilinear
  // filtering so the map has smooth blobs (proper wipe/displacement fields).
  const S = 256, N = 32;
  let seed = 123456789;
  const rnd = () => (seed = (seed*1103515245 + 12345) & 0x7fffffff) / 0x7fffffff;
  const small = document.createElement('canvas');
  small.width = N; small.height = N;
  const sctx = small.getContext('2d');
  const img = sctx.createImageData(N, N);
  for(let i=0;i<img.data.length;i++) img.data[i] = Math.floor(rnd()*256);
  sctx.putImageData(img, 0, 0);
  const big = document.createElement('canvas');
  big.width = S; big.height = S;
  const bctx = big.getContext('2d');
  bctx.imageSmoothingEnabled = true;
  bctx.drawImage(small, 0, 0, S, S);
  const tex = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, tex);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, big);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);
  return tex;
}

function loadImage(url){
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error('load failed: ' + url));
    img.src = url;
  });
}

function uploadImage(gl, img){
  const tex = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, tex);
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  return tex;
}

let gl = null, prog = null, locs = {}, texFrom = null, texTo = null, texExtra = null;

async function init(){
  const canvas = document.getElementById('c');
  gl = canvas.getContext('webgl', {preserveDrawingBuffer: true, antialias: false});
  if(!gl){ fail('WebGL unavailable'); return; }
  const vs = compile(gl, gl.VERTEX_SHADER, VERT_SRC);
  const fs = compile(gl, gl.FRAGMENT_SHADER, FRAG_SRC);
  if(!vs || !fs) return;
  prog = gl.createProgram();
  gl.attachShader(prog, vs);
  gl.attachShader(prog, fs);
  gl.linkProgram(prog);
  if(!gl.getProgramParameter(prog, gl.LINK_STATUS)){
    fail('program link: ' + gl.getProgramInfoLog(prog)); return;
  }
  gl.useProgram(prog);
  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 3,-1, -1,3]), gl.STATIC_DRAW);
  const aPos = gl.getAttribLocation(prog, 'a_pos');
  gl.enableVertexAttribArray(aPos);
  gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

  for(const name of Object.keys(UNIFORMS)){
    locs[name] = gl.getUniformLocation(prog, name);
  }
  locs['from'] = gl.getUniformLocation(prog, 'from');
  locs['to'] = gl.getUniformLocation(prog, 'to');
  locs['progress'] = gl.getUniformLocation(prog, 'progress');
  locs['ratio'] = gl.getUniformLocation(prog, 'ratio');
  for(const name of EXTRA_SAMPLERS){
    locs[name] = gl.getUniformLocation(prog, name);
  }

  try{
    const [fromImg, toImg] = await Promise.all([loadImage(FROM_URL), loadImage(TO_URL)]);
    texFrom = uploadImage(gl, fromImg);
    texTo = uploadImage(gl, toImg);
    texExtra = makeNoiseTexture(gl);
  }catch(e){ fail(e.message); return; }

  gl.uniform1f(locs['ratio'], W / H);
  // Custom uniforms (defaults from the .glsl header, overridable via --param).
  for(const [name, spec] of Object.entries(UNIFORMS)){
    const loc = locs[name];
    if(loc === null) continue;
    const v = spec.value;
    if(spec.type === 'float') gl.uniform1f(loc, v);
    else if(spec.type === 'int' || spec.type === 'bool') gl.uniform1i(loc, v);
    else if(spec.type === 'vec2') gl.uniform2f(loc, v[0], v[1]);
    else if(spec.type === 'vec3') gl.uniform3f(loc, v[0], v[1], v[2]);
    else if(spec.type === 'vec4') gl.uniform4f(loc, v[0], v[1], v[2], v[3]);
  }
  window.__ready = true;
}

function setProgress(p){
  gl.activeTexture(gl.TEXTURE0);
  gl.bindTexture(gl.TEXTURE_2D, texFrom);
  gl.uniform1i(locs['from'], 0);
  gl.activeTexture(gl.TEXTURE1);
  gl.bindTexture(gl.TEXTURE_2D, texTo);
  gl.uniform1i(locs['to'], 1);
  EXTRA_SAMPLERS.forEach((name, i) => {
    gl.activeTexture(gl.TEXTURE2 + i);
    gl.bindTexture(gl.TEXTURE_2D, texExtra);
    gl.uniform1i(locs[name], 2 + i);
  });
  gl.uniform1f(locs['progress'], p);
  gl.viewport(0, 0, W, H);
  gl.drawArrays(gl.TRIANGLES, 0, 3);
  return p;
}
window.setProgress = setProgress;
init();
</script>
</body></html>
"""


def js_escape(s):
    return s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")


def render_frames(transition, uniforms, width, height, nframes, from_path, to_path, frames_dir):
    from playwright.sync_api import sync_playwright

    extra_samplers = [
        n for n, (t, _d) in uniforms.items() if t == "sampler2D"
    ]
    js_uniforms = {}
    for uname, (utype, _default) in uniforms.items():
        if utype == "sampler2D":
            continue
        js_uniforms[uname] = {"type": utype, "value": coerce_value(utype, _default)}

    frag_src = build_frag_src(
        js_escape(parse_transition(transition)[1]), uniforms, width, height
    )
    page_html = (
        PAGE_TMPL.replace("__W__", str(width))
        .replace("__H__", str(height))
        .replace("__VERT__", "`" + js_escape(VERT_SRC) + "`")
        .replace("__FRAG__", "`" + frag_src + "`")
        .replace("__UNIFORMS__", json.dumps(js_uniforms))
        .replace("__FROM_URL__", json.dumps("from" + os.path.splitext(from_path)[1]))
        .replace("__TO_URL__", json.dumps("to" + os.path.splitext(to_path)[1]))
        .replace("__EXTRA__", json.dumps(extra_samplers))
    )

    tmpdir = tempfile.mkdtemp(prefix="gltrans_")
    try:
        with open(os.path.join(tmpdir, "page.html"), "w", encoding="utf-8") as fh:
            fh.write(page_html)
        shutil.copyfile(from_path, os.path.join(tmpdir, "from" + os.path.splitext(from_path)[1]))
        shutil.copyfile(to_path, os.path.join(tmpdir, "to" + os.path.splitext(to_path)[1]))

        handler = functools.partial(
            http.server.SimpleHTTPRequestHandler, directory=tmpdir
        )
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(
                    args=["--enable-unsafe-swiftshader", "--disable-gpu-sandbox"]
                )
                page = browser.new_page(viewport={"width": width, "height": height})
                page.goto(f"http://127.0.0.1:{port}/page.html")
                page.wait_for_function("window.__ready === true", timeout=30000)
                if page.evaluate("window.__error || null"):
                    raise RuntimeError(page.evaluate("window.__error"))
                os.makedirs(frames_dir, exist_ok=True)
                for i in range(nframes):
                    t = 0.0 if nframes == 1 else i / (nframes - 1)
                    page.evaluate(f"window.setProgress({t!r})")
                    page.screenshot(
                        path=os.path.join(frames_dir, f"frame_{i:04d}.png")
                    )
                browser.close()
        finally:
            server.shutdown()
            thread.join()
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def encode_mp4(frames_dir, nframes, fps, out_path):
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "18", "-movflags", "+faststart",
        out_path,
    ]
    subprocess.run(cmd, check=True)
    return out_path


def parse_param(text):
    if "=" not in text:
        raise argparse.ArgumentTypeError("--param needs name=value")
    name, value = text.split("=", 1)
    return name.strip(), value.strip()


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Render a gl-transitions GLSL transition between two "
                    "images to MP4 (headless Chromium + ffmpeg)."
    )
    ap.add_argument("--list", action="store_true",
                    help="list available transition names and exit")
    ap.add_argument("--from", dest="from_img", metavar="IMAGE",
                    help="source image (shown at progress 0)")
    ap.add_argument("--to", dest="to_img", metavar="IMAGE",
                    help="destination image (shown at progress 1)")
    ap.add_argument("--transition", default="fade",
                    help="transition name (see --list)")
    ap.add_argument("--duration", type=float, default=1.0,
                    help="transition duration in seconds (default 1.0)")
    ap.add_argument("--fps", type=float, default=24.0,
                    help="output frames per second (default 24)")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--out", default="transition.mp4",
                    help="output MP4 path")
    ap.add_argument("--keep-frames", metavar="DIR",
                    help="keep the rendered PNG frames in DIR (default: temp, deleted)")
    ap.add_argument("--param", action="append", default=[],
                    type=parse_param, metavar="name=value",
                    help="override a transition uniform (repeatable)")
    args = ap.parse_args(argv)

    if args.list:
        for name in list_transitions():
            print(name)
        return 0

    if not args.from_img or not args.to_img:
        ap.error("--from and --to are required (unless --list)")

    uniforms, _body = parse_transition(args.transition)
    for name, value in args.param:
        if name not in uniforms:
            raise SystemExit(
                f"--param {name!r}: not a uniform of {args.transition} "
                f"(available: {', '.join(sorted(uniforms)) or 'none'})"
            )
        utype, _default = uniforms[name]
        if utype == "sampler2D":
            raise SystemExit(f"--param {name!r}: sampler uniforms cannot be overridden")
        uniforms[name] = (utype, value)  # validate now, fail fast
        coerce_value(utype, value)

    nframes = max(2, int(round(args.duration * args.fps)))
    frames_dir = args.keep_frames or tempfile.mkdtemp(prefix="gltrans_frames_")
    try:
        render_frames(args.transition, uniforms, args.width, args.height,
                      nframes, args.from_img, args.to_img, frames_dir)
        encode_mp4(frames_dir, nframes, args.fps, args.out)
    finally:
        if not args.keep_frames:
            shutil.rmtree(frames_dir, ignore_errors=True)

    print(f"wrote {args.out} ({nframes} frames, {args.transition}, "
          f"{args.width}x{args.height}@{args.fps:g}fps)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
