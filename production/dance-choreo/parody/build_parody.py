#!/usr/bin/env python3
"""Cape Jones hallway parody build v2 (Sc057 + Sc059, GB214 'The Words').
ROI/streaming version. Method + gaps documented in the PR README (lander.py).
"""
import io, os, sys, json, math, time, threading, subprocess
import numpy as np
import cv2
from PIL import Image, ImageDraw

W, H, FPS = 1920, 1080, 25
BASE = os.path.expanduser('~/workspace/_dance_choreo_work')
CJDIR = os.path.expanduser('~/workspace/_cj-dance-v2/build/parts')
STUDY = json.load(open(os.path.expanduser('~/workspace/_hallway_study/study_data_final.json')))
CHOREO = json.load(open(os.path.join(BASE, 'dance-gumball-darwin-words-sc057-sc059.json')))
t0 = time.time()
def log(*a): print(f'[{time.time()-t0:7.1f}s]', *a, flush=True)

def head_track_057():
    rot = {}
    for L in CHOREO['scene_057']['darwin_puppet_timeline'][0]['layers']:
        if L['name'] == 'GB200_DRW_HEADCOMP':
            for k in L['keyframes']:
                for e in k.get('elements', []):
                    m = e.get('matrix') or {}
                    if m.get('a') is not None and m.get('b') is not None:
                        rot[k['frame']] = math.degrees(math.atan2(m['b'], m['a']))
    return {f: (s, tx, ty, rot.get(f, 0.0)) for f, s, tx, ty in STUDY['sc057_darwin_headcomp_track_frame_scale_tx_ty']}

def head_track_059():
    tr = {}
    for L in CHOREO['scene_059']['darwin_puppet_timeline'][0]['layers']:
        if L['name'] == 'GB200_DRW_HEADCOMP':
            for k in L['keyframes']:
                for e in k.get('elements', []):
                    m = e.get('matrix') or {}
                    if m.get('a') is not None:
                        b = m.get('b') or 0.0
                        tr[k['frame']] = (math.hypot(m['a'], b), m.get('tx') or 0.0, m.get('ty') or 0.0,
                                          math.degrees(math.atan2(b, m['a'])))
    return tr

def leg_tracks(scene_key):
    out = {}
    for L in CHOREO[scene_key]['darwin_puppet_timeline'][0]['layers']:
        if L['name'] in ('Layer 22', 'Layer 23'):
            series = {}
            for k in L['keyframes']:
                for e in k.get('elements', []):
                    m = e.get('matrix') or {}
                    if e.get('type') == 'DOMSymbolInstance' and m.get('a') is not None and m.get('b') is not None:
                        series[k['frame']] = math.degrees(math.atan2(m['b'], m['a']))
            out[L['name']] = series
    return out

def hold_last(series, f, default=None):
    bv = default
    for k in sorted(series):
        if k <= f: bv = series[k]
        else: break
    return bv

PIVOTS = json.load(open(os.path.join(CJDIR, 'pivots.json')))
CANVAS = PIVOTS['size']; FEET = (CANVAS[0] / 2.0, float(CANVAS[1]))
PARTS = {}
def load_part(name, fname, pivot_key):
    im = Image.open(os.path.join(CJDIR, fname)).convert('RGBA')
    a = np.array(im)[..., 3]
    ys, xs = np.where(a > 0)
    pad = int(0.6 * max(xs.max() - xs.min(), ys.max() - ys.min())) + 10
    x0, x1 = max(0, xs.min() - pad), min(im.width, xs.max() + pad)
    y0, y1 = max(0, ys.min() - pad), min(im.height, ys.max() + pad)
    pv = PIVOTS['pivots'][pivot_key]
    PARTS[name] = (im.crop((x0, y0, x1, y1)), (pv[0] - x0, pv[1] - y0))
for n, f, p in [('cape', 'layer_cape.png', 'cape'), ('leg_l', 'layer_leg_l.png', 'leg_l'),
                ('leg_r', 'layer_leg_r.png', 'leg_r'), ('torso', 'layer_torso.png', 'torso'),
                ('arm_l', 'layer_arm_l.png', 'arm_l'), ('arm_r', 'layer_arm_r.png', 'arm_r'),
                ('head', 'layer_head.png', 'head')]:
    load_part(n, f, p)
