# Wird von gen.py per exec() ausgeführt: Szenen nach dem Zeit-Kasten (Kapitel 1 Rest bis Abspann).
# Verfügbar: W, SEG, put, light, typed, cursor, actor, otto_svg, svgbox, art, SFX, MUTED, AMBER, RED, PAPER, ORANGE, OTTO_TOP, _head_base, _face
GREEN = "#7CFF8A"


def chapter(cid, sid, num, title):
    a, _ = SEG[sid]
    put(cid, sid, f"""
  <div id="{cid}-k" class="t" style="left:0;right:0;top:400px;text-align:center;font-size:30px;font-weight:700;letter-spacing:.6em;color:{MUTED};opacity:0">KAPITEL {num}</div>
  <div id="{cid}-t" class="t cond" style="left:0;right:0;top:460px;text-align:center;font-size:130px;letter-spacing:.1em;opacity:0">{title}</div>
  <div id="{cid}-l" class="actor" style="left:260px;top:640px;width:1400px;height:2px;background:{AMBER};transform-origin:0 50%"></div>""", f"""
  tl.fromTo("#{cid}-k", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }}, 0.05);
  tl.fromTo("#{cid}-t", {{ opacity: 0, x: -120, filter: "blur(12px)" }}, {{ opacity: 1, x: 0, filter: "blur(0px)", duration: 0.5, ease: "power4.out" }}, 0.2);
  tl.fromTo("#{cid}-l", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.8, ease: "power3.inOut" }}, 0.3);
  tl.to(["#{cid}-k", "#{cid}-t", "#{cid}-l"], {{ opacity: 0, duration: 0.35, ease: "power2.in" }}, T.end - 0.4);""", {})
    SFX.extend([(a + 0.05, "whoosh", 0.6), (a + 0.25, "boom", 0.7)])


def otto_at(cid, x, faces, top=OTTO_TOP, s=1.0, **kw):
    lt = light(f"{cid}-ol", x + 300 * s, top + 320 * s, 480 * s, "rgba(255,226,180,.28)")
    return (lt + f'<div id="{cid}-otto" class="actor" style="left:{x}px;top:{top}px;width:{600 * s:.0f}px;height:{760 * s:.0f}px;">'
            f'<div style="position:absolute;left:0;top:0;width:600px;height:760px;transform:scale({s});transform-origin:0 0">{otto_svg(cid + "o", faces, **kw)}</div></div>')


def header(cid, kicker, title, x=130):
    return (f'<div id="{cid}-hk" class="t" style="left:{x}px;top:180px;font-size:28px;font-weight:800;letter-spacing:.4em;color:{AMBER};opacity:0">{kicker}</div>'
            f'<div id="{cid}-ht" class="t cond" style="left:{x}px;top:222px;font-size:88px;opacity:0">{title}</div>')


HEADER_JS = lambda cid: f'fadeIn("#{cid}-hk", 0.1, 0.4); tl.fromTo("#{cid}-ht", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power4.out" }}, 0.25);'  # noqa: E731


def foot(cid, text):
    return f'<div id="{cid}-ft" class="t" style="left:130px;top:880px;font-size:28px;font-weight:600;letter-spacing:.14em;color:{MUTED};opacity:0">{text}</div>'


def clock_html(id_, txt, x, y, size=72):
    return (f'<div id="{id_}" class="actor" style="left:{x}px;top:{y}px;padding:10px 26px;background:#111;border:3px solid #333;border-radius:18px;'
            f'font-family:\'Space Mono\';font-weight:700;font-size:{size}px;color:#FF5A4A;text-shadow:0 0 30px rgba(255,60,40,.5);opacity:0">{txt}</div>')


# ================================================================ c8 Horizont → FR 23:58
S = "v_horizont"; a = SEG[S][0]
ticks = "".join(f'<div style="position:absolute;left:{i * 160}px;top:0;width:2px;height:{40 if i % 7 == 0 else 20}px;background:#5A606B"></div>'
                f'<div class="t" style="left:{i * 160 - 30}px;top:52px;width:60px;text-align:center;font-size:26px;color:#6E717A;font-weight:700">{["MO","DI","MI","DO","FR","SA","SO"][i % 7]}</div>'
                for i in range(60))
T8 = dict(nicht=W("nicht,", a), zuviel=W("viel", a), drei=W("Drei", a), horizont=W("Horizont.", a), freitag=W("Freitag,", a), konkret=W("konkret.", a))
put("c8", S, f"""
  <div id="c8-cam" class="lay">
    {otto_at("c8", 220, ("excuse", "shock"))}
    <div id="c8-a" class="t cond" style="left:900px;top:300px;font-size:84px;opacity:0">ZU WENIG ZEIT?</div>
    <div id="c8-ax" class="actor" style="left:890px;top:345px;width:620px;height:10px;background:{RED};transform:rotate(-4deg);transform-origin:0 50%"></div>
    <div id="c8-b" class="t cond" style="left:900px;top:420px;font-size:84px;color:{AMBER};opacity:0">ZU VIEL ZEIT<br>FÜHLT SICH NACH<br>NICHTS AN.</div>
  </div>
  <div id="c8-hz" class="lay" style="opacity:0">
    {light("c8-hl", 960, 540, 900, "rgba(140,190,255,.10)")}
    <div class="t" style="left:0;right:0;top:300px;text-align:center;font-size:30px;font-weight:800;letter-spacing:.4em;color:{MUTED}">3 WOCHEN … ODER UNENDLICH?</div>
    <div class="actor" style="left:0;top:520px;width:1920px;height:3px;background:linear-gradient(90deg,transparent,#5A606B 20%,#5A606B 80%,transparent)"></div>
    <div id="c8-tr" class="actor" style="left:200px;top:500px;width:9600px;height:90px">{ticks}</div>
    <div class="t cond" style="left:0;right:0;top:640px;text-align:center;font-size:96px;letter-spacing:.06em">UNENDLICH WEITER HORIZONT</div>
  </div>
  <div id="c8-fr" class="lay" style="background:#0B0C0E;opacity:0">
    {light("c8-rl", 960, 470, 520, "rgba(255,60,40,.22)")}
    <div class="t" style="left:0;right:0;top:330px;text-align:center;font-family:'Space Mono';font-weight:700;font-size:200px;color:#FF5A4A;text-shadow:0 0 50px rgba(255,60,40,.6)">FR 23:58</div>
    <div id="c8-k" class="t cond" style="left:0;right:0;top:620px;text-align:center;font-size:84px;opacity:0">SEHR, SEHR KONKRET.</div>
  </div>""", r"""
  fadeIn("#c8-cam", 0, 0.4);
  fadeIn("#c8-a", T.nicht - 0.6, 0.4);
  tl.fromTo("#c8-ax", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.inOut" }, T.nicht + 0.1);
  face("c8o", "excuse", "shock", T.zuviel);
  fadeIn("#c8-b", T.zuviel, 0.5, { from: { y: 30 }, to: { y: 0 } });
  tl.to("#c8-cam", { opacity: 0, duration: 0.4 }, T.drei - 0.3);
  fadeIn("#c8-hz", T.drei - 0.2, 0.5);
  tl.fromTo("#c8-tr", { x: 0 }, { x: -6200, duration: T.freitag - T.drei + 0.2, ease: "power1.in" }, T.drei - 0.2);
  tl.set("#c8-hz", { opacity: 0 }, T.freitag - 0.05);
  tl.fromTo("#c8-fr", { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power4.out" }, T.freitag - 0.05);
  tl.fromTo("#c8-fr", { x: 0 }, { keyframes: [{ x: -14, duration: 0.04 }, { x: 12, duration: 0.04 }, { x: 0, duration: 0.06 }], immediateRender: false }, T.freitag + 0.2);
  fadeIn("#c8-k", T.konkret - 0.6, 0.4);
  fadeOut("#c8-fr", T.end - 0.35, 0.35);
""", T8)
SFX.extend([(T8["drei"] - 0.2, "whoosh", 0.35), (T8["freitag"] - 0.05, "boom", 0.45), (T8["freitag"], "tick", 0.3)])

