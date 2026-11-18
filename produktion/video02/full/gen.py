"""Video 02 – Testvideo (ca. 1 Min.): Doku-Look + mehr Motion Graphics + interaktive Elemente (Mauszeiger, Umfrage, UI-Karten).

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
    T = {k: v - a for k, v in T.items()}
    T["end"] = e - a
    scene(cid, html, js, T)
    HOSTS.append((cid, a, e))
    return a


# ================================================================ c0 Kaltstart: Uhr tickt, Tippen
a, e = SEG["open"]
lines = "".join(f'<div id="c0-l{i}" style="height:14px;margin:12px 0;width:{w}%;background:#C5CCD6;border-radius:4px;opacity:0"></div>'
                for i, w in enumerate([82, 64, 90, 71, 55, 88, 77, 60, 93, 69]))
put("c0", "open", f"""
  <div id="c0-cam" class="lay">
    {light("c0-l", 960, 620, 520, "rgba(140,190,255,.22)")}
    <div id="c0-clock" class="t" style="left:0;right:0;top:230px;text-align:center;font-family:'Space Mono';font-weight:700;font-size:150px;color:#FF5A4A;text-shadow:0 0 40px rgba(255,60,40,.6);">
      <span style="font-size:60px;color:#B44;vertical-align:middle;margin-right:30px">FR</span>23:58:<span id="c0-s">47</span></div>
    <div id="c0-lap" class="actor" style="left:660px;top:520px;width:600px;height:330px;background:#2E333B;border:5px solid #111;border-radius:16px;padding:26px 34px;">
      <div style="background:#F4F5F7;border-radius:6px;height:100%;padding:14px 22px;overflow:hidden">{lines}</div></div>
  </div>""", r"""
  fadeIn("#c0-cam", 0, 0.25);
  ["48", "49", "50"].forEach((s, i) => tl.set("#c0-s", { textContent: s }, 0.8 + i));
  for (let i = 0; i < 10; i++) tl.fromTo(`#c0-l${i}`, { opacity: 0, scaleX: 0, transformOrigin: "0 50%" }, { opacity: 1, scaleX: 1, duration: 0.12, ease: "none" }, 0.35 + i * 0.22);
  tl.fromTo("#c0-cam", { x: 0 }, { keyframes: [...Array(16)].map((_, i) => ({ x: (i % 2 ? 3 : -3), y: (i % 3 ? -2 : 2), duration: 0.12 })), immediateRender: false }, 0.6);
  fadeOut("#c0-cam", T.end - 0.25, 0.25);
