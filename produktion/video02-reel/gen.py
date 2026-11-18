"""Video 02 als Reel/Short (1080x1920): Hook → „in einer Minute erklärt“ → 60-Sekunden-Timer → „Zeit um!“ → YouTube-Verweis.

Liest assets/words.json + assets/segments.json (aus voice.py). Schreibt index.html, compositions/*.html, assets/sfx.json.
Sichere Zone (Shorts/Reels): Grafik y 430–1030, Untertitel y 1070–1240, wichtiges zwischen x 150 und 930.
"""
import json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")  # produktion/
sys.path.insert(0, os.path.join(ROOT, "video01"))
sys.path.insert(0, os.path.join(ROOT, "video01-hf"))
from rig import otto_svg  # noqa: E402

WORDS = json.load(open(f"{HERE}/assets/words.json"))
SEG = {s["id"]: (s["start"], s["end"]) for s in json.load(open(f"{HERE}/assets/segments.json"))}
END = round(max(e for _, e in SEG.values()), 3)
T0, T1 = SEG["timer"]  # Timer 60 → 0
MUTED, AMBER, RED, GREEN, ORANGE, BLUE = "#8C8F96", "#E8C27A", "#FF4B3E", "#5BE37D", "#FF7A1A", "#4FA3FF"
os.makedirs(f"{HERE}/compositions", exist_ok=True)
SFX = []


def norm(w):
    return re.sub(r"[^\wäöüß]", "", w.lower())


def W(word, after=0.0):
    for w in WORDS:
        if w["start"] >= after - 1e-6 and norm(w["text"]) == norm(word):
            return w["start"]
    raise KeyError(word)


def light(id_, x, y, r, col, a=1.0):
    return (f'<div id="{id_}" class="light" style="left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;opacity:{a};'
            f'background:radial-gradient(circle, {col} 0%, transparent 70%);"></div>')


def otto(cid, x, top, s, faces, **kw):
    return (f'<div id="{cid}-otto" class="actor" style="left:{x}px;top:{top}px;width:{600 * s:.0f}px;height:{760 * s:.0f}px;opacity:0">'
            f'<div style="position:absolute;left:0;top:0;width:600px;height:760px;transform:scale({s});transform-origin:0 0">{otto_svg(cid + "o", faces, **kw)}</div></div>')


def ctext(id_, top, html, size, cls="cond", color="#FFF", extra=""):
    return (f'<div id="{id_}" class="t {cls}" style="left:0;width:1080px;top:{top}px;text-align:center;font-size:{size}px;color:{color};opacity:0;{extra}">{html}</div>')


def tag(cid, num, title):
    return (f'<div id="{cid}-tag" class="t" style="left:0;width:1080px;top:442px;text-align:center;opacity:0">'
            f'<span style="display:inline-flex;align-items:center;gap:16px;padding:8px 28px 8px 10px;background:#16181D;border:2px solid #3A3F48;'
            f'border-radius:44px;font-size:30px;font-weight:800;letter-spacing:.16em;color:#EDE6D6">'
            f'<span style="width:50px;height:50px;border-radius:50%;background:{AMBER};color:#111;display:inline-flex;align-items:center;justify-content:center;'
            f'font-size:28px;letter-spacing:0">{num}</span>{title}</span></div>')


CSS = """
  #root { position:absolute; inset:0; overflow:hidden; color:#FFF; font-family:'Inter', sans-serif; }
  #root .actor, #root .light, #root .lay, #root .t { position:absolute; }
  #root .lay { inset:0; }
  #root .t { white-space:nowrap; }
  #root .cond { font-family:'Oswald', sans-serif; font-weight:700; text-transform:uppercase; line-height:1; }
  #root .mono { font-family:'Space Mono', monospace; font-weight:700; line-height:1; }
  #root .card { background:#16181D; border:2px solid #3A3F48; border-radius:26px; box-shadow:0 30px 80px rgba(0,0,0,.6); }
  #root .emo { line-height:1; }
"""
JS = r"""
  const tl = gsap.timeline({ paused: true });
  const fadeIn = (sel, t, d = 0.3) => tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: d, ease: "power2.out" }, t);
  const fadeOut = (sel, t, d = 0.22) => tl.to(sel, { opacity: 0, duration: d, ease: "power2.in" }, t);
  const popIn = (sel, t, d = 0.32, s = 0.3) => tl.fromTo(sel, { opacity: 0, scale: s }, { opacity: 1, scale: 1, duration: d, ease: "back.out(2.2)" }, t);
  const slam = (sel, t, s = 2.4) => tl.fromTo(sel, { opacity: 0, scale: s }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.in" }, t);
  const upIn = (sel, t, d = 0.3) => tl.fromTo(sel, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: d, ease: "power3.out" }, t);
  const outUp = (sel, t, d = 0.22) => tl.to(sel, { opacity: 0, y: -50, scale: 0.9, duration: d, ease: "power2.in" }, t);
  const shake = (sel, t, a = 14) => tl.fromTo(sel, { x: 0, y: 0 }, { keyframes: [...Array(8)].map((_, i) => ({ x: (i % 2 ? a : -a) * (1 - i / 8), y: (i % 3 ? -a : a) * 0.5 * (1 - i / 8), duration: 0.035 })).concat([{ x: 0, y: 0, duration: 0.04 }]), immediateRender: false }, t);
  const tagIn = (sel, t) => tl.fromTo(sel, { opacity: 0, y: -30, scale: 0.8 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(2)" }, t);
  const face = (p, from, to, t) => { tl.set(`#${p}-face-${from}`, { opacity: 0 }, t); tl.set(`#${p}-face-${to}`, { opacity: 1 }, t); };
"""
HOSTS = []


def scene(cid, a, e, html, js, T=None, track=1):
    T = {k: round(v - a, 3) for k, v in (T or {}).items()}
    T["end"] = round(e - a, 3)
    src = (f'<template>\n  <style>{CSS}</style>\n  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">\n{html}\n  </div>\n'
           f'  <script>\n  const T = {json.dumps(T)};\n{JS}\n{js}\n  window.__timelines["{cid}"] = tl;\n  </script>\n</template>\n')
    open(f"{HERE}/compositions/{cid}.html", "w", encoding="utf-8").write(src)
    HOSTS.append((cid, a, e, track))


# ================================================================ Hintergrund: warme Lichter, die langsam wandern
scene("bg", 0, END, f"""
  <div style="position:absolute;inset:0;background:#0B0C0E"></div>
  {light("bg-l1", 540, 760, 640, "rgba(255,226,180,.20)")}
  {light("bg-l2", 300, 1300, 520, "rgba(140,190,255,.07)")}
  {light("bg-l3", 820, 400, 420, "rgba(255,150,80,.08)")}""", f"""
  tl.fromTo("#bg-l1", {{ x: -60, y: 0 }}, {{ x: 60, y: 40, duration: {END}, ease: "sine.inOut" }}, 0);
  tl.fromTo("#bg-l2", {{ x: 0, y: 0 }}, {{ x: 180, y: -120, duration: {END}, ease: "sine.inOut" }}, 0);
  tl.fromTo("#bg-l3", {{ x: 0, y: 0 }}, {{ x: -200, y: 80, duration: {END}, ease: "sine.inOut" }}, 0);
""", track=0)

# ================================================================ H0 Hook: 3 Wochen Kalender → durchgestrichen → FR 23:58
a, e = 0, SEG["r_hook"][1]
cells = "".join(
    f'<div id="h0-d{i}" class="actor" style="left:{204 + (i % 7) * 98}px;top:{570 + (i // 7) * 98}px;width:84px;height:84px;border-radius:14px;'
    f'background:#22262E;border:2px solid #3A3F48;font-size:30px;font-weight:800;color:#9AA0AA;display:flex;align-items:center;justify-content:center;">{i + 1}'
    f'<div id="h0-x{i}" style="position:absolute;inset:0;opacity:0"><svg viewBox="0 0 84 84" width="84" height="84"><path d="M18,18 L66,66 M66,18 L18,66" stroke="{RED}" stroke-width="9" stroke-linecap="round"/></svg></div></div>'
    for i in range(21))
