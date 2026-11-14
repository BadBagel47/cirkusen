#!/usr/bin/env python3
"""Draft tool (D-006): builds the poster draft with generated figure images.

Takes the restyled scene from drafts/2026-11-14-v2/index.html, replaces every figure
with a cut-out image from drafts/2026-11-14-v3/img/, and draws signs, party letters
and ground shadows on top as code so that the text stays sharp.

Usage (from the repo root):  tools/compose_v3.py
Nothing under public/ is touched.
"""
import re

SRC = "drafts/2026-11-14-v2/index.html"
DST = "drafts/2026-11-14-v3/index.html"
OUT = "#1A0F26"
PARTY = {"S": "#E8112D", "M": "#52BDEC", "SD": "#E3D200", "C": "#0E9F45", "V": "#AF0B1E", "MP": "#83CF39", "KD": "#1A2A7A", "L": "#006AB3"}
LIGHT_TEXT = {"S", "C", "V", "KD", "L"}


def n(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


class Fig:
    """One figure: image size, place on the 1080x1620 poster, and overlays in image pixels."""

    def __init__(self, key, label, cls, img, size, left, top, width, flip=False, shadow=None):
        self.key, self.label, self.cls, self.img = key, label, cls, img
        self.flip, self.shadow = flip, shadow   # shadow: (x, y, half width, strength) in image pixels
        self.w, self.h = size
        self.left, self.top, self.width = left, top, width
        self.k = width / self.w            # poster px per image px
        self.height = self.h * self.k
        self.parts = []

    def px(self, poster_px):               # a size given in poster px, in image px
        return poster_px / self.k

    def X(self, x):                        # overlays are given for the unflipped image
        return self.w - x if self.flip else x

    def ground_shadow(self):
        if not self.shadow:
            return ""
        x, y, half, strength = self.shadow
        return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#bg-shadow)" opacity="%s"/>' % (
            n(self.left + self.X(x) * self.k), n(self.top + y * self.k), n(half * self.k), n(max(9, half * self.k * 0.1)), strength)

    def plate(self, x, y, text, size=11, colour=OUT, fill="#FFFDF6", rot=0, pad=7, width=None):
        fs = self.px(size)
        x, rot = self.X(x), (-rot if self.flip else rot)
        w = width or (len(text) * fs * 0.78 + self.px(pad) * 2)
        h = fs * 1.75
        g = '<g transform="rotate(%s %s %s)">' % (rot, n(x), n(y))
        g += '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>' % (n(x - w / 2), n(y - h / 2), n(w), n(h), n(fs * 0.35), fill)
        g += '<text x="%s" y="%s" text-anchor="middle" font-size="%s" fill="%s" stroke="none">%s</text></g>' % (n(x), n(y + fs * 0.36), n(fs), colour, text)
        self.parts.append(g)
        return self

    def badge(self, x, y, party, r=15):
        x = self.X(x)
        rr, fs = self.px(r), self.px(r * (1.05 if len(party) == 1 else 0.78))
        colour = "#fff" if party in LIGHT_TEXT else OUT
        self.parts.append(
            '<circle cx="%s" cy="%s" r="%s" fill="%s"/><circle cx="%s" cy="%s" r="%s" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="%s"/>'
            % (n(x), n(y), n(rr), PARTY[party], n(x), n(y), n(rr * 0.78), n(self.px(1.6)))
            + '<text x="%s" y="%s" text-anchor="middle" font-size="%s" fill="%s" stroke="none">%s</text>' % (n(x), n(y + fs * 0.36), n(fs), colour, party)
        )
        return self

    def text(self, x, y, text, size=12, colour="#fff", rot=0, outline=True):
        fs = self.px(size)
        x, rot = self.X(x), (-rot if self.flip else rot)
        stroke = ' stroke="%s" stroke-width="%s" paint-order="stroke"' % (OUT, n(fs * 0.28)) if outline else ' stroke="none"'
        self.parts.append('<text x="%s" y="%s" text-anchor="middle" font-size="%s" fill="%s"%s transform="rotate(%s %s %s)">%s</text>' % (n(x), n(y), n(fs), colour, stroke, rot, n(x), n(y), text))
        return self

    def raw(self, svg):
        self.parts.append(svg)
        return self

    def html(self):
        style = "position: absolute; left: %spx; top: %spx; width: %spx; height: %spx; background: transparent; border: 0; padding: 0; cursor: pointer" % (n(self.left), n(self.top), n(self.width), n(self.height))
        overlay = ""
        if self.parts:
            overlay = ('<svg viewBox="0 0 %d %d" style="position:absolute;left:0;top:0;width:100%%;height:100%%;overflow:visible"><g stroke="%s" stroke-width="%s" stroke-linejoin="round" font-family="Bungee, sans-serif">%s</g></svg>'
                       % (self.w, self.h, OUT, n(self.px(3)), "".join(self.parts)))
        return ('<button type="button" class="act %s" aria-label="%s" data-act="%s" aria-expanded="false" style="%s"><img src="img/%s.webp" alt="" width="%d" height="%d" decoding="async" style="display:block;width:100%%;height:100%%%s">%s</button>'
                % (self.cls, self.label, self.key, style, self.img, self.w, self.h, ";transform:scaleX(-1)" if self.flip else "", overlay))


