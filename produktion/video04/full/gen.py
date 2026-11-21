"""Video 04 „Warum du nach 5 Minuten Arbeit wieder am Handy bist“ (ca. 7 Min.): Doku-Look + Motion Graphics + interaktive Elemente.

Liest assets/words.json + assets/segments.json (aus voice.py). Schreibt index.html, compositions/*.html, assets/sfx.json.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")  # produktion/
sys.path.insert(0, os.path.join(ROOT, "video01"))
sys.path.insert(0, os.path.join(ROOT, "video01-hf"))
import art  # noqa: E402
from art import INK, ORANGE, _head_base, _face  # noqa: E402
from rig import otto_svg, actor, svgbox  # noqa: E402

WORDS = json.load(open(f"{HERE}/assets/words.json"))
SEG = {s["id"]: (s["start"], s["end"]) for s in json.load(open(f"{HERE}/assets/segments.json"))}
END = round(max(e for _, e in SEG.values()), 3)
BAR, OTTO_TOP = 132, 150
MUTED, AMBER, RED, PAPER = "#8C8F96", "#E8C27A", "#E2483D", "#EDE6D6"
os.makedirs(f"{HERE}/compositions", exist_ok=True)
SFX = []  # (zeit, datei, lautstärke)


def norm(w):
    return re.sub(r"[^\wäöüß]", "", w.lower())


def W(word, after=0.0):
    for w in WORDS:
        if w["start"] >= after - 1e-6 and norm(w["text"]) == norm(word):
            return w["start"]
    raise KeyError(word)


def light(id_, x, y, r, col, a=1.0):
    return (f'<div id="{id_}" class="light" style="left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;opacity:{a};'
            f'background:radial-gradient(circle, {col} 0%, transparent 70%);"></div>')


def typed(id_, text, style=""):
    sp = "".join(f'<span id="{id_}-{i}" style="opacity:0">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(text))
    return f'<div id="{id_}" class="t stamp" style="{style}">{sp}</div>', len(text)


CURSOR = ('<svg viewBox="0 0 40 52" width="44" height="57"><path d="M4,3 L4,42 L14,33 L21,49 L28,46 L21,30 L35,30 Z" '
          'fill="#FFF" stroke="#111" stroke-width="3" stroke-linejoin="round"/></svg>')


def cursor(cid, x, y):
    return (f'<div id="{cid}-cur" class="actor" style="left:{x}px;top:{y}px;width:44px;height:57px;z-index:20;opacity:0">'
            f'<div id="{cid}-rip" style="position:absolute;left:-26px;top:-26px;width:60px;height:60px;border-radius:50%;'
            f'border:4px solid {AMBER};opacity:0"></div>{CURSOR}</div>')


CSS = f"""
  #root {{ position:absolute; inset:0; overflow:hidden; background:#0B0C0E; color:#FFF; font-family:'Inter', sans-serif; }}
  #root .actor, #root .light, #root .lay, #root .t {{ position:absolute; }}
  #root .lay {{ inset:0; }}
  #root .t {{ white-space:nowrap; }}
  #root .stamp {{ font-weight:700; font-size:30px; letter-spacing:.3em; color:#D9D4C7; }}
  #root .cond {{ font-family:'Oswald', sans-serif; font-weight:700; text-transform:uppercase; line-height:1; }}
  #root .card {{ background:#16181D; border:2px solid #3A3F48; border-radius:22px; box-shadow:0 30px 80px rgba(0,0,0,.6); }}
  #root .floor {{ position:absolute; border-radius:50%; background:radial-gradient(ellipse, rgba(255,240,215,.16) 0%, transparent 70%); }}