log('parts loaded')

def place(dst, name, scale, sx, angle, target, flip, extra=1.0):
    crop, pv = PARTS[name]
    s = scale * extra
    img = crop.resize((max(2, int(crop.width * s)), max(2, int(crop.height * s))), Image.BICUBIC)
    if sx != 1.0:
        img = img.resize((max(2, int(img.width * sx)), img.height), Image.BICUBIC)
    pvx, pvy = pv[0] * s * sx, pv[1] * s
    if flip:
        img = img.transpose(Image.FLIP_LEFT_RIGHT); pvx = img.width - pvx
    if angle:
        img = img.rotate(angle, resample=Image.BICUBIC, center=(pvx, pvy))
    dst.alpha_composite(img, (int(round(target[0] - pvx)), int(round(target[1] - pvy))))

def map_pt(p, feet, s, sx, flip):
    dx = (p[0] - FEET[0]) * s * sx
    return (feet[0] + (-dx if flip else dx), feet[1] + (p[1] - FEET[1]) * s)

def orange_mask(rgb):
    R, G, B = rgb[..., 0].astype(np.int16), rgb[..., 1].astype(np.int16), rgb[..., 2].astype(np.int16)
    return ((R > 200) & (G > 90) & (G < 190) & (B < 90)).astype(np.uint8)

def chunked_median(files):
    stack = np.stack([np.array(Image.open(f).convert('RGB')) for f in files])
    out = np.empty((H, W, 3), np.uint8)
    for y in range(0, H, 270):
        out[y:y+270] = np.median(stack[:, y:y+270].astype(np.float32), axis=0).astype(np.uint8)
    del stack
    return out