T = dict(drei=W("Drei"), trotzdem=W("trotzdem"), letzten=W("letzten"), nacht=W("Nacht?"))
scene("h0", a, e, f"""
  <div id="h0-cam" class="lay">
    <div id="h0-cal" class="lay">
      {ctext("h0-lab", 470, "3 WOCHEN ZEIT", 64, color=AMBER, extra="opacity:1")}
      {cells}
    </div>
    <div id="h0-clk" class="t mono" style="left:0;width:1080px;top:520px;text-align:center;font-size:170px;color:#FF5A4A;text-shadow:0 0 50px rgba(255,60,40,.7);opacity:0">
      <span style="font-size:70px;color:#C44;vertical-align:middle;margin-right:24px">FR</span>23:58</div>
    {otto("h0", 405, 700, 0.45, ("shock",))}
  </div>""", r"""
  tl.fromTo("#h0-cal", { scale: 1.12 }, { scale: 1, duration: 0.6, ease: "back.out(2)", immediateRender: false }, 0.05);
  for (let i = 0; i < 21; i++) tl.fromTo(`#h0-d${i}`, { y: -14 }, { y: 0, duration: 0.25, ease: "back.out(3)", immediateRender: false }, 0.1 + i * 0.025);
  for (let i = 0; i < 21; i++) tl.fromTo(`#h0-x${i}`, { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.1, ease: "power3.in" }, T.trotzdem + i * 0.07);
  tl.to("#h0-cal", { scale: 0.3, opacity: 0, duration: 0.25, ease: "power3.in" }, T.letzten - 0.05);
  slam("#h0-clk", T.letzten + 0.15, 2.8);
  shake("#h0-cam", T.letzten + 0.37, 18);
  tl.fromTo("#h0-otto", { opacity: 0, y: 160 }, { opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, T.nacht);
  tl.fromTo("#h0-clk", { textShadow: "0 0 50px rgba(255,60,40,.7)" }, { textShadow: "0 0 90px rgba(255,60,40,1)", duration: 0.3, repeat: 1, yoyo: true, immediateRender: false }, T.nacht + 0.1);
  tl.to("#h0-cam", { opacity: 0, scale: 1.08, duration: 0.2, ease: "power2.in" }, T.end - 0.2);
""", T)
SFX += [(0.15, "pop", 0.3), (T["trotzdem"], "typing", 0.4), (T["letzten"] - 0.1, "whoosh", 0.5), (T["letzten"] + 0.35, "boom", 0.85)]

# ================================================================ H1 Versprechen: kinetische Typo → 1 MINUTE → LOS!
a, e = SEG["r_promise"][0], SEG["go"][1]
T = dict(warum=W("Warum"), du=W("du", 4.5), kurz=W("kurz"), vor=W("vor"), der=W("der", 5.5), deadline=W("Deadline"), ploetzlich=W("plötzlich"),
         ein=W("ein", 6.5), genie=W("Genie"), erklaer=W("erklär"), einer=W("einer", 8), minute=W("Minute."), los=W("Los!"))
w1 = "".join(f'<span id="h1-w{i}" style="display:inline-block;opacity:0;margin:0 10px">{w}</span>' for i, w in enumerate(["WARUM", "DU", "KURZ", "VOR", "DER"]))
ring = (f'<svg viewBox="-200 -200 400 400" width="400" height="400"><circle r="170" fill="#111" stroke="#3A3F48" stroke-width="18"/>'
        f'<circle id="h1-arc" r="170" fill="none" stroke="{AMBER}" stroke-width="18" stroke-linecap="round" stroke-dasharray="1068" stroke-dashoffset="1068" transform="rotate(-90)"/>'
        f'<rect x="-26" y="-226" width="52" height="34" rx="8" fill="#3A3F48"/></svg>')
scene("h1", a, e, f"""
  <div id="h1-cam" class="lay">
    <div id="h1-txt" class="lay">
      <div class="t cond" style="left:0;width:1080px;top:470px;text-align:center;font-size:72px">{w1}</div>
      {ctext("h1-dl", 560, "DEADLINE", 190, color=RED, extra="text-shadow:0 0 40px rgba(255,60,40,.45)")}
      <div class="t cond" style="left:0;width:1080px;top:770px;text-align:center;font-size:72px"><span id="h1-p" style="display:inline-block;opacity:0">PLÖTZLICH</span>
        <span id="h1-e" style="display:inline-block;opacity:0;margin-left:16px">EIN</span></div>
      {ctext("h1-g", 850, 'GENIE <span class="emo">💡</span>', 170, color=AMBER, extra="text-shadow:0 0 50px rgba(232,194,122,.5)")}
    </div>
    {ctext("h1-k", 470, "ERKLÄRT IN", 56, color=MUTED, extra="letter-spacing:.2em")}
    <div id="h1-ring" class="actor" style="left:340px;top:540px;width:400px;height:400px;opacity:0">{ring}
      <div class="t mono" style="left:0;width:400px;top:140px;text-align:center;font-size:110px;color:#FFF">1:00</div></div>
    {ctext("h1-m", 960, "1 MINUTE", 120, color=AMBER)}
    {ctext("h1-los", 660, "LOS!", 210, color=GREEN, extra="text-shadow:0 0 60px rgba(91,227,125,.6)")}
  </div>""", r"""
  ["warum", "du", "kurz", "vor", "der"].forEach((k, i) => tl.fromTo(`#h1-w${i}`, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.18, ease: "back.out(2.5)" }, T[k]));
  slam("#h1-dl", T.deadline, 2.2);
  shake("#h1-cam", T.deadline + 0.22, 10);
  tl.fromTo("#h1-p", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.2, ease: "back.out(2.5)" }, T.ploetzlich);
  tl.fromTo("#h1-e", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.2, ease: "back.out(2.5)" }, T.ein);
  popIn("#h1-g", T.genie, 0.35, 0.4);
  outUp("#h1-txt", T.erklaer, 0.25);
  tl.fromTo("#h1-k", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, T.erklaer + 0.15);
  popIn("#h1-ring", T.einer - 0.1, 0.35, 0.2);
  tl.fromTo("#h1-arc", { attr: { "stroke-dashoffset": 1068 } }, { attr: { "stroke-dashoffset": 0 }, duration: 0.6, ease: "power2.inOut" }, T.einer);
  slam("#h1-m", T.minute, 2.0);
  tl.to(["#h1-k", "#h1-m"], { opacity: 0, duration: 0.15 }, T.los - 0.1);
  tl.to("#h1-ring", { y: -360, scale: 0.25, opacity: 0, duration: 0.35, ease: "power3.in" }, T.los - 0.05);
  slam("#h1-los", T.los, 2.5);
  tl.to("#h1-los", { opacity: 0, scale: 1.4, duration: 0.25, ease: "power2.in" }, T.end - 0.25);
""", T)
SFX += [(T["deadline"] + 0.2, "boom", 0.55), (T["genie"], "pop", 0.45), (T["erklaer"], "whoosh", 0.4),
        (T["einer"] + 0.1, "boom", 0.7), (T["los"], "click", 0.7), (T["los"] - 0.05, "whoosh", 0.5)]

