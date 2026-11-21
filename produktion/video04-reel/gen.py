"""Video 04 als Reel/Short (1080x1920): Hook → „in einer Minute erklärt“ → 60-Sekunden-Timer → „Zeit um!“ → Bildschirmzeit-Check → YouTube-Verweis.

Liest assets/words.json + assets/segments.json (aus voice.py). Schreibt index.html, compositions/*.html, assets/sfx.json.
Sichere Zone (Shorts/Reels): Grafik y 430–1030, Untertitel y 1070–1240, wichtiges zwischen x 150 und 930.
"""
import json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")  # produktion/
sys.path.insert(0, os.path.join(ROOT, "video01"))
sys.path.insert(0, os.path.join(ROOT, "video01-hf"))
from rig import otto_svg, svgbox  # noqa: E402
import art  # noqa: E402

WORDS = json.load(open(f"{HERE}/assets/words.json"))
SEG = {s["id"]: (s["start"], s["end"]) for s in json.load(open(f"{HERE}/assets/segments.json"))}
END = round(max(e for _, e in SEG.values()), 3)
T0, T1 = SEG["timer"]  # Timer 60 → 0
MUTED, AMBER, RED, GREEN, ORANGE, BLUE = "#8C8F96", "#E8C27A", "#FF4B3E", "#5BE37D", "#FF7A1A", "#4FA3FF"
os.makedirs(f"{HERE}/compositions", exist_ok=True)
SFX = []


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


def otto(cid, x, top, s, faces, **kw):
    return (f'<div id="{cid}-otto" class="actor" style="left:{x}px;top:{top}px;width:{600 * s:.0f}px;height:{760 * s:.0f}px;opacity:0">'
            f'<div style="position:absolute;left:0;top:0;width:600px;height:760px;transform:scale({s});transform-origin:0 0">{otto_svg(cid + "o", faces, **kw)}</div></div>')


def ctext(id_, top, html, size, cls="cond", color="#FFF", extra=""):
    return (f'<div id="{id_}" class="t {cls}" style="left:0;width:1080px;top:{top}px;text-align:center;font-size:{size}px;color:{color};opacity:0;{extra}">{html}</div>')


def tag(cid, num, title):
    return (f'<div id="{cid}-tag" class="t" style="left:0;width:1080px;top:442px;text-align:center;opacity:0">'
            f'<span style="display:inline-flex;align-items:center;gap:16px;padding:8px 28px 8px 10px;background:#16181D;border:2px solid #3A3F48;'
            f'border-radius:44px;font-size:30px;font-weight:800;letter-spacing:.16em;color:#EDE6D6">'
            f'<span style="width:50px;height:50px;border-radius:50%;background:{AMBER};color:#111;display:inline-flex;align-items:center;justify-content:center;'
            f'font-size:28px;letter-spacing:0">{num}</span>{title}</span></div>')


CSS = """
  #root { position:absolute; inset:0; overflow:hidden; color:#FFF; font-family:'Inter', sans-serif; }
  #root .actor, #root .light, #root .lay, #root .t { position:absolute; }
  #root .lay { inset:0; }
  #root .t { white-space:nowrap; }
  #root .cond { font-family:'Oswald', sans-serif; font-weight:700; text-transform:uppercase; line-height:1; }
  #root .mono { font-family:'Space Mono', monospace; font-weight:700; line-height:1; }
  #root .card { background:#16181D; border:2px solid #3A3F48; border-radius:26px; box-shadow:0 30px 80px rgba(0,0,0,.6); }
  #root .emo { line-height:1; }
"""
JS = r"""
  const tl = gsap.timeline({ paused: true });
  const fadeIn = (sel, t, d = 0.3) => tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: d, ease: "power2.out" }, t);
  const fadeOut = (sel, t, d = 0.22) => tl.to(sel, { opacity: 0, duration: d, ease: "power2.in" }, t);
  const popIn = (sel, t, d = 0.32, s = 0.3) => tl.fromTo(sel, { opacity: 0, scale: s }, { opacity: 1, scale: 1, duration: d, ease: "back.out(2.2)" }, t);
  const slam = (sel, t, s = 2.4) => tl.fromTo(sel, { opacity: 0, scale: Math.min(s, 1.3) },  /* Richtlinie: nichts über den Bildrand */ { opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }, t);
  const upIn = (sel, t, d = 0.3) => tl.fromTo(sel, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: d, ease: "power3.out" }, t);
  const outUp = (sel, t, d = 0.22) => tl.to(sel, { opacity: 0, y: -50, scale: 0.9, duration: d, ease: "power2.in" }, t);
  const shake = (sel, t, a = 14) => tl.fromTo(sel, { x: 0, y: 0 }, { keyframes: [...Array(8)].map((_, i) => ({ x: (i % 2 ? a : -a) * (1 - i / 8), y: (i % 3 ? -a : a) * 0.5 * (1 - i / 8), duration: 0.035 })).concat([{ x: 0, y: 0, duration: 0.04 }]), immediateRender: false }, t);
  const tagIn = (sel, t) => tl.fromTo(sel, { opacity: 0, y: -30, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(2)" }, t);
  const face = (p, from, to, t) => { tl.set(`#${p}-face-${from}`, { opacity: 0 }, t); tl.set(`#${p}-face-${to}`, { opacity: 1 }, t); };
"""
HOSTS = []


