"""Erzeugt das HyperFrames-Projekt für die Animations-Probe von Video 01 (0:00–0:42.6).

Aufruf: python3 gen.py   (liest Wort-Zeiten aus ../video01/out/untertitel_video01_karaoke.ass)
"""
import json, os, re, subprocess, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "video01"))
import art  # noqa: E402
from art import INK, ORANGE, ORANGE_D, SKIN, GREY, mug, phone, _arm, _hand, _head_base, _face, sparkle, spray, sock, penguin  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "video01", "out")
END = 42.6
os.makedirs(f"{HERE}/compositions", exist_ok=True)
os.makedirs(f"{HERE}/assets", exist_ok=True)

# ------------------------------------------------------------ Wort-Zeiten
WORDS = []
for ln in open(f"{SRC}/untertitel_video01_karaoke.ass", encoding="utf-8"):
    if not ln.startswith("Dialogue:"):
        continue
    f = ln.split(",", 9)
    m = re.search(r"\{\\c&H1A7AFF&\}(.*?)\{\\c&HFFFFFF&\}", f[9])
    if not m:
        continue
    def sec(s):
        h, mi, se = s.split(":")
        return int(h) * 3600 + int(mi) * 60 + float(se)
    a, b = sec(f[1]), sec(f[2])
    if a >= END:
        break
    WORDS.append({"text": m.group(1), "start": round(a, 3), "end": round(min(b, END), 3)})


def norm(w):
    return re.sub(r"[^\wäöüÄÖÜß]", "", w).lower()


def W(word, after=0.0):
    """Startzeit (absolut) des ersten Wortes `word` nach `after`."""
    for w in WORDS:
        if w["start"] >= after - 1e-6 and norm(w["text"]) == norm(word):
            return w["start"]
    raise KeyError(word)


# ------------------------------------------------------------ Otto-Rig
def otto_svg(p, faces=("tired",), pose="down", item=None, held="", label="SPÄTER", bags="normal"):
    """Otto als SVG (600x760 Box, Kopfmitte bei 300,200). Gesichter einzeln schaltbar: #p-face-<name>."""
    b = []
    for lx in (-1, 1):
        d = f"M{45*lx},330 L{52*lx},470"
        b.append(f'<path d="{d}" stroke="{INK}" stroke-width="60" fill="none" stroke-linecap="round"/>'
                 f'<path d="{d}" stroke="{GREY}" stroke-width="48" fill="none" stroke-linecap="round"/>')
    b.append(f'<g stroke="{INK}" stroke-width="6" fill="#FFF"><path d="M-100,500 Q-100,462 -60,462 Q-28,462 -22,500 Z"/>'
             f'<path d="M100,500 Q100,462 60,462 Q28,462 22,500 Z"/></g>'
             f'<path d="M-100,494 L-22,494 M22,494 L100,494" stroke="{ORANGE}" stroke-width="5"/>')
    b.append(_arm("M-86,170 Q-132,235 -124,318") + _hand(-124, 336))
    b.append(f'''<g stroke="{INK}" stroke-width="6">
      <path d="M-92,100 Q0,160 92,100 Q112,150 78,168 L-78,168 Q-112,150 -92,100 Z" fill="{ORANGE_D}"/>
      <rect x="-22" y="100" width="44" height="50" fill="{SKIN}"/>
      <path d="M-96,152 Q0,132 96,152 L110,330 Q0,348 -110,330 Z" fill="{ORANGE}"/>
      <rect x="-112" y="318" width="224" height="26" rx="10" fill="{ORANGE_D}"/>
      <path d="M-52,142 Q0,200 52,142" fill="none"/>
      <path d="M-18,178 L-24,238 M18,178 L24,232" fill="none" stroke-width="5"/>
      <circle cx="-24" cy="244" r="6" fill="#FFF" stroke-width="4"/><circle cx="24" cy="238" r="6" fill="#FFF" stroke-width="4"/>
      <path d="M-62,256 L62,256 L78,318 L-78,318 Z" fill="#F08A3E"/></g>''')
    arm = f'<g id="{p}-arm">'
    if pose == "bent":
        arm += _arm("M86,170 Q140,230 126,272 Q100,300 30,244")
        arm += (mug(48, 190, label) + _hand(24, 234)) if item == "mug" else (held + _hand(30, 244))
    elif pose == "raised":
        arm += _arm("M86,170 Q150,140 150,40") + held + _hand(150, 28)
    else:
        arm += _arm("M86,170 Q132,235 124,318") + _hand(124, 336)
    arm += "</g>"
    b.append(arm)
    fs = "".join(f'<g id="{p}-face-{f}" opacity="{1 if i == 0 else 0}">{_face(f, bags)}</g>' for i, f in enumerate(faces))
    b.append(f'<g id="{p}-head">{_head_base()}{fs}</g>')
    return (f'<svg viewBox="-300 -200 600 760" width="600" height="760" overflow="visible">'
            f'{"".join(b)}</svg>')