# ================================================================ Timer (oben, läuft 60 → 0)
TIMER_IN = W("Los!") + 0.12
sets = "".join(f'tl.set("#tm-n", {{ textContent: "0:{60 - i:02d}" }}, {T0 + i - TIMER_IN:.3f});' for i in range(1, 61))
scene("tm", TIMER_IN, min(T1 + 1.2, END), f"""
  <div id="tm-box" class="actor card" style="left:360px;top:296px;width:360px;height:104px;border-radius:52px;display:flex;align-items:center;justify-content:center;gap:22px;opacity:0">
    <svg viewBox="-30 -34 60 64" width="56" height="60"><circle r="24" fill="none" stroke="{AMBER}" stroke-width="6"/><rect x="-6" y="-34" width="12" height="8" rx="2" fill="{AMBER}"/>
      <path id="tm-hand" d="M0,0 L0,-15" stroke="{AMBER}" stroke-width="6" stroke-linecap="round"/></svg>
    <div id="tm-n" class="mono" style="font-size:68px;color:#FFF">1:00</div></div>
  <div id="tm-bar" class="actor" style="left:400px;top:412px;width:280px;height:8px;border-radius:4px;background:{AMBER};transform-origin:0 50%;opacity:0"></div>""", f"""
  popIn("#tm-box", 0, 0.35, 0.3);
  fadeIn("#tm-bar", 0.2, 0.2);
  tl.fromTo("#tm-bar", {{ scaleX: 1 }}, {{ scaleX: 0, duration: 60, ease: "none", immediateRender: false }}, {T0 - TIMER_IN:.3f});
  tl.fromTo("#tm-hand", {{ rotation: 0 }}, {{ rotation: 360 * 60, svgOrigin: "0 0", duration: 60, ease: "none", immediateRender: false }}, {T0 - TIMER_IN:.3f});
  {sets}
  tl.set(["#tm-n"], {{ color: "{RED}" }}, {T1 - 10 - TIMER_IN:.3f});
  tl.set("#tm-bar", {{ backgroundColor: "{RED}" }}, {T1 - 10 - TIMER_IN:.3f});
  for (let i = 5; i >= 1; i--) tl.fromTo("#tm-box", {{ scale: 1.14 }}, {{ scale: 1, duration: 0.4, ease: "power2.out", immediateRender: false }}, {T1 - TIMER_IN:.3f} - i);
  tl.fromTo("#tm-box", {{ scale: 1.35 }}, {{ scale: 1, duration: 0.5, ease: "elastic.out(1, 0.4)", immediateRender: false }}, {T1 - TIMER_IN:.3f});
  tl.to(["#tm-box", "#tm-bar"], {{ opacity: 0, y: -40, duration: 0.3, ease: "power2.in" }}, T.end - 0.3);
""", {}, track=3)
SFX += [(T1 - 5, "tick", 0.32)]

# ================================================================ P1 Parkinsons Gesetz: Zeit-Kasten mit Arbeit-Blob → FR 23:58
a, e = SEG["go"][1], SEG["r_park"][1]
T = dict(erstens=W("Erstens:"), arbeit=W("Arbeit"), dehnt=W("dehnt"), zeit=W("Zeit", 14), drei=W("Drei", 15), nichts=W("nichts"),
         freitag=W("Freitag,"), konkret=W("konkret."))
scene("p1", a, e, f"""
  <div id="p1-cam" class="lay">
    {tag("p1", 1, "PARKINSONS GESETZ")}
    <div id="p1-g" class="lay">
      {ctext("p1-lab", 540, "ZEIT", 48, cls="", color=MUTED, extra="font-weight:800;letter-spacing:.3em")}
      <div id="p1-box" class="actor" style="left:170px;top:610px;width:740px;height:260px;border:5px solid #C9CDD4;border-radius:22px;opacity:0"></div>
      <div id="p1-blob" class="actor" style="left:195px;top:640px;width:690px;height:200px;border-radius:90px;background:{ORANGE};box-shadow:0 0 50px rgba(255,122,26,.45);opacity:0"></div>
      {ctext("p1-bt", 712, "ARBEIT", 64, color="#1A1A1A")}
      {ctext("p1-nix", 920, "= GEFÜHLT: NICHTS", 64, color=AMBER)}
    </div>
    <div id="p1-clk" class="t mono" style="left:0;width:1080px;top:560px;text-align:center;font-size:170px;color:#FF5A4A;text-shadow:0 0 50px rgba(255,60,40,.7);opacity:0">
      <span style="font-size:70px;color:#C44;vertical-align:middle;margin-right:24px">FR</span>23:58</div>
    {ctext("p1-k", 820, "SEHR KONKRET.", 110, color=AMBER)}
  </div>""", r"""
  tagIn("#p1-tag", T.erstens);
  fadeIn("#p1-lab", T.arbeit - 0.1, 0.2);
  tl.fromTo("#p1-box", { opacity: 0, scaleX: 0.18, scaleY: 0.5 }, { opacity: 1, scaleX: 0.405, scaleY: 1, duration: 0.3, ease: "back.out(2)" }, T.arbeit - 0.1);
  tl.fromTo("#p1-blob", { opacity: 0, scaleX: 0.1, scaleY: 0.3 }, { opacity: 1, scaleX: 0.348, scaleY: 1, duration: 0.35, ease: "back.out(2)" }, T.arbeit);
  fadeIn("#p1-bt", T.arbeit + 0.1, 0.2);
  tl.to("#p1-box", { scaleX: 1, duration: 0.6, ease: "power3.inOut" }, T.dehnt);
  tl.to("#p1-blob", { scaleX: 1, duration: 1.0, ease: "elastic.out(1, 0.5)" }, T.dehnt + 0.15);
  tl.fromTo("#p1-lab", { color: "#8C8F96", scale: 1 }, { color: "#E8C27A", scale: 1.3, duration: 0.25, yoyo: true, repeat: 1, immediateRender: false }, T.zeit);
  tl.set("#p1-lab", { textContent: "3 WOCHEN" }, T.drei);
  tl.fromTo("#p1-lab", { scale: 1.5 }, { scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, T.drei);
  tl.to(["#p1-blob", "#p1-box", "#p1-bt"], { opacity: 0.18, filter: "blur(6px)", duration: 0.5, ease: "power2.out" }, T.nichts - 0.1);
  slam("#p1-nix", T.nichts, 1.8);
  tl.to("#p1-g", { opacity: 0, scale: 0.85, duration: 0.25, ease: "power2.in" }, T.freitag - 0.25);
  slam("#p1-clk", T.freitag, 2.8);
  shake("#p1-cam", T.freitag + 0.22, 18);
  tl.fromTo("#p1-clk", { scale: 1 }, { keyframes: [{ scale: 1.06, duration: 0.25 }, { scale: 1, duration: 0.25 }], repeat: 4, immediateRender: false }, T.freitag + 0.5);
  slam("#p1-k", T.konkret, 2.0);
  tl.to("#p1-cam", { opacity: 0, duration: 0.2 }, T.end - 0.2);
""", T)
SFX += [(T["erstens"], "whoosh", 0.45), (T["arbeit"], "pop", 0.45), (T["dehnt"], "whoosh", 0.4), (T["nichts"], "drop", 0.4),
        (T["freitag"] + 0.2, "boom", 0.75), (T["konkret"], "pop", 0.4)]

# ================================================================ P2 Der Turbo: Countdown, Alarm, Waage, EKG, Tunnelblick, Ablenkungen, Kurve
a, e = SEG["r_turbo"]
T = dict(zweitens=W("Zweitens:"), turbo=W("Turbo."), naeher=W("näher"), desto=W("desto"), alarm=W("Alarm"), ploetzlich=W("Plötzlich", 28), nicht=W("Nicht-Machen"),
         machen=W("Machen.", 30), stress=W("Stresshormone,"), puls=W("Puls"), fokus=W("Fokus"), ablenk=W("Ablenkungen?"), weg=W("Weg."),
         bis=W("Bis", 37), punkt=W("Punkt"), leistung=W("Leistung."), kippt=W("kippt"), ende=W("sie.", 40))
