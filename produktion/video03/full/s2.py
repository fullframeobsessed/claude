# Wird von gen.py per exec() ausgeführt: Kapitel 2 (Autopilot) und Kapitel 3 (Aha-Moment) inkl. Pause.

chapter("c12", "kap2", 2, "DER AUTOPILOT IM KOPF")

# ================================================================ c13 Gedanken wandern + 47 %
S = "v_wandern"; a = SEG[S][0]
T = dict(dusche=W("Dusche", a), schlaf=W("Schlaf.", a), koerper=W("Körper", a), kopf=W("Kopf", a), wandern=W("wandern.", a), harvard=W("Harvard", a),
         haelfte=W("Hälfte", a), abschweifen=W("abschweifen.", a))
bub = [("🏖️", 120, -40), ("🎵", 260, -120), ("🍕", 60, -200), ("✈️", 230, -260)]
bh = "".join(f'<div id="c13-b{i}" class="actor" style="left:{560 + dx}px;top:{460 + dy}px;width:110px;height:110px;border-radius:50%;background:rgba(255,255,255,.1);border:3px solid rgba(255,255,255,.35);'
             f'display:flex;align-items:center;justify-content:center;font-size:56px;opacity:0">{em}</div>' for i, (em, dx, dy) in enumerate(bub))
R = 170; CIRC = 2 * 3.14159 * R
put("c13", S, f"""
  <div id="c13-cam" class="lay">
    {otto_at("c13", 180, ("tired", "happy"), top=230, s=0.9)}
    {chip("c13-k1", 160, 860, "🧍 KÖRPER: BESCHÄFTIGT", "#183A24", GREEN, 32, "#2E6B42")}
    {chip("c13-k2", 160, 150, "🧠 KOPF: FREI", "#2C2A24", AMBER, 32, "#6B5A30")}
    {bh}
    <div id="c13-chart" class="actor" style="left:1180px;top:240px;width:440px;height:440px;opacity:0">
      <svg viewBox="0 0 440 440" width="440" height="440"><circle cx="220" cy="220" r="{R}" fill="none" stroke="#2A2E36" stroke-width="60"/>
        <circle id="c13-arc" cx="220" cy="220" r="{R}" fill="none" stroke="{AMBER}" stroke-width="60" stroke-dasharray="{CIRC:.1f}" stroke-dashoffset="{CIRC:.1f}" transform="rotate(-90 220 220)"/></svg>
      <div class="t" style="left:0;width:440px;top:170px;text-align:center;font-family:'Space Mono';font-weight:700;font-size:96px"><span id="c13-p">0</span>%</div></div>
    <div id="c13-cl" class="t" style="left:1080px;width:640px;top:720px;text-align:center;font-size:34px;font-weight:800;letter-spacing:.06em;line-height:1.3;opacity:0">DER WACHEN ZEIT<br><span style="color:{AMBER}">SCHWEIFEN UNSERE GEDANKEN AB</span></div>
    {foot("c13", "Killingsworth &amp; Gilbert (2010), Harvard", 1080)}
  </div>""", r"""
  fadeIn("#c13-cam", 0, 0.4);
  tl.fromTo("#c13-k1", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, T.koerper);
  tl.fromTo("#c13-k2", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, T.kopf);
  for (let i = 0; i < 4; i++) {
    tl.fromTo(`#c13-b${i}`, { opacity: 0, scale: 0.2, y: 120 }, { opacity: 1, scale: 1, y: 0, duration: 0.6, ease: "back.out(1.6)" }, T.wandern - 0.5 + i * 0.25);
    tl.to(`#c13-b${i}`, { y: -15, x: (i % 2 ? 20 : -20), duration: 3, ease: "sine.inOut", yoyo: true, repeat: 1 }, T.wandern + 0.3 + i * 0.25);
  }
  face("c13o", "tired", "happy", T.wandern);
  popIn("#c13-chart", T.harvard - 0.2, 0.45);
  tl.fromTo("#c13-arc", { attr: { "stroke-dashoffset": %CIRC% } }, { attr: { "stroke-dashoffset": %OFF% }, duration: 1.4, ease: "power2.inOut" }, T.haelfte - 0.3);
  tl.fromTo("#c13-p", { textContent: 0 }, { textContent: 47, duration: 1.4, ease: "power2.inOut", snap: { textContent: 1 } }, T.haelfte - 0.3);
  fadeIn("#c13-cl", T.haelfte - 0.2, 0.4); fadeIn("#c13-ft", T.harvard, 0.4);
  fadeOut("#c13-cam", T.end - 0.3, 0.3);
""".replace("%CIRC%", f"{CIRC:.1f}").replace("%OFF%", f"{CIRC * 0.53:.1f}"), T)
SFX += [(T["koerper"], "pop", 0.35), (T["kopf"], "pop", 0.35)] + [(T["wandern"] - 0.5 + i * 0.25, "pop", 0.25) for i in range(4)] + [(T["harvard"] - 0.2, "click", 0.5)]

