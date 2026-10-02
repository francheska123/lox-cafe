"""Draw the Lox Café logo (a small-town-diner nod: flannel plaid, hanging sign,
backwards cap, diner mug). Writes art/logo-1024.png.  Run: python3 art/make_logo.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT = '/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf'
S = 2048; k = S / 1024
INK = (43, 26, 20); CREAM = (250, 243, 231); CHOC = (58, 24, 9); TERRA = (138, 62, 31)
NAVY = (40, 82, 150); BLUE = (98, 160, 232); PINK = (255, 143, 196); BLUSH = (255, 160, 190); MUG = (255, 253, 247); ESP = (74, 42, 26); LAPIS = (110, 191, 234)
r = lambda v: [int(x * k) for x in v]

def plaid(w, h):
    base = Image.new('RGBA', (w, h), BLUE + (255,))
    ov = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    step = int(170 * k)
    for i in range(-step, max(w, h) + step, step):
        d.rectangle([i, 0, i + int(70 * k), h], fill=(60, 118, 205, 120))
        d.rectangle([0, i, w, i + int(70 * k)], fill=(60, 118, 205, 120))
        d.rectangle([i + int(108 * k), 0, i + int(120 * k), h], fill=(255, 255, 255, 150))
        d.rectangle([0, i + int(108 * k), w, i + int(120 * k)], fill=(255, 255, 255, 150))
        d.rectangle([i + int(140 * k), 0, i + int(145 * k), h], fill=PINK + (200,))
        d.rectangle([0, i + int(140 * k), w, i + int(145 * k)], fill=PINK + (200,))
    base.alpha_composite(ov)
    return base

def draw_logo():
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    m = 100
    mask = Image.new('L', (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle(r([m, m, 1024 - m, 1024 - m]), radius=int(185 * k), fill=255)
    img.paste(plaid(S, S), (0, 0), mask)
    d = ImageDraw.Draw(img)

    # Chains and hanging sign
    for x in (330, 694):
        d.line(r([x, m + 10, x, 205]), fill=INK, width=int(9 * k))
        for y in range(m + 25, 200, 26):
            d.ellipse(r([x - 9, y, x + 9, y + 18]), outline=INK, width=int(6 * k))
    d.rounded_rectangle(r([218, 195, 806, 340]), radius=int(24 * k), fill=CREAM, outline=INK, width=int(18 * k))
    d.rounded_rectangle(r([240, 216, 784, 319]), radius=int(14 * k), outline=PINK, width=int(6 * k))
    font = ImageFont.truetype(FONT, int(76 * k))
    text = 'LOX CAFÉ'
    tw = d.textlength(text, font=font)
    bbox = d.textbbox((0, 0), text, font=font)
    th = bbox[3] - bbox[1]
    d.text(((S - tw) / 2, int(267 * k) - th / 2 - bbox[1]), text, font=font, fill=CHOC)

    # Backwards cap tipped on the sign's corner (drawn on its own layer, then tilted)
    cap = Image.new('RGBA', (int(260 * k), int(200 * k)), (0, 0, 0, 0)); c = ImageDraw.Draw(cap)
    q = lambda v: [int(x * k) for x in v]
    c.rounded_rectangle(q([116, 110, 232, 152]), radius=int(20 * k), fill=NAVY, outline=INK, width=int(8 * k))   # bill pointing back
    c.pieslice(q([20, 40, 190, 200]), 180, 360, fill=NAVY, outline=INK, width=int(9 * k))                       # crown
    c.line(q([24, 120, 186, 120]), fill=INK, width=int(9 * k))                                                  # brim edge
    c.arc(q([62, 40, 148, 200]), 180, 360, fill=(84, 126, 176), width=int(6 * k))                              # panel seams
    c.line(q([105, 42, 105, 118]), fill=(84, 126, 176), width=int(6 * k))
    c.ellipse(q([94, 30, 116, 52]), fill=NAVY, outline=INK, width=int(6 * k))                                   # button
    c.chord(q([30, 96, 72, 136]), 180, 360, fill=CREAM, outline=INK, width=int(5 * k))                          # strap opening at the back
    cap = cap.rotate(-14, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(cap, (int(640 * k), int(92 * k)))
    d = ImageDraw.Draw(img)

    # Steam: soft sine waves
    import math
    for x0 in (448, 512, 576):
        pts = [(int((x0 + 11 * math.sin(t / 11)) * k), int((436 - t) * k)) for t in range(0, 72, 2)]
        d.line(pts, fill=CREAM, width=int(13 * k), joint='curve')
        for px, py in (pts[0], pts[-1]):
            rr = int(6.5 * k); d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=CREAM)

    def heart(cx, cy, size, fill):
        sz = size
        d.ellipse(r([cx - sz, cy - sz * .6, cx, cy + sz * .4]), fill=fill)
        d.ellipse(r([cx, cy - sz * .6, cx + sz, cy + sz * .4]), fill=fill)
        d.polygon(r([cx - sz * .95, cy, cx + sz * .95, cy, cx, cy + sz * 1.05]), fill=fill)
    heart(512, 350, 22, PINK)
    def sparkle(cx, cy, s, fill):
        d.polygon(r([cx, cy - s, cx + s * .28, cy - s * .28, cx + s, cy, cx + s * .28, cy + s * .28, cx, cy + s, cx - s * .28, cy + s * .28, cx - s, cy, cx - s * .28, cy - s * .28]), fill=fill)
    for (sx, sy, ss) in ((205, 430, 30), (812, 470, 24), (230, 640, 18), (800, 760, 28), (176, 760, 16)):
        sparkle(sx, sy, ss, (255, 244, 170))

    # Saucer, handle, mug, stripes, coffee
    d.ellipse(r([240, 772, 784, 860]), fill=MUG, outline=INK, width=int(18 * k))
    d.ellipse(r([618, 548, 772, 716]), outline=INK, width=int(46 * k))
    d.ellipse(r([626, 556, 764, 708]), outline=MUG, width=int(26 * k))
    d.rounded_rectangle(r([318, 470, 666, 812]), radius=int(66 * k), fill=MUG, outline=INK, width=int(20 * k))
    d.rectangle(r([329, 532, 655, 546]), fill=PINK)
    # Face: big shiny eyes, blush, cheeky grin with two tiny teeth
    for ex in (420, 564):
        d.ellipse(r([ex - 30, 600, ex + 30, 668]), fill=INK)
        d.ellipse(r([ex - 17, 610, ex + 3, 632]), fill=(255, 255, 255))
        d.ellipse(r([ex + 6, 642, ex + 16, 652]), fill=(255, 255, 255))
    for bx in (370, 614):
        d.ellipse(r([bx - 30, 676, bx + 30, 702]), fill=BLUSH)
    d.chord(r([452, 664, 532, 726]), 0, 180, fill=INK)
    d.polygon(r([470, 694, 482, 694, 476, 708]), fill=(255, 255, 255))
    d.polygon(r([502, 694, 514, 694, 508, 708]), fill=(255, 255, 255))
    d.ellipse(r([478, 704, 506, 722]), fill=(242, 110, 140))
    d.ellipse(r([318, 438, 666, 512]), fill=ESP, outline=INK, width=int(20 * k))
    d.ellipse(r([420, 456, 564, 492]), fill=(214, 160, 110))

    # Tile outline on top
    ImageDraw.Draw(img).rounded_rectangle(r([m, m, 1024 - m, 1024 - m]), radius=int(185 * k), outline=INK, width=int(22 * k))
    return img.resize((1024, 1024), Image.LANCZOS)

if __name__ == '__main__':
    out = Path(__file__).with_name('logo-1024.png')
    draw_logo().save(out)
    print('wrote', out)