# Kurve (umgekehrtes U) als Pfad + Keyframes für den Punkt
CX0, CX1, CB, CH = 200, 880, 960, 360
pts = [(CX0 + (CX1 - CX0) * u, CB - CH * math.sin(math.pi * u) ** 1.2) for u in [i / 60 for i in range(61)]]
path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
up_kf = ", ".join(f'{{ x: {x - CX0:.1f}, y: {y - CB:.1f}, duration: {(T["leistung"] - T["punkt"]) / 31:.3f} }}' for x, y in pts[:31])
dn_kf = ", ".join(f'{{ x: {x - CX0:.1f}, y: {y - CB:.1f}, duration: {(e - T["kippt"] - 0.1) / 31:.3f} }}' for x, y in pts[30:])
ekg = "M170,700 " + " ".join(f"l{40},0 l12,-20 l10,20 l14,0 l8,26 l12,-150 l12,180 l10,-56 l30,0" for _ in range(5))
icons = [("📱", -280, -150), ("📺", 280, -150), ("🍕", -290, 120), ("💬", 290, 120), ("🐧", 0, -150), ("🎮", 0, 230)]
ic = "".join(f'<div id="p2-i{i}" class="actor emo" style="left:{490 + dx}px;top:{690 + dy}px;font-size:100px;opacity:0">{e_}</div>' for i, (e_, dx, dy) in enumerate(icons))
ic_out = "".join(f'tl.to("#p2-i{i}", {{ x: {dx * 3}, y: {dy * 3}, rotation: {(-1) ** i * 200}, opacity: 0, duration: 0.45, ease: "power3.in" }}, T.weg);' for i, (_, dx, dy) in enumerate(icons))
scene("p2", a, e, f"""
  <div id="p2-cam" class="lay">
    {tag("p2", 2, "DER TURBO")}
    {ctext("p2-tb", 600, 'TURBO <span class="emo">🚀</span>', 170, color=ORANGE, extra="text-shadow:0 0 50px rgba(255,122,26,.5)")}
    <div id="p2-A" class="lay">
      {ctext("p2-dk", 540, "DEADLINE IN", 50, cls="", color=MUTED, extra="font-weight:800;letter-spacing:.25em")}
      <div id="p2-dn" class="t mono" style="left:0;width:1080px;top:620px;text-align:center;font-size:120px;color:#FFF;opacity:0">3 WOCHEN</div>
    </div>
    <div id="p2-B" class="lay">
      <div id="p2-r0" class="actor" style="left:390px;top:540px;width:300px;height:300px;border-radius:50%;border:8px solid {RED};opacity:0"></div>
      <div id="p2-r1" class="actor" style="left:390px;top:540px;width:300px;height:300px;border-radius:50%;border:8px solid {RED};opacity:0"></div>
      <div id="p2-sir" class="actor emo" style="left:440px;top:590px;font-size:200px;opacity:0">🚨</div>
      {ctext("p2-al", 870, "ALARM!", 120, color=RED, extra="text-shadow:0 0 40px rgba(255,60,40,.6)")}
    </div>
    <div id="p2-C" class="lay" style="opacity:0">
      <div class="actor" style="left:520px;top:640px;width:40px;height:300px;background:#4A4E57;border-radius:8px"></div>
      <div class="actor" style="left:400px;top:930px;width:280px;height:30px;background:#4A4E57;border-radius:12px"></div>
      <div id="p2-beam" class="actor" style="left:190px;top:610px;width:700px;height:300px;transform-origin:350px 30px">
        <div class="actor" style="left:0;top:20px;width:700px;height:22px;background:#C9CDD4;border-radius:11px"></div>
        <div class="actor" style="left:330px;top:12px;width:40px;height:40px;border-radius:50%;background:{AMBER}"></div>
        <div id="p2-pl" class="actor" style="left:-10px;top:42px;width:240px;height:150px;border-bottom:8px solid #C9CDD4;border-left:4px solid transparent;border-right:4px solid transparent">
          <div id="p2-ml" class="t cond" style="left:0;width:240px;top:72px;text-align:center;font-size:52px">MACHEN</div></div>
        <div id="p2-pr" class="actor" style="left:470px;top:42px;width:240px;height:150px;border-bottom:8px solid #C9CDD4">
          <div class="t cond" style="left:0;width:240px;top:20px;text-align:center;font-size:52px;color:{RED};line-height:1.0">NICHT<br>MACHEN</div></div>
        <div id="p2-wt" class="actor emo" style="left:540px;top:-120px;font-size:100px;opacity:0">😱</div>
      </div>
    </div>
    <div id="p2-D" class="lay" style="opacity:0">
      {ctext("p2-sh", 520, "STRESSHORMONE ↑", 60, color=AMBER)}
      <svg class="actor" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">
        <path id="p2-ekg" d="{ekg}" fill="none" stroke="{GREEN}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"
          stroke-dasharray="4000" stroke-dashoffset="4000" style="filter:drop-shadow(0 0 10px rgba(91,227,125,.7))"/></svg>
      <div id="p2-bpm" class="t" style="left:0;width:1080px;top:820px;text-align:center;opacity:0">
        <span id="p2-hrt" class="emo" style="display:inline-block;font-size:80px;vertical-align:middle">❤️</span>
        <span id="p2-n" class="mono" style="font-size:96px;vertical-align:middle;margin-left:16px">72</span>
        <span class="mono" style="font-size:44px;color:{MUTED};vertical-align:middle">BPM</span></div>
      <div id="p2-tun" class="actor" style="left:-1080px;top:-1400px;width:3240px;height:4320px;opacity:0;
        background:radial-gradient(circle at 50% 50%, transparent 0px, transparent 360px, rgba(0,0,0,.92) 580px)"></div>
      {ctext("p2-fk", 1000, "TUNNELBLICK", 56, cls="", color="#FFF", extra="font-weight:800;letter-spacing:.3em")}
      {ic}
    </div>
    <div id="p2-E" class="lay" style="opacity:0">
      <svg class="actor" style="left:0;top:0" width="1080" height="1920" viewBox="0 0 1080 1920">
        <path d="M{CX0 - 20},{CB + 20} L{CX1 + 30},{CB + 20}" stroke="#5A606B" stroke-width="4"/>
        <path d="M{CX0 - 20},{CB + 20} L{CX0 - 20},{CB - CH - 30}" stroke="#5A606B" stroke-width="4"/>
        <path id="p2-cv" d="{path}" fill="none" stroke="{AMBER}" stroke-width="8" stroke-linecap="round" stroke-dasharray="1400" stroke-dashoffset="1400"/></svg>
      <div class="t" style="left:{CX0}px;top:{CB - CH - 40}px;font-size:30px;font-weight:800;letter-spacing:.2em;color:{MUTED}">LEISTUNG</div>
      <div class="t" style="left:{CX1 - 190}px;top:{CB + 36}px;font-size:30px;font-weight:800;letter-spacing:.2em;color:{MUTED}">DRUCK →</div>
      <div id="p2-dot" class="actor" style="left:{CX0 - 26}px;top:{CB - 26}px;width:52px;height:52px;border-radius:50%;background:{ORANGE};border:5px solid #FFF;box-shadow:0 0 30px rgba(255,122,26,.8);opacity:0"></div>
      <div id="p2-top" class="t cond" style="left:0;width:1080px;text-align:center;top:515px;font-size:64px;color:{GREEN};opacity:0">TOP!</div>
      <div id="p2-zv" class="t cond" style="left:0;width:1080px;text-align:center;top:515px;font-size:64px;color:{RED};opacity:0">ZU VIEL!</div>
    </div>
  </div>""", f"""
  tagIn("#p2-tag", T.zweitens);
  slam("#p2-tb", T.turbo, 2.2);
  tl.to("#p2-tb", {{ x: 900, opacity: 0, duration: 0.3, ease: "power3.in" }}, T.naeher - 0.3);
  fadeIn("#p2-dk", T.naeher - 0.15, 0.2);
  popIn("#p2-dn", T.naeher - 0.1, 0.25, 0.6);
  tl.set("#p2-dn", {{ textContent: "3 TAGE" }}, T.naeher + 0.45);
  tl.set("#p2-dn", {{ textContent: "3 STUNDEN", color: "{RED}" }}, T.naeher + 0.9);
  [0.45, 0.9].forEach(d => tl.fromTo("#p2-dn", {{ scale: 1.35 }}, {{ scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }}, T.naeher + d));
  outUp("#p2-A", T.alarm - 0.25);
  slam("#p2-sir", T.alarm - 0.05, 2.2);
  for (let i = 0; i < 4; i++) tl.fromTo(i % 2 ? "#p2-r1" : "#p2-r0", {{ opacity: 0.9, scale: 0.7 }}, {{ opacity: 0, scale: 1.9, duration: 0.6, ease: "power2.out", immediateRender: false }}, T.alarm + i * 0.3);
  slam("#p2-al", T.alarm + 0.1, 2);
  shake("#p2-cam", T.alarm + 0.3, 12);
  outUp("#p2-B", T.ploetzlich - 0.1);
  fadeIn("#p2-C", T.ploetzlich, 0.25);
  tl.fromTo("#p2-beam", {{ rotation: -12 }}, {{ rotation: -12, duration: 0.01 }}, T.ploetzlich);
  tl.fromTo("#p2-wt", {{ opacity: 0, y: -200 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.in" }}, T.nicht);
  tl.to("#p2-beam", {{ rotation: 14, duration: 0.7, ease: "elastic.out(1, 0.5)" }}, T.nicht + 0.3);
  tl.to("#p2-ml", {{ color: "{GREEN}", scale: 1.25, duration: 0.25, ease: "back.out(2)" }}, T.machen);
  outUp("#p2-C", T.stress - 0.2);
  fadeIn("#p2-D", T.stress - 0.1, 0.15);
  popIn("#p2-sh", T.stress, 0.3, 0.6);
  tl.fromTo("#p2-ekg", {{ attr: {{ "stroke-dashoffset": 4000 }} }}, {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 2.4, ease: "none" }}, T.stress + 0.1);
  fadeIn("#p2-bpm", T.puls - 0.2, 0.2);
  tl.fromTo("#p2-n", {{ textContent: 72 }}, {{ textContent: 148, duration: 1.0, ease: "power2.in", snap: {{ textContent: 1 }} }}, T.puls);
  for (let i = 0; i < 6; i++) tl.fromTo("#p2-hrt", {{ scale: 1.3 }}, {{ scale: 1, duration: 0.25, ease: "power2.out", immediateRender: false }}, T.puls + i * 0.38);
  tl.fromTo("#p2-tun", {{ opacity: 0, scale: 2.4 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "power3.inOut" }}, T.fokus);
  tl.to("#p2-sh", {{ opacity: 0, duration: 0.2 }}, T.fokus);
  popIn("#p2-fk", T.fokus + 0.3, 0.3, 0.6);
  tl.to(["#p2-ekg", "#p2-bpm", "#p2-fk"], {{ opacity: 0.2, duration: 0.2 }}, T.ablenk - 0.1);
  for (let i = 0; i < 6; i++) popIn(`#p2-i${{i}}`, T.ablenk + i * 0.06, 0.25, 0.2);
  {ic_out}
  outUp("#p2-D", T.bis - 0.2);
  fadeIn("#p2-E", T.bis - 0.05, 0.2);
  tl.fromTo("#p2-cv", {{ attr: {{ "stroke-dashoffset": 1400 }} }}, {{ attr: {{ "stroke-dashoffset": 0 }}, duration: 0.8, ease: "power2.inOut" }}, T.bis);
  popIn("#p2-dot", T.bis + 0.2, 0.25, 0.3);
  tl.to("#p2-dot", {{ keyframes: [{up_kf}], ease: "none" }}, T.punkt);
  popIn("#p2-top", T.leistung, 0.3, 0.5);
  tl.to("#p2-top", {{ opacity: 0, duration: 0.2 }}, T.kippt - 0.1);
  tl.to("#p2-dot", {{ keyframes: [{dn_kf}], ease: "none" }}, T.kippt);
  tl.to("#p2-dot", {{ backgroundColor: "{RED}", duration: 0.2 }}, T.kippt);
  slam("#p2-zv", T.kippt, 2);
  tl.to("#p2-cam", {{ opacity: 0, duration: 0.2 }}, T.end - 0.2);
""", T)
SFX += [(T["zweitens"], "whoosh", 0.45), (T["turbo"], "boom", 0.45), (T["naeher"] - 0.3, "whoosh", 0.4), (T["naeher"], "tick", 0.25), (T["alarm"], "boom", 0.6), (T["nicht"] + 0.25, "drop", 0.5),
        (T["machen"], "pop", 0.35), (T["puls"], "heart", 0.6), (T["fokus"], "whoosh", 0.35), (T["ablenk"], "pop", 0.35),
        (T["weg"], "whoosh", 0.6), (T["bis"], "whoosh", 0.25), (T["leistung"], "pop", 0.4), (T["kippt"], "scratch", 0.35)]

