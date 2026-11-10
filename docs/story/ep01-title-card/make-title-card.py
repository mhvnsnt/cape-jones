"""TRACK C — IMMORTAL QOMBAT title card (Ep1 Scene 3).
Script beat: full-frame TV graphic, IMMORTAL QOMBAT, kanji below,
stylized Q animates open into the word Qombat. Dark/dramatic MK-parody tone.
No 'Western Heart' anywhere. Kanji: (fushi, immortality) — owner-confirmed.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

OUT = os.path.dirname(os.path.abspath(__file__))
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CJK  = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"

BONE = (235, 228, 210)
RED  = (196, 18, 28)
GOLD = (212, 175, 105)
DARK = (8, 6, 8)

def font(path, size, idx=0):
    try: return ImageFont.truetype(path, size, index=idx)
    except Exception: return ImageFont.truetype(path, size)

def cjk_font(size):
    # NotoSerifCJK-Bold.ttc: try indices until kanji renders (JP face)
    for idx in range(6):
        try:
            f = ImageFont.truetype(CJK, size, index=idx)
            # check glyph exists by mask size
            m = f.getmask("\u4e0d")
            if m.size[0] > 0: return f
        except Exception: pass
    return ImageFont.truetype(CJK, size)

def text_w(draw, s, f):
    b = draw.textbbox((0,0), s, font=f)
    return b[2]-b[0], b[3]-b[1]

def draw_centered(draw, cx, y, s, f, fill, tracking=0, stroke_w=0, stroke_fill=None):
    # manual tracking
    widths = []
    for ch in s:
        bb = draw.textbbox((0,0), ch, font=f)
        widths.append(bb[2]-bb[0])
    total = sum(widths) + tracking*(len(s)-1)
    x = cx - total/2
    for ch, w in zip(s, widths):
        draw.text((x, y), ch, font=f, fill=fill, stroke_width=stroke_w, stroke_fill=stroke_fill)
        x += w + tracking
    return total

def background(W, H, glow=1.0):
    img = Image.new("RGB", (W, H), DARK)
    d0 = ImageDraw.Draw(img)
    # subtle vertical gradient: lighter toward center
    for y in range(H):
        t = y / H
        v = int(14 + 18 * max(0.0, 1 - abs(t - 0.48) * 2.2))
        d0.line([(0, y), (W, y)], fill=(v, v - 2, v - 2))
    # soft red radial glow, heavily blurred so it has NO hard oval edge
    sw, sh = W // 8, H // 8
    glow_img = Image.new("RGB", (sw, sh), (0, 0, 0))
    gd = ImageDraw.Draw(glow_img)
    cx, cy = sw // 2, int(sh * 0.46)
    for i in range(24, 0, -1):
        a = int(30 * glow * (i / 24) ** 2)
        r = int(sw * 0.42 * i / 24)
        gd.ellipse([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)], fill=(a, 0, 0))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(sw // 10)).resize((W, H))
    from PIL import ImageChops
    img = ImageChops.screen(img, glow_img)
    # soft vignette (blurred radial mask)
    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-W * 0.12, -H * 0.18, W * 1.12, H * 1.18], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(W // 6))
    img = Image.composite(img, Image.new("RGB", (W, H), (0, 0, 0)), vig)
    return img

def draw_card(W, H, t=1.0, q_open=1.0, kanji_a=1.0, title_a=1.0):
    """t: overall; q_open 0..1 = Q standalone -> full QOMBAT revealed;
       kanji_a, title_a: fade alphas."""
    base = background(W, H, glow=0.4 + 0.6*title_a)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cy_title = int(H*0.40)
    # IMMORTAL (smaller, gold, tracked)
    f_imm = font(SANS, int(H*0.078))
    if title_a > 0:
        a = int(255*title_a)
        draw_centered(d, W//2, int(H*0.235), "IMMORTAL", f_imm,
                      fill=GOLD+(a,), tracking=int(W*0.028))
    # QOMBAT: Q in red, rest bone. Layout measured at full alpha positions.
    f_q = font(SANS, int(H*0.19))
    # measure full word
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    wQ, _ = text_w(tmp, "Q", f_q)
    w_rest, _ = text_w(tmp, "OMBAT", f_q)
    track = int(W*0.004)
    total = wQ + track + w_rest + track*4
    x0 = W//2 - total//2
    yq = int(H*0.355)
    # Q tail slash (stylized Q): diagonal stroke through lower-right of Q
    # draw Q
    if title_a > 0:
        a = int(255*title_a)
        d.text((x0, yq), "Q", font=f_q, fill=RED+(a,),
               stroke_width=max(3, W//700), stroke_fill=(60, 0, 0, a))
        # slash tail: from Q lower bowl outward down-right
        qbox = d.textbbox((x0, yq), "Q", font=f_q)
        d.line([qbox[2]-wQ*0.18, qbox[3]-H*0.02, qbox[2]+wQ*0.22, qbox[3]+H*0.055],
               fill=RED+(a,), width=max(8, W//240))
        # rest of word reveals as q_open grows: OMBAT fades + slides in
        # from the right out of the Q (no mask crop: masks caused ghost overlap)
        if q_open > 0:
            xr = x0 + wQ + track
            off = int((1 - q_open) * W * 0.03)
            rest_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            rd = ImageDraw.Draw(rest_layer)
            draw_centered(rd, xr + w_rest // 2 + track * 2, yq, "OMBAT", f_q,
                          fill=BONE + (int(255 * q_open),), tracking=track)
            shifted = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            shifted.paste(rest_layer, (off, 0))
            layer = Image.alpha_composite(layer, shifted)
    # divider rules + kanji (re-bind Draw: layer was replaced by the reveal composite)
    d = ImageDraw.Draw(layer)
    if kanji_a > 0:
        a = int(255*kanji_a)
        ky = int(H*0.625)
        f_k = cjk_font(int(H*0.15))
        kw, _ = text_w(d, "\u4e0d\u6b7b", f_k)
        d.text((W//2 - kw//2, ky), "\u4e0d\u6b7b", font=f_k, fill=RED+(a,),
               stroke_width=max(2, W//900), stroke_fill=(40, 0, 0, a))
        rw = int(W*0.10)
        gap = int(W*0.02)
        ry = ky + int(H*0.15)//2
        d.line([W//2 - kw//2 - gap - rw, ry, W//2 - kw//2 - gap, ry], fill=GOLD+(a,), width=max(3, H//400))
        d.line([W//2 + kw//2 + gap, ry, W//2 + kw//2 + gap + rw, ry], fill=GOLD+(a,), width=max(3, H//400))
    out = Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")
    return out

if __name__ == "__main__":
    import sys
    W, H = 3840, 2160
    still = draw_card(W, H)
    still.save(os.path.join(OUT, "immortal-qombat-title-card-4k.png"))
    print("still saved", still.size)
    # animation frames at 1920x1080, 6s @ 30fps
    FW, FH, FPS, DUR = 1920, 1080, 30, 6
    n = FPS * DUR
    for i in range(n):
        t = i / FPS
        if t < 0.8: title_a = t/0.8; q_open = 0.0; kanji_a = 0.0
        elif t < 2.2: title_a = 1.0; q_open = (t-0.8)/1.4; kanji_a = 0.0
        elif t < 3.2: title_a = 1.0; q_open = 1.0; kanji_a = (t-2.2)/1.0
        else:
            title_a = 1.0; q_open = 1.0; kanji_a = 1.0
        # ease
        def ease(x): return x*x*(3-2*x)
        fr = draw_card(FW, FH, title_a=ease(title_a), q_open=ease(q_open), kanji_a=ease(kanji_a))
        fr.save(os.path.join(OUT, "frames", f"f{i:04d}.png"))
        if i % 30 == 0: print(f"frame {i}/{n}")
    print("frames done")
