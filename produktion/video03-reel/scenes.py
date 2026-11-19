# Wird von gen.py per exec() ausgeführt. Koordinaten vor der DY-Verschiebung: Grafik y 430–1030, x 150–930.
import math as _m

WATER = "#8EC5FF"
BULB = """<g stroke="#111" stroke-width="5"><path d="M-30,30 a60,60 0 1 1 60,0 l0,40 l-60,0 Z" fill="#FFD43B"/><rect x="-32" y="70" width="64" height="26" rx="6" fill="#9AA0A6"/></g>"""


def bulb(id_, cx, cy, s=1.0):
    return (light(f"{id_}-g", cx, cy, 200 * s, "rgba(255,220,120,.6)", 0)
            + f'<div id="{id_}" class="actor" style="left:{cx - 100 * s:.0f}px;top:{cy - 110 * s:.0f}px;width:{200 * s:.0f}px;height:{230 * s:.0f}px;opacity:0">'
            f'<svg viewBox="-100 -110 200 230" width="{200 * s:.0f}" height="{230 * s:.0f}">{BULB}</svg></div>')


def foam(hx, hy, s):
    blobs = [(-130, -130, 100), (-60, -170, 120), (30, -175, 120), (120, -145, 100), (170, -95, 70), (-155, -80, 70), (110, -75, 60), (-20, -120, 90)]
    return "".join(f'<div class="actor" style="left:{hx + dx * s:.0f}px;top:{hy + dy * s:.0f}px;width:{r * s:.0f}px;height:{r * s:.0f}px;border-radius:50%;'
                   f'background:radial-gradient(circle at 35% 30%,#FFF,#E3E9F1);border:3px solid #B9C3D0"></div>' for dx, dy, r in blobs)


def shower(id_, cx, top, s):
    streams = "".join(f'<div class="actor" style="left:{cx - 130 * s + i * 22 * s:.0f}px;top:{top + 40 * s:.0f}px;width:4px;height:{560 * s:.0f}px;'
                      f'background:repeating-linear-gradient(180deg,rgba(142,197,255,0) 0 18px,rgba(142,197,255,.55) 18px 54px)"></div>' for i in range(13))
    return (f'<div class="actor" style="left:{cx - 150 * s:.0f}px;top:{top}px;width:{300 * s:.0f}px;height:{36 * s:.0f}px;border-radius:18px;background:#9AA0AA"></div>'
            f'<div id="{id_}-w" class="lay">{streams}</div>')


def chip(id_, x, y, text, bg="#22262E", col="#FFF", size=40, border="#3A3F48", extra=""):
    return (f'<div id="{id_}" class="actor" style="left:{x}px;top:{y}px;padding:14px 26px;border-radius:18px;background:{bg};border:2px solid {border};'
            f'font-size:{size}px;font-weight:800;color:{col};white-space:nowrap;opacity:0;{extra}">{text}</div>')