# ================================================================ P3 Genie-Illusion: GENIE → ILLUSION, Balken, Polaroids
a, e = SEG["r_illusion"]
T = dict(aber=W("Aber:"), genie=W("Genie", 41), illusion=W("Illusion."), lang=W("Langzeitstudie"), stress=W("Stress,", 45),
         krank=W("Krankheitssymptome"), schlecht=W("schlechtere"), du=W("Du", 49.5), eine=W("eine", 50.5), geklappt=W("geklappt"))
bars = [("STRESS", 300, RED, "↑"), ("KRANK", 540, RED, "↑"), ("NOTEN", 780, GREEN, "")]
bh = "".join(f'<div id="p3-b{i}" class="actor" style="left:{x - 80}px;top:650px;width:160px;height:290px;transform-origin:50% 100%;'
             f'background:{c};border-radius:14px 14px 4px 4px;opacity:0"></div>'
             f'<div class="t" style="left:{x - 120}px;width:240px;top:955px;text-align:center;font-size:34px;font-weight:800;letter-spacing:.14em">{lab}</div>'
             f'<div id="p3-a{i}" class="t cond" style="left:{x - 60}px;width:120px;top:572px;text-align:center;font-size:80px;color:{RED};opacity:0">↑</div>'
             for i, (lab, x, c, _) in enumerate(bars))
pol = [("🌙", "GEKLAPPT ✓", 230, 540), ("😬", "KNAPP", 580, 540), ("🙈", "PEINLICH", 230, 805), ("😐", "MITTELMÄSSIG", 580, 805)]
ph = "".join(f'<div id="p3-p{i}" class="actor" style="left:{x}px;top:{y}px;width:270px;height:250px;background:#EDE6D6;border-radius:8px;padding:14px;'
             f'transform:rotate({(-4, 3, 2, -3)[i]}deg);box-shadow:0 20px 50px rgba(0,0,0,.6);opacity:0">'
             f'<div style="height:160px;background:#2A2D33;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:90px">{em}</div>'
             f'<div style="text-align:center;margin-top:12px;font-size:28px;font-weight:900;color:#1A1A1A;letter-spacing:.06em">{lab}</div></div>'
             for i, (em, lab, x, y) in enumerate(pol))
