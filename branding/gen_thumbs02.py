"""Thumbnails für Video 02 „Warum du kurz vor der Deadline plötzlich ein Genie bist“ (1280x720), drei Varianten zum A/B-Testen.

Aufruf: python3 gen_thumbs02.py  ->  je Projekt hyperframes snapshot --at 0
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
    dust = "".join(f'<div style="position:absolute;left:{r.uniform(0, 1280):.0f}px;top:{r.uniform(0, 720):.0f}px;width:3px;height:3px;border-radius:50%;'
                   f'background:rgba(255,236,205,{r.uniform(.15, .4):.2f});"></div>' for _ in range(40)) if dark else ""
    vig = "rgba(0,0,0,.65)" if dark else "rgba(120,40,0,.45)"
    return (dust + f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 55% 50%, transparent 45%, {vig} 100%);"></div>'
            f'<div style="position:absolute;inset:0;background-image:url(&quot;{NOISE}&quot;);background-size:256px 256px;opacity:.12;mix-blend-mode:overlay;"></div>')


def otto(x, y, s, faces, **kw):
    """x,y = Kopfmitte im Thumbnail."""
    return (f'<div style="position:absolute;left:{x - 300 * s:.0f}px;top:{y - 200 * s:.0f}px;width:{600 * s:.0f}px;height:{760 * s:.0f}px;">'
            f'<div style="position:absolute;left:0;top:0;width:600px;height:760px;transform:scale({s});transform-origin:0 0">'
            f'{otto_svg("t", faces, **kw)}</div></div>')


def laptop(cx, top, w):
    """Laptop von hinten (Deckel), davor leuchtet der Bildschirm nach oben aufs Gesicht."""
    h = w * .62
    return (f'<div style="position:absolute;left:{cx - w * .75:.0f}px;top:{top - h * 1.1:.0f}px;width:{w * 1.5:.0f}px;height:{h * 1.4:.0f}px;'
            f'background:radial-gradient(ellipse at 50% 100%, rgba(170,210,255,.55) 0%, transparent 65%);mix-blend-mode:screen;"></div>'
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
    d = f"{HERE}/thumb02_{name}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w").write(f"""<!doctype html>
<html lang="de"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1280, height=720" />
<style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1280px; height:720px; overflow:hidden; background:#0B0C0E; }}
#root {{ position:absolute; inset:0; overflow:hidden; font-family:'Inter', sans-serif; color:#FFF; }}
#root .cond {{ font-family:'Oswald', sans-serif; font-weight:700; text-transform:uppercase; line-height:.95; }}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="1" data-width="1280" data-height="720" data-no-timeline>
{body}
</div></body></html>""")
    for fn in ("hyperframes.json", "package.json", "meta.json"):
        src = os.path.join(HERE, "..", "produktion", "video01-doku", fn)
        open(f"{d}/{fn}", "w").write(open(src).read().replace("otto-video01-doku", f"otto-thumb02-{name}"))


# A: dunkel, Otto schockiert hinter dem Laptop, Funken, rote Uhr 23:58, „GENIE?“
project("a_genie", f"""
  <div style="position:absolute;inset:0;background:#0B0C0E;"></div>
  {light(960, 300, 430, "rgba(255,226,180,.30)")}
  {sparks(960, 250, 250, 330, 9, AMBER)}
  {otto(960, 270, 1.15, ("shock",))}
  {laptop(960, 520, 360)}
  {clock(58, 70, 120, "23:58", "FREITAG")}
  <div class="cond" style="position:absolute;left:48px;top:330px;font-size:250px;color:{AMBER};text-shadow:0 10px 30px rgba(0,0,0,.7);">GENIE?</div>
  {film(True)}""")

# B: dunkel, Otto grinst mit Glühbirne, Text „UNTER DRUCK BESSER?“ + Uhr
project("b_druck", f"""
  <div style="position:absolute;inset:0;background:#0B0C0E;"></div>
  {light(960, 330, 440, "rgba(255,226,180,.32)")}
  {light(1150, 120, 160, "rgba(255,214,110,.75)")}
  <div style="position:absolute;left:1112px;top:58px;font-size:96px;line-height:1;">💡</div>
  {otto(950, 300, 1.2, ("smirk",))}
  {laptop(950, 545, 340)}
  <div class="cond" style="position:absolute;left:56px;top:110px;font-size:140px;text-shadow:0 8px 30px rgba(0,0,0,.6);">UNTER<br>DRUCK<br><span style="color:{AMBER}">BESSER?</span></div>
  {clock(62, 545, 74, "23:58")}
  {film(True)}""")

# C: orange (Kontrast-Test), riesige Uhr, „GENIE?“ mit Strich, Otto schockiert
project("c_orange", f"""
  <div style="position:absolute;inset:0;background:#FF7A1A;"></div>
  {light(1010, 330, 460, "rgba(255,236,200,.55)")}
  {sparks(1010, 270, 245, 320, 9, "#1E1E1E", 5)}
  {otto(1010, 290, 1.15, ("shock",))}
  {laptop(1010, 540, 340)}
  {clock(50, 60, 130, "23:58")}
  <div class="cond" style="position:absolute;left:48px;top:300px;font-size:230px;color:#FFF;-webkit-text-stroke:6px #1E1E1E;text-shadow:0 10px 0 #1E1E1E;">GENIE?</div>
  <div style="position:absolute;left:58px;top:585px;padding:10px 22px;background:#1E1E1E;font-size:38px;font-weight:900;letter-spacing:.06em;">ODER NUR EIN TRICK</div>
  {film(False)}""")
print("ok")
