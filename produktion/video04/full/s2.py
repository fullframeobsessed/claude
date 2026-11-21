# Wird von gen.py per exec() ausgeführt: Kapitel 2 (Spielautomat) und Kapitel 3 (Flucht nach vorne) inkl. Pause.

chapter("c10", "kap2", 2, "DER SPIELAUTOMAT IN DEINER TASCHE")

# ================================================================ c11 Warum das Handy? + Skinners Tauben
a = SEG["v_warum"][0]; e = SEG["v_skinner"][1]
T = dict(warum=W("warum", a), skinner=W("Skinner", a), tauben=W("Tauben", a), wann=W("wann", a), zwei=W("zwei", a), zwanzig=W("zwanzig.", a), unber=W("Unberechenbarkeit", a))
putr("c11", a, e, f"""
  <div id="c11-cam" class="lay">
    <div id="c11-w" class="t cond" style="left:0;right:0;top:420px;text-align:center;font-size:130px;opacity:0">WARUM <span style="color:{AMBER}">DAS HANDY?</span></div>
    <div id="c11-B" class="lay" style="opacity:0">
      {header("c11", "SKINNER", "DIE TAUBEN-BOX")}
      <div class="actor" style="left:520px;top:340px;width:880px;height:520px;border:4px solid #4A4E57;border-radius:20px;background:rgba(255,255,255,.02)"></div>
      <div id="c11-btn" class="actor" style="left:1180px;top:520px;width:90px;height:90px;border-radius:50%;background:{RED};box-shadow:0 0 30px rgba(255,75,62,.6)"></div>
      <div id="c11-pg" class="actor" style="left:900px;top:520px;font-size:200px;line-height:1;transform-origin:70% 90%">🐦</div>
      <div id="c11-f" class="actor" style="left:1180px;top:700px;font-size:80px;opacity:0">🌽</div>
      <div id="c11-cnt" class="t" style="left:560px;top:380px;font-family:'Space Mono';font-weight:700;font-size:48px;color:{AMBER};opacity:0">PICKS BIS FUTTER: <span id="c11-n">2</span></div>
      <div id="c11-u" class="t cond" style="left:0;right:0;top:870px;text-align:center;font-size:52px;color:{AMBER};opacity:0">UNBERECHENBAR = AUSDAUERND</div>
    </div>
    {foot("c11", "Ferster &amp; Skinner (1957)")}
  </div>""", r"""
  tl.fromTo("#c11-w", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }, 0.05);
  tl.to("#c11-w", { opacity: 0, y: -40, duration: 0.25 }, T.skinner - 0.5);
  fadeIn("#c11-B", T.skinner - 0.3, 0.3);
  fadeIn("#c11-hk", T.skinner - 0.2, 0.4); tl.fromTo("#c11-ht", { opacity: 0, x: -60 }, { opacity: 1, x: 0, duration: 0.5, ease: "power4.out" }, T.skinner);
  fadeIn("#c11-ft", T.skinner, 0.3);
  for (let i = 0; i < 14; i++) tl.fromTo("#c11-pg", { rotation: 0 }, { keyframes: [{ rotation: 18, duration: 0.12 }, { rotation: 0, duration: 0.18 }], immediateRender: false }, T.tauben + i * 0.42);
  fadeIn("#c11-cnt", T.wann, 0.3);
  tl.set("#c11-n", { textContent: "2" }, T.zwei); tl.set("#c11-n", { textContent: "20" }, T.zwanzig); tl.set("#c11-n", { textContent: "5" }, T.zwanzig + 1.2);
  [T.zwei + 0.3, T.zwanzig + 0.3].forEach(t => tl.fromTo("#c11-f", { opacity: 0, y: -40 }, { keyframes: [{ opacity: 1, y: 0, duration: 0.25 }, { opacity: 0, duration: 0.3, delay: 0.5 }], immediateRender: false }, t));
  fadeIn("#c11-u", T.unber, 0.4);
  fadeOut("#c11-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["skinner"] - 0.3, "click", 0.4), (T["zwei"] + 0.3, "pop", 0.35), (T["zwanzig"] + 0.3, "pop", 0.35), (T["unber"], "pop", 0.35)]

# ================================================================ c12 Spielautomat: Walzen, Hebel, endloser Feed
S = "v_automat"; a = SEG[S][0]
T = dict(handy=W("Handy", a), nachricht=W("Nachricht.", a), like=W("Like.", a), nichts=W("nichts.", a), nochmal=W("nochmal.", a), nochmal2=W("nochmal.", W("nochmal.", a) + 0.1),
         spiel=W("Spielautomaten,", a), apps=W("Apps", a), feed=W("Feed", a), runter=W("Runterziehen", a), hebel=W("Hebel", a))
SYM = ["💬", "❤️", "🔕", "📸", "🔕", "👍", "🔕", "🎵", "🔕", "💬", "🔕", "❤️"]
reel = lambda i: (f'<div class="actor" style="left:{620 + i * 230}px;top:420px;width:200px;height:200px;border-radius:16px;background:#F4F6FA;overflow:hidden;border:4px solid #C9A64A">'
                  f'<div id="c12-s{i}" style="position:absolute;left:0;top:0;width:200px">' + "".join(f'<div style="height:200px;display:flex;align-items:center;justify-content:center;font-size:110px">{s}</div>' for s in SYM * 3) + '</div></div>')
feed = "".join(f'<div style="height:110px;margin:12px 14px;border-radius:12px;background:{c}"></div>' for c in ["#3A5A8C", "#8C3A5A", "#5A8C3A", "#8C7A3A", "#3A8C82", "#6A3A8C"] * 3)
put("c12", S, f"""
  <div id="c12-cam" class="lay">
    <div id="c12-A" class="lay">
      <div id="c12-box" class="actor" style="left:560px;top:250px;width:800px;height:560px;border-radius:40px;background:linear-gradient(180deg,#3A2A1A,#221A12);border:6px solid #C9A64A;box-shadow:0 40px 90px rgba(0,0,0,.6);opacity:0">
        <div class="t cond" style="left:0;right:0;top:40px;text-align:center;font-size:64px;color:{AMBER}">🎰 JACKPOT?</div></div>
      {reel(0)}{reel(1)}{reel(2)}
      <div id="c12-lv" class="actor" style="left:1400px;top:300px;width:30px;height:300px;transform-origin:50% 100%;opacity:0">
        <div style="position:absolute;left:0;top:40px;width:30px;height:260px;border-radius:15px;background:#9AA0AA"></div>
        <div style="position:absolute;left:-25px;top:0;width:80px;height:80px;border-radius:50%;background:{RED}"></div></div>
      <div id="c12-res" class="t cond" style="left:560px;width:800px;top:680px;text-align:center;font-size:72px;opacity:0">—</div>
    </div>
    <div id="c12-B" class="lay" style="opacity:0">
      <div id="c12-ph" class="actor" style="left:820px;top:170px;width:280px;height:740px;border-radius:40px;background:#111;border:6px solid #444;overflow:hidden">
        <div id="c12-feed" style="position:absolute;left:0;top:0;width:268px">{feed}</div></div>
      <div id="c12-ar" class="t" style="left:1150px;top:220px;font-size:90px;color:{AMBER};opacity:0">↓</div>
      <div id="c12-inf" class="t cond" style="left:1150px;top:400px;font-size:60px;opacity:0">FEED OHNE ENDE</div>
      <div id="c12-rf" class="t cond" style="left:1150px;top:520px;font-size:60px;color:{AMBER};opacity:0">= HEBEL 🎰</div>
    </div>
  </div>""", r"""
  fadeIn("#c12-cam", 0, 0.3);
  popIn("#c12-box", 0.1, 0.45); popIn("#c12-lv", 0.2, 0.4);
  const spin = (t, idx, label) => {
    tl.fromTo("#c12-lv", { rotation: 0 }, { keyframes: [{ rotation: 35, duration: 0.15 }, { rotation: 0, duration: 0.35 }], immediateRender: false }, t - 0.5);
    for (let i = 0; i < 3; i++) tl.fromTo(`#c12-s${i}`, { y: 0 }, { y: -(12 + idx[i]) * 200, duration: 0.5 + i * 0.12, ease: "power3.out", immediateRender: false }, t - 0.45);
    tl.set("#c12-res", { textContent: label, opacity: 1 }, t + 0.25);
  };
  spin(T.nachricht, [0, 2, 4], "1 NACHRICHT");
  spin(T.like, [1, 6, 8], "1 LIKE");
  spin(T.nichts, [2, 4, 6], "NICHTS.");
  spin(T.nochmal, [4, 8, 10], "NICHTS.");
  spin(T.nochmal2, [6, 2, 4], "NICHTS.");
  tl.to("#c12-A", { opacity: 0, scale: 0.9, duration: 0.3 }, T.apps - 0.3);
  fadeIn("#c12-B", T.apps - 0.1, 0.3);
  tl.fromTo("#c12-feed", { y: 0 }, { y: -1900, duration: 6, ease: "none", immediateRender: false }, T.feed - 0.2);
  fadeIn("#c12-inf", T.feed, 0.3);
  tl.fromTo("#c12-ar", { opacity: 0, y: -30 }, { opacity: 1, y: 40, duration: 0.6, repeat: 2, ease: "power2.in" }, T.runter);
  popIn("#c12-rf", T.hebel - 0.1, 0.35);
  fadeOut("#c12-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(t, "click", 0.4) for t in (T["nachricht"] - 0.5, T["like"] - 0.5, T["nichts"] - 0.5, T["nochmal"] - 0.5, T["nochmal2"] - 0.5)] + \
       [(T["nachricht"] + 0.25, "pop", 0.4), (T["like"] + 0.25, "pop", 0.4), (T["hebel"] - 0.1, "pop", 0.4)]

# ================================================================ c13 Erwartung schlägt Belohnung: Kurve
S = "v_erwartung"; a = SEG[S][0]
T = dict(belohnung=W("Belohnungssystem", a), erwartung=W("Erwartung.", a), kribbeln=W("Kribbeln", a), kick=W("Kick,", a), siehst=W("siehst.", a))
pts = [(300, 820), (520, 800), (700, 700), (820, 420), (900, 320), (980, 420), (1080, 640), (1300, 760), (1560, 790)]
path = "M" + " L".join(f"{x},{y}" for x, y in pts)
put("c13", S, f"""
  <div id="c13-cam" class="lay">
    {header("c13", "BELOHNUNGSSYSTEM", "DIE VORFREUDE IST DER KICK")}
    <svg class="actor" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
      <path d="M280,860 L1600,860" stroke="#5A606B" stroke-width="4"/>
      <path id="c13-cv" d="{path}" fill="none" stroke="{AMBER}" stroke-width="8" stroke-linejoin="round" stroke-dasharray="2200" stroke-dashoffset="2200"/></svg>
    <div class="t" style="left:280px;top:875px;font-size:28px;font-weight:800;letter-spacing:.14em;color:{MUTED}">VORHER</div>
    <div class="t" style="left:820px;top:875px;font-size:28px;font-weight:800;letter-spacing:.14em;color:{MUTED}">🔓 ENTSPERREN</div>
    <div class="t" style="left:1320px;top:875px;font-size:28px;font-weight:800;letter-spacing:.14em;color:{MUTED}">INHALT</div>
    <div id="c13-p" class="t cond" style="left:960px;top:300px;font-size:56px;color:{AMBER};opacity:0">← VORFREUDE</div>
    <div id="c13-i" class="t cond" style="left:1280px;top:650px;font-size:48px;color:{MUTED};opacity:0">„… ach, nichts Neues.“</div>
    <div id="c13-ft" class="t" style="left:1380px;top:200px;font-size:28px;font-weight:600;letter-spacing:.14em;color:{MUTED};opacity:0">Schultz (2016) · vereinfacht</div>
  </div>""", HEADER_JS("c13") + r"""
  fadeIn("#c13-cam", 0, 0.3);
  tl.to("#c13-cv", { attr: { "stroke-dashoffset": 0 }, duration: 2.6, ease: "power1.inOut" }, T.erwartung - 1.2);
  popIn("#c13-p", T.kribbeln, 0.35);
  fadeIn("#c13-i", T.siehst - 1.4, 0.3);
  fadeIn("#c13-ft", T.belohnung, 0.3);
  fadeOut("#c13-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["kribbeln"], "pop", 0.4)]

chapter("c14", "kap3", 3, "DIE FLUCHT NACH VORNE")

# ================================================================ c15 Rückbezug Folge 1: Gefühlsproblem
S = "v_folge1"; a = SEG[S][0]
T = dict(erste=W("erste", a), zeit=W("Zeitproblem,", a), gefuehl=W("Gefühlsproblem.", a), hier=W("hier", a))
put("c15", S, f"""
  <div id="c15-cam" class="lay">
    <div id="c15-th" class="actor" style="left:180px;top:260px;width:720px;height:405px;border-radius:18px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.6);opacity:0">
      <img src="assets/thumb01.png" style="width:720px;height:405px;display:block" /></div>
    <div id="c15-lb" class="t" style="left:180px;top:690px;font-size:32px;font-weight:900;letter-spacing:.2em;color:{AMBER};opacity:0">◀ FOLGE 1</div>
    <div id="c15-z" class="t cond" style="left:1020px;top:320px;font-size:84px;opacity:0">ZEITPROBLEM</div>
    <div id="c15-x" class="actor" style="left:1010px;top:365px;width:560px;height:12px;background:{RED};border-radius:6px;transform-origin:0 50%;transform:rotate(-4deg);opacity:0"></div>
    <div id="c15-g" class="t cond" style="left:1020px;top:470px;font-size:96px;color:{AMBER};opacity:0">GEFÜHLSPROBLEM</div>
  </div>""", r"""
  fadeIn("#c15-cam", 0, 0.3);
  tl.fromTo("#c15-th", { opacity: 0, x: -80, rotation: -4 }, { opacity: 1, x: 0, rotation: -2, duration: 0.5, ease: "back.out(1.6)" }, T.erste - 0.3);
  fadeIn("#c15-lb", T.erste, 0.3);
  fadeIn("#c15-z", T.zeit - 0.3, 0.3);
  tl.fromTo("#c15-x", { opacity: 1, scaleX: 0 }, { opacity: 1, scaleX: 1, duration: 0.3, ease: "power3.out" }, T.zeit + 0.3);
  popIn("#c15-g", T.gefuehl - 0.1, 0.4);
  fadeOut("#c15-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["erste"] - 0.3, "pop", 0.35), (T["zeit"] + 0.3, "click", 0.5), (T["gefuehl"] - 0.1, "pop", 0.4)]

# ================================================================ c16 Notausgang: unangenehm → Handy
S = "v_notausgang"; a = SEG[S][0]
T = dict(schau=W("Schau", a), flow=W("Flow.", a), unang=W("unangenehm", a), satz=W("Satz", a), zaeh=W("zäh", a), notaus=W("Notausgang,", a))
put("c16", S, f"""
  <div id="c16-cam" class="lay">
    {otto_at("c16", 160, ("tired", "excuse"))}
    <div id="c16-th" class="actor" style="left:880px;top:220px;width:70px;height:520px;border-radius:35px;background:#22262E;border:4px solid #3A3F48;overflow:hidden;opacity:0">
      <div id="c16-lv" style="position:absolute;left:0;right:0;bottom:0;height:100%;background:linear-gradient(0deg,#4FA3FF,#FF4B3E);transform-origin:50% 100%"></div></div>
    <div id="c16-tl" class="t" style="left:980px;top:230px;font-size:32px;font-weight:900;letter-spacing:.14em;color:{RED};opacity:0">UNANGENEHM</div>
    {chip("c16-s", 980, 380, "✍️ ERSTER SATZ?", size=38)}
    {chip("c16-z", 980, 480, "🐌 ZÄH …", size=38)}
    <div id="c16-ex" class="actor" style="left:1240px;top:600px;padding:20px 30px;border-radius:14px;background:#1B8A3A;border:4px solid #7CFF8A;font-size:52px;font-weight:900;opacity:0">🏃 NOTAUSGANG 📱</div>
  </div>""", r"""
  fadeIn("#c16-cam", 0, 0.3);
  fadeIn("#c16-th", T.flow, 0.3);
  tl.fromTo("#c16-lv", { scaleY: 0.1 }, { scaleY: 0.95, duration: 2.2, ease: "power2.in" }, T.unang - 0.3);
  fadeIn("#c16-tl", T.unang, 0.3);
  popIn("#c16-s", T.satz - 0.2, 0.3); popIn("#c16-z", T.zaeh - 0.2, 0.3);
  face("c16o", "tired", "excuse", T.zaeh);
  tl.fromTo("#c16-ex", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, T.notaus - 0.2);
  tl.to("#c16-ex", { boxShadow: "0 0 50px rgba(124,255,138,.8)", duration: 0.4, yoyo: true, repeat: 3 }, T.notaus + 0.3);
  fadeOut("#c16-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["satz"] - 0.2, "pop", 0.35), (T["zaeh"] - 0.2, "pop", 0.35), (T["notaus"] - 0.2, "pop", 0.45)]

# ================================================================ c17 Aufmerksamkeitsrest: Geister-Otto scrollt weiter
S = "v_rest"; a = SEG[S][0]
T = dict(problem=W("Problem:", a), leroy=W("Leroy", a), wechsel=W("Wechsel", a), rest=W("Aufmerksamkeitsrest.", a), zurueck=W("zurück", a), scrollt=W("scrollt", a),
         versuchen=W("Versuchen", a), schlechter=W("schlechter", a))
put("c17", S, f"""
  <div id="c17-cam" class="lay">
    {header("c17", "SOPHIE LEROY · 2009", "AUFMERKSAMKEITSREST")}
    <div id="c17-g" class="actor" style="left:250px;top:260px;width:492px;height:623px;opacity:0;filter:grayscale(1) blur(1px)"><div style="transform:scale(.82);transform-origin:0 0;width:600px;height:760px">{otto_svg("c17g", ("smirk",), pose="bent", held='<rect x="10" y="190" width="44" height="80" rx="8" fill="#111" stroke="#111" stroke-width="5"/>')}</div></div>
    <div class="actor" style="left:130px;top:260px;width:492px;height:623px"><div style="transform:scale(.82);transform-origin:0 0;width:600px;height:760px">{otto_svg("c17o", ("tired",))}</div></div>
    <div id="c17-bar" class="actor card" style="left:900px;top:400px;width:880px;height:170px;padding:26px 30px;opacity:0">
      <div style="font-size:30px;font-weight:800;letter-spacing:.2em;color:{MUTED}">AUFMERKSAMKEIT BEI DER ARBEIT</div>
      <div style="margin-top:20px;height:40px;border-radius:20px;background:#2A2E36;overflow:hidden"><div id="c17-f" style="height:100%;background:{GREEN};transform-origin:0 50%"></div></div></div>
    <div id="c17-p" class="t" style="left:900px;top:590px;font-size:40px;font-weight:900;color:{RED};opacity:0">EIN TEIL HÄNGT NOCH AM HANDY</div>
    <div id="c17-s" class="t cond" style="left:900px;top:680px;font-size:64px;color:{AMBER};opacity:0">NÄCHSTE AUFGABE: SCHLECHTER ↓</div>
    {foot("c17", "Leroy (2009), Organizational Behavior and Human Decision Processes")}
  </div>""", HEADER_JS("c17") + r"""
  fadeIn("#c17-cam", 0, 0.3);
  tl.fromTo("#c17-bar", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, T.wechsel - 0.3);
  tl.fromTo("#c17-f", { scaleX: 1 }, { scaleX: 0.68, duration: 0.8, ease: "power3.inOut" }, T.wechsel + 0.4);
  fadeIn("#c17-p", T.rest - 0.2, 0.3);
  tl.fromTo("#c17-g", { opacity: 0, x: 0 }, { opacity: 0.35, x: 120, duration: 0.6, ease: "power2.out" }, T.scrollt - 0.4);
  fadeIn("#c17-ft", T.leroy, 0.3);
  tl.fromTo("#c17-s", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, T.schlechter - 0.2);
  fadeOut("#c17-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["wechsel"] - 0.3, "pop", 0.35), (T["scrollt"] - 0.4, "pop", 0.3), (T["schlechter"] - 0.2, "click", 0.45)]

# ================================================================ c18 Brain Drain: Handy auf dem Tisch / Tasche / anderer Raum
S = "v_brain"; a = SEG[S][0]
T = dict(liegt=W("liegt.", a), experiment=W("Experiment", a), tisch=W("Tisch", a), raum=W("Raum", a), aus=W("ausgeschaltet.", a), folge=W("Folgestudien", a), zieht=W("zieht", a))
cols = [("AUF DEM TISCH", "📱", 0.45), ("IN DER TASCHE", "👜", 0.65), ("ANDERER RAUM", "🚪", 0.9)]
ch = "".join(f'<div class="t" style="left:{330 + i * 460}px;width:360px;top:830px;text-align:center;font-size:30px;font-weight:900">{lab}</div>'
             f'<div id="c18-i{i}" class="actor" style="left:{460 + i * 460}px;top:250px;font-size:90px;opacity:0">{em}</div>'
             f'<div id="c18-b{i}" class="actor" style="left:{410 + i * 460}px;top:{810 - int(420 * h)}px;width:200px;height:{int(420 * h)}px;border-radius:12px 12px 4px 4px;'
             f'background:{[RED, "#C9A64A", GREEN][i]};transform-origin:50% 100%;opacity:0"></div>' for i, (lab, em, h) in enumerate(cols))
put("c18", S, f"""
  <div id="c18-cam" class="lay">
    <div class="t" style="left:130px;top:180px;font-size:28px;font-weight:800;letter-spacing:.4em;color:{AMBER}">DENKLEISTUNG</div>
    {ch}
    {chip("c18-off", 1260, 180, "🔌 SOGAR AUSGESCHALTET", size=34)}
    <div id="c18-fn" class="t" style="left:130px;top:880px;font-size:28px;font-weight:700;color:{MUTED};opacity:0">Ward et al. (2017) · Folgestudien: Effekt nicht immer gleich stark</div>
    <div id="c18-mg" class="t cond" style="left:0;right:0;top:230px;text-align:center;font-size:84px;color:{AMBER};opacity:0">🧲 WAS DU SIEHST, ZIEHT AN DIR.</div>
  </div>""", r"""
  fadeIn("#c18-cam", 0, 0.3);
  for (let i = 0; i < 3; i++) popIn(`#c18-i${i}`, T.experiment + i * 0.2, 0.35);
  for (let i = 0; i < 3; i++) tl.fromTo(`#c18-b${i}`, { opacity: 1, scaleY: 0 }, { opacity: 1, scaleY: 1, duration: 0.6, ease: "back.out(1.4)" }, [T.tisch, T.tisch + 0.6, T.raum][i]);
  popIn("#c18-off", T.aus - 0.2, 0.35);
  fadeIn("#c18-fn", T.experiment, 0.3);
  tl.to(["#c18-i0", "#c18-i1", "#c18-i2", "#c18-off"], { opacity: 0, duration: 0.3 }, T.zieht - 1.5);
  popIn("#c18-mg", T.zieht - 1.2, 0.4);
  fadeOut("#c18-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["tisch"], "pop", 0.35), (T["raum"], "pop", 0.4), (T["aus"] - 0.2, "click", 0.45), (T["zieht"] - 0.5, "pop", 0.4)]

# ================================================================ c19 Pause-Moment: Bildschirmzeit-Check + Freeze
a = SEG["v_pause"][0]; e = SEG["pausefreeze"][1]
T = dict(pausier=W("Pausier", a), check=W("Check:", a), bild=W("Bildschirmzeit,", a), tipp=W("Tipp", a))
putr("c19", a, e, f"""
  <div id="c19-cam" class="lay">
    <div id="c19-p" class="actor" style="left:250px;top:300px;width:300px;height:320px;opacity:0;display:flex;gap:60px;justify-content:center">
      <div style="width:110px;height:320px;border-radius:18px;background:#FFF"></div><div style="width:110px;height:320px;border-radius:18px;background:#FFF"></div></div>
    <div id="c19-g" class="actor card" style="left:760px;top:230px;width:900px;padding:34px 40px;opacity:0">
      <div style="font-size:30px;font-weight:800;letter-spacing:.3em;color:{AMBER}">SO FINDEST DU ES</div>
      <div style="margin-top:22px;font-size:42px;font-weight:800">🍏 iPhone: Bildschirmzeit → <span style="color:{AMBER}">Aktivierungen</span></div>
      <div style="margin-top:18px;font-size:42px;font-weight:800">🤖 Android: Digital Wellbeing → <span style="color:{AMBER}">Entsperrungen</span></div></div>
    <div id="c19-q" class="t cond" style="left:760px;top:640px;font-size:84px;opacity:0">LAG DEIN TIPP RICHTIG? 🎯</div>
    <div id="c19-fr" class="actor" style="left:0;top:132px;width:1920px;height:816px;background:rgba(255,255,255,.06);opacity:0"></div>
  </div>""", r"""
  fadeIn("#c19-cam", 0, 0.2);
  tl.fromTo("#c19-p", { opacity: 0, scale: 1.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "power4.in" }, T.pausier);
  tl.fromTo("#c19-g", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, T.bild - 0.3);
  popIn("#c19-q", T.tipp - 0.2, 0.4);
  tl.fromTo("#c19-fr", { opacity: 0 }, { opacity: 1, duration: 0.1 }, T.end - 1.5);
  fadeOut("#c19-cam", T.end - 0.3, 0.3);
""", T)
SFX += [(T["pausier"] + 0.25, "click", 0.7), (T["bild"] - 0.3, "pop", 0.35), (T["tipp"] - 0.2, "pop", 0.4)]