def actor(id_, x, y, w, h, inner, extra=""):
    return f'<div id="{id_}" class="actor" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px" {extra}>{inner}</div>'


def svgbox(inner, vb, w, h):
    return f'<svg viewBox="{vb}" width="{w}" height="{h}" overflow="visible">{inner}</svg>'


COMMON_CSS = f"""
  #root {{ position:absolute; inset:0; overflow:hidden; font-family:'Nunito', sans-serif; color:{INK}; }}
  #root .actor {{ position:absolute; }}
  #root .ground {{ position:absolute; inset:0; }}
  #root .cam {{ position:absolute; inset:0; }}
  #root .hero {{ position:absolute; font-family:'Archivo Black', sans-serif; line-height:1; }}
  #root .txt {{ position:absolute; font-weight:800; }}
"""

JS_HELPERS = r"""
  const tl = gsap.timeline({ paused: true });
  const face = (p, from, to, t) => {
    tl.set(`#${p}-face-${from}`, { opacity: 0 }, t);
    tl.set(`#${p}-face-${to}`, { opacity: 1 }, t);
    tl.fromTo(`#${p}-head`, { scaleY: 0.88, transformOrigin: "50% 100%" },
      { scaleY: 1, duration: 0.32, ease: "back.out(2.2)", immediateRender: false }, t);
  };
  const pop = (sel, t, extra = {}) => tl.fromTo(sel, { scale: 0, rotation: extra.rot || 0 },
      { scale: 1, rotation: 0, duration: extra.d || 0.5, ease: extra.ease || "back.out(1.6)" }, t);
"""


def scene(sid, dur, bg, html, js, css=""):
    T = json.dumps({k: round(v, 3) for k, v in js[1].items()})
    src = f"""<template>
  <style>{COMMON_CSS}{css}
  #root {{ background:{bg}; }}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
{html}
  </div>
  <script>
  const T = {T};
{JS_HELPERS}
{js[0]}
  window.__timelines["{sid}"] = tl;
  </script>
</template>
"""
    open(f"{HERE}/compositions/{sid}.html", "w", encoding="utf-8").write(src)


# =============================================================== S1 Hook
S1, S1E = 0.0, 6.63
L = lambda t: t - S1  # noqa: E731
todo = (f'<div id="s1-todo" class="actor" style="left:1080px;top:300px;width:560px;height:330px;background:#FFF;'
        f'border:6px solid {INK};border-radius:22px;padding:34px 40px;">'
        f'<div style="font-family:Archivo Black;font-size:44px;">HEUTE</div>'
        f'<div style="display:flex;align-items:center;gap:26px;margin-top:40px;font-size:52px;font-weight:800;">'
        f'<div style="width:62px;height:62px;border:6px solid {INK};border-radius:10px;"></div>Steuererklärung</div>'
        f'<div style="margin-top:28px;font-size:30px;color:#888;font-weight:700;">1 Aufgabe · Deadline Freitag</div></div>')
