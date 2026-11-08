#!/usr/bin/env python3
"""Backfill missing dusaitool og images (1200x630) in the style of the
existing Loop template cards: navy diagonal gradient, DUS AI TOOL
eyebrow + blue bar, bold title left, frosted square with a white
spark (site mark) right, footer line. Titles come from each
article's own frontmatter, so nothing is invented.

Repo copy of ~/workspace/dusaitool-tag-cleanup/generate_og.py, adapted
so it can run anywhere the repo is checked out (locally and in the
GitHub Actions deploy job). Differences from the local copy:
- repo root comes from this file's location (scripts/../), or the
  DUSAITOOL_ROOT env var, never a hardcoded /home/... path;
- fonts resolve per font as env var (OG_FONT_EN_BOLD, OG_FONT_EN_REG,
  OG_FONT_HI_BOLD, OG_FONT_HI_REG) -> `fc-match` query -> the
  /usr/share/fonts/truetype/noto/... fallback, and only when a card is
  actually rendered, so a run with nothing missing never touches fonts;
- a missing font fails loudly instead of rendering tofu boxes.

Usage:
  python3 scripts/generate_og.py samples   # 4 sample cards into ./samples/
  python3 scripts/generate_og.py all       # missing-only: every article
                                            # without ogImage gets a card
                                            # in public/og/ + an ogImage
                                            # frontmatter line (checkout
                                            # only; nothing is committed)
"""
import math, os, pathlib, re, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630


def _repo_root():
    env = os.environ.get("DUSAITOOL_ROOT")
    if env:
        return pathlib.Path(env)
    return pathlib.Path(__file__).resolve().parent.parent


BASE = _repo_root()
OG = BASE / "public/og"

_FALLBACK_FONTS = {
    "en_bold": "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "en_reg": "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "hi_bold": "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf",
    "hi_reg": "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
}
_FC_QUERY = {
    "en_bold": "Noto Sans:weight=bold",
    "en_reg": "Noto Sans",
    "hi_bold": "Noto Sans Devanagari:weight=bold",
    "hi_reg": "Noto Sans Devanagari",
}
_ENV_FONT = {
    "en_bold": "OG_FONT_EN_BOLD",
    "en_reg": "OG_FONT_EN_REG",
    "hi_bold": "OG_FONT_HI_BOLD",
    "hi_reg": "OG_FONT_HI_REG",
}
_FONT_CACHE = {}


def _fc_match(query):
    fc = shutil.which("fc-match")
    if not fc:
        return None
    try:
        out = subprocess.run([fc, "-f", "%{file}\n", query],
                             capture_output=True, text=True, timeout=15)
    except Exception:
        return None
    lines = out.stdout.strip().splitlines()
    return lines[0] if lines else None


def _font_path(key):
    """Resolve one font file, lazily; fail loudly if none is usable."""
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    env = os.environ.get(_ENV_FONT[key])
    if env and pathlib.Path(env).is_file():
        path = env
    else:
        fc = _fc_match(_FC_QUERY[key])
        if fc and pathlib.Path(fc).is_file():
            path = fc
        elif pathlib.Path(_FALLBACK_FONTS[key]).is_file():
            path = _FALLBACK_FONTS[key]
        else:
            raise SystemExit(
                f"og font not found for {key}: tried env {_ENV_FONT[key]}, "
                f"fc-match '{_FC_QUERY[key]}', fallback {_FALLBACK_FONTS[key]}")
    _FONT_CACHE[key] = path
    return path


FOOTER = {
    "en-IN": "Free AI Tools in India \u2022 dusaitool.pages.dev",
    "hi": "\u092d\u093e\u0930\u0924 \u092e\u0947\u0902 \u092e\u0941\u092b\u094d\u0924 AI \u091f\u0942\u0932 \u2022 dusaitool.pages.dev",
}
RAQM = ImageFont.Layout.RAQM

# sampled from an existing Loop card: TL #112f50 TR #2b5980 BL #1c4b75 BR #2b5d88
CORNERS = {"tl": (0x11, 0x2F, 0x50), "tr": (0x2B, 0x59, 0x80),
           "bl": (0x1C, 0x4B, 0x75), "br": (0x2B, 0x5D, 0x88)}


def gradient():
    import numpy as np
    tl, tr, bl, br = (np.array(CORNERS[k], dtype=float) for k in ("tl", "tr", "bl", "br"))
    fx = np.linspace(0, 1, W)[None, :, None]
    fy = np.linspace(0, 1, H)[:, None, None]
    top = tl + (tr - tl) * fx
    bot = bl + (br - bl) * fx
    arr = (top + (bot - top) * fy).astype("uint8")
    return Image.fromarray(arr, "RGB")


def spark_points(cx, cy, r_out, r_in):
    pts = []
    for i in range(8):
        ang = -math.pi / 2 + i * math.pi / 4
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def _is_deva(word):
    return any("\u0900" <= ch <= "\u097f" for ch in word)


def _font(word, size, bold):
    key = ("hi_bold" if bold else "hi_reg") if _is_deva(word) else ("en_bold" if bold else "en_reg")
    return ImageFont.truetype(_font_path(key), size, layout_engine=RAQM)


def mixed_width(text, size, bold):
    words = text.split()
    if not words:
        return 0
    space = ImageFont.truetype(_font_path("en_bold" if bold else "en_reg"), size, layout_engine=RAQM).getlength(" ")
    return sum(_font(w, size, bold).getlength(w) for w in words) + space * (len(words) - 1)