chapter("c9", "kap2", 2, "DER TURBO IM KOPF")

# ================================================================ c10 Amygdala & Waage
S = "v_amy"; a = SEG[S][0]
beam = f'''<g stroke="#1A1A1A" stroke-width="5" stroke-linejoin="round">
  <path d="M-70,330 L70,330 L24,280 L-24,280 Z" fill="#8A8F98"/><rect x="-10" y="40" width="20" height="242" fill="#B5BAC2"/>
  <g id="c10-beam"><rect x="-330" y="26" width="660" height="22" rx="10" fill="#B5BAC2"/>
    <g id="c10-pL"><path d="M-300,40 L-360,170 M-300,40 L-240,170" stroke-width="4"/><path d="M-390,170 Q-300,230 -210,170 Z" fill="#CFC9BC"/></g>
    <g id="c10-pR"><path d="M300,40 L240,170 M300,40 L360,170" stroke-width="4"/><path d="M210,170 Q300,230 390,170 Z" fill="#CFC9BC"/></g>
  </g><circle cx="0" cy="40" r="16" fill="{ORANGE}"/></g>'''
T10 = dict(alarm=W("Alarmanlage", a), amy=W("Amygdala?", a), solange=W("Solange", a), naeher=W("näher", a), uebel=W("Übel.", a), dreht=W("dreht", a))
put("c10", S, f"""
  <div id="c10-cam" class="lay">
    {light("c10-l", 960, 520, 700, "rgba(255,226,180,.18)")}
    <div id="c10-al" class="actor" style="left:180px;top:300px;width:300px;height:380px;opacity:0">{svgbox(art.alarm_guy(0, 0, 1.4), "-150 -220 300 380", 300, 380)}</div>
    <div id="c10-al-l" class="t" style="left:150px;top:700px;font-size:30px;font-weight:800;letter-spacing:.2em;opacity:0">AMYGDALA</div>
    <div id="c10-bal" class="actor" style="left:560px;top:250px;width:800px;height:520px;opacity:0">{svgbox(beam, "-400 -60 800 520", 800, 520)}</div>
    <div id="c10-lL" class="t cond" style="left:610px;top:640px;width:300px;text-align:center;font-size:54px;opacity:0">MACHEN</div>
    <div id="c10-lR" class="t cond" style="left:1010px;top:640px;width:300px;text-align:center;font-size:54px;color:{AMBER};opacity:0">NICHT<br>MACHEN</div>
    {clock_html("c10-clk", '<span id="c10-ct">MO 09:00</span>', 1450, 240, 60)}
  </div>""", r"""
  fadeIn("#c10-cam", 0, 0.4);
  popIn("#c10-al", T.alarm - 0.2); fadeIn("#c10-al-l", T.amy, 0.4);
  fadeIn("#c10-bal", T.solange - 0.3, 0.5); fadeIn("#c10-lL", T.solange, 0.4); fadeIn("#c10-lR", T.solange + 0.2, 0.4);
  tl.fromTo("#c10-beam", { rotation: 0, svgOrigin: "0 40" }, { rotation: -14, duration: 0.8, ease: "back.out(1.6)" }, T.solange + 0.6);
  tl.fromTo("#c10-pL", { rotation: 0, svgOrigin: "-300 40" }, { rotation: 14, duration: 0.8, ease: "back.out(1.6)" }, T.solange + 0.6);
  tl.fromTo("#c10-pR", { rotation: 0, svgOrigin: "300 40" }, { rotation: 14, duration: 0.8, ease: "back.out(1.6)" }, T.solange + 0.6);
  fadeIn("#c10-clk", T.naeher - 0.4, 0.3);
  ["DI 14:00", "MI 20:00", "DO 22:00", "FR 18:00", "FR 23:58"].forEach((s, i) => tl.set("#c10-ct", { textContent: s }, T.naeher + i * 0.5));
  tl.to("#c10-beam", { rotation: 16, duration: 1.0, ease: "back.out(1.4)" }, T.dreht);
  tl.to(["#c10-pL", "#c10-pR"], { rotation: -16, duration: 1.0, ease: "back.out(1.4)" }, T.dreht);
  tl.to("#c10-lR", { scale: 1.15, duration: 0.4, ease: "back.out(2)" }, T.uebel - 0.2);
  fadeOut("#c10-cam", T.end - 0.35, 0.35);
""", T10)
SFX.extend([(T10["alarm"] - 0.2, "pop", 0.4), (T10["naeher"], "tick", 0.25), (T10["dreht"], "whoosh", 0.3)])

# ================================================================ c11 Noradrenalin, Puls, Fokus
S = "v_hormon"; a = SEG[S][0]
ekg = "M0,100 " + " ".join(f"L{x + 40},100 L{x + 55},70 L{x + 70},100 L{x + 90},100 L{x + 100},20 L{x + 110},170 L{x + 120},100 L{x + 160},100" for x in range(0, 3200, 160))
distr = [("📱", 1350, 300), ("🐧", 1550, 420), ("🧦", 1380, 600), ("📺", 1620, 680)]
T11 = dict(nor=W("Noradrenalin", a), puls=W("Puls", a), fokus=W("Fokus", a), abl=W("Ablenkungen", a))
put("c11", S, f"""
  <div id="c11-cam" class="lay">
    {light("c11-l", 700, 500, 700, "rgba(255,90,80,.14)")}
    <div id="c11-chip" class="actor" style="left:180px;top:220px;padding:12px 26px;border-radius:14px;background:#2A1D1D;border:2px solid #FF5A4A;font-size:40px;font-weight:900;letter-spacing:.08em;color:#FF8A7A;opacity:0">NORADRENALIN ↑</div>
    <div id="c11-ekgw" class="actor" style="left:180px;top:360px;width:1000px;height:200px;overflow:hidden;opacity:0">
      <svg id="c11-ekg" width="3200" height="200" viewBox="0 0 3200 200" style="position:absolute;left:0;top:0"><path d="{ekg}" fill="none" stroke="#FF5A4A" stroke-width="5" stroke-linejoin="round"/></svg></div>
    <div id="c11-bpm" class="t cond" style="left:180px;top:590px;font-size:110px;color:#FF5A4A;opacity:0"><span id="c11-n">72</span> <span style="font-size:50px">BPM</span></div>
    {"".join(f'<div id="c11-d{i}" class="t" style="left:{x}px;top:{y}px;font-size:110px;opacity:0">{e}</div>' for i, (e, x, y) in enumerate(distr))}
    <div id="c11-vig" class="lay" style="background:radial-gradient(circle at 680px 480px, transparent 30%, rgba(0,0,0,.92) 62%);opacity:0"></div>
    <div id="c11-f" class="t cond" style="left:180px;top:780px;font-size:56px;letter-spacing:.2em;color:{AMBER};opacity:0">TUNNELBLICK</div>
  </div>""", r"""
  fadeIn("#c11-cam", 0, 0.4);
  popIn("#c11-chip", T.nor - 0.2);
  fadeIn("#c11-ekgw", T.puls - 0.6, 0.4);
  tl.fromTo("#c11-ekg", { x: 0 }, { x: -2100, duration: T.end, ease: "power2.in" }, 0);
  fadeIn("#c11-bpm", T.puls - 0.3, 0.3);
  tl.fromTo("#c11-n", { textContent: 72 }, { textContent: 128, duration: 2.2, ease: "power2.in", snap: { textContent: 1 } }, T.puls);
  [0, 1, 2, 3].forEach(i => fadeIn(`#c11-d${i}`, 0.6 + i * 0.25, 0.4, { from: { scale: 0.5 }, to: { scale: 1 } }));
  tl.fromTo("#c11-vig", { opacity: 0 }, { opacity: 1, duration: 1.2, ease: "power2.inOut" }, T.fokus);
  fadeIn("#c11-f", T.fokus + 0.4, 0.4);
  [0, 1, 2, 3].forEach(i => tl.to(`#c11-d${i}`, { x: 900, y: -200 + i * 120, rotation: 140, opacity: 0, duration: 0.6, ease: "power3.in" }, T.abl + i * 0.12));
  fadeOut("#c11-cam", T.end - 0.35, 0.35);
""", T11)
SFX.extend([(T11["puls"] - 0.3, "heart", 0.6), (T11["abl"], "whoosh", 0.4)])