letters = "".join(f'<span id="s1-l{i}" style="display:inline-block">{c}</span>' for i, c in enumerate("OTTO"))
s1_html = f"""
    <div id="s1-cam" class="cam">
      {actor("s1-otto", 360, 150, 600, 760, otto_svg("s1o", ("tired", "smirk"), pose="bent", item="mug"))}
      <div id="s1-name" class="hero" style="left:1060px;top:360px;font-size:250px;">{letters}</div>
      {todo}
    </div>"""
s1_T = dict(otto=L(W("Otto")), heute=L(W("heute")), aufgabe=L(W("Aufgabe")), und=L(W("Und", 4)),
            nicht=L(W("nicht", 4)), end=S1E - S1)
s1_js = r"""
  tl.fromTo("#s1-otto", { y: 820 }, { y: 0, duration: 0.6, ease: "back.out(1.3)" }, 0.08);
  tl.fromTo("#s1-otto", { scaleY: 1 }, { keyframes: [{ scaleY: 0.9, scaleX: 1.06, duration: 0.09 }, { scaleY: 1, scaleX: 1, duration: 0.3, ease: "back.out(3)" }], transformOrigin: "50% 92%", immediateRender: false }, 0.6);
  ["#s1-l0", "#s1-l1", "#s1-l2", "#s1-l3"].forEach((s, i) => tl.fromTo(s, { opacity: 0, y: 40, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.25, ease: "expo.out" }, T.otto + i * 0.09));
  tl.to("#s1-name", { opacity: 0, filter: "blur(10px)", duration: 0.2, ease: "power3.in" }, T.heute - 0.25);
  tl.fromTo("#s1-todo", { scale: 0.5, opacity: 0, rotation: 6 }, { scale: 1, opacity: 1, rotation: -2, duration: 0.55, ease: "back.out(1.5)" }, T.heute);
  face("s1o", "tired", "smirk", T.und);
  tl.to("#s1-todo", { x: 900, rotation: 18, duration: 0.45, ease: "power3.in" }, T.und + 0.25);
  tl.fromTo("#s1-cam", { scale: 1 }, { scale: 2.6, x: 217, y: -40, transformOrigin: "743px 580px", duration: 0.4, ease: "power3.out", immediateRender: false }, T.nicht);
"""
scene("s1", S1E - S1, "#FFF8EE", s1_html, (s1_js, s1_T))

# ========================================================= S2 Montage
S2, S2E = 6.63, 15.32
L = lambda t: t - S2  # noqa: E731
socks_html = "".join(actor(f"s2-sock{i}", 1010 + i * 128, 470, 150, 200,
                           svgbox(sock(0, 0, c, 0.9), "-60 -90 150 200", 150, 200))
                     for i, c in enumerate(["#FF4D4D", "#FFB300", "#FFE14D", "#4CD964", "#3FA9F5", "#9B59B6"]))
sparks_html = "".join(actor(f"s2-sp{i}", x, y, 120, 120, svgbox(sparkle(0, 0, s), "-60 -60 120 120", 120, 120))
                      for i, (x, y, s) in enumerate([(1180, 300, 1.4), (1440, 520, 1.0), (1120, 640, 1.2), (1560, 250, 0.8)]))
pengs = "".join(actor(f"s2-p{i}", x, y, 160, 200, svgbox(penguin(0, 0, s), "-80 -100 160 200", 160, 200))
                for i, (x, y, s) in enumerate([(1080, 470, 1.7), (1270, 500, 1.3), (1420, 530, 1.0)]))
