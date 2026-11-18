"""Doku-Look-Version der Probe (Kinobalken, Lichtkegel, Filmkorn, ruhige Kamera). Liest assets/words.json + segments.json."""
import json, os, random, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "video01"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "video01-hf"))
import art  # noqa: E402
from art import INK, ORANGE, sock, penguin, sparkle, spray, _head_base, _face  # noqa: E402
from rig import otto_svg, actor, svgbox  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = json.load(open(f"{HERE}/assets/words.json"))
SEG = {s["id"]: (s["start"], s["end"]) for s in json.load(open(f"{HERE}/assets/segments.json"))}
END = round(max(e for _, e in SEG.values()), 3)
for w in WORDS:  # Whisper setzt das erste Wort oft zu früh an
    w["start"] = max(w["start"], SEG["s01_hook"][0] + 0.02)
os.makedirs(f"{HERE}/compositions", exist_ok=True)

BG, PAPER, MUTED, RED = "#0B0C0E", "#EDE6D6", "#8C8F96", "#E2483D"
BAR = 132  # Kinobalken oben/unten -> Bild ca. 2,35:1


def norm(w):
    return re.sub(r"[^\wäöüß]", "", w.lower())


def W(word, after=0.0):
    for w in WORDS:
        if w["start"] >= after - 1e-6 and norm(w["text"]) == norm(word):
            return w["start"]
    raise KeyError(word)


def light(id_, x, y, r, col, a=1.0):
    return (f'<div id="{id_}" class="light" style="left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;'
            f'opacity:{a};background:radial-gradient(circle, {col} 0%, transparent 70%);"></div>')


CSS = f"""
  #root {{ position:absolute; inset:0; overflow:hidden; background:{BG}; color:#FFF; font-family:'Inter', sans-serif; }}
  #root .actor, #root .light, #root .lay, #root .t {{ position:absolute; }}
  #root .lay {{ inset:0; }}
  #root .t {{ white-space:nowrap; }}
  #root .stamp {{ font-family:'Inter'; font-weight:700; font-size:30px; letter-spacing:.3em; color:#D9D4C7; }}
  #root .cond {{ font-family:'Oswald', sans-serif; font-weight:700; text-transform:uppercase; }}
  #root .floor {{ position:absolute; border-radius:50%; background:radial-gradient(ellipse, rgba(255,240,215,.16) 0%, transparent 70%); }}
"""
JS = r"""
  const tl = gsap.timeline({ paused: true });
  const face = (p, from, to, t) => {
    tl.set(`#${p}-face-${from}`, { opacity: 0 }, t);
    tl.set(`#${p}-face-${to}`, { opacity: 1 }, t);
    tl.fromTo(`#${p}-head`, { scaleY: 0.94, transformOrigin: "50% 100%" }, { scaleY: 1, duration: 0.4, ease: "power2.out", immediateRender: false }, t);
  };
  const type = (sel, n, t, gap = 0.045) => { for (let i = 0; i < n; i++) tl.fromTo(`${sel}-${i}`, { opacity: 0 }, { opacity: 1, duration: 0.01 }, t + i * gap); };
  const fadeIn = (sel, t, d = 0.6, extra = {}) => tl.fromTo(sel, { opacity: 0, ...extra.from }, { opacity: 1, duration: d, ease: "power2.out", ...extra.to }, t);
  const fadeOut = (sel, t, d = 0.4) => tl.to(sel, { opacity: 0, duration: d, ease: "power2.in" }, t);
"""


