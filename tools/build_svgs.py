"""Builds the animated SVGs used in the profile README (assets/*.svg).
Run: python3 tools/build_svgs.py
GitHub shows README images without scripts, so everything here is plain SVG + CSS animation.
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

BG, BG2 = "#060A13", "#0B1222"
INK, MUTED, FAINT = "#E6EDF7", "#8A97AD", "#2A3550"
CY, VI, PK, LIME, AMB = "#22D3EE", "#8B5CF6", "#F472B6", "#A3E635", "#FBBF24"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}.rm{opacity:1!important;stroke-dashoffset:0!important}}"


def defs_common(uid):
    return f"""<defs>
<linearGradient id="edge{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CY}"/><stop offset=".5" stop-color="{VI}"/><stop offset="1" stop-color="{PK}"/></linearGradient>
<linearGradient id="txt{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CY}"/><stop offset=".55" stop-color="{VI}"/><stop offset="1" stop-color="{PK}"/></linearGradient>
<linearGradient id="scan{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="glowA{uid}"><stop offset="0" stop-color="{VI}" stop-opacity=".35"/><stop offset="1" stop-color="{VI}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowB{uid}"><stop offset="0" stop-color="{CY}" stop-opacity=".25"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></radialGradient>
<filter id="neon{uid}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="dots{uid}" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{FAINT}"/></pattern>
</defs>"""


def text_w(s, size, weight=500):
    """Rough text width for layout (system sans)."""
    return len(s) * size * (0.58 if weight >= 600 else 0.54)


# ---------------------------------------------------------------- project cards
W, H = 520, 260


def chips(tags, x, y, color=MUTED):
    out, cx = [], x
    for t in tags:
        w = text_w(t, 11.5) + 22
        out.append(f'<rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="24" rx="12" fill="#ffffff" fill-opacity=".03" stroke="{color}" stroke-opacity=".35"/>'
                   f'<text x="{cx + w / 2:.1f}" y="{y + 16}" class="tag" text-anchor="middle">{t}</text>')
        cx += w + 7
    return "".join(out)


def card(name, kicker, title, sub, kpi, kpi_label, tags, visual, accent=CY):
    uid = name
    css = f"""<style>
.k{{font:700 10.5px {MONO};fill:{accent};letter-spacing:2.2px}}
.t{{font:700 22px {SANS};fill:{INK}}}
.s{{font:400 13.5px {SANS};fill:{MUTED}}}
.kpi{{font:800 40px {SANS};letter-spacing:-1px}}
.kl{{font:500 12px {MONO};fill:{MUTED}}}
.tag{{font:500 11.5px {SANS};fill:{MUTED}}}
.go{{font:700 12px {MONO};fill:{INK}}}
.scan{{animation:sc 7s linear infinite}}@keyframes sc{{0%{{transform:translateX(-200px)}}60%,100%{{transform:translateX(720px)}}}}
.edge{{animation:eg 6s ease-in-out infinite}}@keyframes eg{{0%,100%{{stroke-opacity:.45}}50%{{stroke-opacity:.95}}}}
.live{{animation:lv 1.6s ease-in-out infinite}}@keyframes lv{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
.draw{{stroke-dasharray:1;stroke-dashoffset:1;animation:dr 6s ease-out infinite}}@keyframes dr{{0%{{stroke-dashoffset:1}}55%,90%{{stroke-dashoffset:0}}100%{{stroke-dashoffset:0;opacity:.4}}}}
.pop{{opacity:0;animation:pp 6s ease-out infinite}}@keyframes pp{{0%,20%{{opacity:0}}40%,90%{{opacity:1}}100%{{opacity:.4}}}}
.grow{{transform-box:fill-box;transform-origin:left center;animation:gw 6s ease-out infinite}}@keyframes gw{{0%{{transform:scaleX(0)}}45%,90%{{transform:scaleX(1)}}100%{{transform:scaleX(1);opacity:.4}}}}
.rise{{transform-box:fill-box;transform-origin:center bottom;animation:rs 6s ease-out infinite}}@keyframes rs{{0%{{transform:scaleY(0)}}45%,90%{{transform:scaleY(1)}}100%{{transform:scaleY(1);opacity:.4}}}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pu 2.6s ease-in-out infinite}}@keyframes pu{{0%,100%{{transform:scale(1);opacity:1}}50%{{transform:scale(1.8);opacity:.35}}}}
.ring{{transform-box:fill-box;transform-origin:center;animation:rg 2.6s ease-out infinite}}@keyframes rg{{0%{{transform:scale(.4);opacity:.9}}100%{{transform:scale(2.6);opacity:0}}}}
.blink{{animation:bk 1.2s steps(1) infinite}}@keyframes bk{{50%{{opacity:0}}}}
{REDUCED}
</style>"""
    body = f"""<rect width="{W}" height="{H}" rx="20" fill="{BG}"/>
