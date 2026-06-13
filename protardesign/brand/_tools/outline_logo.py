"""
ProtarDesign ロゴ SVG のテキスト要素を Fraunces のグリフパスに置換する。
出力された *-outlined.svg はフォント未インストール環境でも同じ字形を保つ。
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.mutator import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

FRAUNCES_TTF = Path.home() / "Library/Fonts/Fraunces[SOFT,WONK,opsz,wght].ttf"
BRAND_DIR = Path(__file__).resolve().parent.parent

# (input, output, font-size を Fraunces の opsz にどう写すか)
JOBS = [
    ("logo-icon.svg",       "logo-icon-outlined.svg"),
    ("logo-icon-small.svg", "logo-icon-small-outlined.svg"),
]

def make_instance(weight: float, opsz: float):
    base = TTFont(FRAUNCES_TTF)
    return instantiateVariableFont(base, {"wght": weight, "opsz": opsz})

def text_to_path_group(text: str, x: float, y: float, font_size: float,
                       weight: float, letter_spacing: float, fill: str) -> str:
    # opsz は font-size に追従させる（Fraunces 推奨の運用）
    inst = make_instance(weight, opsz=max(9, min(144, font_size)))
    upm = inst["head"].unitsPerEm
    cmap = inst.getBestCmap()
    glyph_set = inst.getGlyphSet()
    hmtx = inst["hmtx"]
    os2 = inst["OS/2"]
    scale = font_size / upm
    # dominant-baseline=central: text の中心が y にくる
    # baseline_svg_y = y + (asc+desc)/2 * scale
    baseline_y = y + (os2.sTypoAscender + os2.sTypoDescender) / 2 * scale

    parts = []
    cur_x = x
    for ch in text:
        gname = cmap.get(ord(ch))
        if not gname:
            continue
        pen = SVGPathPen(glyph_set)
        glyph_set[gname].draw(pen)
        d = pen.getCommands()
        adv = hmtx[gname][0]
        if d:
            t = (f"translate({cur_x:.4f},{baseline_y:.4f}) "
                 f"scale({scale:.6f},{-scale:.6f})")
            parts.append(f'    <path d="{d}" transform="{t}" fill="{fill}"/>')
        cur_x += adv * scale + letter_spacing
    return "\n".join(parts)

TEXT_RE = re.compile(
    r'<text\b[^>]*\bx="([^"]+)"[^>]*\by="([^"]+)"[^>]*\bfont-weight="([^"]+)"'
    r'[^>]*\bfont-size="([^"]+)"[^>]*\bletter-spacing="([^"]+)"'
    r'[^>]*\bfill="([^"]+)"[^>]*>([^<]+)</text>',
    re.DOTALL,
)

def replace_text_with_path(svg: str) -> str:
    def repl(m: re.Match) -> str:
        x = float(m.group(1)); y = float(m.group(2))
        weight = float(m.group(3)); fs = float(m.group(4))
        ls = float(m.group(5)); fill = m.group(6)
        text = m.group(7)
        return f"<g data-orig-text=\"{text}\">\n" + text_to_path_group(
            text, x, y, fs, weight, ls, fill
        ) + "\n  </g>"
    return TEXT_RE.sub(repl, svg)

def strip_font_imports(svg: str) -> str:
    # Google Fonts @import や font-family CSS はもう不要
    svg = re.sub(r"@import\s+url\([^)]+\);?", "", svg)
    svg = re.sub(r"<defs>\s*<style>\s*</style>\s*</defs>", "<defs></defs>", svg)
    return svg

def main():
    if not FRAUNCES_TTF.exists():
        sys.exit(f"Fraunces font not found at {FRAUNCES_TTF}")
    for src, dst in JOBS:
        src_path = BRAND_DIR / src
        dst_path = BRAND_DIR / dst
        svg = src_path.read_text(encoding="utf-8")
        out = replace_text_with_path(svg)
        out = strip_font_imports(out)
        dst_path.write_text(out, encoding="utf-8")
        print(f"  {src}  ->  {dst}")

if __name__ == "__main__":
    main()