"""
JS = r"""
  const tl = gsap.timeline({ paused: true });
  const face = (p, from, to, t) => {
    tl.set(`#${p}-face-${from}`, { opacity: 0 }, t); tl.set(`#${p}-face-${to}`, { opacity: 1 }, t);
    tl.fromTo(`#${p}-head`, { scaleY: 0.9, transformOrigin: "50% 100%" }, { scaleY: 1, duration: 0.4, ease: "back.out(2.5)", immediateRender: false }, t);
  };
  const type = (sel, n, t, gap = 0.035) => { for (let i = 0; i < n; i++) tl.fromTo(`${sel}-${i}`, { opacity: 0 }, { opacity: 1, duration: 0.01 }, t + i * gap); };
  const fadeIn = (sel, t, d = 0.5, extra = {}) => tl.fromTo(sel, { opacity: 0, ...extra.from }, { opacity: 1, duration: d, ease: "power3.out", ...extra.to }, t);
  const popIn = (sel, t, d = 0.5) => tl.fromTo(sel, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: d, ease: "back.out(1.8)" }, t);
  const fadeOut = (sel, t, d = 0.35) => tl.to(sel, { opacity: 0, duration: d, ease: "power2.in" }, t);
  const move = (sel, x, y, t, d = 0.6) => tl.to(sel, { x, y, duration: d, ease: "power3.inOut" }, t);
  const click = (cid, t) => { tl.fromTo(`#${cid}-cur`, { scale: 1 }, { keyframes: [{ scale: 0.85, duration: 0.07 }, { scale: 1, duration: 0.15 }], immediateRender: false }, t);
    tl.fromTo(`#${cid}-rip`, { opacity: 1, scale: 0.3 }, { opacity: 0, scale: 1.6, duration: 0.45, ease: "power2.out", immediateRender: false }, t); };
