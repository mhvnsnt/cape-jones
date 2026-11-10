#!/usr/bin/env python3
"""TOOL 5 — SWF inspector + Ruffle (rank #5).
Two honest halves, kept separate:
 (a) pure-Python SWF header parser — signature (FWS uncompressed / CWS
     zlib / ZWS LZMA), version, frame size (RECT bit-packed), frame rate,
     frame count. This is the same header read the show-repo audit used
     to get Foster's reel fps + frame counts (all 24 fps).
 (b) Ruffle 0.7.1 player (installed in this folder, ./ruffle --version
     verified) for eye-checking a real .swf. Ruffle desktop is a PLAYER,
     not a headless batch renderer — there is no screenshot mode in the
     stable CLI, so this tool does NOT claim batch SWF rendering.
     Command to eye-check: ./ruffle <file.swf>
Usage:
  tool5_swf_ruffle.py header <file.swf>   -> header JSON
  tool5_swf_ruffle.py make-test-swf <out.swf> -> minimal FWS header, 24 fps, 1 frame
  tool5_swf_ruffle.py ruffle-version -> installed Ruffle version
"""
import sys, os, json, struct, subprocess, zlib

def parse_header(path):
    data = open(path, "rb").read()
    if len(data) < 8:
        return {"tool": "swf_ruffle", "error": "file too short for a SWF header"}
    sig = data[0:3].decode("latin1")
    version = data[3]
    length = struct.unpack("<I", data[4:8])[0]
    body = data[8:]
    if sig == "CWS":
        try:
            body = zlib.decompress(body)
        except Exception as e:
            return {"tool": "swf_ruffle", "error": f"zlib decompress failed: {e}"}
    if sig == "ZWS":
        return {"tool": "swf_ruffle", "signature": sig, "version": version,
                "note": "LZMA-compressed SWF — header body not parsed here, Ruffle handles it"}
    # RECT: 5 bits nbits, then 4 x nbits values, in twips (1/20 px)
    b0 = body[0]
    nbits = b0 >> 3
    total_bits = 5 + 4 * nbits
    total_bytes = (total_bits + 7) // 8
    bits = "".join(f"{b:08b}" for b in body[:total_bytes])
    vals = []
    for i in range(4):
        chunk = bits[5 + i * nbits: 5 + (i + 1) * nbits]
        v = int(chunk, 2) if chunk else 0
        if v >= (1 << (nbits - 1)):
            v -= (1 << nbits)
        vals.append(v / 20.0)
    off = total_bytes
    fps = body[off] + body[off + 1] / 256.0 if len(body) > off + 1 else None
    frames = struct.unpack("<H", body[off + 2:off + 4])[0] if len(body) > off + 3 else None
    return {"tool": "swf_ruffle", "signature": sig, "version": version,
            "declared_length": length, "frame_size_px": vals,
            "frame_rate": fps, "frame_count": frames}

def make_test_swf(out):
    # FWS, version 10, RECT nbits=5, xmin=0 xmax=1100*20, ymin=0 ymax=1500*20
    # RECT bits: 00101 + 4x5-bit values (0, 22000 needs >5 bits -> use nbits=16)
    nbits = 16
    vals = [0, 22000, 0, 30000]
    bits = f"{nbits:05b}" + "".join(f"{v:016b}" for v in vals)
    bits += "0" * ((8 - len(bits) % 8) % 8)
    rect = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
    body = rect + bytes([24, 0]) + struct.pack("<H", 1)  # 24.0 fps, 1 frame
    data = b"FWS" + bytes([10]) + struct.pack("<I", 8 + len(body)) + body
    open(out, "wb").write(data)
    return {"tool": "swf_ruffle", "test_swf": out, "bytes": len(data)}

def ruffle_version():
    r = subprocess.run([os.path.join(os.path.dirname(__file__), "ruffle"), "--version"],
                       capture_output=True, text=True)
    return {"tool": "swf_ruffle", "ruffle": (r.stdout or r.stderr).strip(),
            "eye_check_command": "./ruffle <file.swf>",
            "limit": "Ruffle desktop is a player, not a headless batch renderer"}

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "header":
        print(json.dumps(parse_header(sys.argv[2]), indent=2))
    elif cmd == "make-test-swf":
        print(json.dumps(make_test_swf(sys.argv[2]), indent=2))
    elif cmd == "ruffle-version":
        print(json.dumps(ruffle_version(), indent=2))
    else:
        print("usage: header|make-test-swf|ruffle-version", file=sys.stderr); sys.exit(2)