def figures():
    f = []
    cannon = Fig("cannon", "Extravalskanonen", "", "cannon", (885, 728), 14, 300, 250)
    cannon.text(590, 226, "EXTRAVAL", 13.5, "#2A1B3D", rot=-27, outline=False).plate(560, 650, "2 AV 4 NEJ", 12, "#FFD23F", fill="#2A1B3D")
    f.append(cannon)

    c = Fig("C", "Centerpartiet", "swingC", "c", (682, 960), 395, 268, 290)
    c.text(92, 322, "S", 18).text(581, 322, "M", 18).plate(88, 420, "TOTALPAKET", 8.5, rot=-6).plate(590, 420, "TOTALPAKET", 8.5, rot=6).badge(351, 492, "C", 13)
    f.append(c)

    s = Fig("S", "Socialdemokraterna", "lean", "s", (865, 700), -4, 560, 470, shadow=(380, 690, 270, 1))
    s.plate(797, 262, "INFLYTANDE", 9).raw('<path d="M85 546v14" fill="none"/>').plate(88, 584, "STÖDPARTI", 11, "#B0201A", rot=-4).badge(352, 432, "S", 14)
    f.append(s)

    m = Fig("M", "Moderaterna", "teeter", "m", (668, 993), 752, 446, 315, flip=True, shadow=(321, 985, 140, 1))
    m.text(86, 100, "KD", 15).text(300, 36, "C", 15).text(566, 88, "L", 15).badge(321, 872, "M", 14)
    m.raw('<g class="hover"><ellipse cx="%s" cy="742" rx="78" ry="21" fill="#E3D200"/><ellipse cx="%s" cy="736" rx="44" ry="9" fill="#fff" fill-opacity=".4" stroke="none"/></g>' % (n(m.X(596)), n(m.X(582))))
    m.text(596, 708, "SD", 13, "#F6EFE0").text(596, 806, "SVÄVAR SJÄLV", 7.5, "#F6EFE0")
    f.append(m)

    v = Fig("V", "Vänsterpartiet", "", "v", (708, 974), 440, 716, 250, shadow=(330, 962, 330, 1))
    v.raw('<path d="M40 650V880" fill="none" stroke="#1A0F26" stroke-width="20"/><path d="M40 650V880" fill="none" stroke="#8A5A2B" stroke-width="11"/>').plate(40, 640, "MINISTER", 9.5, "#FFD23F", fill="#2A1B3D", rot=-5).badge(264, 884, "V", 14)
    v.text(607, 850, "KONGRESS-", 6.5, "#FFD23F", outline=False).text(607, 876, "BESLUT", 6.5, "#FFD23F", outline=False).text(607, 904, "1000 KG", 6, "#F6EFE0", outline=False)
    f.append(v)

    chair = Fig("chair", "Statsministerstolen", "", "chair", (593, 969), 706, 902, 180, shadow=(300, 958, 270, 1))
    chair.plate(262, 330, "LEDIG", 17, "#C8322B", rot=-3).plate(300, 690, "ÖVERGÅNG", 8)
    f.append(chair)

    l = Fig("L", "Liberalerna", "", "l", (959, 703), 280, 1075, 300, shadow=(480, 698, 400, 0.5))
    l.text(432, 290, "L", 19).plate(330, 500, "SPÄRREN 4 %", 10, "#FFD23F", fill="#2A1B3D")
    f.append(l)

    kd = Fig("KD", "Kristdemokraterna", "march", "kd", (695, 982), 6, 1035, 270, shadow=(350, 972, 310, 1))
    kd.text(452, 566, "SAMMA", 11, "#1A2A7A", outline=False).text(446, 640, "LÅT", 16, "#C8322B", outline=False).text(436, 690, "SEDAN VALNATTEN", 5.2, "#1A2A7A", outline=False).badge(130, 232, "KD", 12)
    f.append(kd)

    sd = Fig("SD", "Sverigedemokraterna", "", "sd", (743, 938), 730, 1128, 340, shadow=(400, 928, 380, 1))
    sd.badge(160, 600, "SD", 14).text(31, 258, "JA", 7, "#F6EFE0").text(141, 258, "NEJ", 7, "#F6EFE0").plate(596, 330, "AVSTÅ", 8, rot=20)
    sd.text(650, 425, "MINISTERKRAV", 6.5, "#2A1B3D", outline=False).raw('<path d="M560 420H742" fill="none" stroke="#C8322B" stroke-width="%s"/>' % n(sd.px(2.6)))
    f.append(sd)

    t = Fig("T", "Talmannen", "bounce", "t", (749, 928), 505, 1240, 270, shadow=(370, 920, 340, 1))
    t.text(660, 250, "PROGRAM", 8.5, "#2A1B3D", outline=False)
    for i, (row, colour) in enumerate((("1. S", "#2A1B3D"), ("2. C", "#2A1B3D"), ("3. M?", "#2A1B3D"), ("4. ???", "#8A8496"))):
        t.text(660, 345 + i * 105, row, 12, colour, outline=False)
    t.raw('<path d="M600 332H722M600 437H722" fill="none" stroke="#C8322B" stroke-width="%s"/>' % n(t.px(2.8)))
    f.append(t)

    mp = Fig("MP", "Miljöpartiet", "ride", "mp", (872, 973), 232, 1310, 235, shadow=(430, 962, 320, 1))
    mp.text(706, 96, "KAN VI PRATA", 7.2, "#2A1B3D", rot=-3, outline=False).text(708, 160, "BUDGET NU?", 9.6, "#2E7D1E", rot=-3, outline=False).badge(398, 500, "MP", 12)
    f.append(mp)
    order = ['cannon', 'C', 'M', 'S', 'V', 'chair', 'L', 'KD', 'SD', 'T', 'MP']
    return sorted(f, key=lambda fig: order.index(fig.key))


