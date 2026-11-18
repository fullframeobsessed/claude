"""Thumbnails für Video 01 (1280x720) in drei Varianten für YouTube „Testen und vergleichen“.

Aufruf: python3 gen_thumbs.py  ->  je Projekt hyperframes snapshot --at 0
"""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "produktion", "video01"))
sys.path.insert(0, os.path.join(HERE, "..", "produktion", "video01-hf"))
from rig import otto_svg  # noqa: E402

AMBER, RED = "#E8C27A", "#E2483D"
NOISE = ("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence "
         "type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")


def light(x, y, r, col):
    return (f'<div style="position:absolute;left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;'
            f'background:radial-gradient(circle, {col} 0%, transparent 70%);"></div>')


def film(dark=True):
    r = random.Random(5)
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


def project(name, body):
    d = f"{HERE}/thumb_{name}"
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
        open(f"{d}/{fn}", "w").write(open(src).read().replace("otto-video01-doku", f"otto-thumb-{name}"))


# A: dunkel, „FAUL?“ durchgestrichen, Otto ertappt (Schweißtropfen)
project("a_faul", f"""
  <div style="position:absolute;inset:0;background:#0B0C0E;"></div>
  {light(930, 330, 420, "rgba(255,226,180,.38)")}
  {otto(930, 300, 1.25, ("excuse",))}
  <div style="position:absolute;left:60px;top:150px;font-size:34px;font-weight:800;letter-spacing:.3em;color:{AMBER};">DU BIST NICHT</div>
  <div class="cond" style="position:absolute;left:50px;top:200px;font-size:300px;text-shadow:0 8px 30px rgba(0,0,0,.6);">FAUL</div>
  <div style="position:absolute;left:40px;top:330px;width:560px;height:26px;background:{RED};transform:rotate(-8deg);box-shadow:0 4px 20px rgba(0,0,0,.5);"></div>
  {film(True)}""")

# B: dunkel, Nahaufnahme Tasse „SPÄTER“, Otto grinst
project("b_spaeter", f"""
  <div style="position:absolute;inset:0;background:#0B0C0E;"></div>
  {light(900, 380, 460, "rgba(255,226,180,.36)")}
  {otto(860, 150, 1.9, ("smirk",), pose="bent", item="mug", label="SPÄTER")}
  <div class="cond" style="position:absolute;left:60px;top:170px;font-size:150px;text-shadow:0 8px 30px rgba(0,0,0,.6);">MACH ICH<br><span style="color:{AMBER}">MORGEN.</span></div>
  <div style="position:absolute;left:66px;top:485px;font-size:34px;font-weight:800;letter-spacing:.25em;color:#D9D4C7;">WARUM EIGENTLICH?</div>
  {film(True)}""")

# C: hell/orange (Kontrast-Test), „FAUL?“ mit schwarzem Strich, Otto schockiert
project("c_orange", f"""
  <div style="position:absolute;inset:0;background:#FF7A1A;"></div>
  {light(1010, 320, 460, "rgba(255,236,200,.55)")}
  {otto(1020, 300, 1.25, ("shock",))}
  <div class="cond" style="position:absolute;left:50px;top:180px;font-size:270px;color:#FFF;-webkit-text-stroke:6px #1E1E1E;text-shadow:0 10px 0 #1E1E1E;">FAUL?</div>
  <div style="position:absolute;left:40px;top:315px;width:540px;height:30px;background:#1E1E1E;transform:rotate(-8deg);"></div>
  <div style="position:absolute;left:60px;top:520px;padding:10px 22px;background:#1E1E1E;font-size:40px;font-weight:900;letter-spacing:.06em;">ES IST WAS ANDERES</div>
  {film(False)}""")
print("ok")
