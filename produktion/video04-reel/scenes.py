# Wird von gen.py per exec() ausgeführt. Koordinaten vor der DY-Verschiebung: Grafik y 430–1030, x 150–930 (Richtlinie: nichts über den Rand).
import math as _m

BULB = """<g stroke="#111" stroke-width="5"><path d="M-30,30 a60,60 0 1 1 60,0 l0,40 l-60,0 Z" fill="#FFD43B"/><rect x="-32" y="70" width="64" height="26" rx="6" fill="#9AA0A6"/></g>"""


def chip(id_, x, y, text, bg="#22262E", col="#FFF", size=40, border="#3A3F48", extra=""):
    return (f'<div id="{id_}" class="actor" style="left:{x}px;top:{y}px;padding:14px 26px;border-radius:18px;background:{bg};border:2px solid {border};'
            f'font-size:{size}px;font-weight:800;color:{col};white-space:nowrap;opacity:0;{extra}">{text}</div>')


def cchip(id_, y, text, bg="#22262E", col="#FFF", size=40, border="#3A3F48"):
    return (f'<div id="{id_}" class="t" style="left:0;width:1080px;top:{y}px;text-align:center;opacity:0"><span style="display:inline-block;padding:14px 26px;border-radius:18px;'
            f'background:{bg};border:2px solid {border};font-size:{size}px;font-weight:800;color:{col}">{text}</span></div>')


def phone(id_, x, y, w, h, screen=""):
    return (f'<div id="{id_}" class="actor" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{w * 0.14:.0f}px;background:#111;border:6px solid #444;opacity:0">'
            f'<div style="position:absolute;left:{w * 0.06:.0f}px;top:{h * 0.05:.0f}px;right:{w * 0.06:.0f}px;bottom:{h * 0.05:.0f}px;border-radius:{w * 0.06:.0f}px;'
            f'background:linear-gradient(180deg,#1E2A44,#141824);overflow:hidden">{screen}</div></div>')


# ================================================================ H0 Hook: kein Anruf, keine Nachricht – Hand greift trotzdem
a, e = 0, SEG["r_hook"][1]
T = dict(anruf=W("Anruf."), nachricht=W("Nachricht.", 1), trotzdem=W("trotzdem"), hand=W("Hand?"))
scene("h0", a, e, f"""
  <div id="h0-cam" class="lay">
    {cchip("h0-a", 450, "📞 KEIN ANRUF", size=44)}
    {cchip("h0-n", 540, "💬 KEINE NACHRICHT", size=44)}
    <div id="h0-ph" class="actor" style="left:410px;top:640px;width:260px;height:380px;border-radius:36px;background:#111;border:6px solid #444">
      <div style="position:absolute;left:16px;top:20px;right:16px;bottom:20px;border-radius:16px;background:#2A3E66;display:flex;align-items:center;justify-content:center;text-align:center;font-size:30px;font-weight:800">0 neue<br>Nachrichten</div></div>
    <div id="h0-hand" data-layout-allow-overlap class="actor" style="left:700px;top:780px;font-size:150px;line-height:1;opacity:0">🤚</div>
    {ctext("h0-s", 455, "SCHON WIEDER?!", 120, color=AMBER, extra="text-shadow:0 0 40px rgba(0,0,0,.8)")}
  </div>""", r"""
  tl.fromTo("#h0-ph", { scale: 1.08 }, { scale: 1, duration: 0.5, ease: "back.out(2)", immediateRender: false }, 0.05);
  popIn("#h0-a", T.anruf - 0.15, 0.3, 0.5);
  popIn("#h0-n", T.nachricht - 0.15, 0.3, 0.5);
  tl.fromTo("#h0-hand", { opacity: 0, x: 120 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, T.trotzdem - 0.2);
  tl.to("#h0-hand", { x: -170, y: -30, duration: 0.35, ease: "power2.in" }, T.trotzdem + 0.5);
  tl.to("#h0-ph", { rotation: -10, y: -20, duration: 0.3, ease: "power2.out" }, T.trotzdem + 0.8);
  tl.to(["#h0-a", "#h0-n"], { opacity: 0, duration: 0.15 }, T.trotzdem + 0.85);
  slam("#h0-s", T.trotzdem + 1.0, 2.2);
  tl.to("#h0-cam", { opacity: 0, scale: 1.06, duration: 0.2, ease: "power2.in" }, T.end - 0.2);
""", T)
SFX += [(T["anruf"] - 0.15, "pop", 0.35), (T["nachricht"] - 0.15, "pop", 0.35), (T["trotzdem"] + 0.8, "click", 0.6), (T["trotzdem"] + 1.2, "boom", 0.45)]