# ================================================================ H0 Hook: Schreibtisch (nichts) → Dusche (Idee)
a, e = 0, SEG["r_hook"][1]
T = dict(nichts=W("nichts."), fuenf=W("Fünf"), dusche=W("Dusche:"), perfekte=W("perfekte"), idee=W("Idee."))
OX, OT, OS = 360, 560, 0.6
HX, HY = OX + 300 * OS, OT + 200 * OS
scene("h0", a, e, f"""
  <div id="h0-cam" class="lay">
    <div id="h0-desk" class="lay">
      {ctext("h0-lab", 450, "2 STUNDEN AM SCHREIBTISCH", 52, color=AMBER, extra="opacity:1")}
      <div id="h0-doc" class="actor card" style="left:190px;top:540px;width:700px;height:380px">
        <div style="height:60px;border-bottom:2px solid #3A3F48;display:flex;align-items:center;gap:14px;padding:0 22px">
          <span style="width:16px;height:16px;border-radius:50%;background:#FF5F57"></span><span style="width:16px;height:16px;border-radius:50%;background:#FEBC2E"></span>
          <span style="width:16px;height:16px;border-radius:50%;background:#28C840"></span><span style="margin-left:10px;font-size:28px;font-weight:700;color:{MUTED}">Ideen.docx</span></div>
        <div style="position:absolute;left:40px;top:90px;width:620px;height:250px;background:#F4F5F7;border-radius:6px"></div>
        <div id="h0-cur" class="actor" style="left:66px;top:110px;width:5px;height:46px;background:#111"></div>
        <div id="h0-clk" class="actor" style="right:-30px;top:-40px;padding:6px 18px;background:#111;border:3px solid #333;border-radius:12px;font-family:'Space Mono';font-weight:700;font-size:48px;color:#FF5A4A">14:00</div></div>
      {ctext("h0-n", 830, "NICHTS.", 190, color=RED, extra="text-shadow:0 0 40px rgba(255,60,40,.5)")}
    </div>
    <div id="h0-sh" class="lay" style="opacity:0">
      {shower("h0", 540, 515, 1.0)}
      {otto("h0", OX, OT, OS, ("tired", "aha"))}
      <div id="h0-foam" class="lay" style="opacity:0">{foam(HX, HY, OS)}</div>
      {bulb("h0-b", 790, 560, 0.75)}
      {ctext("h0-s", 450, "5 MINUTEN DUSCHE", 52, color=WATER)}
    </div>
  </div>""", r"""
  for (let k = 1; k <= 12; k++) { const mm = k * 10; tl.set("#h0-clk", { textContent: `${14 + Math.floor(mm / 60)}:${String(mm % 60).padStart(2, "0")}` }, 0.1 + k * 0.08); }
  tl.fromTo("#h0-cur", { opacity: 1 }, { opacity: 0, duration: 0.01, repeat: 5, yoyo: true, repeatDelay: 0.22, immediateRender: false }, 0.2);
  tl.to("#h0-doc", { opacity: 0.3, duration: 0.2 }, T.nichts - 0.1);
  slam("#h0-n", T.nichts, 2.4);
  shake("#h0-cam", T.nichts + 0.22, 12);
  tl.to("#h0-desk", { x: -200, opacity: 0, duration: 0.3, ease: "power3.in" }, T.fuenf - 0.2);
  tl.fromTo("#h0-sh", { opacity: 0, x: 200 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, T.fuenf - 0.05);
  tl.fromTo("#h0-otto", { opacity: 0 }, { opacity: 1, duration: 0.01 }, T.fuenf - 0.05);
  fadeIn("#h0-s", T.fuenf, 0.2);
  tl.fromTo("#h0-w", { y: -54 }, { y: 0, duration: 0.4, ease: "none", repeat: 8, immediateRender: false }, T.fuenf);
  tl.fromTo("#h0-foam", { opacity: 0, scale: 0.6, transformOrigin: "50% 30%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, T.dusche);
  face("h0o", "tired", "aha", T.perfekte);
  tl.fromTo("#h0-b", { opacity: 0, scale: 0.3, y: 40 }, { opacity: 1, scale: 1, y: 0, duration: 0.35, ease: "back.out(2.5)" }, T.perfekte);
  tl.fromTo("#h0-b-g", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T.perfekte + 0.1);
  tl.to("#h0-cam", { opacity: 0, scale: 1.06, duration: 0.2, ease: "power2.in" }, T.end - 0.2);
""", T)
SFX += [(0.1, "tick", 0.3), (T["nichts"] + 0.2, "boom", 0.6), (T["fuenf"] - 0.2, "click", 0.5), (T["dusche"], "pop", 0.4), (T["perfekte"], "ding", 0.7)]

# ================================================================ H1 Versprechen: WARUM? → 1 MINUTE → LOS!
a, e = SEG["r_promise"][0], SEG["go"][1]
T = dict(warum=W("Warum?"), erklaer=W("erklär"), einer=W("einer"), minute=W("Minute."), los=W("Los!"))
ring = (f'<svg viewBox="-200 -200 400 400" width="400" height="400"><circle r="170" fill="#111" stroke="#3A3F48" stroke-width="18"/>'
        f'<circle id="h1-arc" r="170" fill="none" stroke="{AMBER}" stroke-width="18" stroke-linecap="round" stroke-dasharray="1068" stroke-dashoffset="1068" transform="rotate(-90)"/>'
        f'<rect x="-26" y="-226" width="52" height="34" rx="8" fill="#3A3F48"/></svg>')