<g clip-path="url(#clip{uid})"><rect width="{W}" height="{H}" fill="url(#dots{uid})" opacity=".55"/>
<circle cx="{W - 60}" cy="40" r="170" fill="url(#glowA{uid})"/>
<circle cx="40" cy="{H}" r="150" fill="url(#glowB{uid})"/>
<rect class="scan" x="0" y="0" width="140" height="{H}" fill="url(#scan{uid})"/></g>
<rect class="edge" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="19" fill="none" stroke="url(#edge{uid})" stroke-width="1.5"/>
<circle class="live" cx="30" cy="34" r="3.5" fill="{accent}"/>
<text class="k" x="42" y="38">{kicker}</text>
<text class="go" x="{W - 26}" y="38" text-anchor="end">OPEN REPORT ↗</text>
<text class="t" x="26" y="74">{title}</text>
<text class="s" x="26" y="96">{sub}</text>
<text class="kpi" x="26" y="160" fill="url(#txt{uid})" filter="url(#neon{uid})">{kpi}</text>
<text class="kl" x="27" y="182">{kpi_label}</text>
{chips(tags, 26, 212)}
<g>{visual}</g>"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}: {sub}">
{css}{defs_common(uid)}<clipPath id="clip{uid}"><rect width="{W}" height="{H}" rx="20"/></clipPath>
{body}
</svg>"""
    with open(os.path.join(OUT, f"card-{name}.svg"), "w") as f:
        f.write(svg)


# visual area: x 290..494, y 110..200
VX0, VX1, VY0, VY1 = 292, 494, 112, 198


def frame():
    out = []
    for i in range(4):
        y = VY0 + (VY1 - VY0) * i / 3
        out.append(f'<line x1="{VX0}" x2="{VX1}" y1="{y:.1f}" y2="{y:.1f}" stroke="{FAINT}" stroke-dasharray="2 4"/>')
    return "".join(out)


def vis_trials():
    r = random.Random(3)
    out = []
    n = 9
    for i in range(n):
        y = VY0 + 4 + i * 10.5
        st = VX0 + r.random() * 30
        stop = i in (2, 5, 7)
        end = st + (VX1 - st) * (0.3 + r.random() * 0.35) if stop else VX1 - r.random() * 10
        col = MUTED if stop else CY
        out.append(f'<line class="grow" style="animation-delay:{i * .12:.2f}s" x1="{st:.1f}" x2="{end:.1f}" y1="{y:.1f}" y2="{y:.1f}" stroke="{col}" stroke-opacity="{.45 if stop else .95}" stroke-width="4.5" stroke-linecap="round"/>')
        if stop:
            out.append(f'<path class="pop" style="animation-delay:{i * .12 + .6:.2f}s" d="M{end - 5:.1f},{y - 5:.1f} L{end + 5:.1f},{y + 5:.1f} M{end + 5:.1f},{y - 5:.1f} L{end - 5:.1f},{y + 5:.1f}" stroke="{PK}" stroke-width="2.4" stroke-linecap="round" filter="url(#neontrials)"/>')
        else:
            out.append(f'<circle class="pop" style="animation-delay:{i * .12 + .6:.2f}s" cx="{end:.1f}" cy="{y:.1f}" r="3" fill="{LIME}"/>')
    return "".join(out)


def vis_km():
    r = random.Random(11)
    out = [frame()]
    for col, hz, d in [(CY, .004, 0), (AMB, .022, .3), (PK, .03, .6)]:
        s, x, y = 1.0, VX0, VY0
        pts = [f"M{x:.1f},{y:.1f}"]
        ticks = []
        steps = 34
        for i in range(1, steps + 1):
            nx = VX0 + (VX1 - VX0) * i / steps
            pts.append(f"H{nx:.1f}")
            if r.random() < .6:
                s *= 1 - hz * (2 + r.random() * 5)
                y = VY0 + (VY1 - VY0) * (1 - s)
                pts.append(f"V{y:.1f}")
            if r.random() < .12:
                ticks.append((nx - 2, y))
        out.append(f'<path class="draw" pathLength="1" style="animation-delay:{d}s" d="{"".join(pts)}" fill="none" stroke="{col}" stroke-width="2.3" filter="url(#neoncdisc)"/>')
        for tx, ty in ticks:
            out.append(f'<line class="pop" style="animation-delay:{d + 1:.1f}s" x1="{tx:.1f}" x2="{tx:.1f}" y1="{ty - 4:.1f}" y2="{ty + 4:.1f}" stroke="{col}" stroke-width="1.4"/>')
    lx = VX0
    for lab, col in [("placebo", CY), ("low", AMB), ("high", PK)]:
        out.append(f'<circle cx="{lx + 4}" cy="{VY1 + 12}" r="3" fill="{col}"/><text x="{lx + 11}" y="{VY1 + 16}" font-family="{MONO}" font-size="10" fill="{MUTED}">{lab}</text>')
        lx += 62
    return "".join(out)


def vis_barley():
    r = random.Random(5)
    out = []
    n = 26
    bw = (VX1 - VX0) / n
    for i in range(n):
        x = (i - n * .55) / (n * .22)
        h = math.exp(-x * x / 2) * (VY1 - VY0) * .95 + 3
        bad = i < 5
        col = PK if bad else AMB
        out.append(f'<rect class="rise" style="animation-delay:{i * .04:.2f}s" x="{VX0 + i * bw + 1:.1f}" y="{VY1 - h:.1f}" width="{bw - 2:.1f}" height="{h:.1f}" rx="1.5" fill="{col}" fill-opacity="{.95 if bad else .75}"/>')
    xq = VX0 + 5 * bw
    out.append(f'<line class="pop" x1="{xq:.1f}" x2="{xq:.1f}" y1="{VY0 - 4}" y2="{VY1}" stroke="{PK}" stroke-dasharray="3 3"/><text class="pop" x="{xq + 5:.1f}" y="{VY0 + 6}" font-family="{MONO}" font-size="10" fill="{PK}">1-in-10</text>')
    return "".join(out)


def vis_grid():
    r = random.Random(8)
    pts = [(VX0 + 8 + r.random() * (VX1 - VX0 - 16), VY0 + r.random() * (VY1 - VY0 + 10)) for _ in range(18)]
    out = []
    for i, p in enumerate(pts):
        near = sorted(range(len(pts)), key=lambda j: (pts[j][0] - p[0]) ** 2 + (pts[j][1] - p[1]) ** 2)[1:3]
        for j in near:
            if j > i:
                out.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{pts[j][0]:.1f}" y2="{pts[j][1]:.1f}" stroke="{VI}" stroke-opacity=".45"/>')
    for i, (x, y) in enumerate(pts):
        short = i % 3 == 0
        col = PK if short else CY
        if short:
            out.append(f'<circle class="ring" style="animation-delay:{i * .2:.1f}s" cx="{x:.1f}" cy="{y:.1f}" r="5" fill="none" stroke="{PK}"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{4 if short else 2.8}" fill="{col}" filter="url(#neongrid)"/>')
    return "".join(out)


def vis_load():
    n = 70
    f = lambda t: .5 - .25 * math.sin(t * math.pi * 4 - 1.2) - .12 * math.sin(t * math.pi * 8 + .4)
    xs = [VX0 + (VX1 - VX0) * i / n for i in range(n + 1)]
    ys = [VY0 + (VY1 - VY0) * f(i / n) for i in range(n + 1)]
    band = "M" + " L".join(f"{x:.1f},{y - 9:.1f}" for x, y in zip(xs, ys)) + " L" + " L".join(f"{x:.1f},{y + 9:.1f}" for x, y in reversed(list(zip(xs, ys)))) + " Z"
    r = random.Random(2)
    act = "M" + " L".join(f"{x:.1f},{y + (r.random() - .5) * 8:.1f}" for x, y in zip(xs, ys))
    fc = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    return (frame() + f'<path class="pop" d="{band}" fill="{VI}" fill-opacity=".22"/>'
            f'<path class="pop" d="{fc}" fill="none" stroke="{VI}" stroke-width="2" stroke-dasharray="5 4"/>'
            f'<path class="draw" pathLength="1" style="animation-delay:.4s" d="{act}" fill="none" stroke="{CY}" stroke-width="2.3" filter="url(#neonload)"/>')


def vis_health():
    r = random.Random(4)
    out = []
    cx, cy = (VX0 + VX1) / 2, (VY0 + VY1) / 2 + 4
    st = 9
    for yy in range(VY0 - 4, VY1 + 12, st):
        for xx in range(VX0, VX1, st):
            ox = xx + (st / 2 if (yy // st) % 2 else 0)
            dx, dy = (ox - cx) / 62, (yy - cy) / 52
            if dx * dx + dy * dy + math.sin(ox * .05) * .12 > 1:
                continue
            v = r.random() * .6 + (.4 if dx < -.15 and dy > -.1 else 0)
            col = PK if v > .8 else VI if v > .55 else CY
            op = .95 if v > .55 else .35
            cls = ' class="pulse"' if v > .9 else ""
            out.append(f'<circle{cls} style="animation-delay:{r.random() * 2:.1f}s" cx="{ox:.1f}" cy="{yy}" r="3.1" fill="{col}" fill-opacity="{op}"/>')
    return "".join(out)


def vis_flow():
    n = 80
    q = VY0 + (VY1 - VY0) * .72
    xs = [VX0 + (VX1 - VX0) * i / n for i in range(n + 1)]
    ys = [VY0 + 18 + (VY1 - VY0 - 10) * (.42 - .45 * math.cos(i / n * math.pi * 5)) for i in range(n + 1)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    out = [f'<line x1="{VX0}" x2="{VX1}" y1="{q:.1f}" y2="{q:.1f}" stroke="{PK}" stroke-dasharray="4 4" stroke-opacity=".8"/>',
           f'<text x="{VX1}" y="{q - 5:.1f}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{PK}">Q95 low flow</text>',
           f'<path class="draw" pathLength="1" d="{d}" fill="none" stroke="{CY}" stroke-width="2.4" filter="url(#neonflow)"/>']
    for i in range(n):
        if ys[i] > q and ys[i - 1] <= q:
            out.append(f'<circle class="ring" cx="{xs[i]:.1f}" cy="{q:.1f}" r="5" fill="none" stroke="{PK}"/><circle cx="{xs[i]:.1f}" cy="{q:.1f}" r="3" fill="{PK}"/>')
    return "".join(out)


def vis_jobs():
    n = 60
    fx = .72
    f = lambda t: .2 + .55 * math.exp(-(((t - .4) / .13) ** 2)) + .05 * math.sin(t * 30) * .4
    xs = [VX0 + (VX1 - VX0) * fx * i / n for i in range(n + 1)]
    ys = [VY1 - (VY1 - VY0) * f(fx * i / n) for i in range(n + 1)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    x0, y0 = xs[-1], ys[-1]
    fan = f"M{x0:.1f},{y0:.1f} L{VX1},{y0 - 26:.1f} L{VX1},{y0 + 26:.1f} Z"
    return (frame() + f'<path class="draw" pathLength="1" d="{d}" fill="none" stroke="{CY}" stroke-width="2.4" filter="url(#neonjobs)"/>'
            f'<path class="pop" d="{fan}" fill="{PK}" fill-opacity=".22"/>'
            f'<line class="pop" x1="{x0:.1f}" y1="{y0:.1f}" x2="{VX1}" y2="{y0 - 3:.1f}" stroke="{PK}" stroke-width="2" stroke-dasharray="4 3"/>'
            f'<line x1="{x0:.1f}" x2="{x0:.1f}" y1="{VY0}" y2="{VY1}" stroke="{MUTED}" stroke-opacity=".4" stroke-dasharray="2 3"/>'
            f'<text x="{x0 + 4:.1f}" y="{VY0 + 8}" font-family="{MONO}" font-size="10" fill="{MUTED}">forecast</text>')


def vis_h7n9():
    # PCA-style paths: three strains drift along PC1, H7N9 peels off on its own axis
    out = [frame()]
    x0, y0 = VX0 + 10, VY1 - 22
    paths = [(CY, [(x0, y0), (x0 + 40, y0 + 2), (x0 + 110, y0 + 8), (x0 + 175, y0 + 14)]),
             (LIME, [(x0, y0), (x0 + 45, y0 + 4), (x0 + 120, y0 + 5), (x0 + 185, y0 + 10)]),
             (VI, [(x0, y0), (x0 + 50, y0 - 6), (x0 + 125, y0 - 8), (x0 + 190, y0 - 6)]),
             (PK, [(x0, y0), (x0 + 30, y0 - 12), (x0 + 75, y0 - 44), (x0 + 120, y0 - 78)])]
    for i, (c, pts) in enumerate(paths):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        w = 3 if c == PK else 1.8
        out.append(f'<path class="draw" pathLength="1" style="animation-delay:{i * .25:.2f}s" d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-opacity="{1 if c == PK else .7}"{" filter=\"url(#neonh7n9)\"" if c == PK else ""}/>')
        for j, (x, y) in enumerate(pts[1:], 1):
            out.append(f'<circle class="pop" style="animation-delay:{i * .25 + j * .3:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="{2 + j}" fill="{c}" fill-opacity="{1 if c == PK else .75}"/>')
    ex, ey = paths[3][1][-1]
    out.append(f'<circle class="ring" cx="{ex:.1f}" cy="{ey:.1f}" r="6" fill="none" stroke="{PK}"/>')
    out.append(f'<text x="{ex + 10:.1f}" y="{ey + 4:.1f}" font-family="{MONO}" font-size="10" fill="{PK}">H7N9 24 h</text>')
    return "".join(out)


def vis_sog1():
    # phylogram: banana SOG1 (lime) inside the SOG1 clade, an early land-plant copy at the base
    out = [frame()]
    tips = 8
    ys = [VY0 + 8 + i * (VY1 - VY0 - 16) / (tips - 1) for i in range(tips)]
    xr = VX1 - 46
    # (y-index pairs joined, x of join) built bottom-up
    joins = [((0, 1), xr - 26), ((2, 3), xr - 34), ((0.5, 2.5), xr - 60), ((4, 5), xr - 30), ((4.5, 6), xr - 70),
             ((1.5, 5.25), xr - 104), ((3.375, 7), xr - 150)]
    yat = lambda k: ys[0] + k * (ys[1] - ys[0])
    xs = {}
    for i in range(tips):
        xs[float(i)] = xr - (60 if i == 7 else 0)
    for n, ((a, b), xj) in enumerate(joins):
        ya, yb = yat(a), yat(b)
        out.append(f'<path class="draw" pathLength="1" style="animation-delay:{n * .18:.2f}s" d="M{xs[float(a)]:.1f},{ya:.1f} H{xj:.1f} V{yb:.1f} H{xs[float(b)]:.1f}" fill="none" stroke="{MUTED}" stroke-opacity=".8" stroke-width="1.6"/>')
        xs[(a + b) / 2] = xj
    for i, y in enumerate(ys):
        col = LIME if i == 2 else (VI if i == 7 else CY)
        x = xs[float(i)]
        out.append(f'<circle class="pop" style="animation-delay:{1.2 + i * .08:.2f}s" cx="{x + 4:.1f}" cy="{y:.1f}" r="{4.5 if i == 2 else 3}" fill="{col}"{" filter=\"url(#neonsog1)\"" if i == 2 else ""}/>')
    out.append(f'<text x="{xs[2.0] + 12:.1f}" y="{ys[2] + 4:.1f}" font-family="{MONO}" font-size="10" fill="{LIME}">MaSOG1</text>')
    out.append(f'<text x="{xs[7.0] + 12:.1f}" y="{ys[7] + 4:.1f}" font-family="{MONO}" font-size="10" fill="{MUTED}">moss</text>')
    return "".join(out)


CARDS = [
    ("trials", "CLINICAL TRIALS · PYTHON", "Why clinical trials stop early", "40,124 trials · interactive trial explorer", "1 in 6", "stopped early", ["scikit-learn", "API", "risk model"], vis_trials, CY),
    ("cdisc", "CLINICAL · R · CDISC", "Trial safety: SDTM to ADaM", "Alzheimer's drug trial · 254 patients", "100%", "independent QC agreement", ["admiral", "survival", "SQL"], vis_km, PK),
    ("barley", "SUPPLY CHAIN · PYTHON", "Barley, Weather and Beer", "40 years of weather vs Irish harvests · map", "1-in-10", "bad-harvest range", ["forecasting", "Monte Carlo", "map"], vis_barley, AMB),
    ("grid", "ENERGY · PYTHON", "Cork &amp; Dublin 2040 grid plans", "Peak demand, substations and budget", "122", "substations short by 2040", ["Monte Carlo", "Leaflet", "planning"], vis_grid, VI),
    ("load", "ENERGY · FORECASTING", "Irish electricity demand", "Day-ahead forecast with prediction intervals", "34%", "better than benchmark", ["gradient boosting", "time series"], vis_load, CY),
    ("health", "PUBLIC HEALTH · CENSUS", "Health and deprivation", "3,420 Irish communities, Census 2022", "63%", "explained by social factors", ["regression", "clustering"], vis_health, VI),
    ("flow", "WATER · EARLY WARNING", "River low-flow warning", "7-day warning from 21 years of data", "4 of 4", "episodes flagged a week ahead", ["random forest", "hydrology"], vis_flow, CY),
    ("h7n9", "VIROLOGY · R · TRANSCRIPTOMICS", "What makes H7N9 different?", "4 flu strains × 4 time points · 78 arrays", "1,279", "genes unique to H7N9 at 24 h", ["limma", "fgsea", "WGCNA"], vis_h7n9, PK),
    ("sog1", "PLANT GENOMICS · PYTHON", "SOG1 in banana, phase 2", "17 plant genomes · ML tree · promoters", "3×", "SOG1 sites at target genes", ["HMMER", "IQ-TREE", "dN/dS"], vis_sog1, LIME),
    ("jobs", "LABOUR MARKET · FORECASTING", "Irish unemployment outlook", "Four models tested on 56 unseen months", "56", "months of honest backtesting", ["time series", "backtesting"], vis_jobs, PK),
]


# ---------------------------------------------------------------- header
def header():
    Wd, Hd = 1200, 360
    uid = "hdr"
    roles = ["Bioinformatics", "Clinical trial data", "Genomics &amp; microbiome", "Data analysis", "Forecasting &amp; risk"]
    n = len(roles)
    per = 100 / n
    role_css = []
    for i in range(n):
        a = i * per
        role_css.append(f"@keyframes r{i}{{0%,{a:.2f}%{{opacity:0;transform:translateY(10px)}}{a + 2:.2f}%,{a + per - 2:.2f}%{{opacity:1;transform:translateY(0)}}{a + per:.2f}%,100%{{opacity:0;transform:translateY(-10px)}}}}.r{i}{{opacity:0;animation:r{i} {n * 3.2:.1f}s infinite}}")
    css = f"""<style>