# ================================================================ c12 Leistungskurve
S = "v_kurve"; a = SEG[S][0]
import math  # noqa: E402
X0, Y0, WD, HT = 460, 780, 1000, 480
pts = [(X0 + WD * u, Y0 - HT * math.exp(-((u - 0.5) ** 2) / 0.045)) for u in [i / 60 for i in range(61)]]
path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
plen = sum(math.dist(pts[i], pts[i + 1]) for i in range(60))


def kpts(u0, u1, n=8):
    return [{"x": round(X0 + WD * u - 960, 1), "y": round(Y0 - HT * math.exp(-((u - 0.5) ** 2) / 0.045) - 540, 1)} for u in [u0 + (u1 - u0) * k / n for k in range(1, n + 1)]]


T12 = dict(kurve=W("Kurve:", a), steigt=W("steigt", a), punkt=W("Punkt.", a), kippt=W("kippt", a), steil=W("steilen", a), faellt=W("fällt", a))
put("c12", S, f"""
  <div id="c12-cam" class="lay">
    {light("c12-l", 960, 520, 760, "rgba(255,226,180,.14)")}
    <svg class="actor" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
      <path d="M{X0},{Y0} L{X0 + WD + 40},{Y0} M{X0},{Y0} L{X0},{Y0 - HT - 60}" stroke="#CFC9BC" stroke-width="4" fill="none"/>
      <path id="c12-c" d="{path}" stroke="{AMBER}" stroke-width="8" fill="none" stroke-linecap="round" stroke-dasharray="{plen:.0f}" stroke-dashoffset="{plen:.0f}"/></svg>
    <div class="t" style="left:{X0 + WD - 260}px;top:{Y0 + 20}px;font-size:28px;font-weight:800;letter-spacing:.3em;color:{MUTED}">ANSPANNUNG →</div>
    <div class="t" style="left:{X0 - 30}px;top:{Y0 - HT - 110}px;font-size:28px;font-weight:800;letter-spacing:.3em;color:{MUTED}">LEISTUNG</div>
    <div id="c12-z1" class="t" style="left:{X0 + 40}px;top:{Y0 - 80}px;font-size:28px;font-weight:700;color:#6E717A;opacity:0">ZU ENTSPANNT</div>
    <div id="c12-z2" class="t" style="left:{X0 + WD // 2 - 80}px;top:{Y0 - HT - 70}px;font-size:28px;font-weight:800;color:{GREEN};opacity:0">OPTIMAL</div>
    <div id="c12-z3" class="t" style="left:{X0 + WD - 230}px;top:{Y0 - 80}px;font-size:28px;font-weight:700;color:{RED};opacity:0">PANIK</div>
    <div id="c12-dot" class="actor" style="left:{960 - 55}px;top:{540 - 55}px;width:110px;height:110px;opacity:0">{svgbox(_head_base() + _face("aha"), "-150 -180 300 300", 110, 110)}</div>
    <div class="t" style="left:130px;top:880px;font-size:28px;font-weight:600;letter-spacing:.14em;color:{MUTED}">NACH YERKES &amp; DODSON (1908), VEREINFACHT</div>
  </div>""", f"""
  fadeIn("#c12-cam", 0, 0.4);
  tl.to("#c12-c", {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 2.0, ease: "power2.inOut" }}, T.kurve - 0.2);
  tl.set("#c12-dot", {{ x: {X0 - 960}, y: {Y0 - 540} }}, 0);
  fadeIn("#c12-dot", T.steigt - 0.3, 0.3); fadeIn("#c12-z1", T.steigt - 0.3, 0.4);
  tl.to("#c12-dot", {{ keyframes: {json.dumps(kpts(0.0, 0.5))}, duration: 1.3, ease: "none" }}, T.steigt);
  fadeIn("#c12-z2", T.punkt - 0.2, 0.4);
  fadeIn("#c12-z3", T.kippt - 0.2, 0.4);
  tl.to("#c12-dot", {{ keyframes: {json.dumps(kpts(0.5, 0.82))}, duration: 0.9, ease: "none" }}, T.kippt);
  tl.to("#c12-dot", {{ keyframes: {json.dumps(kpts(0.82, 0.38, 10))}, duration: 1.0, ease: "none" }}, T.steil - 0.3);
  tl.to("#c12-dot", {{ keyframes: {json.dumps(kpts(0.38, 0.62, 6) + kpts(0.62, 0.96, 8))}, duration: 1.4, ease: "power2.in" }}, T.faellt - 0.2);
  tl.to("#c12-dot", {{ rotation: 200, duration: 1.0, ease: "power2.in" }}, T.faellt + 0.3);
  fadeOut("#c12-cam", T.end - 0.35, 0.35);
""", T12)
SFX.extend([(T12["kippt"], "whoosh", 0.3), (T12["faellt"] + 0.2, "whoosh", 0.35)])

chapter("c13", "kap3", 3, "DIE GENIE-ILLUSION")

# ================================================================ c14 Also doch? Nicht ganz.
S = "v_doch"; a = SEG[S][0]
T14 = dict(unter=W("Unter", a), nicht=W("Nicht", a))
put("c14", S, f"""
  <div id="c14-cam" class="lay">
    {otto_at("c14", 1150, ("happy", "excuse"))}
    <div id="c14-q" class="t cond" style="left:150px;top:320px;font-size:110px;opacity:0">UNTER DRUCK<br>BESSER?</div>
    <div id="c14-n" class="actor" style="left:170px;top:620px;padding:14px 30px;border:6px solid {RED};border-radius:12px;color:{RED};font-family:'Oswald';font-weight:700;font-size:80px;transform:rotate(-6deg);opacity:0">NICHT GANZ.</div>
  </div>""", r"""
  fadeIn("#c14-cam", 0, 0.3);
  tl.fromTo("#c14-q", { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.5, ease: "power4.out" }, T.unter - 0.2);
  tl.fromTo("#c14-n", { opacity: 0, scale: 2.4 }, { opacity: 1, scale: 1, duration: 0.22, ease: "expo.out" }, T.nicht);
  face("c14o", "happy", "excuse", T.nicht + 0.1);
  fadeOut("#c14-cam", T.end - 0.3, 0.3);
""", T14)
SFX.extend([(T14["nicht"], "boom", 0.35)])

