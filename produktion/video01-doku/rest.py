# Wird von gen.py per exec() ausgeführt. Szenen 9–34 von Video 01 im Doku-Look.
# Verfügbar aus gen.py: W, SEG, scene, light, typed, actor, otto_svg, svgbox, art, chapter, HOSTS,
#                       MUTED, PAPER, RED, ORANGE, INK, OTTO_TOP, sock, sparkle, spray, _head_base, _face
AMBER, WARM = "#E8C27A", "rgba(255,226,180,.28)"


def w(word, sid, after=None):
    a = SEG[sid][0]
    return W(word, a if after is None else W(after, a)) - a


def dur(sid):
    return SEG[sid][1] - SEG[sid][0]


def otto_block(cid, x, faces, **kw):
    lc = kw.pop("light_col", WARM)
    return (light(f"{cid}-ol", x + 300, 470, 520, lc)
            + f'<div class="floor" style="left:{x + 60}px;top:820px;width:480px;height:70px;"></div>'
            + actor(f"{cid}-otto", x, OTTO_TOP, 600, 760, otto_svg(f"{cid}o", faces, **kw)))


def header(cid, kicker, title, x=130):
    return (f'<div id="{cid}-hk" class="t" style="left:{x}px;top:180px;font-size:28px;font-weight:700;letter-spacing:.4em;color:{AMBER};">{kicker}</div>'
            f'<div id="{cid}-ht" class="t cond" style="left:{x}px;top:225px;font-size:92px;line-height:1;letter-spacing:.04em;">{title}</div>')


def foot(cid, text):
    return f'<div id="{cid}-ft" class="t" style="left:130px;top:880px;font-size:28px;font-weight:600;letter-spacing:.14em;color:{MUTED};">{text}</div>'


def lower(cid, name, role, x=130, y=700):
    return (f'<div id="{cid}-lt" class="t" style="left:{x}px;top:{y}px;">'
            f'<div id="{cid}-ltl" style="width:420px;height:3px;background:#FFF;transform-origin:0 50%;"></div>'
            f'<div class="cond" style="margin-top:16px;font-size:72px;letter-spacing:.12em;line-height:1;">{name}</div>'
            f'<div style="margin-top:12px;font-size:28px;letter-spacing:.24em;color:{MUTED};font-weight:600;">{role}</div></div>')


def lower_js(cid, t_in, t_out):
    return (f'tl.fromTo("#{cid}-ltl", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.7, ease: "power3.out" }}, {t_in:.3f});'
            f'fadeIn("#{cid}-lt", {t_in:.3f}, 0.6); fadeOut("#{cid}-lt", {t_out:.3f}, 0.4);')


def cam_js(cid):
    return (f'tl.fromTo("#{cid}-cam", {{ scale: 1 }}, {{ scale: 1.04, duration: T.end, ease: "none", transformOrigin: "960px 540px" }}, 0);'
            f'fadeIn("#{cid}-cam", 0, 0.5); tl.to("#{cid}-cam", {{ opacity: 0, duration: 0.4, ease: "power2.in" }}, T.end - 0.4);')


def html_cam(cid, inner, outside=""):
    return f'<div id="{cid}-cam" class="lay">{inner}</div>{outside}'


def put(sid, cid, html, js, T, push=True):
    T["end"] = dur(sid)
    cj = cam_js(cid) if push else (f'fadeIn("#{cid}-cam", 0, 0.4); tl.to("#{cid}-cam", {{ opacity: 0, duration: 0.4 }}, T.end - 0.4);')
    scene(cid, html, cj + "\n" + js, T)
    HOSTS.append((cid, *SEG[sid]))


def svg_actor(id_, x, y, w_, h_, inner, vb, extra=""):
    return f'<div id="{id_}" class="actor" style="left:{x}px;top:{y}px;width:{w_}px;height:{h_}px;{extra}">{svgbox(inner, vb, w_, h_)}</div>'


