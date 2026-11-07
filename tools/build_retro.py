"""Builds the retro (CRT / 8-bit) profile graphics in assets/retro/.

Every number on the cards comes from a finished project report. Run: python tools/build_retro.py
"""
import os, math

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "retro")
os.makedirs(OUT, exist_ok=True)

# palette: phosphor screen, amber, plus the portfolio's pink, violet, sage and maroon
BG, BG2 = "#07100B", "#0C1A12"
GRN, GRN2 = "#3CFF7E", "#1E8F4A"
AMB = "#FFB627"
PNK = "#FF5FA2"
VIO = "#A78BFA"
CYN = "#5EEAD4"
SAGE = "#A4AF98"
CREAM = "#E9E2CC"
INK = "#F4F1E6"
DIM = "#6F8F7B"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

# ------------------------------------------------------------------ 5x7 pixel font
F = {
 "A": ["01110","10001","10001","11111","10001","10001","10001"],
 "B": ["11110","10001","10001","11110","10001","10001","11110"],
 "C": ["01111","10000","10000","10000","10000","10000","01111"],
 "D": ["11110","10001","10001","10001","10001","10001","11110"],
 "E": ["11111","10000","10000","11110","10000","10000","11111"],
 "F": ["11111","10000","10000","11110","10000","10000","10000"],
 "G": ["01111","10000","10000","10011","10001","10001","01111"],
 "H": ["10001","10001","10001","11111","10001","10001","10001"],
 "I": ["11111","00100","00100","00100","00100","00100","11111"],
 "J": ["00111","00010","00010","00010","00010","10010","01100"],
 "K": ["10001","10010","10100","11000","10100","10010","10001"],
 "L": ["10000","10000","10000","10000","10000","10000","11111"],
 "M": ["10001","11011","10101","10101","10001","10001","10001"],
 "N": ["10001","11001","10101","10011","10001","10001","10001"],
 "O": ["01110","10001","10001","10001","10001","10001","01110"],
 "P": ["11110","10001","10001","11110","10000","10000","10000"],
 "Q": ["01110","10001","10001","10001","10101","10010","01101"],
 "R": ["11110","10001","10001","11110","10100","10010","10001"],
 "S": ["01111","10000","10000","01110","00001","00001","11110"],
 "T": ["11111","00100","00100","00100","00100","00100","00100"],
 "U": ["10001","10001","10001","10001","10001","10001","01110"],
 "V": ["10001","10001","10001","10001","10001","01010","00100"],
 "W": ["10001","10001","10001","10101","10101","10101","01010"],
 "X": ["10001","10001","01010","00100","01010","10001","10001"],
 "Y": ["10001","10001","01010","00100","00100","00100","00100"],
 "Z": ["11111","00001","00010","00100","01000","10000","11111"],
 "0": ["01110","10001","10011","10101","11001","10001","01110"],
 "1": ["00100","01100","00100","00100","00100","00100","01110"],
 "2": ["01110","10001","00001","00010","00100","01000","11111"],
 "3": ["11110","00001","00001","01110","00001","00001","11110"],
 "4": ["00010","00110","01010","10010","11111","00010","00010"],
 "5": ["11111","10000","11110","00001","00001","10001","01110"],
 "6": ["00110","01000","10000","11110","10001","10001","01110"],
 "7": ["11111","00001","00010","00100","01000","01000","01000"],
 "8": ["01110","10001","10001","01110","10001","10001","01110"],
 "9": ["01110","10001","10001","01111","00001","00010","01100"],
 " ": ["00000"]*7,
 ".": ["00000","00000","00000","00000","00000","01100","01100"],
 ",": ["00000","00000","00000","00000","01100","00100","01000"],
 "%": ["11001","11010","00010","00100","01000","01011","10011"],
 "-": ["00000","00000","00000","11111","00000","00000","00000"],
 "&": ["01100","10010","10100","01000","10101","10010","01101"],
 ":": ["00000","01100","01100","00000","01100","01100","00000"],
 "!": ["00100","00100","00100","00100","00100","00000","00100"],
 ">": ["01000","00100","00010","00001","00010","00100","01000"],
 "/": ["00001","00010","00010","00100","01000","01000","10000"],
 "+": ["00000","00100","00100","11111","00100","00100","00000"],
 "'": ["00100","00100","01000","00000","00000","00000","00000"],
 "?": ["01110","10001","00001","00010","00100","00000","00100"],
 "*": ["00000","10101","01110","11111","01110","10101","00000"],
}

def ptext(s, x, y, px, color, cls="", spacing=1):
    """Draw text in the pixel font; returns (svg, width). Each row is merged into runs."""
    out, cx = [], x
    for ch in s.upper():
        g = F.get(ch, F["?"])
        for r, row in enumerate(g):
            c = 0
            while c < len(row):
                if row[c] == "1":
                    s0 = c
                    while c < len(row) and row[c] == "1":
                        c += 1
                    out.append(f'<rect x="{cx+s0*px}" y="{y+r*px}" width="{(c-s0)*px}" height="{px}"/>')
                else:
                    c += 1
        cx += (len(g[0]) + spacing) * px
    w = cx - x - spacing * px
    return f'<g fill="{color}" class="{cls}" shape-rendering="crispEdges">' + "".join(out) + "</g>", w