# ================================================================ c15 Tice & Baumeister
S = "v_tice"; a = SEG[S][0]


def bars(cid, side, x, vals):
    out = f'<div class="t" style="left:{x}px;top:250px;width:520px;text-align:center;font-size:30px;font-weight:800;letter-spacing:.3em;color:{MUTED}">{side}</div>'
    for j, (lab, va, vb) in enumerate(vals):
        out += (f'<div class="t" style="left:{x}px;top:{330 + j * 150}px;font-size:28px;font-weight:700">{lab}</div>'
                f'<div id="{cid}-a{j}" class="actor" style="left:{x}px;top:{372 + j * 150}px;width:{va * 4}px;height:30px;background:{ORANGE};border-radius:6px;transform-origin:0 50%"></div>'
                f'<div id="{cid}-b{j}" class="actor" style="left:{x}px;top:{406 + j * 150}px;width:{vb * 4}px;height:30px;background:#6E717A;border-radius:6px;transform-origin:0 50%"></div>')
    return out


T15 = dict(tice=W("Tice", a), anfang=W("Anfang", a), ende=W("Ende", a), noten=W("Noten.", a))
put("c15", S, f"""
  <div id="c15-cam" class="lay">
    {light("c15-l", 960, 520, 760, "rgba(255,226,180,.14)")}
    <div id="c15-L" style="position:absolute;inset:0;opacity:0">{bars("c15L", "ANFANG DES SEMESTERS", 260, [("STRESS", 30, 70), ("KRANKHEIT", 25, 55), ("NOTEN", 70, 72)])}</div>
    <div id="c15-R" style="position:absolute;inset:0;opacity:0">{bars("c15R", "ENDE DES SEMESTERS", 1080, [("STRESS", 100, 75), ("KRANKHEIT", 90, 60), ("NOTEN", 45, 75)])}</div>
    <div id="c15-leg" class="t" style="left:260px;top:180px;font-size:28px;font-weight:700;opacity:0"><span style="color:{ORANGE}">■</span> AUFSCHIEBER &nbsp;&nbsp; <span style="color:#6E717A">■</span> ANDERE &nbsp;&nbsp; <span style="color:{MUTED}">(illustrativ)</span></div>
    <div id="c15-ft" class="t" style="left:130px;top:880px;font-size:28px;font-weight:600;letter-spacing:.14em;color:{MUTED};opacity:0">TICE &amp; BAUMEISTER (1997), PSYCHOLOGICAL SCIENCE</div>
  </div>""", r"""
  fadeIn("#c15-cam", 0, 0.3); tl.fromTo("#c15-cam", { scale: 1 }, { scale: 1.05, duration: T.end, ease: "none", transformOrigin: "960px 540px", immediateRender: false }, 0); fadeIn("#c15-ft", T.tice, 0.5); fadeIn("#c15-leg", T.tice + 0.3, 0.5);
  fadeIn("#c15-L", T.anfang - 0.4, 0.4);
  for (let j = 0; j < 3; j++) { tl.fromTo(`#c15La${j}`, { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.out" }, T.anfang + j * 0.12); tl.fromTo(`#c15Lb${j}`, { scaleX: 0 }, { scaleX: 1, duration: 0.6, ease: "power3.out" }, T.anfang + 0.06 + j * 0.12); }
  fadeIn("#c15-R", T.ende - 0.4, 0.4);
  for (let j = 0; j < 3; j++) { tl.fromTo(`#c15Ra${j}`, { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.out" }, T.ende + j * 0.5); tl.fromTo(`#c15Rb${j}`, { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.out" }, T.ende + 0.06 + j * 0.5); }
  tl.to("#c15Ra2", { backgroundColor: "#E2483D", duration: 0.3 }, T.noten);
  fadeOut("#c15-cam", T.end - 0.35, 0.35);
""".replace("c15La", "c15L-a").replace("c15Lb", "c15L-b").replace("c15Ra", "c15R-a").replace("c15Rb", "c15R-b"), T15)

# ================================================================ c16 Gedächtnistrick: Polaroids
S = "v_gedaechtnis"; a = SEG[S][0]
pol = [("GEKLAPPT ✓", GREEN, -6), ("KNAPP", MUTED, 4), ("PEINLICH", MUTED, -3), ("MITTELMÄSSIG", MUTED, 6)]
ph = "".join(f'<div id="c16-p{i}" class="actor" style="left:{230 + i * 380}px;top:300px;width:330px;height:400px;background:{PAPER};padding:20px 20px 0;'
             f'box-shadow:0 30px 60px rgba(0,0,0,.6);transform:rotate({r}deg);opacity:0"><div style="height:280px;background:#1C1F25;display:flex;align-items:center;justify-content:center">'
             f'{svgbox(_head_base() + _face("happy" if i == 0 else ["sad", "excuse", "tired"][i - 1]), "-150 -180 300 300", 200, 200)}</div>'
             f'<div style="margin-top:22px;text-align:center;font-family:\'Oswald\';font-weight:700;font-size:40px;color:{"#1E7A2E" if i == 0 else "#555"}">{t}</div></div>'
             for i, (t, c, r) in enumerate(pol))
T16 = dict(trick=W("Gedächtnistrick.", a), nacht=W("Nacht,", a), vergessen=W("vergessen", a), knapp=W("knapp,", a), peinlich=W("peinlich", a), mittel=W("mittelmäßig", a))
put("c16", S, f"""
  <div id="c16-cam" class="lay">
    {light("c16-l", 960, 500, 760, "rgba(255,226,180,.16)")}
    <div id="c16-h" class="t cond" style="left:0;right:0;top:170px;text-align:center;font-size:76px;opacity:0">DER GEDÄCHTNIS-TRICK</div>
    {ph}
  </div>""", r"""
  fadeIn("#c16-cam", 0, 0.3); fadeIn("#c16-h", T.trick - 0.3, 0.5);
  tl.fromTo("#c16-p0", { opacity: 0, y: -200, rotation: -20 }, { opacity: 1, y: 0, rotation: -6, duration: 0.6, ease: "back.out(1.4)" }, T.nacht - 0.2);
  [T.knapp, T.peinlich, T.mittel].forEach((t, i) => tl.fromTo(`#c16-p${i + 1}`, { opacity: 0, y: -200 }, { opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.4)" }, t - 0.15));
  tl.to(["#c16-p1", "#c16-p2", "#c16-p3"], { opacity: 0.2, filter: "blur(4px) grayscale(1)", duration: 0.8, ease: "power2.inOut" }, T.end - 1.4);
  tl.to("#c16-p0", { scale: 1.12, duration: 0.8, ease: "power2.inOut" }, T.end - 1.4);
  fadeOut("#c16-cam", T.end - 0.35, 0.35);
""", T16)
SFX.extend([(T16["nacht"] - 0.2, "pop", 0.4), (T16["knapp"] - 0.15, "pop", 0.3), (T16["peinlich"] - 0.15, "pop", 0.3), (T16["mittel"] - 0.15, "pop", 0.3)])