def wrap_mixed(text, size, bold, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if mixed_width(trial, size, bold) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_mixed(d, x, y, text, size, bold, fill):
    space = ImageFont.truetype(_font_path("en_bold" if bold else "en_reg"), size, layout_engine=RAQM).getlength(" ")
    for w in text.split():
        f = _font(w, size, bold)
        d.text((x, y), w, font=f, fill=fill)
        x += f.getlength(w) + space


def render(title, footer, bold_path, reg_path):
    img = gradient().convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    # soft circles, top-right and bottom-right
    d.ellipse([1090 - 190, 30 - 190, 1090 + 190, 30 + 190], fill=(255, 255, 255, 16))
    d.ellipse([1095 - 150, 615 - 150, 1095 + 150, 615 + 150], fill=(110, 170, 230, 55))
    # frosted square
    d.rounded_rectangle([855, 140, 1145, 500], radius=26, fill=(255, 255, 255, 30),
                        outline=(255, 255, 255, 90), width=2)
    # orbit ring (rotated ellipse) + dot, echoing the Orbit Spark mark
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    rd = ImageDraw.Draw(ring)
    rd.ellipse([1000 - 130, 320 - 55, 1000 + 130, 320 + 55], outline=(255, 255, 255, 220), width=5)
    rd.ellipse([1000 + 118, 320 - 62, 1000 + 134, 320 - 46], fill=(255, 255, 255, 255))
    ring = ring.rotate(20, center=(1000, 320), resample=Image.BICUBIC)
    ov = Image.alpha_composite(ov, ring)
    d = ImageDraw.Draw(ov)
    # white spark
    d.polygon(spark_points(1000, 320, 105, 30), fill=(255, 255, 255, 255))
    img = Image.alpha_composite(img, ov)
    d = ImageDraw.Draw(img)
    # eyebrow, letter-spaced
    eb = ImageFont.truetype(_font_path("en_bold"), 30, layout_engine=RAQM)
    x = 80
    for ch in "DUS AI TOOL":
        d.text((x, 68), ch, font=eb, fill=(255, 255, 255, 255))
        x += d.textlength(ch, font=eb) + (14 if ch == " " else 7)
    d.rounded_rectangle([80, 122, 146, 128], radius=3, fill=(78, 167, 252, 255))
    # title, auto-fit to max 4 lines
    size = 62
    while size > 40:
        lines = wrap_mixed(title, size, True, 640)
        if len(lines) <= 4:
            break
        size -= 2
    lines = wrap_mixed(title, size, True, 640)
    y = 196
    for ln in lines:
        draw_mixed(d, 80, y, ln, size, True, (255, 255, 255, 255))
        y += int(size * 1.28)
    # footer
    draw_mixed(d, 80, 560, footer, 26, False, (207, 224, 240, 255))
    return img.convert("RGB")


def frontmatter(path):
    t = path.read_text(encoding="utf-8")
    m = re.match(r"---\s*\n(.*?)\n---", t, re.S)
    return m.group(1) if m else ""


def missing_articles():
    out = []
    for loc in ("en-IN", "hi"):
        for p in sorted((BASE / "src/content/blog" / loc).glob("*.md")):
            fm = frontmatter(p)
            if re.search(r"^ogImage:", fm, re.M):
                continue
            t = re.search(r"^title:\s*\"(.*)\"\s*$", fm, re.M)
            out.append((loc, p, t.group(1) if t else p.stem))
    return out


def patch_frontmatter(path, og_value):
    t = path.read_text(encoding="utf-8")
    m = re.match(r"(---\s*\n.*?\n)(---)", t, re.S)
    fm = m.group(1)
    line = f"ogImage: '{og_value}'\n"
    if re.search(r"^heroAlt:.*$", fm, re.M):
        fm2 = re.sub(r"^heroAlt:.*$", lambda mm: mm.group(0) + "\n" + line.rstrip("\n"), fm, count=1, flags=re.M)
    elif re.search(r"^verdict:.*$", fm, re.M):
        fm2 = re.sub(r"^verdict:.*$", lambda mm: mm.group(0) + "\n" + line.rstrip("\n"), fm, count=1, flags=re.M)
    else:
        fm2 = fm + line
    path.write_text(fm2 + m.group(2) + t[m.end():], encoding="utf-8")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "samples"
    miss = missing_articles()
    print(f"missing articles: {len(miss)}")
    if mode == "samples":
        sdir = pathlib.Path(__file__).with_name("samples")
        sdir.mkdir(exist_ok=True)
        picks = [miss[0], miss[1], miss[150], miss[151]]
        for loc, p, title in picks:
            bold = _font_path("en_bold" if loc == "en-IN" else "hi_bold")
            reg = _font_path("en_reg" if loc == "en-IN" else "hi_reg")
            img = render(title, FOOTER[loc], bold, reg)
            tag = "en" if loc == "en-IN" else "hi"
            img.save(sdir / f"{p.stem}-{tag}.jpg", quality=85)
            img.save(sdir / f"{p.stem}-{tag}.png", optimize=True)
            print("sample:", p.stem, "|", title[:60])
    elif mode == "all":
        if miss:
            for k in ("en_bold", "en_reg", "hi_bold", "hi_reg"):
                print(f"font {k}: {_font_path(k)}")
        for loc, p, title in miss:
            bold = _font_path("en_bold" if loc == "en-IN" else "hi_bold")
            reg = _font_path("en_reg" if loc == "en-IN" else "hi_reg")
            tag = "en" if loc == "en-IN" else "hi"
            out = OG / f"{p.stem}-{tag}.jpg"
            render(title, FOOTER[loc], bold, reg).save(out, quality=85)
            patch_frontmatter(p, f"/og/{p.stem}-{tag}.jpg")
        print(f"generated {len(miss)} images + patched {len(miss)} frontmatter files")
    else:
        print("unknown mode:", mode)