clock_html = (f'<div id="s2-clock" class="actor" style="left:1500px;top:90px;width:300px;height:130px;background:{INK};'
              f'border-radius:24px;overflow:hidden;">'
              + "".join(f'<div id="s2-t{i}" style="position:absolute;inset:14px;background:#2E3B2E;border-radius:12px;'
                        f'color:#7CFF8A;font-family:Space Mono;font-weight:700;font-size:70px;display:flex;align-items:center;'
                        f'justify-content:center;opacity:{1 if i == 0 else 0}">{t}</div>' for i, t in enumerate(["11:30", "14:00", "17:30"]))
              + "</div>")
phone_card = (f'<div id="s2-phone" class="actor" style="left:990px;top:270px;width:600px;height:470px;background:#FFF;'
              f'border:6px solid {INK};border-radius:30px;">'
              f'<div style="padding:24px 34px;font-size:40px;font-weight:800;border-bottom:4px solid #DDD;">Pinguine – Wikipedia</div></div>')
s2_html = f"""
    <div id="s2-g1" class="ground" style="background:#DDEFFF"></div>
    <div id="s2-g2" class="ground" style="background:#FFF0D2;opacity:0"></div>
    <div id="s2-g3" class="ground" style="background:#E6F4EA;opacity:0"></div>
    <div id="s2-stage" class="cam">
      {actor("s2-otto", 360, 150, 600, 760, otto_svg("s2o", ("happy", "aha", "tired"), pose="down"))}
      {actor("s2-spray", 980, 330, 200, 260, svgbox(spray(0, 0, 1.6), "-80 -110 200 260", 200, 260))}
      {sparks_html}
      {socks_html}
      {phone_card}
      {pengs}
      <div id="s2-2h" class="hero" style="left:1630px;top:250px;font-size:64px;color:{ORANGE};">+2 Std.</div>
      {clock_html}
    </div>"""
s2_T = dict(socken=L(W("Sortiert")), farbe=L(W("Farbe")), pingu=L(W("liest")), stunden=L(W("Stunden")), end=S2E - S2)
s2_js = r"""
  tl.fromTo("#s2-spray", { y: 300, rotation: 30, opacity: 0 }, { y: 0, rotation: -10, opacity: 1, duration: 0.5, ease: "back.out(1.6)" }, 0.1);
  tl.to("#s2-spray", { rotation: 8, duration: 0.18, ease: "power2.inOut", yoyo: true, repeat: 3 }, 0.6);
  [0, 1, 2, 3].forEach(i => pop(`#s2-sp${i}`, 0.55 + i * 0.16, { rot: -90 }));
  tl.to(["#s2-spray", "#s2-sp0", "#s2-sp1", "#s2-sp2", "#s2-sp3"], { y: -900, opacity: 0, duration: 0.35, ease: "power3.in", stagger: 0.03 }, T.socken - 0.3);
  tl.to("#s2-g2", { opacity: 1, duration: 0.4, ease: "power2.inOut" }, T.socken - 0.2);
  face("s2o", "happy", "aha", T.socken);
  [0, 1, 2, 3, 4, 5].forEach(i => tl.fromTo(`#s2-sock${i}`, { x: 900, y: -260, rotation: 160, opacity: 0 }, { x: 0, y: 0, rotation: 0, opacity: 1, duration: 0.5, ease: "back.out(1.4)" }, T.socken + 0.05 + i * 0.12));
  tl.to("#s2-t0", { y: -110, opacity: 0, duration: 0.22, ease: "power3.in" }, T.socken - 0.15);
  tl.fromTo("#s2-t1", { y: 110, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "expo.out" }, T.socken + 0.05);
  tl.to([0, 1, 2, 3, 4, 5].map(i => `#s2-sock${i}`), { y: 700, opacity: 0, duration: 0.35, ease: "power3.in", stagger: 0.03 }, T.pingu - 0.3);
  tl.to("#s2-g3", { opacity: 1, duration: 0.4, ease: "power2.inOut" }, T.pingu - 0.2);
  tl.fromTo("#s2-phone", { y: 700, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: "expo.out" }, T.pingu);
  [0, 1, 2].forEach(i => pop(`#s2-p${i}`, T.pingu + 0.35 + i * 0.13));
  face("s2o", "aha", "tired", T.stunden);
  tl.to("#s2-t1", { y: -110, opacity: 0, duration: 0.22, ease: "power3.in" }, T.stunden - 0.15);
  tl.fromTo("#s2-t2", { y: 110, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "expo.out" }, T.stunden + 0.05);
  tl.fromTo("#s2-2h", { opacity: 0, scale: 1.6, filter: "blur(8px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out" }, T.stunden + 0.1);
  tl.to("#s2-stage", { x: -1400, filter: "blur(18px)", duration: 0.28, ease: "power3.in" }, T.end - 0.28);
"""
scene("s2", S2E - S2, "#DDEFFF", s2_html, (s2_js, s2_T))

