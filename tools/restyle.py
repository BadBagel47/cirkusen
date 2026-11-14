#!/usr/bin/env python3
"""Draft tool: restyles a poster's figures towards a classic hand-drawn cartoon look.

It reads a poster page and writes a new page where every figure gets:
  - soft volume shading (each flat fill becomes a light-to-dark gradient),
  - bolder, blacker outlines and a sheen along arms and legs,
  - white cartoon gloves instead of plain hand circles,
  - taller eyes with oval pupils and a glint, and glossy shoes.

Usage (from the repo root):
  tools/restyle.py public/2026-11-14/index.html drafts/2026-11-14-v2/index.html

The output is a draft. Nothing under public/ is touched.
"""
import math
import re
import sys

OUTLINE_OLD = "#2A1B3D"
OUTLINE_NEW = "#1A0F26"

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
# Eye whites to make taller, per figure.
EYE_WHITES = {
    "M": [(158, 186), (182, 186)],
    "L": [(212, 52), (228, 52)],
    "MP": [(118, 78), (142, 78)],
}
# Pupils to turn into ovals with a glint, per figure: (cx, cy) -> stretch factor.
PUPILS = {
    "M": {(161, 181): 1.0, (179, 181): 1.0},
    "L": {(213, 55): 1.0, (229, 55): 1.0},
    "MP": {(121, 75): 1.0, (145, 75): 1.0},
    "C": {(142, 99): 0.8, (178, 99): 0.8},
    "T": {(144, 122): 0.8, (176, 124): 0.8},
    "SD": {(151, 121): 0.6, (175, 121): 0.6},
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


def gradient_for(color):
    rgb = hex_to_rgb(color)
    key = "%02X%02X%02X" % rgb
    if key not in gradients:
        lum = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
        if lum > 235:  # whites: keep them white, shade towards a cool grey
            stops = [(0, (255, 255, 255)), (0.55, (255, 255, 255)), (1, (200, 208, 230))]
        elif lum < 45:  # darks: add a visible sheen
            stops = [(0, mix(rgb, (255, 255, 255), 0.42)), (0.4, rgb), (1, mix(rgb, (0, 0, 0), 0.4))]
        else:
            stops = [
                (0, mix(rgb, (255, 255, 255), 0.36)),
                (0.42, rgb),
                (1, mix(rgb, hex_to_rgb(OUTLINE_NEW), 0.34)),
            ]
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


def glove(cx, cy, r, angle):
    g = max(r * 1.3, 13)
    fill = gradient_for("#FFFFFF")
    c = lambda x, y, rad: '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (num(x * g), num(y * g), num(rad * g), fill)
    parts = [
        '<g transform="translate(%s %s) rotate(%s)" stroke-width="3">' % (num(cx), num(cy), num(angle)),
        '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>'
        % (num(-1.5 * g), num(-0.86 * g), num(0.7 * g), num(1.72 * g), num(0.32 * g), fill),
        c(1.02, -0.74, 0.52),
        c(1.36, 0, 0.56),
        c(1.02, 0.74, 0.52),
        c(0.05, -1.1, 0.46),
        c(0.1, 0, 1.08),
        '<path d="M%s %sh%sM%s 0h%sM%s %sh%s" fill="none" stroke-width="2"/>'
        % (num(-0.42 * g), num(-0.4 * g), num(0.6 * g), num(-0.5 * g), num(0.7 * g), num(-0.42 * g), num(0.4 * g), num(0.6 * g)),
        "</g>",
    ]
    return "".join(parts)


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

    # 1. Sheen along coloured limbs (thick, unfilled, non-outline strokes).
    def sheen(m):
        tag = m.group(0)
        w, stroke = attr(tag, "stroke-width"), attr(tag, "stroke")
        if attr(tag, "fill") == "none" and stroke and stroke.upper() != OUTLINE_OLD and w and float(w) >= 12:
            hl = '<path d="%s" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="%s"/>' % (attr(tag, "d"), num(float(w) * 0.3))
            return tag + hl
        return tag

    content = re.sub(r"<path\b[^>]*/>", sheen, content)

    # 2. Gloves, eyes, pupils and shoes (matched on the original coordinates).
    def shapes(m):
        tag = m.group(0)
        kind = m.group(1)
        cx, cy = attr(tag, "cx"), attr(tag, "cy")
        if cx is None or "transform" in tag:
            return tag
        key = (float(cx), float(cy))
        fill = (attr(tag, "fill") or "").upper()
        if kind == "circle" and key in HANDS.get(name, {}):
            fixed = HANDS[name][key]
            angle = fixed if fixed is not None else arm_angle(content, m.start(), key[0], key[1], center)
            return glove(key[0], key[1], float(attr(tag, "r")), angle)
        if key in EYE_WHITES.get(name, []):
            rx = float(attr(tag, "rx") or attr(tag, "r"))
            ry = float(attr(tag, "ry") or attr(tag, "r"))
            return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" stroke-width="3"/>' % (cx, num(key[1] - ry * 0.15), num(rx * 1.18), num(ry * 1.45))
        if kind == "circle" and key in PUPILS.get(name, {}) and float(attr(tag, "r")) <= 5:
            r, k = float(attr(tag, "r")), PUPILS[name][key]
            rx, ry = r * (1 + 0.2 * k), r * (1 + 0.8 * k)
            return (
                '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" stroke="none"/>' % (cx, cy, num(rx), num(ry), OUTLINE_NEW)
                + '<circle cx="%s" cy="%s" r="%s" fill="#fff" stroke="none"/>' % (num(key[0] - rx * 0.3), num(key[1] - ry * 0.45), num(r * 0.42))
            )
        if kind == "ellipse" and fill == OUTLINE_OLD and attr(tag, "rx") and 17 <= float(attr(tag, "rx")) <= 26 and float(attr(tag, "ry")) <= 11:
            rx, ry = float(attr(tag, "rx")), float(attr(tag, "ry"))
            return (
                '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"/>' % (cx, num(key[1] - ry * 0.25), num(rx * 1.22), num(ry * 1.5), OUTLINE_OLD)
                + '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" fill-opacity=".38" stroke="none"/>'
                % (num(key[0] - rx * 0.3), num(key[1] - ry * 0.85), num(rx * 0.5), num(ry * 0.36))
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
            elif v <= 8 and tag.startswith("<g"):
                v = 4.8
            elif v <= 8 and "stroke-opacity" not in tag:
                v *= 1.25
            tag = re.sub(r'stroke-width="[^"]*"', 'stroke-width="%s"' % num(v), tag, count=1)
        return tag

    content = re.sub(r"<(?:g|path|rect|circle|ellipse|polygon|text)\b[^>]*>", strokes, content)

    # 4. Volume shading on flat fills.
    def shade(m):
        tag = m.group(0)
        if "fill-opacity" in tag:
            return tag
        return re.sub(r'\bfill="(#[0-9A-Fa-f]{3,6})"', lambda f: 'fill="%s"' % gradient_for(f.group(1)), tag, count=1)

    content = re.sub(r"<(?:path|rect|circle|ellipse|polygon)\b[^>]*>", shade, content)

    content = content.replace('stroke="%s"' % OUTLINE_OLD, 'stroke="%s"' % OUTLINE_NEW)
    content = content.replace("stroke:%s" % OUTLINE_OLD, "stroke:%s" % OUTLINE_NEW)
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