def pwidth(s, px, spacing=1):
    return sum((len(F.get(c, F["?"])[0]) + spacing) * px for c in s.upper()) - spacing * px

# ------------------------------------------------------------------ the pixel avatar (maroon turban, beard, gold glasses)
AV = [
 "....tttttt....",
 "...tTTTTTTt...",
 "..tTTTTTTTTt..",
 "..tTTtTTTTTt..",
 "..tTTTTTTTTt..",
 "..ssssssssss..",
 "..sgggsgggss..",
 "..sgwgsgwgss..",
 "..ssssssssss..",
 "..bsssbbsssb..",
 "..bbbmmmmbbb..",
 "...bbbbbbbb...",
 "....bbbbbb....",
 "..JJJJcJJJJJ..",
 ".JJJJJcJJJJJJ.",
 "JJJJJJJJJJJJJJ",
 "JJsJJJJJJJJsJJ",
 "JJJJJJJJJJJJJJ",
]
AVC = {"t": "#5A1530", "T": "#7A1F3D", "s": "#C98B5E", "g": "#D9A53A", "w": "#1A1A1A",
       "b": "#2B1B14", "m": "#F4F1E6", "J": "#8E2F45", "c": "#2F6FD1"}

def avatar(x, y, px, cls=""):
    out = []
    for r, row in enumerate(AV):
        for c, ch in enumerate(row):
            if ch != ".":
                out.append(f'<rect x="{x+c*px}" y="{y+r*px}" width="{px}" height="{px}" fill="{AVC[ch]}"/>')
    return f'<g class="{cls}" shape-rendering="crispEdges">' + "".join(out) + "</g>"

# ------------------------------------------------------------------ shared CRT bits
def crt_defs(uid):
    return f"""<defs>
<pattern id="sl{uid}" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".28"/></pattern>
<radialGradient id="vg{uid}" cx="50%" cy="50%" r="75%"><stop offset="60%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".65"/></radialGradient>
<filter id="gl{uid}" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>"""

def crt_overlay(uid, x, y, w, h, rx=18):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#sl{uid})"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#vg{uid})"/>'
            f'<rect class="roll" x="{x}" y="{y}" width="{w}" height="26" fill="#3CFF7E" opacity=".05"/>')

BASE_CSS = f"""
.m{{font-family:{MONO}}}
.blink{{animation:bl 1s steps(1) infinite}}@keyframes bl{{50%{{opacity:0}}}}
.roll{{animation:ro 7s linear infinite}}@keyframes ro{{from{{transform:translateY(-30px)}}to{{transform:translateY(460px)}}}}
.flick{{animation:fk 5s infinite}}@keyframes fk{{0%,97%,100%{{opacity:1}}98%{{opacity:.82}}}}
"""

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def save(name, w, h, body, label, css=""):
    label = esc(label)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
           f"<title>{label}</title><style>{BASE_CSS}{css}</style>{body}</svg>")
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)

def appear(i, start, step, total):
    """keyframes that show item i at start+i*step seconds and keep it (one-shot boot)."""
    t = start + i * step
    return f".a{i}{{opacity:0;animation:ap{i} .01s {t:.2f}s forwards}}@keyframes ap{i}{{to{{opacity:1}}}}"

