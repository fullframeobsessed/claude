"""Erzeugt YouTube-Banner (2560x1440) und Profilbilder (800x800) für „Otto Normalpsyche“ als HyperFrames-Standbilder.

Aufruf: python3 gen_branding.py  ->  danach je Projekt: hyperframes snapshot --at 0
"""
import os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "produktion", "video01"))
sys.path.insert(0, os.path.join(HERE, "..", "produktion", "video01-hf"))
import art  # noqa: E402
from rig import otto_svg  # noqa: E402

AMBER, MUTED = "#E8C27A", "#8C8F96"
NOISE = ("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence "
         "type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")


def light(x, y, r, col):
    return (f'<div style="position:absolute;left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;'
            f'background:radial-gradient(circle, {col} 0%, transparent 70%);"></div>')


def dust(w, h, n, seed):
    r = random.Random(seed)
    out = ""
    for _ in range(n):
        x, y, s = r.uniform(0, w), r.uniform(0, h), r.uniform(2, 6)
        out += (f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{s:.1f}px;height:{s:.1f}px;border-radius:50%;'
                f'background:rgba(255,236,205,{r.uniform(.15, .45):.2f});filter:blur(1px);"></div>')
    return out


def film(w, h):
    return (f'<div style="position:absolute;inset:0;background:#5a3c14;mix-blend-mode:soft-light;opacity:.35;"></div>'
            f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%, transparent 40%, rgba(0,0,0,.72) 100%);"></div>'
            f'<div style="position:absolute;inset:0;background-image:url(&quot;{NOISE}&quot;);background-size:256px 256px;opacity:.14;mix-blend-mode:overlay;"></div>')


def project(name, w, h, body):
    d = f"{HERE}/{name}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/index.html", "w").write(f"""<!doctype html>
<html lang="de"><head><meta charset="UTF-8" /><meta name="viewport" content="width={w}, height={h}" />
<style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:{w}px; height:{h}px; overflow:hidden; background:#0B0C0E; }}
#root {{ position:absolute; inset:0; overflow:hidden; font-family:'Inter', sans-serif; color:#FFF; }}
#root .cond {{ font-family:'Oswald', sans-serif; font-weight:700; text-transform:uppercase; }}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="1" data-width="{w}" data-height="{h}" data-no-timeline>
{body}
</div></body></html>""")
    for fn in ("hyperframes.json", "package.json", "meta.json"):
        src = os.path.join(HERE, "..", "produktion", "video01-doku", fn)
        open(f"{d}/{fn}", "w").write(open(src).read().replace("otto-video01-doku", f"otto-{name}"))


# ------------------------------------------------------------------ Banner 2560x1440
# Sicherer Bereich (überall sichtbar): 1546x423 mittig -> x 507..2053, y 508..931
otto_s = 0.5
banner = f"""
  <div style="position:absolute;inset:0;background:#0B0C0E;"></div>
  {light(730, 720, 420, "rgba(255,226,180,.30)")}
  {light(1500, 700, 700, "rgba(255,226,180,.10)")}
  {light(2300, 640, 380, "rgba(140,190,255,.12)")}
  {light(260, 760, 380, "rgba(240,180,90,.12)")}
  <div style="position:absolute;left:{730 - 300 * otto_s:.0f}px;top:{605 - 200 * otto_s:.0f}px;width:{600 * otto_s:.0f}px;height:{760 * otto_s:.0f}px;">
    <div style="position:absolute;left:0;top:0;width:600px;height:760px;transform:scale({otto_s});transform-origin:0 0">
      {otto_svg("b", ("smirk",), pose="bent", item="mug", label="SPÄTER")}</div></div>
  <div style="position:absolute;left:600px;top:{605 + 485 * otto_s:.0f}px;width:260px;height:30px;border-radius:50%;background:radial-gradient(ellipse, rgba(255,240,215,.18), transparent 70%);"></div>
  <div style="position:absolute;left:960px;top:560px;font-size:30px;font-weight:700;letter-spacing:.45em;color:{AMBER};">ALLTAGSPSYCHOLOGIE MIT OTTO</div>
  <div class="cond" style="position:absolute;left:955px;top:610px;font-size:110px;line-height:1;letter-spacing:.05em;">OTTO NORMALPSYCHE</div>
  <div style="position:absolute;left:962px;top:735px;width:560px;height:3px;background:#FFF;"></div>
  <div style="position:absolute;left:960px;top:762px;font-family:'EB Garamond';font-style:italic;font-size:46px;color:#EDE6D6;">Du bist nicht faul. Du bist nur ganz normal.</div>
  <div style="position:absolute;left:960px;top:842px;font-size:26px;font-weight:600;letter-spacing:.3em;color:{MUTED};">NEUE FOLGE JEDE WOCHE</div>
  <!-- nur auf großen Bildschirmen sichtbar -->
  <div style="position:absolute;left:2230px;top:600px;width:240px;height:100px;background:#111;border:3px solid #2a2a2a;border-radius:16px;opacity:.55;
       color:#7CFF8A;font-family:'Space Mono';font-weight:700;font-size:50px;display:flex;align-items:center;justify-content:center;filter:blur(1.5px);">23:58</div>
  <div style="position:absolute;left:150px;top:650px;opacity:.35;filter:blur(2px);">
    <svg viewBox="-40 -20 520 300" width="360" height="208">{art.laptop(0, 0, 1.2, "")}</svg></div>
  {dust(2560, 1440, 120, 3)}
  {film(2560, 1440)}
"""
project("banner", 2560, 1440, banner)


# ------------------------------------------------------------------ Profilbilder 800x800 (rund beschnitten)
def avatar(name, bg, face, glow):
    s = 2.05
    project(name, 800, 800, f"""
  <div style="position:absolute;inset:0;background:{bg};"></div>
  {light(400, 380, 420, glow)}
  <div style="position:absolute;left:{400 - 300 * s:.0f}px;top:{400 - 200 * s + 30:.0f}px;width:{600 * s:.0f}px;height:{760 * s:.0f}px;">
    <div style="position:absolute;left:0;top:0;width:600px;height:760px;transform:scale({s});transform-origin:0 0">
      {otto_svg("a", (face,), pose="down")}</div></div>
  {dust(800, 800, 25, 9) if bg.startswith("#0") else ""}
  {film(800, 800) if bg.startswith("#0") else '<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 45%, transparent 55%, rgba(120,40,0,.35) 100%);"></div>'}
""")


avatar("profil_orange", "#FF7A1A", "smirk", "rgba(255,230,190,.55)")
avatar("profil_dunkel", "#0B0C0E", "smirk", "rgba(255,226,180,.35)")
print("Projekte erzeugt:", [d for d in os.listdir(HERE) if os.path.isdir(f"{HERE}/{d}")])
