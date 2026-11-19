"""Reel-Titelbilder (1080x1920) für Video 03 im Look der Video-03-Thumbnails. Wichtiges im 3:4-Ausschnitt (y 240–1680).

Aufruf: python3 gen_reelcover03.py  ->  je Projekt hyperframes snapshot --at 0
"""
import os, sys, random, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "produktion", "video01"))
sys.path.insert(0, os.path.join(HERE, "..", "produktion", "video01-hf"))
from rig import otto_svg  # noqa: E402

AMBER, RED = "#E8C27A", "#FF3B2F"
NOISE = ("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence "
         "type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")


def light(x, y, r, col):
    return (f'<div style="position:absolute;left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;'
            f'background:radial-gradient(circle, {col} 0%, transparent 70%);"></div>')


def film(dark=True):
    r = random.Random(7)
    dust = "".join(f'<div style="position:absolute;left:{r.uniform(0, 1080):.0f}px;top:{r.uniform(0, 1920):.0f}px;width:3px;height:3px;border-radius:50%;'
                   f'background:rgba(255,236,205,{r.uniform(.15, .4):.2f});"></div>' for _ in range(70)) if dark else ""
    vig = "rgba(0,0,0,.65)" if dark else "rgba(120,40,0,.45)"
    return (dust + f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%, transparent 45%, {vig} 100%);"></div>'
            f'<div style="position:absolute;inset:0;background-image:url(&quot;{NOISE}&quot;);background-size:256px 256px;opacity:.12;mix-blend-mode:overlay;"></div>')


def otto(x, y, s, faces, **kw):
    """x,y = Kopfmitte im Thumbnail."""
    return (f'<div style="position:absolute;left:{x - 300 * s:.0f}px;top:{y - 200 * s:.0f}px;width:{600 * s:.0f}px;height:{760 * s:.0f}px;">'
            f'<div style="position:absolute;left:0;top:0;width:600px;height:760px;transform:scale({s});transform-origin:0 0">'
            f'{otto_svg("t", faces, **kw)}</div></div>')


def laptop(cx, top, w):
    """Laptop von hinten (Deckel), davor leuchtet der Bildschirm nach oben aufs Gesicht."""
    h = w * .62
    return (f'<div style="position:absolute;left:{cx - w * .75:.0f}px;top:{top - h * 1.1:.0f}px;width:{w * 1.5:.0f}px;height:{h * 2.2:.0f}px;'
            f'background:radial-gradient(ellipse at 50% 64%, rgba(170,210,255,.55) 0%, transparent 65%);mix-blend-mode:screen;"></div>'
            f'<div style="position:absolute;left:{cx - w / 2:.0f}px;top:{top:.0f}px;width:{w:.0f}px;height:{h:.0f}px;border-radius:16px 16px 4px 4px;'
            f'background:linear-gradient(180deg,#3A3D44,#202227);border:3px solid #4A4E57;box-shadow:0 -6px 30px rgba(170,210,255,.45);"></div>'
            f'<div style="position:absolute;left:{cx - 22:.0f}px;top:{top + h * .42:.0f}px;width:44px;height:44px;border-radius:50%;background:#FF7A1A;opacity:.85;"></div>')


def sparks(cx, cy, r0, r1, n, col, seed=3):
    rnd = random.Random(seed)
    out = ""
    for i in range(n):
        a = -math.pi * (0.05 + 0.9 * i / (n - 1)) + rnd.uniform(-.08, .08)
        l = rnd.uniform(r0, r1) - r0
        x, y = cx + math.cos(a) * r0, cy + math.sin(a) * r0
        out += (f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{l:.0f}px;height:7px;border-radius:4px;background:{col};'
                f'transform-origin:0 50%;transform:rotate({math.degrees(a):.0f}deg);box-shadow:0 0 12px {col};"></div>')
    return out


def clock(x, y, size, txt="23:58", label=None):
    lab = (f'<div style="font-size:{size * .22:.0f}px;font-weight:800;letter-spacing:.3em;color:{RED};opacity:.85;margin-bottom:{size * .05:.0f}px;">{label}</div>'
           if label else "")
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;padding:{size * .12:.0f}px {size * .2:.0f}px;background:#120606;border:4px solid #5A1612;'
            f'border-radius:{size * .12:.0f}px;box-shadow:0 0 50px rgba(255,59,47,.35), inset 0 0 20px rgba(255,59,47,.15);">{lab}'
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:{size}px;line-height:1;color:{RED};'
            f'text-shadow:0 0 18px rgba(255,59,47,.85), 0 0 40px rgba(255,59,47,.5);">{txt}</div></div>')


def project(name, body):
    d = f"{HERE}/reel03_{name}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w").write(f"""<!doctype html>
<html lang="de"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0B0C0E; }}
#root {{ position:absolute; inset:0; overflow:hidden; font-family:'Inter', sans-serif; color:#FFF; }}
#root .cond {{ font-family:'Oswald', sans-serif; font-weight:700; text-transform:uppercase; line-height:.95; }}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="1" data-width="1080" data-height="1920" data-no-timeline>
{body}
</div></body></html>""")
    for fn in ("hyperframes.json", "package.json", "meta.json"):
        src = os.path.join(HERE, "..", "produktion", "video01-doku", fn)
        open(f"{d}/{fn}", "w").write(open(src).read().replace("otto-video01-doku", f"otto-reel03-{name}"))