# ------------------------------------------------------------------ 1. header: a CRT monitor booting MANKIRAT-OS
def header():
    W, H, u = 1200, 460, "h"
    sx, sy, sw, sh = 46, 34, 1108, 352
    lines = [
        ("MANKIRAT-OS (R) BIOS v20.26 · CORK, IRELAND", DIM),
        ("CPU: BENCH-TO-CODE @ 2 OMICS LAYERS ...... OK", DIM),
        ("MEMORY TEST: 21 PROJECTS ............... OK", DIM),
        ("LOADING GENOME  [■■■■■■■■■■■■■■■■] 100%", GRN),
        ("C:\\> whoami", INK),
    ]
    css = "".join(appear(i, .3, .45, len(lines)) for i in range(len(lines) + 3))
    b = [crt_defs(u)]
    # beige monitor
    b.append(f'<rect x="8" y="6" width="{W-16}" height="{H-12}" rx="34" fill="{CREAM}"/>')
    b.append(f'<rect x="8" y="6" width="{W-16}" height="{H-12}" rx="34" fill="none" stroke="#B9B095" stroke-width="3"/>')
    b.append(f'<rect x="{sx-10}" y="{sy-10}" width="{sw+20}" height="{sh+20}" rx="26" fill="#3A3A33"/>')
    b.append(f'<g class="flick"><rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="18" fill="{BG}"/>')
    y = sy + 40
    for i, (t, c) in enumerate(lines):
        b.append(f'<text class="m a{i}" x="{sx+30}" y="{y}" font-size="15" fill="{c}" letter-spacing="1">{t}</text>')
        y += 24
    # name in pixel font
    g, wname = ptext("MANKIRAT SINGH", sx + 30, y + 6, 8, AMB)
    b.append(f'<g class="a5" filter="url(#gl{u})">{g}</g>')
    ny = y + 6 + 7 * 8 + 26
    b.append(f'<text class="m a6" x="{sx+32}" y="{ny}" font-size="17" fill="{GRN}" letter-spacing="1">bioinformatician · data scientist · lab bench to code</text>')
    b.append(f'<text class="m a7" x="{sx+32}" y="{ny+30}" font-size="17" fill="{INK}" letter-spacing="1">Human from Earth, currently orbiting Cork.<tspan class="blink" fill="{GRN}"> █</tspan></text>')
    # pixel DNA helix on the right
    cx, top, n, R = sx + sw - 150, sy + 34, 14, 52
    cols = [PNK, VIO, CYN, AMB]
    for i in range(n):
        yy = top + i * 21
        d = -i * .18
        b.append(f'<g class="dA" style="animation-delay:{d:.2f}s"><rect x="{cx-6}" y="{yy}" width="12" height="12" fill="{PNK}"/></g>')
        b.append(f'<g class="dB" style="animation-delay:{d:.2f}s"><rect x="{cx-6}" y="{yy}" width="12" height="12" fill="{CYN}"/></g>')
        b.append(f'<rect class="rung" style="animation-delay:{d:.2f}s" x="{cx-R}" y="{yy+4}" width="{2*R}" height="4" fill="{cols[i%4]}" opacity=".55"/>')
    b.append(crt_overlay(u, sx, sy, sw, sh) + "</g>")
    # bezel details
    b.append(f'<text class="m" x="{sx}" y="{H-30}" font-size="13" fill="#7C745E" letter-spacing="3">MK-2026 · PERSONAL BIO-COMPUTER</text>')
    b.append(f'<circle class="blink" cx="{W-70}" cy="{H-35}" r="7" fill="{GRN}"/>')
    b.append(f'<rect x="{W-230}" y="{H-42}" width="130" height="14" rx="3" fill="#CFC6AC"/>')
    css += f"""
.dA{{animation:da 3.2s steps(16) infinite}}.dB{{animation:db 3.2s steps(16) infinite}}
@keyframes da{{0%,100%{{transform:translateX(-52px)}}50%{{transform:translateX(52px)}}}}
@keyframes db{{0%,100%{{transform:translateX(52px)}}50%{{transform:translateX(-52px)}}}}
.rung{{transform-box:fill-box;transform-origin:center;animation:rg 3.2s steps(16) infinite}}
@keyframes rg{{0%,50%,100%{{transform:scaleX(1)}}25%,75%{{transform:scaleX(.08)}}}}"""
    save("header.svg", W, H, "".join(b), "Mankirat Singh: bioinformatician and data scientist in Cork, Ireland", css)

# ------------------------------------------------------------------ 2. about: an RPG dialogue box with the avatar
def about():
    W, H, u = 1200, 250, "a"
    lines = [
        "Hello, traveller! I'm a bioinformatician and data scientist in Cork.",
        "I started at the lab bench: NGS diagnostic kits, qPCR, histology and in vivo",
        "studies. Now I build Python, R and SQL pipelines, models, maps and reports.",
        "MSc Bioinformatics and Computational Biology, University College Cork.",
        "QUEST: a PhD first, and I'm open to R&D, bioinformatics and data roles.",
    ]
    css = "".join(appear(i, .4, .7, len(lines)) for i in range(len(lines) + 1))
    b = [crt_defs(u)]
    b.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="14" fill="{BG}" stroke="{INK}" stroke-width="5"/>')
    b.append(f'<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="8" fill="none" stroke="{DIM}" stroke-width="2"/>')
    # portrait frame
    b.append(f'<rect x="34" y="36" width="160" height="178" rx="6" fill="{BG2}" stroke="{SAGE}" stroke-width="3"/>')
    b.append(avatar(50, 48, 9, "bob"))
    g, _ = ptext("MANKIRAT", 222, 40, 4, AMB)
    b.append(g)
    y = 92
    for i, t in enumerate(lines):
        col = GRN if t.startswith("QUEST") else INK
        b.append(f'<text class="m a{i}" x="222" y="{y}" font-size="17" fill="{col}">{esc(t)}</text>')
        y += 27
    b.append(f'<g class="a5"><path class="nx" d="M{W-60} {H-46} l14 0 l-7 9 z" fill="{AMB}"/></g>')
    b.append(crt_overlay(u, 16, 16, W - 32, H - 32, 8))
    css += ".bob{animation:bo 1.2s steps(2) infinite}@keyframes bo{50%{transform:translateY(3px)}}.nx{animation:bl .8s steps(1) infinite}"
    save("about.svg", W, H, "".join(b), "Hello! I'm Mankirat, a bioinformatician and data scientist in Cork. Lab bench to code. MSc Bioinformatics and Computational Biology, University College Cork. Looking for a PhD first, and open to R&D, bioinformatics and data roles.", css)

