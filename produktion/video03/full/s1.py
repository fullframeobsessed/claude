# Wird von gen.py per exec() ausgeführt: Kaltstart, Hook, Frage, Umfrage, Titel, Kapitel 1.
import math as _m

# ================================================================ c0 Kaltstart: Tropfen, Ringe, Glühbirne
a, e = SEG["open"]
put("c0", "open", f"""
  <div id="c0-cam" class="lay">
    <div id="c0-drop" class="actor" style="left:935px;top:160px;width:50px;height:70px;border-radius:50% 50% 50% 50% / 60% 60% 40% 40%;background:{WATER};box-shadow:0 0 30px rgba(142,197,255,.6);opacity:0"></div>
    <div id="c0-r0" class="actor" style="left:810px;top:690px;width:300px;height:70px;border-radius:50%;border:4px solid {WATER};opacity:0"></div>
    <div id="c0-r1" class="actor" style="left:810px;top:690px;width:300px;height:70px;border-radius:50%;border:3px solid {WATER};opacity:0"></div>
    {bulb_html("c0-b", 860, 330)}
  </div>""", r"""
  tl.fromTo("#c0-drop", { opacity: 1, y: 0 }, { opacity: 1, y: 520, duration: 0.9, ease: "power2.in" }, 0.1);
  tl.to("#c0-drop", { opacity: 0, scaleY: 0.3, duration: 0.08 }, 1.0);
  [0, 1].forEach(i => tl.fromTo(`#c0-r${i}`, { opacity: 0.9, scale: 0.2 }, { opacity: 0, scale: 1.6 + i * 0.6, duration: 1.2, ease: "power2.out" }, 1.0 + i * 0.18));
  tl.fromTo("#c0-b", { opacity: 0 }, { keyframes: [{ opacity: 0.6, duration: 0.05 }, { opacity: 0.1, duration: 0.08 }, { opacity: 0.8, duration: 0.05 }, { opacity: 0.2, duration: 0.1 }, { opacity: 1, duration: 0.05 }] }, 1.7);
  tl.fromTo("#c0-b-g", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 2.05);
  fadeOut("#c0-cam", T.end - 0.25, 0.25);
""", {})
SFX += [(a + 1.0, "drop", 0.5), (a + 2.05, "ding", 0.55)]