# ================================================================ c17 Pause-Moment (inkl. stiller Freeze)
S = "v_pause"; a = SEG[S][0]
SEG["v_pause_all"] = (SEG["v_pause"][0], SEG["pausefreeze"][1])
T17 = dict(pausier=W("Pausier", a), ehrlich=W("ehrlich:", a), wie=W("Wie", a))
put("c17", "v_pause_all", f"""
  <div id="c17-cam" class="lay">
    <div id="c17-ic" class="actor" style="left:860px;top:260px;width:200px;height:220px;opacity:0">
      <div style="position:absolute;left:30px;top:0;width:52px;height:220px;background:#FFF;border-radius:10px"></div>
      <div style="position:absolute;left:118px;top:0;width:52px;height:220px;background:#FFF;border-radius:10px"></div></div>
    <div id="c17-q" class="t cond" style="left:0;right:0;top:560px;text-align:center;font-size:84px;opacity:0">WIE OFT HAT ES BEI DIR<br><span style="color:{AMBER}">WIRKLICH</span> GEKLAPPT?</div>
    <div id="c17-bar" class="actor" style="left:660px;top:820px;width:600px;height:8px;background:{AMBER};border-radius:4px;transform-origin:0 50%;opacity:0"></div>
  </div>""", r"""
  tl.fromTo("#c17-ic", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.25, ease: "expo.out" }, T.pausier);
  tl.fromTo("#c17-q", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, T.wie - 0.2);
  tl.fromTo("#c17-bar", { opacity: 1, scaleX: 1 }, { opacity: 1, scaleX: 0, duration: T.end - T.wie - 0.4, ease: "none" }, T.wie);
  fadeOut("#c17-cam", T.end - 0.3, 0.3);
""", T17)
SFX.extend([(T17["pausier"], "scratch", 0.55)])

chapter("c18", "kap4", 4, "DER DEADLINE-HACK")

# ================================================================ c19 Gute Nachricht: Turbo-Tacho
S = "v_gut"; a = SEG[S][0]
gauge = f'''<path d="M-200,0 A200,200 0 0 1 200,0" fill="none" stroke="#2A2E36" stroke-width="36"/>
  <path d="M-200,0 A200,200 0 0 1 200,0" fill="none" stroke="{ORANGE}" stroke-width="36" stroke-dasharray="628" stroke-dashoffset="628" id="c19-arc"/>
  <g id="c19-needle"><path d="M-8,0 L0,-170 L8,0 Z" fill="#FFF"/><circle r="22" fill="#FFF"/></g>'''
T19 = dict(turbo=W("Turbo", a), ohne=W("ohne", a))
put("c19", S, f"""
  <div id="c19-cam" class="lay">
    {light("c19-l", 960, 560, 600, "rgba(255,150,80,.18)")}
    <div class="actor" style="left:710px;top:300px;width:500px;height:300px">{svgbox(gauge, "-250 -230 500 280", 500, 280)}</div>
    <div id="c19-t" class="t cond" style="left:0;right:0;top:640px;text-align:center;font-size:96px;opacity:0">TURBO OHNE<br><span style="color:{AMBER}">FREITAGNACHT</span></div>
  </div>""", r"""
  fadeIn("#c19-cam", 0, 0.3);
  tl.fromTo("#c19-needle", { rotation: -90, svgOrigin: "0 0" }, { rotation: 75, duration: 1.2, ease: "elastic.out(1, 0.5)" }, T.turbo - 0.2);
  tl.to("#c19-arc", { attr: { "stroke-dashoffset": 80 }, duration: 1.2, ease: "power3.out" }, T.turbo - 0.2);
  fadeIn("#c19-t", T.ohne, 0.5, { from: { y: 30 }, to: { y: 0 } });
  fadeOut("#c19-cam", T.end - 0.3, 0.3);
""", T19)
SFX.extend([(T19["turbo"] - 0.2, "whoosh", 0.4)])

# ================================================================ c20 Ariely & Wertenbroch
S = "v_ariely"; a = SEG[S][0]
rows = [("FESTE TERMINE", [0.33, 0.66, 1.0]), ("SELBST GESETZT", [0.6, 0.85, 1.0]), ("EIN TERMIN AM ENDE", [1.0])]
rh = ""
for r, (lab, ds) in enumerate(rows):
    y = 330 + r * 150
    rh += (f'<div id="c20-r{r}" style="position:absolute;inset:0;opacity:0"><div class="t" style="left:180px;top:{y - 18}px;font-size:30px;font-weight:800;letter-spacing:.1em">{lab}</div>'
           f'<div class="actor" style="left:640px;top:{y}px;width:1000px;height:4px;background:#5A606B"></div>'
           + "".join(f'<div id="c20-f{r}{k}" class="actor" style="left:{640 + d * 1000 - 18}px;top:{y - 40}px;font-size:46px;opacity:0">🚩</div>' for k, d in enumerate(ds)) + "</div>")
pod = [(1, "FESTE TERMINE", 820, 220, GREEN), (2, "SELBST GESETZT", 540, 160, AMBER), (3, "EIN TERMIN", 1100, 110, RED)]
ph20 = "".join(f'<div id="c20-p{n}" class="actor" style="left:{x}px;top:{760 - h}px;width:260px;height:{h}px;background:#22262E;border:3px solid {c};border-radius:10px 10px 0 0;transform-origin:50% 100%;opacity:0">'
               f'<div class="t cond" style="left:0;right:0;top:14px;text-align:center;font-size:72px;color:{c}">{n}</div>'
               f'<div class="t" style="left:-40px;right:-40px;top:{h + 14}px;text-align:center;font-size:26px;font-weight:800;letter-spacing:.08em">{lab}</div></div>'
               for n, lab, x, h, c in pod)
T20 = dict(dan=W("Dan", a), gruppe=W("Gruppe", a), selbst=W("selbst", a), einen=W("einen", W("hatte", W("Und", a))), ergebnis=W("Ergebnis:", a),
           also=W("Also:", a), vorne=W("vorne.", a))
put("c20", S, f"""
  <div id="c20-cam" class="lay">
    {light("c20-l", 960, 520, 800, "rgba(255,226,180,.14)")}
    <div id="c20-tl" style="position:absolute;inset:0">{rh}</div>
    <div id="c20-pod" style="position:absolute;inset:0;opacity:0">{ph20}</div>
    <div id="c20-lt" class="t" style="left:130px;top:700px;opacity:0">
      <div style="width:440px;height:3px;background:#FFF"></div>
      <div class="cond" style="margin-top:16px;font-size:60px;letter-spacing:.08em;">ARIELY &amp; WERTENBROCH</div>
      <div style="margin-top:10px;font-size:28px;letter-spacing:.24em;color:{MUTED};font-weight:600;">PSYCHOLOGICAL SCIENCE · 2002</div></div>
    <div id="c20-v" class="lay" style="opacity:0">
      <div class="actor" style="left:260px;top:560px;width:1400px;height:4px;background:#5A606B"></div>
      <div id="c20-flag" class="actor" style="left:1560px;top:470px;font-size:90px">🚩</div>
      <div class="t cond" style="left:0;right:0;top:300px;text-align:center;font-size:100px;">HOL DIR DIE DEADLINE<br><span style="color:{AMBER}">NACH VORNE</span></div></div>
  </div>""", r"""
  fadeIn("#c20-cam", 0, 0.3);
  fadeIn("#c20-lt", T.dan, 0.5); fadeOut("#c20-lt", T.gruppe - 0.4, 0.3);
  const rr = [T.gruppe, T.selbst, T.einen];
  [0, 1, 2].forEach(r => { fadeIn(`#c20-r${r}`, rr[r] - 0.2, 0.4); for (let k = 0; k < [3, 3, 1][r]; k++) tl.fromTo(`#c20-f${r}${k}`, { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }, rr[r] + 0.3 + k * 0.25); });
  tl.to("#c20-tl", { opacity: 0, duration: 0.4 }, T.ergebnis - 0.3);
  fadeIn("#c20-pod", T.ergebnis - 0.2, 0.3);
  [1, 2, 3].forEach((n, i) => tl.fromTo(`#c20-p${n}`, { opacity: 0, scaleY: 0 }, { opacity: 1, scaleY: 1, duration: 0.5, ease: "back.out(1.6)" }, T.ergebnis + 0.3 + i * 0.5));
  tl.to("#c20-pod", { opacity: 0, duration: 0.4 }, T.also - 0.3);
  fadeIn("#c20-v", T.also - 0.1, 0.4);
  tl.fromTo("#c20-flag", { x: 0 }, { x: -1100, duration: 1.4, ease: "power3.inOut" }, T.vorne - 0.8);
  fadeOut("#c20-cam", T.end - 0.3, 0.3);
""", T20)
SFX.extend([(T20["ergebnis"] + 0.3 + i * 0.5, "pop", 0.45) for i in range(3)] + [(T20["vorne"] - 0.8, "whoosh", 0.4)])