def render_scene(scene, nframes, head_tr, leg_tr, is059, stats, sheet_frames, sheet_idx, sink):
    files = [os.path.join(BASE, f'frames{scene}_hd', f'{i}.png') for i in range(1, nframes + 1)]
    log(scene, 'median...')
    median = chunked_median(files[::4])
    log(scene, 'root track...')
    roots, union = [], np.zeros((H, W), np.uint8)
    for f in files:
        m = orange_mask(np.array(Image.open(f).convert('RGB')))
        ys, xs = np.where(m > 0)
        roots.append((int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())) if len(xs) else None)
        if is059: union |= m
    valid_roots = [r for r in roots if r is not None]
    log(scene, 'h first/last', valid_roots[0][3]-valid_roots[0][2], valid_roots[-1][3]-valid_roots[-1][2],
        '| no-Darwin frames:', len(roots) - len(valid_roots))
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
    plate059 = None
    if is059:
        um = cv2.dilate(union, ker, iterations=2)
        plate059 = cv2.inpaint(median, um, 8, cv2.INPAINT_TELEA)
        res = int(orange_mask(plate059).sum()); log(scene, 'plate residual orange', res)
        if res > 200:
            plate059 = cv2.inpaint(plate059, cv2.dilate(orange_mask(plate059), ker, iterations=1), 8, cv2.INPAINT_TELEA)
            log(scene, 'plate pass2 residual', int(orange_mask(plate059).sum()))
    hs = [head_tr[k] for k in sorted(head_tr)]
    tx_med = float(np.median([v[1] for v in hs])); ty_med = float(np.median([v[2] for v in hs])); s0 = hs[0][0]
    base_aspect = float(np.median([(r[1]-r[0]) / max(1, r[3]-r[2]) for r in roots[:42] if r is not None])) if is059 else None
    leg_l_series, leg_r_series = leg_tr.get('Layer 22', {}), leg_tr.get('Layer 23', {})
    log(scene, 'leg symbol kfs L22/L23:', len(leg_l_series), len(leg_r_series))
    cape_ang, prev_fx = 0.0, None
    for i in range(nframes):
        rgb = np.array(Image.open(files[i]).convert('RGB'))
        root_i = roots[i - (i % 2)]
        if root_i is None:
            # Recovery patch A: no Darwin in this source frame (Sc059 entry —
            # he is still off-screen) -> emit the clean plate with no CJ.
            rgb_out = (plate059 if is059 else rgb).copy()
            stats.append(dict(scene=scene, frame=i + 1, h=0, fx=-1, head_rot=0.0,
                              leg_l=0.0, leg_r=0.0, sx=1.0,
                              orange_plate=int(orange_mask(plate059[::4, ::4]).sum()) * 16 if is059 else 0,
                              green_plate=0, skin_px=0))
            if (i + 1) in sheet_idx:
                sheet_frames.append(Image.fromarray(rgb_out).resize((640, 360), Image.LANCZOS))
            sink(rgb_out)
            continue
        x0r, x1r, y0r, y1r = root_i
        if is059:
            plate = plate059
            orange_plate = int(orange_mask(plate059[::4, ::4]).sum()) * 16
            green_plate = 0
        else:
            shoe_ext = int(0.30 * (y1r - y0r)) + 12
            gx0, gx1 = max(0, x0r - 60), min(W, x1r + 60)
            gy0, gy1 = max(0, y0r - 60), min(H, y1r + 60 + shoe_ext)
            roi, med = rgb[gy0:gy1, gx0:gx1], median[gy0:gy1, gx0:gx1]
            m = orange_mask(roi)
            R, G, B = roi[..., 0].astype(np.int16), roi[..., 1].astype(np.int16), roi[..., 2].astype(np.int16)
            green = ((G > R + 25) & (G > B + 25) & (G > 90)).astype(np.uint8)
            diff = (np.abs(roi.astype(np.int16) - med.astype(np.int16)).max(axis=2) > 42).astype(np.uint8)
            bx0, bx1, by0, by1 = x0r - gx0, x1r - gx0, y0r - gy0, y1r - gy0
            # Patch C(b): inner extends BELOW the orange bbox — Darwin's green
            # shoes hang below his lowest orange pixel and escaped the old region.
            inner = np.zeros_like(m); inner[max(0,by0-18):by1+18+shoe_ext, max(0,bx0-18):bx1+18] = 1
            mask = np.clip(cv2.dilate(m, ker, iterations=1) + green * inner + diff * inner, 0, 1)
            # Patch C(a): fill by inpainting the frame itself, NOT from the
            # temporal median. Visual QA of run 3 proved the median is itself a
            # Darwin ghost (he occupies the dance zone in most samples), and the
            # old fill smeared that ghost around CJ. Inpaint propagates the
            # frame's own boundary colours (Sc059's plate relies on it too).
            # The median is kept only as the diff reference above.
            proi = cv2.inpaint(roi, (mask > 0).astype(np.uint8), 8, cv2.INPAINT_TELEA)
            res = orange_mask(proi) * inner
            if res.sum() > 150:
                proi = cv2.inpaint(proi, cv2.dilate(res, ker, iterations=1), 6, cv2.INPAINT_TELEA)
            R2, G2, B2 = proi[..., 0].astype(np.int16), proi[..., 1].astype(np.int16), proi[..., 2].astype(np.int16)
            gres = ((G2 > R2 + 25) & (G2 > B2 + 25) & (G2 > 90)).astype(np.uint8) * inner
            if gres.sum() > 150:
                proi = cv2.inpaint(proi, cv2.dilate(gres, ker, iterations=1), 6, cv2.INPAINT_TELEA)
                R2, G2, B2 = proi[..., 0].astype(np.int16), proi[..., 1].astype(np.int16), proi[..., 2].astype(np.int16)
                gres = ((G2 > R2 + 25) & (G2 > B2 + 25) & (G2 > 90)).astype(np.uint8) * inner
            plate = rgb.copy(); plate[gy0:gy1, gx0:gx1] = proi
            orange_plate = int(orange_mask(proi[by0:by1, bx0:bx1]).sum())
            green_plate = int(gres.sum())
        bw, bh = x1r - x0r, y1r - y0r
        fx, fy = (x0r + x1r) / 2.0, float(y1r)
        s = bh / CANVAS[1]
        flip = True
        hscale_v, htx, hty, hrot = hold_last(head_tr, i - (i % 2), default=(s0, tx_med, ty_med, 0.0))
        # Patch C(c): fold head-symbol back-view flips (atan2 ~ +/-180 in the
        # source track) to the equivalent near-level tilt. CJ has no back-view
        # head (disclosed gap); run 3 applied the flip raw and CJ tumbled
        # upside-down wherever Darwin's symbol flipped (e.g. Sc057 finale).
        hrot = ((hrot + 90.0) % 180.0) - 90.0
        hdx = float(np.clip((htx - tx_med) * 0.045 * (bh / 140.0), -0.32 * bh, 0.32 * bh))
        hdy = float(np.clip((hty - ty_med) * 0.045 * (bh / 140.0), -0.25 * bh, 0.25 * bh))
        spread = float(np.clip((bw / max(1, bh) - 0.62) * 55.0, 0, 28)) if not is059 else 0.0
        lr_l = hold_last(leg_l_series, i - (i % 2)); lr_r = hold_last(leg_r_series, i - (i % 2))
        if is059:
            ang_ll = lr_l if lr_l is not None else 0.0; ang_lr = lr_r if lr_r is not None else 0.0
        else:
            ang_ll = (lr_l * 0.6 if lr_l is not None else 0.0) + spread
            ang_lr = (lr_r * 0.6 if lr_r is not None else 0.0) - spread
        sx = 1.0
        if is059 and base_aspect:
            sx = float(np.clip((bw / max(1, bh)) / base_aspect, 0.30, 1.15))
            if sx < 0.5: flip = not flip
        vx = 0.0 if prev_fx is None else fx - prev_fx; prev_fx = fx
        cape_ang += (float(np.clip(-vx * 1.3, -28, 28)) - cape_ang) * 0.25
        lean = hrot * 0.35 + float(np.clip(vx * 0.12, -6, 6))
        img = Image.fromarray(plate).convert('RGBA')
        ImageDraw.Draw(img, 'RGBA').ellipse([fx - bw * 0.45, fy - 6, fx + bw * 0.45, fy + 10], fill=(0, 0, 0, 80))
        feet, pv = (fx, fy), PIVOTS['pivots']
        place(img, 'cape', s, sx, -cape_ang if not flip else cape_ang, map_pt(pv['cape'], feet, s, sx, flip), flip)
        place(img, 'leg_l', s, sx, -ang_ll if flip else ang_ll, map_pt(pv['leg_l'], feet, s, sx, flip), flip)
        place(img, 'leg_r', s, sx, -ang_lr if flip else ang_lr, map_pt(pv['leg_r'], feet, s, sx, flip), flip)
        place(img, 'torso', s, sx, -lean if flip else lean, map_pt(pv['torso'], feet, s, sx, flip), flip)
        arm_swing = float(np.clip(-hrot * 1.1, -30, 30))
        place(img, 'arm_l', s, sx, -arm_swing if flip else arm_swing, map_pt(pv['arm_l'], feet, s, sx, flip), flip)
        place(img, 'arm_r', s, sx, arm_swing if flip else -arm_swing, map_pt(pv['arm_r'], feet, s, sx, flip), flip)
        head_t = map_pt(pv['head'], feet, s, sx, flip)
        head_t = (head_t[0] + (-hdx if flip else hdx), head_t[1] + hdy)
        place(img, 'head', s, sx, -hrot if flip else hrot, head_t, flip,
              extra=float(np.clip((hscale_v / s0) ** 0.55, 0.85, 1.65)))
        rgb_out = np.array(img.convert('RGB'))
        skin = int(((np.abs(rgb_out[..., 0].astype(np.int16) - 229) < 38) &
                    (np.abs(rgb_out[..., 1].astype(np.int16) - 178) < 38) &
                    (np.abs(rgb_out[..., 2].astype(np.int16) - 140) < 42)).sum())
        stats.append(dict(scene=scene, frame=i + 1, h=int(bh), fx=int(fx), head_rot=round(float(hrot), 1),
                          leg_l=round(float(ang_ll), 1), leg_r=round(float(ang_lr), 1), sx=round(sx, 2),
                          orange_plate=int(orange_plate), green_plate=int(green_plate), skin_px=skin))
        if (i + 1) in sheet_idx:
            sheet_frames.append(img.convert('RGB').resize((640, 360), Image.LANCZOS))
        sink(rgb_out)
        if (i + 1) % 40 == 0: log(scene, 'rendered', i + 1)