# ================================================================ c1 Hook: leeres Dokument, Uhr rast, NICHTS
S = "v_hook"; a = SEG[S][0]
T = dict(otto=W("Otto.", a), zwei=W("zwei", a), leeren=W("leeren", a), idee=W("Idee", a), nichts=W("Nichts.", a), absolut=W("Absolut", a))
put("c1", S, f"""
  <div id="c1-cam" class="lay">
    {otto_at("c1", 180, ("tired", "sad"))}
    <div id="c1-doc" class="actor card" style="left:860px;top:200px;width:880px;height:560px;opacity:0">
      <div style="height:70px;border-bottom:2px solid #3A3F48;display:flex;align-items:center;gap:16px;padding:0 26px;font-size:28px;font-weight:700;color:{MUTED}">
        <span style="width:16px;height:16px;border-radius:50%;background:#FF5F57"></span><span style="width:16px;height:16px;border-radius:50%;background:#FEBC2E"></span>
        <span style="width:16px;height:16px;border-radius:50%;background:#28C840"></span><span style="margin-left:14px">Präsentation_Ideen.docx</span></div>
      <div style="position:absolute;left:70px;top:120px;width:740px;height:370px;background:#F4F5F7;border-radius:6px"></div>
      <div id="c1-cur" class="actor" style="left:100px;top:150px;width:5px;height:50px;background:#111"></div>
      <div class="t" style="right:30px;bottom:20px;font-size:28px;font-weight:700;color:{MUTED}">0 Wörter</div></div>
    <div id="c1-clk" class="actor" style="left:1430px;top:160px;padding:8px 22px;background:#111;border:3px solid #333;border-radius:14px;font-family:'Space Mono';font-weight:700;font-size:56px;color:#FF5A4A;opacity:0">
      <span id="c1-txt">14:00</span></div>
    <div id="c1-n" class="t cond" style="left:860px;width:880px;top:360px;text-align:center;font-size:170px;color:{RED};opacity:0">NICHTS.</div>
  </div>""", r"""
  fadeIn("#c1-cam", 0, 0.4);
  tl.fromTo("#c1-doc", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, T.leeren - 0.6);
  for (let i = 0; i < 9; i++) tl.fromTo("#c1-cur", { opacity: 1 }, { opacity: 0, duration: 0.01, immediateRender: false }, T.leeren + 0.4 + i * 0.5).fromTo("#c1-cur", { opacity: 0 }, { opacity: 1, duration: 0.01, immediateRender: false }, T.leeren + 0.65 + i * 0.5);
  popIn("#c1-clk", T.zwei - 0.2, 0.35);
  for (let k = 1; k <= 16; k++) { const mm = Math.round(k * 7.5); tl.set("#c1-txt", { textContent: `${14 + Math.floor(mm / 60)}:${String(mm % 60).padStart(2, "0")}` }, T.zwei + k * 0.1); }
  face("c1o", "tired", "sad", T.nichts - 0.2);
  tl.to("#c1-doc", { opacity: 0.25, duration: 0.3 }, T.nichts - 0.1);
  slam("#c1-n", T.nichts, 2.4);
  shake("#c1-cam", T.absolut, 12);
  fadeOut("#c1-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["leeren"] - 0.5, "pop", 0.4), (T["zwei"], "tick", 0.35), (T["nichts"] + 0.2, "boom", 0.5)]

# ================================================================ c2 Dusche: Schaum, Glühbirne, kein Stift / kein Handy
S = "v_dusche"; a = SEG[S][0]
T = dict(duschen=W("duschen.", a), shampoo=W("Shampoo:", a), perfekte=W("perfekte", a), stift=W("Stift.", a), handy=W("Handy.", a), schaum=W("Schaum.", a))
streams = "".join(f'<div class="actor" style="left:{300 + i * 26}px;top:215px;width:4px;height:700px;background:repeating-linear-gradient(180deg,rgba(142,197,255,.0) 0 20px,rgba(142,197,255,.45) 20px 60px);"></div>' for i in range(14))
foam = "".join(f'<div class="actor" style="left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;background:#F4F6FA;border:3px solid #CFD6E0"></div>'
               for x, y, r in [(170, 70, 100), (240, 30, 120), (330, 25, 120), (420, 55, 100), (470, 105, 70), (145, 120, 70), (410, 125, 60)])
icons = [("✏️", "KEIN STIFT", "stift"), ("📱", "KEIN HANDY", "handy"), ("🫧", "NUR SCHAUM", "schaum")]
ih = "".join(f'<div id="c2-i{i}" class="actor card" style="left:{1060 + i * 260}px;top:610px;width:230px;height:230px;opacity:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px">'
             f'<div style="font-size:100px;line-height:1">{em}</div><div style="font-size:28px;font-weight:800;letter-spacing:.03em">{lab}</div>'
             + (f'<div id="c2-x{i}" style="position:absolute;inset:0;opacity:0"><svg viewBox="0 0 230 230" width="230" height="230"><path d="M40,40 L190,190 M190,40 L40,190" stroke="{RED}" stroke-width="14" stroke-linecap="round"/></svg></div>' if i < 2 else "")
             + '</div>' for i, (em, lab, _) in enumerate(icons))
put("c2", S, f"""
  <div id="c2-fog" class="actor" style="left:0;top:132px;width:1920px;height:816px;background:linear-gradient(90deg,rgba(220,230,240,.0),rgba(220,230,240,.55),rgba(220,230,240,.0));filter:blur(30px);opacity:0"></div>
  <div id="c2-cam" class="lay" style="opacity:0">
    {light("c2-l", 470, 400, 520, "rgba(142,197,255,.20)")}
    <div class="actor" style="left:330px;top:180px;width:300px;height:36px;border-radius:18px;background:#9AA0AA"></div>
    <div class="actor" style="left:460px;top:150px;width:40px;height:34px;background:#7A808A"></div>
    <div id="c2-water" class="lay">{streams}</div>
    <div class="actor" style="left:170px;top:225px;width:600px;height:760px">
      <div style="position:absolute;left:0;top:0;width:600px;height:760px">{otto_svg("c2o", ("tired", "aha"))}</div>
      <div id="c2-foam" style="position:absolute;inset:0;opacity:0">{foam}</div></div>
    {bulb_html("c2-b", 700, 190, 0.8)}
    {ih}
  </div>""", r"""
  tl.fromTo("#c2-fog", { opacity: 0, x: -1400 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.inOut" }, T.duschen - 0.5);
  tl.to("#c2-fog", { opacity: 0, x: 1400, duration: 0.6, ease: "power2.inOut" }, T.duschen + 0.1);
  fadeIn("#c2-cam", T.duschen, 0.4);
  tl.fromTo("#c2-water", { y: -40 }, { y: 0, duration: 0.5, ease: "none", repeat: 18, immediateRender: false }, T.duschen);
  tl.fromTo("#c2-foam", { opacity: 0, scale: 0.6, transformOrigin: "50% 25%" }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, T.shampoo - 0.3);
  face("c2o", "tired", "aha", T.perfekte);
  tl.fromTo("#c2-b", { opacity: 0, scale: 0.3, y: 40 }, { opacity: 1, scale: 1, y: 0, duration: 0.45, ease: "back.out(2.5)" }, T.perfekte);
  tl.fromTo("#c2-b-g", { opacity: 0 }, { opacity: 1, duration: 0.4 }, T.perfekte + 0.1);
  [T.stift, T.handy, T.schaum].forEach((t, i) => { popIn(`#c2-i${i}`, t - 0.15, 0.35); if (i < 2) tl.fromTo(`#c2-x${i}`, { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power3.in" }, t + 0.25); });
  fadeOut("#c2-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["perfekte"], "ding", 0.6), (T["stift"] - 0.15, "pop", 0.4), (T["stift"] + 0.25, "click", 0.5), (T["handy"] - 0.15, "pop", 0.4),
        (T["handy"] + 0.25, "click", 0.5), (T["schaum"] - 0.15, "pop", 0.45)]

# ================================================================ c3 Frage: Schreibtisch vs. Dusche
S = "v_frage"; a = SEG[S][0]
T = dict(warum=W("Warum", a), beste=W("beste", a), genau=W("genau", a), suchst=W("suchst?", a))
put("c3", S, f"""
  <div id="c3-cam" class="lay">
    <div id="c3-a" class="actor card" style="left:260px;top:220px;width:620px;height:560px;opacity:0">
      <div style="position:absolute;left:0;right:0;top:70px;text-align:center;font-size:140px">💻</div>
      <div class="t cond" style="left:0;right:0;top:300px;text-align:center;font-size:84px">SCHREIBTISCH</div>
      <div class="t" style="left:0;right:0;top:420px;text-align:center;font-size:44px;font-weight:900;color:{MUTED}">0 IDEEN</div></div>
    <div id="c3-b" class="actor card" style="left:1040px;top:220px;width:620px;height:560px;opacity:0">
      {light("c3-g", 310, 160, 220, "rgba(255,220,120,.5)", 0)}
      <div style="position:absolute;left:0;right:0;top:70px;text-align:center;font-size:140px">🚿</div>
      <div class="t cond" style="left:0;right:0;top:300px;text-align:center;font-size:84px">DUSCHE</div>
      <div class="t" style="left:0;right:0;top:420px;text-align:center;font-size:44px;font-weight:900;color:{AMBER}">1 GENIE-IDEE 💡</div></div>
    {cursor("c3", 900, 860)}
  </div>""", r"""
  fadeIn("#c3-cam", 0, 0.3);
  tl.fromTo("#c3-a", { opacity: 0, x: -300, rotation: -6 }, { opacity: 1, x: 0, rotation: -2, duration: 0.6, ease: "power4.out" }, 0.05);
  tl.fromTo("#c3-b", { opacity: 0, x: 300, rotation: 6 }, { opacity: 1, x: 0, rotation: 2, duration: 0.6, ease: "power4.out" }, T.beste - 0.2);
  fadeIn("#c3-cur", 0.3, 0.2);
  move("#c3-cur", -340, -330, 0.4, 0.7);
  move("#c3-cur", 450, -330, T.genau - 0.2, 0.7);
  tl.to("#c3-a", { opacity: 0.4, scale: 0.96, duration: 0.3 }, T.genau + 0.3);
  tl.to("#c3-b", { scale: 1.05, duration: 0.3, ease: "back.out(2)" }, T.genau + 0.4);
  tl.fromTo("#c3-g", { opacity: 0 }, { opacity: 1, duration: 0.4 }, T.genau + 0.4);
  click("c3", T.suchst - 0.2);
  fadeOut("#c3-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["beste"] - 0.2, "pop", 0.35), (T["suchst"] - 0.2, "click", 0.7)]

# ================================================================ c4 Umfrage A/B/C
S = "v_poll"; a = SEG[S][0]
POLL_OPTS = [("A", "🚿", "Unter der Dusche"), ("B", "🚶", "Beim Spazierengehen"), ("C", "🛏️", "Kurz vorm Einschlafen")]


def poll_opts(cid):
    return "".join(f'<div id="{cid}-o{i}" class="actor" style="left:60px;top:{220 + i * 120}px;width:1000px;height:96px;border-radius:16px;background:#22262E;'
                   f'border:2px solid #3A3F48;display:flex;align-items:center;gap:28px;padding:0 28px;opacity:0">'
                   f'<div style="width:56px;height:56px;border-radius:50%;background:{AMBER};color:#111;font-size:32px;font-weight:900;display:flex;align-items:center;justify-content:center">{k}</div>'
                   f'<div style="font-size:44px">{em}</div><div style="font-size:40px;font-weight:700">{v}</div>'
                   f'<div id="{cid}-tg{i}" style="margin-left:auto;font-size:28px;font-weight:800;color:{GREEN};letter-spacing:.04em;white-space:nowrap;opacity:0">🧠 WANDERN ✓</div></div>'
                   for i, (k, em, v) in enumerate(POLL_OPTS))


q_html, nq = typed("c4-qq", "Wo kommen dir die besten Ideen?", "left:60px;top:120px;font-size:44px;letter-spacing:0;font-weight:700;color:#FFF;")
T = dict(kurze=W("Kurze", a), wo=W("Wo", a), A=W("A:", a), B=W("B:", a), C=W("C:", a), merk=W("Merk", a), ende=W("Ende", a))
put("c4", S, f"""
  <div id="c4-cam" class="lay">
    {light("c4-l", 960, 500, 760, "rgba(255,226,180,.14)")}
    <div id="c4-card" class="actor card" style="left:400px;top:190px;width:1120px;height:620px;opacity:0">
      <div class="t" style="left:60px;top:50px;font-size:28px;font-weight:800;letter-spacing:.4em;color:{AMBER}">UMFRAGE</div>
      {q_html}{poll_opts("c4")}</div>
    <div id="c4-m" class="t cond" style="left:0;right:0;top:330px;text-align:center;font-size:120px;opacity:0">MERK DIR<br>DEINE ANTWORT</div>
    <div id="c4-e" class="t" style="left:0;right:0;top:700px;text-align:center;font-size:30px;font-weight:800;letter-spacing:.3em;color:{MUTED};opacity:0">AUFLÖSUNG AM ENDE ↓</div>
    {cursor("c4", 1500, 860)}
  </div>""", f'type("#c4-qq", {nq}, T.wo, 0.03);' + r"""
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
  fadeIn("#c4-e", T.ende - 0.6, 0.5);
  fadeOut("#c4-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["kurze"] - 0.1, "pop", 0.3)] + [(T[k], "pop", 0.55) for k in ("A", "B", "C")] + [(T["merk"], "click", 0.5)]

# ================================================================ c5 Titelkarte
title = "DER DUSCH-EFFEKT"
letters = "".join(f'<span id="c5-c{i}" style="display:inline-block;opacity:0">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(title))
a5, e5 = SEG["title"]
drops = "".join(f'<div id="c5-d{i}" class="actor" style="left:{300 + i * 140}px;top:-40px;width:10px;height:26px;border-radius:5px;background:{WATER};opacity:0"></div>' for i in range(10))
put("c5", "title", f"""
  <div class="actor" style="left:0;top:140px;width:1920px;height:800px;overflow:hidden">{drops}</div>
  <div id="c5-k" class="t" style="left:0;right:0;top:380px;text-align:center;font-size:40px;font-weight:800;letter-spacing:.8em;color:{AMBER};opacity:0">OTTO</div>
  <div class="t cond" style="left:0;right:0;top:450px;text-align:center;font-size:150px;letter-spacing:.06em;">{letters}</div>
  <div id="c5-line" class="actor" style="left:560px;top:640px;width:800px;height:3px;background:#FFF;transform-origin:50% 50%"></div>""", f"""
  fadeIn("#c5-k", 0.05, 0.4);
  for (let i = 0; i < {len(title)}; i++) tl.fromTo(`#c5-c${{i}}`, {{ opacity: 0, y: -90, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }}, 0.25 + i * 0.03);
  tl.fromTo("#c5-line", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power3.out" }}, 0.7);
  for (let i = 0; i < 10; i++) tl.fromTo(`#c5-d${{i}}`, {{ opacity: 0.8, y: 0 }}, {{ opacity: 0.8, y: 880, duration: 1.0, ease: "power2.in" }}, 0.1 + (i * 37 % 10) * 0.11);
  tl.to(["#c5-k", "#c5-line"], {{ opacity: 0, duration: 0.3 }}, T.end - 0.35);
  for (let i = 0; i < {len(title)}; i++) tl.to(`#c5-c${{i}}`, {{ opacity: 0, y: 40, duration: 0.25, ease: "power2.in" }}, T.end - 0.4 + i * 0.008);
""", {})
SFX += [(a5 + 0.05, "click", 0.5), (a5 + 0.3, "boom", 0.7)]

# ================================================================ Kapitel 1
chapter("c6", "kap1", 1, "DAS BRETT VORM KOPF")

# ================================================================ c7 Experiment: Ziegelstein + 10-Sekunden-Countdown
a, _ = SEG["v_experiment"]; e = SEG["countdown"][1]; c0 = SEG["countdown"][0]
BRICK = (f'<div style="position:absolute;inset:0;border-radius:14px;background:linear-gradient(160deg,#C2593A,#8E3B26);box-shadow:inset 0 -14px 0 rgba(0,0,0,.25),0 30px 60px rgba(0,0,0,.6)"></div>'
         + "".join(f'<div style="position:absolute;left:{70 + i * 120}px;top:52px;width:56px;height:56px;border-radius:50%;background:#5A2316;box-shadow:inset 0 6px 10px rgba(0,0,0,.5)"></div>' for i in range(3)))
q7, n7 = typed("c7-q", "Was kann man alles mit einem Ziegelstein machen?", "left:130px;top:335px;font-size:50px;letter-spacing:0;font-weight:800;color:#FFF;")
lines7 = "".join(f'<div style="height:66px;border-bottom:3px solid #C9C2B0;font-family:\'Caveat\',cursive;font-size:44px;color:#8A8370;padding-left:8px">{i + 1}.</div>' for i in range(4))
T = dict(experiment=W("Experiment.", a), zehn=W("zehn", a), was=W("Was", a), ziegel=W("Ziegelstein", a), los=W("Los!", a))
putr("c7", a, e, f"""
  <div id="c7-cam" class="lay">
    {header("c7", "MITMACHEN", "DAS ZIEGELSTEIN-EXPERIMENT")}
    {q7}
    <div id="c7-brick" class="actor" style="left:250px;top:500px;width:420px;height:160px;opacity:0">{BRICK}</div>
    <div id="c7-pad" class="actor" style="left:180px;top:430px;width:560px;height:420px;background:#EDE6D6;border-radius:10px;padding:40px 40px;box-shadow:0 30px 70px rgba(0,0,0,.6);opacity:0">{lines7}</div>
    <svg id="c7-ring" class="actor" style="left:1080px;top:330px;opacity:0" width="520" height="520" viewBox="0 0 520 520">
      <circle cx="260" cy="260" r="220" fill="#111" stroke="#2A2E36" stroke-width="26"/>
      <circle id="c7-arc" cx="260" cy="260" r="220" fill="none" stroke="{AMBER}" stroke-width="26" stroke-linecap="round" stroke-dasharray="1382" stroke-dashoffset="0" transform="rotate(-90 260 260)"/></svg>
    <div id="c7-n" class="t" style="left:1080px;width:520px;top:470px;text-align:center;font-family:'Space Mono';font-weight:700;font-size:200px;line-height:1;opacity:0">10</div>
    <div id="c7-z" class="t cond" style="left:1080px;width:520px;top:520px;text-align:center;font-size:150px;color:{RED};opacity:0">ZEIT!</div>
  </div>""", f'type("#c7-q", {n7}, T.was, 0.022);' + HEADER_JS("c7") + f"""
  tl.fromTo("#c7-brick", {{ opacity: 0, y: -160, rotation: -30 }}, {{ opacity: 1, y: 0, rotation: -6, duration: 0.6, ease: "bounce.out" }}, T.ziegel - 0.1);
  tl.to("#c7-brick", {{ rotation: 6, duration: Math.max(0.1, (T.los - T.ziegel - 0.75) / 2), ease: "sine.inOut", yoyo: true, repeat: 1 }}, T.ziegel + 0.6);
  tl.to("#c7-brick", {{ x: 0, y: -360, scale: 0.55, rotation: 0, duration: 0.5, ease: "power3.inOut" }}, T.los);
  tl.fromTo("#c7-pad", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, T.los + 0.15);
  tl.set("#c7-brick", {{ zIndex: 3 }}, T.los);
  popIn("#c7-ring", T.los - 0.1, 0.4); popIn("#c7-n", T.los - 0.1, 0.4);
  tl.fromTo("#c7-arc", {{ attr: {{ "stroke-dashoffset": 0 }} }}, {{ attr: {{ "stroke-dashoffset": 1382 }}, duration: 10, ease: "none" }}, {c0 - a + 0.3:.3f});
  for (let i = 1; i <= 10; i++) {{
    tl.set("#c7-n", {{ textContent: String(10 - i) }}, {c0 - a + 0.3:.3f} + i);
    tl.fromTo("#c7-n", {{ scale: 1.15 }}, {{ scale: 1, duration: 0.3, ease: "power2.out", immediateRender: false }}, {c0 - a + 0.3:.3f} + i);
  }}
  tl.set("#c7-n", {{ color: "{RED}" }}, {c0 - a + 0.3 + 7:.3f});
  tl.to("#c7-n", {{ opacity: 0, duration: 0.1 }}, {c0 - a + 10.3:.3f});
  slam("#c7-z", {c0 - a + 10.3:.3f}, 2);
  fadeOut("#c7-cam", T.end - 0.25, 0.25);
""", T)
SFX += [(T["ziegel"] + 0.3, "drop", 0.4), (T["los"], "click", 0.6), (c0 + 0.3, "tick", 0.4), (c0 + 5.3, "tick", 0.4), (c0 + 10.3, "ding", 0.7)]

# ================================================================ c8 Die üblichen Verdächtigen
S = "v_ueblich"; a = SEG[S][0]
T = dict(bauen=W("bauen,", a), werfen=W("werfen,", a), tuer=W("Türstopper.", a), meisten=W("meisten", a), otto=W("Otto", a), schreib=W("Schreibtisch.", a))
ans = [("🏠", "BAUEN", 300, 300), ("🤾", "WERFEN", 1300, 300), ("🚪", "TÜRSTOPPER", 760, 720)]
ah = "".join(chip(f"c8-a{i}", x, y, f"{em} {t}", size=48) for i, (em, t, x, y) in enumerate(ans))
put("c8", S, f"""
  <div id="c8-cam" class="lay">
    {light("c8-l", 960, 520, 520, "rgba(255,226,180,.18)")}
    <div id="c8-brick" class="actor" style="left:750px;top:440px;width:420px;height:160px">{BRICK}</div>
    {ah}
    {stamp("c8-st", 520, 470, "DIE ÜBLICHEN VERDÄCHTIGEN", RED, 80, -6)}
  </div>""", r"""
  fadeIn("#c8-cam", 0, 0.3);
  tl.fromTo("#c8-brick", { scale: 0.6, rotation: -8 }, { scale: 1, rotation: 0, duration: 0.5, ease: "back.out(2)" }, 0);
  [T.bauen, T.werfen, T.tuer].forEach((t, i) => popIn(`#c8-a${i}`, t - 0.1, 0.4));
  slam("#c8-st", T.meisten + 0.2, 2.2);
  tl.to(["#c8-a0", "#c8-a1", "#c8-a2", "#c8-brick"], { opacity: 0.3, duration: 0.3 }, T.meisten + 0.1);
  fadeOut("#c8-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["bauen"] - 0.1, "pop", 0.4), (T["werfen"] - 0.1, "pop", 0.4), (T["tuer"] - 0.1, "pop", 0.4), (T["meisten"] + 0.35, "boom", 0.4)]

# ================================================================ c9 Fixierung: Rundlauf, Spur wird tiefer
S = "v_fix"; a = SEG[S][0]
T = dict(wenn=W("Wenn", a), wege=W("Wege", a), fix=W("Fixierung.", a), kreis=W("Kreis", a), erste=W("erste,", a))
CX, CY, RX, RY = 960, 610, 420, 200
loop = [(CX + RX * _m.cos(2 * _m.pi * k / 48), CY + RY * _m.sin(2 * _m.pi * k / 48)) for k in range(49)]
laps = 5
dur_lap = max((SEG[S][1] - T["wege"] - 0.6) / laps, 1.2)
kf = ", ".join(f'{{ x: {x - CX - RX:.1f}, y: {y - CY:.1f}, duration: {dur_lap / 48:.3f} }}' for _ in range(laps) for x, y in loop[1:])
exits = "".join(f'<path d="M{CX + RX * _m.cos(t):.0f},{CY + RY * _m.sin(t):.0f} L{CX + (RX + 200) * _m.cos(t):.0f},{CY + (RY + 110) * _m.sin(t):.0f}" stroke="#5A606B" stroke-width="5" stroke-dasharray="14 12"/>'
                f'<text x="{CX + (RX + 225) * _m.cos(t):.0f}" y="{CY + (RY + 135) * _m.sin(t) + 14:.0f}" fill="#8C8F96" font-size="44" font-weight="800" text-anchor="middle" font-family="Inter">?</text>'
                for t in [_m.pi * 1.25, _m.pi * 1.75, _m.pi * 0.25, _m.pi * 0.75])
put("c9", S, f"""
  <div id="c9-cam" class="lay">
    {header("c9", "KAPITEL 1", "FIXIERUNG")}
    <svg class="actor" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
      <g id="c9-ex" opacity="0">{exits}</g>
      <ellipse id="c9-tr" cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="#3A3F48" stroke-width="10"/></svg>
    <div id="c9-dot" class="actor" style="left:{CX + RX - 26}px;top:{CY - 26}px;width:52px;height:52px;border-radius:50%;background:{ORANGE};border:5px solid #FFF;box-shadow:0 0 30px rgba(255,122,26,.8);opacity:0"></div>
    <div id="c9-lab" class="t" style="left:0;right:0;top:585px;text-align:center;font-size:34px;font-weight:800;letter-spacing:.3em;color:{MUTED};opacity:0">IMMER DIESELBE SPUR</div>
  </div>""", HEADER_JS("c9") + f"""
  fadeIn("#c9-cam", 0, 0.3);
  popIn("#c9-dot", T.wege - 0.3, 0.3);
  tl.to("#c9-dot", {{ keyframes: [{kf}], ease: "none" }}, T.wege);
  tl.fromTo("#c9-tr", {{ attr: {{ "stroke-width": 10 }}, stroke: "#3A3F48" }}, {{ attr: {{ "stroke-width": 46 }}, stroke: "#8A5A2E", duration: {dur_lap * laps:.2f}, ease: "none" }}, T.wege);
  fadeIn("#c9-lab", T.fix, 0.4);
  tl.fromTo("#c9-ex", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, T.kreis - 0.6);
  fadeOut("#c9-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["fix"], "click", 0.5)]

# ================================================================ c10 Duncker: Kerzen-Problem
S = "v_kerze"; a = SEG[S][0]
T = dict(karl=W("Karl", a), kerze=W("Kerze,", a), schachtel=W("Schachtel", a), streich=W("Streichhölzer.", a), aufgabe=W("Aufgabe:", a),
         nageln=W("nageln", a), wachs=W("Wachs", W("nageln", a)), loesung=W("Lösung:", a), aus=W("ausleeren,", a), pinnen=W("pinnen,", a),
         rein=W("reinstellen.", a), fertig=W("Fertig.", a), behaelter=W("Behälter", a), regal=W("Regal", a))
tacks = "".join(f'<div id="c10-tk{i}" class="actor" style="left:{18 + (i % 4) * 34}px;top:{22 + (i // 4) * 26}px;width:18px;height:18px;border-radius:50%;background:#D7DCE3;border:3px solid #6B7280"></div>' for i in range(8))
put("c10", S, f"""
  <div id="c10-cam" class="lay">
    {header("c10", "KARL DUNCKER · 1930ER", "DAS KERZEN-PROBLEM")}
    {lower_third("c10", "KARL DUNCKER", "PSYCHOLOGE", 130, 690)}
    <div id="c10-wall" class="actor" style="left:1180px;top:150px;width:560px;height:620px;background:linear-gradient(180deg,#2B2721,#221F1A);border:2px solid #3A352C;opacity:0"></div>
    <div id="c10-table" class="actor" style="left:420px;top:770px;width:1320px;height:30px;background:#5B4632;border-radius:6px;box-shadow:0 20px 40px rgba(0,0,0,.6);opacity:0"></div>
    <div id="c10-candle" class="actor" style="left:600px;top:560px;width:60px;height:210px;opacity:0">
      <div style="position:absolute;left:0;top:30px;width:60px;height:180px;background:#F4EFE3;border-radius:8px"></div>
      <div style="position:absolute;left:28px;top:14px;width:4px;height:20px;background:#333"></div>
      <div id="c10-fl" style="position:absolute;left:14px;top:-40px;width:32px;height:56px;border-radius:50% 50% 50% 50% / 60% 60% 40% 40%;background:radial-gradient(circle at 50% 70%,#FFF6C8,#FFB33B 60%,rgba(255,120,0,0));opacity:0"></div></div>
    <div id="c10-box" class="actor" style="left:780px;top:670px;width:170px;height:100px;background:#B9874E;border:4px solid #7A5530;border-radius:6px;opacity:0">{tacks}</div>
    <div id="c10-match" class="actor" style="left:1010px;top:740px;width:150px;height:30px;opacity:0">
      {"".join(f'<div style="position:absolute;left:{i * 8}px;top:{i * 3}px;width:120px;height:7px;background:#E8D4A8;border-radius:3px"><div style="position:absolute;right:-8px;top:-3px;width:14px;height:13px;border-radius:50%;background:#C0392B"></div></div>' for i in range(3))}</div>
    <div id="c10-task" class="actor card" style="left:130px;top:360px;width:420px;padding:24px 28px;opacity:0">
      <div style="font-size:28px;font-weight:800;letter-spacing:.3em;color:{AMBER}">AUFGABE</div>
      <div style="margin-top:12px;font-size:34px;font-weight:700;line-height:1.25">Kerze an die Wand.<br>Kein Wachs auf den Tisch.</div></div>
    <div id="c10-x" class="t" style="left:1330px;top:330px;font-size:150px;color:{RED};opacity:0">✗</div>
    <div id="c10-ok" class="t" style="left:1560px;top:260px;font-size:120px;color:{GREEN};opacity:0">✓</div>
    <div id="c10-lb" class="t" style="left:1210px;top:560px;width:300px;text-align:center;font-size:30px;font-weight:900;letter-spacing:.1em;color:{MUTED};opacity:0">BEHÄLTER?</div>
    <div id="c10-lr" class="t cond" style="left:1210px;top:550px;width:300px;text-align:center;font-size:64px;color:{AMBER};opacity:0">REGAL!</div>
    {cursor("c10", 1500, 860)}
  </div>""", HEADER_JS("c10") + LT_JS("c10", "T.karl") + r"""
  fadeIn("#c10-cam", 0, 0.3);
  fadeOut("#c10-lt", T.kerze - 0.4, 0.3);
  fadeIn("#c10-table", T.kerze - 0.3, 0.3);
  popIn("#c10-candle", T.kerze, 0.4); popIn("#c10-box", T.schachtel, 0.4); popIn("#c10-match", T.streich, 0.4);
  fadeIn("#c10-wall", T.aufgabe - 0.2, 0.4);
  tl.fromTo("#c10-task", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }, T.aufgabe);
  fadeIn("#c10-cur", T.nageln - 1.0, 0.2);
  move("#c10-cur", -860, -230, T.nageln - 0.9, 0.5);
  tl.to("#c10-candle", { x: 760, y: -240, rotation: 0, duration: 0.5, ease: "power3.inOut" }, T.nageln - 0.4);
  move("#c10-cur", -100, -470, T.nageln - 0.4, 0.5);
  popIn("#c10-x", T.nageln + 0.2, 0.25);
  tl.to("#c10-candle", { x: 0, y: 0, rotation: 0, duration: 0.5, ease: "bounce.out" }, T.nageln + 0.5);
  tl.to("#c10-x", { opacity: 0, duration: 0.2 }, T.wachs - 0.3);
  tl.to("#c10-candle", { x: 760, y: -240, duration: 0.45, ease: "power3.inOut" }, T.wachs - 0.2);
  popIn("#c10-x", T.wachs + 0.4, 0.25);
  tl.to("#c10-candle", { x: 0, y: 0, rotation: 0, duration: 0.5, ease: "bounce.out" }, T.wachs + 0.7);
  tl.to("#c10-x", { opacity: 0, duration: 0.2 }, T.loesung - 0.2);
  fadeOut("#c10-cur", T.loesung - 0.2, 0.2);
  for (let i = 0; i < 8; i++) tl.to(`#c10-tk${i}`, { x: (i - 4) * 40, y: -160 - (i % 3) * 40, rotation: 180, opacity: 0, duration: 0.5, ease: "power2.out" }, T.aus + i * 0.03);
  tl.to("#c10-box", { x: 500, y: -230, rotation: 0, duration: 0.6, ease: "back.inOut(1.4)" }, T.pinnen - 0.3);
  tl.to("#c10-candle", { x: 735, y: -235, duration: 0.6, ease: "back.out(1.6)" }, T.rein - 0.2);
  tl.fromTo("#c10-fl", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, T.fertig - 0.1);
  tl.to("#c10-fl", { scaleY: 1.12, duration: 0.25, yoyo: true, repeat: 20, ease: "sine.inOut" }, T.fertig + 0.2);
  popIn("#c10-ok", T.fertig, 0.35);
  fadeIn("#c10-lb", T.behaelter, 0.3);
  tl.to("#c10-lb", { opacity: 0, duration: 0.2 }, T.regal - 0.2);
  popIn("#c10-lr", T.regal, 0.35);
  fadeOut("#c10-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["karl"], "click", 0.5), (T["kerze"], "pop", 0.4), (T["schachtel"], "pop", 0.4), (T["streich"], "pop", 0.4), (T["nageln"] + 0.2, "click", 0.6),
        (T["wachs"] + 0.4, "click", 0.6), (T["aus"], "pop", 0.4), (T["pinnen"] - 0.3, "pop", 0.4), (T["rein"] - 0.2, "pop", 0.4), (T["fertig"], "ding", 0.6), (T["regal"], "pop", 0.5)]

# ================================================================ c11 Luchins: Wasserkrüge, umständlicher Weg
S = "v_krug"; a = SEG[S][0]
T = dict(dicker=W("dicker:", a), gelernt=W("gelernt", a), einfacheren=W("einfacheren", a), luchins=W("Luchins", a), verkrampfter=W("verkrampfter", a), spur=W("Spur.", a))
jugs = [("A", 21, 0.55, 300), ("B", 127, 0.85, 620), ("C", 3, 0.25, 940)]
jh = "".join(f'<div id="c11-j{i}" class="actor" style="left:{x}px;top:{760 - int(320 * hh)}px;width:200px;height:{int(320 * hh)}px;border:5px solid #C9CDD4;border-top:none;border-radius:0 0 26px 26px;overflow:hidden;opacity:0">'
             f'<div id="c11-w{i}" style="position:absolute;left:0;right:0;bottom:0;height:70%;background:linear-gradient(180deg,#7DB8F5,#3F7FCF);transform-origin:50% 100%"></div></div>'
             f'<div id="c11-jl{i}" class="t" style="left:{x}px;width:200px;top:780px;text-align:center;font-size:36px;font-weight:900;opacity:0">{n} L</div>'
             for i, (k, n, hh, x) in enumerate(jugs))
steps = "".join(chip(f"c11-s{i}", 1260, 320 + i * 100, f"SCHRITT {i + 1}", size=36) for i in range(4))
put("c11", S, f"""
  <div id="c11-cam" class="lay">
    {header("c11", "ABRAHAM LUCHINS · 1942", "DIE WASSERKRÜGE")}
    {jh}
    <div id="c11-goal" class="t cond" style="left:300px;width:840px;top:330px;text-align:center;font-size:70px;color:{AMBER};opacity:0">ZIEL: 20 LITER</div>
    {steps}
    <div id="c11-easy" class="actor" style="left:1250px;top:740px;padding:12px 26px;border-radius:16px;border:3px dashed {GREEN};font-size:36px;font-weight:900;color:{GREEN};opacity:0">1 SCHRITT 👀</div>
    <div id="c11-spur" class="t cond" style="left:0;right:0;top:420px;text-align:center;font-size:96px;opacity:0">JE VERKRAMPFTER,<br><span style="color:{AMBER}">DESTO TIEFER DIE SPUR</span></div>
  </div>""", HEADER_JS("c11") + r"""
  fadeIn("#c11-cam", 0, 0.3);
  for (let i = 0; i < 3; i++) { popIn(`#c11-j${i}`, 0.2 + i * 0.15, 0.4); fadeIn(`#c11-jl${i}`, 0.4 + i * 0.15, 0.3); }
  fadeIn("#c11-goal", T.dicker, 0.4);
  for (let i = 0; i < 4; i++) {
    tl.fromTo(`#c11-s${i}`, { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.3, ease: "back.out(2)" }, T.gelernt + i * 0.35);
    tl.to(`#c11-w${i % 3}`, { scaleY: [0.3, 1, 0.6, 0.85][i], duration: 0.4, ease: "power2.inOut" }, T.gelernt + i * 0.35);
  }
  tl.fromTo("#c11-easy", { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.2 }, { opacity: 0.25, duration: 0.4 }, { opacity: 1, duration: 0.2 }, { opacity: 0.25, duration: 0.4 }] }, T.einfacheren);
  tl.to(["#c11-j0", "#c11-j1", "#c11-j2", "#c11-jl0", "#c11-jl1", "#c11-jl2", "#c11-goal", "#c11-s0", "#c11-s1", "#c11-s2", "#c11-s3", "#c11-easy", "#c11-hk", "#c11-ht"], { opacity: 0, duration: 0.3 }, T.verkrampfter - 0.4);
  tl.fromTo("#c11-spur", { opacity: 0, scale: 1.2 }, { opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }, T.verkrampfter);
  fadeOut("#c11-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["gelernt"] + i * 0.35, "click", 0.4) for i in range(4)] + [(T["einfacheren"], "pop", 0.4), (T["verkrampfter"], "boom", 0.35)]