# ================================================================ H1 Versprechen: WARUM? → 1 MINUTE → LOS!
a, e = SEG["r_promise"][0], SEG["go"][1]
T = dict(warum=W("Warum?"), erklaer=W("erklär"), einer=W("einer"), minute=W("Minute."), los=W("Los!"))
ring = (f'<svg viewBox="-200 -200 400 400" width="400" height="400"><circle r="170" fill="#111" stroke="#3A3F48" stroke-width="18"/>'
        f'<circle id="h1-arc" r="170" fill="none" stroke="{AMBER}" stroke-width="18" stroke-linecap="round" stroke-dasharray="1068" stroke-dashoffset="1068" transform="rotate(-90)"/>'
        f'<rect x="-26" y="-226" width="52" height="34" rx="8" fill="#3A3F48"/></svg>')
scene("h1", a, e, f"""
  <div id="h1-cam" class="lay">
    {ctext("h1-w", 560, 'WARUM?', 250, color=AMBER, extra="text-shadow:0 0 50px rgba(232,194,122,.5)")}
    {ctext("h1-e", 830, '📱 = 🧲', 110, cls="")}
    {ctext("h1-k", 470, "ERKLÄRT IN", 56, color=MUTED, extra="letter-spacing:.2em")}
    <div id="h1-ring" class="actor" style="left:340px;top:540px;width:400px;height:400px;opacity:0">{ring}
      <div class="t mono" style="left:0;width:400px;top:140px;text-align:center;font-size:110px;color:#FFF">1:00</div></div>
    {ctext("h1-m", 960, "1 MINUTE", 120, color=AMBER)}
    {ctext("h1-los", 660, "LOS!", 210, color=GREEN, extra="text-shadow:0 0 60px rgba(91,227,125,.6)")}
  </div>""", r"""
  slam("#h1-w", T.warum - 0.05, 2.4);
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
SFX += [(T["warum"] + 0.2, "boom", 0.45), (T["warum"] + 0.35, "pop", 0.4), (T["erklaer"], "click", 0.4), (T["einer"] + 0.1, "boom", 0.55), (T["los"], "click", 0.7)]

# ================================================================ P1 Der Griff: 0:47 · 50 % selbst · Gewohnheits-Schleife · ×1000
a, e = SEG["go"][1], SEG["r_griff"][1]
T = dict(erstens=W("Erstens:"), bild=W("Bildschirm"), sieben=W("siebenundvierzig"), haelfte=W("Hälfte"), selbst=W("selbst."), gewohnheit=W("Gewohnheit:"),
         lang=W("langweilig,"), griff=W("Griff,", 22), neues=W("Neues."), tausend=W("Tausendmal"), zaehne=W("Zähneputzen."))
LX, LY, LR = 540, 760, 190
nodes = [("😐", "LANGWEILIG", -90), ("📱", "GRIFF", 30), ("✨", "NEUES", 150)]
nh = "".join(f'<div id="p1-n{i}" class="actor card" style="left:{LX + LR * _m.cos(_m.radians(ang)) - 120:.0f}px;top:{LY + LR * _m.sin(_m.radians(ang)) - 60:.0f}px;width:240px;height:120px;'
             f'display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0"><div style="font-size:46px;line-height:1">{em}</div>'
             f'<div class="cond" style="font-size:36px;margin-top:4px">{lab}</div></div>' for i, (em, lab, ang) in enumerate(nodes))
ring = [(LX + LR * _m.cos(_m.radians(-90 + 360 * k / 30)), LY + LR * _m.sin(_m.radians(-90 + 360 * k / 30))) for k in range(31)]
laps = [1.4, 1.0, 0.7, 0.5, 0.4, 0.3, 0.3]
kf = ", ".join(f'{{ x: {x - ring[0][0]:.1f}, y: {y - ring[0][1]:.1f}, duration: {d / 30:.3f} }}' for d in laps for x, y in ring[1:])
scene("p1", a, e, f"""
  <div id="p1-cam" class="lay">
    {tag("p1", 1, "DER GRIFF")}
    <div id="p1-A" class="lay">
      {ctext("p1-l", 540, "Ø AUFMERKSAMKEIT AM BILDSCHIRM", 32, cls="", color=MUTED, extra="font-weight:800;letter-spacing:.03em")}
      <div id="p1-t" class="t mono" style="left:0;width:1080px;top:620px;text-align:center;font-size:200px;color:#FFF;opacity:0">2:30</div>
      {ctext("p1-s", 860, "SEKUNDEN PRO SACHE", 56, color=AMBER)}
    </div>
    <div id="p1-B" class="lay">
      {ctext("p1-h", 560, "50 %", 220, color=ORANGE)}
      {ctext("p1-hs", 800, "DER UNTERBRECHUNGEN:<br>VON UNS SELBST", 60, extra="line-height:1.1")}
    </div>
    <div id="p1-C" class="lay">
      <svg class="actor" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">
        <circle id="p1-rg" cx="{LX}" cy="{LY}" r="{LR}" fill="none" stroke="#3A3F48" stroke-width="8" opacity="0"/></svg>
      {nh}
      <div id="p1-dot" class="actor" style="left:{ring[0][0] - 20:.0f}px;top:{ring[0][1] - 20:.0f}px;width:40px;height:40px;border-radius:50%;background:{ORANGE};border:5px solid #FFF;opacity:0"></div>
      <div id="p1-cnt" class="t mono" style="left:0;width:1080px;top:730px;text-align:center;font-size:72px;color:{AMBER};opacity:0">×<span id="p1-n">1</span></div>
      {ctext("p1-au", 1000, "🪥 AUTOMATISCH", 60)}
    </div>
  </div>""", f"""
  tagIn("#p1-tag", T.erstens);
  fadeIn("#p1-l", T.bild - 0.2, 0.3);
  popIn("#p1-t", T.bild, 0.3, 0.6);
  for (let k = 0; k <= 10; k++) {{ const s = Math.round(150 - (150 - 47) * k / 10); tl.set("#p1-t", {{ textContent: `${{Math.floor(s / 60)}}:${{String(s % 60).padStart(2, "0")}}` }}, T.sieben - 0.6 + k * 0.07); }}
  tl.set("#p1-t", {{ color: "{RED}" }}, T.sieben + 0.15);
  fadeIn("#p1-s", T.sieben + 0.3, 0.3);
  outUp("#p1-A", T.haelfte - 0.4);
  slam("#p1-h", T.haelfte - 0.1, 2.0);
  fadeIn("#p1-hs", T.selbst - 0.6, 0.3);
  outUp("#p1-B", T.gewohnheit - 0.4);
  tl.fromTo("#p1-rg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, T.gewohnheit - 0.1);
  [T.lang, T.griff, T.neues].forEach((t, i) => popIn(`#p1-n${{i}}`, t - 0.2, 0.3));
  popIn("#p1-dot", T.neues + 0.2, 0.25);
  tl.to("#p1-dot", {{ keyframes: [{kf}], ease: "none" }}, T.neues + 0.4);
  tl.fromTo("#p1-rg", {{ attr: {{ "stroke-width": 8 }}, stroke: "#3A3F48" }}, {{ attr: {{ "stroke-width": 34 }}, stroke: "#8A5A2E", duration: {sum(laps):.2f}, ease: "power1.in", immediateRender: false }}, T.neues + 0.4);
  fadeIn("#p1-cnt", T.tausend - 0.2, 0.2);
  tl.fromTo("#p1-n", {{ textContent: 1 }}, {{ textContent: 1000, duration: 1.4, ease: "power2.in", snap: {{ textContent: 1 }} }}, T.tausend - 0.1);
  popIn("#p1-au", T.zaehne - 0.3, 0.35, 0.5);
  tl.to("#p1-cam", {{ opacity: 0, duration: 0.15 }}, T.end - 0.15);
""", T)
SFX += [(T["erstens"], "click", 0.45), (T["sieben"] + 0.15, "pop", 0.4), (T["haelfte"] + 0.1, "boom", 0.35)] + [(T[k] - 0.2, "pop", 0.35) for k in ("lang", "griff", "neues")] + \
       [(T["tausend"] - 0.1, "tick", 0.3), (T["zaehne"] - 0.3, "pop", 0.4)]

# ================================================================ P2 Spielautomat: Walzen, meistens nichts
a, e = SEG["r_automat"]
T = dict(zweitens=W("Zweitens:"), nachricht=W("Nachricht,", 30), like=W("Like,"), nichts=W("nichts.", 34), vorher=W("vorher."), unber=W("Unberechenbarkeit"), hose=W("Hosentasche"))
SYM = ["💬", "❤️", "🔕", "📸", "🔕", "👍", "🔕", "🎵", "🔕", "💬", "🔕", "❤️"]
reel = lambda i: (f'<div class="actor" style="left:{240 + i * 210}px;top:620px;width:180px;height:180px;border-radius:16px;background:#F4F6FA;overflow:hidden;border:4px solid #C9A64A">'
                  f'<div id="p2-s{i}" style="position:absolute;left:0;top:0;width:180px">' + "".join(f'<div style="height:180px;display:flex;align-items:center;justify-content:center;font-size:100px">{s}</div>' for s in SYM * 3) + '</div></div>')
scene("p2", a, e, f"""
  <div id="p2-cam" class="lay">
    {tag("p2", 2, "DER SPIELAUTOMAT")}
    <div id="p2-box" class="actor" style="left:190px;top:520px;width:700px;height:420px;border-radius:40px;background:linear-gradient(180deg,#3A2A1A,#221A12);border:6px solid #C9A64A;opacity:0">
      <div class="t cond" style="left:0;right:0;top:24px;text-align:center;font-size:56px;color:{AMBER}">🎰 JACKPOT?</div></div>
    {reel(0)}{reel(1)}{reel(2)}
    <div id="p2-res" class="t cond" style="left:0;width:1080px;top:830px;text-align:center;font-size:72px;opacity:0">—</div>
    {ctext("p2-u", 980, "UNBERECHENBAR = UNWIDERSTEHLICH", 50, color=AMBER)}
    {ctext("p2-h", 980, "📱 = 🎰 IN DER HOSENTASCHE", 52, color="#FFF")}
  </div>""", r"""
  tagIn("#p2-tag", T.zweitens);
  popIn("#p2-box", T.zweitens + 0.3, 0.4);
  const spin = (t, idx, label) => {
    for (let i = 0; i < 3; i++) tl.fromTo(`#p2-s${i}`, { y: 0 }, { y: -(12 + idx[i]) * 180, duration: 0.45 + i * 0.1, ease: "power3.out", immediateRender: false }, t - 0.4);
    tl.set("#p2-res", { textContent: label, opacity: 1 }, t + 0.2);
  };
  spin(T.nachricht, [0, 2, 4], "1 NACHRICHT");
  spin(T.like, [1, 6, 8], "1 LIKE");
  spin(T.nichts, [2, 4, 6], "NICHTS.");
  tl.set("#p2-res", { textContent: "???" }, T.vorher - 0.2);
  fadeIn("#p2-u", T.unber, 0.3);
  tl.to("#p2-u", { opacity: 0, duration: 0.2 }, T.hose - 0.6);
  popIn("#p2-h", T.hose - 0.4, 0.35, 0.5);
  tl.to("#p2-cam", { opacity: 0, duration: 0.15 }, T.end - 0.15);
""", T)
SFX += [(T["zweitens"], "click", 0.45)] + [(t - 0.4, "click", 0.35) for t in (T["nachricht"], T["like"], T["nichts"])] + [(T["nachricht"] + 0.2, "pop", 0.4), (T["like"] + 0.2, "pop", 0.4), (T["hose"] - 0.4, "pop", 0.4)]

# ================================================================ P3 Flucht: unangenehm → Notausgang → Aufmerksamkeitsrest
a, e = SEG["r_flucht"]
T = dict(drittens=W("Drittens:"), flow=W("Flow"), unang=W("unangenehm"), notaus=W("Notausgang."), danach=W("danach"), aufm=W("Aufmerksamkeit"))
scene("p3", a, e, f"""
  <div id="p3-cam" class="lay">
    {tag("p3", 3, "DIE FLUCHT")}
    <div id="p3-A" class="lay">
      {otto("p3", 170, 540, 0.62, ("tired", "excuse"))}
      <div id="p3-th" class="actor" style="left:620px;top:540px;width:70px;height:440px;border-radius:35px;background:#22262E;border:4px solid #3A3F48;overflow:hidden;opacity:0">
        <div id="p3-lv" style="position:absolute;left:0;right:0;bottom:0;height:100%;background:linear-gradient(0deg,#4FA3FF,#FF4B3E);transform-origin:50% 100%"></div></div>
      <div id="p3-tl" class="t" style="left:710px;top:560px;font-size:30px;font-weight:900;letter-spacing:.08em;color:{RED};opacity:0">UNANGE-<br>NEHM</div>
    </div>
    {cchip("p3-ex", 520, "🏃 NOTAUSGANG 📱", "#1B8A3A", "#FFF", 60, "#7CFF8A")}
    <div id="p3-B" class="lay" style="opacity:0">
      <div class="actor card" style="left:170px;top:660px;width:740px;padding:28px 30px">
        <div style="font-size:30px;font-weight:800;letter-spacing:.14em;color:{MUTED}">AUFMERKSAMKEIT DANACH</div>
        <div style="margin-top:18px;height:40px;border-radius:20px;background:#2A2E36;overflow:hidden"><div id="p3-f" style="height:100%;background:{GREEN};transform-origin:0 50%"></div></div></div>
      {ctext("p3-r", 880, "EIN TEIL HÄNGT NOCH AM HANDY", 48, color=RED)}
    </div>
  </div>""", r"""
  tagIn("#p3-tag", T.drittens);
  fadeIn("#p3-otto", T.drittens + 0.3, 0.3);
  fadeIn("#p3-th", T.flow, 0.3);
  tl.fromTo("#p3-lv", { scaleY: 0.1 }, { scaleY: 0.95, duration: 1.4, ease: "power2.in" }, T.unang - 0.4);
  fadeIn("#p3-tl", T.unang, 0.3);
  face("p3o", "tired", "excuse", T.unang);
  outUp("#p3-A", T.notaus - 0.5, 0.25);
  slam("#p3-ex", T.notaus - 0.3, 1.8);
  fadeIn("#p3-B", T.danach - 0.1, 0.3);
  tl.fromTo("#p3-f", { scaleX: 1 }, { scaleX: 0.66, duration: 0.8, ease: "power3.inOut" }, T.aufm - 0.2);
  fadeIn("#p3-r", T.aufm - 0.3, 0.3);
  tl.to("#p3-cam", { opacity: 0, duration: 0.15 }, T.end - 0.15);
""", T)
SFX += [(T["drittens"], "click", 0.45), (T["notaus"] - 0.3, "pop", 0.45), (T["aufm"] - 0.2, "pop", 0.35)]

# ================================================================ P4 Der Trick: keine Willenskraft · anderer Raum · Benachrichtigungen aus · 10 Sekunden
a, e = SEG["r_trick"]
T = dict(der=W("Der", 55), willens=W("Willenskraft."), raum=W("Raum."), bena=W("Benachrichtigungen", 60), zaehl=W("Zähl"), was=W("was", 65))
rows = [("🚪", "HANDY IN ANDEREN RAUM", "raum"), ("🔕", "BENACHRICHTIGUNGEN AUS", "bena"), ("⏱️", "BIS 10 ZÄHLEN", "zaehl")]
rh = "".join(f'<div id="p4-r{i}" class="actor card" style="left:170px;top:{640 + i * 110}px;width:740px;height:96px;display:flex;align-items:center;gap:22px;padding:0 26px;opacity:0">'
             f'<span style="font-size:48px">{em}</span><span style="font-size:38px;font-weight:900">{t}</span></div>' for i, (em, t, _) in enumerate(rows))
scene("p4", a, e, f"""
  <div id="p4-cam" class="lay">
    {tag("p4", 4, "DER TRICK")}
    {ctext("p4-w", 520, "💪 WILLENSKRAFT", 80)}
    <div id="p4-x" class="actor" style="left:250px;top:560px;width:580px;height:12px;background:{RED};border-radius:6px;transform:rotate(-4deg);transform-origin:0 50%;opacity:0"></div>
    {rh}
    <div id="p4-q" class="actor" style="left:170px;top:980px;padding:18px 28px;border-radius:30px;background:#F4F6FA;color:#1A1A1A;font-size:36px;font-weight:900;opacity:0">💭 Was will ich gerade vermeiden?</div>
  </div>""", r"""
  tagIn("#p4-tag", T.der);
  fadeIn("#p4-w", T.der + 0.3, 0.3);
  tl.fromTo("#p4-x", { opacity: 1, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.3, ease: "power3.out" }, T.willens + 0.2);
  [T.raum, T.bena, T.zaehl].forEach((t, i) => tl.fromTo(`#p4-r${i}`, { opacity: 0, x: 100 }, { opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }, t - 0.3));
  tl.fromTo("#p4-q", { opacity: 0, scale: 0.5, transformOrigin: "0% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, T.was - 0.2);
  tl.to("#p4-cam", { opacity: 0, duration: 0.15 }, T.end - 0.15);
""", T)
SFX += [(T["der"], "click", 0.45), (T["willens"] + 0.2, "click", 0.4)] + [(T[k] - 0.3, "pop", 0.4) for k in ("raum", "bena", "zaehl")] + [(T["was"] - 0.2, "pop", 0.35)]

# ================================================================ P5 Zeit um! → Bildschirmzeit-Check → ganze Folge morgen Abend, Link in der Bio
a, e = SEG["r_trick"][1], END
T = dict(zeit=T1, kleiner=W("Kleiner"), wie=W("Wie", 70), schau=W("Schau", 72), zahl=W("Zahl"), die=W("Die", 75.5), ganze=W("ganze", 75.5),
         morgen=W("morgen"), youtube=W("YouTube."), link=W("Link"), bio=W("Bio."))
scene("p5", a, e, f"""
  <div id="p5-fl" class="actor" style="left:0;top:-400px;width:1080px;height:2700px;background:#FFF;opacity:0"></div>
  <div id="p5-cam" class="lay">
    {ctext("p5-zu", 620, "ZEIT UM!", 180, color=RED, extra="text-shadow:0 0 60px rgba(255,60,40,.7)")}
    <div id="p5-C" class="lay">
      {ctext("p5-ch", 450, "📱 DEIN CHECK", 60, color=AMBER)}
      <div id="p5-g" class="actor card" style="left:170px;top:560px;width:740px;padding:26px 30px;opacity:0">
        <div style="font-size:36px;font-weight:800">🍏 Bildschirmzeit → <span style="color:{AMBER}">Aktivierungen</span></div>
        <div style="margin-top:14px;font-size:36px;font-weight:800">🤖 Digital Wellbeing → <span style="color:{AMBER}">Entsperrungen</span></div></div>
      <div id="p5-cm" class="actor card" style="left:170px;top:820px;width:740px;height:96px;display:flex;align-items:center;gap:18px;padding:0 24px;opacity:0">
        <span style="font-size:44px">💬</span><span style="font-size:34px;font-weight:800;color:{MUTED}">Heute entsperrt: ___ mal</span></div>
    </div>
    <div id="p5-D" class="lay">
      {ctext("p5-k", 446, "DIE GANZE FOLGE", 56, cls="", color=AMBER, extra="font-weight:900;letter-spacing:.18em")}
      <div id="p5-card" class="actor" style="left:192px;top:540px;width:696px;height:391px;border-radius:22px;overflow:hidden;box-shadow:0 30px 90px rgba(0,0,0,.7), 0 0 0 4px #2A2D33;opacity:0">
        <img src="assets/thumb.png" style="width:696px;height:391px;display:block" />
        <div style="position:absolute;right:18px;bottom:18px;padding:4px 12px;border-radius:8px;background:rgba(0,0,0,.85);font-size:30px;font-weight:800">6:49</div>
        <div id="p5-play" style="position:absolute;left:288px;top:138px;width:120px;height:116px;opacity:0">
          <svg viewBox="0 0 120 116" width="120" height="116"><rect x="0" y="16" width="120" height="84" rx="24" fill="#FF0033"/><path d="M48,38 L82,58 L48,78 Z" fill="#FFF"/></svg></div></div>
      <div id="p5-so" class="actor" style="left:560px;top:570px;padding:10px 22px;border-radius:14px;background:{AMBER};color:#1A1A1A;font-size:36px;font-weight:900;letter-spacing:.04em;transform:rotate(6deg);box-shadow:0 12px 30px rgba(0,0,0,.5);opacity:0">MORGEN ABEND</div>
      <div id="p5-yt" class="t" style="left:0;width:1080px;top:960px;text-align:center;opacity:0">
        <span style="display:inline-flex;align-items:center;gap:14px;padding:10px 26px;border-radius:40px;background:#FF0033;font-size:36px;font-weight:900">▶ YouTube · Otto Normalpsyche</span></div>
      <div id="p5-bio" class="t" style="left:0;width:1080px;top:960px;text-align:center;opacity:0">
        <span style="display:inline-flex;align-items:center;gap:14px;padding:10px 30px;border-radius:40px;background:#FFF;color:#1A1A1A;font-size:40px;font-weight:900">🔗 LINK IN DER BIO</span></div>
      {otto("p5", 70, 770, 0.36, ("happy",))}
    </div>
  </div>""", r"""
  tl.fromTo("#p5-fl", { opacity: 0.45 }, { opacity: 0, duration: 0.35, ease: "power2.out", immediateRender: false }, T.zeit);
  slam("#p5-zu", T.zeit, 2.8);
  shake("#p5-cam", T.zeit + 0.22, 8);
  tl.to("#p5-zu", { y: -260, scale: 0.4, opacity: 0, duration: 0.3, ease: "power3.in" }, T.kleiner - 0.2);
  popIn("#p5-ch", T.kleiner, 0.35, 0.5);
  tl.fromTo("#p5-g", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, T.schau - 0.2);
  tl.fromTo("#p5-cm", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, T.zahl - 0.3);
  outUp("#p5-C", T.die - 0.2, 0.2);
  fadeIn("#p5-k", T.die, 0.3);
  tl.fromTo("#p5-card", { opacity: 0, y: 200, scale: 0.8, rotation: -4 }, { opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.5)" }, T.die);
  popIn("#p5-play", T.ganze + 0.3, 0.35, 0.3);
  tl.fromTo("#p5-otto", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.8)" }, T.ganze + 0.5);
  tl.fromTo("#p5-so", { opacity: 0, scale: 2.2, rotation: 20 }, { opacity: 1, scale: 1, rotation: 6, duration: 0.3, ease: "back.out(2)" }, T.morgen);
  popIn("#p5-yt", T.youtube - 0.1, 0.35, 0.5);
  tl.to("#p5-yt", { opacity: 0, y: 30, duration: 0.2, ease: "power2.in" }, T.link - 0.15);
  popIn("#p5-bio", T.link, 0.35, 0.5);
  tl.fromTo("#p5-bio", { scale: 1.12 }, { scale: 1, duration: 0.4, ease: "back.out(3)", immediateRender: false }, T.bio);
  for (let i = 0; i < 3; i++) tl.fromTo("#p5-play", { scale: 1.15 }, { scale: 1, duration: 0.5, ease: "power2.out", immediateRender: false }, T.bio + 0.5 + i * 0.8);
""", T)
SFX += [(T["zeit"], "ding", 0.6), (T["kleiner"], "pop", 0.4), (T["schau"] - 0.2, "pop", 0.35), (T["zahl"] - 0.3, "pop", 0.35), (T["die"], "click", 0.45),
        (T["ganze"] + 0.3, "pop", 0.4), (T["morgen"], "pop", 0.45), (T["youtube"] - 0.1, "click", 0.6), (T["link"], "pop", 0.45), (T["bio"], "click", 0.5)]