# ============================================================ S3 FAUL?
S3, S3E = 15.32, 22.18
L = lambda t: t - S3  # noqa: E731
s3_html = f"""
    <div id="s3-cam" class="cam">
      {actor("s3-otto", 1240, 150, 600, 760, otto_svg("s3o", ("excuse", "happy"), pose="raised", held=f'<g id="s3o-sock">{sock(150, -60, "#3FA9F5", 0.8)}</g>'))}
      <div id="s3-say" class="txt" style="left:170px;top:250px;font-size:56px;">
        <span id="s3-w0">Die</span> <span id="s3-w1">meisten</span> <span id="s3-w2">sagen:</span></div>
      <div id="s3-faul" class="hero" style="left:150px;top:360px;font-size:300px;">FAUL?</div>
      <div id="s3-strike" class="actor" style="left:130px;top:500px;width:1060px;height:34px;background:#FF3B30;border-radius:17px;"></div>
    </div>"""
s3_T = dict(meisten=L(W("meisten")), sagen=L(W("sagen")), faul=L(W("faul")), aber=L(W("Aber")),
            socken=L(W("Socken", 19)), end=S3E - S3)
s3_js = r"""
  tl.fromTo("#s3-otto", { x: 700, filter: "blur(16px)" }, { x: 0, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }, 0);
  tl.fromTo(["#s3-w0", "#s3-w1", "#s3-w2"], { color: "#C9C2B6" }, { color: "#1E1E1E", duration: 0.12, stagger: 0.09 }, T.meisten - 0.1);
  tl.fromTo("#s3-faul", { opacity: 0, scale: 2.4, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.28, ease: "expo.out", transformOrigin: "40% 50%" }, T.faul);
  tl.fromTo("#s3-cam", { x: 0 }, { keyframes: [{ x: -14, duration: 0.04 }, { x: 12, duration: 0.04 }, { x: -6, duration: 0.04 }, { x: 0, duration: 0.05 }], immediateRender: false }, T.faul + 0.2);
  tl.fromTo("#s3-strike", { scaleX: 0, rotation: -8, transformOrigin: "0% 50%" }, { scaleX: 1, rotation: -8, duration: 0.32, ease: "power2.inOut" }, T.aber);
  tl.to("#s3-faul", { color: "#B9B2A6", duration: 0.3 }, T.aber + 0.2);
  face("s3o", "excuse", "happy", T.aber + 0.3);
  tl.fromTo("#s3o-sock", { scale: 0, svgOrigin: "150 0" }, { scale: 1, duration: 0.45, ease: "back.out(2)" }, T.socken - 0.25);
  tl.fromTo("#s3o-arm", { rotation: 40, svgOrigin: "86 170" }, { rotation: 0, duration: 0.45, ease: "back.out(1.6)" }, T.socken - 0.35);
"""
scene("s3", S3E - S3, "#FFF8EE", s3_html, (s3_js, s3_T))