# ================================================================ c14 Ruhezustandsnetzwerk: Knoten verbinden → IDEE
S = "v_dmn"; a = SEG[S][0]
T = dict(netz=W("Netzwerk,", a), ruhe=W("Ruhezustandsnetzwerk,", a), default=W("Default", a), verk=W("verknüpft", a), erinn=W("Erinnerungen,", a),
         bilder=W("Bilder", a), gedanken=W("Gedanken,", a), stoff=W("Stoff,", a), ideen=W("Ideen", a))
nodes = [(820, 420), (960, 360), (1100, 430), (900, 540), (1050, 560), (980, 460)]
nh = "".join(f'<div id="c14-n{i}" class="actor" style="left:{x - 14}px;top:{y - 14}px;width:28px;height:28px;border-radius:50%;background:{AMBER};box-shadow:0 0 24px rgba(232,194,122,.9);opacity:0"></div>' for i, (x, y) in enumerate(nodes))
tags = [("🏖️ URLAUB 2019", 250, 260), ("🎵 SONG IM RADIO", 1360, 250), ("📊 PRÄSENTATION", 760, 780)]
th = "".join(chip(f"c14-t{i}", x, y, t, size=34) for i, (t, x, y) in enumerate(tags))
ends = [(560, 300), (1360, 290), (960, 780)]
lh = "".join(f'<path id="c14-l{i}" d="M{x},{y} L960,470" stroke="{AMBER}" stroke-width="5" fill="none" stroke-dasharray="900" stroke-dashoffset="900"/>' for i, (x, y) in enumerate(ends))
put("c14", S, f"""
  <div id="c14-cam" class="lay">
    {light("c14-l", 960, 470, 520, "rgba(247,168,196,.12)")}
    <div id="c14-brain" class="actor" style="left:660px;top:250px;width:600px;height:450px;opacity:0">{svgbox(art.brain(0, 0, 1.3, "#6E4A5A"), "-260 -200 520 400", 600, 450)}</div>
    {nh}
    <svg class="actor" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">{lh}</svg>
    {th}
    <div id="c14-name" class="t" style="left:0;right:0;top:150px;text-align:center;opacity:0">
      <div class="cond" style="font-size:72px;letter-spacing:.06em">RUHEZUSTANDSNETZWERK</div>
      <div id="c14-en" style="margin-top:6px;font-size:30px;font-weight:800;letter-spacing:.3em;color:{MUTED};opacity:0">DEFAULT MODE NETWORK</div></div>
    <div id="c14-idea" class="actor" style="left:880px;top:380px;width:160px;height:160px;opacity:0">
      {light("c14-ig", 80, 80, 200, "rgba(255,220,120,.7)")}
      <div style="position:absolute;left:30px;top:10px">{svgbox(BULB, "-100 -110 200 230", 100, 115)}</div>
      <div class="t cond" style="left:-40px;width:240px;top:130px;text-align:center;font-size:56px;color:{AMBER}">IDEE!</div></div>
  </div>""", r"""
  fadeIn("#c14-cam", 0, 0.3);
  tl.fromTo("#c14-brain", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }, T.netz - 0.6);
  for (let i = 0; i < 6; i++) { popIn(`#c14-n${i}`, T.netz + i * 0.12, 0.3); tl.to(`#c14-n${i}`, { scale: 1.5, duration: 0.5, yoyo: true, repeat: 7, ease: "sine.inOut" }, T.netz + 0.6 + i * 0.15); }
  fadeIn("#c14-name", T.ruhe - 0.1, 0.4); fadeIn("#c14-en", T.default, 0.4);
  [T.erinn, T.bilder, T.gedanken].forEach((t, i) => { popIn(`#c14-t${i}`, t - 0.1, 0.35);
    tl.to(`#c14-l${i}`, { attr: { "stroke-dashoffset": 0 }, duration: 0.6, ease: "power2.inOut" }, t + 0.2); });
  tl.to("#c14-brain", { opacity: 0.35, duration: 0.4 }, T.stoff - 0.4);
  popIn("#c14-idea", T.ideen - 0.15, 0.45);
  fadeOut("#c14-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["netz"] + i * 0.12, "pop", 0.2) for i in range(0, 6, 2)] + [(T[k] - 0.1, "pop", 0.4) for k in ("erinn", "bilder", "gedanken")] + [(T["ideen"] - 0.15, "ding", 0.6)]

# ================================================================ c15 Studie 2022: Regler langweilig ↔ anstrengend
S = "v_mittel"; a = SEG[S][0]
T = dict(studie=W("Studie", a), jahr=W("zweitausendzweiundzwanzig", a), bisschen=W("bisschen", a), lang=W("langweilig,", a), anstr=W("anstrengend.", a),
         duschen=W("Duschen.", a), spazier=W("Spazierengehen.", a))
put("c15", S, f"""
  <div id="c15-cam" class="lay">
    {header("c15", "STUDIE 2022", "DIE GOLDENE MITTE")}
    <div id="c15-trk" class="actor" style="left:260px;top:560px;width:1400px;height:24px;border-radius:12px;background:linear-gradient(90deg,#4A6FA5,#2A2E36 35%,#2A2E36 65%,#B5483D);opacity:0"></div>
    <div id="c15-zone" class="actor" style="left:760px;top:520px;width:400px;height:104px;border-radius:20px;border:4px solid {GREEN};background:rgba(124,255,138,.10);opacity:0"></div>
    <div id="c15-zl" class="t" style="left:760px;width:400px;top:470px;text-align:center;font-size:28px;font-weight:900;letter-spacing:.2em;color:{GREEN};opacity:0">OPTIMAL</div>
    <div class="t" style="left:220px;top:640px;font-size:36px;font-weight:900;letter-spacing:.1em;color:#8EB4E8">😴 LANGWEILIG</div>
    <div class="t" style="left:1420px;top:640px;font-size:36px;font-weight:900;letter-spacing:.1em;color:#F08A7E">ANSTRENGEND 😵</div>
    <div id="c15-ptr" class="actor" style="left:934px;top:500px;width:52px;height:144px;opacity:0">
      <div style="position:absolute;left:0;top:0;width:0;height:0;border-left:26px solid transparent;border-right:26px solid transparent;border-top:40px solid {AMBER}"></div>
      <div style="position:absolute;left:22px;top:36px;width:8px;height:108px;background:{AMBER};border-radius:4px"></div></div>
    <div id="c15-i0" class="actor" style="left:840px;top:330px;font-size:110px;opacity:0">🚿</div>
    <div id="c15-i1" class="actor" style="left:990px;top:330px;font-size:110px;opacity:0">🚶</div>
    {foot("c15", "Irving et al. (2022), Psychology of Aesthetics, Creativity, and the Arts")}
  </div>""", HEADER_JS("c15") + r"""
  fadeIn("#c15-cam", 0, 0.3);
  fadeIn("#c15-trk", T.studie, 0.4); fadeIn("#c15-ft", T.jahr, 0.4);
  popIn("#c15-ptr", T.studie + 0.2, 0.3);
  tl.to("#c15-ptr", { x: -600, duration: 0.5, ease: "power2.inOut" }, T.lang - 0.3);
  tl.to("#c15-ptr", { x: 600, duration: 0.6, ease: "power2.inOut" }, T.anstr - 0.3);
  tl.to("#c15-ptr", { x: 0, duration: 0.9, ease: "elastic.out(1, 0.5)" }, T.anstr + 0.5);
  tl.fromTo("#c15-zone", { opacity: 0, scaleX: 0.3 }, { opacity: 1, scaleX: 1, duration: 0.4, ease: "back.out(2)" }, T.bisschen);
  fadeIn("#c15-zl", T.bisschen + 0.2, 0.3);
  tl.fromTo("#c15-i0", { opacity: 0, y: -200 }, { opacity: 1, y: 0, duration: 0.5, ease: "bounce.out" }, T.duschen - 0.2);
  tl.fromTo("#c15-i1", { opacity: 0, y: -200 }, { opacity: 1, y: 0, duration: 0.5, ease: "bounce.out" }, T.spazier - 0.2);
  fadeOut("#c15-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["lang"] - 0.3, "click", 0.35), (T["anstr"] - 0.3, "click", 0.35), (T["bisschen"], "pop", 0.4), (T["duschen"], "drop", 0.35), (T["spazier"], "drop", 0.35)]

# ================================================================ c16 Letzter Ort ohne Bildschirm: Benachrichtigungen prallen ab
S = "v_ohnescreen"; a = SEG[S][0]
T = dict(vorteil=W("Vorteil:", a), bild=W("Bildschirm.", a), handy=W("Handy,", a), mails=W("Mails,", a), nachr=W("Nachrichten.", a), warme=W("warme", a),
         rauschen=W("Rauschen", a), allein=W("allein", a), alltag=W("Alltag", a))
noti = [("📱", -1, 340), ("✉️", 1, 480), ("🔔", -1, 620)]
nh2 = "".join(f'<div id="c16-n{i}" class="actor card" style="left:{(70 if s < 0 else 1510)}px;top:{y}px;width:340px;height:110px;display:flex;align-items:center;gap:16px;padding:0 20px;opacity:0">'
              f'<span style="font-size:56px">{em}</span><span style="font-size:28px;font-weight:800">{["NEUE NACHRICHT", "3 NEUE MAILS", "ERINNERUNG"][i]}</span></div>' for i, (em, s, y) in enumerate(noti))
steam = "".join(f'<div id="c16-s{i}" class="actor" style="left:{740 + (i * 97) % 440}px;top:780px;width:{120 + (i * 31) % 80}px;height:{120 + (i * 31) % 80}px;border-radius:50%;background:rgba(230,236,244,.18);filter:blur(18px);opacity:0"></div>' for i in range(9))
put("c16", S, f"""
  <div id="c16-cam" class="lay">
    {light("c16-l", 960, 520, 560, "rgba(142,197,255,.16)")}
    <div class="actor" style="left:660px;top:150px;width:600px;height:760px;opacity:.55;filter:blur(3px)">{otto_svg("c16o", ("happy",))}</div>
    <div id="c16-glass" class="actor" style="left:600px;top:150px;width:720px;height:770px;border-radius:20px;background:linear-gradient(135deg,rgba(220,232,244,.22),rgba(220,232,244,.08));
      border:3px solid rgba(220,232,244,.45);box-shadow:inset 0 0 80px rgba(255,255,255,.12);opacity:0"></div>
    <div id="c16-kb" class="t cond" style="left:600px;width:720px;top:470px;text-align:center;font-size:84px;color:#F4F7FB;text-shadow:0 0 30px rgba(0,0,0,.6);opacity:0">KEIN<br>BILDSCHIRM</div>
    {nh2}
    {steam}
    <div id="c16-th" class="actor" style="left:1110px;top:170px;padding:16px 26px;border-radius:30px;background:#F4F6FA;color:#1A1A1A;font-size:34px;font-weight:800;opacity:0">💭 nur ich und meine Gedanken</div>
  </div>""", r"""
  fadeIn("#c16-cam", 0, 0.3);
  tl.fromTo("#c16-glass", { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, T.vorteil - 0.2);
  popIn("#c16-kb", T.bild - 0.1, 0.4);
  [T.handy, T.mails, T.nachr].forEach((t, i) => {
    const s = [-1, 1, -1][i];
    tl.fromTo(`#c16-n${i}`, { opacity: 0, x: s * 160 }, { opacity: 1, x: -s * 230, duration: 0.35, ease: "power3.in" }, t - 0.5);
    tl.to(`#c16-n${i}`, { x: s * 500, rotation: -s * 25, opacity: 0, duration: 0.5, ease: "power2.out" }, t + 0.35);
  });
  tl.to("#c16-kb", { opacity: 0.25, duration: 0.4 }, T.warme - 0.2);
  for (let i = 0; i < 9; i++) tl.fromTo(`#c16-s${i}`, { opacity: 0, y: 0 }, { opacity: 1, y: -380 - i * 15, duration: 4, ease: "sine.out" }, T.warme + i * 0.25);
  tl.fromTo("#c16-th", { opacity: 0, scale: 0.5, transformOrigin: "0% 100%" }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }, T.allein);
  fadeOut("#c16-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T[k] + 0.05, "click", 0.5) for k in ("handy", "mails", "nachr")] + [(T["allein"], "pop", 0.4)]

chapter("c17", "kap3", 3, "DER AHA-MOMENT")

# ================================================================ c18 Keine Zauberei
S = "v_zauber"; a = SEG[S][0]
T = dict(achtung=W("Achtung:", a), zaubert=W("zaubert", a), nichts=W("Nichts.", a))
put("c18", S, f"""
  <div id="c18-cam" class="lay">
    {light("c18-l", 960, 470, 520, "rgba(200,170,255,.16)")}
    <div id="c18-hat" class="actor" style="left:810px;top:300px;font-size:260px;line-height:1;opacity:0">🎩</div>
    <div id="c18-sp" data-layout-allow-overlap class="actor" style="left:1060px;top:260px;font-size:110px;opacity:0">✨</div>
    <div id="c18-q" class="t cond" style="left:0;right:0;top:620px;text-align:center;font-size:84px;opacity:0">IDEEN AUS DEM NICHTS?</div>
    {stamp("c18-st", 760, 380, "NEIN.", RED, 170, -10)}
  </div>""", r"""
  fadeIn("#c18-cam", 0, 0.3);
  popIn("#c18-hat", T.achtung, 0.45);
  tl.fromTo("#c18-sp", { opacity: 0, scale: 0.3, rotation: -40 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }, T.zaubert);
  fadeIn("#c18-q", T.zaubert, 0.3);
  slam("#c18-st", T.nichts, 2.4);
  shake("#c18-cam", T.nichts + 0.25, 10);
  fadeOut("#c18-cam", T.end - 0.25, 0.25);
""", T)
SFX += [(T["zaubert"], "pop", 0.4), (T["nichts"] + 0.25, "boom", 0.45)]

# ================================================================ c19 Poincaré: Wochen → Bus → Idee
S = "v_poincare"; a = SEG[S][0]
T = dict(math=W("Mathematiker", a), wochen=W("wochenlang", a), einfiel=W("einfiel,", a), bus=W("Bus", a), ohne=W("Ohne", a), davor=W("davor", a))
pages = "".join(f'<div id="c19-p{i}" class="actor" style="left:{230 + i * 40}px;top:{330 + i * 30}px;width:300px;height:360px;background:#EDE6D6;border-radius:6px;box-shadow:0 20px 50px rgba(0,0,0,.6);'
                f'color:#333;padding:26px;opacity:0;transform:rotate({(-6, 2, 7)[i]}deg)" data-layout-allow-overlap><div style="font-size:28px;font-weight:900;letter-spacing:.2em;color:#8A2B1E">WOCHE {i + 1}</div>'
                f'<div style="margin-top:22px;font-family:\'EB Garamond\';font-size:30px;line-height:1.5;color:#555">f(z) = …<br>∑ aₙ zⁿ<br>z ↦ (az+b)/(cz+d)<br>?</div></div>' for i in range(3))
put("c19", S, f"""
  <div id="c19-cam" class="lay">
    {lower_third("c19", "HENRI POINCARÉ", "MATHEMATIKER · 1854–1912", 130, 180)}
    {pages}
    <div id="c19-road" class="actor" style="left:760px;top:740px;width:1100px;height:10px;background:#3A3F48;border-radius:5px;opacity:0"></div>
    <div id="c19-bus" class="actor" style="left:1280px;top:470px;font-size:280px;line-height:1;opacity:0">🚌</div>
    {bulb_html("c19-b", 1330, 190, 0.9)}
    <div id="c19-o" class="t cond" style="left:200px;width:560px;top:760px;text-align:center;font-size:52px;color:{AMBER};opacity:0">OHNE DIE WOCHEN DAVOR:<br>KEINE IDEE</div>
  </div>""", LT_JS("c19", "T.math - 0.3") + r"""
  fadeIn("#c19-cam", 0, 0.3);
  for (let i = 0; i < 3; i++) tl.fromTo(`#c19-p${i}`, { opacity: 0, y: -200 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.4)" }, T.wochen - 0.2 + i * 0.3);
  fadeIn("#c19-road", T.einfiel - 0.8, 0.3);
  tl.fromTo("#c19-bus", { opacity: 0, x: 400 }, { opacity: 1, x: 0, duration: 1.0, ease: "power3.out" }, T.einfiel - 0.8);
  tl.fromTo("#c19-b", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }, T.bus);
  tl.fromTo("#c19-b-g", { opacity: 0 }, { opacity: 1, duration: 0.4 }, T.bus + 0.1);
  fadeOut("#c19-lt", T.ohne - 0.6, 0.3);
  for (let i = 0; i < 3; i++) tl.to(`#c19-p${i}`, { boxShadow: "0 0 40px rgba(232,194,122,.8)", duration: 0.3 }, T.ohne + i * 0.15);
  fadeIn("#c19-o", T.davor, 0.4);
  fadeOut("#c19-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["wochen"] - 0.2 + i * 0.3, "pop", 0.3) for i in range(3)] + [(T["bus"], "ding", 0.55)]

# ================================================================ c20 Inkubation: 3 Phasen, Zahnräder, Studienbalken
S = "v_inkubation"; a = SEG[S][0]
T = dict(ink=W("Inkubation:", a), hart=W("hart", a), los=W("los.", a), hinter=W("Hintergrund", a), weiter=W("weiter.", a), studien=W("Studien", a),
         pause=W("Pause", a), stur=W("stur", a))
ph = [("VORBEREITEN", "📚"), ("LOSLASSEN", "⏸"), ("GEISTESBLITZ", "💡")]
phh = "".join(f'<div id="c20-p{i}" class="actor card" style="left:{230 + i * 520}px;top:330px;width:420px;height:260px;opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px">'
              f'<div style="font-size:90px;line-height:1">{em}</div><div class="cond" style="font-size:52px">{t}</div>'
              f'<div style="position:absolute;left:30px;right:30px;bottom:24px;height:12px;border-radius:6px;background:#2A2E36;overflow:hidden"><div id="c20-f{i}" style="height:100%;background:{AMBER};transform-origin:0 50%"></div></div></div>'
              + (f'<div id="c20-ar{i}" class="t" style="left:{665 + i * 520}px;top:420px;font-size:70px;color:{MUTED};opacity:0">→</div>' if i < 2 else "") for i, (t, em) in enumerate(ph))
gear = lambda gx, gy, r, id_: (f'<svg id="{id_}" class="actor" style="left:{gx - r}px;top:{gy - r}px;opacity:0" width="{2 * r}" height="{2 * r}" viewBox="-60 -60 120 120">'
                               + "".join(f'<rect x="-8" y="-58" width="16" height="20" rx="3" fill="#3A3F48" transform="rotate({k * 45})"/>' for k in range(8))
                               + '<circle r="44" fill="#3A3F48"/><circle r="16" fill="#0B0C0E"/></svg>')
put("c20", S, f"""
  <div id="c20-cam" class="lay">
    {header("c20", "KAPITEL 3", "INKUBATION")}
    {gear(960, 760, 90, "c20-g0")}{gear(1090, 700, 60, "c20-g1")}
    {phh}
    <div id="c20-bars" class="lay" style="opacity:0">
      <div id="c20-b0" class="actor" style="left:640px;top:520px;width:220px;height:300px;background:{GREEN};border-radius:14px 14px 4px 4px;transform-origin:50% 100%"></div>
      <div id="c20-b1" class="actor" style="left:1060px;top:680px;width:220px;height:140px;background:#6B7280;border-radius:14px 14px 4px 4px;transform-origin:50% 100%"></div>
      <div class="t" style="left:560px;width:380px;top:840px;text-align:center;font-size:32px;font-weight:900">MIT PAUSE</div>
      <div class="t" style="left:980px;width:380px;top:840px;text-align:center;font-size:32px;font-weight:900">STUR WEITER</div>
      <div class="t" style="left:600px;width:300px;top:440px;text-align:center;font-size:30px;font-weight:900;color:{GREEN}">BESSERE LÖSUNGEN</div></div>
    {foot("c20", "Sio &amp; Ormerod (2009), Meta-Analyse · vereinfacht")}
  </div>""", HEADER_JS("c20") + r"""
  fadeIn("#c20-cam", 0, 0.3);
  for (let i = 0; i < 3; i++) popIn(`#c20-p${i}`, T.ink + 0.2 + i * 0.15, 0.4);
  fadeIn("#c20-ar0", T.ink + 0.5, 0.3); fadeIn("#c20-ar1", T.ink + 0.65, 0.3);
  tl.fromTo("#c20-f0", { scaleX: 0 }, { scaleX: 1, duration: 1.2, ease: "power2.inOut" }, T.hart);
  tl.to("#c20-p0", { borderColor: "#E8C27A", duration: 0.3 }, T.hart);
  tl.fromTo("#c20-f1", { scaleX: 0 }, { scaleX: 1, duration: 1.2, ease: "none" }, T.los);
  tl.to("#c20-p1", { borderColor: "#E8C27A", duration: 0.3 }, T.los);
  fadeIn("#c20-g0", T.hinter - 0.2, 0.4); fadeIn("#c20-g1", T.hinter - 0.2, 0.4);
  tl.fromTo("#c20-g0", { rotation: 0 }, { rotation: 360, duration: 6, ease: "none", svgOrigin: "0 0", immediateRender: false }, T.hinter - 0.2);
  tl.fromTo("#c20-g1", { rotation: 0 }, { rotation: -540, duration: 6, ease: "none", svgOrigin: "0 0", immediateRender: false }, T.hinter - 0.2);
  tl.fromTo("#c20-f2", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power3.out" }, T.weiter);
  tl.fromTo("#c20-p2", { boxShadow: "0 30px 80px rgba(0,0,0,.6)" }, { boxShadow: "0 0 70px rgba(255,220,120,.7)", duration: 0.4, immediateRender: false }, T.weiter);
  tl.to(["#c20-p0", "#c20-p1", "#c20-p2", "#c20-ar0", "#c20-ar1", "#c20-g0", "#c20-g1"], { opacity: 0, duration: 0.3 }, T.studien - 0.3);
  fadeIn("#c20-bars", T.studien, 0.3); fadeIn("#c20-ft", T.studien, 0.3);
  tl.fromTo("#c20-b0", { scaleY: 0 }, { scaleY: 1, duration: 0.6, ease: "back.out(1.5)" }, T.pause);
  tl.fromTo("#c20-b1", { scaleY: 0 }, { scaleY: 1, duration: 0.5, ease: "power3.out" }, T.stur);
  fadeOut("#c20-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["ink"] + 0.2 + i * 0.15, "pop", 0.3) for i in range(3)] + [(T["weiter"], "ding", 0.45), (T["pause"], "pop", 0.4), (T["stur"], "pop", 0.3)]

# ================================================================ c21 Wallas: 4 Phasen, Dusch-Idee wird beim Abtrocknen zerknüllt
S = "v_wallas"; a = SEG[S][0]
T = dict(wallas=W("Wallas", a), vier=W("vier", a), vorb=W("Vorbereitung,", a), inku=W("Inkubation,", a), erl=W("Erleuchtung", a), ueber=W("Überprüfung.", a),
         vergessen=W("vergessen.", a), dusch=W("Dusch-Idee", a), genial=W("genial.", a), abtr=W("Abtrocknen", a))
st = ["VORBEREITUNG", "INKUBATION", "ERLEUCHTUNG", "ÜBERPRÜFUNG"]
sh = "".join(f'<div id="c21-s{i}" class="actor" style="left:{150 + i * 410}px;top:360px;width:380px;height:150px;border-radius:20px;background:#16181D;border:3px solid #3A3F48;'
             f'display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0"><div style="font-size:26px;font-weight:900;color:{AMBER};letter-spacing:.2em">PHASE {i + 1}</div>'
             f'<div class="cond" style="font-size:46px;margin-top:6px">{t}</div></div>' for i, t in enumerate(st))
put("c21", S, f"""
  <div id="c21-cam" class="lay">
    {header("c21", "GRAHAM WALLAS · 1926", "DIE 4 PHASEN")}
    {sh}
    <div id="c21-note" class="actor" style="left:700px;top:580px;width:520px;height:250px;background:#FFE680;color:#1A1A1A;padding:28px;box-shadow:0 20px 50px rgba(0,0,0,.6);transform:rotate(-3deg);opacity:0">
      <div style="font-size:28px;font-weight:900;letter-spacing:.2em;color:#7A5A00">💡 DUSCH-IDEE</div>
      <div style="margin-top:14px;font-family:'Caveat',cursive;font-size:54px;line-height:1.1">Ein Pizza-Abo<br>für Katzen!</div></div>
    <div id="c21-towel" class="actor" style="left:1300px;top:600px;font-size:150px;line-height:1;opacity:0">🧻</div>
  </div>""", HEADER_JS("c21") + r"""
  fadeIn("#c21-cam", 0, 0.3);
  [T.vorb, T.inku, T.erl, T.ueber].forEach((t, i) => tl.fromTo(`#c21-s${i}`, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, t - 0.1));
  tl.to("#c21-s3", { borderColor: "#FF4B3E", scale: 1.06, duration: 0.3, ease: "back.out(2)" }, T.vergessen - 0.3);
  tl.to(["#c21-s0", "#c21-s1", "#c21-s2"], { opacity: 0.35, duration: 0.3 }, T.vergessen - 0.3);
  tl.fromTo("#c21-note", { opacity: 0, y: 120, rotation: -12 }, { opacity: 1, y: 0, rotation: -3, duration: 0.5, ease: "back.out(1.6)" }, T.dusch - 0.2);
  tl.fromTo("#c21-towel", { opacity: 0, x: 300 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, T.abtr - 0.5);
  tl.to("#c21-note", { scale: 0.15, rotation: 220, borderRadius: 60, duration: 0.45, ease: "power3.in" }, T.abtr + 0.1);
  tl.to("#c21-note", { y: 500, opacity: 0, duration: 0.5, ease: "power2.in" }, T.abtr + 0.55);
  fadeOut("#c21-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T[k] - 0.1, "pop", 0.35) for k in ("vorb", "inku", "erl", "ueber")] + [(T["dusch"] - 0.2, "pop", 0.4), (T["abtr"] + 0.1, "click", 0.5), (T["abtr"] + 0.6, "drop", 0.35)]

# ================================================================ c22 Außenwelt ausblenden → Blitz
S = "v_ausblenden"; a = SEG[S][0]
T = dict(kurz=W("kurz", a), blitz=W("Geistesblitz", a), aussen=W("Außenwelt", a), leise=W("leise", a), idee=W("Idee", a))
dots = "".join(f'<div class="actor" style="left:{(i * 211) % 1800 + 40}px;top:{(i * 137) % 690 + 160}px;font-size:56px;opacity:.85">{["📱", "🚗", "🔔", "💬", "📺", "🐕", "🎵", "✉️"][i % 8]}</div>' for i in range(18))
put("c22", S, f"""
  <div id="c22-cam" class="lay">
    <div id="c22-world" class="lay">{dots}</div>
    <div id="c22-vig" class="actor" style="left:-1080px;top:-1260px;width:4080px;height:3600px;opacity:0;
      background:radial-gradient(circle at 50% 50%, transparent 0px, transparent 150px, rgba(0,0,0,.96) 320px)"></div>
    <div id="c22-dot" class="actor" style="left:930px;top:510px;width:60px;height:60px;border-radius:50%;background:radial-gradient(circle,#FFF6C8,#FFD43B 50%,rgba(255,212,59,0) 72%);opacity:0"></div>
    <div id="c22-fl" class="actor" style="left:0;top:132px;width:1920px;height:816px;background:#FFF6D8;opacity:0"></div>
    {bulb_html("c22-b", 860, 380)}
  </div>""", r"""
  fadeIn("#c22-cam", 0, 0.3);
  tl.fromTo("#c22-vig", { opacity: 0, scale: 3 }, { opacity: 1, scale: 1, duration: 1.4, ease: "power2.inOut" }, T.aussen - 0.3);
  tl.to("#c22-world", { opacity: 0.25, filter: "blur(6px)", duration: 1.2 }, T.aussen - 0.2);
  tl.fromTo("#c22-dot", { opacity: 0, scale: 0.3 }, { keyframes: [{ opacity: 1, scale: 1.6, duration: Math.max(0.2, T.idee - T.leise + 0.25) }, { opacity: 0, duration: 0.08 }] }, T.leise - 0.3);
  tl.fromTo("#c22-fl", { opacity: 0.85 }, { opacity: 0, duration: 0.6, ease: "power2.out", immediateRender: false }, T.idee);
  tl.fromTo("#c22-b", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }, T.idee);
  tl.fromTo("#c22-b-g", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T.idee);
  fadeOut("#c22-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["idee"], "ding", 0.7)]

# ================================================================ c23 Pause-Moment + Freeze
a = SEG["v_pause"][0]; e = SEG["pausefreeze"][1]
T = dict(pausier=W("Pausier", a), wann=W("Wann", a), was=W("was", a))
q1, n1 = typed("c23-q1", "Mein letzter Geistesblitz: ________", "left:70px;top:110px;font-family:'Caveat',cursive;font-size:56px;letter-spacing:0;font-weight:700;color:#1A1A1A;")
q2, n2 = typed("c23-q2", "Was ich da gemacht habe: ________", "left:70px;top:210px;font-family:'Caveat',cursive;font-size:56px;letter-spacing:0;font-weight:700;color:#1A1A1A;")
putr("c23", a, e, f"""
  <div id="c23-cam" class="lay">
    <div id="c23-p" class="actor" style="left:810px;top:230px;width:300px;height:320px;opacity:0;display:flex;gap:60px;justify-content:center">
      <div style="width:110px;height:320px;border-radius:18px;background:#FFF"></div><div style="width:110px;height:320px;border-radius:18px;background:#FFF"></div></div>
    <div id="c23-note" class="actor" style="left:500px;top:600px;width:920px;height:320px;background:#FFE680;box-shadow:0 20px 50px rgba(0,0,0,.6);transform:rotate(-1.5deg);opacity:0">{q1}{q2}</div>
    <div id="c23-fr" class="actor" style="left:0;top:132px;width:1920px;height:816px;background:rgba(255,255,255,.06);opacity:0"></div>
  </div>""", f'type("#c23-q1", {n1}, T.wann, 0.03); type("#c23-q2", {n2}, T.was, 0.03);' + r"""
  fadeIn("#c23-cam", 0, 0.2);
  tl.fromTo("#c23-p", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power4.in" }, T.pausier);
  tl.to("#c23-p", { y: -90, scale: 0.7, duration: 0.5, ease: "power3.inOut" }, T.wann - 0.6);
  tl.fromTo("#c23-note", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.6)" }, T.wann - 0.4);
  tl.fromTo("#c23-fr", { opacity: 0 }, { opacity: 1, duration: 0.1 }, T.end - 1.5);
  fadeOut("#c23-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["pausier"] + 0.25, "click", 0.7), (T["wann"] - 0.4, "pop", 0.35), (T["wann"], "typing", 0.25)]