scene("h1", a, e, f"""
  <div id="h1-cam" class="lay">
    {ctext("h1-w", 560, 'WARUM?', 250, color=AMBER, extra="text-shadow:0 0 50px rgba(232,194,122,.5)")}
    {ctext("h1-e", 830, '🚿 = 💡', 110, cls="")}
    {ctext("h1-k", 470, "ERKLÄRT IN", 56, color=MUTED, extra="letter-spacing:.2em")}
    <div id="h1-ring" class="actor" style="left:340px;top:540px;width:400px;height:400px;opacity:0">{ring}
      <div class="t mono" style="left:0;width:400px;top:140px;text-align:center;font-size:110px;color:#FFF">1:00</div></div>
    {ctext("h1-m", 960, "1 MINUTE", 120, color=AMBER)}
    {ctext("h1-los", 660, "LOS!", 210, color=GREEN, extra="text-shadow:0 0 60px rgba(91,227,125,.6)")}
  </div>""", r"""
  slam("#h1-w", T.warum - 0.05, 2.4);
  shake("#h1-cam", T.warum + 0.2, 10);
  popIn("#h1-e", T.warum + 0.35, 0.35, 0.4);
  outUp(["#h1-w", "#h1-e"], T.erklaer - 0.1, 0.25);
  tl.fromTo("#h1-k", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, T.erklaer + 0.1);
  popIn("#h1-ring", T.einer - 0.15, 0.35, 0.2);
  tl.fromTo("#h1-arc", { attr: { "stroke-dashoffset": 1068 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.6, ease: "power2.inOut" }, T.einer);
  slam("#h1-m", T.minute, 2.0);
  tl.to(["#h1-k", "#h1-m"], { opacity: 0, duration: 0.15 }, T.los - 0.1);
  tl.to("#h1-ring", { y: -360, scale: 0.25, opacity: 0, duration: 0.35, ease: "power3.in" }, T.los - 0.05);
  slam("#h1-los", T.los, 2.5);
  tl.to("#h1-los", { opacity: 0, scale: 1.4, duration: 0.25, ease: "power2.in" }, T.end - 0.25);
""", T)
SFX += [(T["warum"] + 0.2, "boom", 0.5), (T["warum"] + 0.35, "pop", 0.4), (T["erklaer"], "click", 0.4), (T["einer"] + 0.1, "boom", 0.6), (T["los"], "click", 0.7)]

# ================================================================ P1 Brett vorm Kopf: Rundlauf, Spur wird tiefer
a, e = SEG["go"][1], SEG["r_fix"][1]
T = dict(erstens=W("Erstens:"), wenn=W("Wenn"), wege=W("Wege"), fix=W("Fixierung."), kreis=W("Kreis"), erste=W("erste"), verk=W("verkrampfter"), spur=W("Spur."))
CX, CY, RX, RY = 540, 720, 320, 160
loop = [(CX + RX * _m.cos(2 * _m.pi * k / 40), CY + RY * _m.sin(2 * _m.pi * k / 40)) for k in range(41)]
laps = 6; lap = (e - T["wege"] - 0.4) / laps
kf = ", ".join(f'{{ x: {x - CX - RX:.1f}, y: {y - CY:.1f}, duration: {lap / 40:.3f} }}' for _ in range(laps) for x, y in loop[1:])
exits = "".join(f'<path d="M{CX + RX * _m.cos(t):.0f},{CY + RY * _m.sin(t):.0f} L{CX + (RX + 75) * _m.cos(t):.0f},{CY + (RY + 80) * _m.sin(t):.0f}" stroke="#5A606B" stroke-width="5" stroke-dasharray="12 10"/>'
                f'<text x="{CX + (RX + 92) * _m.cos(t):.0f}" y="{CY + (RY + 100) * _m.sin(t) + 14:.0f}" fill="#8C8F96" font-size="44" font-weight="800" text-anchor="middle" font-family="Inter">?</text>'
                for t in [_m.pi * 1.2, _m.pi * 1.8, _m.pi * 0.2, _m.pi * 0.8])