# ======================================================== S4 Versprechen
S4, S4E = 22.18, 40.41
L = lambda t: t - S4  # noqa: E731
mirror = (f'<div id="s4-mirror" class="actor" style="left:1100px;top:170px;width:520px;height:640px;">'
          f'<div style="position:absolute;left:236px;top:600px;width:48px;height:60px;background:#9AA0A6;border:6px solid {INK};"></div>'
          f'<div style="position:absolute;inset:0 0 40px 0;border-radius:260px 260px 30px 30px;background:#C68A4E;border:6px solid {INK};"></div>'
          f'<div style="position:absolute;left:34px;top:34px;right:34px;bottom:74px;border-radius:230px 230px 18px 18px;'
          f'background:#DCEBF2;border:5px solid {INK};overflow:hidden;">'
          f'<div style="position:absolute;left:40px;top:60px;width:60px;height:300px;background:#FFF;opacity:.7;transform-origin:center;rotate:25deg;"></div>'
          f'<div id="s4-du" class="hero" style="left:0;right:0;top:190px;text-align:center;font-size:170px;color:{ORANGE};">DU?</div></div></div>')
bar = (f'<div id="s4-meter" class="actor" style="left:1180px;top:200px;width:460px;height:600px;">'
       f'<div style="position:absolute;left:150px;bottom:80px;width:160px;height:520px;border:6px solid {INK};border-radius:16px;background:#FFF;"></div>'
       f'<div id="s4-bar" style="position:absolute;left:156px;bottom:86px;width:148px;height:508px;background:{ORANGE};border-radius:10px;transform-origin:50% 100%;"></div>'
       f'<div style="position:absolute;left:0;right:0;bottom:0;text-align:center;font-size:46px;font-weight:800;">Aufschieben</div></div>')
chest = (f'<div id="s4-chest" class="actor" style="left:1080px;top:330px;width:560px;height:420px;">'
         + svgbox(f'''<g stroke="{INK}" stroke-width="6" stroke-linejoin="round">
  <rect x="-200" y="-60" width="400" height="200" rx="16" fill="#C68A4E"/>
  <path d="M-200,-60 Q0,-170 200,-60 Z" fill="#D9A066"/>
  <g id="s4-lock"><rect x="-40" y="-40" width="80" height="90" rx="10" fill="#FFD43B"/>
  <path d="M-24,-40 v-30 a24,24 0 0 1 48,0 v30" fill="none" stroke-width="10"/></g>
  {art.text(0, 120, "TRICK", 48, color="#FFF", extra='stroke="none"')}</g>''', "-280 -200 560 420", 560, 420) + '</div>')
stamp = (f'<div id="s4-stamp" class="actor" style="left:1000px;top:460px;width:720px;height:150px;border:10px solid #D7263D;'
         f'border-radius:18px;color:#D7263D;font-family:Archivo Black;font-size:50px;line-height:1.05;text-align:center;'
         f'padding-top:18px;background:rgba(255,248,238,.85);">WISSENSCHAFTLICH<br>GETESTET ✓</div>')
iris = f'<div id="s4-iris" class="actor" style="left:1310px;top:530px;width:100px;height:100px;border-radius:50%;background:{ORANGE};"></div>'
s4_html = f"""
    <div id="s4-cam" class="cam">
      {actor("s4-otto", 330, 150, 600, 760, otto_svg("s4o", ("smirk", "aha", "excuse", "happy"), pose="raised"))}
      {mirror}
      {bar}
      {chest}
      {stamp}
      {iris}
    </div>"""
s4_T = dict(dir=L(W("dir", 22)), anderes=L(W("anderes")), wenn=L(W("wenn", 27)), weniger=L(W("weniger")),
            ende=L(W("Ende")), trick=L(W("Trick")), peinlich=L(W("peinlich")), aber=L(W("Aber", 35)),
            getestet=L(W("wissenschaftlich")), end=S4E - S4)