# ------------------------------------------------------------------ 3. high scores
def scores():
    W, H, u = 1200, 330, "s"
    rows = [("1ST", "21", "PROJECTS, BENCH TO CODE", AMB),
            ("2ND", "40,124", "CLINICAL TRIALS ANALYSED", PNK),
            ("3RD", "34%", "BETTER POWER FORECAST", CYN),
            ("4TH", "17", "PLANT GENOMES SEARCHED", GRN)]
    css = "".join(appear(i, .3, .35, 4) for i in range(5))
    b = [crt_defs(u), f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16" fill="#0A0612" stroke="{VIO}" stroke-width="4"/>']
    g, w = ptext("HIGH SCORES", 0, 0, 6, PNK)
    b.append(f'<g transform="translate({(W-w)//2},30)" filter="url(#gl{u})">{g}</g>')
    b.append(f'<text class="m blink" x="60" y="62" font-size="18" fill="{AMB}" font-weight="700">1UP</text>')
    b.append(f'<text class="m" x="{W-200}" y="62" font-size="18" fill="{SAGE}" font-weight="700">CREDIT 01</text>')
    y = 98
    for i, (rank, num, lab, c) in enumerate(rows):
        r, _ = ptext(rank, 120, y, 4, c)
        n, nw = ptext(num, 0, 0, 5, c)
        b.append(f'<g class="a{i}">{r}<g transform="translate({560-nw},{y-3})">{n}</g>')
        b.append(f'<text class="m" x="600" y="{y+24}" font-size="20" fill="{INK}" letter-spacing="2">{lab}</text></g>')
        y += 44
    b.append(f'<text class="m a4" x="{W//2}" y="{H-22}" text-anchor="middle" font-size="15" fill="{GRN}" letter-spacing="2"><tspan class="blink">▶ PRESS START</tspan>  bymankirat.github.io/myportfolio</text>')
    b.append(crt_overlay(u, 6, 6, W - 12, H - 12, 16))
    save("scores.svg", W, H, "".join(b), "High scores: 21 projects from bench to code, 40,124 clinical trials analysed, a power forecast 34% better than the benchmark, 17 plant genomes searched", css)

# ------------------------------------------------------------------ 4. world map: the journey, level by level
def worldmap():
    W, H, u = 1200, 390, "w"
    stops = [("1-1", "DELHI", "BSC LIFE SCI", "2020-23", 120, 290),
             ("1-2", "MOHALI", "BRIC-NABI", "2023-24", 300, 160),
             ("1-3", "NEW DELHI", "PREMAS R&D", "2024-25", 480, 290),
             ("1-4", "MUMBAI", "PG DIPLOMA", "2024-25", 660, 160),
             ("1-5", "MALAGA", "MSC THESIS", "2026", 840, 290),
             ("1-6", "CORK", "MSC UCC", "2025-26", 1040, 160)]
    b = [crt_defs(u), f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16" fill="#0B1F14" stroke="{GRN2}" stroke-width="4"/>']
    # pixel grass speckles
    import random
    rnd = random.Random(7)
    for _ in range(140):
        x, y = rnd.randrange(20, W - 20, 6), rnd.randrange(60, H - 20, 6)
        b.append(f'<rect x="{x}" y="{y}" width="6" height="6" fill="{GRN2}" opacity=".35"/>')
    g, w = ptext("WORLD 1: BENCH TO CODE", 0, 0, 4, AMB)
    b.append(f'<g transform="translate(40,26)">{g}</g>')
    # dotted path
    for (a, c) in zip(stops, stops[1:]):
        x1, y1, x2, y2 = a[4], a[5], c[4], c[5]
        nseg = 14
        for k in range(1, nseg):
            t = k / nseg
            b.append(f'<rect x="{x1+(x2-x1)*t-4:.0f}" y="{y1+(y2-y1)*t-4:.0f}" width="8" height="8" fill="{CREAM}" opacity=".85"/>')
    for i, (lv, city, what, yrs, x, y) in enumerate(stops):
        last = i == len(stops) - 1
        col = PNK if last else AMB
        b.append(f'<rect x="{x-22}" y="{y-22}" width="44" height="44" fill="{col}" stroke="#2B1B14" stroke-width="4"/>')
        t, tw = ptext(lv, 0, 0, 3, "#2B1B14")
        b.append(f'<g transform="translate({x-tw//2},{y-10})">{t}</g>')
        ly = y - 58 if y < 200 else y + 48
        b.append(f'<text class="m" x="{x}" y="{ly}" text-anchor="middle" font-size="16" font-weight="700" fill="{INK}">{city}</text>')
        b.append(f'<text class="m" x="{x}" y="{ly+19}" text-anchor="middle" font-size="13" fill="{GRN}">{esc(what)} · {yrs}</text>')
        if not last:
            b.append(f'<text class="m" x="{x+26}" y="{y-24}" font-size="14" fill="{AMB}">★</text>')
    # "you are here"
    hx, hy = stops[-1][4], stops[-1][5]
    b.append(f'<text class="m blink" x="{hx}" y="{hy+46}" text-anchor="middle" font-size="14" font-weight="700" fill="{PNK}">▲ YOU ARE HERE</text>')
    # the avatar walks the path, stop by stop
    pts = [(s[4] - 21, s[5] - 40) for s in stops]
    n = len(pts)
    frames = []
    for i, (x, y) in enumerate(pts):
        p0 = i / (n - 1) * 88
        frames.append(f"{p0:.1f}%{{transform:translate({x}px,{y}px)}}")
        if i < n - 1:
            frames.append(f"{p0+8:.1f}%{{transform:translate({x}px,{y}px)}}")
    frames.append(f"100%{{transform:translate({pts[-1][0]}px,{pts[-1][1]}px)}}")
    css = "@keyframes walk{" + "".join(frames) + "}.walker{animation:walk 12s steps(60) infinite}"
    b.append(f'<g class="walker">{avatar(0, 0, 3)}</g>')
    b.append(crt_overlay(u, 6, 6, W - 12, H - 12, 16))
    save("worldmap.svg", W, H, "".join(b), "World map of my path: Delhi (BSc Life Sciences), Mohali (BRIC-NABI), New Delhi (Premas R&D), Mumbai (PG Diploma), Málaga (MSc thesis) and Cork (MSc, University College Cork)", css)

# ------------------------------------------------------------------ 5. section banners
def banner(name, text, color, label):
    W, H = 1200, 84
    g, w = ptext(text, 0, 0, 6, color)
    b = [f'<rect width="{W}" height="{H}" fill="none"/>',
         f'<g transform="translate(70,20)">{g}</g>',
         f'<text class="m blink" x="30" y="58" font-size="34" fill="{color}">▶</text>',
         f'<rect x="{90+w}" y="40" width="{W-120-w}" height="6" fill="{color}" opacity=".35"/>']
    save(name, W, H, "".join(b), label)

# ------------------------------------------------------------------ 6. project cards: retro windows with pixel charts
def vis(kind, x, y, w, h, c, seed):
    import random
    r = random.Random(seed)
    out = []
    if kind == "bars":
        n = 9
        for i in range(n):
            v = r.uniform(.25, 1)
            bh = int(v * h // 8) * 8
            out.append(f'<rect class="grow" style="animation-delay:{i*.12:.2f}s" x="{x+i*(w//n)}" y="{y+h-bh}" width="{w//n-6}" height="{bh}" fill="{c}"/>')
    elif kind == "line":
        pts, v = [], .5
        for i in range(0, w, 8):
            v = min(.95, max(.05, v + r.uniform(-.18, .18)))
            pts.append((x + i, y + int((1 - v) * h // 8) * 8))
        for i, (px, py) in enumerate(pts):
            out.append(f'<rect class="pop" style="animation-delay:{i*.04:.2f}s" x="{px}" y="{py}" width="8" height="8" fill="{c}"/>')
    elif kind == "grid":
        for i in range(0, w, 12):
            for j in range(0, h, 12):
                if r.random() < .55:
                    o = r.choice([.25, .5, .8, 1])
                    out.append(f'<rect class="tw" style="animation-delay:{r.uniform(0,3):.2f}s" x="{x+i}" y="{y+j}" width="10" height="10" fill="{c}" opacity="{o}"/>')
    elif kind == "helix":
        for i in range(0, w, 10):
            a = i / w * math.pi * 4
            y1 = y + h / 2 + math.sin(a) * h * .4
            y2 = y + h / 2 - math.sin(a) * h * .4
            out.append(f'<rect x="{x+i}" y="{int(y1)//4*4}" width="8" height="8" fill="{c}"/><rect x="{x+i}" y="{int(y2)//4*4}" width="8" height="8" fill="{CYN}"/>')
    elif kind == "map":
        for _ in range(40):
            px, py = x + r.randrange(0, w, 8), y + r.randrange(0, h, 8)
            out.append(f'<rect class="tw" style="animation-delay:{r.uniform(0,3):.2f}s" x="{px}" y="{py}" width="8" height="8" fill="{c}"/>')
        out.append(f'<rect x="{x}" y="{y+h//2}" width="{w}" height="4" fill="{SAGE}" opacity=".6"/>')
    elif kind == "km":
        yy = y
        for i in range(0, w, 16):
            out.append(f'<rect x="{x+i}" y="{yy}" width="16" height="6" fill="{c}"/>')
            if r.random() < .45:
                yy += 8
                out.append(f'<rect x="{x+i+12}" y="{yy-8}" width="4" height="10" fill="{c}"/>')
    return "".join(out)

CARDS = [
    ("trials", "TRIALS.EXE", "CLINICAL · PYTHON", "Why clinical trials stop early", "40,124 trials · design-stage risk score", "1 IN 6", "stopped early", "bars", PNK),
    ("cdisc", "CDISC.EXE", "CLINICAL · R · CDISC", "Trial safety: SDTM to ADaM", "Alzheimer's drug trial · 254 patients", "100%", "independent QC match", "km", AMB),
    ("gpc3", "GPC3.EXE", "CANCER · TCGA + GTEX", "Glypican-3 across 33 cancers", "Diagnosis, survival, methylation, 3D", "0.94", "AUC in liver cancer", "grid", VIO),
    ("h7n9", "H7N9.EXE", "VIROLOGY · R", "What makes H7N9 different?", "4 flu strains · 78 arrays · limma", "1,279", "genes unique to H7N9", "grid", PNK),
    ("sog1", "SOG1.EXE", "PLANT GENOMICS", "SOG1 across 17 plant genomes", "HMMER · IQ-TREE · dN/dS", "3X", "binding sites at targets", "helix", GRN),
    ("load", "POWER.EXE", "ENERGY · FORECAST", "Irish electricity demand", "Day-ahead, 15-minute EirGrid data", "34%", "better than benchmark", "line", CYN),
    ("wind", "WIND.EXE", "ENERGY · STATISTICS", "Wind turned away by the grid", "Four years of EirGrid data", "R 0.86", "match to EirGrid", "line", GRN),
    ("grid", "GRID2040.EXE", "ENERGY · MONTE CARLO", "Cork & Dublin 2040 grid", "Demand, substations, budget", "122", "substations short by 2040", "map", VIO),
    ("rail", "RAIL.EXE", "TRANSPORT · GIS", "Cork commuter rail 2040", "Who the new stations would reach", "22,648", "people within 1 km", "map", AMB),
    ("health", "CENSUS.EXE", "PUBLIC HEALTH", "Health and deprivation", "3,420 Irish communities", "63%", "explained by social factors", "grid", CYN),
    ("flow", "RIVER.EXE", "WATER · EARLY WARNING", "River low-flow warning", "7-day warning, 21 years of data", "4 OF 4", "episodes flagged early", "line", CYN),
    ("store", "KPI.EXE", "CONTROLLING · CUSUM", "Store KPI controlling toolkit", "Simulated 40-store chain", "3 OF 3", "problem stores caught", "bars", AMB),
    ("jobs", "JOBS.EXE", "LABOUR MARKET", "Irish unemployment outlook", "Four models, honest backtest", "56", "unseen months tested", "line", PNK),
    ("cyp", "CYP19A1.EXE", "GENE EXPRESSION · R", "CYP19A1 in human and mouse", "GTEx, mouse atlas, TCGA ovarian", "54", "human tissues profiled", "bars", VIO),
]

def card(slug, fn, kick, title, sub, kpi, kpil, kind, c, seed):
    label = f"{title}: {sub}. {kpi.title()} {kpil}"
    kick, title, sub, kpil = esc(kick), esc(title), esc(sub), esc(kpil)
    W, H, u = 600, 300, slug
    b = [crt_defs(u)]
    b.append(f'<rect x="4" y="4" width="{W-8}" height="{H-8}" fill="{CREAM}" stroke="#2B1B14" stroke-width="4"/>')
    # classic title bar with stripes
    b.append(f'<rect x="4" y="4" width="{W-8}" height="30" fill="{CREAM}" stroke="#2B1B14" stroke-width="4"/>')
    for k in range(7):
        b.append(f'<rect x="12" y="{11+k*3}" width="{W-24}" height="1.5" fill="#2B1B14" opacity=".55"/>')
    tw = len(fn) * 10 + 28
    b.append(f'<rect x="{(W-tw)//2}" y="8" width="{tw}" height="22" fill="{CREAM}"/>')
    b.append(f'<text class="m" x="{W//2}" y="25" text-anchor="middle" font-size="15" font-weight="700" fill="#2B1B14">{fn}</text>')
    b.append(f'<rect x="18" y="11" width="16" height="16" fill="{CREAM}" stroke="#2B1B14" stroke-width="2"/>')
    # screen
    b.append(f'<rect x="16" y="44" width="{W-32}" height="{H-60}" fill="{BG}"/>')
    b.append(f'<text class="m" x="34" y="72" font-size="13" fill="{c}" letter-spacing="2">{kick}</text>')
    b.append(f'<text class="m" x="34" y="102" font-size="22" font-weight="700" fill="{INK}">{title}</text>')
    b.append(f'<text class="m" x="34" y="126" font-size="14" fill="{SAGE}">{sub}</text>')
    g, kw = ptext(kpi, 34, 150, 6, c)
    b.append(f'<g filter="url(#gl{u})">{g}</g>')
    b.append(f'<text class="m" x="34" y="222" font-size="15" fill="{INK}">{kpil}</text>')
    b.append(f'<g opacity=".9">{vis(kind, 360, 150, 200, 80, c, seed)}</g>')
    b.append(f'<text class="m" x="34" y="{H-28}" font-size="14" font-weight="700" fill="{GRN}"><tspan class="blink">▶</tspan> RUN REPORT</text>')
    b.append(crt_overlay(u, 16, 44, W - 32, H - 60, 0))
    css = (".grow{transform-box:fill-box;transform-origin:bottom;animation:gr 2.4s steps(6) infinite alternate}@keyframes gr{from{transform:scaleY(.15)}to{transform:scaleY(1)}}"
           ".pop{animation:pp 3s steps(1) infinite}@keyframes pp{0%{opacity:0}20%,100%{opacity:1}}"
           ".tw{animation:tw 2.6s steps(2) infinite}@keyframes tw{50%{opacity:.15}}")
    save(f"card-{slug}.svg", W, H, "".join(b), label, css)


# ------------------------------------------------------------------ 6a. featured cartridge: SwapSeq, my open-source tool
def featured():
    W, H, u = 1200, 400, "sw"
    b = [crt_defs(u)]
    b.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16" fill="{BG}" stroke="{AMB}" stroke-width="4"/>')
    b.append(f'<text class="m" x="44" y="56" font-size="14" fill="{AMB}" letter-spacing="2"><tspan class="blink">★</tspan> NEW GAME · MY OPEN-SOURCE TOOL · v1.1.1 · WEB + R</text>')
    g, w = ptext("SWAPSEQ", 44, 78, 9, GRN)
    b.append(f'<g filter="url(#gl{u})">{g}</g>')
    b.append(f'<text class="m" x="44" y="178" font-size="19" fill="{INK}">Catches swapped tubes and wrong labels in</text>')
    b.append(f'<text class="m" x="44" y="202" font-size="19" fill="{INK}">longitudinal microbiome studies. Runs in your browser.</text>')
    kp = [("92%", "swaps flagged, adult gut", PNK), ("30", "public datasets graded", CYN), ("16,336", "samples in the Atlas", VIO)]
    x = 44
    for i, (k, l, c) in enumerate(kp):
        g, kw = ptext(k, x, 236, 5, c)
        b.append(f'<g class="a{i}" filter="url(#gl{u})">{g}</g>')
        b.append(f'<text class="m a{i}" x="{x}" y="296" font-size="14" fill="{SAGE}">{l}</text>')
        x += max(kw, 200) + 34
    b.append(f'<text class="m" x="44" y="{H-40}" font-size="15" font-weight="700" fill="{GRN}"><tspan class="blink">▶</tspan> RUN TOOL   <tspan fill="{AMB}">▶ ATLAS</tspan>   <tspan fill="{VIO}">▶ R PACKAGE</tspan></text>')
    # a 96-well plate where two wells trade places: the error SwapSeq finds
    px, py, cs = 790, 74, 30
    b.append(f'<rect x="{px-18}" y="{py-18}" width="{12*cs+24}" height="{8*cs+24}" rx="10" fill="{BG2}" stroke="{SAGE}" stroke-width="3"/>')
    import random
    r = random.Random(7)
    pal = [GRN2, "#2C6E4F", "#3A8C60", "#24563F"]
    for row in range(8):
        for col in range(12):
            cx, cy = px + col * cs + 3, py + row * cs + 3
            if (row, col) == (4, 3):
                b.append(f'<rect class="swA" x="{cx}" y="{cy}" width="{cs-8}" height="{cs-8}" rx="4"/>')
            elif (row, col) == (4, 8):
                b.append(f'<rect class="swB" x="{cx}" y="{cy}" width="{cs-8}" height="{cs-8}" rx="4"/>')
            else:
                b.append(f'<rect x="{cx}" y="{cy}" width="{cs-8}" height="{cs-8}" rx="4" fill="{r.choice(pal)}"/>')
    for k in range(8):
        b.append(f'<text class="m" x="{px-12}" y="{py+k*cs+18}" font-size="10" fill="{DIM}" text-anchor="middle">{"ABCDEFGH"[k]}</text>')
    b.append(f'<rect class="hit" x="{px+3*cs-1}" y="{py+4*cs-1}" width="{5*cs+cs-4}" height="{cs-4}" fill="none" stroke="{PNK}" stroke-width="3" stroke-dasharray="6 4"/>')
    b.append(f'<text class="m hit" x="{px+6*cs-2}" y="{py+8*cs+30}" text-anchor="middle" font-size="14" font-weight="700" fill="{PNK}">E4 ⇄ E9  SWAP FOUND</text>')
    b.append(crt_overlay(u, 6, 6, W - 12, H - 12, 16))
    css = ("".join(appear(i, .4, .35, 3) for i in range(3)) +
           f".swA{{animation:sa 4s steps(1) infinite}}.swB{{animation:sb 4s steps(1) infinite}}"
           f"@keyframes sa{{0%,49%{{fill:{AMB}}}50%,100%{{fill:{PNK}}}}}@keyframes sb{{0%,49%{{fill:{PNK}}}50%,100%{{fill:{AMB}}}}}"
           ".hit{animation:ht 4s steps(1) infinite}@keyframes ht{0%,49%{opacity:0}50%,100%{opacity:1}}")
    save("swapseq.svg", W, H, "".join(b), "SwapSeq, my open-source tool (v1.1.1, web and R): catches swapped tubes and wrong labels in longitudinal microbiome studies. 92% of swaps flagged in adult gut 16S; 30 public datasets and 16,336 samples graded in the SwapSeq Atlas", css)

# ------------------------------------------------------------------ 7. inventory (no fake skill levels)
def inventory():
    W, u = 1200, "i"
    groups = [("LANGUAGES", AMB, ["Python", "R", "SQL", "JavaScript"]),
              ("OMICS", PNK, ["QIIME2", "DADA2", "phyloseq", "mixOmics", "ANCOM-BC2", "limma", "WGCNA", "fgsea", "HMMER", "IQ-TREE"]),
              ("CLINICAL", VIO, ["CDISC SDTM", "ADaM", "admiral", "survival", "double programming"]),
              ("STATS + ML", CYN, ["scikit-learn", "gradient boosting", "random forest", "CUSUM", "Monte Carlo", "time series"]),
              ("DATA + BI", GRN, ["Power BI", "DAX", "DuckDB", "pandas", "Git", "GitHub Pages"]),
              ("LAB", CREAM, ["NGS (Illumina)", "qPCR", "Western blot", "cloning", "microtomy", "H&E"])]
    b, y = [], 30
    rows = []
    for name, c, items in groups:
        x = 230
        line = []
        for it in items:
            w = len(it) * 9 + 30
            if x + w > W - 30:
                rows.append((name, c, line)); name, line, x = "", [], 230
            line.append((x, it, w)); x += w + 10
        rows.append((name, c, line))
    H = 50 + len(rows) * 46 + 20
    b.append(crt_defs(u))
    b.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="14" fill="{BG}" stroke="{AMB}" stroke-width="4"/>')
    b.append(f'<text class="m" x="30" y="44" font-size="14" fill="{SAGE}" letter-spacing="1">ITEMS COLLECTED IN FINISHED PROJECTS</text>')
    y = 64
    for name, c, line in rows:
        if name:
            b.append(f'<text class="m" x="30" y="{y+23}" font-size="15" font-weight="700" fill="{c}" letter-spacing="2">{name}</text>')
        for (x, it, w) in line:
            b.append(f'<rect x="{x}" y="{y}" width="{w}" height="34" fill="{BG2}" stroke="{c}" stroke-width="3"/>')
            b.append(f'<rect x="{x+8}" y="{y+13}" width="8" height="8" fill="{c}"/>')
            b.append(f'<text class="m" x="{x+22}" y="{y+23}" font-size="14" fill="{INK}">{it.replace("&","&amp;")}</text>')
        y += 46
    b.append(crt_overlay(u, 6, 6, W - 12, H - 12, 14))
    save("inventory.svg", W, H, "".join(b), "Inventory: Python, R, SQL, JavaScript; QIIME2, DADA2, phyloseq, mixOmics, ANCOM-BC2, limma, WGCNA, fgsea, HMMER, IQ-TREE; CDISC SDTM, ADaM, admiral, survival analysis, double programming; scikit-learn, gradient boosting, random forest, CUSUM, Monte Carlo, time series; Power BI, DAX, DuckDB, pandas, Git, GitHub Pages; NGS, qPCR, Western blot, cloning, microtomy, H&E")

# ------------------------------------------------------------------ 8. footer
def footer():
    W, H = 1200, 120
    g, w = ptext("CONTINUE?", 0, 0, 6, AMB)
    b = [f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="14" fill="#0A0612" stroke="{PNK}" stroke-width="4"/>',
         f'<g transform="translate({(W-w)//2},26)">{g}</g>',
         f'<text class="m" x="{W//2}" y="96" text-anchor="middle" font-size="16" fill="{INK}"><tspan class="blink" fill="{GRN}">INSERT COIN</tspan>  ·  PhD supervisors, labs and data teams: let\'s talk</text>']
    save("footer.svg", W, H, "".join(b), "Continue? PhD supervisors, labs and data teams: let's talk")

if __name__ == "__main__":
    header(); about(); scores(); worldmap(); inventory(); footer(); featured()
    banner("sec-projects.svg", "SELECT PROJECT", PNK, "Select a project")
    banner("sec-map.svg", "WORLD MAP", GRN, "World map")
    banner("sec-inv.svg", "INVENTORY", AMB, "Inventory")
    for i, c in enumerate(CARDS):
        card(*c, seed=i * 13 + 5)
    print("wrote", len(os.listdir(OUT)), "files to", os.path.abspath(OUT))