"""


def scene(cid, html, js, T):
    src = (f'<template>\n  <style>{CSS}</style>\n  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">\n{html}\n  </div>\n'
           f'  <script>\n  const T = {json.dumps({k: round(v, 3) for k, v in T.items()})};\n{JS}\n{js}\n  window.__timelines["{cid}"] = tl;\n  </script>\n</template>\n')
    open(f"{HERE}/compositions/{cid}.html", "w", encoding="utf-8").write(src)


HOSTS = []


def put(cid, sid, html, js, T):
    a, e = SEG[sid]
    for k, v in T.items():  # Wort-Zeitpunkte müssen in der Szene liegen (sonst falsches Wort erwischt)
        if not (a - 0.6 <= v <= e + 0.3):
            print(f"  WARNUNG {cid}: Zeitpunkt '{k}' = {v:.2f} liegt außerhalb {a:.2f}–{e:.2f}")
    T = {k: v - a for k, v in T.items()}
    T["end"] = e - a
    scene(cid, html, js, T)
    HOSTS.append((cid, a, e))
    return a



def putr(cid, a, e, html, js, T):
    """Wie put(), aber mit freiem Zeitbereich (z. B. über mehrere Segmente)."""
    SEG[f"_{cid}"] = (a, e)
    return put(cid, f"_{cid}", html, js, T)


GREEN, BLUE, WATER = "#7CFF8A", "#4FA3FF", "#8EC5FF"
BULB = """<g stroke="#111" stroke-width="5"><path d="M-30,30 a60,60 0 1 1 60,0 l0,40 l-60,0 Z" fill="#FFD43B"/><rect x="-32" y="70" width="64" height="26" rx="6" fill="#9AA0A6"/></g>"""


def bulb_html(id_, x, y, s=1.0, glow=True):
    g = light(f"{id_}-g", x + 100 * s, y + 90 * s, 220 * s, "rgba(255,220,120,.55)", 0) if glow else ""
    return g + f'<div id="{id_}" class="actor" style="left:{x}px;top:{y}px;width:{200 * s:.0f}px;height:{230 * s:.0f}px;opacity:0">{svgbox(BULB, "-100 -110 200 230", round(200 * s), round(230 * s))}</div>'


def chapter(cid, sid, num, title):
    a, _ = SEG[sid]
    put(cid, sid, f"""
  <div id="{cid}-k" class="t" style="left:0;right:0;top:400px;text-align:center;font-size:30px;font-weight:700;letter-spacing:.6em;color:{MUTED};opacity:0">KAPITEL {num}</div>
  <div id="{cid}-t" class="t cond" style="left:0;right:0;top:460px;text-align:center;font-size:130px;letter-spacing:.1em;opacity:0">{title}</div>
  <div id="{cid}-l" class="actor" style="left:260px;top:640px;width:1400px;height:2px;background:{AMBER};transform-origin:0 50%"></div>""", f"""
  tl.fromTo("#{cid}-k", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }}, 0.05);
  tl.fromTo("#{cid}-t", {{ opacity: 0, x: -120, filter: "blur(12px)" }}, {{ opacity: 1, x: 0, filter: "blur(0px)", duration: 0.5, ease: "power4.out" }}, 0.2);
  tl.fromTo("#{cid}-l", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8, ease: "power3.inOut" }}, 0.3);
  tl.to(["#{cid}-k", "#{cid}-t", "#{cid}-l"], {{ opacity: 0, duration: 0.35, ease: "power2.in" }}, T.end - 0.4);""", {})
    SFX.extend([(a + 0.05, "click", 0.5), (a + 0.25, "boom", 0.7)])


def otto_at(cid, x, faces, top=OTTO_TOP, s=1.0, **kw):
    lt = light(f"{cid}-ol", x + 300 * s, top + 320 * s, 480 * s, "rgba(255,226,180,.28)")
    return (lt + f'<div id="{cid}-otto" class="actor" style="left:{x}px;top:{top}px;width:{600 * s:.0f}px;height:{760 * s:.0f}px;">'
            f'<div style="position:absolute;left:0;top:0;width:600px;height:760px;transform:scale({s});transform-origin:0 0">{otto_svg(cid + "o", faces, **kw)}</div></div>')


def header(cid, kicker, title, x=130):
    return (f'<div id="{cid}-hk" class="t" style="left:{x}px;top:180px;font-size:28px;font-weight:800;letter-spacing:.4em;color:{AMBER};opacity:0">{kicker}</div>'
            f'<div id="{cid}-ht" class="t cond" style="left:{x}px;top:222px;font-size:88px;opacity:0">{title}</div>')


HEADER_JS = lambda cid: f'fadeIn("#{cid}-hk", 0.1, 0.4); tl.fromTo("#{cid}-ht", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power4.out" }}, 0.25);'  # noqa: E731


def foot(cid, text, x=130):
    return f'<div id="{cid}-ft" class="t" style="left:{x}px;top:880px;font-size:28px;font-weight:600;letter-spacing:.14em;color:{MUTED};opacity:0">{text}</div>'


def lower_third(cid, name, role, x=130, y=700):
    return (f'<div id="{cid}-lt" class="t" style="left:{x}px;top:{y}px;opacity:0"><div id="{cid}-ltl" style="width:440px;height:3px;background:#FFF;transform-origin:0 50%"></div>'
            f'<div class="cond" style="margin-top:16px;font-size:60px;letter-spacing:.08em;">{name}</div>'
            f'<div style="margin-top:10px;font-size:28px;letter-spacing:.24em;color:{MUTED};font-weight:600;">{role}</div></div>')


LT_JS = lambda cid, t: f'fadeIn("#{cid}-lt", {t}, 0.5); tl.fromTo("#{cid}-ltl", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power3.out" }}, {t});'  # noqa: E731


def chip(id_, x, y, text, bg="#22262E", col="#FFF", size=40, border="#3A3F48"):
    return (f'<div id="{id_}" class="actor" style="left:{x}px;top:{y}px;padding:14px 28px;border-radius:18px;background:{bg};border:2px solid {border};'
            f'font-size:{size}px;font-weight:800;color:{col};white-space:nowrap;opacity:0">{text}</div>')


def stamp(id_, x, y, text, col=RED, size=90, rot=-8):
    return (f'<div id="{id_}" class="t cond" style="left:{x}px;top:{y}px;font-size:{size}px;color:{col};border:8px solid {col};border-radius:16px;'
            f'padding:4px 26px;transform:rotate({rot}deg);opacity:0;background:rgba(11,12,14,.55)">{text}</div>')


SLAM_JS = r"""
  const slam = (sel, t, s = 2.2) => tl.fromTo(sel, { opacity: 0, scale: s }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.in" }, t);
  const shake = (sel, t, a = 10) => tl.fromTo(sel, { x: 0, y: 0 }, { keyframes: [...Array(8)].map((_, i) => ({ x: (i % 2 ? a : -a) * (1 - i / 8), y: (i % 3 ? -a : a) * 0.5 * (1 - i / 8), duration: 0.035 })).concat([{ x: 0, y: 0, duration: 0.04 }]), immediateRender: false }, t);
"""
JS += SLAM_JS

# ================================================================ Szenen
exec(open(f"{HERE}/s1.py", encoding="utf-8").read())
exec(open(f"{HERE}/s2.py", encoding="utf-8").read())
exec(open(f"{HERE}/s3.py", encoding="utf-8").read())

# ================================================================ Rahmen (alter Film, aus Video 01)
exec(open(os.path.join(ROOT, "video01-doku", "film.py"), encoding="utf-8").read())

# ================================================================ Untertitel im Balken
groups, cur = [], []
for i, w in enumerate(WORDS):
    cur.append(w)
    nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
    if len(cur) >= 7 or re.search(r"[.!?:,]$", w["text"]) or not nxt or (nxt["start"] - w["end"] >= 0.25 and len(cur) >= 3):
        groups.append(cur); cur = []
starts = [max(g[0]["start"] - 0.05, 0.12) for g in groups] + [END]
ch, cj = [], []
for gi, g in enumerate(groups):
    ga, gb = starts[gi], min(g[-1]["end"] + 0.25, END, starts[gi + 1] - 0.02)
    ch.append(f'<div id="k{gi}" class="clip cap" data-start="{ga:.3f}" data-duration="{gb - ga:.3f}">{" ".join(w["text"] for w in g)}</div>')
    fd = min(0.15, (gb - ga) / 3)
    cj.append(f'tl.fromTo("#k{gi}", {{opacity:0}}, {{opacity:1, duration:{fd:.3f}}}, {ga:.3f}); tl.to("#k{gi}", {{opacity:0, duration:{fd:.3f}}}, {gb - fd:.3f});')
open(f"{HERE}/compositions/captions.html", "w", encoding="utf-8").write(f"""<template>
  <style>
  #root {{ position:absolute; inset:0; }}
  #root .cap {{ position:absolute; left:0; right:0; top:{1080 - BAR + 44}px; text-align:center; font-family:'Inter', sans-serif;
          font-weight:500; font-size:36px; color:#F2F2F2; opacity:0; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1920" data-height="1080" data-layout-allow-caption-zone>{"".join(ch)}</div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  {"".join(cj)}
  window.__timelines["captions"] = tl;
  </script>
</template>
""")

# ================================================================ SRT
def _srt(x):
    ms = int(round(x * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
with open(f"{HERE}/untertitel_video04.srt", "w", encoding="utf-8") as f:
    for gi, g in enumerate(groups):
        ga, gb = starts[gi], min(g[-1]["end"] + 0.25, END, starts[gi + 1] - 0.02)
        f.write(f"{gi + 1}\n{_srt(ga)} --> {_srt(gb)}\n{' '.join(w['text'] for w in g)}\n\n")
NOCAP = "--nocap" in sys.argv

# ================================================================ Root
hh = "\n".join(f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{a:.3f}" data-duration="{e - a:.3f}" '
               f'data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>' for c, a, e in HOSTS)
open(f"{HERE}/index.html", "w").write(f"""<!doctype html>
<html lang="de" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1920px; height:1080px; overflow:hidden; background:#000; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1920" data-height="1080">
{hh}
      <div id="frame" data-composition-id="frame" data-composition-src="compositions/frame.html" data-start="0" data-duration="{END}" data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{END}" data-track-index="3" data-track-kind="captions" data-width="1920" data-height="1080"{' data-hidden' if NOCAP else ''}></div>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
# Glühbirnen-/Geistesblitz-Glocke dezent (Richtlinie): höchstens 0.2
SFX = [(t, f, min(g * 0.3, 0.2) if f == "ding" else g) for t, f, g in SFX]
json.dump([{"t": round(t, 3), "f": f, "g": g} for t, f, g in SFX if g > 0], open(f"{HERE}/assets/sfx.json", "w"), indent=0)
for fn in ("hyperframes.json", "package.json", "meta.json"):
    open(f"{HERE}/{fn}", "w").write(open(os.path.join(ROOT, "video01-doku", fn)).read().replace("otto-video01-doku", "otto-video04"))
print(f"Video 04: {END}s, {len(HOSTS)} Szenen, {len(groups)} Untertitel, {len([s for s in SFX if s[2] > 0])} Soundeffekte")