""", {})
SFX += [(0.1, "tick", 0.32), (0.35, "typing", 0.38)]

# ================================================================ c1 Hook: Datei, Kalender, Fortschritt, Sterne
S = "v_hook"; a = SEG[S][0]
cal = "".join(f'<div id="c1-d{i}" style="position:absolute;left:{(i % 7) * 74}px;top:{60 + (i // 7) * 74}px;width:64px;height:64px;border-radius:10px;'
              f'background:#22262E;border:2px solid #3A3F48;font-size:24px;font-weight:700;color:#9AA0AA;display:flex;align-items:center;justify-content:center;opacity:0">{i + 1}'
              f'<div id="c1-x{i}" style="position:absolute;inset:0;opacity:0"><svg viewBox="0 0 64 64" width="64" height="64"><path d="M14,14 L50,50 M50,14 L14,50" stroke="{RED}" stroke-width="7" stroke-linecap="round"/></svg></div></div>'
              for i in range(21))
stars = "".join(f'<div id="c1-st{i}" class="t" style="left:{1030 + i * 92}px;top:690px;font-size:84px;color:{AMBER};opacity:0">★</div>' for i in range(5))
T1 = dict(otto=W("Otto.", a), praes=W("Präsentation", a), drei=W("drei", a), wochen=W("Wochen", a), letzten=W("letzten", a),
          stunden=W("Stunden.", a), gut=W("richtig", a))
put("c1", S, f"""
  <div id="c1-cam" class="lay">
    {light("c1-l", 640, 470, 520, "rgba(255,226,180,.30)")}
    {light("c1-l2", 1360, 470, 620, "rgba(140,190,255,.10)")}
    <div class="floor" style="left:400px;top:820px;width:480px;height:70px;"></div>
    {actor("c1-otto", 340, OTTO_TOP, 600, 760, otto_svg("c1o", ("tired", "shock", "happy")))}
    <div id="c1-file" class="actor card" style="left:1010px;top:200px;width:520px;height:110px;display:flex;align-items:center;gap:26px;padding:0 30px;opacity:0">
      <div style="width:56px;height:70px;background:{ORANGE};border-radius:6px;position:relative"><div style="position:absolute;right:0;top:0;width:18px;height:18px;background:#0B0C0E;"></div></div>
      <div style="font-size:36px;font-weight:700">Präsentation.pptx</div></div>
    <div id="c1-cal" class="actor" style="left:1010px;top:330px;width:520px;height:300px;opacity:0">
      <div class="t" style="left:0;top:0;font-size:28px;font-weight:800;letter-spacing:.3em;color:{AMBER}">3 WOCHEN ZEIT</div>{cal}</div>
    <div id="c1-chip" class="actor" style="left:1010px;top:340px;padding:10px 26px;border-radius:14px;background:{RED};font-size:40px;font-weight:900;letter-spacing:.06em;opacity:0">NUR NOCH 3 STD</div>
    <div id="c1-prog" class="actor card" style="left:1010px;top:440px;width:620px;height:150px;padding:26px 30px;opacity:0">
      <div style="display:flex;justify-content:space-between;font-size:30px;font-weight:700"><span>Wird gespeichert …</span><span><span id="c1-pct">0</span> %</span></div>
      <div style="margin-top:22px;height:22px;border-radius:11px;background:#2A2E36;overflow:hidden"><div id="c1-bar" style="height:100%;width:100%;background:linear-gradient(90deg,{ORANGE},{AMBER});transform-origin:0 50%"></div></div></div>
    <div id="c1-save" class="actor" style="left:1440px;top:610px;padding:12px 26px;border-radius:12px;background:#2D6CDF;font-size:30px;font-weight:800;opacity:0">SPEICHERN</div>
    {stars}
    {cursor("c1", 1300, 900)}
  </div>""", r"""
  fadeIn("#c1-cam", 0, 0.4);
  popIn("#c1-file", T.praes - 0.1);
  fadeIn("#c1-cal", T.drei - 0.1, 0.3);
  for (let i = 0; i < 21; i++) tl.fromTo(`#c1-d${i}`, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: "back.out(2)" }, T.drei + i * 0.02);
  for (let i = 0; i < 21; i++) tl.fromTo(`#c1-x${i}`, { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.12 }, T.wochen + 0.5 + i * 0.045);
  face("c1o", "tired", "shock", T.letzten - 0.2);
  tl.to("#c1-cal", { scale: 0.2, opacity: 0, duration: 0.45, ease: "power3.in", transformOrigin: "10% 10%" }, T.letzten);
  popIn("#c1-chip", T.stunden - 0.1, 0.45);
  fadeIn("#c1-prog", T.stunden + 0.1, 0.4, { from: { y: 30 }, to: { y: 0 } });
  tl.fromTo("#c1-bar", { scaleX: 0 }, { scaleX: 1, duration: 1.2, ease: "power2.inOut" }, T.stunden + 0.3);
  tl.fromTo("#c1-pct", { textContent: 0 }, { textContent: 100, duration: 1.2, ease: "power2.inOut", snap: { textContent: 1 } }, T.stunden + 0.3);
  popIn("#c1-save", T.stunden + 0.5, 0.35);
  fadeIn("#c1-cur", T.stunden + 0.4, 0.2);
  move("#c1-cur", 270, -240, T.stunden + 0.5, 0.7);
  click("c1", T.stunden + 1.3);
  tl.to(["#c1-prog", "#c1-save", "#c1-chip", "#c1-file"], { opacity: 0.25, duration: 0.4 }, T.gut - 0.3);
  fadeOut("#c1-cur", T.gut - 0.3, 0.2);
  face("c1o", "shock", "happy", T.gut);
  for (let i = 0; i < 5; i++) tl.fromTo(`#c1-st${i}`, { opacity: 0, scale: 0, rotation: -90 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2.5)" }, T.gut + i * 0.12);
  fadeOut("#c1-cam", T.end - 0.3, 0.3);
""", T1)
SFX += [(T1["otto"] + 0.1, "click", 0.0)]  # Platzhalter (ohne Lautstärke)
SFX += [(T1["praes"], "pop", 0.5), (T1["stunden"] - 0.05, "pop", 0.5), (T1["stunden"] + 1.3, "click", 0.9)]
SFX += [(T1["gut"] + i * 0.12, "pop", 0.35) for i in range(5)]

# ================================================================ c2 Genie oder Gehirn-Trick?
S = "v_frage"; a = SEG[S][0]
bulb = f'''<g stroke="#111" stroke-width="5"><path d="M-30,30 a60,60 0 1 1 60,0 l0,40 l-60,0 Z" fill="#FFD43B"/><rect x="-32" y="70" width="64" height="26" rx="6" fill="#9AA0A6"/></g>'''
T2 = dict(genie=W("Genie,", a), druck=W("Druck", a), oder=W("Oder", a), gehirn=W("Gehirn", a), streich=W("Streich?", a))
put("c2", S, f"""
  <div id="c2-cam" class="lay">
    {light("c2-la", 560, 500, 480, "rgba(255,220,120,.22)")}
    {light("c2-lb", 1360, 500, 480, "rgba(255,160,190,.18)")}
    <div id="c2-a" class="actor card" style="left:250px;top:230px;width:620px;height:560px;opacity:0">
      {light("c2-glow", 310, 220, 200, "rgba(255,220,120,.55)", 0)}
      <div style="position:absolute;left:210px;top:60px">{svgbox(bulb, "-100 -110 200 230", 200, 230)}</div>
      <div class="t cond" style="left:0;right:0;top:330px;text-align:center;font-size:110px;">GENIE?</div>
      <div class="t" style="left:0;right:0;top:460px;text-align:center;font-size:30px;font-weight:700;letter-spacing:.2em;color:{MUTED}">BRAUCHT NUR DRUCK</div></div>
    <div id="c2-b" class="actor card" style="left:1050px;top:230px;width:620px;height:560px;opacity:0">
      <div style="position:absolute;left:140px;top:50px">{svgbox(art.brain(0, 0, 0.9, "#9C6F80"), "-200 -180 400 330", 340, 280)}</div>
      <div class="t cond" style="left:0;right:0;top:330px;text-align:center;font-size:96px;">GEHIRN-TRICK?</div>
      <div class="t" style="left:0;right:0;top:460px;text-align:center;font-size:30px;font-weight:700;letter-spacing:.2em;color:{MUTED}">EIN STREICH IM KOPF</div></div>
    <div id="c2-q" class="t cond" style="left:900px;top:420px;width:120px;text-align:center;font-size:150px;color:{AMBER};opacity:0">?</div>
    {cursor("c2", 900, 900)}
  </div>""", r"""
  fadeIn("#c2-cam", 0, 0.3);
  tl.fromTo("#c2-a", { opacity: 0, x: -400, rotation: -8 }, { opacity: 1, x: 0, rotation: -2, duration: 0.7, ease: "power4.out" }, T.genie - 0.3);
  tl.fromTo("#c2-glow", { opacity: 0 }, { opacity: 1, duration: 0.6 }, T.druck);
  tl.fromTo("#c2-b", { opacity: 0, x: 400, rotation: 8 }, { opacity: 1, x: 0, rotation: 2, duration: 0.7, ease: "power4.out" }, T.oder);
  tl.fromTo("#c2-q", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, T.oder + 0.3);
  tl.fromTo("#c2-q", { rotation: 0 }, { rotation: 360, duration: 3, ease: "none", immediateRender: false }, T.oder + 0.3);
  fadeIn("#c2-cur", T.druck - 0.2, 0.2);
  move("#c2-cur", -340, -330, T.druck - 0.1, 0.8);
  tl.to("#c2-a", { scale: 1.04, duration: 0.3 }, T.druck + 0.6);
  move("#c2-cur", 460, -330, T.gehirn - 0.4, 0.8);
  tl.to("#c2-a", { scale: 1, opacity: 0.6, duration: 0.3 }, T.gehirn);
  tl.to("#c2-b", { scale: 1.04, duration: 0.3 }, T.gehirn + 0.2);
  fadeOut("#c2-cam", T.end - 0.3, 0.3);
""", T2)
SFX += [(T2["genie"] - 0.3, "whoosh", 0.35), (T2["oder"], "whoosh", 0.35)]

# ================================================================ c3 Umfrage A/B/C
S = "v_poll"; a = SEG[S][0]
q_html, nq = typed("c3-qq", "Wann hast du deine letzte große Aufgabe erledigt?", "left:60px;top:120px;font-size:40px;letter-spacing:0;font-weight:700;color:#FFF;")
opts = [("A", "Früh"), ("B", "Pünktlich"), ("C", "In letzter Minute")]
oh = "".join(f'<div id="c3-o{i}" class="actor" style="left:60px;top:{220 + i * 120}px;width:1000px;height:96px;border-radius:16px;background:#22262E;'
             f'border:2px solid #3A3F48;display:flex;align-items:center;gap:28px;padding:0 28px;opacity:0">'
             f'<div style="width:56px;height:56px;border-radius:50%;background:{AMBER};color:#111;font-size:32px;font-weight:900;display:flex;align-items:center;justify-content:center">{k}</div>'
             f'<div style="font-size:40px;font-weight:700">{v}</div></div>' for i, (k, v) in enumerate(opts))
T3 = dict(kurze=W("Kurze", a), wann=W("Wann", a), A=W("A:", a), B=W("B:", a), C=W("C:", a), merk=W("Merk", a), ende=W("Ende", a))
put("c3", S, f"""
  <div id="c3-cam" class="lay">
    {light("c3-l", 960, 500, 760, "rgba(255,226,180,.14)")}
    <div id="c3-card" class="actor card" style="left:400px;top:190px;width:1120px;height:620px;opacity:0">
      <div class="t" style="left:60px;top:50px;font-size:28px;font-weight:800;letter-spacing:.4em;color:{AMBER}">UMFRAGE</div>
      {q_html}{oh}</div>
    <div id="c3-m" class="t cond" style="left:0;right:0;top:330px;text-align:center;font-size:120px;opacity:0">MERK DIR<br>DEINE ANTWORT</div>
    <svg id="c3-ring" class="actor" style="left:880px;top:610px;opacity:0" width="160" height="160" viewBox="0 0 160 160">
      <circle cx="80" cy="80" r="66" fill="none" stroke="#2A2E36" stroke-width="10"/>
      <circle id="c3-arc" cx="80" cy="80" r="66" fill="none" stroke="{AMBER}" stroke-width="10" stroke-dasharray="415" stroke-dashoffset="0" transform="rotate(-90 80 80)"/></svg>
    <div id="c3-n" class="t cond" style="left:880px;width:160px;top:648px;text-align:center;font-size:80px;opacity:0">3</div>
    <div id="c3-e" class="t" style="left:0;right:0;top:820px;text-align:center;font-size:30px;font-weight:800;letter-spacing:.3em;color:{MUTED};opacity:0">AUFLÖSUNG AM ENDE ↓</div>
    {cursor("c3", 1500, 900)}
  </div>""", f'type("#c3-qq", {nq}, T.wann, 0.025);' + r"""
  fadeIn("#c3-cam", 0, 0.3);
  tl.fromTo("#c3-card", { opacity: 0, y: 80, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power4.out" }, T.kurze - 0.1);
  fadeIn("#c3-cur", T.A - 0.6, 0.2);
  [T.A, T.B, T.C].forEach((t, i) => {
    tl.fromTo(`#c3-o${i}`, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.45, ease: "back.out(1.6)" }, t);
    move("#c3-cur", -520, -442 + i * 120, t - 0.25, 0.4);
    tl.to(`#c3-o${i}`, { borderColor: "#E8C27A", backgroundColor: "#2C2A24", duration: 0.2 }, t + 0.15);
    if (i < 2) tl.to(`#c3-o${i}`, { borderColor: "#3A3F48", backgroundColor: "#22262E", duration: 0.2 }, [T.B, T.C][i] - 0.1);
  });
  fadeOut("#c3-cur", T.merk - 0.3, 0.2);
  tl.to("#c3-card", { opacity: 0.12, scale: 0.97, duration: 0.5, ease: "power2.inOut" }, T.merk - 0.2);
  tl.fromTo("#c3-m", { opacity: 0, scale: 1.15 }, { opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }, T.merk);
  fadeIn("#c3-ring", T.merk + 0.3, 0.3); fadeIn("#c3-n", T.merk + 0.3, 0.3);
  tl.fromTo("#c3-arc", { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": 415 }, duration: 2.4, ease: "none" }, T.merk + 0.3);
  tl.set("#c3-n", { textContent: "2" }, T.merk + 1.1); tl.set("#c3-n", { textContent: "1" }, T.merk + 1.9);
  fadeIn("#c3-e", T.ende - 0.8, 0.5);
  fadeOut("#c3-cam", T.end - 0.3, 0.3);
""", T3)
SFX += [(T3["kurze"] - 0.1, "whoosh", 0.3)] + [(T3[k], "pop", 0.55) for k in ("A", "B", "C")] + [(T3["merk"], "boom", 0.25)]

# ================================================================ c4 Titelkarte: Buchstaben fallen, Lichtschwenk
title = "DAS DEADLINE-GENIE"
letters = "".join(f'<span id="c4-c{i}" style="display:inline-block;opacity:0">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(title))
a4, e4 = SEG["title"]
put("c4", "title", f"""
  <div id="c4-sweep" class="light" style="left:-700px;top:-200px;width:700px;height:1480px;opacity:.0;background:linear-gradient(90deg,transparent,rgba(255,236,205,.16),transparent);transform:rotate(12deg)"></div>
  <div id="c4-k" class="t" style="left:0;right:0;top:380px;text-align:center;font-size:40px;font-weight:800;letter-spacing:.8em;color:{AMBER};opacity:0">OTTO</div>
  <div class="t cond" style="left:0;right:0;top:450px;text-align:center;font-size:150px;letter-spacing:.06em;">{letters}</div>
  <div id="c4-line" class="actor" style="left:560px;top:640px;width:800px;height:3px;background:#FFF;transform-origin:50% 50%"></div>""", r"""
  fadeIn("#c4-k", 0.05, 0.4);
  for (let i = 0; i < 18; i++) tl.fromTo(`#c4-c${i}`, { opacity: 0, y: -90, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }, 0.25 + i * 0.03);
  tl.fromTo("#c4-line", { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.out" }, 0.7);
  tl.fromTo("#c4-sweep", { x: 0, opacity: 1 }, { x: 2800, opacity: 1, duration: 1.6, ease: "power2.inOut" }, 0.4);
  tl.to(["#c4-k", "#c4-line"], { opacity: 0, duration: 0.3 }, T.end - 0.35);
  for (let i = 0; i < 18; i++) tl.to(`#c4-c${i}`, { opacity: 0, y: 40, duration: 0.25, ease: "power2.in" }, T.end - 0.4 + i * 0.008);
""", {})
SFX += [(a4 + 0.05, "whoosh", 0.6), (a4 + 0.3, "boom", 0.7)]

# ================================================================ c5 Kapitel 1
a5, e5 = SEG["kap1"]
put("c5", "kap1", f"""
  <div id="c5-k" class="t" style="left:0;right:0;top:400px;text-align:center;font-size:30px;font-weight:700;letter-spacing:.6em;color:{MUTED};opacity:0">KAPITEL 1</div>
  <div id="c5-t" class="t cond" style="left:0;right:0;top:460px;text-align:center;font-size:130px;letter-spacing:.1em;opacity:0">DAS GESETZ DER ZEIT</div>
  <div id="c5-l1" class="actor" style="left:260px;top:640px;width:1400px;height:2px;background:{AMBER};transform-origin:0 50%"></div>""", r"""
  tl.fromTo("#c5-k", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }, 0.05);
  tl.fromTo("#c5-t", { opacity: 0, x: -120, filter: "blur(12px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.5, ease: "power4.out" }, 0.2);
  tl.fromTo("#c5-l1", { scaleX: 0 }, { scaleX: 1, duration: 0.8, ease: "power3.inOut" }, 0.3);
  tl.to(["#c5-k", "#c5-t", "#c5-l1"], { opacity: 0, duration: 0.35, ease: "power2.in" }, T.end - 0.4);
""", {})
SFX += [(a5 + 0.05, "whoosh", 0.6), (a5 + 0.25, "boom", 0.7)]

# ================================================================ c6 Parkinson: Zeitung + kinetisches Zitat
S = "v_park"; a = SEG[S][0]
st6, n6 = typed("c6-st", "NOVEMBER 1955 · ZEITSCHRIFTEN-ESSAY", "left:130px;top:178px;")
paper = (f'<div id="c6-paper" class="actor" style="left:880px;top:250px;width:800px;height:580px;background:{PAPER};color:#222;padding:40px 54px;'
         f'box-shadow:0 40px 90px rgba(0,0,0,.7);font-family:\'EB Garamond\';opacity:0">'
         f'<div style="border-bottom:3px double #333;padding-bottom:10px;font-size:30px;letter-spacing:.3em;text-align:center">ESSAY · 1955</div>'
         f'<div style="margin-top:30px;font-size:84px;font-weight:700;text-align:center;line-height:1">Parkinson\'s Law</div>'
         f'<div style="margin-top:34px;columns:2;column-gap:40px;font-size:22px;line-height:1.5;color:#555">'
         + "".join('<div style="height:14px;margin:9px 0;background:#BDB6A6;width:%d%%"></div>' % w for w in [100, 94, 98, 88, 100, 76, 96, 99, 90, 100, 85, 97, 93, 70]) +
         '</div></div>')
qw = [("ARBEIT", "arbeit"), ("DEHNT SICH", "dehnt"), ("GENAU SO WEIT AUS,", "genau"), ("WIE ZEIT", "wie"), ("FÜR SIE", "für"), ("ZUR VERFÜGUNG STEHT.", "zur")]
qh = ('<div id="c6-q" class="t cond" style="left:0;right:0;top:270px;text-align:center;font-size:96px;line-height:1.15;">'
      + "".join(f'<span id="c6-w{i}" style="display:inline-block;margin:0 14px;opacity:0{";color:" + AMBER if i == 1 else ""}">{t}</span>' + ("<br>" if i in (0, 1, 3) else "") for i, (t, _) in enumerate(qw)) + "</div>")
T6 = dict(cyril=W("Cyril", a), satz=W("Satz,", a), arbeit=W("Arbeit", a), dehnt=W("dehnt", a), sich=W("sich", a), genau=W("genau", a),
          wie=W("wie", a), fuer=W("für", W("Zeit", a)), zur=W("zur", a))
put("c6", S, f"""
  <div id="c6-cam" class="lay">
    {light("c6-l", 960, 500, 700, "rgba(255,226,180,.2)")}
    {paper}
    <div id="c6-lt" class="t" style="left:130px;top:660px;opacity:0">
      <div id="c6-ltl" style="width:440px;height:3px;background:#FFF;transform-origin:0 50%"></div>
      <div class="cond" style="margin-top:16px;font-size:64px;letter-spacing:.1em;">C. NORTHCOTE PARKINSON</div>
      <div style="margin-top:10px;font-size:28px;letter-spacing:.24em;color:{MUTED};font-weight:600;">BRITISCHER HISTORIKER</div></div>
    {qh}
  </div>{st6}""", f'type("#c6-st", {n6}, 0.3, 0.025);' + r"""
  fadeIn("#c6-cam", 0, 0.3);
  tl.fromTo("#c6-paper", { opacity: 0, rotation: -14, scale: 0.6, y: 120 }, { opacity: 1, rotation: -3, scale: 1, y: 0, duration: 0.9, ease: "power4.out" }, 0.6);
  tl.to("#c6-paper", { rotation: 1, y: -10, duration: T.arbeit - 1.5, ease: "none" }, 1.5);
  fadeIn("#c6-lt", T.cyril, 0.5); tl.fromTo("#c6-ltl", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.out" }, T.cyril);
  fadeOut("#c6-lt", T.arbeit - 0.6, 0.3);
  tl.to("#c6-paper", { scale: 1.6, opacity: 0, filter: "blur(10px)", duration: 0.5, ease: "power3.in" }, T.arbeit - 0.5);
  fadeOut("#c6-st", T.arbeit - 0.5, 0.3);
  const k = [T.arbeit, T.dehnt, T.genau, T.wie, T.fuer, T.zur];
  k.forEach((t, i) => tl.fromTo(`#c6-w${i}`, { opacity: 0, y: 40, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.3, ease: "power3.out" }, t - 0.05));
  tl.fromTo("#c6-w1", { scaleX: 1 }, { scaleX: 1.35, duration: 0.9, ease: "elastic.out(1, 0.5)", transformOrigin: "50% 50%", immediateRender: false }, T.sich);
  fadeOut("#c6-cam", T.end - 0.35, 0.35);
""", T6)
SFX += [(a + 0.6, "whoosh", 0.4), (T6["cyril"], "click", 0.8)]

# ================================================================ c7 Zeit-Kasten mit Arbeits-Blob
S = "v_box"; a = SEG[S][0]
T7 = dict(wochen=W("Wochen", a), braucht=W("braucht", a), stunden=W("Stunden,", a), braucht2=W("braucht", W("Stunden,", a)))
put("c7", S, f"""
  <div id="c7-cam" class="lay">
    {light("c7-l", 960, 480, 760, "rgba(255,226,180,.14)")}
    <div id="c7-box" class="actor" style="left:360px;top:300px;width:1200px;height:300px;border:4px dashed #CFC9BC;border-radius:24px;transform-origin:0 50%;opacity:0"></div>
    <div id="c7-lab" class="t" style="left:360px;top:250px;font-size:30px;font-weight:800;letter-spacing:.3em;color:{MUTED};opacity:0">ZEIT</div>
    <div id="c7-w" class="t cond" style="left:360px;width:1200px;top:630px;text-align:center;font-size:84px;color:{AMBER};opacity:0">3 WOCHEN</div>
    <div id="c7-s" class="t cond" style="left:360px;width:300px;top:630px;text-align:center;font-size:84px;color:{RED};opacity:0">3 STD</div>
    <div id="c7-blob" class="actor" style="left:380px;top:320px;width:1160px;height:260px;border-radius:120px;background:{ORANGE};transform-origin:0 50%;
         display:flex;align-items:center;justify-content:center;font-family:'Oswald';font-weight:700;font-size:80px;color:#1E1E1E;opacity:0">ARBEIT</div>
    <div style="position:absolute;left:1560px;top:520px;width:320px;height:400px;overflow:hidden">
      <div style="position:absolute;left:0;top:0;width:600px;height:760px;transform:scale(.5);transform-origin:0 0">{otto_svg("c7o", ("tired", "shock"))}</div></div>
  </div>""", r"""
  fadeIn("#c7-cam", 0, 0.3);
  fadeIn("#c7-lab", 0.1, 0.4);
  tl.fromTo("#c7-box", { opacity: 0, scaleX: 0.2 }, { opacity: 1, scaleX: 1, duration: 0.8, ease: "power3.out" }, T.wochen - 0.4);
  fadeIn("#c7-w", T.wochen, 0.4);
  tl.fromTo("#c7-blob", { opacity: 0, scaleX: 0.08, scaleY: 0.5 }, { opacity: 1, scaleX: 1, scaleY: 1, duration: 1.0, ease: "elastic.out(1, 0.55)" }, T.braucht);
  fadeOut("#c7-w", T.stunden - 0.3, 0.2);
  tl.to("#c7-box", { scaleX: 0.25, duration: 0.6, ease: "power3.inOut" }, T.stunden);
  fadeIn("#c7-s", T.stunden + 0.4, 0.3);
  face("c7o", "tired", "shock", T.stunden + 0.2);
  tl.to("#c7-blob", { keyframes: [{ scaleX: 0.3, scaleY: 1.25, duration: 0.35, ease: "power3.in" }, { scaleX: 0.238, scaleY: 1, duration: 0.6, ease: "elastic.out(1, 0.45)" }] }, T.stunden + 0.05);
  tl.to("#c7-blob", { keyframes: [{ scaleY: 1.12, duration: 0.15 }, { scaleY: 1, duration: 0.4, ease: "elastic.out(1, 0.4)" }] }, T.braucht2);
  fadeOut("#c7-cam", T.end - 0.4, 0.4);
""", T7)
SFX += [(T7["braucht"], "whoosh", 0.3), (T7["stunden"], "whoosh", 0.45)]

# ================================================================ Kapitel 1 (Rest) bis Abspann
exec(open(f"{HERE}/part2.py", encoding="utf-8").read())

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
with open(f"{HERE}/untertitel_video02.srt", "w", encoding="utf-8") as f:
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
json.dump([{"t": round(t, 3), "f": f, "g": g} for t, f, g in SFX if g > 0], open(f"{HERE}/assets/sfx.json", "w"), indent=0)
for fn in ("hyperframes.json", "package.json", "meta.json"):
    open(f"{HERE}/{fn}", "w").write(open(os.path.join(ROOT, "video01-doku", fn)).read().replace("otto-video01-doku", "otto-video02"))
print(f"Video 02: {END}s, {len(HOSTS)} Szenen, {len(groups)} Untertitel, {len([s for s in SFX if s[2] > 0])} Soundeffekte")
