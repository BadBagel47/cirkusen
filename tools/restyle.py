#!/usr/bin/env python3
"""Draft tool: redraws a poster's figures in a classic hand-drawn cartoon style (D-006).

It reads a poster page and writes a new page where every figure gets:
  - a body drawn from scratch: a pear-shaped torso, rubber-hose arms and legs,
    big white gloves and big bulbous shoes,
  - a newly drawn, large head with big oval eyes, a round nose and a clear expression,
  - soft volume shading (each flat fill becomes a light-to-dark gradient),
  - bolder, blacker outlines and a sheen along arms and legs.
The scene around them follows: a lit tent, an audience with eyes, a shaded ring
wall and floor, and a glossy title sign.

The figures are drawn for this poster (see FIGURES and the fig_* functions). They reuse
the original props by line number, so another poster needs its own entries there.

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
    out.append(SCENE_DEFS)
    out.append("</defs></svg>")
    return "".join(out)


# ---------------------------------------------------------------- the scene
# Gradients for the big background surfaces, in poster coordinates (1080 x 1620).
SCENE_DEFS = (
    '<radialGradient id="bg-glow" gradientUnits="userSpaceOnUse" cx="540" cy="560" r="760">'
    '<stop offset="0" stop-color="#FFD9A0" stop-opacity=".2"/><stop offset=".45" stop-color="#FFD9A0" stop-opacity="0"/>'
    '<stop offset="1" stop-color="#0B0514" stop-opacity=".62"/></radialGradient>'
    '<linearGradient id="bg-wall" gradientUnits="userSpaceOnUse" x1="0" y1="690" x2="0" y2="754">'
    '<stop offset="0" stop-color="#E9543F"/><stop offset=".45" stop-color="#C8322B"/><stop offset="1" stop-color="#84181A"/></linearGradient>'
    '<linearGradient id="bg-trim" gradientUnits="userSpaceOnUse" x1="0" y1="684" x2="0" y2="696">'
    '<stop offset="0" stop-color="#FFF0A0"/><stop offset=".5" stop-color="#FFD23F"/><stop offset="1" stop-color="#D08F17"/></linearGradient>'
    '<radialGradient id="bg-floor" gradientUnits="userSpaceOnUse" cx="540" cy="1140" r="900">'
    '<stop offset="0" stop-color="#F7DDA4"/><stop offset=".5" stop-color="#E3BE7E"/><stop offset="1" stop-color="#A97C43"/></radialGradient>'
    '<linearGradient id="bg-board" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#34204F"/><stop offset="1" stop-color="#0F0719"/></linearGradient>'
    '<linearGradient id="bg-title" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset=".15" stop-color="#FF9A62"/><stop offset=".5" stop-color="#FF4B3A"/><stop offset=".9" stop-color="#B8201F"/></linearGradient>'
)


def crowd(m):
    """An audience member: a shaded, outlined head. The two front rows get eyes that watch the ring."""
    tag = m.group(0)
    cx, cy, r = (float(attr(tag, k)) for k in ("cx", "cy", "r"))
    colour = attr(tag, "fill").upper()
    out = '<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="3"/>' % (num(cx), num(cy), num(r), gradient_for(colour), OUT)
    if colour != "#3B2A5A":
        look = max(-1, min(1, (540 - cx) / 400))
        for side in (-1, 1):
            ex, ey = cx + side * r * 0.3, cy - r * 0.3
            out += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" stroke="%s" stroke-width="2"/>' % (num(ex), num(ey), num(r * 0.22), num(r * 0.32), OUT)
            out += '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (num(ex + look * r * 0.08), num(ey + r * 0.1), num(r * 0.1), num(r * 0.16), OUT)
    return out


def restyle_scene(svg):
    def rep(old, new, count=1):
        nonlocal svg
        assert svg.count(old) >= 1, old[:60]
        svg = svg.replace(old, new, count)

    # Tent: warm glow in the middle, dark towards the edges.
    first_crowd = re.search(r'<circle [^>]*fill="#3B2A5A"[^>]*/>', svg).start()
    svg = svg[:first_crowd] + '<rect width="1080" height="700" fill="url(#bg-glow)"/>' + svg[first_crowd:]
    # Audience.
    svg = re.sub(r'<circle [^>]*fill="#(?:3B2A5A|4A3570|5A4488)"[^>]*/>', crowd, svg)
    # Ring wall with trim and stars.
    rep('<rect x="0" y="690" width="1080" height="64" fill="#C8322B"/>', '<rect x="0" y="690" width="1080" height="64" fill="url(#bg-wall)"/>')
    rep('<rect x="0" y="684" width="1080" height="12" fill="#FFD23F"/>',
        '<rect x="-6" y="684" width="1092" height="12" fill="url(#bg-trim)" stroke="%s" stroke-width="3.5"/>' % OUT)
    svg = re.sub(r'(<path d="M\d+ 712l4 9[^"]*" fill=")#FFD23F"', lambda m: m.group(1) + gradient_for("#FFD23F") + '" stroke="%s" stroke-width="2.6" stroke-linejoin="round"' % OUT, svg)
    # Floor: a pool of light in the middle of the ring.
    rep('<rect x="0" y="754" width="1080" height="866" fill="#E3BE7E"/>',
        '<rect x="0" y="754" width="1080" height="866" fill="url(#bg-floor)"/><path d="M0 754H1080" fill="none" stroke="%s" stroke-width="4"/>' % OUT)
    svg = svg.replace('fill="#8A6A3A" opacity=".35"', 'fill="#5E3F1F" opacity=".4"')
    # Marquee board, bulbs, title and ribbon.
    rep('fill="#170C26" stroke="#FFD23F" stroke-width="6"/>', 'fill="url(#bg-board)" stroke="#FFD23F" stroke-width="7"/>')
    board = re.search(r'<rect x="40" y="22" width="1000" height="232" rx="32"[^>]*/>', svg)
    svg = svg[: board.start()] + '<rect x="40" y="22" width="1000" height="232" rx="32" fill="none" stroke="%s" stroke-width="15"/>' % OUT + svg[board.start():]

    def bulb(m):
        tag = m.group(0).replace('stroke-width="2"', 'stroke-width="3"')
        return tag + '<circle cx="%s" cy="%s" r="2.6" fill="#fff" fill-opacity=".85"/>' % (num(float(attr(tag, "cx")) - 2.6), num(float(attr(tag, "cy")) - 2.8))

    svg = re.sub(r'<circle class="b[12]"[^>]*/>', bulb, svg)
    rep('fill="#FF4B3A" stroke="#2A1B3D" stroke-width="2" style="stroke:#2A1B3D"',
        'fill="url(#bg-title)" stroke="%s" stroke-width="7" stroke-linejoin="round" paint-order="stroke" style="stroke:%s"' % (OUT, OUT))
    rep('fill="#F6EFE0" stroke="#2A1B3D" stroke-width="4" stroke-linejoin="round"/>',
        'fill="%s" stroke="%s" stroke-width="5" stroke-linejoin="round"/>' % (gradient_for("#F6EFE0"), OUT))
    # Bunting.
    svg = re.sub(r'(<path class="flag"[^>]*fill=")(#[0-9A-Fa-f]{6})(" stroke="#2A1B3D" stroke-width=")2\.5',
                 lambda m: m.group(1) + gradient_for(m.group(2)) + m.group(3) + "3.6", svg)
    svg = svg.replace('fill="none" stroke="#F6EFE0" stroke-width="3"/>', 'fill="none" stroke="#F6EFE0" stroke-width="4"/>')
    return svg.replace('stroke="%s"' % OUTLINE_OLD, 'stroke="%s"' % OUT)


def restyle_page_chrome(page):
    """The date stamp gets a sheen and a hard cartoon shadow."""
    old = "background: #FFD23F; border: 4px dashed #2A1B3D;"
    assert old in page
    return page.replace(old, "background: linear-gradient(160deg, #FFF0A0, #FFD23F 45%%, #E8A91E); border: 4px dashed %s; box-shadow: 6px 7px 0 rgba(26, 15, 38, .55);" % OUT)


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


# ---------------------------------------------------------------- body kit
DARK = "#2A1B3D"


def limb(d, colour, w=18):
    """A rubber-hose arm or leg: outline, colour and a sheen along it."""
    return (
        '<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (d, OUT, num(w + 8))
        + '<path d="%s" fill="none" stroke="%s" stroke-width="%s"/>' % (d, colour, num(w))
        + '<path d="%s" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="%s"/>' % (d, num(w * 0.28))
    )


def glove(cx, cy, angle, g=20, kind="fist"):
    """A big white cartoon glove. 'fist' is a mitt that grips, 'open' has spread fingers."""
    n = lambda v: num(v * g)
    white = "#FFFFFF"
    out = ['<g transform="translate(%s %s) rotate(%s)" stroke-width="3.6">' % (num(cx), num(cy), num(angle))]
    out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (n(-1.6), n(-0.78), n(0.74), n(1.56), n(0.34), white))
    if kind == "open":
        for a in (-40, 0, 40):
            x, y = math.cos(math.radians(a)) * 1.3, math.sin(math.radians(a)) * 1.3
            out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(%s %s %s)"/>' % (n(x), n(y), n(0.7), n(0.4), white, a, n(x), n(y)))
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(-68 %s %s)"/>' % (n(-0.1), n(-1.05), n(0.56), n(0.36), white, n(-0.1), n(-1.05)))
        out.append('<circle r="%s" fill="%s"/>' % (n(1.0), white))
    else:
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(-24 %s %s)"/>' % (n(0.05), n(-0.92), n(0.52), n(0.4), white, n(0.05), n(-0.92)))
        out.append('<ellipse cx="%s" cy="0" rx="%s" ry="%s" fill="%s"/>' % (n(0.22), n(1.18), n(1.02), white))
        out.append('<path d="M%s %sQ%s %s %s %sM%s %sQ%s %s %s %s" fill="none" stroke-width="2.4"/>'
                   % (n(0.72), n(-0.3), n(1.1), n(-0.4), n(1.36), n(-0.3), n(0.72), n(0.3), n(1.1), n(0.4), n(1.36), n(0.3)))
    out.append('<path d="M%s %sh%sM%s 0h%sM%s %sh%s" fill="none" stroke-width="2.2"/>'
               % (n(-0.62), n(-0.36), n(0.44), n(-0.7), n(0.52), n(-0.62), n(0.36), n(0.44)))
    out.append("</g>")
    return "".join(out)


def shoe(cx, cy, s=22, colour=DARK, flip=False, angle=0):
    """A big bulbous shoe. (cx, cy) is the sole under the ankle, the toe points right unless flipped."""
    n = lambda v: num(v * s)
    d = ("M%s %s C%s %s %s %s %s %s C%s %s %s %s %s %s C%s %s %s %s %s %s L%s %s C%s %s %s %s %s %sZ" % tuple(n(v) for v in (
        -0.72, -0.5, -0.78, -1.0, 0.05, -1.02, 0.28, -0.6, 0.85, -1.08, 1.95, -0.72, 1.95, -0.02,
        1.95, 0.34, 1.55, 0.42, 1.0, 0.42, -0.5, 0.42, -0.98, 0.42, -0.95, -0.25, -0.72, -0.5)))
    return (
        '<g transform="translate(%s %s) rotate(%s) scale(%s 1)">' % (num(cx), num(cy), num(angle), -1 if flip else 1)
        + '<path d="%s" fill="%s"/>' % (d, colour)
        + '<path d="M%s %sQ%s %s %s %s" fill="none" stroke-width="2.4" stroke-opacity=".55"/>' % (n(-0.78), n(0.2), n(0.6), n(0.3), n(1.88), n(0.16))
        + '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" fill-opacity=".42" stroke="none" transform="rotate(-12 %s %s)"/>' % (n(1.22), n(-0.5), n(0.42), n(0.15), n(1.22), n(-0.5))
        + "</g>"
    )


def head(draw, cx, cy, k):
    """A head drawn at radius 50, scaled into place with an even outline width."""
    art = re.sub(r'stroke-width="([\d.]+)"', lambda m: 'stroke-width="%s"' % num(float(m.group(1)) / k), draw())
    return '<g transform="translate(%s %s) scale(%s)" stroke-width="%s">%s</g>' % (cx, cy, k, num(4.8 / k), art)


def body(d, colour):
    return '<path d="%s" fill="%s"/>' % (d, colour)


def moved(transform, markup):
    return '<g transform="%s">%s</g>' % (transform, markup)


# ---------------------------------------------------------------- the figures
# Each figure is drawn from scratch around its props. o(a, b) splices the original
# poster's lines a..b for that figure (props, signs and labels that carry the satire).

def fig_s(o):
    red = "#E8112D"
    return (
        o(1, 10)
        + limb("M130 314 Q124 350 116 382", "#F6EFE0", 24) + limb("M172 314 Q180 350 190 382", "#F6EFE0", 24)
        + shoe(110, 404, 27, DARK, flip=True) + shoe(196, 404, 27, DARK)
        + body("M98 184 Q150 160 202 184 Q240 252 226 314 Q150 344 74 314 Q60 252 98 184Z", red)
        + o(14, 17)
        + limb("M206 198 Q248 208 256 244", red, 20) + glove(258, 252, 78, 21)
        + limb("M94 198 Q52 198 50 162", red, 20) + glove(50, 150, -90, 21)
        + head(head_s, 150, 106, 1.16)
        + moved("translate(6 -24) translate(150 76) scale(1.08) translate(-150 -76)", o(28, 29))
    )


def fig_c(o):
    skin, green = "#F6D2B0", "#0E9F45"
    return (
        o(1, 9)
        + limb("M176 252 Q200 294 156 324", skin, 15) + limb("M144 252 Q138 300 168 332", skin, 15)
        + shoe(152, 336, 15, green, flip=True, angle=-25) + shoe(172, 346, 15, green, angle=20)
        + o(14)
        + body("M132 150 Q160 138 188 150 Q200 200 190 238 Q160 248 130 238 Q120 200 132 150Z", green)
        + o(16, 17)
        + limb("M134 162 Q104 172 88 198", skin, 13) + glove(84, 204, 125, 15, "open")
        + limb("M186 162 Q226 162 244 186", skin, 13) + glove(248, 192, 55, 15, "open")
        + o(22, 24)
        + head(head_c, 160, 90, 1.06)
        + o(37, 40)
    )


def fig_v(o):
    skin = "#EDBE94"
    return (
        o(1, 10)
        + limb("M134 262 Q128 286 122 300", skin, 22) + limb("M186 262 Q192 286 198 300", skin, 22)
        + shoe(114, 318, 22, DARK, flip=True) + shoe(206, 318, 22, DARK)
        + o(13)
        + body("M82 178 Q160 128 238 178 Q262 224 226 254 L94 254 Q58 224 82 178Z", skin)
        + body("M112 164 Q160 214 208 164 L224 254 L96 254Z", "#AF0B1E")
        + o(16, 17)
        + limb("M232 190 Q226 244 130 226", skin, 34) + limb("M88 190 Q98 240 194 218", skin, 34)
        + glove(202, 214, 190, 20) + glove(120, 226, -10, 20)
        + o(21, 23)
        + '<g class="no">' + head(head_v, 160, 94, 1.04) + "</g>"
    )


def fig_m(o):
    blue, navy = "#52BDEC", "#1F3A6B"
    return (
        o(1, 3)
        + limb("M166 332 Q122 348 102 386", navy, 18) + shoe(100, 400, 20, DARK, flip=True, angle=-38)
        + limb("M172 330 L172 394", navy, 18) + shoe(168, 410, 21, DARK)
        + o(8)
        + body("M138 234 Q170 220 202 234 Q222 290 212 334 Q170 352 128 334 Q118 290 138 234Z", blue)
        + o(10, 13)
        + limb("M144 246 Q94 266 72 210", blue, 16) + glove(72, 200, -100, 17)
        + limb("M196 246 Q246 266 268 210", blue, 16) + glove(268, 200, -80, 17)
        + head(head_m, 170, 190, 0.9)
        + o(27, 37)
    )


def fig_l(o):
    skin, blue = "#E8B48C", "#006AB3"
    return (
        o(1, 5)
        + '<g class="fly">' + o(7)
        + limb("M118 86 Q84 96 60 76", "#F6EFE0", 12) + limb("M116 72 Q84 70 64 50", "#F6EFE0", 12)
        + shoe(54, 70, 12, blue, flip=True, angle=35) + shoe(58, 44, 12, blue, flip=True, angle=45)
        + body("M106 64 Q160 38 206 54 Q220 72 206 90 Q160 106 108 96 Q94 80 106 64Z", blue)
        + o(11)
        + limb("M198 80 Q232 84 258 72", skin, 11) + limb("M196 62 Q226 46 252 32", skin, 11)
        + glove(262, 26, -30, 13, "open") + glove(268, 70, -8, 13, "open")
        + head(head_l, 222, 48, 0.62)
        + "</g>"
    )


def fig_kd(o):
    navy = "#1A2A7A"
    return (
        o(1, 3)
        + limb("M172 288 Q166 334 172 368", navy, 22) + shoe(172, 390, 24, DARK)
        + limb("M202 288 Q248 296 240 334", navy, 22) + shoe(240, 356, 23, DARK, angle=14)
        + body("M148 178 Q188 158 228 178 Q248 240 236 292 Q188 312 138 292 Q128 236 148 178Z", navy)
        + o(9, 11)
        + '<g class="beat">' + limb("M152 188 Q122 192 112 210", navy, 16)
        + '<path d="M110 214L86 196" fill="none" stroke="#8A5A2B" stroke-width="6"/><circle cx="82" cy="193" r="11" fill="#C8322B"/>'
        + glove(110, 214, 120, 17) + "</g>"
        + head(head_kd, 190, 114, 1.0)
        + o(16, 18)
        + limb("M220 190 Q254 182 246 150", navy, 16) + glove(246, 142, -95, 17)
        + moved("translate(0 -24) translate(190 96) scale(1.18) translate(-190 -96)", o(21, 24))
        + o(25)
    )


def fig_sd(o):
    suit = "#2B2B55"
    return (
        o(1, 2)
        + limb("M146 396 L142 444", suit, 18) + limb("M176 396 L180 444", suit, 18)
        + shoe(136, 460, 20, DARK, flip=True) + shoe(186, 460, 20, DARK)
        + body("M126 176 Q160 162 194 176 Q216 300 208 400 L112 400 Q104 300 126 176Z", suit)
        + o(6, 13)
        + limb("M128 188 Q84 218 58 176", suit, 16) + glove(56, 166, -110, 17)
        + o(16, 21)
        + limb("M192 188 Q240 214 260 254", suit, 16)
        + o(23) + glove(262, 262, 62, 17)
        + head(head_sd, 160, 116, 1.0)
        + moved("translate(0 -24) translate(160 84) scale(1.16) translate(-160 -84)", o(33, 34))
        + o(35, 36)
    )


def fig_t(o):
    purple = "#5B2A86"
    return (
        o(1, 2)
        + limb("M138 328 L132 390", "#F6EFE0", 24) + limb("M182 328 L190 390", "#F6EFE0", 24)
        + shoe(124, 412, 26, DARK, flip=True) + shoe(198, 412, 26, DARK)
        + o(5)
        + body("M110 192 Q160 168 210 192 Q252 264 228 332 Q160 358 92 332 Q68 264 110 192Z", purple)
        + o(7, 10)
        + limb("M112 208 Q80 204 94 168", purple, 19) + glove(96, 158, -80, 19)
        + o(12, 15)
        + limb("M208 208 Q238 210 244 228", purple, 19) + glove(246, 236, 75, 18)
        + head(head_t, 160, 120, 1.08)
        + moved("translate(0 -20) translate(160 90) scale(1.04) translate(-160 -90)", o(23, 24))
    )


def fig_mp(o):
    green = "#83CF39"
    return (
        o(1, 5)
        + limb("M126 200 Q154 218 138 238", "#F6EFE0", 15) + shoe(130, 256, 20, "#C8322B")
        + body("M96 126 Q132 106 168 128 Q182 172 168 208 Q130 224 94 208 Q82 166 96 126Z", green)
        + o(9, 10)
        + limb("M106 142 Q124 174 164 188", green, 14) + glove(172, 190, 15, 14)
        + limb("M160 138 Q196 142 210 152", green, 14) + glove(216, 152, 10, 14)
        + o(13)
        + moved("translate(128 78) scale(1.2) translate(-130 -84)", o(14))
        + head(head_mp, 128, 78, 0.82)
    )


FIGURES = {"S": fig_s, "C": fig_c, "V": fig_v, "M": fig_m, "L": fig_l, "KD": fig_kd, "SD": fig_sd, "T": fig_t, "MP": fig_mp}

# Plain text patches on the original lines before they are reused.
PATCHES = {
    "MP": [('<g transform="rotate(-4 213 36)">', '<g transform="translate(22 -8) rotate(-4 213 36)">'), ('<path d="M214 152V62"', '<path d="M216 152V52"')],
    "V": [(
        '<rect x="108" y="66" width="104" height="28" rx="6" fill="#2A1B3D"/><text x="160" y="86" text-anchor="middle" font-size="14" fill="#FFD23F">MINISTER</text>',
        '<path d="M124 96V10M196 96V10" fill="none" stroke="#2A1B3D" stroke-width="6"/><rect x="104" y="-16" width="112" height="30" rx="6" fill="#2A1B3D"/><text x="160" y="5" text-anchor="middle" font-size="15" fill="#FFD23F">MINISTER</text>',
    )],
}


def restyle_lines(content):
    """Shared treatment of the original artwork: limb sheen, bolder outlines."""

    def sheen(m):
        tag = m.group(0)
        w, stroke = attr(tag, "stroke-width"), attr(tag, "stroke")
        if attr(tag, "fill") == "none" and stroke and stroke.upper() != OUTLINE_OLD and w and float(w) >= 12:
            return tag + '<path d="%s" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="%s"/>' % (attr(tag, "d"), num(float(w) * 0.3))
        return tag

    content = re.sub(r"<path\b[^>]*/>", sheen, content)

    def strokes(m):
        tag = m.group(0)
        w = attr(tag, "stroke-width")
        if w:
            v = float(w)
            dark = (attr(tag, "stroke") or "").upper() == OUTLINE_OLD
            if v >= 12 and dark:
                v += 3
            elif v <= 8 and tag.startswith("<g"):
                v = 4.8
            elif v <= 8 and "stroke-opacity" not in tag:
                v *= 1.25
            tag = re.sub(r'stroke-width="[^"]*"', 'stroke-width="%s"' % num(v), tag, count=1)
        return tag

    return re.sub(r"<(?:g|path|rect|circle|ellipse|polygon|text)\b[^>]*>", strokes, content)


def restyle_figure(name, content):
    for old, new in PATCHES.get(name, []):
        assert old in content, (name, old[:40])
        content = content.replace(old, new)
    lines = [restyle_lines(l) for l in content.split("\n")]
    if name in FIGURES:
        o = lambda a, b=None: "\n".join(lines[a : (b if b is not None else a) + 1])
        content = lines[0] + "\n" + FIGURES[name](o) + "\n" + lines[-1]
    else:
        content = "\n".join(lines)
    content = shade(content)
    content = content.replace('stroke="%s"' % OUTLINE_OLD, 'stroke="%s"' % OUT)
    return content.replace("stroke:%s" % OUTLINE_OLD, "stroke:%s" % OUT)


def main(src, dst):
    page = open(src, encoding="utf-8").read()

    def figure(m):
        return m.group(1) + restyle_figure(m.group(2), m.group(3)) + "</button>"

    page, n = re.subn(r'(<button[^>]*data-act="(\w+)"[^>]*>)(.*?)</button>', figure, page, flags=re.S)
    scene = re.search(r'<svg aria-hidden="true" width="1080".*?</svg>', page, flags=re.S)
    page = page[: scene.start()] + restyle_scene(scene.group(0)) + page[scene.end():]
    page = restyle_page_chrome(page)
    page = page.replace('<div id="stage">', '<div id="stage">' + gradient_defs(), 1)
    open(dst, "w", encoding="utf-8").write(page)
    print("Restyled %d figures, %d gradients -> %s" % (n, len(gradients), dst))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