scene("p1", a, e, f"""
  <div id="p1-cam" class="lay">
    {tag("p1", 1, "DAS BRETT VORM KOPF")}
    <svg class="actor" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">
      <g id="p1-ex" opacity="0">{exits}</g>
      <ellipse id="p1-tr" cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="#3A3F48" stroke-width="10" opacity="0"/></svg>
    <div id="p1-dot" class="actor" style="left:{CX + RX - 26}px;top:{CY - 26}px;width:52px;height:52px;border-radius:50%;background:{ORANGE};border:5px solid #FFF;box-shadow:0 0 30px rgba(255,122,26,.8);opacity:0"></div>
    {ctext("p1-f", 690, "FIXIERUNG", 72, color="#FFF")}
    {ctext("p1-i", 540, "IDEE #1 … IDEE #1 … IDEE #1", 40, cls="", color=AMBER, extra="font-weight:900;letter-spacing:.04em")}
    {ctext("p1-s", 945, "JE VERKRAMPFTER,<br>DESTO TIEFER DIE SPUR", 56, color=AMBER, extra="line-height:1.05")}
  </div>""", f"""
  tagIn("#p1-tag", T.erstens);
  tl.fromTo("#p1-tr", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, T.wenn);
  popIn("#p1-dot", T.wege - 0.3, 0.3);
  tl.to("#p1-dot", {{ keyframes: [{kf}], ease: "none" }}, T.wege);
  tl.fromTo("#p1-tr", {{ attr: {{ "stroke-width": 10 }}, stroke: "#3A3F48" }}, {{ attr: {{ "stroke-width": 50 }}, stroke: "#8A5A2E", duration: {lap * laps:.2f}, ease: "none", immediateRender: false }}, T.wege);
  slam("#p1-f", T.fix, 1.8);
  tl.fromTo("#p1-ex", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, T.kreis - 0.3);
  popIn("#p1-i", T.erste, 0.3, 0.6);
  slam("#p1-s", T.verk, 1.6);
  tl.to("#p1-cam", {{ opacity: 0, duration: 0.15 }}, T.end - 0.15);
""", T)
SFX += [(T["erstens"], "click", 0.45), (T["fix"], "boom", 0.4), (T["erste"], "pop", 0.35), (T["verk"], "pop", 0.45)]

# ================================================================ P2 Autopilot: Dusche, Körper/Kopf, Gedanken wandern, Netzwerk → IDEE, kein Handy
a, e = SEG["r_auto"]
T = dict(zweitens=W("Zweitens:"), duschen=W("Duschen"), koerper=W("Körper"), kopf=W("Kopf", 31), gedanken=W("Gedanken", 32), gehirn=W("Gehirn", 34),
         dinge=W("Dinge,"), ideen=W("Ideen.", 39), dusche=W("Dusche", 40.5), handy=W("Handy.", 42))
OX2, OT2, OS2 = 380, 610, 0.53
bub = [("🏖️", 650, 540), ("🎵", 770, 630), ("🍕", 680, 750), ("✈️", 780, 860)]
bh = "".join(f'<div id="p2-b{i}" class="actor" style="left:{x}px;top:{y}px;width:100px;height:100px;border-radius:50%;background:rgba(255,255,255,.1);border:3px solid rgba(255,255,255,.35);'
             f'display:flex;align-items:center;justify-content:center;font-size:52px;opacity:0">{em}</div>' for i, (em, x, y) in enumerate(bub))