DY = 170  # alles (außer Hintergrund) so viel tiefer, damit die Grafik optisch mittig sitzt


def scene(cid, a, e, html, js, T=None, track=1):
    if cid != "bg":
        html = f'<div class="lay" style="transform:translateY({DY}px)">\n{html}\n</div>'
    T = {k: round(v - a, 3) for k, v in (T or {}).items()}
    T["end"] = round(e - a, 3)
    src = (f'<template>\n  <style>{CSS}</style>\n  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">\n{html}\n  </div>\n'
           f'  <script>\n  const T = {json.dumps(T)};\n{JS}\n{js}\n  window.__timelines["{cid}"] = tl;\n  </script>\n</template>\n')
    open(f"{HERE}/compositions/{cid}.html", "w", encoding="utf-8").write(src)
    HOSTS.append((cid, a, e, track))


# ================================================================ Hintergrund: warme Lichter, die langsam wandern
scene("bg", 0, END, f"""
  <div style="position:absolute;inset:0;background:#0B0C0E"></div>
  {light("bg-l1", 540, 930, 640, "rgba(255,226,180,.20)")}
  {light("bg-l2", 300, 1300, 520, "rgba(140,190,255,.07)")}
  {light("bg-l3", 820, 400, 420, "rgba(255,150,80,.08)")}""", f"""
  tl.fromTo("#bg-l1", {{ x: -60, y: 0 }}, {{ x: 60, y: 40, duration: {END}, ease: "sine.inOut" }}, 0);
  tl.fromTo("#bg-l2", {{ x: 0, y: 0 }}, {{ x: 180, y: -120, duration: {END}, ease: "sine.inOut" }}, 0);
  tl.fromTo("#bg-l3", {{ x: 0, y: 0 }}, {{ x: -200, y: 80, duration: {END}, ease: "sine.inOut" }}, 0);
""", track=0)


exec(open(f"{HERE}/scenes.py", encoding="utf-8").read())

# ================================================================ Timer (oben, läuft 60 → 0)
TIMER_IN = W("Los!") + 0.12
sets = "".join(f'tl.set("#tm-n", {{ textContent: "0:{60 - i:02d}" }}, {T0 + i - TIMER_IN:.3f});' for i in range(1, 61))
scene("tm", TIMER_IN, min(T1 + 1.2, END), f"""
  <div id="tm-box" class="actor card" style="left:360px;top:296px;width:360px;height:104px;border-radius:52px;display:flex;align-items:center;justify-content:center;gap:22px;opacity:0">
    <svg viewBox="-30 -34 60 64" width="56" height="60"><circle r="24" fill="none" stroke="{AMBER}" stroke-width="6"/><rect x="-6" y="-34" width="12" height="8" rx="2" fill="{AMBER}"/>
      <path id="tm-hand" d="M0,0 L0,-15" stroke="{AMBER}" stroke-width="6" stroke-linecap="round"/></svg>
    <div id="tm-n" class="mono" style="font-size:68px;color:#FFF">1:00</div></div>
  <div id="tm-bar" class="actor" style="left:400px;top:412px;width:280px;height:8px;border-radius:4px;background:{AMBER};transform-origin:0 50%;opacity:0"></div>""", f"""
  popIn("#tm-box", 0, 0.35, 0.3);
  fadeIn("#tm-bar", 0.2, 0.2);
  tl.fromTo("#tm-bar", {{ scaleX: 1 }}, {{ scaleX: 0, duration: 60, ease: "none", immediateRender: false }}, {T0 - TIMER_IN:.3f});
  tl.fromTo("#tm-hand", {{ rotation: 0 }}, {{ rotation: 360 * 60, svgOrigin: "0 0", duration: 60, ease: "none", immediateRender: false }}, {T0 - TIMER_IN:.3f});
  {sets}
  tl.set(["#tm-n"], {{ color: "{RED}" }}, {T1 - 10 - TIMER_IN:.3f});
  tl.set("#tm-bar", {{ backgroundColor: "{RED}" }}, {T1 - 10 - TIMER_IN:.3f});
  for (let i = 5; i >= 1; i--) tl.fromTo("#tm-box", {{ scale: 1.14 }}, {{ scale: 1, duration: 0.4, ease: "power2.out", immediateRender: false }}, {T1 - TIMER_IN:.3f} - i);
  tl.fromTo("#tm-box", {{ scale: 1.35 }}, {{ scale: 1, duration: 0.5, ease: "elastic.out(1, 0.4)", immediateRender: false }}, {T1 - TIMER_IN:.3f});
  tl.to(["#tm-box", "#tm-bar"], {{ opacity: 0, y: -40, duration: 0.3, ease: "power2.in" }}, T.end - 0.3);
""", {}, track=3)
SFX += [(T1 - 5, "tick", 0.32)]