scene("p3", a, e, f"""
  <div id="p3-cam" class="lay">
    {tag("p3", 3, "DIE GENIE-ILLUSION")}
    <div id="p3-A" class="lay">
      <div id="p3-bulb" class="actor emo" style="left:450px;top:520px;font-size:180px;opacity:0">💡</div>
      {ctext("p3-g", 740, "GENIE", 210, color=AMBER, extra="text-shadow:0 0 50px rgba(232,194,122,.5)")}
      <div id="p3-st" class="t cond" data-layout-allow-overlap style="left:190px;width:700px;top:760px;text-align:center;font-size:150px;color:{RED};border:12px solid {RED};border-radius:20px;
        padding:6px 0;transform:rotate(-9deg);opacity:0;background:rgba(11,12,14,.55)">ILLUSION</div>
    </div>
    <div id="p3-B" class="lay" style="opacity:0">
      {ctext("p3-h", 512, "AUFSCHIEBER AM ENDE:", 40, cls="", color="#EDE6D6", extra="font-weight:800;letter-spacing:.14em")}
      {bh}
      {ctext("p3-src", 1018, "Tice &amp; Baumeister (1997) · vereinfacht", 28, cls="", color=MUTED, extra="font-weight:600")}
    </div>
    <div id="p3-C" class="lay">{ph}</div>
  </div>""", r"""
  tagIn("#p3-tag", T.aber);
  popIn("#p3-bulb", T.genie - 0.1, 0.3, 0.3);
  popIn("#p3-g", T.genie, 0.3, 0.5);
  slam("#p3-st", T.illusion, 2.6);
  shake("#p3-cam", T.illusion + 0.22, 16);
  tl.to("#p3-bulb", { opacity: 0.2, filter: "grayscale(1)", duration: 0.15, ease: "steps(3)" }, T.illusion + 0.2);
  tl.to("#p3-g", { opacity: 0.35, duration: 0.2 }, T.illusion + 0.2);
  outUp("#p3-A", T.lang - 0.3);
  fadeIn("#p3-B", T.lang - 0.05, 0.15);
  fadeIn("#p3-h", T.lang, 0.25);
  fadeIn("#p3-src", T.lang + 0.2, 0.25);
  [0, 1, 2].forEach(i => tl.fromTo(`#p3-b${i}`, { opacity: 0, scaleY: 0 }, { opacity: 1, scaleY: i < 2 ? 0.12 : 0.8, duration: 0.3, ease: "power3.out" }, T.lang + 0.15 + i * 0.08));
  tl.to("#p3-b0", { scaleY: 0.95, duration: 0.5, ease: "back.out(1.6)" }, T.stress);
  popIn("#p3-a0", T.stress + 0.1, 0.25, 0.4);
  tl.to("#p3-b1", { scaleY: 0.85, duration: 0.5, ease: "back.out(1.6)" }, T.krank);
  popIn("#p3-a1", T.krank + 0.1, 0.25, 0.4);
  tl.to("#p3-b2", { scaleY: 0.25, backgroundColor: "#FF4B3E", duration: 0.5, ease: "power3.in" }, T.schlecht);
  tl.set("#p3-a2", { textContent: "↓", top: 760 }, T.schlecht);
  popIn("#p3-a2", T.schlecht + 0.35, 0.25, 0.4);
  outUp("#p3-B", T.du - 0.2);
  for (let i = 0; i < 4; i++) tl.fromTo(`#p3-p${i}`, { opacity: 0, y: 120, scale: 0.7 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, T.du + i * 0.08);
  tl.to("#p3-p0", { scale: 1.1, boxShadow: "0 0 60px rgba(232,194,122,.9)", zIndex: 5, duration: 0.3, ease: "back.out(2)" }, T.eine);
  tl.to(["#p3-p1", "#p3-p2", "#p3-p3"], { opacity: 0.18, filter: "grayscale(1) blur(3px)", scale: 0.9, duration: 0.5, ease: "power2.out" }, T.geklappt - 0.3);
  tl.to("#p3-cam", { opacity: 0, duration: 0.2 }, T.end - 0.2);
""", T)
SFX += [(T["aber"], "whoosh", 0.45), (T["genie"], "pop", 0.4), (T["illusion"] + 0.2, "boom", 0.75), (T["stress"], "pop", 0.4),
        (T["krank"], "pop", 0.4), (T["schlecht"], "drop", 0.4), (T["du"], "pop", 0.3), (T["eine"], "click", 0.5)]

# ================================================================ P4 Der Trick: Deadline nach vorne, Studie, Zwischen-Deadlines, öffentlich, Wenn-dann
a, e = SEG["r_trick"]
T = dict(der=W("Der", 52.5), deadline=W("Deadline", 53.5), nach=W("nach", 54), studien=W("Studien"), feste=W("Feste"), schlagen=W("schlagen"),
         eine=W("eine", 57.9), also=W("Also:"), zwd=W("Zwischen-Deadlines."), sag=W("Sag"), fertig=W("fertig"), bist=W("bist.", 63.5),
         und=W("Und", 64), plan=W("Wenn-dann-Plan:"), wenn=W("Wenn", 66), oeffne=W("öffne"), datei=W("Datei."))
days = "".join(f'<div class="actor" style="left:{190 + i * 175 - 2}px;top:690px;width:4px;height:30px;background:#5A606B"></div>'
               f'<div class="t" style="left:{190 + i * 175 - 50}px;width:100px;top:740px;text-align:center;font-size:32px;font-weight:800;color:#9AA0AA">{d}</div>'
               for i, d in enumerate(["MO", "DI", "MI", "DO", "FR"]))
blocks = "".join(f'<div id="p4-k{i}" class="actor" style="left:{200 + i * 170}px;top:690px;width:170px;height:170px;background:{ORANGE};'
                 f'border-radius:{"18px 0 0 18px" if i == 0 else ("0 18px 18px 0" if i == 3 else "0")};opacity:0">'
                 f'<div id="p4-kt{i}" class="t" style="left:0;width:170px;top:-70px;text-align:center;opacity:0"><span style="padding:6px 16px;border-radius:10px;'
                 f'background:#16181D;border:2px solid {AMBER};font-size:30px;font-weight:900;color:{AMBER}">{d}</span></div></div>'
                 for i, d in enumerate(["MO", "DI", "MI", "DO"]))