tags_ = [("🏖️ URLAUB", 170, 500), ("🎵 SONG", 700, 500), ("📊 PRÄSENTATION", 330, 940)]
th = "".join(chip(f"p2-t{i}", x, y, t, size=34) for i, (t, x, y) in enumerate(tags_))
ends = [(290, 560), (800, 560), (540, 940)]
lh = "".join(f'<path id="p2-l{i}" d="M{x},{y} L540,740" stroke="{AMBER}" stroke-width="6" fill="none" stroke-dasharray="700" stroke-dashoffset="700"/>' for i, (x, y) in enumerate(ends))
scene("p2", a, e, f"""
  <div id="p2-cam" class="lay">
    {tag("p2", 2, "DER AUTOPILOT")}
    <div id="p2-A" class="lay">
      {shower("p2", 540, 560, 0.9)}
      {otto("p2", OX2, OT2, OS2, ("tired", "happy"))}
      {foam(OX2 + 300 * OS2, OT2 + 200 * OS2, OS2).replace('class="actor"', 'class="actor p2-fo"')}
      {chip("p2-k1", 150, 990, "🧍 KÖRPER: BESCHÄFTIGT", "#183A24", GREEN, 32, "#2E6B42")}
      {chip("p2-k2", 150, 560, "🧠 KOPF: FREI", "#2C2A24", AMBER, 32, "#6B5A30")}
      {bh}
    </div>
    <div id="p2-B" class="lay" style="opacity:0">
      <svg class="actor" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">{lh}</svg>
      <div id="p2-br" class="actor" style="left:340px;top:600px;width:400px;height:300px">{svgbox(art.brain(0, 0, 0.9, "#6E4A5A"), "-200 -180 400 330", 400, 300)}</div>
      {th}
      {bulb("p2-bi", 540, 720, 0.8)}
      {ctext("p2-id", 840, "NEUE IDEE!", 80, color=AMBER)}
    </div>
    <div id="p2-C" class="lay" style="opacity:0">
      <div id="p2-ph" class="actor" style="left:420px;top:560px;width:240px;height:420px;border-radius:34px;background:#111;border:6px solid #444">
        <div style="margin:24px 16px;height:340px;border-radius:14px;background:linear-gradient(180deg,#3A5A8C,#8C3A5A)"></div></div>
      <div id="p2-x" class="t" style="left:0;width:1080px;top:600px;text-align:center;font-size:300px;line-height:1;color:{RED};opacity:0">✗</div>
      {ctext("p2-kh", 995, "LETZTER ORT OHNE HANDY", 52, color=WATER)}
    </div>
  </div>""", r"""
  tagIn("#p2-tag", T.zweitens);
  tl.fromTo("#p2-A", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T.zweitens + 0.6);
  tl.fromTo("#p2-otto", { opacity: 0 }, { opacity: 1, duration: 0.01 }, T.zweitens + 0.6);
  tl.fromTo("#p2-w", { y: -54 }, { y: 0, duration: 0.4, ease: "none", repeat: 16, immediateRender: false }, T.zweitens + 0.6);
  tl.fromTo("#p2-k1", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, T.koerper);
  tl.fromTo("#p2-k2", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, T.kopf);
  face("p2o", "tired", "happy", T.gedanken);
  for (let i = 0; i < 4; i++) { tl.fromTo(`#p2-b${i}`, { opacity: 0, scale: 0.2, y: 80 }, { opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(1.8)" }, T.gedanken + i * 0.18);
    tl.to(`#p2-b${i}`, { y: -20, duration: 0.8, yoyo: true, repeat: 1, ease: "sine.inOut" }, T.gedanken + 0.5 + i * 0.1); }
  outUp("#p2-A", T.gehirn - 0.2, 0.2);
  fadeIn("#p2-B", T.gehirn - 0.05, 0.15);
  tl.fromTo("#p2-br", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, T.gehirn - 0.05);
  for (let i = 0; i < 3; i++) { popIn(`#p2-t${i}`, T.dinge - 0.2 + i * 0.25, 0.3); tl.to(`#p2-l${i}`, { attr: { "stroke-dashoffset": 0 }, duration: 0.4, ease: "power2.inOut" }, T.dinge + 0.1 + i * 0.25); }
  tl.to("#p2-br", { opacity: 0.3, duration: 0.3 }, T.ideen - 0.3);
  tl.fromTo("#p2-bi", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }, T.ideen - 0.1);
  tl.fromTo("#p2-bi-g", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T.ideen);
  slam("#p2-id", T.ideen, 1.8);
  outUp("#p2-B", T.dusche - 0.2, 0.2);
  fadeIn("#p2-C", T.dusche - 0.05, 0.15);
  popIn("#p2-ph", T.dusche, 0.3, 0.6);
  fadeIn("#p2-kh", T.dusche + 0.2, 0.3);
  slam("#p2-x", T.handy - 0.1, 2.2);
  tl.to("#p2-cam", { opacity: 0, duration: 0.15 }, T.end - 0.15);
""", T)
SFX += [(T["zweitens"], "click", 0.45), (T["koerper"], "pop", 0.35), (T["kopf"], "pop", 0.35)] + [(T["gedanken"] + i * 0.18, "pop", 0.25) for i in range(0, 4, 2)] + \
       [(T["dinge"] - 0.2 + i * 0.25, "pop", 0.3) for i in range(3)] + [(T["ideen"] - 0.1, "ding", 0.65), (T["dusche"], "pop", 0.35), (T["handy"] - 0.1, "click", 0.6)]