# ================================================================ Film-Look (Korn, Vignette, Staub, Flackern) – deterministisch
_noise = ("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence "
          "type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")
motes = "".join(f'<div id="fr-m{i}" class="mote"></div>' for i in range(40))
open(f"{HERE}/compositions/frame.html", "w").write(f"""<template>
  <style>
  #root {{ position:absolute; inset:0; pointer-events:none; overflow:hidden; }}
  #root .mote {{ position:absolute; left:0; top:0; width:6px; height:6px; border-radius:50%; background:rgba(255,236,205,.9); filter:blur(1.2px); mix-blend-mode:screen; opacity:0; }}
  </style>
  <div id="root" data-composition-id="frame" data-width="1080" data-height="1920" data-layout-ignore>
    {motes}
    <div style="position:absolute;inset:0;background:#5a3c14;mix-blend-mode:soft-light;opacity:.3;"></div>
    <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%, transparent 48%, rgba(0,0,0,.6) 100%);"></div>
    <div id="fr-flick" style="position:absolute;inset:0;background:#000;opacity:0;"></div>
    <div id="fr-grain" style="position:absolute;inset:-64px;background-image:url(&quot;{_noise}&quot;);background-size:256px 256px;opacity:.12;mix-blend-mode:overlay;"></div>
  </div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  const H = (k, i) => {{ let x = Math.sin(k * 127.1 + i * 311.7) * 43758.5453; return x - Math.floor(x); }};
  const $ = id => document.getElementById(id);
  const motes = [...Array(40).keys()].map(i => ({{ el: $(`fr-m${{i}}`), x: H(i, 1) * 1080, y: H(i, 2) * 1920, vx: (H(i, 3) - 0.5) * 16, vy: -6 - H(i, 4) * 14,
      w: 0.4 + H(i, 5) * 0.9, ph: H(i, 6) * 6.28, s: 0.5 + H(i, 7) * 1.3 }}));
  function render(t) {{
    const k = Math.floor(t * 12);
    $("fr-grain").style.transform = `translate(${{-H(k, 1) * 64}}px, ${{-H(k, 2) * 64}}px)`;
    $("fr-flick").style.opacity = (0.015 + H(k, 3) * 0.05).toFixed(3);
    for (const m of motes) {{
      const x = ((m.x + m.vx * t + 40 * Math.sin(t * 0.3 + m.ph)) % 1080 + 1080) % 1080;
      const y = ((m.y + m.vy * t) % 1920 + 1920) % 1920;
      m.el.style.transform = `translate(${{x.toFixed(1)}}px, ${{y.toFixed(1)}}px) scale(${{m.s.toFixed(2)}})`;
      m.el.style.opacity = (0.1 + 0.25 * (0.5 + 0.5 * Math.sin(t * m.w + m.ph))).toFixed(3);
    }}
  }}
  const clock = {{ t: 0 }};
  tl.to(clock, {{ t: {END}, duration: {END}, ease: "none", onUpdate: () => render(clock.t) }}, 0);
  render(0);
  window.__timelines["frame"] = tl;
  </script>
</template>
""")

