# Wird von gen.py per exec() ausgeführt: Kapitel 4 (5 Handy-Hacks), Auflösung, Umfrage, Brücke, Abspann.

chapter("c20", "kap4", 4, "DER HANDY-HACK")

# ================================================================ c21 Keine Willenskraft – 5 Tricks
S = "v_gut"; a = SEG[S][0]
T = dict(reflex=W("Reflex", a), willens=W("Willenskraft.", a), tricks=W("Tricks.", a))
dots = "".join(f'<div id="c21-d{i}" class="actor" style="left:{600 + i * 150}px;top:640px;width:110px;height:110px;border-radius:50%;background:{AMBER};color:#111;'
               f'display:flex;align-items:center;justify-content:center;font-family:\'Oswald\';font-weight:700;font-size:64px;opacity:0">{i + 1}</div>' for i in range(5))
put("c21", S, f"""
  <div id="c21-cam" class="lay">
    <div id="c21-w" class="t cond" style="left:0;right:0;top:300px;text-align:center;font-size:120px;opacity:0">💪 WILLENSKRAFT</div>
    <div id="c21-x" class="actor" style="left:560px;top:355px;width:800px;height:16px;background:{RED};border-radius:8px;transform:rotate(-4deg);transform-origin:0 50%;opacity:0"></div>
    <div id="c21-t" class="t cond" style="left:0;right:0;top:480px;text-align:center;font-size:96px;color:{AMBER};opacity:0">5 EINFACHE TRICKS</div>
    {dots}
  </div>""", r"""
  fadeIn("#c21-cam", 0, 0.3);
  popIn("#c21-w", T.reflex, 0.4);
  tl.fromTo("#c21-x", { opacity: 1, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.3, ease: "power3.out" }, T.willens + 0.2);
  fadeIn("#c21-t", T.tricks - 0.3, 0.3);
  for (let i = 0; i < 5; i++) popIn(`#c21-d${i}`, T.tricks + i * 0.1, 0.3);
  fadeOut("#c21-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["willens"] + 0.2, "click", 0.5), (T["tricks"], "pop", 0.35)]

# ================================================================ c22 Hack 1: aus den Augen (Grundriss)
S = "v_hack1"; a = SEG[S][0]
T = dict(augen=W("Augen.", a), umdrehen=W("umdrehen,", a), lautlos=W("lautlos", a), raum=W("Raum", a), siehst=W("siehst,", a))
put("c22", S, f"""
  <div id="c22-cam" class="lay">
    {header("c22", "HACK 1", "AUS DEN AUGEN")}
    <div class="actor" style="left:330px;top:360px;width:640px;height:480px;border:6px solid #8C8F96;border-radius:8px"></div>
    <div class="actor" style="left:964px;top:360px;width:640px;height:480px;border:6px solid #8C8F96;border-radius:8px"></div>
    <div class="t" style="left:350px;top:375px;font-size:28px;font-weight:900;letter-spacing:.2em;color:{MUTED}">ARBEITSZIMMER</div>
    <div class="t" style="left:990px;top:375px;font-size:28px;font-weight:900;letter-spacing:.2em;color:{MUTED}">KÜCHE</div>
    <div class="actor" style="left:440px;top:560px;width:260px;height:120px;border-radius:10px;background:#5B4632"></div>
    <div class="actor" style="left:470px;top:470px;font-size:80px">🧑‍💻</div>
    <div id="c22-door" class="actor" style="left:958px;top:540px;width:16px;height:130px;background:#C9A64A;transform-origin:50% 0%"></div>
    <div id="c22-ph" class="actor" style="left:720px;top:600px;font-size:70px">📱</div>
    {chip("c22-u", 1180, 180, "🔄 UMDREHEN ✗", size=34)}
    {chip("c22-l", 1180, 270, "🔇 LAUTLOS ✗", size=34)}
    <div id="c22-ok" class="t cond" style="left:1100px;top:720px;font-size:56px;color:{GREEN};opacity:0">✓ AUS DEN AUGEN</div>
  </div>""", HEADER_JS("c22") + r"""
  fadeIn("#c22-cam", 0, 0.3);
  popIn("#c22-u", T.umdrehen - 0.1, 0.3); popIn("#c22-l", T.lautlos - 0.1, 0.3);
  tl.to("#c22-ph", { keyframes: [{ x: 300, y: -40, duration: 0.5 }, { x: 600, y: 0, duration: 0.5 }], ease: "power2.inOut" }, T.raum - 0.4);
  tl.fromTo("#c22-door", { rotation: -80 }, { rotation: 0, duration: 0.4, ease: "back.out(2)" }, T.raum + 0.7);
  popIn("#c22-ok", T.siehst, 0.35);
  fadeOut("#c22-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["umdrehen"] - 0.1, "pop", 0.3), (T["lautlos"] - 0.1, "pop", 0.3), (T["raum"] + 0.7, "click", 0.6)]

# ================================================================ c23 Hack 2: Benachrichtigungen aus
S = "v_hack2"; a = SEG[S][0]
T = dict(aus=W("aus.", a), experiment=W("Experiment", a), haeufiger=W("häufiger", a), wichtig=W("wichtig", a), zweimal=W("zweimal", a))
apps = ["📸 Social Media", "🎵 Video-App", "💬 Gruppenchats", "📰 News", "✉️ Mails"]
tg = "".join(f'<div class="actor" style="left:230px;top:{360 + i * 96}px;width:620px;height:80px;border-radius:14px;background:#16181D;border:2px solid #3A3F48;display:flex;align-items:center;padding:0 24px;font-size:34px;font-weight:800">'
             f'{n}<div id="c23-sw{i}" style="margin-left:auto;width:90px;height:48px;border-radius:24px;background:#34C759;position:relative">'
             f'<div id="c23-k{i}" style="position:absolute;left:46px;top:4px;width:40px;height:40px;border-radius:50%;background:#FFF"></div></div></div>' for i, n in enumerate(apps))
put("c23", S, f"""
  <div id="c23-cam" class="lay">
    {header("c23", "HACK 2", "BENACHRICHTIGUNGEN AUS")}
    {tg}
    <div id="c23-bars" class="lay" style="opacity:0">
      <div class="t" style="left:1000px;top:360px;font-size:28px;font-weight:800;letter-spacing:.2em;color:{MUTED}">UNAUFMERKSAMKEIT</div>
      <div id="c23-b0" class="actor" style="left:1040px;top:470px;width:200px;height:300px;background:{RED};border-radius:12px 12px 4px 4px;transform-origin:50% 100%"></div>
      <div id="c23-b1" class="actor" style="left:1340px;top:620px;width:200px;height:150px;background:{GREEN};border-radius:12px 12px 4px 4px;transform-origin:50% 100%"></div>
      <div class="t" style="left:980px;width:320px;top:785px;text-align:center;font-size:28px;font-weight:900">🔔 MIT</div>
      <div class="t" style="left:1280px;width:320px;top:785px;text-align:center;font-size:28px;font-weight:900">🔕 OHNE</div></div>
    <div id="c23-clk" class="actor card" style="left:1080px;top:380px;width:440px;height:380px;display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0">
      <div style="font-size:150px;line-height:1">🕐</div><div class="cond" style="margin-top:14px;font-size:52px;color:{AMBER}">2× PRO STUNDE</div></div>
    {foot("c23", "Kushlev, Proulx &amp; Dunn (2016) · Selbstauskünfte")}
  </div>""", HEADER_JS("c23") + r"""
  fadeIn("#c23-cam", 0, 0.3);
  for (let i = 0; i < 5; i++) { tl.to(`#c23-k${i}`, { x: -42, duration: 0.2, ease: "power2.inOut" }, T.aus + i * 0.18); tl.to(`#c23-sw${i}`, { backgroundColor: "#4A4E57", duration: 0.2 }, T.aus + i * 0.18); }
  fadeIn("#c23-bars", T.experiment, 0.3); fadeIn("#c23-ft", T.experiment, 0.3);
  tl.fromTo("#c23-b0", { scaleY: 0 }, { scaleY: 1, duration: 0.6, ease: "back.out(1.4)" }, T.haeufiger - 0.3);
  tl.fromTo("#c23-b1", { scaleY: 0 }, { scaleY: 1, duration: 0.5, ease: "power3.out" }, T.haeufiger + 0.3);
  tl.to("#c23-k2", { x: 0, duration: 0.2 }, T.wichtig); tl.to("#c23-sw2", { backgroundColor: "#34C759", duration: 0.2 }, T.wichtig);
  tl.to(["#c23-bars", "#c23-ft"], { opacity: 0, duration: 0.3 }, T.zweimal - 0.5);
  popIn("#c23-clk", T.zweimal - 0.2, 0.4);
  fadeOut("#c23-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["aus"] + i * 0.18, "click", 0.35) for i in range(5)] + [(T["haeufiger"] - 0.3, "pop", 0.35), (T["wichtig"], "click", 0.4), (T["zweimal"] - 0.2, "pop", 0.4)]

# ================================================================ c24 Hack 3: Reibung (Apps in Ordner, abmelden)
S = "v_hack3"; a = SEG[S][0]
T = dict(reibung=W("Reibung", a), ordner=W("Ordner.", a), melde=W("Melde", a), handgriff=W("Handgriff", a), auto=W("Autopiloten.", a))
icons = [("📸", "#C13584"), ("🎵", "#111"), ("▶️", "#FF0033"), ("💬", "#25D366"), ("🛒", "#FF9900"), ("📰", "#3A5A8C"), ("🗺️", "#4285F4"), ("📷", "#6B7280"), ("☀️", "#F4B400")]
ih = "".join(f'<div id="c24-a{i}" class="actor" style="left:{770 + (i % 3) * 140}px;top:{370 + (i // 3) * 130}px;width:110px;height:110px;border-radius:24px;background:{c};'
             f'display:flex;align-items:center;justify-content:center;font-size:60px">{em}</div>' for i, (em, c) in enumerate(icons))
put("c24", S, f"""
  <div id="c24-cam" class="lay">
    {header("c24", "HACK 3", "BAU REIBUNG EIN")}
    <div class="actor" style="left:730px;top:330px;width:460px;height:590px;border-radius:50px;background:#111;border:6px solid #444"></div>
    {ih}
    <div id="c24-f" class="actor" style="left:850px;top:770px;width:220px;height:130px;border-radius:26px;background:rgba(255,255,255,.18);border:3px solid rgba(255,255,255,.4);
      display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:800;opacity:0">📁 Später</div>
    <div id="c24-lk" class="actor" style="left:1260px;top:420px;font-size:120px;opacity:0">🔒</div>
    <div id="c24-lt" class="t cond" style="left:1260px;top:570px;font-size:48px;opacity:0">ABGEMELDET</div>
    <div id="c24-tx" class="t cond" style="left:130px;top:780px;font-size:56px;color:{AMBER};opacity:0">JEDER HANDGRIFF<br>BREMST DEN AUTOPILOTEN</div>
  </div>""", HEADER_JS("c24") + r"""
  fadeIn("#c24-cam", 0, 0.3);
  popIn("#c24-f", T.ordner - 0.8, 0.35);
  [0, 1, 2].forEach((i, k) => tl.to(`#c24-a${i}`, { x: 100 - (i % 3) * 140 + 40, y: 470, scale: 0.25, opacity: 0, duration: 0.45, ease: "power3.in" }, T.ordner - 0.5 + k * 0.15));
  popIn("#c24-lk", T.melde, 0.35); fadeIn("#c24-lt", T.melde + 0.2, 0.3);
  tl.fromTo("#c24-tx", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }, T.handgriff - 0.2);
  fadeOut("#c24-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["ordner"] - 0.5 + k * 0.15, "pop", 0.3) for k in range(3)] + [(T["melde"], "click", 0.5)]

# ================================================================ c25 Hack 4: 10-Sekunden-Regel
S = "v_hack4"; a = SEG[S][0]
T = dict(regel=W("Zehn-Sekunden-Regel.", a), drang=W("Drang", a), zaehl=W("zähl", a), frag=W("frag", a), vermeiden=W("vermeiden?", a), bemerkst=W("bemerkst.", a), mini=W("Mini-Countdown", a))
put("c25", S, f"""
  <div id="c25-cam" class="lay">
    {header("c25", "HACK 4", "DIE 10-SEKUNDEN-REGEL")}
    <svg id="c25-ring" class="actor" style="left:200px;top:360px;opacity:0" width="440" height="440" viewBox="0 0 440 440">
      <circle cx="220" cy="220" r="170" fill="#111" stroke="#2A2E36" stroke-width="22"/>
      <circle id="c25-arc" cx="220" cy="220" r="170" fill="none" stroke="{AMBER}" stroke-width="22" stroke-dasharray="1068" stroke-dashoffset="0" transform="rotate(-90 220 220)"/></svg>
    <div id="c25-n" class="t" style="left:200px;width:440px;top:500px;text-align:center;font-family:'Space Mono';font-weight:700;font-size:140px;line-height:1;opacity:0">10</div>
    <div id="c25-q" class="actor" style="left:760px;top:400px;padding:28px 36px;border-radius:40px;background:#F4F6FA;color:#1A1A1A;font-size:48px;font-weight:900;opacity:0">💭 Was will ich gerade vermeiden?</div>
    <div id="c25-ok" class="t cond" style="left:760px;top:580px;font-size:56px;color:{GREEN};opacity:0">BEMERKT = OFT SCHON VORBEI</div>
    {chip("c25-m", 760, 700, "⏱ 25:00 MINI-COUNTDOWN · FOLGE 2", "#2C2A24", AMBER, 38, "#6B5A30")}
  </div>""", HEADER_JS("c25") + r"""
  fadeIn("#c25-cam", 0, 0.3);
  popIn("#c25-ring", T.drang - 0.2, 0.35); popIn("#c25-n", T.drang - 0.2, 0.35);
  tl.to("#c25-arc", { attr: { "stroke-dashoffset": 1068 }, duration: 3.0, ease: "none" }, T.zaehl);
  for (let i = 1; i <= 10; i++) tl.set("#c25-n", { textContent: String(10 - i) }, T.zaehl + i * 0.3);
  tl.fromTo("#c25-q", { opacity: 0, scale: 0.5, transformOrigin: "0% 50%" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, T.frag);
  fadeIn("#c25-ok", T.bemerkst - 0.6, 0.4);
  popIn("#c25-m", T.mini - 0.2, 0.4);
  fadeOut("#c25-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["zaehl"], "tick", 0.3), (T["frag"], "pop", 0.4), (T["mini"] - 0.2, "pop", 0.4)]

# ================================================================ c26 Hack 5: Langeweile aushalten
S = "v_hack5"; a = SEG[S][0]
T = dict(lang=W("Langeweile", a), letzten=W("letzten", a), ideen=W("Ideen.", a), luecke=W("Lücke", a), dusch=W("Dusch-Momente", a))
idots = "".join(f'<div id="c26-i{i}" class="actor" style="left:{620 + (i * 97) % 520}px;top:{420 + (i * 61) % 260}px;width:26px;height:26px;border-radius:50%;background:{AMBER};opacity:0"></div>' for i in range(8))
put("c26", S, f"""
  <div id="c26-cam" class="lay">
    {header("c26", "HACK 5", "HALTE LANGEWEILE AUS")}
    <div id="c26-bub" class="actor" style="left:540px;top:340px;width:760px;height:460px;border-radius:50%;border:5px solid rgba(255,255,255,.55);opacity:0"></div>
    {idots}
    {bulb_html("c26-b", 820, 440, 0.9)}
    {chip("c26-f3", 1360, 300, "🚿 FOLGE 3", "#2C2A24", AMBER, 36, "#6B5A30")}
    <div id="c26-ph" class="actor" style="left:740px;top:300px;width:360px;height:560px;border-radius:44px;background:#111;border:6px solid #444;opacity:0">
      <div style="margin:30px 20px;height:480px;border-radius:20px;background:linear-gradient(180deg,#3A5A8C,#8C3A5A)"></div></div>
  </div>""", HEADER_JS("c26") + r"""
  fadeIn("#c26-cam", 0, 0.3);
  popIn("#c26-bub", T.lang, 0.4);
  popIn("#c26-f3", T.letzten, 0.35);
  for (let i = 0; i < 8; i++) { popIn(`#c26-i${i}`, T.letzten + 0.4 + i * 0.1, 0.25); tl.to(`#c26-i${i}`, { x: ((i * 37) % 80) - 40, y: ((i * 53) % 60) - 30, duration: 1.4, yoyo: true, repeat: 1, ease: "sine.inOut" }, T.letzten + 0.8); }
  tl.fromTo("#c26-b", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }, T.ideen - 0.2);
  tl.fromTo("#c26-b-g", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T.ideen);
  tl.fromTo("#c26-ph", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, T.luecke - 0.2);
  fadeOut("#c26-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["lang"], "pop", 0.35), (T["letzten"], "pop", 0.35), (T["ideen"] - 0.2, "ding", 0.6), (T["luecke"] - 0.2, "click", 0.45)]

# ================================================================ c27 Auflösung: Handy in der Küche, Griff ins Leere, 60:00 ✓
S = "v_aufl"; a = SEG[S][0]
T = dict(ausprobiert=W("ausprobiert.", a), kueche=W("Küche.", a), leere=W("Leere.", a), stunde=W("Stunde", a), fertig=W("fertig.", a), verpasst=W("verpasst", a))
put("c27", S, f"""
  <div id="c27-cam" class="lay">
    {otto_at("c27", 160, ("tired", "happy"))}
    {chip("c27-k", 900, 200, "📱 → 🍳 KÜCHE", size=40)}
    <div id="c27-h" class="actor" style="left:700px;top:560px;opacity:0">{HAND}</div>
    <div id="c27-x" class="t" style="left:860px;top:560px;font-size:48px;font-weight:900;color:{RED};opacity:0">… LEER</div>
    <div id="c27-sw" class="actor card" style="left:1080px;top:330px;width:560px;height:230px;opacity:0">
      <div style="position:absolute;left:30px;top:24px;font-size:28px;font-weight:800;letter-spacing:.2em;color:{MUTED}">⏱ OHNE HANDY</div>
      <div id="c27-t" class="t" style="left:30px;top:80px;font-family:'Space Mono';font-weight:700;font-size:110px;color:#FFF">0:00</div>
      <div id="c27-ck" style="position:absolute;right:30px;top:90px;font-size:90px;color:{GREEN};opacity:0">✓</div></div>
    {chip("c27-f", 1080, 610, "📊 PRÄSENTATION: FAST FERTIG", size=36)}
    {chip("c27-v", 1080, 710, "😌 NICHTS VERPASST", "#183A24", GREEN, 36, "#2E6B42")}
  </div>""", r"""
  fadeIn("#c27-cam", 0, 0.3);
  popIn("#c27-k", T.kueche - 0.3, 0.35);
  for (let i = 0; i < 3; i++) tl.fromTo("#c27-h", { opacity: 0, x: 60 }, { keyframes: [{ opacity: 1, x: 0, duration: 0.25 }, { opacity: 0, duration: 0.25, delay: 0.25 }], immediateRender: false }, T.leere - 1.6 + i * 0.75);
  tl.fromTo("#c27-x", { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.2 }, { opacity: 0, duration: 0.3, delay: 0.8 }], immediateRender: false }, T.leere - 0.2);
  popIn("#c27-sw", T.stunde - 0.6, 0.35);
  for (let k = 0; k <= 15; k++) tl.set("#c27-t", { textContent: `${k * 4}:00` }, T.stunde - 0.3 + k * 0.08);
  popIn("#c27-ck", T.stunde + 1.0, 0.3);
  face("c27o", "tired", "happy", T.stunde + 1.0);
  popIn("#c27-f", T.fertig - 0.3, 0.35);
  popIn("#c27-v", T.verpasst - 0.3, 0.35);
  fadeOut("#c27-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["kueche"] - 0.3, "pop", 0.35), (T["stunde"] + 1.0, "ding", 0.6), (T["fertig"] - 0.3, "pop", 0.35), (T["verpasst"] - 0.3, "pop", 0.35)]

# ================================================================ c28 Umfrage-Auflösung: Otto hat auch C
S = "v_umfrage2"; a = SEG[S][0]
T = dict(und=W("du?", a), A=W("A,", a), B=W("B", a), C=W("C?", a), komm=W("Kommentare.", a), otto=W("Otto", a), c2=W("C.", a))
put("c28", S, f"""
  <div id="c28-cam" class="lay">
    {light("c28-l", 960, 500, 760, "rgba(255,226,180,.14)")}
    <div id="c28-card" class="actor card" style="left:400px;top:190px;width:1120px;height:620px;opacity:0">
      <div class="t" style="left:60px;top:50px;font-size:28px;font-weight:800;letter-spacing:.4em;color:{AMBER}">AUFLÖSUNG</div>
      <div class="t" style="left:60px;top:120px;font-size:42px;font-weight:700">Wie oft hast du dein Handy heute entsperrt?</div>
      {poll_opts("c28")}</div>
    {cursor("c28", 1500, 860)}
  </div>""", r"""
  fadeIn("#c28-cam", 0, 0.3);
  tl.fromTo("#c28-card", { opacity: 0, y: 80, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power4.out" }, T.und - 0.3);
  [T.A, T.B, T.C].forEach((t, i) => tl.fromTo(`#c28-o${i}`, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.6)" }, t - 0.1));
  fadeIn("#c28-cur", T.komm - 1.0, 0.2);
  move("#c28-cur", -520, -202, T.komm - 0.9, 0.5);
  tl.to("#c28-o2", { borderColor: "#E8C27A", backgroundColor: "#2C2A24", scale: 1.04, duration: 0.3 }, T.otto);
  tl.fromTo("#c28-tg2", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, T.c2 - 0.1);
  click("c28", T.c2);
  fadeOut("#c28-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T[k] - 0.1, "pop", 0.4) for k in ("A", "B", "C")] + [(T["c2"], "click", 0.6)]

# ================================================================ c29 Brücke: nachts im Bett mit Handy
S = "v_bruecke"; a = SEG[S][0]
T = dict(abends=W("abends", a), bett=W("Bett,", a), todmuede=W("todmüde", a), naechstes=W("nächstes", a))
put("c29", S, f"""
  <div id="c29-cam" class="lay">
    <div class="actor" style="left:0;top:132px;width:1920px;height:816px;background:rgba(10,14,30,.6)"></div>
    {light("c29-gl", 560, 420, 260, "rgba(142,197,255,.45)")}
    {otto_at("c29", 260, ("tired",), top=200, s=0.9)}
    <div id="c29-clk" class="actor" style="left:1200px;top:220px;padding:10px 24px;background:#111;border:3px solid #333;border-radius:14px;font-family:'Space Mono';font-weight:700;font-size:72px;color:#FF5A4A;opacity:0">01:12</div>
    <div id="c29-k" class="t" style="left:900px;top:520px;font-size:30px;font-weight:800;letter-spacing:.4em;color:{MUTED};opacity:0">NÄCHSTE FOLGE</div>
    <div id="c29-t" class="t cond" style="left:900px;top:570px;font-size:72px;line-height:1.05;opacity:0">WARUM DU ABENDS<br>NICHT INS BETT GEHST</div>
  </div>""", r"""
  fadeIn("#c29-cam", 0, 0.4);
  popIn("#c29-clk", T.abends, 0.35);
  tl.to("#c29-gl", { opacity: 0.6, duration: 0.3, yoyo: true, repeat: 5 }, T.bett);
  fadeIn("#c29-k", T.todmuede + 0.3, 0.4);
  tl.fromTo("#c29-t", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, T.todmuede + 0.5);
  fadeOut("#c29-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["abends"], "pop", 0.35), (T["todmuede"] + 0.5, "pop", 0.35)]

# ================================================================ c30 Abspann (Platzhalter für YouTube-Endbildschirm)
put("c30", "endcard", f"""
  <div id="c30-ch" class="t cond" style="left:0;right:0;top:190px;text-align:center;font-size:70px;letter-spacing:.3em;opacity:0">OTTO NORMALPSYCHE</div>
  <div id="c30-sub" class="t" style="left:0;right:0;top:285px;text-align:center;font-size:28px;font-weight:600;letter-spacing:.4em;color:{MUTED};opacity:0">WARUM WIR TUN, WAS WIR TUN</div>
  <div id="c30-sb" class="actor" style="left:300px;top:420px;width:300px;height:300px;border-radius:50%;border:2px dashed #555;opacity:0"></div>
  <div id="c30-sbt" class="t" style="left:300px;width:300px;top:740px;text-align:center;font-size:28px;font-weight:700;letter-spacing:.3em;opacity:0">ABONNIEREN</div>
  <div id="c30-nv" class="actor" style="left:900px;top:400px;width:720px;height:405px;border:2px dashed #555;opacity:0"></div>
  <div id="c30-nt" class="t" style="left:900px;top:350px;font-size:28px;font-weight:700;letter-spacing:.4em;color:{AMBER};opacity:0">WEITERSCHAUEN</div>""", r"""
  fadeIn("#c30-ch", 0.3, 0.8); fadeIn("#c30-sub", 0.8, 0.6);
  ["#c30-sb", "#c30-sbt", "#c30-nv", "#c30-nt"].forEach((s, i) => fadeIn(s, 1.2 + i * 0.15, 0.6));
""", {})
SFX += [(SEG["endcard"][0] + 0.3, "pop", 0.25)]