stats, sheet_frames = [], []
WORKDIR = os.path.expanduser('~/workspace/_hallway_study')

# Recovery patch D (segmented, reboot-proof): encode PER SCENE (same settings),
# and the moment a scene finishes, upload its MP4 as a GitHub blob and persist
# its stats as JSON — server-side persistence survives the VM reboots/drains
# that killed runs 2 and 4. SKIP057=1 resumes from scene 057's blob + stats.
# The two scene MP4s are joined with the ffmpeg concat demuxer (stream copy,
# re-wrapped to one fragmented MP4) — verified working on a 40-frame test.
def gh_blob(data):
    import base64 as b64
    payload = json.dumps({"content": b64.b64encode(data).decode(), "encoding": "base64"})
    for att in range(4):
        r = subprocess.run(['gh', 'api', '--method', 'POST', 'repos/mhvnsnt/cape-jones/git/blobs', '--input', '-'],
                           input=payload, capture_output=True, text=True)
        if r.returncode == 0:
            return json.loads(r.stdout)['sha']
        log('blob upload attempt', att + 1, 'failed:', r.stderr[:160]); time.sleep(5 * (att + 1))
    raise RuntimeError('blob upload failed after retries')

def gh_get_blob(sha):
    import base64 as b64
    r = subprocess.run(['gh', 'api', f'repos/mhvnsnt/cape-jones/git/blobs/{sha}'], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:300]
    return b64.b64decode(json.loads(r.stdout)['content'])