def typed(id_, text, cls="stamp", style=""):
    sp = "".join(f'<span id="{id_}-{i}" style="opacity:0">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(text))
    return f'<div id="{id_}" class="t {cls}" style="{style}">{sp}</div>', len(text)


def scene(sid, html, js, T):
    src = (f'<template>\n  <style>{CSS}</style>\n  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">\n'
           f'{html}\n  </div>\n  <script>\n  const T = {json.dumps({k: round(v, 3) for k, v in T.items()})};\n{JS}\n{js}\n'
           f'  window.__timelines["{sid}"] = tl;\n  </script>\n</template>\n')
    open(f"{HERE}/compositions/{sid}.html", "w", encoding="utf-8").write(src)


OTTO_TOP = 150  # Füße bei ~850, oberhalb des unteren Balkens (948)

# ------------------------------------------------------------ d0 Kaltstart
a0, e0 = SEG["open"]
scene("d0", f"""
    <div id="d0-q" class="t" style="left:0;right:0;top:500px;text-align:center;font-family:'EB Garamond';font-style:italic;font-size:44px;color:#CFC9BC;">
      Die folgende Geschichte beruht auf wahren Begebenheiten.</div>""",
      r"""  fadeIn("#d0-q", 0.15, 0.6); fadeOut("#d0-q", T.end - 0.45, 0.4);""", {"end": e0 - a0})

# ------------------------------------------------------------ d1 Hook
a1, e1 = SEG["s01_hook"]
L = lambda t: t - a1  # noqa: E731
OX = 340
mugx, mugy = OX + 300 + 83, OTTO_TOP + 200 + 229
stamp1, n1 = typed("d1-st", "DIENSTAG · 09:00 UHR", style="left:130px;top:178px;")
paper = (f'<div id="d1-paper" class="actor" style="left:560px;top:250px;width:800px;height:560px;background:{PAPER};'
         f'box-shadow:0 30px 60px rgba(0,0,0,.6);padding:60px 70px;color:#2A2622;font-family:\'EB Garamond\';">'
         f'<div style="font-size:64px;font-weight:700;letter-spacing:.08em;">HEUTE</div>'
         f'<div style="margin-top:50px;font-size:62px;font-style:italic;display:flex;align-items:center;gap:30px;">'
         f'<span style="display:inline-block;width:56px;height:56px;border:4px solid #2A2622;"></span>Steuererklärung</div>'
         f'<div style="margin-top:46px;font-size:34px;color:#6B635A;">Deadline: Freitag</div>'
         f'<div style="position:absolute;right:90px;top:-30px;width:44px;height:120px;border:7px solid #9AA0A6;border-radius:22px;"></div></div>')
scene("d1", f"""
    <div id="d1-wide" class="lay">
      <div id="d1-cam" class="lay">
        {light("d1-l", OX + 300, 470, 520, "rgba(255,226,180,.32)")}
        <div class="floor" style="left:{OX + 60}px;top:820px;width:480px;height:70px;"></div>
        {actor("d1-otto", OX, OTTO_TOP, 600, 760, otto_svg("d1o", ("tired", "smirk"), pose="bent", item="mug"))}
      </div>
      <div id="d1-lt" class="t" style="left:1060px;top:520px;">
        <div id="d1-ltline" style="width:420px;height:3px;background:#FFF;transform-origin:0 50%;"></div>
        <div id="d1-ltname" class="cond" style="margin-top:18px;font-size:96px;letter-spacing:.18em;line-height:1;">OTTO</div>
        <div id="d1-ltrole" style="margin-top:14px;font-size:28px;letter-spacing:.3em;color:{MUTED};font-weight:600;">34 · BÜROANGESTELLTER</div>
      </div>
      {stamp1}
    </div>
    <div id="d1-ins" class="lay" style="background:#121316;opacity:0">
      {light("d1-l2", 960, 520, 620, "rgba(255,226,180,.22)")}
      {paper}
    </div>""", r"""
  fadeIn("#d1-wide", 0, 0.8);
  type("#d1-st", %d, 0.1, 0.03);
  fadeOut("#d1-st", T.heute, 0.3);
  tl.fromTo("#d1-cam", { scale: 1 }, { scale: 1.05, duration: T.heute, ease: "none", transformOrigin: "640px 540px" }, 0);
  tl.fromTo("#d1-ltline", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.out" }, T.otto - 0.1);
  fadeIn("#d1-ltname", T.otto, 0.7, { from: { scale: 1.06, transformOrigin: "0%% 50%%" }, to: { scale: 1 } });
  fadeIn("#d1-ltrole", T.otto + 0.3, 0.6);
  fadeOut("#d1-lt", T.heute - 0.35, 0.35);
  tl.to("#d1-ins", { opacity: 1, duration: 0.4, ease: "power2.inOut" }, T.heute - 0.1);
  tl.fromTo("#d1-paper", { scale: 1, rotation: -4 }, { scale: 1.08, rotation: -2, duration: T.und - T.heute + 0.4, ease: "none" }, T.heute - 0.1);
  tl.to("#d1-ins", { opacity: 0, duration: 0.35, ease: "power2.inOut" }, T.und - 0.15);
  face("d1o", "tired", "smirk", T.und + 0.1);
  tl.to("#d1-cam", { scale: 2.5, x: %d, y: %d, transformOrigin: "%dpx %dpx", duration: 1.2, ease: "power2.inOut" }, T.nicht - 0.2);
  fadeOut("#d1-wide", T.end - 0.3, 0.3);
""" % (n1, 960 - mugx, 520 - mugy, mugx, mugy),
      {"otto": L(W("Otto.")), "heute": L(W("heute")), "und": L(W("Und")), "nicht": L(W("nicht")), "end": e1 - a1})

# ------------------------------------------------------------ d2 Titel
a2, e2 = SEG["title"]
scene("d2", f"""
    <div id="d2-t" class="t cond" style="left:0;right:0;top:390px;text-align:center;font-size:230px;line-height:1;">OTTO</div>
    <div id="d2-s" class="t" style="left:0;right:0;top:660px;text-align:center;font-size:30px;font-weight:600;letter-spacing:.5em;color:{MUTED};">DIE KUNST DES AUFSCHIEBENS</div>""",
      r"""
  tl.fromTo("#d2-t", { opacity: 0 }, { opacity: 1, duration: 1.0, ease: "power2.out" }, 0);
  tl.fromTo("#d2-t", { scale: 1.12 }, { scale: 1, duration: T.end - 0.6, ease: "power2.out", immediateRender: false }, 0);
  fadeIn("#d2-s", 0.45, 0.6);
  fadeOut(["#d2-t", "#d2-s"], T.end - 0.55, 0.5);""", {"end": e2 - a2})

# ------------------------------------------------------------ d3 Montage
a3, e3 = SEG["s02_bad"][0], SEG["s04_pinguine"][1]
L = lambda t: t - a3  # noqa: E731
st_a, na = typed("d3-sa", "11:30 UHR", style="left:130px;top:178px;")
st_b, nb = typed("d3-sb", "14:00 UHR", style="left:130px;top:178px;")
st_c, nc = typed("d3-sc", "17:30 UHR", style="left:130px;top:178px;")
socks = "".join(actor(f"d3-k{i}", 1030 + i * 122, 520, 150, 200, svgbox(sock(0, 0, c, 0.85), "-60 -90 150 200", 150, 200))
                for i, c in enumerate(["#C94A43", "#C9932F", "#C9B94A", "#4E9E5E", "#3F7FB5", "#7D58A0"]))
sparks = "".join(actor(f"d3-sp{i}", x, y, 120, 120, svgbox(sparkle(0, 0, s, "#E8D9A8"), "-60 -60 120 120", 120, 120))
                 for i, (x, y, s) in enumerate([(1200, 330, 1.1), (1420, 520, 0.8), (1120, 620, 0.9)]))
pengs = "".join(actor(f"d3-p{i}", x, y, 160, 200, svgbox(penguin(0, 0, s), "-80 -100 160 200", 160, 200))
                for i, (x, y, s) in enumerate([(1100, 470, 1.5), (1280, 500, 1.15), (1420, 525, 0.9)]))
scene("d3", f"""
    <div id="d3-cam" class="lay">
      {light("d3-la", 1000, 500, 760, "rgba(120,180,220,.30)")}
      {light("d3-lb", 1000, 500, 760, "rgba(240,180,90,.30)", 0)}
      {light("d3-lc", 1000, 500, 760, "rgba(90,140,255,.22)", 0)}
      <div class="floor" style="left:400px;top:820px;width:480px;height:70px;"></div>
      {actor("d3-otto", 340, OTTO_TOP, 600, 760, otto_svg("d3o", ("happy", "aha", "tired"), pose="down"))}
      {light("d3-glow", 640, 330, 260, "rgba(140,190,255,.35)", 0)}
      {actor("d3-spray", 1020, 360, 200, 260, svgbox(spray(0, 0, 1.5), "-80 -110 200 260", 200, 260))}
      {sparks}{socks}
      <div id="d3-phone" class="actor" style="left:1000px;top:300px;width:560px;height:440px;background:#1B2230;border:3px solid #3C4A63;border-radius:28px;box-shadow:0 0 120px rgba(90,140,255,.35);">
        <div style="padding:24px 32px;font-size:34px;font-weight:700;color:#DCE6FF;border-bottom:2px solid #3C4A63;">Pinguine – Wikipedia</div></div>
      {pengs}
    </div>
    {st_a}{st_b}{st_c}""", r"""
  tl.fromTo("#d3-cam", { scale: 1 }, { scale: 1.06, duration: T.end, ease: "none", transformOrigin: "800px 540px" }, 0);
  type("#d3-sa", %d, 0.1); fadeOut("#d3-sa", T.sock - 0.4, 0.3);
  fadeIn("#d3-spray", 0.15, 0.6, { from: { y: 30 }, to: { y: 0 } });
  [0, 1, 2].forEach(i => fadeIn(`#d3-sp${i}`, 0.6 + i * 0.25, 0.5, { from: { scale: 0.6 }, to: { scale: 1 } }));
  fadeOut(["#d3-spray", "#d3-sp0", "#d3-sp1", "#d3-sp2"], T.sock - 0.4, 0.4);
  tl.to("#d3-la", { opacity: 0, duration: 0.6, ease: "power2.inOut" }, T.sock - 0.4);
  tl.to("#d3-lb", { opacity: 1, duration: 0.6, ease: "power2.inOut" }, T.sock - 0.4);
  face("d3o", "happy", "aha", T.sock);
  type("#d3-sb", %d, T.sock); fadeOut("#d3-sb", T.pingu - 0.4, 0.3);
  [0, 1, 2, 3, 4, 5].forEach(i => tl.fromTo(`#d3-k${i}`, { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, T.sock + 0.1 + i * 0.12));
  fadeOut([0, 1, 2, 3, 4, 5].map(i => `#d3-k${i}`), T.pingu - 0.4, 0.4);
  tl.to("#d3-lb", { opacity: 0, duration: 0.6, ease: "power2.inOut" }, T.pingu - 0.4);
  tl.to(["#d3-lc", "#d3-glow"], { opacity: 1, duration: 0.6, ease: "power2.inOut" }, T.pingu - 0.4);
  face("d3o", "aha", "tired", T.pingu + 0.2);
  type("#d3-sc", %d, T.pingu);
  fadeIn("#d3-phone", T.pingu, 0.7, { from: { y: 40 }, to: { y: 0 } });
  [0, 1, 2].forEach(i => fadeIn(`#d3-p${i}`, T.pingu + 0.5 + i * 0.2, 0.5));
  fadeOut("#d3-cam", T.end - 0.35, 0.35); fadeOut("#d3-sc", T.end - 0.35, 0.35);
""" % (na, nb, nc), {"sock": L(W("Sortiert")), "pingu": L(W("liest")), "end": e3 - a3})

# ------------------------------------------------------------ d4 FAUL?
a4, e4 = SEG["s05_faul"][0], SEG["s06_nicht_faul"][1]
L = lambda t: t - a4  # noqa: E731
scene("d4", f"""
    {light("d4-l", 1450, 470, 520, "rgba(255,226,180,.28)")}
    <div class="floor" style="left:1210px;top:820px;width:480px;height:70px;"></div>
    {actor("d4-otto", 1150, OTTO_TOP, 600, 760, otto_svg("d4o", ("excuse", "happy"), pose="raised", held=f'<g id="d4o-sock">{sock(150, -60, "#3F7FB5", 0.8)}</g>'))}
    <div id="d4-say" class="t" style="left:150px;top:300px;font-size:28px;font-weight:700;letter-spacing:.4em;color:{MUTED};">DIE MEISTEN SAGEN</div>
    <div id="d4-faul" class="t cond" style="left:140px;top:360px;font-size:290px;line-height:1;letter-spacing:.06em;">FAUL?</div>
    <div id="d4-line" class="actor" style="left:120px;top:540px;width:860px;height:8px;background:{RED};"></div>""", r"""
  fadeIn("#d4-say", T.meisten - 0.1, 0.5);
  fadeIn("#d4-faul", T.faul - 0.05, 0.6, { from: { scale: 1.08, transformOrigin: "0% 50%" }, to: { scale: 1 } });
  tl.fromTo("#d4-line", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.6, ease: "power2.inOut" }, T.aber);
  tl.to("#d4-faul", { color: "#55585E", duration: 0.5 }, T.aber + 0.3);
  face("d4o", "excuse", "happy", T.aber + 0.4);
  tl.fromTo("#d4o-arm", { rotation: 40, svgOrigin: "86 170" }, { rotation: 0, duration: 0.6, ease: "power2.out" }, T.socken - 0.4);
  tl.fromTo("#d4o-sock", { opacity: 0 }, { opacity: 1, duration: 0.4 }, T.socken - 0.3);
  tl.to(["#d4-faul", "#d4-say", "#d4-line", "#d4-otto", "#d4-l"], { opacity: 0, duration: 0.4, ease: "power2.in" }, T.end - 0.4);
""", {"meisten": L(W("meisten")), "faul": L(W("faul.")), "aber": L(W("Aber")), "socken": L(W("Socken.", a4)), "end": e4 - a4})

# ------------------------------------------------------------ d5 Versprechen
a5, e5 = SEG["s07_versprechen"]
L = lambda t: t - a5  # noqa: E731
mirror = (f'<div id="d5-mirror" class="actor" style="left:1120px;top:200px;width:480px;height:600px;">'
          f'<div style="position:absolute;inset:0 0 30px 0;border-radius:240px 240px 24px 24px;background:#6E5236;border:4px solid #2A2016;"></div>'
          f'<div style="position:absolute;left:30px;top:30px;right:30px;bottom:60px;border-radius:210px 210px 14px 14px;'
          f'background:linear-gradient(160deg,#4A5966,#22292F);overflow:hidden;">'
          f'<div id="d5-du" class="t cond" style="left:0;right:0;top:190px;text-align:center;font-size:150px;color:#E8E2D5;letter-spacing:.1em;">DU?</div></div></div>')
meter = (f'<div id="d5-meter" class="actor" style="left:1200px;top:220px;width:420px;height:600px;">'
         f'<div style="position:absolute;left:150px;bottom:80px;width:120px;height:480px;border:3px solid #CFC9BC;"></div>'
         f'<div id="d5-bar" style="position:absolute;left:156px;bottom:86px;width:108px;height:468px;background:{ORANGE};transform-origin:50% 100%;"></div>'
         f'<div class="t" style="left:0;right:0;bottom:0;text-align:center;font-size:28px;font-weight:700;letter-spacing:.3em;color:#CFC9BC;">AUFSCHIEBEN</div></div>')
chest = (f'<div id="d5-chest" class="actor" style="left:1100px;top:330px;width:560px;height:420px;">'
         + svgbox(f'''<g stroke="#1A140E" stroke-width="5" stroke-linejoin="round">
  <rect x="-200" y="-60" width="400" height="200" rx="12" fill="#7A5634"/>
  <path d="M-200,-60 Q0,-170 200,-60 Z" fill="#8C6640"/>
  <g id="d5-lock"><rect x="-40" y="-40" width="80" height="90" rx="10" fill="#C9A646"/>
  <path d="M-24,-40 v-30 a24,24 0 0 1 48,0 v30" fill="none" stroke-width="9"/></g></g>''', "-280 -200 560 420", 560, 420) + '</div>')
scene("d5", f"""
    <div id="d5-cam" class="lay">
      {light("d5-l", 640, 470, 520, "rgba(255,226,180,.28)")}
      {light("d5-l2", 1400, 500, 520, "rgba(255,226,180,.18)")}
      <div class="floor" style="left:400px;top:820px;width:480px;height:70px;"></div>
      {actor("d5-otto", 340, OTTO_TOP, 600, 760, otto_svg("d5o", ("smirk", "aha", "excuse", "happy"), pose="raised"))}
      {mirror}{meter}{chest}
    </div>
    <div id="d5-wg" class="t" style="left:1000px;top:250px;">
      <div class="cond" style="font-size:84px;line-height:1.05;letter-spacing:.06em;">WISSENSCHAFTLICH<br>GETESTET</div>
      <div id="d5-wgl" style="margin-top:22px;width:520px;height:3px;background:#FFF;transform-origin:0 50%;"></div>
      <div style="margin-top:18px;font-size:28px;font-weight:600;letter-spacing:.12em;color:{MUTED};">WOHL, PYCHYL &amp; BENNETT (2010)</div>
    </div>""", r"""
  tl.fromTo("#d5-cam", { scale: 1 }, { scale: 1.05, duration: T.end, ease: "none", transformOrigin: "800px 540px" }, 0);
  tl.fromTo("#d5o-arm", { rotation: 70, svgOrigin: "86 170" }, { rotation: 0, duration: 0.7, ease: "power2.out" }, T.dir - 0.5);
  fadeIn("#d5-mirror", T.dir - 0.6, 0.8, { from: { y: 30 }, to: { y: 0 } });
  fadeIn("#d5-du", T.dir, 0.6);
  fadeOut("#d5-mirror", T.wenn - 0.4, 0.4);
  tl.fromTo("#d5o-arm", { rotation: 0 }, { rotation: 70, duration: 0.6, ease: "power2.inOut", immediateRender: false }, T.wenn - 0.4);
  face("d5o", "smirk", "aha", T.wenn);
  fadeIn("#d5-meter", T.wenn, 0.6);
  tl.fromTo("#d5-bar", { scaleY: 1 }, { scaleY: 0.3, duration: 1.0, ease: "power2.inOut", immediateRender: false }, T.weniger);
  fadeOut("#d5-meter", T.ende - 0.5, 0.4);
  fadeIn("#d5-chest", T.trick - 0.2, 0.7, { from: { y: 30 }, to: { y: 0 } });
  face("d5o", "aha", "excuse", T.peinlich);
  tl.fromTo("#d5-lock", { rotation: 0, transformOrigin: "50% 0%" }, { keyframes: [{ rotation: -8, duration: 0.12 }, { rotation: 6, duration: 0.14 }, { rotation: 0, duration: 0.16 }], immediateRender: false }, T.peinlich + 0.1);
  tl.to("#d5-chest", { opacity: 0.25, duration: 0.5 }, T.wiss - 0.3);
  fadeIn("#d5-wg", T.wiss, 0.7, { from: { scale: 1.04, transformOrigin: "0% 0%" }, to: { scale: 1 } });
  tl.fromTo("#d5-wgl", { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power3.out" }, T.wiss + 0.3);
  face("d5o", "excuse", "happy", T.wiss + 0.4);
  tl.to(["#d5-cam", "#d5-wg"], { opacity: 0, duration: 0.6, ease: "power2.in" }, T.end - 0.6);
""", {"dir": L(W("dir")), "wenn": L(W("wenn", a5)), "weniger": L(W("weniger")), "ende": L(W("Ende")),
      "trick": L(W("Trick")), "peinlich": L(W("peinlich")), "wiss": L(W("Aber", W("peinlich"))), "end": e5 - a5})

# ------------------------------------------------------------ Kapitelkarten
def chapter(cid, sid, num, title):
    a, e = SEG[sid]
    scene(cid, f"""
    <div id="{cid}-k" class="t" style="left:0;right:0;top:420px;text-align:center;font-size:30px;font-weight:700;letter-spacing:.6em;color:{MUTED};">KAPITEL {num}</div>
    <div id="{cid}-t" class="t cond" style="left:0;right:0;top:480px;text-align:center;font-size:130px;line-height:1;letter-spacing:.12em;">{title}</div>""",
          f"""
  fadeIn("#{cid}-k", 0.1, 0.5);
  tl.fromTo("#{cid}-t", {{ opacity: 0, scale: 1.1 }}, {{ opacity: 1, scale: 1, duration: 1.0, ease: "power2.out" }}, 0.25);
  fadeOut(["#{cid}-k", "#{cid}-t"], T.end - 0.5, 0.45);""", {"end": e - a})
    return (cid, a, e)


HOSTS = [("d0", *SEG["open"]), ("d1", *SEG["s01_hook"]), ("d2", *SEG["title"]), ("d3", a3, e3), ("d4", a4, e4),
         ("d5", *SEG["s07_versprechen"]), chapter("d6", "s08_kap1", 1, "DU BIST NICHT FAUL")]

# ------------------------------------------------------------ Restliche Szenen (Kapitel 1–5, Ende)
exec(open(f"{HERE}/rest.py", encoding="utf-8").read())

# ------------------------------------------------------------ Rahmen: alter Film (Balken, Vignette, Korn, Staub, Kratzer, Flackern)
exec(open(f"{HERE}/film.py", encoding="utf-8").read())

# ------------------------------------------------------------ Untertitel (im unteren Balken)
groups, cur = [], []
for i, w in enumerate(WORDS):
    cur.append(w)
    nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
    if len(cur) >= 7 or re.search(r"[.!?:,]$", w["text"]) or not nxt or (nxt["start"] - w["end"] >= 0.25 and len(cur) >= 3):
        groups.append(cur); cur = []
ch, cj = [], []
starts = [max(g[0]["start"] - 0.05, 0.12) for g in groups] + [END]
for gi, g in enumerate(groups):
    a, b = starts[gi], min(g[-1]["end"] + 0.25, END, starts[gi + 1] - 0.02)
    ch.append(f'<div id="k{gi}" class="clip cap" data-start="{a:.3f}" data-duration="{b - a:.3f}">{" ".join(w["text"] for w in g)}</div>')
    cj.append(f'tl.fromTo("#k{gi}", {{opacity:0}}, {{opacity:1, duration:0.15}}, {a:.3f}); tl.to("#k{gi}", {{opacity:0, duration:0.12}}, {b - 0.12:.3f});')
open(f"{HERE}/compositions/captions.html", "w", encoding="utf-8").write(f"""<template>
  <style>
  #root {{ position:absolute; inset:0; }}
  #root .cap {{ position:absolute; left:0; right:0; top:{1080 - BAR + 44}px; text-align:center; font-family:'Inter', sans-serif;
          font-weight:500; font-size:36px; color:#F2F2F2; letter-spacing:.01em; opacity:0; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1920" data-height="1080" data-layout-allow-caption-zone>
    {"".join(ch)}
  </div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  {"".join(cj)}
  window.__timelines["captions"] = tl;
  </script>
</template>
""")

# ------------------------------------------------------------ SRT für Final Cut / YouTube
def srt_t(x):
    ms = int(round(x * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
with open(f"{HERE}/untertitel_video01.srt", "w", encoding="utf-8") as f:
    for gi, g in enumerate(groups):
        a, b = starts[gi], min(g[-1]["end"] + 0.25, END, starts[gi + 1] - 0.02)
        f.write(f"{gi + 1}\n{srt_t(a)} --> {srt_t(b)}\n{' '.join(w['text'] for w in g)}\n\n")

# ------------------------------------------------------------ Root
NOCAP = "--nocap" in sys.argv
hosts = HOSTS
hh = "\n".join(f'      <div id="{s}" data-composition-id="{s}" data-composition-src="compositions/{s}.html" data-start="{a:.3f}" '
               f'data-duration="{b - a:.3f}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
               for s, a, b in hosts)
open(f"{HERE}/index.html", "w").write(f"""<!doctype html>
<html lang="de" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1920px; height:1080px; overflow:hidden; background:#000; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1920" data-height="1080">
{hh}
      <div id="frame" data-composition-id="frame" data-composition-src="compositions/frame.html" data-start="0" data-duration="{END}" data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{END}" data-track-index="3" data-track-kind="captions" data-width="1920" data-height="1080"{' data-hidden' if NOCAP else ''}></div>
      <audio id="vo" class="clip" src="assets/voice.wav" data-start="0" data-duration="{END}" data-track-index="4" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print(f"Video 01 (Doku): {END}s, {len(WORDS)} Wörter, {len(groups)} Untertitel-Gruppen")