scene("p4", a, e, f"""
  <div id="p4-cam" class="lay">
    {tag("p4", 4, "DER TRICK")}
    <div id="p4-A" class="lay">
      <div class="actor" style="left:170px;top:703px;width:740px;height:5px;background:#5A606B;border-radius:3px"></div>
      {days}
      <div id="p4-fl" class="actor" style="left:830px;top:540px;width:160px;height:160px;opacity:0">
        <div class="emo" style="position:absolute;left:30px;top:30px;font-size:110px">🚩</div>
        <div class="t" style="left:-20px;width:200px;top:-10px;text-align:center;font-size:30px;font-weight:900;color:{RED};letter-spacing:.1em">DEADLINE</div></div>
      {ctext("p4-nv", 840, "← NACH VORNE", 90, color=AMBER)}
    </div>
    <div id="p4-B" class="lay" style="opacity:0">
      <div id="p4-g" class="actor" style="left:250px;top:610px;width:220px;height:330px;transform-origin:50% 100%;background:{GREEN};border-radius:16px 16px 4px 4px;opacity:0"></div>
      <div id="p4-tr" class="actor emo" style="left:305px;top:505px;font-size:100px;opacity:0">🏆</div>
      <div id="p4-r" class="actor" style="left:610px;top:820px;width:220px;height:120px;transform-origin:50% 100%;background:{RED};border-radius:16px 16px 4px 4px;opacity:0"></div>
      <div class="t" style="left:180px;width:360px;top:955px;text-align:center;font-size:30px;font-weight:800;letter-spacing:.06em">ZWISCHENTERMINE</div>
      <div class="t" style="left:540px;width:360px;top:955px;text-align:center;font-size:30px;font-weight:800;letter-spacing:.06em">1 DEADLINE</div>
      {ctext("p4-src", 1010, "Ariely &amp; Wertenbroch (2002)", 28, cls="", color=MUTED, extra="font-weight:600")}
    </div>
    <div id="p4-C" class="lay">
      {ctext("p4-ch", 520, "ZWISCHEN-DEADLINES", 70, color="#FFF")}
      {blocks}
      {ctext("p4-pj", 735, "PROJEKT", 80, color="#1A1A1A")}
    </div>
    <div id="p4-D" class="lay">
      <div id="p4-chat" class="actor card" style="left:180px;top:520px;width:720px;height:470px;opacity:0">
        <div style="height:84px;border-bottom:2px solid #3A3F48;display:flex;align-items:center;gap:18px;padding:0 30px;font-size:34px;font-weight:800">
          <span class="emo" style="font-size:44px">👥</span>Team</div>
        <div id="p4-msg" class="actor" style="right:30px;top:130px;padding:20px 28px;background:{ORANGE};border-radius:28px 28px 6px 28px;font-size:42px;font-weight:800;color:#1A1A1A;opacity:0">
          Bis Mittwoch fertig! 💪 <span id="p4-ck" style="color:#FFF;font-size:30px;opacity:0">✓✓</span></div>
        <div id="p4-rep" class="actor" style="left:30px;top:270px;padding:20px 28px;background:#2E333B;border-radius:28px 28px 28px 6px;font-size:42px;font-weight:700;opacity:0">
          Deal! 👍</div></div>
    </div>
    <div id="p4-E" class="lay">
      {ctext("p4-eh", 520, "WENN-DANN-PLAN", 70, color="#FFF")}
      <div id="p4-w" class="actor" style="left:170px;top:640px;width:370px;height:260px;opacity:0;z-index:2">
        <div style="position:absolute;inset:0;background:{AMBER};border-radius:24px 0 0 24px"></div>
        <div style="position:absolute;right:-44px;top:90px;width:88px;height:88px;border-radius:50%;background:{AMBER}"></div>
        <div class="t cond" style="left:36px;top:36px;font-size:60px;color:#1A1A1A">WENN</div>
        <div class="t" style="left:36px;top:130px;font-size:40px;font-weight:800;color:#1A1A1A;line-height:1.15">Dienstag,<br>18 Uhr</div></div>
      <div id="p4-d" class="actor" style="left:540px;top:640px;width:370px;height:260px;opacity:0">
        <div style="position:absolute;inset:0;background:{ORANGE};border-radius:0 24px 24px 0"></div>
        <div style="position:absolute;left:-44px;top:90px;width:88px;height:88px;border-radius:50%;background:#0B0C0E"></div>
        <div class="t cond" style="left:80px;top:36px;font-size:60px;color:#1A1A1A">DANN</div>
        <div class="t" style="left:80px;top:130px;font-size:40px;font-weight:800;color:#1A1A1A;line-height:1.15">Datei<br>öffnen</div></div>
      <div id="p4-ok" class="t emo" style="left:0;width:1080px;top:930px;text-align:center;font-size:90px;opacity:0">✅</div>
    </div>
  </div>""", r"""
  tagIn("#p4-tag", T.der);
  popIn("#p4-fl", T.deadline - 0.1, 0.3, 0.3);
  tl.to("#p4-fl", { x: -350, duration: 0.5, ease: "back.inOut(1.6)" }, T.nach);
  popIn("#p4-nv", T.nach + 0.2, 0.3, 0.5);
  outUp("#p4-A", T.studien - 0.1);
  fadeIn("#p4-B", T.studien, 0.2);
  tl.fromTo("#p4-g", { opacity: 0, scaleY: 0 }, { opacity: 1, scaleY: 1, duration: 0.5, ease: "back.out(1.5)" }, T.feste);
  popIn("#p4-tr", T.schlagen, 0.35, 0.3);
  tl.fromTo("#p4-r", { opacity: 0, scaleY: 0 }, { opacity: 1, scaleY: 1, duration: 0.4, ease: "power3.out" }, T.eine + 0.2);
  fadeIn("#p4-src", T.feste + 0.3, 0.3);
  outUp("#p4-B", T.also - 0.1);
  popIn("#p4-ch", T.also + 0.1, 0.3, 0.6);
  for (let i = 0; i < 4; i++) fadeIn(`#p4-k${i}`, T.also + 0.15, 0.2);
  fadeIn("#p4-pj", T.also + 0.15, 0.2);
  tl.to("#p4-pj", { opacity: 0, scale: 1.4, duration: 0.2 }, T.zwd);
  for (let i = 0; i < 4; i++) {
    tl.to(`#p4-k${i}`, { x: (i - 1.5) * 30, borderRadius: 18, duration: 0.35, ease: "back.out(2)" }, T.zwd + 0.05);
    popIn(`#p4-kt${i}`, T.zwd + 0.3 + i * 0.12, 0.25, 0.4);
  }
  outUp("#p4-C", T.sag - 0.15);
  popIn("#p4-chat", T.sag, 0.3, 0.7);
  tl.fromTo("#p4-msg", { opacity: 0, y: 140, scale: 0.7 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.8)" }, T.sag + 0.25);
  fadeIn("#p4-ck", T.bist, 0.15);
  tl.fromTo("#p4-ck", { color: "#FFFFFF" }, { color: "#4FA3FF", duration: 0.2, immediateRender: false }, T.bist + 0.2);
  tl.fromTo("#p4-rep", { opacity: 0, y: 60, scale: 0.7 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, T.bist + 0.1);
  outUp("#p4-D", T.und - 0.1);
  popIn("#p4-eh", T.plan, 0.3, 0.6);
  tl.fromTo("#p4-w", { opacity: 0, x: -300 }, { opacity: 1, x: -40, duration: 0.4, ease: "power3.out" }, T.wenn);
  tl.fromTo("#p4-d", { opacity: 0, x: 300 }, { opacity: 1, x: 40, duration: 0.4, ease: "power3.out" }, T.oeffne - 0.1);
  tl.to(["#p4-w", "#p4-d"], { x: 0, duration: 0.2, ease: "power4.in" }, T.datei);
  tl.fromTo("#p4-E", { scale: 1 }, { keyframes: [{ scale: 1.05, duration: 0.08 }, { scale: 1, duration: 0.3, ease: "elastic.out(1, 0.4)" }], immediateRender: false }, T.datei + 0.2);
  popIn("#p4-ok", T.datei + 0.25, 0.3, 0.3);
  tl.to("#p4-cam", { opacity: 0, duration: 0.15 }, T.end - 0.15);
""", T)
SFX += [(T["der"], "whoosh", 0.45), (T["deadline"], "pop", 0.35), (T["nach"], "whoosh", 0.5), (T["feste"], "pop", 0.35), (T["schlagen"], "pop", 0.5),
        (T["eine"] + 0.2, "drop", 0.3), (T["also"], "whoosh", 0.35), (T["zwd"] + 0.05, "click", 0.6)] + \
       [(T["zwd"] + 0.3 + i * 0.12, "pop", 0.25) for i in range(4)] + \
       [(T["sag"] + 0.25, "send", 0.6), (T["bist"] + 0.1, "pop", 0.3), (T["und"], "whoosh", 0.35), (T["wenn"], "whoosh", 0.35),
        (T["oeffne"] - 0.1, "whoosh", 0.35), (T["datei"] + 0.18, "click", 0.85)]

# ================================================================ P5 Zeit um! → ganze Folge auf YouTube
a, e = SEG["r_trick"][1], END
T = dict(zeit=T1, die=W("Die", 71), ganze=W("ganze"), youtube=W("YouTube."))
scene("p5", a, e, f"""
  <div id="p5-fl" class="actor" style="left:0;top:0;width:1080px;height:1920px;background:#FFF;opacity:0"></div>
  <div id="p5-cam" class="lay">
    {ctext("p5-zu", 620, "ZEIT UM!", 180, color=RED, extra="text-shadow:0 0 60px rgba(255,60,40,.7)")}
    {ctext("p5-k", 446, "DIE GANZE FOLGE", 56, cls="", color=AMBER, extra="font-weight:900;letter-spacing:.18em")}
    <div id="p5-card" class="actor" style="left:192px;top:540px;width:696px;height:391px;border-radius:22px;overflow:hidden;
      box-shadow:0 30px 90px rgba(0,0,0,.7), 0 0 0 4px #2A2D33;opacity:0">
      <img src="assets/thumb.png" style="width:696px;height:391px;display:block" />
      <div style="position:absolute;right:18px;bottom:18px;padding:4px 12px;border-radius:8px;background:rgba(0,0,0,.85);font-size:30px;font-weight:800">4:36</div>
      <div id="p5-play" style="position:absolute;left:288px;top:138px;width:120px;height:116px;opacity:0">
        <svg viewBox="0 0 120 116" width="120" height="116"><rect x="0" y="16" width="120" height="84" rx="24" fill="#FF0033"/><path d="M48,38 L82,58 L48,78 Z" fill="#FFF"/></svg></div>
    </div>
    <div id="p5-yt" class="t" style="left:0;width:1080px;top:960px;text-align:center;opacity:0">
      <span style="display:inline-flex;align-items:center;gap:14px;padding:10px 26px;border-radius:40px;background:#FF0033;font-size:36px;font-weight:900">
        ▶ YouTube · Otto Normalpsyche</span></div>
    {otto("p5", 70, 770, 0.36, ("happy",))}
  </div>""", r"""
  tl.fromTo("#p5-fl", { opacity: 0.55 }, { opacity: 0, duration: 0.35, ease: "power2.out", immediateRender: false }, T.zeit);
  slam("#p5-zu", T.zeit, 2.8);
  shake("#p5-cam", T.zeit + 0.22, 20);
  tl.to("#p5-zu", { y: -260, scale: 0.4, opacity: 0, duration: 0.3, ease: "power3.in" }, T.die - 0.2);
  fadeIn("#p5-k", T.die, 0.3);
  tl.fromTo("#p5-card", { opacity: 0, y: 200, scale: 0.8, rotation: -4 }, { opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.5, ease: "back.out(1.5)" }, T.die);
  popIn("#p5-play", T.ganze + 0.2, 0.35, 0.3);
  tl.fromTo("#p5-otto", { opacity: 0, y: 200 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.8)" }, T.ganze + 0.4);
  popIn("#p5-yt", T.youtube - 0.1, 0.35, 0.5);
  for (let i = 0; i < 4; i++) tl.fromTo("#p5-play", { scale: 1.15 }, { scale: 1, duration: 0.5, ease: "power2.out", immediateRender: false }, T.youtube + 0.5 + i * 0.8);
  tl.fromTo("#p5-card", { y: 0 }, { y: -12, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false }, T.youtube + 0.2);
""", T)
SFX += [(T["zeit"], "buzzer", 0.8), (T["zeit"] + 0.2, "boom", 0.5), (T["die"], "whoosh", 0.45), (T["ganze"] + 0.2, "pop", 0.4), (T["youtube"] - 0.1, "click", 0.6)]