def encode_scene(scene, nframes, head_tr, leg_tr, is059, sheet_idx):
    dur = nframes / FPS
    cmd = ['ffmpeg', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0',
           '-i', os.path.join(BASE, f'audio{scene}.mp3'),
           '-filter_complex', f'[1:a]atrim=0:{dur},asetpts=PTS-STARTPTS[a]',
           '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium',
           '-c:a', 'aac', '-b:a', '160k', '-movflags', 'frag_keyframe+empty_moov+default_base_moof', '-f', 'mp4', 'pipe:1']
    log('ffmpeg encode start (streaming)', scene)
    errf = open(os.path.join(WORKDIR, f'ffmpeg_err_{scene}.log'), 'wb')
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errf)
    chunks = []
    def drain():
        while True:
            b = proc.stdout.read(1 << 20)
            if not b: break
            chunks.append(b)
    dt = threading.Thread(target=drain); dt.start()
    def sink(fr):
        proc.stdin.write(fr.tobytes())
    render_scene(scene, nframes, head_tr, leg_tr, is059, stats, sheet_frames, sheet_idx, sink)
    proc.stdin.close(); dt.join(); proc.wait(); errf.close()
    data = b''.join(chunks)
    log(scene, 'scene mp4 bytes', len(data))
    return data

def extract_tiles(mp4_bytes, ns):
    sel = '+'.join(f'eq(n\\,{n})' for n in ns)
    p = subprocess.run(['ffmpeg', '-i', 'pipe:0', '-vf', f"select='{sel}',scale=640:360",
                        '-vsync', '0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', 'pipe:1'],
                       input=mp4_bytes, capture_output=True)
    tb = 640 * 360 * 3
    assert len(p.stdout) == len(ns) * tb, f'tile extract {len(p.stdout)} != {len(ns) * tb}'
    return [Image.frombytes('RGB', (640, 360), p.stdout[i * tb:(i + 1) * tb]) for i in range(len(ns))]