WATER = "#8EC5FF"
BULB = """<g stroke="#111" stroke-width="5"><path d="M-30,30 a60,60 0 1 1 60,0 l0,40 l-60,0 Z" fill="#FFD43B"/><rect x="-32" y="70" width="64" height="26" rx="6" fill="#9AA0A6"/></g>"""


def foam(hx, hy, s):
    """Shampoo-Schaum auf Ottos Kopf (hx, hy = Kopfmitte)."""
    blobs = [(-130, -130, 100), (-60, -170, 120), (30, -175, 120), (120, -145, 100), (170, -95, 70), (-155, -80, 70), (110, -75, 60), (-20, -120, 90)]
    return "".join(f'<div style="position:absolute;left:{hx + dx * s:.0f}px;top:{hy + dy * s:.0f}px;width:{r * s:.0f}px;height:{r * s:.0f}px;border-radius:50%;'
                   f'background:radial-gradient(circle at 35% 30%,#FFFFFF,#E3E9F1);border:{3 * s:.0f}px solid #B9C3D0"></div>' for dx, dy, r in blobs)


def shower(cx, top, s, col="#9AA0AA"):
    head = (f'<div style="position:absolute;left:{cx - 150 * s:.0f}px;top:{top:.0f}px;width:{300 * s:.0f}px;height:{40 * s:.0f}px;border-radius:{20 * s:.0f}px;background:{col}"></div>'
            f'<div style="position:absolute;left:{cx + 120 * s:.0f}px;top:{top - 120 * s:.0f}px;width:{30 * s:.0f}px;height:{140 * s:.0f}px;background:#7A808A"></div>')
    streams = "".join(f'<div style="position:absolute;left:{cx - 130 * s + i * 22 * s:.0f}px;top:{top + 40 * s:.0f}px;width:{4 * s:.1f}px;height:{720:.0f}px;'
                      f'background:repeating-linear-gradient(180deg,rgba(142,197,255,0) 0 18px,rgba(142,197,255,.55) 18px 54px)"></div>' for i in range(13))
    return head + streams


def bulb(x, y, s, glow="rgba(255,220,120,.6)"):
    return (light(x, y, 210 * s, glow)
            + f'<div style="position:absolute;left:{x - 100 * s:.0f}px;top:{y - 110 * s:.0f}px;width:{200 * s:.0f}px;height:{230 * s:.0f}px">'
            f'<svg viewBox="-100 -110 200 230" width="{200 * s:.0f}" height="{230 * s:.0f}">{BULB}</svg></div>')


def drops(seed, n, col):
    import random as _r
    r = _r.Random(seed)
    return "".join(f'<div style="position:absolute;left:{r.uniform(120, 960):.0f}px;top:{r.uniform(300, 1600):.0f}px;width:10px;height:22px;border-radius:50% 50% 50% 50% / 60% 60% 40% 40%;background:{col};opacity:.75"></div>' for _ in range(n))



BADGE = lambda bg, fg, top: (f'<div style="position:absolute;left:0;width:1080px;top:{top}px;text-align:center">'
                             f'<span style="display:inline-block;padding:14px 34px;border-radius:50px;background:{bg};color:{fg};font-size:46px;font-weight:900;letter-spacing:.06em">'
                             f'⏱ IN 60 SEKUNDEN ERKLÄRT</span></div>')

# A: dunkel, Dusche + Otto mit Schaum, „WARUM HIER?!“
project("a_warum", f"""
  <div style="position:absolute;inset:0;background:#0B0C0E;"></div>
  {light(540, 1220, 560, "rgba(142,197,255,.22)")}
  {shower(540, 955, 1.25)}
  {otto(540, 1210, 1.25, ("aha",))}
  {foam(540, 1210, 1.25)}
  {bulb(860, 980, 0.8)}
  <div style="position:absolute;left:0;width:1080px;top:290px;text-align:center;font-size:40px;font-weight:800;letter-spacing:.3em;color:{AMBER};">DIE BESTE IDEE …</div>
  <div class="cond" style="position:absolute;left:0;width:1080px;text-align:center;top:350px;font-size:200px;color:#FFF;text-shadow:0 10px 30px rgba(0,0,0,.7);">WARUM<br><span style="color:{AMBER}">HIER?!</span></div>
  {BADGE("#16181D;border:3px solid " + AMBER, "#FFF", 735)}
  {film(True)}""")

# B: orange, „AHA?!“
project("b_orange", f"""
  <div style="position:absolute;inset:0;background:#FF7A1A;"></div>
  {light(540, 1220, 600, "rgba(255,236,200,.55)")}
  {drops(4, 34, "#FFFFFF")}
  {otto(540, 1210, 1.25, ("aha",))}
  {foam(540, 1210, 1.25)}
  {bulb(860, 980, 0.8, "rgba(255,255,220,.75)")}
  <div class="cond" style="position:absolute;left:0;width:1080px;text-align:center;top:330px;font-size:300px;color:#FFF;-webkit-text-stroke:8px #1E1E1E;text-shadow:0 12px 0 #1E1E1E;">AHA?!</div>
  {BADGE("#1E1E1E", "#FFF", 700)}
  {film(False)}""")
print("ok")