# ================================================================ P3 Keine Ideen aus dem Nichts: Hut → NEIN → 3 Phasen
a, e = SEG["r_aber"]
T = dict(aber=W("Aber:"), nichts=W("Nichts.", 44), erst=W("Erst", 46), besch=W("beschäftigen."), dann=W("Dann", 48.5), los=W("loslassen.", 49), hinter=W("Hintergrund"), weiter=W("weiter.", 51.5))
steps = [("📚", "VORBEREITEN"), ("⏸", "LOSLASSEN"), ("⚙️", "GEHIRN ARBEITET WEITER")]
sh = "".join(f'<div id="p3-s{i}" class="actor card" style="left:190px;top:{540 + i * 150}px;width:700px;height:120px;display:flex;align-items:center;gap:26px;padding:0 30px;opacity:0">'
             f'<span style="font-size:64px">{em}</span><span class="cond" style="font-size:52px">{t}</span>'
             f'<span id="p3-c{i}" style="margin-left:auto;font-size:52px;color:{GREEN};opacity:0">✓</span></div>' for i, (em, t) in enumerate(steps))
scene("p3", a, e, f"""
  <div id="p3-cam" class="lay">
    {tag("p3", 3, "NICHT AUS DEM NICHTS")}
    <div id="p3-A" class="lay">
      <div id="p3-hat" class="actor" style="left:400px;top:560px;font-size:260px;line-height:1;opacity:0">🎩</div>
      {ctext("p3-q", 920, "IDEEN AUS DEM NICHTS?", 64)}
      <div id="p3-st" class="t cond" data-layout-allow-overlap style="left:240px;width:600px;top:620px;text-align:center;font-size:170px;color:{RED};border:12px solid {RED};border-radius:20px;transform:rotate(-9deg);opacity:0;background:rgba(11,12,14,.55)">NEIN.</div>
    </div>
    <div id="p3-B" class="lay">{sh}</div>
  </div>""", r"""
  tagIn("#p3-tag", T.aber);
  popIn("#p3-hat", T.aber + 0.1, 0.35);
  fadeIn("#p3-q", T.aber + 0.4, 0.3);
  slam("#p3-st", T.nichts, 2.4);
  shake("#p3-cam", T.nichts + 0.25, 12);
  outUp("#p3-A", T.erst - 0.2, 0.2);
  [T.besch, T.los, T.hinter].forEach((t, i) => { tl.fromTo(`#p3-s${i}`, { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }, t - 0.4); popIn(`#p3-c${i}`, t + 0.2, 0.25, 0.4); });
  tl.to("#p3-s2", { borderColor: "#E8C27A", duration: 0.3 }, T.weiter);
  tl.to("#p3-cam", { opacity: 0, duration: 0.15 }, T.end - 0.15);
""", T)
SFX += [(T["aber"], "click", 0.45), (T["nichts"] + 0.25, "boom", 0.5)] + [(t - 0.4, "pop", 0.35) for t in (T["besch"], T["los"], T["hinter"])] + [(t + 0.2, "click", 0.35) for t in (T["besch"], T["los"], T["hinter"])]

# ================================================================ P4 Der Trick: 5 Hacks als Checkliste → erst füttern, dann loslassen
a, e = SEG["r_trick"]
T = dict(der=W("Der", 52), zwanzig=W("Zwanzig"), pause=W("Pause,"), geh=W("Geh"), auf=W("Aufschreiben"), schlaf=W("Schlaf", 62), kurz=W("Kurz"),
         fuettern=W("füttern,"), loslassen=W("loslassen.", 65.5), idee=W("Idee", 66.5))
hk = [("⏱️", "20 MIN KONZENTRATION", "zwanzig"), ("📵", "LANGWEILIGE PAUSE", "pause"), ("🚶", "SPAZIEREN GEHEN", "geh"), ("📝", "AUFSCHREIBEN", "auf"), ("🌙", "DRÜBER SCHLAFEN", "schlaf")]
hh = "".join(f'<div id="p4-h{i}" class="actor card" style="left:170px;top:{515 + i * 102}px;width:740px;height:90px;display:flex;align-items:center;gap:22px;padding:0 26px;opacity:0">'
             f'<span style="width:50px;height:50px;border-radius:50%;background:{AMBER};color:#111;display:inline-flex;align-items:center;justify-content:center;font-size:30px;font-weight:900">{i + 1}</span>'
             f'<span style="font-size:44px">{em}</span><span style="font-size:38px;font-weight:900">{t}</span></div>' for i, (em, t, _) in enumerate(hk))
