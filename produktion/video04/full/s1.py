# Wird von gen.py per exec() ausgeführt: Kaltstart, Hook, Frage, Umfrage, Titel, Kapitel 1.
# Richtlinie: alles innerhalb y 150–930 / x 60–1860, nichts in den Kinobalken.
import math as _m


def chapter(cid, sid, num, title):
    """Kapitelkarte mit automatisch passender Schriftgröße (lange Titel bleiben im Bild)."""
    a, _ = SEG[sid]
    size = min(130, int(1650 / (len(title) * 0.62)))
    put(cid, sid, f"""
  <div id="{cid}-k" class="t" style="left:0;right:0;top:400px;text-align:center;font-size:30px;font-weight:700;letter-spacing:.6em;color:{MUTED};opacity:0">KAPITEL {num}</div>
  <div id="{cid}-t" class="t cond" style="left:0;right:0;top:{530 - size * 0.55:.0f}px;text-align:center;font-size:{size}px;letter-spacing:.1em;opacity:0">{title}</div>
  <div id="{cid}-l" class="actor" style="left:260px;top:640px;width:1400px;height:2px;background:{AMBER};transform-origin:0 50%"></div>""", f"""
  tl.fromTo("#{cid}-k", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }}, 0.05);
  tl.fromTo("#{cid}-t", {{ opacity: 0, x: -80, filter: "blur(12px)" }}, {{ opacity: 1, x: 0, filter: "blur(0px)", duration: 0.5, ease: "power4.out" }}, 0.2);
  tl.fromTo("#{cid}-l", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8, ease: "power3.inOut" }}, 0.3);
  tl.to(["#{cid}-k", "#{cid}-t", "#{cid}-l"], {{ opacity: 0, duration: 0.35, ease: "power2.in" }}, T.end - 0.4);""", {})
    SFX.extend([(a + 0.05, "click", 0.5), (a + 0.25, "boom", 0.6)])


def phone(id_, x, y, w=240, h=440, screen="", extra=""):
    return (f'<div id="{id_}" class="actor" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{w * 0.14:.0f}px;background:#111;border:6px solid #444;'
            f'box-shadow:0 30px 70px rgba(0,0,0,.6);{extra}">'
            f'<div style="position:absolute;left:{w * 0.06:.0f}px;top:{h * 0.06:.0f}px;right:{w * 0.06:.0f}px;bottom:{h * 0.06:.0f}px;border-radius:{w * 0.06:.0f}px;'
            f'background:linear-gradient(180deg,#1E2A44,#141824);overflow:hidden">{screen}</div></div>')


HAND = '<div style="font-size:150px;line-height:1">🤚</div>'

# ================================================================ c0 Kaltstart: 0 Nachrichten, Hand greift trotzdem
put("c0", "open", f"""
  <div id="c0-cam" class="lay">
    {light("c0-l", 960, 520, 420, "rgba(142,197,255,.18)")}
    {phone("c0-ph", 840, 250, 240, 440, '<div id="c0-sc" style="position:absolute;inset:0;background:#2A3E66;opacity:0"></div><div id="c0-tx" style="position:absolute;left:0;right:0;top:160px;text-align:center;font-size:28px;font-weight:800;color:#FFF;opacity:0">0 neue<br>Nachrichten</div>')}
    <div id="c0-hand" class="actor" style="left:1110px;top:420px;opacity:0">{HAND}</div>
  </div>""", r"""
  tl.fromTo("#c0-sc", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 0.3);
  fadeIn("#c0-tx", 0.45, 0.25);
  tl.fromTo("#c0-hand", { opacity: 0, x: 160 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, 1.3);
  tl.to("#c0-hand", { x: -150, y: -40, duration: 0.35, ease: "power2.in" }, 1.9);
  tl.to("#c0-ph", { rotation: -8, y: -20, duration: 0.3, ease: "power2.out" }, 2.2);
  fadeOut("#c0-cam", T.end - 0.25, 0.25);
""", {})
SFX += [(0.3, "pop", 0.3), (SEG["open"][0] + 2.2, "click", 0.7)]