s4_js = r"""
  tl.fromTo("#s4-otto", { y: 0 }, { y: 0, duration: 0.01 }, 0);
  tl.fromTo("#s4o-arm", { rotation: 70, svgOrigin: "86 170" }, { rotation: 0, duration: 0.5, ease: "back.out(1.6)" }, T.dir - 0.4);
  tl.fromTo("#s4-mirror", { y: 800, rotation: 8 }, { y: 0, rotation: 0, duration: 0.6, ease: "back.out(1.3)" }, T.dir - 0.55);
  tl.fromTo("#s4-du", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, T.dir);
  tl.to("#s4-mirror", { x: 1000, rotation: 15, duration: 0.4, ease: "power3.in" }, T.wenn - 0.3);
  tl.fromTo("#s4o-arm", { rotation: 0 }, { rotation: 70, duration: 0.4, ease: "power2.inOut", immediateRender: false }, T.wenn - 0.3);
  face("s4o", "smirk", "aha", T.wenn);
  tl.fromTo("#s4-meter", { y: 900 }, { y: 0, duration: 0.55, ease: "expo.out" }, T.wenn);
  tl.fromTo("#s4-bar", { scaleY: 1 }, { scaleY: 0.3, duration: 0.7, ease: "back.out(1.2)", immediateRender: false }, T.weniger);
  tl.to("#s4-meter", { y: 900, duration: 0.35, ease: "power3.in" }, T.ende - 0.4);
  tl.fromTo("#s4-chest", { scale: 0, rotation: -12, transformOrigin: "50% 80%" }, { scale: 1, rotation: 0, duration: 0.6, ease: "back.out(1.7)" }, T.trick - 0.15);
  face("s4o", "aha", "excuse", T.peinlich);
  tl.fromTo("#s4-lock", { rotation: 0, transformOrigin: "50% 0%" }, { keyframes: [{ rotation: -14, duration: 0.08 }, { rotation: 12, duration: 0.1 }, { rotation: -6, duration: 0.1 }, { rotation: 0, duration: 0.12 }], immediateRender: false }, T.peinlich + 0.1);
  tl.fromTo("#s4-stamp", { opacity: 0, scale: 2.4, rotation: -2 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.2, ease: "expo.out" }, T.getestet - 0.1);
  tl.fromTo("#s4-cam", { x: 0 }, { keyframes: [{ x: -12, y: 6, duration: 0.04 }, { x: 10, y: -4, duration: 0.04 }, { x: 0, y: 0, duration: 0.06 }], immediateRender: false }, T.getestet + 0.1);
  face("s4o", "excuse", "happy", T.getestet + 0.15);
  tl.fromTo("#s4-iris", { scale: 0 }, { scale: 48, duration: 0.45, ease: "power3.in" }, T.end - 0.45);
"""
scene("s4", S4E - S4, "#FFF8EE", s4_html, (s4_js, s4_T))

# ======================================================== S5 Kapitelkarte
S5, S5E = 40.41, END
title_words = "".join(f'<span id="s5-w{i}" style="display:inline-block;margin:0 14px">{w}</span>' for i, w in enumerate("Du bist nicht faul".split()))
s5_html = f"""
    <div id="s5-kap" class="txt" style="left:0;right:0;top:330px;text-align:center;font-size:60px;color:#FFE0C2;letter-spacing:.2em;">KAPITEL 1</div>
    <div id="s5-title" class="hero" style="left:0;right:0;top:420px;text-align:center;font-size:150px;color:#FFF;">{title_words}</div>
    {actor("s5-head", 810, 640, 300, 300, svgbox(_head_base() + _face("tired"), "-150 -180 300 300", 300, 300))}"""
s5_js = r"""
  tl.fromTo("#s5-kap", { opacity: 0, filter: "blur(6px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "expo.out" }, 0.05);
  [0, 1, 2, 3].forEach(i => tl.fromTo(`#s5-w${i}`, { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.15, ease: "expo.out" }, 0.08 + i * 0.06));
  tl.fromTo("#s5-head", { y: 400 }, { y: 0, duration: 0.5, ease: "back.out(1.5)" }, 0.45);
"""
scene("s5", S5E - S5, ORANGE, s5_html, (s5_js, {}))