# ================================================================ c21 Hack 1: Zwischen-Deadlines
S = "v_hack1"; a = SEG[S][0]
pieces = "".join(f'<div id="c21-q{i}" class="actor" style="left:{360 + i * 310}px;top:420px;width:290px;height:200px;background:{ORANGE};border-radius:14px;'
                 f'display:flex;align-items:center;justify-content:center;font-family:\'Oswald\';font-weight:700;font-size:40px;color:#1E1E1E">TEIL {i + 1}</div>'
                 f'<div id="c21-tg{i}" class="actor" style="left:{385 + i * 310}px;top:650px;padding:8px 18px;border-radius:10px;background:#22262E;border:2px solid {AMBER};font-size:30px;font-weight:800;opacity:0">{d}</div>'
                 for i, d in enumerate(["MO", "DI", "MI", "DO"]))
T21 = dict(teil=W("Teil", a), stueck=W("Stück", a))
put("c21", S, f"""
  <div id="c21-cam" class="lay">
    {header("c21", "HACK 1", "ZWISCHEN-DEADLINES")}
    <div id="c21-big" class="actor" style="left:360px;top:420px;width:1220px;height:200px;background:{ORANGE};border-radius:14px;display:flex;align-items:center;justify-content:center;font-family:'Oswald';font-weight:700;font-size:80px;color:#1E1E1E;opacity:0">PRÄSENTATION</div>
    <div id="c21-pc" style="position:absolute;inset:0;opacity:0">{pieces}</div>
    {cursor("c21", 1500, 900)}
  </div>""", HEADER_JS("c21") + r"""
  fadeIn("#c21-cam", 0, 0.3);
  popIn("#c21-big", 0.6, 0.5);
  tl.set("#c21-big", { opacity: 0 }, T.teil + 0.3); tl.set("#c21-pc", { opacity: 1 }, T.teil + 0.3);
  [0, 1, 2, 3].forEach(i => tl.fromTo(`#c21-q${i}`, { x: -i * 20 }, { x: 0, y: [-20, 15, -10, 20][i], rotation: [-3, 2, -2, 3][i], duration: 0.6, ease: "back.out(2)" }, T.teil + 0.3));
  fadeIn("#c21-cur", T.stueck - 0.6, 0.2);
  [0, 1, 2, 3].forEach(i => { move("#c21-cur", -1040 + i * 310, -230, T.stueck - 0.4 + i * 0.55, 0.35); click("c21", T.stueck + i * 0.55); popIn(`#c21-tg${i}`, T.stueck + 0.05 + i * 0.55, 0.35); });
  fadeOut("#c21-cam", T.end - 0.3, 0.3);
""", T21)
SFX.extend([(T21["teil"] + 0.3, "whoosh", 0.35)] + [(T21["stueck"] + i * 0.55, "click", 0.7) for i in range(4)])