# ================================================================ c1 Hook: Vorsatz 1 Stunde, Handy daneben
S = "v_hook"; a = SEG[S][0]
T = dict(otto=W("Otto.", a), vorgenommen=W("vorgenommen:", a), stunde=W("Stunde", a), handy=W("Handy?", a), problem=W("Problem.", a))
put("c1", S, f"""
  <div id="c1-cam" class="lay">
    {otto_at("c1", 180, ("happy", "smirk"))}
    <div id="c1-goal" class="actor card" style="left:900px;top:220px;width:760px;padding:30px 36px;opacity:0">
      <div style="font-size:28px;font-weight:800;letter-spacing:.3em;color:{AMBER}">VORSATZ</div>
      <div class="cond" style="margin-top:10px;font-size:76px">1 STUNDE AM STÜCK</div>
      <div id="c1-ck" style="position:absolute;right:30px;top:24px;font-size:64px;color:{GREEN};opacity:0">✓</div></div>
    {phone("c1-ph", 1180, 520, 170, 300, '<div style="position:absolute;inset:0;background:#141824"></div>')}
    <div id="c1-np" class="actor" style="left:900px;top:620px;font-size:44px;font-weight:900;opacity:0">KEIN PROBLEM 😎</div>
  </div>""", r"""
  fadeIn("#c1-cam", 0, 0.4);
  tl.fromTo("#c1-goal", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, T.vorgenommen);
  popIn("#c1-ck", T.stunde + 0.3, 0.35);
  tl.fromTo("#c1-ph", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, T.handy - 0.1);
  tl.fromTo("#c1-np", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.35, ease: "back.out(2)" }, T.problem - 0.2);
  face("c1o", "happy", "smirk", T.problem - 0.2);
  fadeOut("#c1-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["vorgenommen"], "pop", 0.4), (T["stunde"] + 0.3, "click", 0.5), (T["handy"] - 0.1, "pop", 0.35)]

# ================================================================ c2 Satz tippen, löschen, Handy springt in die Hand, Rekord 4:37
S = "v_otto"; a = SEG[S][0]
T = dict(oeffnet=W("öffnet", a), schreibt=W("Schreibt", a), loescht=W("Löscht", a), dann=W("dann,", a), hand=W("Hand.", a), anruf=W("Anruf.", a),
         nachricht=W("Nachricht.", a), einfach=W("Einfach", a), vier=W("Vier", a), rekord=W("Rekord.", a), schlimmste=W("Schlimmste:", a), wollte=W("wollte.", a))
sent = "Folie 1: Warum unser Projekt"
sh = "".join(f'<span id="c2-c{i}" style="opacity:0">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(sent))
put("c2", S, f"""
  <div id="c2-cam" class="lay">
    {otto_at("c2", 140, ("tired", "shock", "excuse"))}
    <div id="c2-doc" class="actor card" style="left:860px;top:190px;width:900px;height:380px;opacity:0">
      <div style="height:64px;border-bottom:2px solid #3A3F48;display:flex;align-items:center;padding:0 26px;font-size:28px;font-weight:700;color:{MUTED}">Präsentation.pptx</div>
      <div style="position:absolute;left:40px;top:100px;width:820px;height:240px;background:#F4F5F7;border-radius:6px"></div>
      <div class="t" style="left:70px;top:150px;font-size:44px;font-weight:700;color:#1A1A1A">{sh}<span id="c2-cur" style="display:inline-block;width:4px;height:46px;background:#111;vertical-align:middle;margin-left:4px"></span></div></div>
    {phone("c2-ph", 1360, 640, 150, 270, '<div style="position:absolute;inset:0;background:#2A3E66"></div>')}
    {chip("c2-a", 900, 620, "📞 KEIN ANRUF", size=36)}
    {chip("c2-n", 900, 720, "💬 KEINE NACHRICHT", size=36)}
    <div id="c2-sw" class="actor card" style="left:1080px;top:600px;width:520px;height:230px;opacity:0">
      <div style="position:absolute;left:30px;top:24px;font-size:28px;font-weight:800;letter-spacing:.2em;color:{MUTED}">⏱ OHNE HANDY</div>
      <div id="c2-t" class="t" style="left:30px;top:80px;font-family:'Space Mono';font-weight:700;font-size:110px;color:#FFF">0:00</div></div>
    <div id="c2-tr" class="actor" style="left:1620px;top:620px;font-size:120px;filter:grayscale(.6);opacity:0">🏆</div>
    <div id="c2-rk" class="t cond" style="left:1080px;width:700px;top:850px;font-size:56px;color:{AMBER};opacity:0">NEUER REKORD …</div>
    <div id="c2-q" class="actor" style="left:860px;top:250px;padding:18px 28px;border-radius:30px;background:#F4F6FA;color:#1A1A1A;font-size:36px;font-weight:800;opacity:0">❓ Was wollte ich eigentlich?</div>
  </div>""", r"""
  fadeIn("#c2-cam", 0, 0.3);
  tl.fromTo("#c2-doc", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, T.oeffnet - 0.2);
  const n = %N%;
  for (let i = 0; i < n; i++) tl.fromTo(`#c2-c${i}`, { opacity: 0 }, { opacity: 1, duration: 0.01 }, T.schreibt + 0.1 + i * 0.045);
  for (let i = 0; i < n; i++) tl.to(`#c2-c${n - 1 - i}`, { opacity: 0, duration: 0.01 }, T.loescht + 0.1 + i * 0.025);
  tl.fromTo("#c2-ph", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T.oeffnet);
  tl.to("#c2-ph", { x: -740, y: -10, rotation: -12, duration: 0.45, ease: "back.in(1.4)" }, T.dann + 0.3);
  face("c2o", "tired", "shock", T.hand);
  tl.to("#c2-doc", { opacity: 0.25, duration: 0.3 }, T.hand);
  popIn("#c2-a", T.anruf - 0.15, 0.3); popIn("#c2-n", T.nachricht - 0.15, 0.3);
  tl.to(["#c2-a", "#c2-n"], { opacity: 0, duration: 0.25 }, T.vier - 0.4);
  popIn("#c2-sw", T.vier - 0.3, 0.35);
  for (let k = 0; k <= 16; k++) { const s = Math.round(277 * (1 - Math.pow(1 - k / 16, 2))); tl.set("#c2-t", { textContent: `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}` }, T.vier + k * 0.1); }
  tl.fromTo("#c2-tr", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, T.rekord - 0.1);
  fadeIn("#c2-rk", T.rekord, 0.3);
  face("c2o", "shock", "excuse", T.schlimmste);
  tl.to("#c2-doc", { opacity: 0, duration: 0.3 }, T.schlimmste);
  tl.fromTo("#c2-q", { opacity: 0, scale: 0.5, transformOrigin: "0% 100%" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, T.schlimmste + 0.4);
  fadeOut("#c2-cam", T.end - 0.3, 0.3);
""".replace("%N%", str(len(sent))), T)
SFX += [(T["schreibt"], "typing", 0.3), (T["dann"] + 0.3, "click", 0.6), (T["anruf"] - 0.15, "pop", 0.35), (T["nachricht"] - 0.15, "pop", 0.35),
        (T["vier"] - 0.3, "pop", 0.35), (T["rekord"] - 0.1, "pop", 0.4), (T["schlimmste"] + 0.4, "pop", 0.35)]

# ================================================================ c3 Frage: 0 Nachrichten – trotzdem? WARUM?
S = "v_frage"; a = SEG[S][0]
T = dict(warum=W("Warum", a), nichts=W("passiert", a), schwer=W("schwer,", a), liegen=W("liegen", a))
put("c3", S, f"""
  <div id="c3-cam" class="lay">
    {light("c3-l", 640, 520, 460, "rgba(142,197,255,.16)")}
    {phone("c3-ph", 520, 200, 260, 480, '<div style="position:absolute;left:0;right:0;top:170px;text-align:center;font-size:30px;font-weight:800;color:#FFF">0 neue<br>Nachrichten</div>')}
    <div id="c3-hand" class="actor" style="left:760px;top:420px">{HAND}</div>
    {stamp("c3-st", 1040, 300, "WARUM?", RED, 140, -6)}
    <div id="c3-s" class="t cond" style="left:1000px;top:560px;font-size:64px;line-height:1.1;opacity:0">… UND WARUM SO SCHWER,<br><span style="color:{AMBER}">ES LIEGEN ZU LASSEN?</span></div>
  </div>""", r"""
  fadeIn("#c3-cam", 0, 0.3);
  tl.fromTo("#c3-hand", { x: 60 }, { keyframes: [{ x: -40, duration: 0.5 }, { x: 0, duration: 0.5 }], repeat: 4, ease: "sine.inOut", immediateRender: false }, 0.2);
  slam("#c3-st", T.warum, 2.2);
  tl.fromTo("#c3-s", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, T.schwer - 0.3);
  fadeOut("#c3-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["warum"] + 0.25, "boom", 0.4), (T["schwer"] - 0.3, "pop", 0.35)]

# ================================================================ c4 Umfrage: Wie oft entsperrt?
S = "v_poll"; a = SEG[S][0]
POLL = [("A", "Weniger als 20×"), ("B", "20 bis 50×"), ("C", "Mehr als 50×")]


def poll_opts(cid):
    return "".join(f'<div id="{cid}-o{i}" class="actor" style="left:60px;top:{220 + i * 120}px;width:1000px;height:96px;border-radius:16px;background:#22262E;'
                   f'border:2px solid #3A3F48;display:flex;align-items:center;gap:28px;padding:0 28px;opacity:0">'
                   f'<div style="width:56px;height:56px;border-radius:50%;background:{AMBER};color:#111;font-size:32px;font-weight:900;display:flex;align-items:center;justify-content:center">{k}</div>'
                   f'<div style="font-size:40px;font-weight:700">{v}</div>'
                   f'<div id="{cid}-tg{i}" style="margin-left:auto;font-size:30px;font-weight:900;color:{AMBER};opacity:0">🙋 OTTO</div></div>'
                   for i, (k, v) in enumerate(POLL))


q_html, nq = typed("c4-qq", "Wie oft hast du dein Handy heute entsperrt?", "left:60px;top:120px;font-size:42px;letter-spacing:0;font-weight:700;color:#FFF;")
T = dict(kurze=W("Kurze", a), wie=W("Wie", a), A=W("A:", a), B=W("B:", a), C=W("C:", a), merk=W("Merk", a), gleich=W("Gleich", a))
put("c4", S, f"""
  <div id="c4-cam" class="lay">
    {light("c4-l", 960, 500, 760, "rgba(255,226,180,.14)")}
    <div id="c4-card" class="actor card" style="left:400px;top:190px;width:1120px;height:620px;opacity:0">
      <div class="t" style="left:60px;top:50px;font-size:28px;font-weight:800;letter-spacing:.4em;color:{AMBER}">SCHÄTZFRAGE</div>
      {q_html}{poll_opts("c4")}</div>
    <div id="c4-m" class="t cond" style="left:0;right:0;top:330px;text-align:center;font-size:120px;opacity:0">MERK DIR<br>DEINEN TIPP</div>
    <div id="c4-e" class="t" style="left:0;right:0;top:700px;text-align:center;font-size:30px;font-weight:800;letter-spacing:.3em;color:{MUTED};opacity:0">DER CHECK KOMMT GLEICH ↓</div>
    {cursor("c4", 1500, 860)}
  </div>""", f'type("#c4-qq", {nq}, T.wie, 0.025);' + r"""
  fadeIn("#c4-cam", 0, 0.3);
  tl.fromTo("#c4-card", { opacity: 0, y: 80, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power4.out" }, T.kurze - 0.1);
  fadeIn("#c4-cur", T.A - 0.6, 0.2);
  [T.A, T.B, T.C].forEach((t, i) => {
    tl.fromTo(`#c4-o${i}`, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.45, ease: "back.out(1.6)" }, t);
    move("#c4-cur", -520, -442 + i * 120, t - 0.25, 0.4);
    tl.to(`#c4-o${i}`, { borderColor: "#E8C27A", backgroundColor: "#2C2A24", duration: 0.2 }, t + 0.15);
    if (i < 2) tl.to(`#c4-o${i}`, { borderColor: "#3A3F48", backgroundColor: "#22262E", duration: 0.2 }, [T.B, T.C][i] - 0.1);
  });
  fadeOut("#c4-cur", T.merk - 0.3, 0.2);
  tl.to("#c4-card", { opacity: 0.12, scale: 0.97, duration: 0.5, ease: "power2.inOut" }, T.merk - 0.2);
  tl.fromTo("#c4-m", { opacity: 0, scale: 1.15 }, { opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }, T.merk);
  fadeIn("#c4-e", T.gleich, 0.5);
  fadeOut("#c4-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["kurze"] - 0.1, "pop", 0.3)] + [(T[k], "pop", 0.5) for k in ("A", "B", "C")] + [(T["merk"], "click", 0.5)]

# ================================================================ c5 Titelkarte
title = "DER HANDY-REFLEX"
letters = "".join(f'<span id="c5-c{i}" style="display:inline-block;opacity:0">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(title))
a5, _ = SEG["title"]
put("c5", "title", f"""
  <div id="c5-k" class="t" style="left:0;right:0;top:380px;text-align:center;font-size:40px;font-weight:800;letter-spacing:.8em;color:{AMBER};opacity:0">OTTO</div>
  <div class="t cond" style="left:0;right:0;top:450px;text-align:center;font-size:150px;letter-spacing:.06em;">{letters}</div>
  <div id="c5-line" class="actor" style="left:560px;top:640px;width:800px;height:3px;background:#FFF;transform-origin:50% 50%"></div>""", f"""
  fadeIn("#c5-k", 0.05, 0.4);
  for (let i = 0; i < {len(title)}; i++) tl.fromTo(`#c5-c${{i}}`, {{ opacity: 0, y: -90, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }}, 0.25 + i * 0.03);
  tl.fromTo("#c5-line", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power3.out" }}, 0.7);
  tl.to(["#c5-k", "#c5-line"], {{ opacity: 0, duration: 0.3 }}, T.end - 0.35);
  for (let i = 0; i < {len(title)}; i++) tl.to(`#c5-c${{i}}`, {{ opacity: 0, y: 40, duration: 0.25, ease: "power2.in" }}, T.end - 0.4 + i * 0.008);
""", {})
SFX += [(a5 + 0.05, "click", 0.5), (a5 + 0.3, "boom", 0.6)]

chapter("c6", "kap1", 1, "DER GRIFF, DEN DU NICHT MERKST")

# ================================================================ c7 Gloria Mark: 2:30 → 0:47
S = "v_mark"; a = SEG[S][0]
T = dict(gloria=W("Gloria", a), bild=W("Bildschirm", a), anfang=W("Anfang", a), zweieinhalb=W("zweieinhalb", a), neueren=W("neueren", a), sieben=W("siebenundvierzig", a))
put("c7", S, f"""
  <div id="c7-cam" class="lay">
    {header("c7", "AUFMERKSAMKEIT AM BILDSCHIRM", "IM SCHNITT PRO SACHE")}
    {lower_third("c7", "GLORIA MARK", "INFORMATIKERIN", 130, 690)}
    <div id="c7-r0" class="t" style="left:130px;top:420px;font-size:34px;font-weight:900;color:{MUTED};opacity:0">ANFANG 2000ER</div>
    <div id="c7-b0" class="actor" style="left:500px;top:405px;width:1200px;height:70px;border-radius:12px;background:#6B7280;transform-origin:0 50%;opacity:0"></div>
    <div id="c7-v0" class="t" style="left:520px;top:412px;font-family:'Space Mono';font-weight:700;font-size:52px;color:#FFF;opacity:0">2:30</div>
    <div id="c7-r1" class="t" style="left:130px;top:560px;font-size:34px;font-weight:900;color:{AMBER};opacity:0">HEUTE</div>
    <div id="c7-b1" class="actor" style="left:500px;top:545px;width:1200px;height:70px;border-radius:12px;background:{AMBER};transform-origin:0 50%;opacity:0"></div>
    <div id="c7-v1" class="t" style="left:520px;top:552px;font-family:'Space Mono';font-weight:700;font-size:52px;color:#111;opacity:0">2:30</div>
    {foot("c7", "Mark (2023), Attention Span · Durchschnittswerte")}
  </div>""", HEADER_JS("c7") + LT_JS("c7", "T.gloria") + r"""
  fadeIn("#c7-cam", 0, 0.3);
  fadeOut("#c7-lt", T.anfang - 0.5, 0.3);
  fadeIn("#c7-r0", T.anfang, 0.3);
  tl.fromTo("#c7-b0", { opacity: 1, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.8, ease: "power3.out" }, T.zweieinhalb - 0.3);
  fadeIn("#c7-v0", T.zweieinhalb, 0.3);
  fadeIn("#c7-r1", T.neueren, 0.3);
  fadeIn("#c7-b1", T.neueren, 0.2);
  tl.fromTo("#c7-b1", { scaleX: 1 }, { scaleX: 0.313, duration: 1.2, ease: "power3.inOut", immediateRender: false }, T.neueren + 0.2);
  fadeIn("#c7-v1", T.neueren + 0.2, 0.2);
  for (let k = 0; k <= 10; k++) { const s = Math.round(150 - (150 - 47) * k / 10); tl.set("#c7-v1", { textContent: `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}` }, T.neueren + 0.2 + k * 0.12); }
  tl.fromTo("#c7-b1", { boxShadow: "0 0 0 rgba(232,194,122,0)" }, { boxShadow: "0 0 40px rgba(232,194,122,.8)", duration: 0.4, immediateRender: false }, T.sieben);
  fadeIn("#c7-ft", T.gloria + 0.5, 0.4);
  fadeOut("#c7-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["gloria"], "click", 0.45), (T["zweieinhalb"] - 0.3, "pop", 0.35), (T["neueren"] + 0.2, "pop", 0.35)]

# ================================================================ c8 Selbst-Unterbrechungen: zwei gleich hohe Stapel
S = "v_selbst"; a = SEG[S][0]
T = dict(verrueckte=W("Verrückte:", a), aussen=W("außen.", a), studien=W("Studien", a), selbst=W("selbst,", a), anderen=W("anderen", a), niemand=W("Niemand", a), ab=W("ab.", a))
st0 = "".join(f'<div id="c8-a{i}" class="actor" style="left:520px;top:{760 - i * 70}px;width:300px;height:56px;border-radius:10px;background:#3A5A8C;opacity:0"></div>' for i in range(6))
st1 = "".join(f'<div id="c8-b{i}" class="actor" style="left:1100px;top:{760 - i * 70}px;width:300px;height:56px;border-radius:10px;background:{ORANGE};opacity:0"></div>' for i in range(6))
put("c8", S, f"""
  <div id="c8-cam" class="lay">
    {header("c8", "UNTERBRECHUNGEN", "WER STÖRT HIER EIGENTLICH?")}
    {st0}{st1}
    <div class="t" style="left:470px;width:400px;top:840px;text-align:center;font-size:34px;font-weight:900">📞 VON ANDEREN</div>
    <div class="t" style="left:1050px;width:400px;top:840px;text-align:center;font-size:34px;font-weight:900">🫵 VON UNS SELBST</div>
    <div id="c8-eq" class="t cond" style="left:880px;width:160px;top:500px;text-align:center;font-size:110px;color:{AMBER};opacity:0">=</div>
    <div id="c8-w" class="t cond" style="left:0;right:0;top:400px;text-align:center;font-size:110px;opacity:0">WIR RUFEN<br><span style="color:{AMBER}">UNS SELBST AB.</span></div>
    {foot("c8", "Dabbish, Mark &amp; González (2011)")}
  </div>""", HEADER_JS("c8") + r"""
  fadeIn("#c8-cam", 0, 0.3);
  for (let i = 0; i < 6; i++) tl.fromTo(`#c8-a${i}`, { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.25, ease: "back.out(2)" }, T.studien + i * 0.12);
  for (let i = 0; i < 6; i++) tl.fromTo(`#c8-b${i}`, { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.25, ease: "back.out(2)" }, T.selbst + i * 0.12);
  popIn("#c8-eq", T.anderen + 0.3, 0.35);
  fadeIn("#c8-ft", T.studien, 0.3);
  tl.to(["#c8-a0", "#c8-a1", "#c8-a2", "#c8-a3", "#c8-a4", "#c8-a5", "#c8-b0", "#c8-b1", "#c8-b2", "#c8-b3", "#c8-b4", "#c8-b5", "#c8-eq", "#c8-hk", "#c8-ht"], { opacity: 0.12, duration: 0.3 }, T.niemand - 0.2);
  tl.fromTo("#c8-w", { opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }, T.niemand + 0.6);
  fadeOut("#c8-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["studien"], "pop", 0.3), (T["selbst"], "pop", 0.3), (T["anderen"] + 0.3, "click", 0.45), (T["niemand"] + 0.6, "pop", 0.4)]

# ================================================================ c9 Gewohnheits-Schleife: Auslöser → Griff → Belohnung, immer schneller
S = "v_schleife"; a = SEG[S][0]
T = dict(gewohnheit=W("Gewohnheit.", a), schleife=W("Schleife:", a), ausloeser=W("Auslöser,", a), handlung=W("Handlung:", a), belohnung=W("Belohnung:", a),
         staerker=W("stärker.", a), tausend=W("tausend", a), fragen=W("fragen.", a), greift=W("greift", a), zaehne=W("Zähneputzen.", a))
LX, LY, LR = 960, 620, 230
nodes = [("😐", "AUSLÖSER", "Langeweile", -90), ("📱", "GRIFF", "zum Handy", 30), ("✨", "BELOHNUNG", "irgendwas Neues", 150)]
nh = "".join(f'<div id="c9-n{i}" class="actor card" style="left:{LX + LR * _m.cos(_m.radians(ang)) - 150:.0f}px;top:{LY + LR * _m.sin(_m.radians(ang)) - 75:.0f}px;width:300px;height:150px;'
             f'display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0"><div style="font-size:52px;line-height:1">{em}</div>'
             f'<div class="cond" style="font-size:40px;margin-top:6px">{lab}</div><div style="font-size:28px;color:{MUTED};font-weight:700">{sub}</div></div>'
             for i, (em, lab, sub, ang) in enumerate(nodes))
ring = [(LX + LR * _m.cos(_m.radians(-90 + 360 * k / 36)), LY + LR * _m.sin(_m.radians(-90 + 360 * k / 36))) for k in range(37)]
laps = [3.0, 2.2, 1.5, 1.0, 0.7, 0.5, 0.4, 0.35]
kf = ", ".join(f'{{ x: {x - ring[0][0]:.1f}, y: {y - ring[0][1]:.1f}, duration: {d / 36:.3f} }}' for d in laps for x, y in ring[1:])
put("c9", S, f"""
  <div id="c9-cam" class="lay">
    {header("c9", "KAPITEL 1", "DIE GEWOHNHEITS-SCHLEIFE")}
    <svg class="actor" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
      <circle id="c9-rg" cx="{LX}" cy="{LY}" r="{LR}" fill="none" stroke="#3A3F48" stroke-width="8" opacity="0"/></svg>
    {nh}
    <div id="c9-dot" class="actor" style="left:{ring[0][0] - 22:.0f}px;top:{ring[0][1] - 22:.0f}px;width:44px;height:44px;border-radius:50%;background:{ORANGE};border:5px solid #FFF;box-shadow:0 0 26px rgba(255,122,26,.8);opacity:0"></div>
    <div id="c9-cnt" class="t" style="left:1500px;top:500px;font-family:'Space Mono';font-weight:700;font-size:72px;color:{AMBER};opacity:0">×<span id="c9-n">1</span></div>
    <div id="c9-auto" class="t cond" style="left:1420px;top:640px;font-size:56px;opacity:0">🪥 AUTOMATISCH</div>
  </div>""", HEADER_JS("c9") + f"""
  fadeIn("#c9-cam", 0, 0.3);
  tl.fromTo("#c9-rg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, T.schleife - 0.2);
  [T.ausloeser, T.handlung, T.belohnung].forEach((t, i) => popIn(`#c9-n${{i}}`, t - 0.15, 0.4));
  popIn("#c9-dot", T.staerker - 0.8, 0.3);
  tl.to("#c9-dot", {{ keyframes: [{kf}], ease: "none" }}, T.staerker - 0.5);
  tl.fromTo("#c9-rg", {{ attr: {{ "stroke-width": 8 }}, stroke: "#3A3F48" }}, {{ attr: {{ "stroke-width": 40 }}, stroke: "#8A5A2E", duration: {sum(laps):.2f}, ease: "power1.in", immediateRender: false }}, T.staerker - 0.5);
  fadeIn("#c9-cnt", T.tausend - 0.3, 0.3);
  tl.fromTo("#c9-n", {{ textContent: 1 }}, {{ textContent: 1000, duration: 1.6, ease: "power2.in", snap: {{ textContent: 1 }} }}, T.tausend - 0.2);
  popIn("#c9-auto", T.zaehne - 0.2, 0.4);
  fadeOut("#c9-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T[k] - 0.15, "pop", 0.4) for k in ("ausloeser", "handlung", "belohnung")] + [(T["tausend"] - 0.2, "tick", 0.3), (T["zaehne"] - 0.2, "pop", 0.4)]