# ============================================================ Captions
groups, cur = [], []
for i, w in enumerate(WORDS):
    cur.append(w)
    nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
    if len(cur) >= 4 or re.search(r"[.!?:]$", w["text"]) or not nxt or nxt["start"] - w["end"] >= 0.15:
        groups.append(cur); cur = []
cap_html, cap_js = [], []
for gi, g in enumerate(groups):
    a, b = max(g[0]["start"] - 0.05, 0.12), min(g[-1]["end"] + 0.12, END)
    spans = " ".join(f'<span id="c{gi}w{wi}">{w["text"]}</span>' for wi, w in enumerate(g))
    cap_html.append(f'<div id="c{gi}" class="clip cap" data-start="{a:.3f}" data-duration="{b - a:.3f}">{spans}</div>')
    cap_js.append(f'tl.fromTo("#c{gi}", {{opacity:0}}, {{opacity:1, duration:0.1}}, {a:.3f});')
    for wi, w in enumerate(g):
        cap_js.append(f'tl.set("#c{gi}w{wi}", {{color:"#C24E00"}}, {w["start"]:.3f}); tl.set("#c{gi}w{wi}", {{color:"{INK}"}}, {w["end"]:.3f});')
    cap_js.append(f'tl.set("#c{gi}", {{opacity:0}}, {b:.3f});')
cap_src = f"""<template>
  <style>
  #root {{ position:absolute; inset:0; }}
  #root .cap {{ position:absolute; left:0; right:0; bottom:70px; text-align:center; font-family:'Nunito', sans-serif;
           font-weight:900; font-size:58px; color:{INK}; overflow:visible; opacity:0;
           text-shadow: 0 0 10px rgba(255,248,238,.9), 0 0 3px rgba(255,248,238,1); }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1920" data-height="1080" data-layout-allow-caption-zone>
    {"".join(cap_html)}
  </div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  {"".join(cap_js)}
  window.__timelines["captions"] = tl;
  </script>
</template>
"""
open(f"{HERE}/compositions/captions.html", "w", encoding="utf-8").write(cap_src)

# ============================================================ Root + Audio
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{SRC}/voiceover_video01.wav", "-t", str(END),
                "-af", f"afade=t=out:st={END - 0.4}:d=0.4", "-ar", "48000", f"{HERE}/assets/voice.wav"], check=True)
hosts = [("s1", S1, S1E), ("s2", S2, S2E), ("s3", S3, S3E), ("s4", S4, S4E), ("s5", S5, S5E)]
host_html = "\n".join(
    f'      <div id="{s}" data-composition-id="{s}" data-composition-src="compositions/{s}.html" data-start="{a:.3f}" '
    f'data-duration="{b - a:.3f}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
    for s, a, b in hosts)
index = f"""<!doctype html>
<html lang="de" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ margin:0; width:1920px; height:1080px; overflow:hidden; background:#FFF8EE; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1920" data-height="1080">
{host_html}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{END}" data-track-index="2" data-track-kind="captions" data-width="1920" data-height="1080"></div>
      <audio id="vo" class="clip" src="assets/voice.wav" data-start="0" data-duration="{END}" data-track-index="3" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
open(f"{HERE}/index.html", "w", encoding="utf-8").write(index)
for fn in ("hyperframes.json", "meta.json", "package.json"):
    p = f"{HERE}/{fn}"
    if not os.path.exists(p):
        src = f"/home/user/hf/otto-test/{fn}"
        if os.path.exists(src):
            open(p, "w").write(open(src).read().replace("otto-test", "otto-video01-probe"))
print(f"{len(WORDS)} Wörter, {len(groups)} Untertitel-Gruppen, {len(hosts)} Szenen")