scene("p4", a, e, f"""
  <div id="p4-cam" class="lay">
    {tag("p4", 4, "DER TRICK")}
    <div id="p4-A" class="lay">{hh}</div>
    <div id="p4-B" class="lay">
      {ctext("p4-f", 560, "ERST FÜTTERN", 110, color="#FFF")}
      {ctext("p4-ar", 680, "↓", 90, cls="", color=MUTED)}
      {ctext("p4-l", 780, "DANN LOSLASSEN", 110, color=AMBER)}
      {bulb("p4-b", 540, 960, 0.6)}
    </div>
  </div>""", r"""
  tagIn("#p4-tag", T.der);
  [T.zwanzig, T.pause, T.geh, T.auf, T.schlaf].forEach((t, i) => tl.fromTo(`#p4-h${i}`, { opacity: 0, x: 120 }, { opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }, t - 0.25));
  outUp("#p4-A", T.kurz - 0.1, 0.25);
  slam("#p4-f", T.fuettern - 0.3, 1.4);
  fadeIn("#p4-ar", T.fuettern + 0.3, 0.2);
  slam("#p4-l", T.loslassen - 0.1, 1.4);
  tl.fromTo("#p4-b", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }, T.idee);
  tl.fromTo("#p4-b-g", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T.idee + 0.1);
  tl.to("#p4-cam", { opacity: 0, duration: 0.15 }, T.end - 0.15);
""", T)
SFX += [(T["der"], "click", 0.45)] + [(T[k] - 0.25, "pop", 0.4) for _, _, k in hk] + [(T["fuettern"] - 0.3, "pop", 0.45), (T["loslassen"] - 0.1, "pop", 0.45), (T["idee"], "ding", 0.6)]

# ================================================================ P5 Zeit um! → Ziegelstein-Challenge → ganze Folge, Sonntagabend, Link in der Bio
a, e = SEG["r_trick"][1], END
T = dict(zeit=T1, kleine=W("Kleine"), ziegel=W("Ziegelstein"), schreib=W("Schreib"), komm=W("Kommentare."), die=W("Die", 77), ganze=W("ganze", 77),
         sonntag=W("Mittwochabend"), youtube=W("YouTube."), link=W("Link"), bio=W("Bio."))
BRICK = (f'<div style="position:absolute;inset:0;border-radius:14px;background:linear-gradient(160deg,#C2593A,#8E3B26);box-shadow:inset 0 -14px 0 rgba(0,0,0,.25),0 30px 60px rgba(0,0,0,.6)"></div>'
         + "".join(f'<div style="position:absolute;left:{70 + i * 120}px;top:52px;width:56px;height:56px;border-radius:50%;background:#5A2316;box-shadow:inset 0 6px 10px rgba(0,0,0,.5)"></div>' for i in range(3)))
