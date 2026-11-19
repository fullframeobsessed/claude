# Wird von gen.py per exec() ausgeführt: Kapitel 4 (5 Hacks), Auflösung, Ziegelstein 2, Umfrage-Auflösung, Brücke, Abspann.

chapter("c24", "kap4", 4, "DER DUSCH-HACK")

# ================================================================ c25 Gute Nachricht: nicht 3x duschen, 5 Hacks
S = "v_gut"; a = SEG[S][0]
T = dict(gute=W("gute", a), dreimal=W("dreimal", a), gezielt=W("gezielt", a), fuenf=W("fünf", a))
sh = "".join(f'<div id="c25-s{i}" class="actor" style="left:{620 + i * 240}px;top:300px;font-size:150px;line-height:1;opacity:0">🚿</div>' for i in range(3))
dots = "".join(f'<div id="c25-d{i}" class="actor" style="left:{600 + i * 150}px;top:640px;width:110px;height:110px;border-radius:50%;background:{AMBER};color:#111;'
               f'display:flex;align-items:center;justify-content:center;font-family:\'Oswald\';font-weight:700;font-size:64px;opacity:0">{i + 1}</div>' for i in range(5))
put("c25", S, f"""
  <div id="c25-cam" class="lay">
    {sh}
    <div id="c25-x" class="actor" style="left:600px;top:390px;width:720px;height:14px;background:{RED};border-radius:7px;transform:rotate(-6deg);transform-origin:0 50%;opacity:0"></div>
    <div id="c25-g" class="t cond" style="left:0;right:0;top:420px;text-align:center;font-size:90px;opacity:0">DEN DUSCH-EFFEKT<br><span style="color:{AMBER}">GEZIELT NUTZEN</span></div>
    <div id="c25-t" class="t cond" style="left:0;right:0;top:480px;text-align:center;font-size:110px;opacity:0">5 HACKS</div>
    {dots}
  </div>""", r"""
  fadeIn("#c25-cam", 0, 0.3);
  for (let i = 0; i < 3; i++) popIn(`#c25-s${i}`, T.dreimal + i * 0.12, 0.35);
  tl.fromTo("#c25-x", { opacity: 1, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.35, ease: "power3.out" }, T.dreimal + 0.9);
  tl.to(["#c25-s0", "#c25-s1", "#c25-s2", "#c25-x"], { opacity: 0, y: -60, duration: 0.3 }, T.gezielt - 0.2);
  tl.fromTo("#c25-g", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, T.gezielt);
  tl.to("#c25-g", { opacity: 0, y: -60, duration: 0.25 }, T.fuenf - 0.45);
  tl.fromTo("#c25-t", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }, T.fuenf - 0.3);
  for (let i = 0; i < 5; i++) popIn(`#c25-d${i}`, T.fuenf + i * 0.1, 0.35);
  fadeOut("#c25-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["dreimal"] + i * 0.12, "pop", 0.3) for i in range(3)] + [(T["dreimal"] + 0.9, "click", 0.5)] + [(T["fuenf"] + i * 0.1, "pop", 0.3) for i in range(0, 5, 2)]

# ================================================================ c26 Hack 1: erst füttern, dann loslassen
S = "v_hack1"; a = SEG[S][0]
T = dict(fuettern=W("füttern,", a), zwanzig=W("zwanzig", a), problem=W("Problem.", a), pause=W("Pause.", a), futter=W("Futter", a))
docs = "".join(f'<div id="c26-d{i}" class="actor" style="left:{300 + i * 90}px;top:{760 - i * 40}px;width:90px;height:115px;background:#EDE6D6;border-radius:6px;box-shadow:0 10px 30px rgba(0,0,0,.5);opacity:0">'
               f'<div style="margin:18px 12px;height:8px;background:#BDB6A6"></div><div style="margin:0 12px;height:8px;background:#BDB6A6"></div><div style="margin:12px 12px;height:8px;width:50%;background:#BDB6A6"></div></div>' for i in range(4))
put("c26", S, f"""
  <div id="c26-cam" class="lay">
    {header("c26", "HACK 1", "ERST FÜTTERN, DANN LOSLASSEN")}
    <svg id="c26-ring" class="actor" style="left:1180px;top:340px;opacity:0" width="440" height="440" viewBox="0 0 440 440">
      <circle cx="220" cy="220" r="170" fill="#111" stroke="#2A2E36" stroke-width="22"/>
      <circle id="c26-arc" cx="220" cy="220" r="170" fill="none" stroke="{ORANGE}" stroke-width="22" stroke-dasharray="1068" stroke-dashoffset="1068" transform="rotate(-90 220 220)"/></svg>
    <div id="c26-tm" class="t" style="left:1180px;width:440px;top:500px;text-align:center;font-family:'Space Mono';font-weight:700;font-size:96px;opacity:0"><span id="c26-m">0</span>:00</div>
    <div id="c26-pz" class="t" style="left:1180px;width:440px;top:470px;text-align:center;font-size:150px;opacity:0">⏸</div>
    <div id="c26-brain" class="actor" style="left:640px;top:380px;width:360px;height:280px;opacity:0">{svgbox(art.brain(0, 0, 0.9, "#9C6F80"), "-200 -180 400 330", 360, 280)}</div>
    {docs}
    <div id="c26-f" class="t cond" style="left:0;right:0;top:820px;text-align:center;font-size:64px;color:{AMBER};opacity:0">OHNE FUTTER KEIN GEISTESBLITZ</div>
  </div>""", HEADER_JS("c26") + r"""
  fadeIn("#c26-cam", 0, 0.3);
  popIn("#c26-brain", T.fuettern, 0.4);
  for (let i = 0; i < 4; i++) {
    popIn(`#c26-d${i}`, T.zwanzig - 0.3 + i * 0.12, 0.3);
    tl.to(`#c26-d${i}`, { x: 420 - i * 90, y: -300 + i * 40, scale: 0.2, opacity: 0, duration: 0.55, ease: "power3.in" }, T.problem - 1.2 + i * 0.3);
  }
  tl.to("#c26-brain", { scale: 1.08, duration: 0.15, yoyo: true, repeat: 7, ease: "sine.inOut" }, T.problem - 1.1);
  popIn("#c26-ring", T.zwanzig, 0.35); popIn("#c26-tm", T.zwanzig, 0.35);
  tl.to("#c26-arc", { attr: { "stroke-dashoffset": 0 }, duration: 1.8, ease: "power1.inOut" }, T.zwanzig + 0.2);
  tl.fromTo("#c26-m", { textContent: 0 }, { textContent: 20, duration: 1.8, ease: "power1.inOut", snap: { textContent: 1 } }, T.zwanzig + 0.2);
  tl.to("#c26-tm", { opacity: 0, duration: 0.2 }, T.pause - 0.3);
  popIn("#c26-pz", T.pause - 0.15, 0.3);
  fadeIn("#c26-f", T.futter - 0.1, 0.4);
  fadeOut("#c26-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["zwanzig"], "pop", 0.35), (T["pause"] - 0.15, "click", 0.5), (T["futter"], "pop", 0.35)]

# ================================================================ c27 Hack 2: langweilige Pause statt Handy
S = "v_hack2"; a = SEG[S][0]
T = dict(lang=W("Langweilige", a), scrollt=W("scrollt,", a), wandern=W("wandern.", a), studie=W("Studie", a), einfachen=W("einfachen,", a))
feed = "".join(f'<div style="height:96px;margin:12px 16px;border-radius:12px;background:{c}"></div>' for c in ["#3A5A8C", "#8C3A5A", "#5A8C3A", "#8C7A3A", "#3A8C82", "#6A3A8C"] * 2)
wd = "".join(f'<div id="c27-w{i}" class="actor" style="left:{540 + (i * 83) % 300}px;top:{420 + (i * 59) % 220}px;width:26px;height:26px;border-radius:50%;background:{AMBER};opacity:0"></div>' for i in range(7))
put("c27", S, f"""
  <div id="c27-cam" class="lay">
    {header("c27", "HACK 2", "LANGWEILIGE PAUSE STATT HANDY")}
    <div id="c27-bub" class="actor" style="left:420px;top:330px;width:560px;height:420px;border-radius:50%;border:5px solid rgba(255,255,255,.6);overflow:hidden;opacity:0">
      <div id="c27-feed" style="position:absolute;left:150px;top:0;width:260px">{feed}</div></div>
    {wd}
    <div id="c27-ph" class="actor" style="left:1050px;top:360px;width:200px;height:380px;border-radius:30px;background:#111;border:6px solid #444;opacity:0">
      <div style="margin:22px 14px;height:300px;border-radius:12px;background:linear-gradient(180deg,#3A5A8C,#8C3A5A)"></div></div>
    <div id="c27-x" class="t" style="left:1040px;top:420px;font-size:220px;line-height:1;color:{RED};opacity:0">✗</div>
    <div id="c27-bars" class="lay" style="opacity:0">
      <div id="c27-b0" class="actor" style="left:1180px;top:430px;width:180px;height:330px;background:{GREEN};border-radius:12px 12px 4px 4px;transform-origin:50% 100%"></div>
      <div id="c27-b1" class="actor" style="left:1440px;top:610px;width:180px;height:150px;background:#6B7280;border-radius:12px 12px 4px 4px;transform-origin:50% 100%"></div>
      <div class="t" style="left:1120px;width:300px;top:780px;text-align:center;font-size:28px;font-weight:900;line-height:1.2">EINFACHE<br>AUFGABE</div>
      <div class="t" style="left:1380px;width:300px;top:780px;text-align:center;font-size:28px;font-weight:900;line-height:1.2">ANSTRENGENDE<br>AUFGABE</div></div>
    {foot("c27", "Baird et al. (2012), Psychological Science · vereinfacht")}
  </div>""", HEADER_JS("c27") + r"""
  fadeIn("#c27-cam", 0, 0.3);
  popIn("#c27-bub", T.lang, 0.45);
  popIn("#c27-ph", T.scrollt - 0.5, 0.35);
  tl.fromTo("#c27-feed", { y: 420 }, { y: -900, duration: 3.2, ease: "power1.inOut" }, T.scrollt - 0.2);
  popIn("#c27-x", T.wandern - 0.2, 0.3);
  tl.to(["#c27-ph", "#c27-x", "#c27-feed"], { opacity: 0, duration: 0.3 }, T.wandern + 0.6);
  for (let i = 0; i < 7; i++) { popIn(`#c27-w${i}`, T.wandern + 0.7 + i * 0.1, 0.3); tl.to(`#c27-w${i}`, { x: ((i * 37) % 80) - 40, y: ((i * 53) % 70) - 35, duration: 2.5, yoyo: true, repeat: 2, ease: "sine.inOut" }, T.wandern + 1.0); }
  fadeIn("#c27-bars", T.studie, 0.3); fadeIn("#c27-ft", T.studie, 0.3);
  tl.fromTo("#c27-b0", { scaleY: 0 }, { scaleY: 1, duration: 0.6, ease: "back.out(1.5)" }, T.einfachen);
  tl.fromTo("#c27-b1", { scaleY: 0 }, { scaleY: 1, duration: 0.5, ease: "power3.out" }, T.einfachen + 0.3);
  fadeOut("#c27-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["lang"], "pop", 0.35), (T["wandern"] - 0.2, "click", 0.6), (T["einfachen"], "pop", 0.4)]

# ================================================================ c28 Hack 3: beweg dich (Stanford)
S = "v_hack3"; a = SEG[S][0]
T = dict(beweg=W("Beweg", a), stanford=W("Stanford", a), gehen=W("Gehen", a), sitzen=W("Sitzen.", a))
steps = "".join(f'<div id="c28-f{i}" class="actor" style="left:{250 + (i % 2) * 70}px;top:{830 - i * 45}px;font-size:48px;opacity:0">👣</div>' for i in range(11))
put("c28", S, f"""
  <div id="c28-cam" class="lay">
    {header("c28", "HACK 3", "BEWEG DICH")}
    {steps}
    <div id="c28-b0" class="actor" style="left:700px;top:620px;width:220px;height:140px;background:#6B7280;border-radius:12px 12px 4px 4px;transform-origin:50% 100%;opacity:0"></div>
    <div id="c28-b1" class="actor" style="left:1000px;top:370px;width:220px;height:390px;background:{GREEN};border-radius:12px 12px 4px 4px;transform-origin:50% 100%;opacity:0"></div>
    <div class="t" style="left:640px;width:340px;top:770px;text-align:center;font-size:34px;font-weight:900">🪑 SITZEN</div>
    <div class="t" style="left:940px;width:340px;top:770px;text-align:center;font-size:34px;font-weight:900">🚶 GEHEN</div>
    <div id="c28-l" class="t" style="left:940px;width:340px;top:300px;text-align:center;font-size:30px;font-weight:900;color:{GREEN};opacity:0">DEUTLICH MEHR IDEEN</div>
    {foot("c28", "Oppezzo &amp; Schwartz (2014), Stanford University")}
  </div>""", HEADER_JS("c28") + r"""
  fadeIn("#c28-cam", 0, 0.3);
  for (let i = 0; i < 11; i++) tl.fromTo(`#c28-f${i}`, { opacity: 0 }, { opacity: 0.6, duration: 0.15 }, T.beweg + i * 0.18);
  fadeIn("#c28-ft", T.stanford, 0.3);
  tl.fromTo("#c28-b1", { opacity: 1, scaleY: 0 }, { opacity: 1, scaleY: 1, duration: 0.7, ease: "back.out(1.5)" }, T.gehen - 0.1);
  tl.fromTo("#c28-b0", { opacity: 1, scaleY: 0 }, { opacity: 1, scaleY: 1, duration: 0.5, ease: "power3.out" }, T.sitzen - 0.2);
  popIn("#c28-l", T.gehen + 0.5, 0.35);
  fadeOut("#c28-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["gehen"] - 0.1, "pop", 0.4), (T["sitzen"] - 0.2, "pop", 0.3)]

# ================================================================ c29 Hack 4: Ideen-Fänger
S = "v_hack4"; a = SEG[S][0]
T = dict(faenger=W("Ideen-Fänger.", a), zettel=W("Zettel", a), sprach=W("Sprachnotiz", a), wasser=W("wasserfeste", a))
wave = "".join(f'<div id="c29-wv{i}" style="display:inline-block;width:12px;height:{30 + (i * 37) % 70}px;margin:0 4px;border-radius:6px;background:{AMBER};vertical-align:middle;transform-origin:50% 50%"></div>' for i in range(12))
cards = [("📝", "ZETTEL AM BETT", ""), ("🎙️", "SPRACHNOTIZ", f'<div style="margin-top:14px;height:100px;display:flex;align-items:center;justify-content:center">{wave}</div>'),
         ("🚿", "WASSERFESTER BLOCK", "")]
ch = "".join(f'<div id="c29-c{i}" class="actor card" style="left:{170 + i * 560}px;top:340px;width:500px;height:440px;opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center">'
             f'<div style="font-size:140px;line-height:1">{em}</div><div class="cond" style="margin-top:20px;font-size:48px">{t}</div>{extra}</div>' for i, (em, t, extra) in enumerate(cards))
put("c29", S, f"""
  <div id="c29-cam" class="lay">
    {header("c29", "HACK 4", "DER IDEEN-FÄNGER")}
    {ch}
  </div>""", HEADER_JS("c29") + r"""
  fadeIn("#c29-cam", 0, 0.3);
  [T.zettel, T.sprach, T.wasser].forEach((t, i) => tl.fromTo(`#c29-c${i}`, { opacity: 0, y: 100, rotation: (i - 1) * 6 }, { opacity: 1, y: 0, rotation: (i - 1) * 2, duration: 0.45, ease: "back.out(1.6)" }, t - 0.2));
  for (let i = 0; i < 12; i++) tl.fromTo(`#c29-wv${i}`, { scaleY: 0.3 }, { scaleY: 1, duration: 0.25, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }, T.sprach + i * 0.04);
  fadeOut("#c29-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T[k] - 0.2, "pop", 0.4) for k in ("zettel", "sprach", "wasser")]

# ================================================================ c30 Hack 5: Schlaf drüber (Nature 2004)
S = "v_hack5"; a = SEG[S][0]
T = dict(schlaf=W("Schlaf", a), nature=W("Nature", a), zahlen=W("Zahlenaufgaben", a), versteckte=W("versteckte", a), geschlafen=W("geschlafen", a),
         doppelt=W("doppelt", a), wach=W("wach", a))
put("c30", S, f"""
  <div id="c30-cam" class="lay">
    {header("c30", "HACK 5", "SCHLAF DRÜBER")}
    <div id="c30-moon" class="actor" style="left:1500px;top:150px;font-size:180px;line-height:1;opacity:0">🌙</div>
    <div id="c30-row" class="t" style="left:130px;top:380px;font-family:'Space Mono';font-weight:700;font-size:64px;letter-spacing:.2em;opacity:0">
      1 1 4 4 9 <span id="c30-hid" style="border-radius:10px;padding:0 8px">9</span> 1 4 …</div>
    <div id="c30-hl" class="t" style="left:130px;top:470px;font-size:30px;font-weight:900;letter-spacing:.14em;color:{GREEN};opacity:0">↑ VERSTECKTE ABKÜRZUNG</div>
    <div id="c30-bars" class="lay" style="opacity:0">
      <div id="c30-b0" class="actor" style="left:640px;top:616px;width:240px;height:124px;background:#6B7280;border-radius:12px 12px 4px 4px;transform-origin:50% 100%;transform:scaleY(0)"></div>
      <div id="c30-b1" class="actor" style="left:1040px;top:420px;width:240px;height:320px;background:{GREEN};border-radius:12px 12px 4px 4px;transform-origin:50% 100%;transform:scaleY(0)"></div>
      <div class="t" style="left:580px;width:360px;top:760px;text-align:center;font-size:34px;font-weight:900">☀️ WACH</div>
      <div class="t" style="left:980px;width:360px;top:760px;text-align:center;font-size:34px;font-weight:900">🌙 GESCHLAFEN</div>
      <div id="c30-v0" class="t" style="left:580px;width:360px;top:540px;text-align:center;font-family:'Space Mono';font-weight:700;font-size:64px;opacity:0"><span id="c30-n0">0</span>%</div>
      <div id="c30-v1" class="t" style="left:980px;width:360px;top:345px;text-align:center;font-family:'Space Mono';font-weight:700;font-size:64px;color:{GREEN};opacity:0"><span id="c30-n1">0</span>%</div></div>
    {foot("c30", "Wagner et al. (2004), Nature")}
  </div>""", HEADER_JS("c30") + r"""
  fadeIn("#c30-cam", 0, 0.3);
  tl.fromTo("#c30-moon", { opacity: 0, y: -80, rotation: -30 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "back.out(1.6)" }, T.schlaf);
  fadeIn("#c30-ft", T.nature, 0.3);
  tl.fromTo("#c30-row", { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }, T.zahlen - 0.2);
  tl.to("#c30-hid", { backgroundColor: "rgba(124,255,138,.35)", duration: 0.3 }, T.versteckte);
  fadeIn("#c30-hl", T.versteckte + 0.1, 0.3);
  tl.to(["#c30-row", "#c30-hl"], { opacity: 0.3, duration: 0.3 }, T.geschlafen - 0.6);
  fadeIn("#c30-bars", T.geschlafen - 0.5, 0.3);
  tl.fromTo("#c30-b1", { scaleY: 0 }, { scaleY: 1, duration: 0.8, ease: "back.out(1.4)" }, T.geschlafen - 0.2);
  fadeIn("#c30-v1", T.geschlafen + 0.2, 0.3);
  tl.fromTo("#c30-n1", { textContent: 0 }, { textContent: 59, duration: 0.8, ease: "power2.out", snap: { textContent: 1 } }, T.geschlafen - 0.2);
  tl.fromTo("#c30-b0", { scaleY: 0 }, { scaleY: 1, duration: 0.6, ease: "power3.out" }, T.wach - 0.3);
  fadeIn("#c30-v0", T.wach, 0.3);
  tl.fromTo("#c30-n0", { textContent: 0 }, { textContent: 23, duration: 0.6, ease: "power2.out", snap: { textContent: 1 } }, T.wach - 0.3);
  fadeOut("#c30-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["schlaf"], "pop", 0.35), (T["versteckte"], "click", 0.45), (T["geschlafen"] - 0.2, "pop", 0.45), (T["wach"] - 0.3, "pop", 0.3)]

# ================================================================ c31 Auflösung: 20 Min., Runde um den Block, Ampel, Notizbuch
S = "v_aufl"; a = SEG[S][0]
T = dict(ausprobiert=W("ausprobiert.", a), zwanzig=W("Zwanzig", a), runde=W("Runde", a), handy=W("Handy.", a), ampel=W("Ampel.", a), notiz=W("Notizbuch", a))
route = "M400,820 L400,360 L1100,360 L1100,820 Z"
put("c31", S, f"""
  <div id="c31-cam" class="lay">
    {otto_at("c31", 1300, ("tired", "aha", "happy"), top=180, s=0.95)}
    <div id="c31-tm" class="actor" style="left:140px;top:170px;padding:10px 24px;background:#111;border:3px solid #333;border-radius:14px;font-family:'Space Mono';font-weight:700;font-size:56px;color:{AMBER};opacity:0">20:00 ✓</div>
    <svg class="actor" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
      <path id="c31-rt" d="{route}" fill="none" stroke="{AMBER}" stroke-width="8" stroke-dasharray="2400" stroke-dashoffset="2400" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <div id="c31-home" class="actor" style="left:350px;top:780px;font-size:80px;opacity:0">🏠</div>
    <div id="c31-nophone" class="actor" style="left:560px;top:540px;font-size:44px;font-weight:900;color:{MUTED};opacity:0">📵 OHNE HANDY</div>
    <div id="c31-tl" class="actor" style="left:1060px;top:240px;width:80px;height:220px;border-radius:20px;background:#1A1A1A;border:4px solid #333;opacity:0">
      <div id="c31-r" style="margin:12px auto;width:52px;height:52px;border-radius:50%;background:#FF3B30"></div>
      <div style="margin:0 auto;width:52px;height:52px;border-radius:50%;background:#3A2A00"></div>
      <div id="c31-g" style="margin:12px auto;width:52px;height:52px;border-radius:50%;background:#123A1A"></div></div>
    {bulb_html("c31-b", 1100, 160, 0.7)}
    <div id="c31-nb" class="actor" style="left:640px;top:520px;font-size:130px;opacity:0">📓</div>
    <div id="c31-ok" data-layout-allow-overlap class="actor" style="left:810px;top:520px;font-size:90px;color:{GREEN};opacity:0">✓</div>
  </div>""", r"""
  fadeIn("#c31-cam", 0, 0.3);
  popIn("#c31-tm", T.zwanzig, 0.35);
  popIn("#c31-home", T.runde - 0.3, 0.3);
  tl.to("#c31-rt", { attr: { "stroke-dashoffset": 600 }, duration: 2.4, ease: "power1.inOut" }, T.runde);
  fadeIn("#c31-nophone", T.handy - 0.2, 0.3);
  popIn("#c31-tl", T.ampel - 0.9, 0.3);
  tl.set("#c31-r", { backgroundColor: "#3A1210" }, T.ampel); tl.set("#c31-g", { backgroundColor: "#34C759", boxShadow: "0 0 30px #34C759" }, T.ampel);
  tl.fromTo("#c31-b", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }, T.ampel + 0.1);
  tl.fromTo("#c31-b-g", { opacity: 0 }, { opacity: 1, duration: 0.3 }, T.ampel + 0.1);
  face("c31o", "tired", "aha", T.ampel + 0.1);
  tl.to("#c31-nophone", { opacity: 0, duration: 0.2 }, T.notiz - 0.6);
  tl.fromTo("#c31-nb", { opacity: 0, y: 80, rotation: -10 }, { opacity: 1, y: 0, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }, T.notiz - 0.3);
  popIn("#c31-ok", T.notiz + 0.2, 0.3);
  face("c31o", "aha", "happy", T.notiz + 0.2);
  fadeOut("#c31-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["zwanzig"], "pop", 0.35), (T["ampel"] + 0.1, "ding", 0.55), (T["notiz"] - 0.3, "pop", 0.4), (T["notiz"] + 0.2, "click", 0.5)]

# ================================================================ c32 Ziegelstein 2: ungewöhnliche Ideen + Kommentar
S = "v_ziegel2"; a = SEG[S][0]
T = dict(ziegel=W("Ziegelstein.", a), mehr=W("mehr", a), schreib=W("Schreib", a), komm=W("Kommentare.", a))
odd = [("🏋️ HANTEL", 200, 230), ("🎨 KUNSTWERK", 1380, 230), ("📄 BRIEFBESCHWERER", 150, 690), ("🌰 NUSSKNACKER", 1330, 690), ("🪴 BLUMENTOPF", 760, 230), ("🛏️ BETTERHÖHUNG", 740, 760)]
oh = "".join(chip(f"c32-o{i}", x, y, t, size=36) for i, (t, x, y) in enumerate(odd))
put("c32", S, f"""
  <div id="c32-cam" class="lay">
    {light("c32-l", 960, 520, 520, "rgba(255,226,180,.18)")}
    <div id="c32-brick" class="actor" style="left:750px;top:440px;width:420px;height:160px;opacity:0">{BRICK}</div>
    {oh}
    <div id="c32-cm" class="actor card" style="left:560px;top:620px;width:800px;height:130px;display:flex;align-items:center;gap:20px;padding:0 30px;opacity:0">
      <span style="font-size:52px">💬</span><span style="font-size:36px;font-weight:700;color:{MUTED}">Meine verrückteste Idee …</span>
      <span id="c32-btn" style="margin-left:auto;padding:12px 22px;border-radius:12px;background:#2D6CDF;font-size:28px;font-weight:900">KOMMENTIEREN</span></div>
    {cursor("c32", 1500, 860)}
  </div>""", r"""
  fadeIn("#c32-cam", 0, 0.3);
  tl.fromTo("#c32-brick", { opacity: 0, y: -160, rotation: -30 }, { opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "bounce.out" }, 0.1);
  for (let i = 0; i < 6; i++) popIn(`#c32-o${i}`, T.mehr - 0.2 + i * 0.22, 0.35);
  tl.to(["#c32-o2", "#c32-o3", "#c32-o5"], { opacity: 0.2, duration: 0.3 }, T.schreib - 0.4);
  tl.fromTo("#c32-cm", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.6)" }, T.schreib - 0.2);
  fadeIn("#c32-cur", T.schreib, 0.2);
  move("#c32-cur", -230, -250, T.schreib + 0.1, 0.6);
  click("c32", T.komm);
  fadeOut("#c32-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(0.1 + a + 0.3, "drop", 0.35)] + [(T["mehr"] - 0.2 + i * 0.22, "pop", 0.3) for i in range(6)] + [(T["komm"], "click", 0.8)]

# ================================================================ c33 Umfrage-Auflösung: alle drei Orte → Kopf darf wandern
S = "v_umfrage2"; a = SEG[S][0]
T = dict(verrat=W("verrat", a), A=W("A,", a), B=W("B", a), C=W("C,", a), gemeinsam=W("gemeinsam.", a), wandern=W("wandern.", a), schlaf=W("Schlaf", a))
put("c33", S, f"""
  <div id="c33-cam" class="lay">
    {light("c33-l", 960, 500, 760, "rgba(255,226,180,.14)")}
    <div id="c33-card" class="actor card" style="left:400px;top:190px;width:1120px;height:620px;opacity:0">
      <div class="t" style="left:60px;top:50px;font-size:28px;font-weight:800;letter-spacing:.4em;color:{AMBER}">UMFRAGE · AUFLÖSUNG</div>
      <div class="t" style="left:60px;top:120px;font-size:44px;font-weight:700">Wo kommen dir die besten Ideen?</div>
      {poll_opts("c33")}</div>
    <div id="c33-moon" class="actor" style="left:1440px;top:430px;font-size:110px;opacity:0">🌙</div>
  </div>""", r"""
  fadeIn("#c33-cam", 0, 0.3);
  tl.fromTo("#c33-card", { opacity: 0, y: 80, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power4.out" }, T.verrat - 0.2);
  [T.A, T.B, T.C].forEach((t, i) => tl.fromTo(`#c33-o${i}`, { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.6)" }, t - 0.1));
  for (let i = 0; i < 3; i++) { tl.to(`#c33-o${i}`, { borderColor: "#7CFF8A", duration: 0.2 }, T.wandern - 0.3 + i * 0.15); tl.fromTo(`#c33-tg${i}`, { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }, T.wandern - 0.3 + i * 0.15); }
  tl.to("#c33-o2", { scale: 1.04, backgroundColor: "#24301F", duration: 0.3 }, T.schlaf - 0.2);
  tl.fromTo("#c33-moon", { opacity: 0, scale: 0.3, rotation: -40 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2)" }, T.schlaf - 0.2);
  fadeOut("#c33-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["verrat"] - 0.2, "pop", 0.3)] + [(T[k] - 0.1, "pop", 0.45) for k in ("A", "B", "C")] + [(T["wandern"] - 0.3 + i * 0.15, "click", 0.35) for i in range(3)] + [(T["schlaf"] - 0.2, "pop", 0.4)]

# ================================================================ c34 Brücke: Handy vibriert → nächste Folge
S = "v_bruecke"; a = SEG[S][0]
T = dict(greifst=W("greifst", a), handy=W("Handy?", a), fuenf=W("fünf", a), naechstes=W("nächstes", a))
put("c34", S, f"""
  <div id="c34-cam" class="lay">
    {otto_at("c34", 260, ("tired", "shock"), top=200, s=0.9)}
    <div id="c34-ph" class="actor" style="left:1000px;top:250px;width:240px;height:440px;border-radius:34px;background:#111;border:6px solid #444;opacity:0">
      <div style="margin:26px 16px;height:360px;border-radius:14px;background:linear-gradient(180deg,#2A2E36,#16181D);display:flex;align-items:flex-start;justify-content:center;padding-top:30px">
        <div id="c34-n" style="width:196px;padding:14px;border-radius:14px;background:#F4F6FA;color:#1A1A1A;font-size:28px;line-height:1.15;font-weight:800;opacity:0">🔔 1 neue Nachricht</div></div></div>
    <div id="c34-k" class="t" style="left:0;right:0;top:760px;text-align:center;font-size:30px;font-weight:800;letter-spacing:.4em;color:{MUTED};opacity:0">NÄCHSTE FOLGE</div>
    <div id="c34-t" class="t cond" style="left:0;right:0;top:810px;text-align:center;font-size:84px;opacity:0">SCHON WIEDER AM HANDY?</div>
  </div>""", r"""
  fadeIn("#c34-cam", 0, 0.3);
  popIn("#c34-ph", T.greifst - 0.4, 0.35);
  tl.fromTo("#c34-n", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, T.greifst);
  tl.fromTo("#c34-ph", { rotation: 0 }, { keyframes: [...Array(12)].map((_, i) => ({ rotation: i % 2 ? 4 : -4, duration: 0.04 })).concat([{ rotation: 0, duration: 0.05 }]), immediateRender: false }, T.greifst);
  tl.fromTo("#c34-ph", { rotation: 0 }, { keyframes: [...Array(12)].map((_, i) => ({ rotation: i % 2 ? 4 : -4, duration: 0.04 })).concat([{ rotation: 0, duration: 0.05 }]), immediateRender: false }, T.fuenf);
  face("c34o", "tired", "shock", T.handy - 0.2);
  tl.to("#c34-otto", { x: 140, duration: 0.35, ease: "power3.out" }, T.handy - 0.1);
  fadeIn("#c34-k", T.naechstes - 0.3, 0.4);
  tl.fromTo("#c34-t", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, T.naechstes);
  fadeOut("#c34-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["greifst"] + i * 0.08, "click", 0.3) for i in range(5)] + [(T["fuenf"] + i * 0.08, "click", 0.3) for i in range(5)] + [(T["naechstes"], "pop", 0.4)]

# ================================================================ c35 Abspann (Platzhalter für YouTube-Endbildschirm)
put("c35", "endcard", f"""
  <div id="c35-ch" class="t cond" style="left:0;right:0;top:190px;text-align:center;font-size:70px;letter-spacing:.3em;opacity:0">OTTO NORMALPSYCHE</div>
  <div id="c35-sub" class="t" style="left:0;right:0;top:285px;text-align:center;font-size:28px;font-weight:600;letter-spacing:.4em;color:{MUTED};opacity:0">WARUM WIR TUN, WAS WIR TUN</div>
  <div id="c35-sb" class="actor" style="left:300px;top:420px;width:300px;height:300px;border-radius:50%;border:2px dashed #555;opacity:0"></div>
  <div id="c35-sbt" class="t" style="left:300px;width:300px;top:740px;text-align:center;font-size:28px;font-weight:700;letter-spacing:.3em;opacity:0">ABONNIEREN</div>
  <div id="c35-nv" class="actor" style="left:900px;top:400px;width:720px;height:405px;border:2px dashed #555;opacity:0"></div>
  <div id="c35-nt" class="t" style="left:900px;top:350px;font-size:28px;font-weight:700;letter-spacing:.4em;color:{AMBER};opacity:0">WEITERSCHAUEN</div>""", r"""
  fadeIn("#c35-ch", 0.3, 0.8); fadeIn("#c35-sub", 0.8, 0.6);
  ["#c35-sb", "#c35-sbt", "#c35-nv", "#c35-nt"].forEach((s, i) => fadeIn(s, 1.2 + i * 0.15, 0.6));
""", {})
SFX += [(SEG["endcard"][0] + 0.3, "pop", 0.25)]