.eb{{font:600 13px {MONO};fill:{CY};letter-spacing:3px}}
.nm{{font:800 72px {SANS};letter-spacing:-2px}}
.pr{{font:500 26px {MONO};fill:{MUTED}}}
.ro{{font:700 26px {MONO};fill:{INK}}}
.tl{{font:400 17px {SANS};fill:{MUTED}}}
.cap{{font:600 10.5px {MONO};fill:{MUTED};letter-spacing:2.5px}}
.st{{font:600 12px {MONO};fill:{LIME}}}
.cur{{animation:bk 1s steps(1) infinite}}@keyframes bk{{50%{{opacity:0}}}}
.floor{{animation:fl 3s linear infinite}}@keyframes fl{{from{{transform:translateY(0)}}to{{transform:translateY(24px)}}}}
.dA{{animation:a 4s ease-in-out infinite}}.dB{{animation:b 4s ease-in-out infinite}}
@keyframes a{{0%,100%{{transform:translateX(-62px)}}50%{{transform:translateX(62px)}}}}
@keyframes b{{0%,100%{{transform:translateX(62px)}}50%{{transform:translateX(-62px)}}}}
.zA{{animation:za 4s ease-in-out infinite}}.zB{{animation:zb 4s ease-in-out infinite}}
@keyframes za{{0%,100%{{opacity:1}}25%{{opacity:.55}}50%{{opacity:.25}}75%{{opacity:.55}}}}
@keyframes zb{{0%,100%{{opacity:.25}}25%{{opacity:.55}}50%{{opacity:1}}75%{{opacity:.55}}}}
.rung{{transform-box:fill-box;transform-origin:center;animation:sq 4s ease-in-out infinite}}
@keyframes sq{{0%,50%,100%{{transform:scaleX(1)}}25%,75%{{transform:scaleX(.04)}}}}
.orb{{animation:ob 9s ease-in-out infinite}}@keyframes ob{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(30px,-14px)}}}}
.live{{animation:lv 1.6s ease-in-out infinite}}@keyframes lv{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
.bit{{animation:bt 6s linear infinite}}@keyframes bt{{from{{transform:translateY(-60px)}}to{{transform:translateY(420px)}}}}
{''.join(role_css)}
{REDUCED}@media (prefers-reduced-motion:reduce){{.r0{{opacity:1}}}}
</style>"""
    # perspective floor
    vp_x, vp_y = 900, 190
    floor = []
    for i in range(-14, 15):
        floor.append(f'<line x1="{vp_x}" y1="{vp_y}" x2="{vp_x + i * 90}" y2="{Hd}" stroke="{VI}" stroke-opacity=".18"/>')
    hl = []
    for k in range(12):
        y = vp_y + (k ** 1.7) * 2.2
        if y > Hd + 30:
            break
        hl.append(f'<line x1="560" x2="{Wd}" y1="{y:.1f}" y2="{y:.1f}" stroke="{CY}" stroke-opacity="{.06 + k * .012:.3f}"/>')
    # helix
    hx, top, bot, npair = 905, 46, 300, 17
    helix = []
    for i in range(npair):
        y = top + (bot - top) * i / (npair - 1)
        d = -(i * .23) % 4
        helix.append(f'<line class="rung" style="animation-delay:{d:.2f}s" x1="{hx - 62}" x2="{hx + 62}" y1="{y:.1f}" y2="{y:.1f}" stroke="{MUTED}" stroke-opacity=".28" stroke-width="2"/>')
        helix.append(f'<g class="zA" style="animation-delay:{d:.2f}s"><circle class="dA" style="animation-delay:{d:.2f}s" cx="{hx}" cy="{y:.1f}" r="6" fill="{PK}" filter="url(#neon{uid})"/></g>')
        helix.append(f'<g class="zB" style="animation-delay:{d:.2f}s"><circle class="dB" style="animation-delay:{d:.2f}s" cx="{hx}" cy="{y:.1f}" r="6" fill="{CY}" filter="url(#neon{uid})"/></g>')
    # falling data bits on the far right
    r = random.Random(9)
    bits = []
    for i in range(16):
        x = 1040 + r.random() * 130
        s = "".join(r.choice("ACGT01") for _ in range(6))
        bits.append(f'<text class="bit" style="animation-delay:-{r.random() * 6:.2f}s;animation-duration:{5 + r.random() * 4:.1f}s" x="{x:.1f}" y="0" font-family="{MONO}" font-size="11" fill="{r.choice([CY, VI, PK])}" fill-opacity="{.25 + r.random() * .35:.2f}" writing-mode="tb">{s}</text>')
    roles_svg = "".join(f'<text class="ro r{i}" x="96" y="222">{t}</text>' for i, t in enumerate(roles))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{Hd}" viewBox="0 0 {Wd} {Hd}" role="img" aria-label="Mankirat Singh: bioinformatics, clinical trial data and data analysis, Cork, Ireland">
{css}{defs_common(uid)}
<clipPath id="clip{uid}"><rect width="{Wd}" height="{Hd}" rx="24"/></clipPath>
<linearGradient id="fade{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}" stop-opacity="1"/><stop offset=".25" stop-color="{BG}" stop-opacity="0"/></linearGradient>
<g clip-path="url(#clip{uid})">
<rect width="{Wd}" height="{Hd}" fill="{BG}"/>
<rect width="{Wd}" height="{Hd}" fill="url(#dots{uid})" opacity=".6"/>
<g class="orb"><circle cx="980" cy="120" r="300" fill="url(#glowA{uid})"/></g>
<circle cx="120" cy="330" r="260" fill="url(#glowB{uid})"/>
<g>{''.join(floor)}</g><g class="floor">{''.join(hl)}</g>
<rect x="560" y="{vp_y}" width="{Wd - 560}" height="70" fill="url(#fade{uid})"/>
<g>{''.join(bits)}</g>
<g>{''.join(helix)}</g>
</g>
<rect x="1" y="1" width="{Wd - 2}" height="{Hd - 2}" rx="23" fill="none" stroke="url(#edge{uid})" stroke-opacity=".7" stroke-width="1.5"/>
<text class="eb" x="66" y="86">CORK, IRELAND · MSc BIOINFORMATICS, UCC</text>
<text class="nm" x="62" y="164" fill="url(#txt{uid})" filter="url(#neon{uid})">Mankirat Singh</text>
<text class="pr" x="66" y="222">&gt;</text>
{roles_svg}
<rect class="cur" x="66" y="236" width="14" height="3" fill="{CY}"/>
<text class="tl" x="66" y="272">Real data · honest models · interactive reports</text>
<circle class="live" cx="72" cy="306" r="4.5" fill="{LIME}"/>
<text class="st" x="84" y="310">OPEN TO ROLES IN IRELAND · PhD POSITIONS</text>
<text class="cap" x="905" y="336" text-anchor="middle">16S · NGS · MULTI-OMICS</text>
</svg>"""
    with open(os.path.join(OUT, "header.svg"), "w") as f:
        f.write(svg)


# ---------------------------------------------------------------- terminal "about"
def terminal():
    Wd = 1200
    uid = "term"
    P = f'<tspan fill="{LIME}">mankirat@cork</tspan><tspan fill="{MUTED}">:</tspan><tspan fill="{CY}">~</tspan><tspan fill="{MUTED}">$ </tspan>'
    lines = [
        ("cmd", "whoami"),
        ("out", "Bioinformatician and data analyst · MSc Bioinformatics &amp; Computational Biology, University College Cork"),
        ("cmd", "cat background.txt"),
        ("out", "Wet lab to code: NGS assay development, 16S microbiome, qPCR and in vivo studies, now Python, R and SQL pipelines"),
        ("cmd", "./run_project --check-data --test-on-unseen --report"),
        ("ok", "data fingerprinted (SHA-256)          automatic quality checks passed"),
        ("ok", "tested on data the model never saw    beats a simple baseline"),
        ("ok", "uncertainty shown, limits written down    interactive report published"),
        ("cmd", "echo $LOOKING_FOR"),
        ("out", "Graduate and junior roles in bioinformatics, clinical / life-science data and data analysis · PhD positions"),
    ]
    y0, lh = 74, 27
    Hd = y0 + lh * len(lines) + 34
    n = len(lines)
    total = 11.0
    css_lines = []
    out = []
    for i, (kind, txt) in enumerate(lines):
        t0 = 2 + i * 5.8
        css_lines.append(f"@keyframes l{i}{{0%,{t0:.1f}%{{opacity:0}}{t0 + 1.5:.1f}%,94%{{opacity:1}}100%{{opacity:0}}}}.l{i}{{opacity:0;animation:l{i} {total}s infinite}}")
        y = y0 + i * lh
        if kind == "cmd":
            out.append(f'<text class="m l{i}" x="34" y="{y}">{P}<tspan fill="{INK}">{txt}</tspan></text>')
        elif kind == "ok":
            a, b = txt.split("    ", 1) if "    " in txt else (txt, "")
            out.append(f'<text class="m l{i}" x="34" y="{y}"><tspan fill="{LIME}">✓ </tspan><tspan fill="{INK}">{a.strip()}</tspan></text>')
            if b:
                out.append(f'<text class="m l{i}" x="600" y="{y}"><tspan fill="{LIME}">✓ </tspan><tspan fill="{INK}">{b.strip()}</tspan></text>')
        else:
            out.append(f'<text class="m l{i}" x="34" y="{y}" fill="{MUTED}">{txt}</text>')
    ylast = y0 + n * lh
    css = f"""<style>
.m{{font:500 15px {MONO}}}
.ttl{{font:600 12px {MONO};fill:{MUTED}}}
.cur{{animation:bk 1s steps(1) infinite}}@keyframes bk{{50%{{opacity:0}}}}
{''.join(css_lines)}
{REDUCED}@media (prefers-reduced-motion:reduce){{{"".join(f".l{i}" + ("," if i < n - 1 else "") for i in range(n))}{{opacity:1}}}}
</style>"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{Hd}" viewBox="0 0 {Wd} {Hd}" role="img" aria-label="About Mankirat Singh: bioinformatician and data analyst, MSc UCC; wet lab to code; open to graduate and junior roles and PhD positions">
{css}{defs_common(uid)}
<rect width="{Wd}" height="{Hd}" rx="18" fill="{BG}"/>
<rect width="{Wd}" height="34" rx="18" fill="{BG2}"/><rect y="18" width="{Wd}" height="16" fill="{BG2}"/>
<circle cx="26" cy="17" r="6" fill="#FF5F57"/><circle cx="46" cy="17" r="6" fill="#FEBC2E"/><circle cx="66" cy="17" r="6" fill="#28C840"/>
<text class="ttl" x="{Wd / 2}" y="21" text-anchor="middle">mankirat@cork — zsh — profile</text>
<rect x="1" y="1" width="{Wd - 2}" height="{Hd - 2}" rx="17" fill="none" stroke="url(#edge{uid})" stroke-opacity=".55" stroke-width="1.5"/>
{''.join(out)}
<text class="m" x="34" y="{ylast}">{P}</text><rect class="cur" x="{34 + 17 * 9.05:.0f}" y="{ylast - 14}" width="9" height="17" fill="{CY}"/>
</svg>"""
    with open(os.path.join(OUT, "about.svg"), "w") as f:
        f.write(svg)


# ---------------------------------------------------------------- stats strip
def stats():
    Wd, Hd = 1200, 150
    uid = "stats"
    items = [("17", "research and data projects"), ("10", "live interactive reports"), ("40,124", "clinical trials analysed"), ("100GB+", "sequencing data processed")]
    tw = (Wd - 40 - 3 * 16) / 4
    out = []
    for i, (v, l) in enumerate(items):
        x = 20 + i * (tw + 16)
        out.append(f'<g class="in" style="animation-delay:{i * .25:.2f}s"><rect x="{x:.1f}" y="18" width="{tw:.1f}" height="{Hd - 36}" rx="16" fill="#ffffff" fill-opacity=".025" stroke="url(#edge{uid})" stroke-opacity=".5"/>'
                   f'<text x="{x + 24:.1f}" y="80" class="v" fill="url(#txt{uid})" filter="url(#neon{uid})">{v}</text><text x="{x + 25:.1f}" y="106" class="l">{l}</text></g>')
    css = f"""<style>
.v{{font:800 40px {SANS};letter-spacing:-1px}}.l{{font:500 12.5px {MONO};fill:{MUTED}}}
.in{{}}
{REDUCED}
</style>"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{Hd}" viewBox="0 0 {Wd} {Hd}" role="img" aria-label="17 projects, 10 live interactive reports, 40,124 clinical trials analysed, 100GB+ sequencing data processed">
{css}{defs_common(uid)}
<rect width="{Wd}" height="{Hd}" rx="18" fill="{BG}"/>
{''.join(out)}
</svg>"""
    with open(os.path.join(OUT, "stats.svg"), "w") as f:
        f.write(svg)


# ---------------------------------------------------------------- tools panel
def stack():
    Wd = 1200
    uid = "stack"
    groups = [
        ("LANGUAGES", CY, ["Python", "R", "SQL"]),
        ("BIOINFORMATICS", PK, ["QIIME2", "DADA2", "phyloseq", "mixOmics", "ANCOM-BC2", "limma", "NGS (Illumina)"]),
        ("CLINICAL DATA", AMB, ["CDISC SDTM / ADaM", "admiral", "survival analysis", "diffdf double programming"]),
        ("MODELLING", VI, ["scikit-learn", "gradient boosting", "random forest", "time series", "Monte Carlo"]),
        ("ENGINEERING", LIME, ["Git", "GitHub Pages", "DuckDB", "testthat", "reproducible pipelines"]),
    ]
    y, out = 56, []
    for name, col, items in groups:
        out.append(f'<circle cx="34" cy="{y - 4}" r="4" fill="{col}" filter="url(#neon{uid})"/><text x="48" y="{y}" class="g" fill="{col}">{name}</text>')
        x = 250
        for it in items:
            w = text_w(it, 13) + 26
            out.append(f'<rect x="{x:.1f}" y="{y - 19}" width="{w:.1f}" height="28" rx="14" fill="{col}" fill-opacity=".07" stroke="{col}" stroke-opacity=".45"/><text x="{x + w / 2:.1f}" y="{y}" class="c" text-anchor="middle">{it}</text>')
            x += w + 9
        y += 46
    Hd = y - 10
    css = f"""<style>.g{{font:700 12px {MONO};letter-spacing:2.5px}}.c{{font:500 13px {SANS};fill:{INK}}}{REDUCED}</style>"""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{Hd}" viewBox="0 0 {Wd} {Hd}" role="img" aria-label="Tools: Python, R, SQL; QIIME2, DADA2, phyloseq, mixOmics, ANCOM-BC2, limma, NGS; CDISC SDTM/ADaM, admiral, survival analysis, diffdf; scikit-learn, gradient boosting, random forest, time series, Monte Carlo; Git, GitHub Pages, DuckDB, testthat">
{css}{defs_common(uid)}
<rect width="{Wd}" height="{Hd}" rx="18" fill="{BG}"/>
<rect x="1" y="1" width="{Wd - 2}" height="{Hd - 2}" rx="17" fill="none" stroke="url(#edge{uid})" stroke-opacity=".4"/>
{''.join(out)}
</svg>"""
    with open(os.path.join(OUT, "stack.svg"), "w") as f:
        f.write(svg)


# ---------------------------------------------------------------- section titles
def section(name, label, num):
    Wd, Hd = 1200, 64
    uid = f"sec{name}"
    css = f"""<style>.n{{font:700 13px {MONO};fill:{CY};letter-spacing:2px}}.h{{font:800 26px {SANS};fill:{INK};letter-spacing:-.5px}}
.ln{{stroke-dasharray:900;stroke-dashoffset:900;animation:ln 5s ease-out infinite}}@keyframes ln{{0%{{stroke-dashoffset:900}}40%,100%{{stroke-dashoffset:0}}}}{REDUCED}</style>"""
    lw = text_w(label, 26, 800) + 70
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{Wd}" height="{Hd}" viewBox="0 0 {Wd} {Hd}" role="img" aria-label="{label}">
{css}{defs_common(uid)}
<text class="n" x="4" y="40">{num}</text><text class="h" x="44" y="42">{label}</text>
<line class="ln rm" x1="{44 + lw:.0f}" x2="{Wd - 4}" y1="33" y2="33" stroke="url(#edge{uid})" stroke-width="1.5"/>
<circle cx="{Wd - 6}" cy="33" r="3.5" fill="{PK}" filter="url(#neon{uid})"/>
</svg>"""
    with open(os.path.join(OUT, f"section-{name}.svg"), "w") as f:
        f.write(svg)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for c in CARDS:
        card(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7](), c[8])
    header(); terminal(); stats(); stack()
    section("work", "Featured work", "01"); section("tools", "Tools and methods", "02")
    print("built", sorted(os.listdir(OUT)))
