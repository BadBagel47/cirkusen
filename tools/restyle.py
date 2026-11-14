#!/usr/bin/env python3
"""Draft tool: redraws a poster's figures in a classic hand-drawn cartoon style (D-006).

It reads a poster page and writes a new page where every figure gets:
  - a newly drawn, larger head with big oval eyes, a round nose and a clear expression,
  - soft volume shading (each flat fill becomes a light-to-dark gradient),
  - bolder, blacker outlines and a sheen along arms and legs,
  - large white cartoon gloves instead of plain hand circles, and glossy shoes.

The heads are drawn for this poster's figures (see FIGURES). A poster with other
figures needs its own entries there.

Usage (from the repo root):
  tools/restyle.py public/2026-11-14/index.html drafts/2026-11-14-v2/index.html

The output is a draft. Nothing under public/ is touched.
"""
import math
import re
import sys

OUTLINE_OLD = "#2A1B3D"
OUT = "#1A0F26"
FLAT = ' fill-opacity="1"'  # marks a shape that must keep its flat colour


# ---------------------------------------------------------------- face parts
# Heads are drawn around (0, 0) with a radius of 50 and then placed and scaled.

def eyes(gap=14, cy=-10, rx=12.5, ry=19, lx=0, ly=0, pr=1.0, cls=""):
    out = []
    for side in (-1, 1):
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff"%s stroke-width="3.2"/>' % (side * gap, cy, rx, ry, FLAT))
    out.append('<g%s>' % (' class="%s"' % cls if cls else ""))
    for side in (-1, 1):
        px, py = side * gap + lx, cy + 4 + ly
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"%s stroke="none"/>' % (px, py, 5.2 * pr, 8.6 * pr, OUT, FLAT))
        out.append('<circle cx="%s" cy="%s" r="%s" fill="#fff"%s stroke="none"/>' % (px - 1.7 * pr, py - 3.6 * pr, 2.2 * pr, FLAT))
    out.append("</g>")
    return "".join(out)


def nose(colour, y=12, rx=8.5, ry=6.5):
    return (
        '<ellipse cx="0" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (y, rx, ry, colour)
        + '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" fill-opacity=".6" stroke="none"/>' % (-rx * 0.3, y - ry * 0.35, rx * 0.36, ry * 0.26)
    )


def cheeks(y=18, x=31, r=8.5):
    return "".join('<circle cx="%s" cy="%s" r="%s" fill="#F4908C" fill-opacity=".55" stroke="none"/>' % (s * x, y, r) for s in (-1, 1))