scene_mp4 = {}
if os.environ.get('SKIP057') and os.path.exists(os.path.join(WORKDIR, 'stats057.json')):
    stats.extend(json.load(open(os.path.join(WORKDIR, 'stats057.json'))))
    sha057 = [l.split()[1] for l in open(os.path.join(WORKDIR, 'run5_blobs.txt')) if l.startswith('SCENE057')][-1]
    scene_mp4['057'] = gh_get_blob(sha057)
    sheet_frames.extend(extract_tiles(scene_mp4['057'], [9, 59, 109, 159, 194]))
    log('resumed 057 from blob', sha057, len(scene_mp4['057']), 'bytes | stats', len(stats), '| tiles', len(sheet_frames))
else:
    s0 = len(stats)
    scene_mp4['057'] = encode_scene('057', 198, head_track_057(), leg_tracks('scene_057'), False, {10, 60, 110, 160, 195})
    json.dump(stats[s0:], open(os.path.join(WORKDIR, 'stats057.json'), 'w'))
    sha = gh_blob(scene_mp4['057'])
    open(os.path.join(WORKDIR, 'run5_blobs.txt'), 'a').write(f"SCENE057 {sha} {len(scene_mp4['057'])}\n")
    log('057 persisted: blob', sha)
s0 = len(stats)
scene_mp4['059'] = encode_scene('059', 105, head_track_059(), leg_tracks('scene_059'), True, {10, 50, 70, 100})
json.dump(stats[s0:], open(os.path.join(WORKDIR, 'stats059.json'), 'w'))
sha = gh_blob(scene_mp4['059'])
open(os.path.join(WORKDIR, 'run5_blobs.txt'), 'a').write(f"SCENE059 {sha} {len(scene_mp4['059'])}\n")
log('059 persisted: blob', sha)
open('/tmp/scene057.mp4', 'wb').write(scene_mp4['057'])
open('/tmp/scene059.mp4', 'wb').write(scene_mp4['059'])
open('/tmp/concat_list.txt', 'w').write("file '/tmp/scene057.mp4'\nfile '/tmp/scene059.mp4'\n")
p = subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', '/tmp/concat_list.txt', '-c', 'copy',
                    '-movflags', 'frag_keyframe+empty_moov+default_base_moof', '-f', 'mp4', 'pipe:1'],
                   capture_output=True)
mp4 = p.stdout
log('concat mp4 bytes', len(mp4), '| ffmpeg tail:', (p.stderr.decode(errors='replace').strip().splitlines() or [''])[-1])
open('/tmp/final_parody.mp4', 'wb').write(mp4)
probe = subprocess.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
                        '-show_entries', 'stream=nb_read_frames', '-of', 'csv', '/tmp/final_parody.mp4'],
                       capture_output=True, text=True)
log('ffprobe video frames:', probe.stdout.strip())
assert '303' in probe.stdout, 'final MP4 frame count is not 303 — not landing'
log('total frames', len(stats), 'sheet tiles', len(sheet_frames))
sheet = Image.new('RGB', (1920, 1080), (24, 24, 24))
for idx, tile in enumerate(sheet_frames[:9]):
    sheet.paste(tile, ((idx % 3) * 640, (idx // 3) * 360))
buf = io.BytesIO(); sheet.save(buf, format='PNG'); sheet_bytes = buf.getvalue()
present = [st for st in stats if st['h'] > 0]
poses = {(st['head_rot'], st['leg_l'], st['leg_r']) for st in present}
h057 = [st['h'] for st in stats if st['scene'] == '057']
verdict = dict(distinct_poses=len(poses), skin_px_min=min(st['skin_px'] for st in present),
               orange_plate_max=max(st['orange_plate'] for st in stats),
               green_plate_max=max(st['green_plate'] for st in stats),
               empty_frames=len(stats) - len(present),
               h057_first=h057[0], h057_last=h057[-1], mp4_bytes=len(mp4), sheet_bytes=len(sheet_bytes), stats=stats)
log('VERIFY', verdict['distinct_poses'], 'poses | skin min', verdict['skin_px_min'], '| orange max', verdict['orange_plate_max'], '| green max', verdict['green_plate_max'])
sys.path.insert(0, os.path.expanduser('~/workspace/_hallway_study'))
import lander
lander.land(mp4, sheet_bytes, verdict)
log('DONE')