# ================================================================ c22 Hack 2: öffentlich machen (Chat)
S = "v_hack2"; a = SEG[S][0]
msg = "Bis Mittwoch ist die Präsentation fertig!"
mh = "".join(f'<span id="c22-c{i}" style="opacity:0">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(msg))
T22 = dict(sag=W("Sag", a), ploetzlich=W("Plötzlich", a), echt=W("echt.", a))
put("c22", S, f"""
  <div id="c22-cam" class="lay">
    {header("c22", "HACK 2", "MACH SIE ÖFFENTLICH")}
    <div id="c22-win" class="actor card" style="left:560px;top:340px;width:800px;height:500px;opacity:0">
      <div style="height:70px;border-bottom:2px solid #3A3F48;display:flex;align-items:center;padding:0 30px;font-size:30px;font-weight:800">💬 Team-Chat</div>
      <div id="c22-bub" class="actor" style="right:30px;top:230px;max-width:600px;padding:18px 24px;border-radius:20px 20px 4px 20px;background:#2D6CDF;font-size:32px;font-weight:600;opacity:0">{msg} <span id="c22-ok" style="opacity:0;color:#9FD3FF">✓✓</span></div>
      <div style="position:absolute;left:20px;right:20px;bottom:20px;height:70px;border-radius:14px;background:#22262E;display:flex;align-items:center;padding:0 20px;font-size:30px"><span id="c22-in">{mh}</span></div>
      <div id="c22-send" class="actor" style="right:30px;bottom:30px;width:52px;height:52px;border-radius:50%;background:#2D6CDF;display:flex;align-items:center;justify-content:center;font-size:28px">➤</div></div>
    <div id="c22-e" class="t cond" style="left:0;right:0;top:860px;text-align:center;font-size:56px;color:{AMBER};opacity:0">PLÖTZLICH IST DIE DEADLINE ECHT.</div>
    {cursor("c22", 1500, 900)}
  </div>""", HEADER_JS("c22") + f"""
  fadeIn("#c22-cam", 0, 0.3);
  tl.fromTo("#c22-win", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power4.out" }}, 0.6);
  for (let i = 0; i < {len(msg)}; i++) tl.fromTo(`#c22-c${{i}}`, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, T.sag + i * 0.04);
  fadeIn("#c22-cur", T.sag + 0.5, 0.2);
  move("#c22-cur", -170, -160, T.sag + 0.6, 0.6);
  click("c22", T.sag + {len(msg) * 0.04 + 0.2:.2f});
  tl.set("#c22-in", {{ opacity: 0 }}, T.sag + {len(msg) * 0.04 + 0.25:.2f});
  tl.fromTo("#c22-bub", {{ opacity: 0, y: 120, scale: 0.8 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "back.out(1.6)" }}, T.sag + {len(msg) * 0.04 + 0.25:.2f});
  fadeIn("#c22-ok", T.ploetzlich - 0.3, 0.3);
  fadeIn("#c22-e", T.ploetzlich, 0.5);
  fadeOut("#c22-cam", T.end - 0.3, 0.3);
""", T22)
SFX.extend([(T22["sag"], "typing", 0.25), (T22["sag"] + len(msg) * 0.04 + 0.2, "click", 0.7), (T22["sag"] + len(msg) * 0.04 + 0.25, "send", 0.6)])

# ================================================================ c23 Hack 3: Mini-Countdown
S = "v_hack3"; a = SEG[S][0]
T23 = dict(timer=W("Timer", a), freitag=W("Freitag,", a))
put("c23", S, f"""
  <div id="c23-cam" class="lay">
    {header("c23", "HACK 3", "DER MINI-COUNTDOWN")}
    <svg class="actor" style="left:310px;top:330px" width="440" height="440" viewBox="0 0 440 440">
      <circle cx="220" cy="220" r="190" fill="#16181D" stroke="#3A3F48" stroke-width="6"/>
      <circle id="c23-arc" cx="220" cy="220" r="170" fill="none" stroke="{ORANGE}" stroke-width="22" stroke-dasharray="1068" stroke-dashoffset="0" transform="rotate(-90 220 220)"/></svg>
    <div id="c23-t" class="t" style="left:310px;width:440px;top:500px;text-align:center;font-family:'Space Mono';font-weight:700;font-size:96px;opacity:0">25:00</div>
    <div id="c23-as" class="t cond" style="left:900px;top:380px;font-size:64px;opacity:0">TU SO, ALS WÄRE ES …</div>
    {clock_html("c23-clk", "FR 23:35", 900, 480, 120)}
  </div>""", HEADER_JS("c23") + r"""
  fadeIn("#c23-cam", 0, 0.3); fadeIn("#c23-t", T.timer - 0.2, 0.3);
  for (let i = 1; i <= 25; i++) tl.set("#c23-t", { textContent: `${String(25 - i).padStart(2, "0")}:${String((i * 37) % 60).padStart(2, "0")}` }, T.timer + 0.4 + i * 0.12);
  tl.to("#c23-arc", { attr: { "stroke-dashoffset": 1068 }, duration: 3.1, ease: "none" }, T.timer + 0.4);
  fadeIn("#c23-as", T.freitag - 0.8, 0.4);
  tl.fromTo("#c23-clk", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }, T.freitag);
  fadeOut("#c23-cam", T.end - 0.3, 0.3);
""", T23)
SFX.extend([(T23["timer"] + 0.4, "tick", 0.3), (T23["freitag"], "boom", 0.3)])

# ================================================================ c24 Hack 4: Wenn-dann-Plan (Puzzle)
S = "v_hack4"; a = SEG[S][0]
T24 = dict(nicht=W("Nicht:", a), wenn=W("Wenn", a), dann=W("dann", a), goll=W("Gollwitzer", a))
put("c24", S, f"""
  <div id="c24-cam" class="lay">
    {header("c24", "HACK 4", "DER WENN-DANN-PLAN")}
    <div id="c24-bad" class="t" style="left:180px;top:380px;font-family:'EB Garamond';font-style:italic;font-size:54px;color:{MUTED};opacity:0">„Ich mach das diese Woche.“</div>
    <div id="c24-x" class="actor" style="left:170px;top:415px;width:620px;height:6px;background:{RED};transform-origin:0 50%"></div>
    <div id="c24-a" class="actor" style="left:300px;top:520px;width:640px;height:170px;background:#2D6CDF;border-radius:20px 0 0 20px;display:flex;flex-direction:column;justify-content:center;padding-left:40px;opacity:0">
      <div style="font-size:28px;font-weight:800;letter-spacing:.3em;opacity:.8">WENN</div><div class="cond" style="font-size:60px">DIENSTAG, 18 UHR</div></div>
    <div id="c24-b" class="actor" style="left:940px;top:520px;width:640px;height:170px;background:{ORANGE};border-radius:0 20px 20px 0;display:flex;flex-direction:column;justify-content:center;padding-left:60px;color:#1E1E1E;opacity:0">
      <div style="font-size:28px;font-weight:800;letter-spacing:.3em;opacity:.8">DANN</div><div class="cond" style="font-size:60px">DATEI ÖFFNEN</div>
      <div style="position:absolute;left:-36px;top:55px;width:60px;height:60px;border-radius:50%;background:{ORANGE}"></div></div>
    {foot("c24", "GOLLWITZER (1999), AMERICAN PSYCHOLOGIST")}
  </div>""", HEADER_JS("c24") + r"""
  fadeIn("#c24-cam", 0, 0.3);
  fadeIn("#c24-bad", T.nicht, 0.4);
  tl.fromTo("#c24-x", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.inOut" }, T.nicht + 1.2);
  tl.fromTo("#c24-a", { opacity: 0, x: -300 }, { opacity: 1, x: 0, duration: 0.6, ease: "power4.out" }, T.wenn - 0.1);
  tl.fromTo("#c24-b", { opacity: 0, x: 500 }, { opacity: 1, x: 80, duration: 0.5, ease: "power3.out" }, T.dann - 0.3);
  tl.to("#c24-b", { x: 0, duration: 0.25, ease: "back.out(3)" }, T.dann + 0.25);
  tl.to(["#c24-a", "#c24-b"], { scale: 1.04, duration: 0.15, yoyo: true, repeat: 1 }, T.dann + 0.5);
  fadeIn("#c24-ft", T.goll, 0.5);
  fadeOut("#c24-cam", T.end - 0.3, 0.3);
""", T24)
SFX.extend([(T24["wenn"] - 0.1, "whoosh", 0.3), (T24["dann"] + 0.5, "click", 0.9)])

# ================================================================ c25 Auflösung: Mittwoch fertig, Freitag schläft Otto
S = "v_aufl"; a = SEG[S][0]
days = "".join(f'<div id="c25-d{i}" class="actor" style="left:{250 + i * 205}px;top:300px;width:180px;height:150px;border-radius:14px;background:#22262E;border:2px solid #3A3F48;'
               f'font-size:40px;font-weight:800;display:flex;align-items:center;justify-content:center">{d}'
               + (f'<div id="c25-ok" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:110px;color:{GREEN};opacity:0">✓</div>' if d == "MI" else "")
               + '</div>' for i, d in enumerate(["MO", "DI", "MI", "DO", "FR", "SA", "SO"]))
zz = "".join(f'<div id="c25-z{i}" class="t cond" style="left:{800 + i * 60}px;top:{400 - i * 70}px;font-size:{60 + i * 20}px;color:{AMBER};opacity:0">Z</div>' for i in range(3))
T25 = dict(mittwoch=W("Mittwochabend", a), freitag=W("Freitag", a), geschlafen=W("geschlafen.", a))
put("c25", S, f"""
  <div id="c25-cam" class="lay">
    {light("c25-l", 960, 400, 800, "rgba(255,226,180,.14)")}
    <div id="c25-cal" style="position:absolute;inset:0">{days}</div>
    <div id="c25-night" class="lay" style="opacity:0">
      {light("c25-nl", 860, 560, 420, "rgba(120,150,255,.16)")}
      {clock_html("c25-clk", "FR 23:58", 1300, 220, 70)}
      <div class="actor" style="left:560px;top:640px;width:800px;height:70px;border-radius:20px;background:#2B3140;border:3px solid #111"></div>
      <div class="actor" style="left:600px;top:560px;width:240px;height:110px;border-radius:50px;background:#E6E2DA;border:3px solid #111"></div>
      <div class="actor" style="left:600px;top:400px;width:240px;height:240px">{svgbox(_head_base() + _face("happy"), "-150 -180 300 300", 240, 240)}</div>
      <div class="actor" style="left:800px;top:560px;width:540px;height:110px;border-radius:24px 40px 40px 24px;background:#3D4A6B;border:3px solid #111"></div>
      {zz}</div>
  </div>""", r"""
  fadeIn("#c25-cam", 0, 0.3);
  for (let i = 0; i < 7; i++) tl.fromTo(`#c25-d${i}`, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, 0.3 + i * 0.05);
  tl.to("#c25-d2", { borderColor: "#7CFF8A", scale: 1.08, duration: 0.3 }, T.mittwoch);
  tl.fromTo("#c25-ok", { opacity: 0, scale: 2 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, T.mittwoch + 0.1);
  tl.to("#c25-cal", { opacity: 0, y: -60, duration: 0.5 }, T.freitag - 0.4);
  fadeIn("#c25-night", T.freitag - 0.2, 0.5); fadeIn("#c25-clk", T.freitag, 0.3);
  [0, 1, 2].forEach(i => tl.fromTo(`#c25-z${i}`, { opacity: 0, y: 20 }, { opacity: 1, y: -20, duration: 0.8, ease: "power2.out" }, T.geschlafen - 0.3 + i * 0.35));
  fadeOut("#c25-cam", T.end - 0.3, 0.3);
""", T25)
SFX.extend([(T25["mittwoch"] + 0.1, "pop", 0.5)])

# ================================================================ c26 Umfrage-Auflösung: Kommentare
S = "v_umfrage2"; a = SEG[S][0]
opts = "".join(f'<div class="actor" style="left:60px;top:{200 + i * 110}px;width:700px;height:90px;border-radius:16px;background:#22262E;border:2px solid #3A3F48;display:flex;align-items:center;gap:24px;padding:0 24px">'
               f'<div style="width:52px;height:52px;border-radius:50%;background:{AMBER};color:#111;font-size:30px;font-weight:900;display:flex;align-items:center;justify-content:center">{k}</div>'
               f'<div style="font-size:36px;font-weight:700">{v}</div></div>' for i, (k, v) in enumerate([("A", "Früh"), ("B", "Pünktlich"), ("C", "In letzter Minute")]))
T26 = dict(antwort=W("Antwort", a), kommentare=W("Kommentare.", a), c=W("C-Menschen", a))
put("c26", S, f"""
  <div id="c26-cam" class="lay">
    {light("c26-l", 960, 500, 760, "rgba(255,226,180,.14)")}
    <div id="c26-card" class="actor card" style="left:560px;top:180px;width:820px;height:620px;opacity:0">
      <div class="t" style="left:60px;top:50px;font-size:28px;font-weight:800;letter-spacing:.4em;color:{AMBER}">UMFRAGE · AUFLÖSUNG</div>
      <div class="t" style="left:60px;top:110px;font-size:36px;font-weight:700">Was war deine Antwort?</div>{opts}
      <div id="c26-btn" class="actor" style="left:60px;top:540px;padding:14px 30px;border-radius:12px;background:#2D6CDF;font-size:32px;font-weight:800">💬 KOMMENTIEREN</div></div>
    {cursor("c26", 1500, 900)}
  </div>""", r"""
  fadeIn("#c26-cam", 0, 0.3);
  tl.fromTo("#c26-card", { opacity: 0, y: 80, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "power4.out" }, 0.3);
  fadeIn("#c26-cur", T.antwort, 0.2);
  move("#c26-cur", -780, -170, T.kommentare - 0.8, 0.7);
  click("c26", T.kommentare);
  tl.to("#c26-btn", { scale: 1.08, duration: 0.15, yoyo: true, repeat: 1 }, T.kommentare);
  fadeOut("#c26-cam", T.end - 0.3, 0.3);
""", T26)
SFX.extend([(T26["kommentare"], "click", 0.9)])

# ================================================================ c27 Brücke: Dusche → Idee
S = "v_bruecke"; a = SEG[S][0]
bulb = f'''<g stroke="#111" stroke-width="5"><path d="M-30,30 a60,60 0 1 1 60,0 l0,40 l-60,0 Z" fill="#FFD43B"/><rect x="-32" y="70" width="64" height="26" rx="6" fill="#9AA0A6"/></g>'''
T27 = dict(dusche=W("Dusche", a), naechstes=W("nächstes", a))
put("c27", S, f"""
  <div id="c27-cam" class="lay">
    <div id="c27-drop" class="actor" style="left:930px;top:150px;width:60px;height:80px;border-radius:50% 50% 50% 50% / 60% 60% 40% 40%;background:#8EC5FF;opacity:0"></div>
    <div id="c27-rip" class="actor" style="left:810px;top:560px;width:300px;height:80px;border-radius:50%;border:4px solid #8EC5FF;opacity:0"></div>
    {light("c27-gl", 960, 430, 300, "rgba(255,220,120,.6)", 0)}
    <div id="c27-b" class="actor" style="left:860px;top:300px;width:200px;height:230px;opacity:0">{svgbox(bulb, "-100 -110 200 230", 200, 230)}</div>
    <div id="c27-t" class="t" style="left:0;right:0;top:700px;text-align:center;font-size:30px;font-weight:800;letter-spacing:.4em;color:{MUTED};opacity:0">NÄCHSTE FOLGE</div>
    <div id="c27-n" class="t cond" style="left:0;right:0;top:750px;text-align:center;font-size:76px;opacity:0">DIE PERFEKTE IDEE UNTER DER DUSCHE</div>
  </div>""", r"""
  tl.fromTo("#c27-drop", { opacity: 1, y: 0 }, { opacity: 1, y: 400, duration: 0.6, ease: "power2.in" }, T.dusche - 0.6);
  tl.set("#c27-drop", { opacity: 0 }, T.dusche);
  tl.fromTo("#c27-rip", { opacity: 1, scale: 0.2 }, { opacity: 0, scale: 1.6, duration: 0.9, ease: "power2.out" }, T.dusche);
  tl.fromTo("#c27-b", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2)" }, T.dusche + 0.6);
  tl.fromTo("#c27-gl", { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.1 }, { opacity: 0.3, duration: 0.08 }, { opacity: 1, duration: 0.2 }] }, T.dusche + 1.0);
  fadeIn("#c27-t", T.dusche + 1.2, 0.4); fadeIn("#c27-n", T.dusche + 1.4, 0.5);
  fadeOut("#c27-cam", T.end - 0.3, 0.3);
""", T27)
SFX.extend([(T27["dusche"], "drop", 0.6)])

# ================================================================ c28 Abspann
put("c28", "endcard", f"""
  <div id="c28-ch" class="t cond" style="left:0;right:0;top:190px;text-align:center;font-size:70px;letter-spacing:.3em;opacity:0">OTTO NORMALPSYCHE</div>
  <div id="c28-sub" class="t" style="left:0;right:0;top:285px;text-align:center;font-size:28px;font-weight:600;letter-spacing:.4em;color:{MUTED};opacity:0">WARUM WIR TUN, WAS WIR TUN</div>
  <div id="c28-sb" class="actor" style="left:300px;top:420px;width:300px;height:300px;border-radius:50%;border:2px dashed #555;opacity:0"></div>
  <div id="c28-sbt" class="t" style="left:300px;width:300px;top:740px;text-align:center;font-size:28px;font-weight:700;letter-spacing:.3em;opacity:0">ABONNIEREN</div>
  <div id="c28-nv" class="actor" style="left:900px;top:400px;width:720px;height:405px;border:2px dashed #555;opacity:0"></div>
  <div id="c28-nt" class="t" style="left:900px;top:350px;font-size:28px;font-weight:700;letter-spacing:.4em;color:{AMBER};opacity:0">NÄCHSTE FOLGE</div>""", r"""
  fadeIn("#c28-ch", 0.3, 0.8); fadeIn("#c28-sub", 0.8, 0.6);
  ["#c28-sb", "#c28-sbt", "#c28-nv", "#c28-nt"].forEach((s, i) => fadeIn(s, 1.2 + i * 0.15, 0.6));
""", {})
SFX.extend([(SEG["endcard"][0] + 0.3, "whoosh", 0.3)])