# ================================================================ Film-Look (Korn, Vignette, Staub, Flackern) – deterministisch
_noise = ("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence "
          "type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")
motes = "".join(f'<div id="fr-m{i}" class="mote"></div>' for i in range(40))
open(f"{HERE}/compositions/frame.html", "w").write(f"""<template>
  <style>
  #root {{ position:absolute; inset:0; pointer-events:none; overflow:hidden; }}
  #root .mote {{ position:absolute; left:0; top:0; width:6px; height:6px; border-radius:50%; background:rgba(255,236,205,.9); filter:blur(1.2px); mix-blend-mode:screen; opacity:0; }}
  </style>
  <div id="root" data-composition-id="frame" data-width="1080" data-height="1920" data-layout-ignore>
    {motes}
    <div style="position:absolute;inset:0;background:#5a3c14;mix-blend-mode:soft-light;opacity:.3;"></div>
    <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%, transparent 48%, rgba(0,0,0,.6) 100%);"></div>
    <div id="fr-flick" style="position:absolute;inset:0;background:#000;opacity:0;"></div>
    <div id="fr-grain" style="position:absolute;inset:-64px;background-image:url(&quot;{_noise}&quot;);background-size:256px 256px;opacity:.12;mix-blend-mode:overlay;"></div>
  </div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  const H = (k, i) => {{ let x = Math.sin(k * 127.1 + i * 311.7) * 43758.5453; return x - Math.floor(x); }};
  const $ = id => document.getElementById(id);
  const motes = [...Array(40).keys()].map(i => ({{ el: $(`fr-m${{i}}`), x: H(i, 1) * 1080, y: H(i, 2) * 1920, vx: (H(i, 3) - 0.5) * 16, vy: -6 - H(i, 4) * 14,
      w: 0.4 + H(i, 5) * 0.9, ph: H(i, 6) * 6.28, s: 0.5 + H(i, 7) * 1.3 }}));
  function render(t) {{
    const k = Math.floor(t * 12);
    $("fr-grain").style.transform = `translate(${{-H(k, 1) * 64}}px, ${{-H(k, 2) * 64}}px)`;
    $("fr-flick").style.opacity = (0.015 + H(k, 3) * 0.05).toFixed(3);
    for (const m of motes) {{
      const x = ((m.x + m.vx * t + 40 * Math.sin(t * 0.3 + m.ph)) % 1080 + 1080) % 1080;
      const y = ((m.y + m.vy * t) % 1920 + 1920) % 1920;
      m.el.style.transform = `translate(${{x.toFixed(1)}}px, ${{y.toFixed(1)}}px) scale(${{m.s.toFixed(2)}})`;
      m.el.style.opacity = (0.1 + 0.25 * (0.5 + 0.5 * Math.sin(t * m.w + m.ph))).toFixed(3);
    }}
  }}
  const clock = {{ t: 0 }};
  tl.to(clock, {{ t: {END}, duration: {END}, ease: "none", onUpdate: () => render(clock.t) }}, 0);
  render(0);
  window.__timelines["frame"] = tl;
  </script>
</template>
""")

# ================================================================ Untertitel: 1–3 Wörter, aktives Wort gelb
groups, cur = [], []
for i, w in enumerate(WORDS):
    cur.append(w)
    nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
    if len(cur) >= 3 or len(" ".join(x["text"] for x in cur)) >= 16 or re.search(r"[.!?:,]$", w["text"]) or not nxt or nxt["start"] - w["end"] >= 0.3:
        groups.append(cur); cur = []
starts = [max(g[0]["start"] - 0.04, 0.05) for g in groups] + [END]
ch, cj = [], []
wi = 0
for gi, g in enumerate(groups):
    ga, gb = starts[gi], min(g[-1]["end"] + 0.3, END, starts[gi + 1] - 0.01)
    spans = []
    for w in g:
        spans.append(f'<span id="w{wi}">{w["text"].upper()}</span>')
        cj.append(f'tl.set("#w{wi}", {{ color: "{AMBER}" }}, {max(w["start"], ga):.3f});')
        wi += 1
    ch.append(f'<div id="k{gi}" class="clip cap" data-start="{ga:.3f}" data-duration="{gb - ga:.3f}">{" ".join(spans)}</div>')
    cj.append(f'tl.fromTo("#k{gi}", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: {min(0.12, (gb - ga) / 3):.3f}, ease: "back.out(2.5)" }}, {ga:.3f});'
              f'tl.to("#k{gi}", {{ opacity: 0, duration: {min(0.06, (gb - ga) / 4):.3f} }}, {gb - min(0.06, (gb - ga) / 4):.3f});')
open(f"{HERE}/compositions/captions.html", "w", encoding="utf-8").write(f"""<template>
  <style>
  #root {{ position:absolute; inset:0; }}
  #root .cap {{ position:absolute; left:192px; width:696px; top:1080px; text-align:center; font-family:'Inter', sans-serif; font-weight:900;
          font-size:64px; line-height:1.12; color:#FFF; opacity:0; letter-spacing:.01em;
          text-shadow:0 5px 0 #000, 0 0 24px rgba(0,0,0,.9), 3px 3px 0 #000, -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-layout-allow-caption-zone>{"".join(ch)}</div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  {"".join(cj)}
  window.__timelines["captions"] = tl;
  </script>
</template>
""")

# ================================================================ Root
hh = "\n".join(f'      <div id="{c}" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{a:.3f}" data-duration="{e - a:.3f}" '
               f'data-track-index="{tr}" data-track-kind="graphics" data-width="1080" data-height="1920"></div>' for c, a, e, tr in HOSTS)
open(f"{HERE}/index.html", "w").write(f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0B0C0E; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
{hh}
      <div id="frame" data-composition-id="frame" data-composition-src="compositions/frame.html" data-start="0" data-duration="{END}" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{END}" data-track-index="5" data-track-kind="captions" data-width="1080" data-height="1920"></div>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
# Kein Rauschen (Whoosh/Senden/Kratzen klangen wie eine Spraydose) → Klicks und Plops
SWAP = {"whoosh": ("click", 1.0), "send": ("pop", 1.0), "scratch": ("pop", 1.0)}
SFX = [(t, SWAP.get(f, (f, 1))[0], g * SWAP.get(f, (f, 1))[1]) for t, f, g in SFX]
SFX = [x for i, x in enumerate(sorted(SFX)) if not any(abs(x[0] - y[0]) < 0.06 and x[1] == y[1] for y in sorted(SFX)[:i])]
json.dump([{"t": round(t, 3), "f": f, "g": g} for t, f, g in SFX if g > 0], open(f"{HERE}/assets/sfx.json", "w"), indent=0)
for fn in ("hyperframes.json", "package.json", "meta.json"):
    open(f"{HERE}/{fn}", "w").write(open(os.path.join(ROOT, "video01-doku", fn)).read().replace("otto-video01-doku", "otto-video02-reel"))
print(f"Reel: {END}s, Timer {T0:.2f}→{T1:.2f}, {len(HOSTS)} Kompositionen, {len(groups)} Untertitel, {len(SFX)} Soundeffekte")