PLATFORM = (
    '<g stroke="%s" stroke-width="4" stroke-linejoin="round">'
    '<path d="M40 498V720M236 498V720" fill="none" stroke="%s" stroke-width="20"/><path d="M40 498V720M236 498V720" fill="none" stroke="#8A5A2B" stroke-width="12"/>'
    '<path d="M44 520L232 640M232 520L44 640" fill="none" stroke="#6E4520" stroke-width="7"/>'
    '<rect x="-12" y="490" width="300" height="20" rx="5" fill="#B47A3C"/><path d="M-10 496H284" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="3"/>'
    '<ellipse cx="140" cy="490" rx="118" ry="9" fill="#3A2412" fill-opacity=".45" stroke="none"/></g>'
) % (OUT, OUT)


def main():
    page = open(SRC, encoding="utf-8").read()
    first = page.index("<button")
    last = page.rindex("</button>") + len("</button>")
    figs = figures()
    page = page[:first] + "\n".join(f.html() for f in figs) + page[last:]

    # Scene: drop the old ground shadows, add a platform for the cannon and new shadows.
    page, dropped = re.subn(r'<ellipse [^>]*fill="#5E3F1F" opacity="\.4"/>', "", page)
    # The sleeping "z z z" belonged to the old placement of M.
    page, zzz = re.subn(r'<g font-size="20" fill="#F6EFE0" class="blink">.*?</g>', "", page, count=1, flags=re.S)
    assert zzz == 1
    crowd = page.index('<rect width="1080" height="700" fill="url(#bg-glow)"/>')
    page = page[:crowd] + PLATFORM + page[crowd:]
    floor_end = page.index('<path d="M0 754H1080"')
    floor_end = page.index("/>", floor_end) + 2
    shadows = "".join(fig.ground_shadow() for fig in figs)
    page = page[:floor_end] + shadows + page[floor_end:]
    page = page.replace("</defs></svg>", '<radialGradient id="bg-shadow"><stop offset="0" stop-color="#2B1708" stop-opacity=".6"/><stop offset=".7" stop-color="#2B1708" stop-opacity=".32"/><stop offset="1" stop-color="#2B1708" stop-opacity="0"/></radialGradient></defs></svg>', 1)
    open(DST, "w", encoding="utf-8").write(page)
    print("Composed %d figures, replaced %d old shadows -> %s" % (len(figs), dropped, DST))


if __name__ == "__main__":
    main()