# ------------------------------------------------------------ 09 Zahlen
S = "s09_zahlen"
grid = "".join(svg_actor(f"k09-p{i}", 1080 + (i % 5) * 130, 380 + (i // 5) * 125, 100, 120, art.person(0, 0, "#6B6F78", 1.0), "-50 -70 100 120")
               + (svg_actor(f"k09-q{i}", 1080 + (i % 5) * 130, 380 + (i // 5) * 125, 100, 120, art.person(0, 0, AMBER, 1.0), "-50 -70 100 120", "opacity:0") if i % 5 == 0 else "")
               for i in range(20))
put(S, "k09", html_cam("k09", f"""
    {light("k09-l", 560, 470, 560, WARM)}
    <div id="k09-num" class="t cond" style="left:190px;top:300px;font-size:300px;line-height:1;"><span id="k09-n">0</span><span style="font-size:200px"> %</span></div>
    <div id="k09-lab" class="t" style="left:200px;top:640px;font-size:34px;font-weight:700;letter-spacing:.2em;line-height:1.5;">DER STUDIERENDEN SCHIEBEN<br>REGELMÄSSIG AUF</div>
    <div id="k09-gl" class="t" style="left:1080px;top:300px;font-size:30px;font-weight:700;letter-spacing:.2em;color:{AMBER};">JEDER 5. ERWACHSENE: CHRONISCH</div>
    {grid}
    {foot("k09", "QUELLE: STEEL (2007), PSYCHOLOGICAL BULLETIN")}"""),
    r"""
  fadeIn("#k09-num", 0.6, 0.8);
  tl.fromTo("#k09-n", { textContent: 0 }, { textContent: 95, duration: 1.3, ease: "power2.out", snap: { textContent: 1 } }, T.p95 - 0.2);
  fadeIn("#k09-lab", T.p95 + 0.4, 0.6); fadeIn("#k09-ft", T.steel, 0.6);
  for (let i = 0; i < 20; i++) fadeIn(`#k09-p${i}`, T.fuenfte - 0.4 + i * 0.03, 0.4);
  fadeIn("#k09-gl", T.fuenfte, 0.6);
  [0, 5, 10, 15].forEach((i, j) => fadeIn(`#k09-q${i}`, T.chron + j * 0.12, 0.4));
  tl.to("#k09-cam", { opacity: 0.12, duration: 0.6, ease: "power2.inOut" }, T.mensch - 0.5);
  fadeIn("#k09-fin", T.mensch - 0.35, 0.5, { from: { scale: 1.06 }, to: { scale: 1 } });
  fadeOut("#k09-fin", T.end - 0.3, 0.28);
""",
    {"p95": w("95", S), "steel": w("Steel", S), "fuenfte": w("fünfte", S), "chron": w("chronisch.", S), "mensch": w("menschlich.", S)})
# Schlusszeile außerhalb der Kamera, damit sie hell bleibt
_s = open(f"{HERE}/compositions/k09.html").read().replace(
    '<div id="k09-cam" class="lay">',
    f'<div id="k09-fin" class="t cond" style="left:0;right:0;top:450px;text-align:center;font-size:120px;letter-spacing:.08em;opacity:0;z-index:5;">EINFACH MENSCHLICH.</div><div id="k09-cam" class="lay">')
open(f"{HERE}/compositions/k09.html", "w").write(_s)

# ------------------------------------------------------------ 10 Zitat
S = "s10_zitat"
q = ["„Aufschieben ist kein Problem", "des Zeitmanagements, sondern", "der Gefühlsregulation.“"]
put(S, "k10", html_cam("k10", f"""
    {light("k10-l", 960, 480, 700, "rgba(255,226,180,.20)")}
    {"".join(f'<div id="k10-q{i}" class="t" style="left:0;right:0;top:{300 + i * 96}px;text-align:center;font-family:EB Garamond;font-style:italic;font-size:72px;color:#EDE6D6;">{line}</div>' for i, line in enumerate(q))}
    <div id="k10-at" class="t" style="left:0;right:0;top:620px;text-align:center;font-size:28px;font-weight:600;letter-spacing:.2em;color:{MUTED};">— SINNGEMÄSS NACH SIROIS &amp; PYCHYL (2013)</div>
    {lower("k10", "TIM PYCHYL", "PSYCHOLOGE · CARLETON UNIVERSITY", 130, 640)}"""),
    lower_js("k10", w("Tim", S), w("Aufschieben", S) - 0.6) + r"""
  [0, 1, 2].forEach(i => fadeIn(`#k10-q${i}`, T.auf + i * 0.9, 0.8, { from: { filter: "blur(6px)" }, to: { filter: "blur(0px)" } }));
  fadeIn("#k10-at", T.gef - 0.6, 0.8);
""", {"auf": w("Aufschieben", S), "gef": w("Gefühlsregulation.", S)})

# ------------------------------------------------------------ 11 Gefühls-Wolke
S = "s11_wolke"
put(S, "k11", html_cam("k11", f"""
    {light("k11-l", 520, 520, 520, "rgba(255,226,180,.18)")}
    {svg_actor("k11-lap", 260, 560, 520, 300, art.laptop(0, 0, 1.2, ""), "-40 -20 520 300")}
    {svg_actor("k11-cloud", 230, 170, 580, 420, art.cloud(0, 0, 1.0, "#555C66"), "-290 -190 580 420")}
    <div id="k11-w0" class="t" style="left:330px;top:250px;font-size:40px;font-weight:800;">Langeweile</div>
    <div id="k11-w1" class="t" style="left:420px;top:310px;font-size:40px;font-weight:800;">Überforderung</div>
    <div id="k11-w2" class="t" style="left:300px;top:370px;font-size:40px;font-weight:800;">Angst, Fehler zu machen</div>
    {otto_block("k11", 1150, ("tired", "shock"))}"""),
    r"""
  fadeIn("#k11-lap", 0.2, 0.6);
  tl.fromTo("#k11-cloud", { opacity: 0, scale: 0.3, transformOrigin: "40% 100%" }, { opacity: 1, scale: 1, duration: 1.0, ease: "power3.out" }, T.gef - 0.2);
  face("k11o", "tired", "shock", T.gef);
  fadeIn("#k11-w0", T.lang, 0.5); fadeIn("#k11-w1", T.ueber, 0.5); fadeIn("#k11-w2", T.angst, 0.5);
""", {"gef": w("Gefühl,", S), "lang": w("Langeweile.", S), "ueber": w("Überforderung.", S), "angst": w("Angst,", S)})

# ------------------------------------------------------------ 12 Flucht vor dem Gefühl
S = "s12_flucht"
sp12 = "".join(svg_actor(f"k12-sp{i}", x, y, 120, 120, sparkle(0, 0, s, "#E8D9A8"), "-60 -60 120 120")
               for i, (x, y, s) in enumerate([(820, 260, 1.0), (900, 470, 0.7), (760, 560, 0.8)]))
put(S, "k12", html_cam("k12", f"""
    {otto_block("k12", 340, ("happy", "excuse"), pose="raised", held=spray(150, -110))}
    {sp12}
    <div id="k12-r1" class="t" style="left:1040px;top:330px;font-size:32px;font-weight:700;letter-spacing:.2em;color:{AMBER};">✓ SOFORT EIN ERGEBNIS</div>
    <div id="k12-r2" class="t cond" style="left:1040px;top:420px;font-size:74px;color:#6E717A;">NICHT VOR DER ARBEIT</div>
    <div id="k12-r3" class="t cond" style="left:1040px;top:520px;font-size:86px;">SONDERN VOR<br>EINEM GEFÜHL.</div>"""),
    r"""
  [0, 1, 2].forEach(i => fadeIn(`#k12-sp${i}`, 0.4 + i * 0.3, 0.5, { from: { scale: 0.5 }, to: { scale: 1 } }));
  fadeIn("#k12-r1", T.erg, 0.6); fadeIn("#k12-r2", T.arb, 0.6);
  face("k12o", "happy", "excuse", T.gef - 0.4);
  fadeIn("#k12-r3", T.gef - 1.0, 0.8, { from: { scale: 1.05, transformOrigin: "0% 50%" }, to: { scale: 1 } });
""", {"erg": w("Ergebnis.", S), "arb": w("Arbeit.", S), "gef": w("Gefühl.", S, after="schlechten")})

# ------------------------------------------------------------ 13 Kapitel 2
HOSTS.append(chapter("k13", "s13_kap2", 2, "DER KAMPF IM KOPF"))


# ------------------------------------------------------------ Gehirn-Bausteine
def brain_html(cid, alarm_scale=1.1):
    return (light(f"{cid}-bl", 960, 470, 640, "rgba(255,210,220,.14)")
            + svg_actor(f"{cid}-brain", 540, 140, 840, 680, art.brain(0, 0, 1.9, "#9C6F80"), "-420 -360 840 680")
            + svg_actor(f"{cid}-al", 610, 300, 220, 300, art.alarm_guy(0, 0, alarm_scale), "-110 -180 220 300")
            + svg_actor(f"{cid}-pl", 1060, 360, 220, 180, art.planner_guy(0, 0, 1.1), "-80 -80 220 180"))


def brain_label(id_, x, title, sub):
    return (f'<div id="{id_}" class="t" style="left:{x}px;top:630px;padding:10px 18px;background:rgba(0,0,0,.6);">'
            f'<div style="font-size:30px;font-weight:800;letter-spacing:.12em;">{title}</div>'
            f'<div style="font-size:28px;color:{MUTED};font-weight:600;">{sub}</div></div>')


# ------------------------------------------------------------ 14 Gehirn
S = "s14_gehirn"
put(S, "k14", html_cam("k14", f"""
    {brain_html("k14")}
    {light("k14-glow", 720, 420, 220, "rgba(255,60,60,.6)", 0)}
    {brain_label("k14-la", 560, "AMYGDALA", "die Alarmanlage")}
    {brain_label("k14-lp", 1000, "PRÄFRONTALER KORTEX", "der Planer")}
    {svg_actor("k14-cal", 1300, 250, 200, 200, art.calendar(0, 0, "FREITAG", 0.9), "-100 -100 200 200")}"""),
    r"""
  fadeIn("#k14-brain", 0.1, 0.9);
  fadeIn("#k14-al", T.amy - 0.3, 0.6, { from: { scale: 0.85 }, to: { scale: 1 } }); fadeIn("#k14-la", T.amy + 0.3, 0.6);
  tl.fromTo("#k14-glow", { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.12 }, { opacity: 0.2, duration: 0.12 }, { opacity: 1, duration: 0.12 }, { opacity: 0, duration: 0.4 }], immediateRender: false }, T.blitz);
  fadeIn("#k14-pl", T.kor - 0.3, 0.6, { from: { scale: 0.85 }, to: { scale: 1 } }); fadeIn("#k14-lp", T.kor + 0.3, 0.6);
  fadeIn("#k14-cal", T.frei - 0.1, 0.5, { from: { y: 20 }, to: { y: 0 } });
""", {"amy": w("Amygdala,", S), "blitz": w("blitzschnell", S), "kor": w("Kortex,", S), "frei": w("Freitag", S)})

# ------------------------------------------------------------ 15 Bochum
S = "s15_bochum"
st15, n15 = typed("k15-st", "RUHR-UNIVERSITÄT BOCHUM · 2018", style="left:130px;top:178px;")
put(S, "k15", html_cam("k15", f"""
    {brain_html("k15")}
    <svg id="k15-cable" class="actor" style="left:0;top:0;opacity:0" width="1920" height="1080" viewBox="0 0 1920 1080"><path d="M790,470 q50,-30 100,0 t100,0 t100,0" fill="none" stroke="#EDE6D6" stroke-width="5" stroke-dasharray="14 10"/></svg>
    {foot("k15", "SCHLÜTER ET AL. (2018), PSYCHOLOGICAL SCIENCE")}""",
    f'{st15}<div id="k15-red" class="lay" style="background:rgba(170,0,0,.35);opacity:0"></div>'),
    f'type("#k15-st", {n15}, 0.2, 0.03);' + r"""
  fadeIn("#k15-ft", 0.6, 0.6); fadeOut("#k15-st", T.end - 0.6, 0.4);
  tl.fromTo("#k15-al", { scale: 1 }, { scale: 1.45, duration: 0.9, ease: "power2.inOut", transformOrigin: "50% 80%" }, T.gr - 0.2);
  fadeIn("#k15-cable", T.ver - 0.2, 0.5);
  tl.to("#k15-cable", { opacity: 0.18, duration: 0.8, ease: "power2.inOut" }, T.schw - 0.2);
  tl.fromTo("#k15-al", { x: 0 }, { keyframes: [{ x: -12, duration: 0.05 }, { x: 12, duration: 0.05 }, { x: -8, duration: 0.05 }, { x: 8, duration: 0.05 }, { x: 0, duration: 0.06 }], immediateRender: false }, T.gef);
  tl.fromTo("#k15-red", { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.1 }, { opacity: 0, duration: 0.6 }], immediateRender: false }, T.gef);
  tl.to("#k15-pl", { scale: 0.8, opacity: 0.6, duration: 0.8, ease: "power2.inOut", transformOrigin: "50% 80%" }, T.klemm - 0.2);
""", {"gr": w("größer.", S), "ver": w("Verbindung", S), "schw": w("schwächer.", S), "gef": w("Gefahr", S), "klemm": w("Klemmbrett", S)})

# ------------------------------------------------------------ 16 Knopf
S = "s16_knopf"
put(S, "k16", html_cam("k16", f"""
    {light("k16-l", 480, 500, 480, "rgba(255,120,120,.16)")}
    {svg_actor("k16-al", 340, 210, 300, 360, art.alarm_guy(0, 0, 1.4), "-150 -220 300 360")}
    {svg_actor("k16-btn", 300, 580, 380, 240, art.big_button(0, 0, "HANDY", 1.2), "-190 -80 380 240")}
    {otto_block("k16", 1150, ("tired", "happy"), pose="bent", item="phone")}
    {light("k16-glow", 1450, 330, 260, "rgba(140,190,255,.4)", 0)}
    <div id="k16-txt" class="t cond" style="left:700px;top:190px;font-size:80px;color:{AMBER};">BELOHNUNG: JETZT</div>
    <div id="k16-sek" class="t" style="left:704px;top:290px;font-size:30px;font-weight:700;letter-spacing:.3em;">IN EINER SEKUNDE</div>"""),
    r"""
  fadeIn("#k16-al", 0.2, 0.6); fadeIn("#k16-btn", 0.4, 0.6);
  tl.fromTo("#k16-btn", { scaleY: 1 }, { keyframes: [{ scaleY: 0.85, duration: 0.12 }, { scaleY: 1, duration: 0.3 }], transformOrigin: "50% 100%", immediateRender: false }, T.bel);
  fadeIn("#k16-txt", T.jetzt, 0.6);
  tl.to("#k16-glow", { opacity: 1, duration: 0.5 }, T.handy); face("k16o", "tired", "happy", T.handy + 0.1);
  fadeIn("#k16-sek", T.handy + 0.4, 0.5);
""", {"bel": w("Belohnungen,", S), "jetzt": w("jetzt.", S), "handy": w("Handy", S), "sek": w("Sekunde.", S)})

# ------------------------------------------------------------ 17 Waage
S = "s17_waage"
beam = f'''<g stroke="#1A1A1A" stroke-width="5" stroke-linejoin="round">
  <path d="M-70,330 L70,330 L24,280 L-24,280 Z" fill="#8A8F98"/><rect x="-10" y="40" width="20" height="242" fill="#B5BAC2"/>
  <g id="k17-beam">
    <rect x="-330" y="26" width="660" height="22" rx="10" fill="#B5BAC2"/>
    <g id="k17-panL"><path d="M-300,40 L-360,170 M-300,40 L-240,170" stroke-width="4"/><path d="M-390,170 Q-300,230 -210,170 Z" fill="#CFC9BC"/>
      <g transform="translate(-300,170)">{art.phone(-28, -110, 1.0)}{art.heart(0, -150, 0.8)}</g></g>
    <g id="k17-panR"><path d="M300,40 L240,170 M300,40 L360,170" stroke-width="4"/><path d="M210,170 Q300,230 390,170 Z" fill="#CFC9BC"/>
      <g transform="translate(300,170)"><g transform="translate(0,-60) scale(0.6)"><rect x="-110" y="-70" width="220" height="140" rx="8" fill="#E6E2DA"/><path d="M-110,-70 L0,10 L110,-70" fill="none"/></g></g></g>
  </g><circle cx="0" cy="40" r="16" fill="{ORANGE}"/></g>'''
put(S, "k17", html_cam("k17", f"""
    {light("k17-l", 960, 520, 640, "rgba(255,226,180,.20)")}
    {svg_actor("k17-bal", 560, 220, 800, 620, beam, "-400 -100 800 620")}
    <div id="k17-a" class="t" style="left:380px;top:250px;font-size:30px;font-weight:700;letter-spacing:.24em;color:{AMBER};">1 SEKUNDE</div>
    <div id="k17-b" class="t" style="left:1260px;top:250px;font-size:30px;font-weight:700;letter-spacing:.24em;color:{MUTED};">STEUERBESCHEID · JULI</div>"""),
    r"""
  fadeIn("#k17-bal", 0.1, 0.8); fadeIn("#k17-a", 0.5, 0.6); fadeIn("#k17-b", T.juli, 0.6);
  tl.fromTo("#k17-beam", { rotation: 0, svgOrigin: "0 40" }, { rotation: -16, duration: 0.9, ease: "power3.out" }, T.gew - 0.1);
  tl.fromTo("#k17-panL", { rotation: 0, svgOrigin: "-300 40" }, { rotation: 16, duration: 0.9, ease: "power3.out" }, T.gew - 0.1);
  tl.fromTo("#k17-panR", { rotation: 0, svgOrigin: "300 40" }, { rotation: 16, duration: 0.9, ease: "power3.out" }, T.gew - 0.1);
""", {"juli": w("Juli,", S), "gew": w("gewinnt.", S)})

# ------------------------------------------------------------ 18 Kapitel 3
HOSTS.append(chapter("k18", "s18_kap3", 3, "DER FREMDE"))

# ------------------------------------------------------------ 19 Morgen-Otto
S = "s19_morgenotto"
put(S, "k19", html_cam("k19", f"""
    {otto_block("k19", 340, ("tired", "shock"))}
    {light("k19-l2", 1450, 470, 520, "rgba(200,190,255,.20)")}
    {actor("k19-mo", 1150, OTTO_TOP, 600, 760, otto_svg("k19m", ("smirk",), pose="bent", item="x", held=art.calendar(70, 230, "MORGEN", 0.7), bags="dark"))}
    {lower("k19", "MORGEN-OTTO", "OTTOS ZUKÜNFTIGES ICH", 790, 170)}"""),
    lower_js("k19", w("Morgen-Otto.", S), dur(S) - 0.5) + r"""
  fadeIn("#k19-mo", T.vor - 0.3, 0.8, { from: { x: 80 }, to: { x: 0 } });
  face("k19o", "tired", "shock", T.vor + 0.4);
""", {"vor": w("vorstellen:", S)})

# ------------------------------------------------------------ 20 Hirnscans
S = "s20_scans"


def scan_svg(cid, i, spots):
    sp = "".join(f'<circle cx="{a}" cy="{b}" r="{r}" fill="#FFB300" opacity=".85"/>' for a, b, r in spots)
    return (f'<ellipse cx="0" cy="0" rx="190" ry="160" fill="#22262E" stroke="#5A606B" stroke-width="5"/>'
            f'<path d="M0,-150 Q-20,-40 0,0 Q20,60 0,150" fill="none" stroke="#3A404B" stroke-width="5"/><g id="{cid}-sp{i}" opacity="0">{sp}</g>')


scans = [((-60, -40, 40), (40, -70, 34), (0, 40, 46)), ((80, 10, 34), (-90, 60, 28)), ((70, 20, 34), (-80, 50, 30))]
labs = ["ICH SELBST", "ICH IN 10 JAHREN", "EIN FREMDER"]
put(S, "k20", html_cam("k20", f"""
    {light("k20-l", 960, 470, 760, "rgba(255,226,180,.14)")}
    {"".join(svg_actor(f"k20-s{i}", 290 + i * 480, 300, 400, 340, scan_svg("k20", i, scans[i]), "-200 -170 400 340") + f'<div id="k20-t{i}" class="t" style="left:{290 + i * 480}px;width:400px;top:670px;text-align:center;font-size:30px;font-weight:700;letter-spacing:.2em;">{labs[i]}</div>' for i in range(3))}
    <div id="k20-eq" class="t cond" style="left:1210px;top:380px;font-size:140px;color:{AMBER};">≈</div>
    {foot("k20", "HERSHFIELD ET AL. (2009), SOCIAL COGNITIVE AND AFFECTIVE NEUROSCIENCE")}"""),
    r"""
  [0, 1, 2].forEach(i => { fadeIn(`#k20-s${i}`, 0.3 + i * 0.25, 0.6); fadeIn(`#k20-t${i}`, 0.5 + i * 0.25, 0.6); });
  fadeIn("#k20-ft", T.her, 0.6);
  fadeIn("#k20-sp0", T.selbst, 0.6); fadeIn("#k20-sp1", T.zehn, 0.6); fadeIn("#k20-sp2", T.fremde, 0.6);
  fadeIn("#k20-eq", T.fremden, 0.7, { from: { scale: 1.3 }, to: { scale: 1 } });
""", {"her": w("Hershfield", S), "selbst": w("selbst", S), "zehn": w("zehn", S), "fremde": w("fremde", S), "fremden": w("Fremden", S)})

# ------------------------------------------------------------ 21 Übergabe
S = "s21_uebergabe"
put(S, "k21", html_cam("k21", f"""
    {otto_block("k21", 340, ("smirk",), pose="give")}
    {light("k21-l2", 1450, 470, 520, "rgba(200,190,255,.18)")}
    {actor("k21-mo", 1150, OTTO_TOP, 600, 760, otto_svg("k21m", ("tired", "shock"), bags="dark"))}
    {svg_actor("k21-stack", 752, 420, 200, 220, art.stack(0, 0, 4, "Steuer-\nerklärung", 0.8), "-100 -170 200 220")}
    <div id="k21-q1" class="t" style="left:0;right:0;top:175px;text-align:center;font-family:EB Garamond;font-style:italic;font-size:54px;color:#CFC9BC;">„Ich mache das morgen.“</div>
    <div id="k21-x" class="actor" style="left:700px;top:212px;width:520px;height:5px;background:{RED};"></div>
    <div id="k21-q2" class="t" style="left:0;right:0;top:255px;text-align:center;font-family:EB Garamond;font-style:italic;font-size:62px;color:#FFF;">„Der da macht das morgen.“</div>"""),
    r"""
  fadeIn("#k21-stack", 0.2, 0.5); fadeIn("#k21-mo", 0.3, 0.6);
  fadeIn("#k21-q1", T.nicht, 0.6);
  tl.fromTo("#k21-x", { scaleX: 0, transformOrigin: "0% 50%" }, { scaleX: 1, duration: 0.5, ease: "power2.inOut" }, T.derda - 0.5);
  fadeIn("#k21-q2", T.derda, 0.7);
  tl.to("#k21-stack", { x: 470, duration: 1.0, ease: "power2.inOut" }, T.derda + 0.2);
  face("k21m", "tired", "shock", T.derda + 1.0);
""", {"nicht": w("nicht:", S), "derda": w("Der", S, after="merken:")})

# ------------------------------------------------------------ 22 Kette
S = "s22_kette"
ch22 = ""
for i in range(4):
    inner = otto_svg(f"k22o{i}", ("tired" if i < 3 else "shock",), pose="give" if i < 3 else "down", bags="dark" if i else "normal")
    stk = svgbox(art.stack(0, 0, 3 + i * 2, "Steuer-\nerklärung", 0.8), "-100 -260 200 320", 200, 320) if i < 3 else ""
    ch22 += (f'<div id="k22-o{i}" class="actor" style="left:{70 + i * 450}px;top:300px;width:372px;height:471px;">'
             f'<div style="position:absolute;left:0;top:0;width:600px;height:760px;transform:scale(.62);transform-origin:0 0">{inner}'
             + (f'<div style="position:absolute;left:412px;top:180px;">{stk}</div>' if stk else "") + '</div></div>'
             f'<div id="k22-t{i}" class="t" style="left:{70 + i * 450}px;width:372px;top:250px;text-align:center;font-size:28px;font-weight:700;letter-spacing:.3em;color:{MUTED};">{["HEUTE", "MORGEN", "ÜBERMORGEN", "FREITAG"][i]}</div>')
put(S, "k22", html_cam("k22", f"""
    {light("k22-l", 960, 520, 900, "rgba(255,226,180,.14)")}
    {ch22}
    <div id="k22-clock" class="actor" style="left:1560px;top:170px;width:260px;height:110px;background:#111;border:3px solid #333;border-radius:18px;
         color:#7CFF8A;font-family:Space Mono;font-weight:700;font-size:54px;display:flex;align-items:center;justify-content:center;">23:58</div>"""),
    r"""
  [0, 1, 2, 3].forEach(i => { const t = [0.2, 0.9, T.ueber - 0.4, T.ueber + 0.6][i]; fadeIn(`#k22-o${i}`, t, 0.6); fadeIn(`#k22-t${i}`, t + 0.1, 0.5); });
  fadeIn("#k22-clock", T.ueber + 0.9, 0.5);
""", {"ueber": w("Übermorgen-Otto.", S)})

# ------------------------------------------------------------ 23 Kapitel 4
HOSTS.append(chapter("k23", "s23_kap4", 4, "DER TEUFELSKREIS"))

# ------------------------------------------------------------ 24 Kreis
S = "s24_kreis"
nodes = [("AUFGABE FÜHLT", "SICH MIES AN", 960, 255, "sad"), ("AUFSCHIEBEN", "", 1330, 520, "smirk"),
         ("KURZE", "ERLEICHTERUNG", 960, 785, "happy"), ("SCHULD-", "GEFÜHL", 590, 520, "sad")]
nh = "".join(f'<div id="k24-n{i}" class="actor" style="left:{x - 190}px;top:{y - 62}px;width:380px;height:124px;background:#16181C;border:2px solid #CFC9BC;">'
             f'{svgbox(_head_base() + _face(f), "-150 -180 300 300", 110, 110)}'
             f'<div class="t" style="left:120px;top:{30 if b else 44}px;font-size:28px;font-weight:800;letter-spacing:.12em;line-height:1.3;">{a}{"<br>" + b if b else ""}</div></div>'
             for i, (a, b, x, y, f) in enumerate(nodes))
put(S, "k24", html_cam("k24", f"""
    {light("k24-l", 960, 520, 700, "rgba(255,226,180,.14)")}
    <svg class="actor" style="left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
      <circle cx="960" cy="520" r="268" fill="none" stroke="#2A2D33" stroke-width="10"/>
      <circle id="k24-ring" cx="960" cy="520" r="268" fill="none" stroke="{ORANGE}" stroke-width="10" stroke-dasharray="1684" stroke-dashoffset="1684" transform="rotate(-90 960 520)"/></svg>
    {nh}
    <div id="k24-q" class="t" style="left:0;right:0;top:490px;text-align:center;font-family:EB Garamond;font-style:italic;font-size:48px;color:#EDE6D6;">„Warum bin ich so?“</div>"""),
    r"""
  fadeIn("#k24-n0", 0.3, 0.6);
  const seg = (t, k) => tl.to("#k24-ring", { attr: { "stroke-dashoffset": 1684 - 421 * k }, duration: 0.8, ease: "power2.inOut" }, t);
  seg(T.auf, 1); fadeIn("#k24-n1", T.auf + 0.2, 0.6);
  seg(T.erl, 2); fadeIn("#k24-n2", T.erl + 0.2, 0.6);
  seg(T.gew, 3); fadeIn("#k24-n3", T.gew + 0.2, 0.6);
  fadeIn("#k24-q", T.warum, 0.6); fadeOut("#k24-q", T.klebt - 1.0, 0.5);
  seg(T.klebt, 4);
  tl.to("#k24-n0", { borderColor: "#E2483D", duration: 0.4 }, T.klebt + 0.3);
  tl.fromTo("#k24-ring", { rotation: 0, svgOrigin: "960 520" }, { rotation: 360, duration: 1.6, ease: "power2.inOut", immediateRender: false }, T.schl);
""", {"auf": w("aufschiebt,", S), "erl": w("Erleichterung.", S), "gew": w("Gewissen.", S), "warum": w("Warum", S),
      "klebt": w("klebt.", S), "schl": w("schlimmer", S)})

# ------------------------------------------------------------ 25 Sich fertigmachen
S = "s25_fertigmachen"
chest25 = svgbox(f'''<g stroke="#1A140E" stroke-width="5" stroke-linejoin="round">
  <rect x="-200" y="-60" width="400" height="200" rx="12" fill="#7A5634"/><path d="M-200,-60 Q0,-170 200,-60 Z" fill="#8C6640"/>
  <rect x="-40" y="-40" width="80" height="90" rx="10" fill="#C9A646"/><path d="M-24,-40 v-30 a24,24 0 0 1 48,0 v30" fill="none" stroke-width="9"/></g>''',
                 "-280 -200 560 420", 560, 420)
put(S, "k25", html_cam("k25", f"""
    {otto_block("k25", 340, ("sad", "aha"), bags="dark")}
    <div id="k25-a" class="t cond" style="left:1040px;top:330px;font-size:96px;">SICH FERTIGMACHEN</div>
    <div id="k25-b" class="t cond" style="left:1040px;top:445px;font-size:96px;color:{RED};">= SCHLIMMER.</div>
    <div id="k25-c" class="actor" style="left:1100px;top:320px;width:560px;height:420px;">{chest25}</div>"""),
    r"""
  fadeIn("#k25-a", T.fert, 0.6); fadeIn("#k25-b", T.schl, 0.6);
  tl.to(["#k25-a", "#k25-b"], { opacity: 0, duration: 0.4 }, T.trick - 0.6);
  fadeIn("#k25-c", T.trick - 0.2, 0.7, { from: { y: 30 }, to: { y: 0 } });
  face("k25o", "sad", "aha", T.trick);
""", {"fert": w("fertigmachen,", S), "schl": w("schlimmer", S), "trick": w("Trick", S)})

# ------------------------------------------------------------ 26 Kapitel 5
HOSTS.append(chapter("k26", "s26_kap5", 5, "DER AUSWEG"))

# ------------------------------------------------------------ 27 Werkzeug 1
S = "s27_vergeben"
put(S, "k27", html_cam("k27", f"""
    {header("k27", "WERKZEUG 1", "VERGIB DIR SELBST")}
    {otto_block("k27", 1150, ("smirk", "happy"))}
    <div id="k27-chart" class="actor" style="left:180px;top:400px;width:700px;height:470px;">
      <div class="t" style="left:0;top:0;font-size:28px;font-weight:700;letter-spacing:.24em;color:{MUTED};">AUFSCHIEBEN</div>
      <div style="position:absolute;left:0;right:0;bottom:70px;height:3px;background:#CFC9BC;"></div>
      <div id="k27-b1" style="position:absolute;left:60px;bottom:73px;width:180px;height:300px;background:#8A8F98;transform-origin:50% 100%;"></div>
      <div id="k27-b2" style="position:absolute;left:330px;bottom:73px;width:180px;height:160px;background:{AMBER};transform-origin:50% 100%;"></div>
      <div class="t" style="left:40px;bottom:20px;font-size:28px;font-weight:700;letter-spacing:.12em;">PRÜFUNG 1</div>
      <div class="t" style="left:310px;bottom:20px;font-size:28px;font-weight:700;letter-spacing:.12em;">PRÜFUNG 2</div>
      <div class="t" style="left:540px;bottom:110px;font-size:28px;color:{MUTED};font-weight:600;">(illustrativ)</div></div>
    <div id="k27-n" class="t cond" style="left:180px;top:520px;font-size:110px;">NACHSICHT <span style="color:{AMBER}">&gt;</span> DRUCK</div>
    {lower("k27", "WOHL, PYCHYL &amp; BENNETT", "STUDIE · 2010", 180, 700)}"""),
    lower_js("k27", w("Studie", S), w("Diejenigen", S) - 0.5) + r"""
  fadeIn("#k27-hk", 0.2, 0.6); fadeIn("#k27-ht", 0.4, 0.8);
  fadeIn("#k27-chart", T.die, 0.5);
  tl.fromTo("#k27-b1", { scaleY: 0 }, { scaleY: 1, duration: 0.8, ease: "power2.out" }, T.die + 0.2);
  tl.fromTo("#k27-b2", { scaleY: 0 }, { scaleY: 1, duration: 0.8, ease: "power2.out" }, T.wen);
  face("k27o", "smirk", "happy", T.wen);
  fadeOut("#k27-chart", T.nach - 0.6, 0.4);
  fadeIn("#k27-n", T.nach, 0.7, { from: { scale: 1.05, transformOrigin: "0% 50%" }, to: { scale: 1 } });
""", {"die": w("Diejenigen", S), "wen": w("weniger", S), "nach": w("Nachsicht.", S)})

# ------------------------------------------------------------ 28 Werkzeug 2
S = "s28_benennen"
put(S, "k28", html_cam("k28", f"""
    {header("k28", "WERKZEUG 2", "BENENNE DAS GEFÜHL", 1000)}
    {otto_block("k28", 340, ("tired", "aha"))}
    {svg_actor("k28-cloud", 1080, 420, 580, 420, art.cloud(0, 0, 1.0, "#555C66"), "-290 -190 580 420")}
    <div id="k28-w0" class="t" style="left:1000px;top:400px;font-family:EB Garamond;font-style:italic;font-size:50px;">Langeweile?</div>
    <div id="k28-w1" class="t" style="left:1500px;top:460px;font-family:EB Garamond;font-style:italic;font-size:50px;">Angst?</div>
    <div id="k28-w2" class="t" style="left:1180px;top:820px;font-family:EB Garamond;font-style:italic;font-size:50px;">Überforderung?</div>
    <div id="k28-tag" class="actor" style="left:1130px;top:560px;width:480px;height:110px;background:#EDE6D6;color:#1A1A1A;border-radius:14px;
         font-size:52px;font-weight:800;display:flex;align-items:center;justify-content:center;rotate:-5deg;">Überforderung</div>"""),
    r"""
  fadeIn("#k28-hk", 0.2, 0.6); fadeIn("#k28-ht", 0.4, 0.8); fadeIn("#k28-cloud", 0.8, 0.8);
  fadeIn("#k28-w0", T.lang, 0.5); fadeIn("#k28-w1", T.angst, 0.5); fadeIn("#k28-w2", T.ueb, 0.5);
  face("k28o", "tired", "aha", T.namen);
  fadeIn("#k28-tag", T.namen, 0.5, { from: { scale: 1.3 }, to: { scale: 1 } });
  tl.to("#k28-cloud", { scale: 0.45, opacity: 0.4, duration: 1.0, ease: "power2.inOut", transformOrigin: "50% 50%" }, T.macht - 0.4);
  tl.to(["#k28-w0", "#k28-w1", "#k28-w2"], { opacity: 0.25, duration: 0.6 }, T.macht - 0.4);
""", {"lang": w("Langeweile?", S), "angst": w("Angst?", S), "ueb": w("Überforderung?", S), "namen": w("Namen", S), "macht": w("Macht.", S)})

# ------------------------------------------------------------ 29 Werkzeug 3
S = "s29_schritt"
mount = f'''<g stroke="#1A1A1A" stroke-width="5" stroke-linejoin="round"><path d="M0,520 L230,40 L330,170 L410,90 L600,520 Z" fill="#5F646D"/>
  <path d="M230,40 L196,110 L240,96 L270,112 Z" fill="#EDE6D6"/></g>'''
put(S, "k29", html_cam("k29", f"""
    {header("k29", "WERKZEUG 3", "DER WINZIGE<br>ERSTE SCHRITT", 1000)}
    {otto_block("k29", 340, ("excuse", "smirk"))}
    {svg_actor("k29-m", 980, 400, 600, 520, mount, "0 0 600 520")}
    <div id="k29-ml" class="t cond" style="left:1080px;top:760px;font-size:54px;letter-spacing:.06em;">STEUERERKLÄRUNG</div>
    {light("k29-red", 1220, 470, 300, "rgba(255,60,60,.45)", 0)}
    <div id="k29-step" class="actor" style="left:1600px;top:790px;width:220px;height:70px;background:{AMBER};"></div>
    <div id="k29-sl" class="t" style="left:1590px;top:735px;font-size:30px;font-weight:800;letter-spacing:.1em;">DATEI ÖFFNEN</div>"""),
    r"""
  fadeIn("#k29-hk", 0.2, 0.6); fadeIn("#k29-ht", 0.4, 0.8);
  fadeIn("#k29-m", T.steu - 0.3, 0.7); fadeIn("#k29-ml", T.steu, 0.6);
  tl.fromTo("#k29-red", { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.15 }, { opacity: 0.3, duration: 0.15 }, { opacity: 1, duration: 0.15 }, { opacity: 0, duration: 0.5 }], immediateRender: false }, T.alarm);
  fadeIn("#k29-step", T.datei, 0.5, { from: { y: 30 }, to: { y: 0 } }); fadeIn("#k29-sl", T.datei + 0.2, 0.5);
  tl.to(["#k29-m", "#k29-ml"], { opacity: 0.25, duration: 0.8 }, T.nichts);
  face("k29o", "excuse", "smirk", T.nichts);
""", {"steu": w("Steuererklärung", S), "alarm": w("Alarm.", S), "datei": w("Datei", S), "nichts": w("nichts.", S)})

# ------------------------------------------------------------ 30 Werkzeug 4
S = "s30_timer"
timer = f'''<circle cx="0" cy="0" r="170" fill="#EDE6D6" stroke="#1A1A1A" stroke-width="6"/>
  <circle cx="0" cy="0" r="120" fill="none" stroke="#D9D3C5" stroke-width="40"/>
  <circle id="k30-arc" cx="0" cy="0" r="120" fill="none" stroke="{ORANGE}" stroke-width="40" stroke-dasharray="754" stroke-dashoffset="0" transform="rotate(-90)"/>
  <rect x="-24" y="-206" width="48" height="34" rx="6" fill="#8A8F98" stroke="#1A1A1A" stroke-width="5"/>'''
put(S, "k30", html_cam("k30", f"""
    {header("k30", "WERKZEUG 4", "DER 10-MINUTEN-DEAL")}
    {otto_block("k30", 1150, ("smirk", "aha"))}
    {svg_actor("k30-t", 330, 380, 400, 420, timer, "-200 -220 400 420")}
    <div id="k30-time" class="t" style="left:330px;width:400px;top:555px;text-align:center;font-family:Space Mono;font-weight:700;font-size:64px;color:#1A1A1A;">10:00</div>
    <div id="k30-w" class="t cond" style="left:780px;top:520px;font-size:70px;color:{AMBER};">…UND MACHT<br>EINFACH WEITER.</div>"""),
    r"""
  fadeIn("#k30-hk", 0.2, 0.6); fadeIn("#k30-ht", 0.4, 0.8); fadeIn("#k30-t", T.min - 0.3, 0.6); fadeIn("#k30-time", T.min - 0.3, 0.6);
  for (let i = 1; i <= 10; i++) tl.set("#k30-time", { textContent: `${10 - i}:00`.padStart(5, "0") }, T.min + 0.6 + i * 0.3);
  tl.fromTo("#k30-arc", { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": 754 }, duration: 3.0, ease: "none" }, T.min + 0.6);
  face("k30o", "smirk", "aha", T.witz);
  fadeIn("#k30-w", T.weiter, 0.7);
""", {"min": w("zehn", S, after="Deal:"), "witz": w("Witz:", S), "weiter": w("weiter.", S)})

# ------------------------------------------------------------ 31 JETZT
MX, MY = 340 + 300 + 83, OTTO_TOP + 200 + 229
S = "s31_jetzt"
put(S, "k31", html_cam("k31", f"""
    {otto_block("k31", 340, ("happy",), pose="bent", item="mug", label="JETZT")}
    {light("k31-lg", 1300, 600, 360, "rgba(255,240,200,.25)")}
    {svg_actor("k31-lap", 1060, 560, 520, 300, art.laptop(0, 0, 1.2, ""), "-40 -20 520 300")}
    <div id="k31-a" class="t cond" style="left:1000px;top:230px;font-size:96px;">OTTO IST NICHT FAUL.</div>
    <div id="k31-b" class="t cond" style="left:1000px;top:345px;font-size:96px;color:{AMBER};">DU AUCH NICHT.</div>"""),
    r"""
  tl.fromTo("#k31-cam", { scale: 2.4, x: %d, y: %d, transformOrigin: "%dpx %dpx" }, { scale: 1, x: 0, y: 0, duration: 1.4, ease: "power2.inOut" }, 1.0);
  fadeIn("#k31-lap", 1.4, 0.6);
  fadeIn("#k31-a", T.faul - 0.3, 0.7); fadeIn("#k31-b", T.du, 0.7);
  tl.to(["#k31-a", "#k31-b"], { opacity: 0, duration: 0.5 }, T.gehirn - 0.3);
""" % (960 - MX, 520 - MY, MX, MY), {"faul": w("faul.", S), "du": w("Du", S), "gehirn": w("Gehirn,", S)}, push=False)

# ------------------------------------------------------------ 32 Tasse wieder SPÄTER (Gag)
S = "s32_spaeter"
mx, my = 340 + 300 + 83, OTTO_TOP + 200 + 229
put(S, "k32", html_cam("k32", f"""{otto_block("k32", 340, ("happy", "smirk"), pose="bent", item="mug", label="SPÄTER")}"""),
    f"""
  face("k32o", "happy", "smirk", 0.3);
  tl.fromTo("#k32-cam", {{ scale: 1, x: 0, y: 0 }}, {{ scale: 2.4, x: {960 - mx}, y: {520 - my}, transformOrigin: "{mx}px {my}px", duration: 1.6, ease: "power2.inOut" }}, 0.5);
""", {}, push=False)

# ------------------------------------------------------------ 33 Deadline-Genie
S = "s33_deadline"
put(S, "k33", html_cam("k33", f"""
    {otto_block("k33", 340, ("tired", "shock"))}
    {light("k33-lg", 1300, 560, 420, "rgba(255,240,200,.35)")}
    {svg_actor("k33-lap", 1060, 560, 520, 300, art.laptop(0, 0, 1.2, "", glow=True), "-40 -20 520 300")}
    {svg_actor("k33-sp", 1150, 380, 300, 260, art.sparks(0, 0, 1.4), "-150 -170 300 260")}
    <div id="k33-clock" class="actor" style="left:1560px;top:170px;width:260px;height:110px;background:#111;border:3px solid #333;border-radius:18px;
         color:#7CFF8A;font-family:Space Mono;font-weight:700;font-size:54px;display:flex;align-items:center;justify-content:center;">23:58</div>"""),
    r"""
  fadeIn("#k33-clock", 0.2, 0.5); fadeIn("#k33-lap", 0.2, 0.5);
  face("k33o", "tired", "shock", T.dead);
  tl.fromTo("#k33-sp", { opacity: 0 }, { keyframes: [{ opacity: 1, duration: 0.1 }, { opacity: 0.3, duration: 0.1 }, { opacity: 1, duration: 0.1 }, { opacity: 0.6, duration: 0.1 }, { opacity: 1, duration: 0.1 }], immediateRender: false }, T.genie);
""", {"dead": w("Deadline", S), "genie": w("Genie", S)})

# ------------------------------------------------------------ 34 Abspann
S = "s34_endcard"
put(S, "k34", html_cam("k34", f"""
    <div id="k34-ch" class="t cond" style="left:0;right:0;top:190px;text-align:center;font-size:70px;letter-spacing:.3em;">OTTO NORMALPSYCHE</div>
    <div id="k34-sub" class="t" style="left:0;right:0;top:285px;text-align:center;font-size:28px;font-weight:600;letter-spacing:.4em;color:{MUTED};">WARUM WIR TUN, WAS WIR TUN</div>
    <div id="k34-sb" class="actor" style="left:300px;top:420px;width:300px;height:300px;border-radius:50%;border:2px dashed #555;"></div>
    <div id="k34-sbt" class="t" style="left:300px;width:300px;top:740px;text-align:center;font-size:28px;font-weight:700;letter-spacing:.3em;">ABONNIEREN</div>
    <div id="k34-nv" class="actor" style="left:900px;top:400px;width:720px;height:405px;border:2px dashed #555;"></div>
    <div id="k34-nt" class="t" style="left:900px;top:350px;font-size:28px;font-weight:700;letter-spacing:.4em;color:{AMBER};">NÄCHSTE FOLGE</div>
    <div id="k34-nn" class="t cond" style="left:940px;top:520px;font-size:54px;line-height:1.15;white-space:normal;width:640px;">WARUM DU KURZ VOR DER DEADLINE PLÖTZLICH EIN GENIE BIST</div>"""),
    r"""
  fadeIn("#k34-ch", 0.3, 1.0); fadeIn("#k34-sub", 0.9, 0.8);
  ["#k34-sb", "#k34-sbt", "#k34-nv", "#k34-nt", "#k34-nn"].forEach((s, i) => fadeIn(s, 1.4 + i * 0.15, 0.7));
""", {})