# ================================================================ Untertitel: 1–3 Wörter, aktives Wort gelb
groups, cur = [], []
for i, w in enumerate(WORDS):
    cur.append(w)
    nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
    if len(cur) >= 3 or len(" ".join(x["text"] for x in cur)) >= 16 or re.search(r"[.!?:,]$", w["text"]) or not nxt or nxt["start"] - w["end"] >= 0.3:
        groups.append(cur); cur = []
starts = [max(g[0]["start"] - 0.04, 0.05) for g in groups] + [END]
ch, cj = [], []
wi = 0
for gi, g in enumerate(groups):
    ga, gb = starts[gi], min(g[-1]["end"] + 0.3, END, starts[gi + 1] - 0.01)
    spans = []
    for w in g:
        spans.append(f'<span id="w{wi}">{w["text"].upper()}</span>')
        cj.append(f'tl.set("#w{wi}", {{ color: "{AMBER}" }}, {max(w["start"], ga):.3f});')
        wi += 1
    ch.append(f'<div id="k{gi}" class="clip cap" data-start="{ga:.3f}" data-duration="{gb - ga:.3f}">{" ".join(spans)}</div>')
    cj.append(f'tl.fromTo("#k{gi}", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: {min(0.12, (gb - ga) / 3):.3f}, ease: "back.out(2.5)" }}, {ga:.3f});'
              f'tl.to("#k{gi}", {{ opacity: 0, duration: {min(0.06, (gb - ga) / 4):.3f} }}, {gb - min(0.06, (gb - ga) / 4):.3f});')
open(f"{HERE}/compositions/captions.html", "w", encoding="utf-8").write(f"""<template>
  <style>
  #root {{ position:absolute; inset:0; }}
  #root .cap {{ position:absolute; left:192px; width:696px; top:1290px; text-align:center; font-family:'Inter', sans-serif; font-weight:900;
          font-size:64px; line-height:1.12; color:#FFF; opacity:0; letter-spacing:.01em;
          text-shadow:0 5px 0 #000, 0 0 24px rgba(0,0,0,.9), 3px 3px 0 #000, -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-layout-allow-caption-zone>{"".join(ch)}</div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  {"".join(cj)}
  window.__timelines["captions"] = tl;
  </script>
</template>
""")

# ================================================================ Root
hh = "\n".join(f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{a:.3f}" data-duration="{e - a:.3f}" '
               f'data-track-index="{tr}" data-track-kind="graphics" data-width="1080" data-height="1920"></div>' for c, a, e, tr in HOSTS)
open(f"{HERE}/index.html", "w").write(f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0B0C0E; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
{hh}
      <div id="frame" data-composition-id="frame" data-composition-src="compositions/frame.html" data-start="0" data-duration="{END}" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{END}" data-track-index="5" data-track-kind="captions" data-width="1080" data-height="1920"></div>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
# Kein Rauschen (Whoosh/Senden/Kratzen klangen wie eine Spraydose) → Klicks und Plops
SWAP = {"whoosh": ("click", 1.0), "send": ("pop", 1.0), "scratch": ("pop", 1.0)}
SFX = [(t, SWAP.get(f, (f, 1))[0], g * SWAP.get(f, (f, 1))[1]) for t, f, g in SFX]
SFX = [x for i, x in enumerate(sorted(SFX)) if not any(abs(x[0] - y[0]) < 0.06 and x[1] == y[1] for y in sorted(SFX)[:i])]
# Glühbirnen-/Geistesblitz-Glocke dezent (Richtlinie): höchstens 0.2
SFX = [(t, f, min(g * 0.3, 0.2) if f == "ding" else g) for t, f, g in SFX]
json.dump([{"t": round(t, 3), "f": f, "g": g} for t, f, g in SFX if g > 0], open(f"{HERE}/assets/sfx.json", "w"), indent=0)
for fn in ("hyperframes.json", "package.json", "meta.json"):
    open(f"{HERE}/{fn}", "w").write(open(os.path.join(ROOT, "video01-doku", fn)).read().replace("otto-video01-doku", "otto-video04-reel"))
print(f"Reel: {END}s, Timer {T0:.2f}→{T1:.2f}, {len(HOSTS)} Kompositionen, {len(groups)} Untertitel, {len(SFX)} Soundeffekte")