scene("p5", a, e, f"""
  <div id="p5-fl" class="actor" style="left:0;top:-400px;width:1080px;height:2700px;background:#FFF;opacity:0"></div>
  <div id="p5-cam" class="lay">
    {ctext("p5-zu", 620, "ZEIT UM!", 180, color=RED, extra="text-shadow:0 0 60px rgba(255,60,40,.7)")}
    <div id="p5-C" class="lay">
      {ctext("p5-ch", 450, "🧱 CHALLENGE", 60, color=AMBER)}
      <div id="p5-brick" class="actor" style="left:330px;top:600px;width:420px;height:160px;opacity:0">{BRICK}</div>
      {ctext("p5-q", 800, "WAS KANN MAN ALLES<br>DAMIT MACHEN?", 64, extra="line-height:1.05")}
      <div id="p5-cm" class="actor card" style="left:170px;top:960px;width:740px;height:96px;display:flex;align-items:center;gap:18px;padding:0 24px;opacity:0">
        <span style="font-size:44px">💬</span><span style="font-size:32px;font-weight:800;color:{MUTED}">Deine verrückteste Idee …</span></div>
    </div>
    <div id="p5-D" class="lay">
      {ctext("p5-k", 446, "DIE GANZE FOLGE", 56, cls="", color=AMBER, extra="font-weight:900;letter-spacing:.18em")}
      <div id="p5-card" class="actor" style="left:192px;top:540px;width:696px;height:391px;border-radius:22px;overflow:hidden;box-shadow:0 30px 90px rgba(0,0,0,.7), 0 0 0 4px #2A2D33;opacity:0">
        <img src="assets/thumb.png" style="width:696px;height:391px;display:block" />
        <div style="position:absolute;right:18px;bottom:18px;padding:4px 12px;border-radius:8px;background:rgba(0,0,0,.85);font-size:30px;font-weight:800">7:14</div>
        <div id="p5-play" style="position:absolute;left:288px;top:138px;width:120px;height:116px;opacity:0">
          <svg viewBox="0 0 120 116" width="120" height="116"><rect x="0" y="16" width="120" height="84" rx="24" fill="#FF0033"/><path d="M48,38 L82,58 L48,78 Z" fill="#FFF"/></svg></div></div>
      <div id="p5-so" class="actor" style="left:530px;top:570px;padding:10px 22px;border-radius:14px;background:{AMBER};color:#1A1A1A;font-size:36px;font-weight:900;letter-spacing:.04em;transform:rotate(6deg);box-shadow:0 12px 30px rgba(0,0,0,.5);opacity:0">MITTWOCHABEND</div>
      <div id="p5-yt" class="t" style="left:0;width:1080px;top:960px;text-align:center;opacity:0">
        <span style="display:inline-flex;align-items:center;gap:14px;padding:10px 26px;border-radius:40px;background:#FF0033;font-size:36px;font-weight:900">▶ YouTube · Otto Normalpsyche</span></div>
      <div id="p5-bio" class="t" style="left:0;width:1080px;top:960px;text-align:center;opacity:0">
        <span style="display:inline-flex;align-items:center;gap:14px;padding:10px 30px;border-radius:40px;background:#FFF;color:#1A1A1A;font-size:40px;font-weight:900">🔗 LINK IN DER BIO</span></div>
      {otto("p5", 70, 770, 0.36, ("happy",))}
    </div>
  </div>""", r"""
  tl.fromTo("#p5-fl", { opacity: 0.55 }, { opacity: 0, duration: 0.35, ease: "power2.out", immediateRender: false }, T.zeit);
  slam("#p5-zu", T.zeit, 2.8);
  shake("#p5-cam", T.zeit + 0.22, 8);
  tl.to("#p5-zu", { y: -260, scale: 0.4, opacity: 0, duration: 0.3, ease: "power3.in" }, T.kleine - 0.25);
  popIn("#p5-ch", T.kleine, 0.35, 0.5);
  tl.fromTo("#p5-brick", { opacity: 0, y: -120, rotation: -30 }, { opacity: 1, y: 0, rotation: -4, duration: 0.6, ease: "bounce.out" }, T.ziegel - 0.3);
  fadeIn("#p5-q", T.ziegel + 0.2, 0.3);
  tl.fromTo("#p5-cm", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, T.schreib);
  tl.fromTo("#p5-cm", { scale: 1.08 }, { scale: 1, duration: 0.3, ease: "back.out(3)", immediateRender: false }, T.komm);
  outUp("#p5-C", T.die - 0.2, 0.2);
  fadeIn("#p5-k", T.die, 0.3);
  tl.fromTo("#p5-card", { opacity: 0, y: 200, scale: 0.8, rotation: -4 }, { opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.5)" }, T.die);
  popIn("#p5-play", T.ganze + 0.3, 0.35, 0.3);
  tl.fromTo("#p5-otto", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.8)" }, T.ganze + 0.5);
  tl.fromTo("#p5-so", { opacity: 0, scale: 2.2, rotation: 20 }, { opacity: 1, scale: 1, rotation: 6, duration: 0.3, ease: "back.out(2)" }, T.sonntag);
  popIn("#p5-yt", T.youtube - 0.1, 0.35, 0.5);
  tl.to("#p5-yt", { opacity: 0, y: 30, duration: 0.2, ease: "power2.in" }, T.link - 0.15);
  popIn("#p5-bio", T.link, 0.35, 0.5);
  tl.fromTo("#p5-bio", { scale: 1.12 }, { scale: 1, duration: 0.4, ease: "back.out(3)", immediateRender: false }, T.bio);
  for (let i = 0; i < 3; i++) tl.fromTo("#p5-play", { scale: 1.15 }, { scale: 1, duration: 0.5, ease: "power2.out", immediateRender: false }, T.bio + 0.5 + i * 0.8);
""", T)
SFX += [(T["zeit"], "ding", 0.75), (T["kleine"], "pop", 0.4), (T["ziegel"] + 0.1, "drop", 0.4), (T["schreib"], "pop", 0.35), (T["komm"], "click", 0.5),
        (T["die"], "click", 0.45), (T["ganze"] + 0.3, "pop", 0.4), (T["sonntag"], "pop", 0.45), (T["youtube"] - 0.1, "click", 0.6), (T["link"], "pop", 0.45), (T["bio"], "click", 0.5)]