def ears(skin, x=48, y=4, r=10):
    return "".join('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (s * x, y, r, skin) for s in (-1, 1))


def line(d, w=4.8, colour=OUT):
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (d, colour, w)


def drip(x, y, delay=None):
    style = ' style="animation-delay:%s"' % delay if delay else ""
    return '<path class="drip"%s d="M%s %sq7 13 0 19q-7 -6 0 -19z" fill="#7FD3FF"/>' % (style, x, y)


GRIN = (
    '<path d="M-27 22 Q0 32 27 22 Q24 49 0 50 Q-24 49 -27 22Z" fill="#6E1423"%s/>' % FLAT
    + '<path d="M-13 43 Q0 33 13 43 Q8 49 0 49 Q-8 49 -13 43Z" fill="#F2788C"%s stroke="none"/>' % FLAT
    + '<path d="M-24 24 Q0 33 24 24 L21 30 Q0 38 -21 30Z" fill="#fff"%s stroke-width="2.4"/>' % FLAT
)


def head_s():
    skin, hair = "#F3C9A5", "#6B4226"
    return (
        '<path d="M-58 6 Q-64 -60 0 -62 Q64 -60 58 6 Q60 36 42 46 L-42 46 Q-60 36 -58 6Z" fill="%s"/>' % hair
        + '<circle r="50" fill="%s"/>' % skin
        + '<path d="M-49 -8 Q-50 -54 0 -54 Q50 -54 49 -8 Q34 -37 4 -35 Q-6 -24 -22 -31 Q-40 -30 -49 -8Z" fill="%s"/>' % hair
        + line("M-28 -34q10 -8 20 -3M8 -37q10 -5 20 3")
        + eyes(cy=-8, ry=17)
        + cheeks()
        + nose("#EBA98A")
        + GRIN
    )


def head_c():
    skin, hair = "#F6D2B0", "#B5462F"
    lens = "M-41 -8 Q-38 -27 -19 -25 Q-2 -23 -3 -6 Q-5 11 -23 11 Q-41 9 -41 -8Z"
    lens_r = "M41 -8 Q38 -27 19 -25 Q2 -23 3 -6 Q5 11 23 11 Q41 9 41 -8Z"
    pupils = "".join(
        '<ellipse cx="%s" cy="-5" rx="5" ry="8" fill="%s"%s stroke="none"/><circle cx="%s" cy="-8.5" r="2.1" fill="#fff"%s stroke="none"/>' % (x, OUT, FLAT, x - 1.7, FLAT)
        for x in (-21, 21)
    )
    return (
        '<circle cx="0" cy="-68" r="27" fill="%s"/>' % hair
        + '<circle r="50" fill="%s"/>' % skin
        + '<path d="M-50 2 Q-57 -57 0 -57 Q57 -57 50 2 Q40 -34 0 -34 Q-40 -34 -50 2Z" fill="%s"/>' % hair
        + '<circle cx="-50" cy="18" r="6.5" fill="#0E9F45"/><circle cx="50" cy="18" r="6.5" fill="#0E9F45"/>'
        + '<path d="%s" fill="#fff"%s stroke-width="5.5"/><path d="%s" fill="#fff"%s stroke-width="5.5"/>' % (lens, FLAT, lens_r, FLAT)
        + line("M-41 -12l-12 -10M41 -12l12 -10", 5)
        + '<g class="eyes">%s</g>' % pupils
        + line("M-36 -37q12 -10 26 -4M10 -41q14 -6 26 4")
        + cheeks(22, 30, 8)
        + nose("#EDB79A", 15, 6, 5)
        + '<ellipse cx="0" cy="32" rx="9" ry="7" fill="#C8322B"/><ellipse cx="0" cy="32" rx="4" ry="3.2" fill="#6E1423"%s stroke="none"/>' % FLAT
        + drip(57, -44)
    )


def head_v():
    skin = "#EDBE94"
    return (
        ears(skin, 49, 4, 11)
        + '<circle r="50" fill="%s"/>' % skin
        + line("M0 -50q-14 -18 3 -24q14 2 6 14")
        + line("M-37 -25l28 10M37 -25l-28 10", 8.5)
        + line("M-29 -5q10 9 21 0M8 -5q10 9 21 0", 5)
        + cheeks(16, 33, 8)
        + nose("#DFA07C", 9, 13, 10)
        + '<path d="M0 24 Q-25 8 -50 27 Q-61 38 -72 24 Q-70 55 -36 44 Q-14 38 0 31 Q14 38 36 44 Q70 55 72 24 Q61 38 50 27 Q25 8 0 24Z" fill="#2A1B3D"/>'
        + line("M-13 45q13 -7 26 0")
    )


def head_m():
    skin = "#F3C9A5"
    teeth = '<rect x="-23" y="25" width="46" height="16" rx="7.5" fill="#fff"%s/>' % FLAT + line("M-11.5 25v16M0 25v16M11.5 25v16M-23 33h46", 2.4)
    return (
        ears(skin, 45, 6, 9)
        + '<ellipse rx="46" ry="50" fill="%s"/>' % skin
        + '<path d="M-45 -12 Q-42 -58 8 -55 Q49 -51 45 -8 Q28 -35 0 -33 Q-26 -33 -45 -12Z" fill="#D9B45A"/>'
        + line("M-35 -29l18 -9M35 -29l-18 -9", 5)
        + eyes(gap=14.5, cy=-6, rx=13.5, ry=18, pr=0.6)
        + nose("#EBA98A", 15, 7, 5.5)
        + teeth
        + drip(54, -26)
        + drip(-60, -10, ".5s")
    )


def head_l():
    skin = "#E8B48C"
    return (
        '<circle r="50" fill="%s"/>' % skin
        + '<path d="M-47 -14 Q-47 -59 4 -57 Q43 -55 50 -18 Q24 -37 -4 -33 Q-28 -33 -47 -14Z" fill="#2B2B55"/>'
        + line("M-47 -14 Q0 -37 50 -18", 13)
        + line("M-47 -14 Q0 -37 50 -18", 7, "#FFD23F")
        + line("M-31 -23l21 7M31 -23l-21 7", 6)
        + eyes(gap=14, cy=-2, rx=12, ry=15, ly=2)
        + nose("#DDA076", 17, 7, 5.5)
        + line("M-18 33q9 -8 18 0q9 8 18 0", 5.5)
        + drip(-64, -62)
    )


def head_kd():
    skin = "#F4CFAE"
    return (
        '<circle cx="-48" cy="6" r="10" fill="%s"/>' % skin
        + '<circle r="50" fill="%s"/>' % skin
        + '<circle cx="-30" cy="18" r="8" fill="#F4908C" fill-opacity=".55" stroke="none"/>'
        + '<circle cx="32" cy="17" r="18" fill="#F4A6A0"/>'
        + '<ellipse cx="26" cy="10" rx="6" ry="3.5" fill="#fff" fill-opacity=".6" stroke="none" transform="rotate(-30 26 10)"/>'
        + line("M-29 -8q11 -13 22 0M7 -10q11 -13 22 0", 5.4)
        + line("M-30 -27q12 -8 23 -3M7 -30q12 -6 23 2")
        + nose("#EBB08F", 6, 7.5, 6)
    )


def head_sd():
    skin, hair = "#F1D0B0", "#3B2A20"
    eye = "".join(
        '<ellipse cx="%s" cy="-6" rx="11.5" ry="7.5" fill="#fff"%s stroke-width="3.2"/>' % (x, FLAT)
        + '<ellipse cx="%s" cy="-5.5" rx="4.4" ry="5.6" fill="%s"%s stroke="none"/><circle cx="%s" cy="-8" r="1.7" fill="#fff"%s stroke="none"/>' % (x + 3.5, OUT, FLAT, x + 2.2, FLAT)
        + line("M%s -12 Q%s -17 %s -10" % (x - 12, x, x + 12), 5)
        for x in (-17, 17)
    )
    return (
        ears(skin, 41, 2, 8)
        + '<ellipse rx="42" ry="50" fill="%s"/>' % skin
        + '<path d="M-41 -12 Q-39 -57 0 -57 Q41 -57 41 -12 Q22 -37 0 -35 Q-22 -37 -41 -12Z" fill="%s"/>' % hair
        + '<path d="M-12 41 Q0 72 12 41 Q0 49 -12 41Z" fill="%s"/>' % hair
        + eye
        + line("M-31 -23q12 -7 24 -1M7 -28q12 -9 24 3")
        + nose("#E3B291", 10, 6.5, 8)
        + line("M-21 28Q0 20 21 28", 6, hair)
        + line("M-12 37Q6 45 21 32")
    )


def head_t():
    skin = "#F2CBA8"
    curl = "M0 15 Q-35 -3 -60 17 Q-75 29 -62 39 Q-52 42 -55 32"
    curl_r = "M0 15 Q35 -3 60 17 Q75 29 62 39 Q52 42 55 32"
    return (
        ears(skin, 49, 2, 10)
        + '<circle r="50" fill="%s"/>' % skin
        + '<ellipse cx="-6" cy="35" rx="15" ry="12.5" fill="#7A1E1E"%s/>' % FLAT
        + '<path d="M-16 39 Q-6 31 4 39 Q-2 46 -6 46 Q-11 46 -16 39Z" fill="#F2788C"%s stroke="none"/>' % FLAT
        + line("M-37 -29l22 5M37 -31l-22 7", 7)
        + eyes(gap=17, cy=-9, rx=11, ry=15)
        + '<circle cx="17" cy="-8" r="19.5" fill="#fff" fill-opacity=".22" stroke="#E3B23C" stroke-width="5"/>'
        + line("M33 4q12 26 2 56", 2.6, "#E3B23C")
        + nose("#E8A688", 9, 10, 8)
        + line(curl, 9.5) + line(curl_r, 9.5)
    )


def head_mp():
    skin = "#F6D2B0"
    return (
        '<circle r="50" fill="%s"/>' % skin
        + line("M-33 -39q12 -10 22 -4M11 -43q12 -6 22 4")
        + eyes(gap=14, cy=-10, rx=12.5, ry=18.5)
        + cheeks(20, 32, 9)
        + '<circle cx="0" cy="14" r="11.5" fill="#C8322B"/><ellipse cx="-3.5" cy="10" rx="4" ry="2.6" fill="#fff" fill-opacity=".65" stroke="none"/>'
        + '<path d="M-24 28 Q0 40 24 28 Q20 48 0 48 Q-20 48 -24 28Z" fill="#6E1423"%s/>' % FLAT
        + '<path d="M-11 42 Q0 34 11 42 Q6 47 0 47 Q-6 47 -11 42Z" fill="#F2788C"%s stroke="none"/>' % FLAT
    )


# Per figure: old head lines to drop, where the new head goes (centre and scale),
# lines to move with it (hats, hair), and plain text patches.
FIGURES = {
    "C": dict(drop=(25, 36), head=(head_c, 160, 92, 1.0)),
    "V": dict(
        drop=(25, 32), head=(head_v, 160, 98, 0.9),
        patch=[(
            '<rect x="108" y="66" width="104" height="28" rx="6" fill="#2A1B3D"/><text x="160" y="86" text-anchor="middle" font-size="14" fill="#FFD23F">MINISTER</text>',
            '<path d="M124 96V40M196 96V40" fill="none" stroke="#2A1B3D" stroke-width="6"/><rect x="104" y="16" width="112" height="30" rx="6" fill="#2A1B3D"/><text x="160" y="37" text-anchor="middle" font-size="15" fill="#FFD23F">MINISTER</text>',
        )],
    ),
    "S": dict(drop=(22, 27), head=(head_s, 150, 112, 1.08), wrap=[(28, 29, "translate(0 -20) translate(150 76) scale(1.15) translate(-150 -76)")]),
    "M": dict(drop=(18, 26), head=(head_m, 170, 192, 0.84)),
    "L": dict(drop=(14, 20), head=(head_l, 221, 49, 0.56)),
    "KD": dict(drop=(13, 15), head=(head_kd, 190, 116, 0.94), wrap=[(21, 24, "translate(0 -19) translate(190 96) scale(1.15) translate(-190 -96)")]),
    "SD": dict(drop=(25, 32), head=(head_sd, 160, 120, 0.9), wrap=[(33, 34, "translate(0 -17) translate(160 84) scale(1.12) translate(-160 -84)")]),
    "T": dict(drop=(17, 22), head=(head_t, 160, 124, 1.0), wrap=[(23, 24, "translate(0 -9) translate(160 90) scale(1.15) translate(-160 -90)")]),
    "MP": dict(drop=(15, 20), head=(head_mp, 130, 78, 0.84), wrap=[(14, 14, "translate(130 78) scale(1.22) translate(-130 -84)")]),
}

# Hand circles to turn into gloves, per figure: (cx, cy) -> optional fixed angle in degrees.
HANDS = {
    "C": {(86, 202): 150, (246, 190): 30},
    "V": {(200, 212): 200, (122, 222): -20},
    "S": {(258, 252): None, (50, 152): None},
    "M": {(72, 202): None, (268, 202): None},
    "L": {(258, 28): -35, (264, 69): 25},
    "KD": {(110, 214): None, (246, 142): None},
    "SD": {(56, 168): None, (262, 262): None},
    "T": {(97, 160): None, (264, 248): None},
    "MP": {(170, 189): None, (214, 152): None},
}

gradients = {}


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def rgb_to_hex(c):
    return "#%02X%02X%02X" % c


def gradient_for(colour):
    rgb = hex_to_rgb(colour)
    key = "%02X%02X%02X" % rgb
    if key not in gradients:
        lum = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
        if lum > 235:  # whites: keep them white, shade towards a cool grey
            stops = [(0, (255, 255, 255)), (0.55, (255, 255, 255)), (1, (200, 208, 230))]
        elif lum < 45:  # darks: add a visible sheen
            stops = [(0, mix(rgb, (255, 255, 255), 0.42)), (0.4, rgb), (1, mix(rgb, (0, 0, 0), 0.4))]
        else:
            stops = [(0, mix(rgb, (255, 255, 255), 0.36)), (0.42, rgb), (1, mix(rgb, hex_to_rgb(OUT), 0.34))]
        gradients[key] = stops
    return "url(#g-%s)" % key


def gradient_defs():
    out = ['<svg aria-hidden="true" width="0" height="0" style="position:absolute"><defs>']
    for key, stops in sorted(gradients.items()):
        out.append('<radialGradient id="g-%s" cx=".34" cy=".26" r=".95">' % key)
        out.extend('<stop offset="%s" stop-color="%s"/>' % (o, rgb_to_hex(c)) for o, c in stops)
        out.append("</radialGradient>")
    out.append("</defs></svg>")
    return "".join(out)


def num(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def attr(tag, name):
    m = re.search(r'\b%s="([^"]*)"' % name, tag)
    return m.group(1) if m else None


def shade(markup):
    """Volume shading: flat fills become gradients (shapes with fill-opacity stay flat)."""

    def one(m):
        tag = m.group(0)
        if "fill-opacity" in tag:
            return tag
        return re.sub(r'\bfill="(#[0-9A-Fa-f]{3,6})"', lambda f: 'fill="%s"' % gradient_for(f.group(1)), tag, count=1)

    return re.sub(r"<(?:path|rect|circle|ellipse|polygon)\b[^>]*>", one, markup)


def glove(cx, cy, r, angle):
    """A white cartoon mitt: cuff, thumb, palm, two finger seams and three darts."""
    g = min(max(r * 1.5, 12), 19)
    fill = gradient_for("#FFFFFF")
    n = lambda v: num(v * g)
    return "".join([
        '<g transform="translate(%s %s) rotate(%s)" stroke-width="3.4">' % (num(cx), num(cy), num(angle)),
        '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (n(-1.5), n(-0.8), n(0.72), n(1.6), n(0.34), fill),
        '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(-24 %s %s)"/>' % (n(0.05), n(-0.92), n(0.52), n(0.4), fill, n(0.05), n(-0.92)),
        '<ellipse cx="%s" cy="0" rx="%s" ry="%s" fill="%s"/>' % (n(0.22), n(1.18), n(1.02), fill),
        '<path d="M%s %sQ%s %s %s %sM%s %sQ%s %s %s %s" fill="none" stroke-width="2.4"/>'
        % (n(0.72), n(-0.3), n(1.1), n(-0.4), n(1.36), n(-0.3), n(0.72), n(0.3), n(1.1), n(0.4), n(1.36), n(0.3)),
        '<path d="M%s %sh%sM%s 0h%sM%s %sh%s" fill="none" stroke-width="2.2"/>'
        % (n(-0.62), n(-0.36), n(0.44), n(-0.7), n(0.52), n(-0.62), n(0.36), n(0.44)),
        "</g>",
    ])


def arm_angle(content, pos, cx, cy, vb_center):
    """Angle of the arm ending at this hand, from the last path before it."""
    paths = list(re.finditer(r'\bd="([^"]*)"', content[:pos]))
    if paths:
        d = paths[-1].group(1)
        if not re.search(r"[a-z]", d.replace("Z", "").replace("z", "")):
            pts = re.findall(r"(-?\d+(?:\.\d+)?)[ ,]+(-?\d+(?:\.\d+)?)", d)
            if len(pts) >= 2:
                (x1, y1), (x2, y2) = [(float(a), float(b)) for a, b in pts[-2:]]
                if math.hypot(x2 - cx, y2 - cy) < 14 and (x1, y1) != (x2, y2):
                    return math.degrees(math.atan2(y2 - y1, x2 - x1))
    return math.degrees(math.atan2(cy - vb_center[1], cx - vb_center[0]))


def restyle_figure(name, content):
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', content)
    center = (int(vb.group(1)) / 2, int(vb.group(2)) / 2)
    cfg = FIGURES.get(name, {})

    # 0. Swap the old head for a placeholder and move hats and hair along with the new head.
    for old, new in cfg.get("patch", []):
        assert old in content, (name, old[:40])
        content = content.replace(old, new)
    lines = content.split("\n")
    for a, b, transform in cfg.get("wrap", []):
        lines[a] = '<g transform="%s">' % transform + lines[a]
        lines[b] = lines[b] + "</g>"
    if "drop" in cfg:
        a, b = cfg["drop"]
        lines[a : b + 1] = ["<!--HEAD-->"]
    content = "\n".join(lines)

    # 1. Sheen along coloured limbs (thick, unfilled, non-outline strokes).
    def sheen(m):
        tag = m.group(0)
        w, stroke = attr(tag, "stroke-width"), attr(tag, "stroke")
        if attr(tag, "fill") == "none" and stroke and stroke.upper() != OUTLINE_OLD and w and float(w) >= 12:
            hl = '<path d="%s" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="%s"/>' % (attr(tag, "d"), num(float(w) * 0.3))
            return tag + hl
        return tag

    content = re.sub(r"<path\b[^>]*/>", sheen, content)

    # 2. Gloves and shoes (matched on the original coordinates).
    def shapes(m):
        tag = m.group(0)
        kind = m.group(1)
        cx, cy = attr(tag, "cx"), attr(tag, "cy")
        if cx is None:
            return tag
        key = (float(cx), float(cy))
        fill = (attr(tag, "fill") or "").upper()
        if kind == "circle" and key in HANDS.get(name, {}):
            fixed = HANDS[name][key]
            angle = fixed if fixed is not None else arm_angle(content, m.start(), key[0], key[1], center)
            return glove(key[0], key[1], float(attr(tag, "r")), angle)
        if kind == "ellipse" and fill == OUTLINE_OLD and attr(tag, "rx") and 17 <= float(attr(tag, "rx")) <= 26 and float(attr(tag, "ry")) <= 11:
            rx, ry = float(attr(tag, "rx")), float(attr(tag, "ry"))
            rot = attr(tag, "transform")
            rot = ' transform="%s"' % rot if rot else ""
            return (
                '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"%s/>' % (cx, num(key[1] - ry * 0.35), num(rx * 1.3), num(ry * 1.75), OUTLINE_OLD, rot)
                + '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" fill-opacity=".38" stroke="none"%s/>'
                % (num(key[0] - rx * 0.3), num(key[1] - ry * 1.05), num(rx * 0.5), num(ry * 0.38), rot)
            )
        return tag

    content = re.sub(r"<(circle|ellipse)\b[^>]*/>", shapes, content)

    # 3. Outlines: bolder and blacker.
    def strokes(m):
        tag = m.group(0)
        w = attr(tag, "stroke-width")
        if w:
            v = float(w)
            dark = (attr(tag, "stroke") or "").upper() == OUTLINE_OLD
            if v >= 12 and dark:
                v += 3
            elif v <= 8 and tag.startswith("<g") and "translate" not in tag:
                v = 4.8
            elif v <= 8 and "stroke-opacity" not in tag and "translate" not in tag:
                v *= 1.25
            tag = re.sub(r'stroke-width="[^"]*"', 'stroke-width="%s"' % num(v), tag, count=1)
        return tag

    content = re.sub(r"<(?:g|path|rect|circle|ellipse|polygon|text)\b[^>]*>", strokes, content)

    # 4. Volume shading on flat fills.
    content = shade(content)
    content = content.replace('stroke="%s"' % OUTLINE_OLD, 'stroke="%s"' % OUT)
    content = content.replace("stroke:%s" % OUTLINE_OLD, "stroke:%s" % OUT)

    # 5. The new head, drawn at radius 50 and scaled into place with an even outline width.
    if "head" in cfg:
        draw, cx, cy, k = cfg["head"]
        art = shade(draw())
        art = re.sub(r'stroke-width="([\d.]+)"', lambda m: 'stroke-width="%s"' % num(float(m.group(1)) / k), art)
        head = '<g transform="translate(%s %s) scale(%s)" stroke-width="%s">%s</g>' % (cx, cy, k, num(4.8 / k), art)
        assert "<!--HEAD-->" in content, name
        content = content.replace("<!--HEAD-->", head)
    return content


def main(src, dst):
    page = open(src, encoding="utf-8").read()

    def figure(m):
        return m.group(1) + restyle_figure(m.group(2), m.group(3)) + "</button>"

    page, n = re.subn(r'(<button[^>]*data-act="(\w+)"[^>]*>)(.*?)</button>', figure, page, flags=re.S)
    page = page.replace('<div id="stage">', '<div id="stage">' + gradient_defs(), 1)
    open(dst, "w", encoding="utf-8").write(page)
    print("Restyled %d figures, %d gradients -> %s" % (n, len(gradients), dst))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
