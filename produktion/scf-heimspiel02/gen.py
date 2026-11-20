"""Reel „Frankenderby“ SCF Nürnberg vs. TSC Heuchelhof (1080x1920, 30 fps).

Liest assets/words.json + assets/segments.json (aus voice.py). Schreibt index.html, compositions/*.html, assets/sfx.json.
Look wie der Flyer: Schwarz/Dunkelrot, Signalrot #E3241B, Barlow Condensed (kursiv, schwer).
Sichere Zone Instagram: Text in y 168–1330, x 90–930 (rechts unten liegt die Aktionsleiste); Untertitel bei y ≈ 1215.
"""
import json, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = json.load(open(f"{HERE}/assets/words.json"))
SEG = {s["id"]: (s["start"], s["end"]) for s in json.load(open(f"{HERE}/assets/segments.json"))}
END = round(max(e for _, e in SEG.values()), 3)
RED, DARK, PAPER = "#E3241B", "#0B0506", "#FAF8F3"
os.makedirs(f"{HERE}/compositions", exist_ok=True)
SFX, HOSTS, CUR, CLICKS = [], [], [], []


def norm(w):
    return re.sub(r"[^\wäöüß0-9]", "", w.lower())


def W(word, after=0.0, end=False):
    for w in WORDS:
        if w["start"] >= after - 1e-6 and norm(w["text"]) == norm(word):
            return w["end"] if end else w["start"]
    raise KeyError(word)


FONTS = "".join(
    f"@font-face{{font-family:'BC';src:url('assets/fonts/barlow-condensed-latin-{w}-{s}.woff2') format('woff2');font-weight:{w};font-style:{s};}}"
    for w, s in [(900, "italic"), (800, "italic"), (800, "normal"), (600, "normal"), (400, "normal")])
CSS = FONTS + f"""
  #root {{ position:absolute; inset:0; overflow:hidden; color:#FFF; font-family:'BC', sans-serif; }}
  #root .a {{ position:absolute; }}
  #root .big {{ font-weight:900; font-style:italic; text-transform:uppercase; line-height:.86; white-space:nowrap; }}
  #root .lbl {{ font-weight:600; letter-spacing:.24em; text-transform:uppercase; color:{RED}; font-size:34px; white-space:nowrap; line-height:1; }}
  #root .ol {{ color:transparent; -webkit-text-stroke:5px #FFF; }}
  #root .c {{ left:0; width:1080px; text-align:center; }}
  #root .strip {{ display:inline-block; font-weight:900; font-style:italic; text-transform:uppercase; white-space:nowrap; line-height:1;
                 box-shadow:0 14px 30px rgba(0,0,0,.45); }}
  #root .chip {{ display:inline-block; font-weight:800; font-style:italic; text-transform:uppercase; white-space:nowrap; line-height:1;
                font-size:44px; padding:14px 26px 12px; background:#1B0B0D; border:3px solid #4A1C1F; border-radius:14px; }}
"""
JS = r"""
  const tl = gsap.timeline({ paused: true });
  const fadeIn = (s, t, d = 0.3) => tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: d, ease: "power2.out" }, t);
  const fadeOut = (s, t, d = 0.22) => tl.to(s, { opacity: 0, duration: d, ease: "power2.in" }, t);
  const popIn = (s, t, d = 0.34, sc = 0.3) => tl.fromTo(s, { opacity: 0, scale: sc }, { opacity: 1, scale: 1, duration: d, ease: "back.out(2.2)" }, t);
  const slam = (s, t, sc = 2.2) => tl.fromTo(s, { opacity: 0, scale: sc }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, t);
  const upIn = (s, t, d = 0.32, dy = 70) => tl.fromTo(s, { opacity: 0, y: dy }, { opacity: 1, y: 0, duration: d, ease: "power3.out" }, t);
  const leftIn = (s, t, d = 0.34, dx = -160, r = 0) => tl.fromTo(s, { opacity: 0, x: dx, rotation: r - 6 }, { opacity: 1, x: 0, rotation: r, duration: d, ease: "back.out(1.6)" }, t);
  const outUp = (s, t, d = 0.2) => tl.to(s, { opacity: 0, y: -60, duration: d, ease: "power2.in" }, t);
  const tap = (s, t, k = 1.08) => tl.fromTo(s, { scale: 1 }, { keyframes: [{ scale: 0.94, duration: 0.07 }, { scale: k, duration: 0.12 }, { scale: 1, duration: 0.18 }], ease: "power2.out", immediateRender: false }, t);
  const shake = (s, t, a = 16) => tl.fromTo(s, { x: 0, y: 0 }, { keyframes: [...Array(8)].map((_, i) => ({ x: (i % 2 ? a : -a) * (1 - i / 8), y: (i % 3 ? -a : a) * 0.5 * (1 - i / 8), duration: 0.035 })).concat([{ x: 0, y: 0, duration: 0.04 }]), immediateRender: false }, t);
  const flash = (s, t, a = 0.85) => tl.fromTo(s, { opacity: a }, { opacity: 0, duration: 0.32, ease: "power2.out", immediateRender: false }, t);
"""


def torn(amp=9, n=7):
    """clip-path: Papierstreifen mit gerissenen Enden links und rechts."""
    left = [f"{0 if i % 2 else amp}px {100 * i / n:.1f}%" for i in range(n + 1)]
    right = [f"calc(100% - {amp if i % 2 else 0}px) {100 * (n - i) / n:.1f}%" for i in range(n + 1)]
    return "polygon(" + ", ".join(left + right) + ")"


TORN = torn()


def strip(id_, x, y, text, fs, bg, fg, rot=0, pad=(10, 34, 6), extra="", hidden=True):
    return (f'<div id="{id_}" class="a" style="left:{x}px;top:{y}px;{"opacity:0;" if hidden else ""}transform-origin:20% 50%;{extra}">'
            f'<span class="strip" style="font-size:{fs}px;background:{bg};color:{fg};padding:{pad[0]}px {pad[1]}px {pad[2]}px;'
            f'clip-path:{TORN};transform:rotate({rot}deg)">{text}</span></div>')


def float3d(ids, dur):
    """Popups schweben dreidimensional: langsames Kippen um X- und Y-Achse mit Perspektive (deterministisch je Element)."""
    out = []
    for i, el in enumerate(ids):
        h = (sum(map(ord, el)) * 37 + i * 101) % 997 / 997
        player = bool(re.search(r"-(pl|st|p\d)$", el))
        ay, ax, d = (2.5 + 1.5 * h, 1.5 + 1 * (1 - h), 2.6 + 1.4 * h) if player else (5 + 3 * h, 3 + 2 * (1 - h), 2.2 + 1.4 * h)
        n = max(1, math.ceil(dur / d) + 1)
        out.append(f'tl.fromTo("#{el}", {{ rotationY: {-ay:.1f}, rotationX: {ax:.1f}, transformPerspective: 900 }}, '
                   f'{{ rotationY: {ay:.1f}, rotationX: {-ax:.1f}, duration: {d:.2f}, ease: "sine.inOut", yoyo: true, repeat: {n}, transformPerspective: 900 }}, 0);')
    return "\n  ".join(out)


def scene(cid, a, e, html, js, T=None, track=1, f3d=()):
    T = {k: round(v - a, 3) for k, v in (T or {}).items()}
    T["end"] = round(e - a, 3)
    js = js + "\n  " + float3d(f3d, e - a)
    src = (f'<template>\n  <style>{CSS}</style>\n  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">\n{html}\n  </div>\n'
           f'  <script>\n  const T = {json.dumps(T)};\n{JS}\n{js}\n  window.__timelines["{cid}"] = tl;\n  </script>\n</template>\n')
    open(f"{HERE}/compositions/{cid}.html", "w", encoding="utf-8").write(src)
    HOSTS.append((cid, a, e, track))


def move(t, x, y, d=0.45, ease="power2.inOut"):
    CUR.append(("move", t, x, y, d, ease))


def click(t, x=None, y=None, snd=True):
    CLICKS.append((t, x, y))
    if snd:
        SFX.append((t, "click", 0.9))


# ================================================================ Hintergrund: Schwarz/Dunkelrot mit wandernden roten Lichtwolken (wie Flyer)
def glow(id_, x, y, r, col):
    return f'<div id="{id_}" class="a" style="left:{x - r}px;top:{y - r}px;width:{2 * r}px;height:{2 * r}px;background:radial-gradient(circle, {col} 0%, transparent 68%);"></div>'


scene("bg", 0, END, f"""
  <div class="a" style="inset:0;background:linear-gradient(180deg,#0A0405 0%,#160507 55%,#0A0405 100%)"></div>
  {glow("bg-g1", 300, 700, 620, "rgba(170,18,24,.42)")}
  {glow("bg-g2", 820, 1250, 560, "rgba(140,12,18,.36)")}
  {glow("bg-g3", 700, 300, 420, "rgba(200,30,30,.18)")}
  {glow("bg-g4", 180, 1500, 460, "rgba(120,10,14,.30)")}""", f"""
  tl.fromTo("#bg-g1", {{ x: -80, y: 0, scale: 1 }}, {{ x: 120, y: 90, scale: 1.15, duration: {END}, ease: "sine.inOut" }}, 0);
  tl.fromTo("#bg-g2", {{ x: 0, y: 0 }}, {{ x: -200, y: -160, duration: {END}, ease: "sine.inOut" }}, 0);
  tl.fromTo("#bg-g3", {{ x: 0, y: 0, opacity: .6 }}, {{ x: -240, y: 120, opacity: 1, duration: {END}, ease: "sine.inOut" }}, 0);
  tl.fromTo("#bg-g4", {{ x: 0, y: 0 }}, {{ x: 260, y: -120, duration: {END}, ease: "sine.inOut" }}, 0);
""", track=0)

def group(pref, base, items, visible=False, start=0):
    """Die vier Spieler-Sticker als Gruppe (Reihenfolge = Malreihenfolge, hinten zuerst); base = Fußlinie in px."""
    out = ""
    for i, (n, x, hh) in enumerate(items, start):
        w, h = Image.open(f"{HERE}/assets/sticker_{n}.png").size
        out += (f'<div id="{pref}{i}" class="a" style="left:{x}px;top:{base - hh}px;width:{round(w * hh / h)}px;height:{hh}px;transform-origin:50% 100%;'
                f'{"" if visible else "opacity:0"}"><img src="assets/sticker_{n}.png" style="width:100%;height:100%"></div>')
    return out


from PIL import Image  # noqa: E402

# ================================================================ 1 Hook: HEIM / SPIEL / 02 FRANKENDERBY (Bild 0 ist schon fertig)
a, e = SEG["s1_hook"]
boxes = "".join(f'<span style="display:inline-block;width:62px;height:46px;margin-right:10px;border:3px solid #FFF;transform:skewX(-12deg);'
                f'font-size:28px;line-height:42px;text-align:center;font-weight:800;font-style:italic;'
                f'{"background:#FFF;color:" + RED if i == 2 else "color:#FFF;opacity:.75"}">0{i}</span>' for i in range(1, 6))
scene("s1", a, e, f"""
  <div id="s1-wedge" class="a" style="left:520px;top:0;width:560px;height:760px;background:{RED};clip-path:polygon(34% 0,100% 0,100% 100%,0 100%);"></div>
  <div id="s1-02" class="a big" style="left:670px;top:318px;font-size:230px;width:330px;text-align:right">02</div>
  <div id="s1-fd" class="a big" style="left:530px;top:540px;width:470px;text-align:right;font-size:58px;font-weight:800;letter-spacing:.06em">FRANKENDERBY</div>
  <div id="s1-hst" class="a" style="left:530px;top:606px;width:470px;text-align:right;font-size:30px;font-weight:600;letter-spacing:.2em">2. HEIMSPIELTAG</div>
  <div id="s1-box" class="a" style="left:650px;top:660px">{boxes}</div>
  <div id="s1-lbl" class="a lbl" style="left:90px;top:290px">Squash Bundesliga</div>
  <div id="s1-sai" class="a lbl" style="left:90px;top:335px;color:#FFF">Saison 2026/27</div>
  <div id="s1-heim" class="a big" style="left:70px;top:380px;font-size:270px">HEIM</div>
  <div id="s1-spiel" class="a big ol" style="left:96px;top:615px;font-size:270px">SPIEL</div>
  {group("s1-p", 1250, [("kandra", 600, 470), ("svec", 560, 320), ("clain", 360, 470), ("thuerauf", 20, 420)], visible=True)}
  <div id="s1-fl" class="a" style="inset:0;background:#FFF;opacity:0"></div>""", """
  tl.fromTo("#s1-heim", { scale: 1.06, x: -10 }, { scale: 1, x: 0, duration: 0.5, ease: "power3.out" }, 0);
  tl.fromTo("#s1-spiel", { x: 70 }, { x: 0, duration: 0.6, ease: "power3.out" }, 0);
  for (let i = 0; i < 4; i++) tl.fromTo(`#s1-p${i}`, { y: 24 + i * 6, scale: 0.98 }, { y: 0, scale: 1.03, duration: T.end, ease: "sine.out" }, 0);
  for (let i = 0; i < 4; i++) tl.fromTo(`#s1-p${i}`, { scaleY: 1 }, { keyframes: [{ scaleY: 0.95, duration: 0.08 }, { scaleY: 1.03, duration: 0.14 }, { scaleY: 1, duration: 0.18 }], immediateRender: false }, T.liga + i * 0.09);
  tl.fromTo("#s1-wedge", { x: 30 }, { x: 0, duration: 0.5, ease: "power3.out" }, 0);
  tap("#s1-box", T.click, 1.12);
  flash("#s1-fl", 0.05, 0.25);
  tl.to(["#s1-heim", "#s1-spiel", "#s1-lbl", "#s1-sai", "#s1-p3", "#s1-p2"], { x: -140, opacity: 0, duration: 0.22, ease: "power2.in", stagger: 0.03 }, T.end - 0.26);
  tl.to(["#s1-wedge", "#s1-02", "#s1-fd", "#s1-hst", "#s1-box", "#s1-p1", "#s1-p0"], { x: 160, opacity: 0, duration: 0.22, ease: "power2.in", stagger: 0.02 }, T.end - 0.26);
""", {"liga": W("Squash-Bundesliga!"), "click": 1.75}, f3d=["s1-02", "s1-box", "s1-p0", "s1-p1", "s1-p2", "s1-p3"])
CUR.append(("set", 0, 980, 1420, 0, ""))
CUR.append(("show", 0.5, 0, 0, 0, ""))
move(0.55, 752, 690, 0.9, "power2.out")
click(1.75, 752, 690)
SFX += [(0.05, "pop", 0.5)]

# ================================================================ 2 Duell: SCF-Logo vs. Heuchelhof-Logo
a, e = SEG["s2_duell"]
scene("s2", a, e, f"""
  <div id="s2-lbl" class="a lbl c" style="top:330px;font-size:38px">Live im Sportpark Nord</div>
  <div id="s2-band" class="a" style="left:-200px;top:690px;width:1480px;height:150px;background:linear-gradient(90deg,transparent,{RED} 30%,{RED} 70%,transparent);transform:rotate(-8deg);opacity:0"></div>
  <div id="s2-l1" class="a" style="left:95px;top:600px;width:320px;height:320px;border-radius:50%;box-shadow:0 20px 60px rgba(0,0,0,.7)"><img src="assets/logo_scf.png" style="width:100%;height:100%"></div>
  <div id="s2-l2" class="a" style="left:665px;top:600px;width:320px;height:320px;border-radius:50%;box-shadow:0 20px 60px rgba(0,0,0,.7)"><img src="assets/logo_tsc.png" style="width:100%;height:100%"></div>
  <div id="s2-vs" class="a big c" style="top:690px;font-size:170px;color:#FFF;text-shadow:0 8px 30px rgba(0,0,0,.8)">VS.</div>
  <div id="s2-n1" class="a big" style="left:55px;top:975px;width:400px;text-align:center;font-size:66px">SCF NÜRNBERG</div>
  <div id="s2-n2" class="a big" style="left:625px;top:975px;width:400px;text-align:center;font-size:66px">TSC HEUCHELHOF</div>
  <div id="s2-h1" class="a lbl" style="left:55px;top:1055px;width:400px;text-align:center;font-size:30px;color:#FFF;opacity:.7">Heim</div>
  <div id="s2-h2" class="a lbl" style="left:625px;top:1055px;width:400px;text-align:center;font-size:30px;color:#FFF;opacity:.7">Gast · Würzburg</div>""", """
  fadeIn("#s2-lbl", 0.0, 0.3);
  tl.fromTo("#s2-l1", { opacity: 0, x: -420, rotation: -140 }, { opacity: 1, x: 0, rotation: 0, duration: 0.5, ease: "back.out(1.4)" }, T.scf);
  upIn("#s2-n1", T.scf + 0.25); fadeIn("#s2-h1", T.scf + 0.4);
  tl.fromTo("#s2-band", { opacity: 0, scaleX: 0.2 }, { opacity: 0.9, scaleX: 1, duration: 0.35, ease: "power3.out" }, T.vs - 0.05);
  slam("#s2-vs", T.vs, 2.6);
  tl.fromTo("#s2-l2", { opacity: 0, x: 420, rotation: 140 }, { opacity: 1, x: 0, rotation: 0, duration: 0.5, ease: "back.out(1.4)" }, T.tsc);
  upIn("#s2-n2", T.tsc + 0.25); fadeIn("#s2-h2", T.tsc + 0.4);
  tl.fromTo("#s2-l1", { x: 0 }, { keyframes: [{ x: 24, duration: 0.08 }, { x: 0, duration: 0.25 }], immediateRender: false }, T.tsc + 0.42);
  tl.fromTo("#s2-l2", { x: 0 }, { keyframes: [{ x: -24, duration: 0.08 }, { x: 0, duration: 0.25 }], immediateRender: false }, T.tsc + 0.42);
  shake("#s2-vs", T.tsc + 0.42, 10);
  tap("#s2-l1", T.c1, 1.07);
  tl.to(["#s2-l1", "#s2-n1", "#s2-h1"], { x: -300, opacity: 0, duration: 0.24, ease: "power2.in" }, T.end - 0.28);
  tl.to(["#s2-l2", "#s2-n2", "#s2-h2"], { x: 300, opacity: 0, duration: 0.24, ease: "power2.in" }, T.end - 0.28);
  tl.to(["#s2-vs", "#s2-band", "#s2-lbl"], { scale: 0.6, opacity: 0, duration: 0.22, ease: "power2.in" }, T.end - 0.26);
""", {"scf": W("SCF") - 0.05, "vs": W("empfängt"), "tsc": W("TSC") - 0.1, "c1": W("Nürnberg") + 0.15}, f3d=["s2-l1", "s2-l2", "s2-vs", "s2-n1", "s2-n2"])
SFX += [(W("SCF"), "pop", 0.8), (W("empfängt"), "pop", 0.6), (W("TSC") + 0.32, "pop", 0.8)]
move(W("SCF") + 0.25, 320, 830, 0.5)
click(W("Nürnberg") + 0.15, 320, 830)
move(W("Nürnberg") + 0.55, 470, 900, 0.6, "sine.inOut")
move(W("TSC") + 0.55, 860, 840, 0.5)

# ================================================================ 3 Line-up: „UNSER TEAM“ + Button
a, e = SEG["s3_lineup"]
BTN_Y = 950
scene("s3", a, e, f"""
  <div id="s3-lbl" class="a lbl c" style="top:385px">Saison 2026/27 · 2. Heimspieltag</div>
  <div id="s3-u" class="a big c" style="top:440px;font-size:200px">UNSER</div>
  <div id="s3-t" class="a big c ol" style="top:615px;font-size:280px">TEAM</div>
  <div id="s3-btn" class="a" style="left:270px;top:{BTN_Y}px;width:540px;height:112px;border-radius:56px;background:#FFF;color:{RED};
       display:flex;align-items:center;justify-content:center;gap:18px;font-weight:900;font-style:italic;font-size:54px;letter-spacing:.02em;
       box-shadow:0 18px 40px rgba(0,0,0,.55)">LINE-UP ANSEHEN <span style="font-style:normal;font-size:40px">▶</span></div>
  <div id="s3-wipe" class="a" style="left:-400px;top:-200px;width:1900px;height:2400px;background:{RED};transform:skewX(-14deg) translateX(-2200px)"></div>""", """
  fadeIn("#s3-lbl", 0.05, 0.3);
  upIn("#s3-u", 0.08, 0.32, 90);
  tl.fromTo("#s3-t", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }, T.team);
  popIn("#s3-btn", T.team + 0.3, 0.4, 0.5);
  tap("#s3-btn", T.click, 1.06);
  tl.to("#s3-btn", { backgroundColor: "#E3241B", color: "#FFFFFF", duration: 0.1 }, T.click + 0.05);
  tl.fromTo("#s3-wipe", { x: 0 }, { x: 2400, duration: 0.42, ease: "power2.in", immediateRender: false }, T.end - 0.42);
""", {"team": W("Team"), "click": W("Heimspieltag:", end=True) + 0.12}, f3d=["s3-u", "s3-t", "s3-btn"])
move(W("Team") + 0.4, 742, BTN_Y + 62, 0.6)
click(W("Heimspieltag:", end=True) + 0.12, 742, BTN_Y + 62)
SFX += [(W("Team") + 0.3, "pop", 0.6)]

# ================================================================ 4–7 Spieler als Papier-Ausschnitte mit Namensstreifen
PLAYERS = [("s4_thuerauf", "thuerauf", "Johannes", "Thürauf", -12), ("s5_clain", "clain", "Edwin", "Clain", 10),
           ("s6_kandra", "kandra", "David", "Kandra", -10), ("s7_svec", "svec", "Martin", "Svec", 12)]
from PIL import Image  # noqa: E402
for k, (sid, img, first, last, rot) in enumerate(PLAYERS):
    a, e = SEG[sid]
    w, h = Image.open(f"{HERE}/assets/sticker_{img}.png").size
    H = 900
    Wd = round(w * H / h)
    if Wd > 1000:  # breite Pose (Svec): auf Bildbreite begrenzen
        Wd = 1000; H = round(h * Wd / w)
    x0 = max(40, 560 - Wd // 2 + (40 if img == "thuerauf" else 0))
    cid = f"p{k + 1}"
    LFS = 132
    lw = len(last) * LFS * 0.5 + 68
    scene(cid, a, e, f"""
  <div id="{cid}-band" class="a" style="left:-260px;top:520px;width:1600px;height:560px;background:linear-gradient(90deg,#8E0E13,{RED} 50%,#8E0E13);transform:rotate({rot}deg)"></div>
  <div id="{cid}-ghost" class="a big ol" data-layout-ignore style="left:-40px;top:250px;font-size:360px;-webkit-text-stroke:4px rgba(255,255,255,.28)">{last.upper()}</div>
  <div id="{cid}-num" class="a big" style="left:760px;top:310px;font-size:150px;color:transparent;-webkit-text-stroke:4px {RED}">0{k + 1}</div>
  <div id="{cid}-pl" class="a" style="left:{x0}px;top:{1190 - H}px;width:{Wd}px;height:{H}px;transform-origin:50% 100%"><img src="assets/sticker_{img}.png" style="width:100%;height:100%"></div>
  <div id="{cid}-tag" class="a" style="left:96px;top:930px;font-size:30px;font-weight:800;letter-spacing:.2em;padding:6px 14px;background:#111;color:#FFF;opacity:0">SPIELER 0{k + 1} / 04</div>
  {strip(cid + "-fn", 90, 980, first.upper(), 64, RED, "#FFF", -3)}
  {strip(cid + "-ln", 90, 1058, last.upper(), LFS, PAPER, "#111", -2, (8, 34, 2))}
  <div id="{cid}-fl" class="a" style="inset:0;background:#FFF;opacity:0"></div>""", """
  tl.fromTo("#CID-band", { x: DIR * 1700 }, { x: 0, duration: 0.26, ease: "power3.out" }, 0);
  tl.fromTo("#CID-ghost", { x: 160, opacity: 0 }, { x: -220, opacity: 1, duration: T.end, ease: "none" }, 0);
  tl.fromTo("#CID-num", { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }, 0.1);
  tl.fromTo("#CID-pl", { opacity: 0, y: 160, scale: 0.86, rotation: -DIR * 5 }, { opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.42, ease: "back.out(1.5)" }, T.inn);
  tl.fromTo("#CID-pl", { x: 0 }, { x: DIR * -26, duration: T.end - T.inn - 0.4, ease: "sine.inOut", immediateRender: false }, T.inn + 0.42);
  flash("#CID-fl", T.inn + 0.02, 0.8);
  fadeIn("#CID-tag", T.inn + 0.12, 0.2);
  leftIn("#CID-fn", T.inn + 0.16);
  leftIn("#CID-ln", T.inn + 0.26, 0.38, -220);
  tap("#CID-ln", T.click, 1.07);
  tl.to(["#CID-pl", "#CID-fn", "#CID-ln", "#CID-tag", "#CID-num", "#CID-ghost"], { x: DIR * -600, opacity: 0, duration: 0.2, ease: "power2.in", stagger: 0.015 }, T.end - 0.22);
  tl.to("#CID-band", { x: DIR * -1700, duration: 0.24, ease: "power2.in" }, T.end - 0.24);
""".replace("CID", cid).replace("DIR", "(1)" if k % 2 == 0 else "(-1)"), {"inn": a + 0.05, "click": a + 0.75},
          f3d=[f"{cid}-pl", f"{cid}-fn", f"{cid}-ln", f"{cid}-tag", f"{cid}-num"])
    SFX += [(a + 0.06, "shutter", 0.9), (a + 0.3, "pop", 0.45)]
    move(a + 0.25, 90 + lw - 18, 1178, 0.45)
    click(a + 0.75, 90 + lw - 18, 1178)

# ================================================================ 8 Gegner: Heuchelhof, Steinmann (WRL 21), Ziel Playoffs
a, e = SEG["s8_gegner"]
sw, sh = Image.open(f"{HERE}/assets/sticker_steinmann.png").size
STW = 860; STH = round(sh * STW / sw)
BADGE = (865, 470)  # Mittelpunkt WRL-Badge
scene("s8", a, e, f"""
  <div id="s8-band" class="a" style="left:-260px;top:560px;width:1600px;height:520px;background:linear-gradient(90deg,#3A0A0D,#7A1015 50%,#3A0A0D);transform:rotate(-10deg);opacity:0"></div>
  <div id="s8-ghost" class="a big ol" data-layout-ignore style="left:-30px;top:560px;font-size:300px;-webkit-text-stroke:4px rgba(255,255,255,.22);opacity:0">STEINMANN</div>
  <div id="s8-lbl" class="a lbl" style="left:100px;top:290px">Der Gegner</div>
  <div id="s8-logo" class="a" style="left:96px;top:340px;width:240px;height:240px;border-radius:50%;box-shadow:0 16px 40px rgba(0,0,0,.6);transform-origin:0 0"><img src="assets/logo_tsc.png" style="width:100%;height:100%"></div>
  <div id="s8-t1" class="a big" style="left:370px;top:365px;font-size:110px">TSC</div>
  <div id="s8-t2" class="a big" style="left:370px;top:465px;font-size:110px">HEUCHELHOF</div>
  <div id="s8-sub" class="a" style="left:100px;top:612px;font-size:32px;font-weight:600;letter-spacing:.12em;color:#FFF;opacity:0">TABELLENDRITTER DER VORSAISON · WÜRZBURG</div>
  <div id="s8-nach" class="a" style="left:100px;top:675px;opacity:0">{strip("s8-nach-s", 0, 0, "HAT NACHGELEGT", 56, RED, "#FFF", -2, hidden=False)}</div>
  <div id="s8-st" class="a" style="left:110px;top:{1200 - STH}px;width:{STW}px;height:{STH}px;transform-origin:50% 100%;opacity:0"><img src="assets/sticker_steinmann.png" style="width:100%;height:100%"></div>
  <div id="s8-badge" class="a" style="left:{BADGE[0] - 105}px;top:{BADGE[1] - 105}px;width:210px;height:210px;border-radius:50%;background:{RED};border:7px solid #FFF;
       box-shadow:0 18px 40px rgba(0,0,0,.6);opacity:0">
    <div class="a c" style="left:0;width:196px;top:30px;font-size:30px;font-weight:800;letter-spacing:.2em;text-align:center">WRL</div>
    <div id="s8-num" class="a big" style="left:0;width:196px;top:62px;font-size:120px;text-align:center">21</div></div>
  <div id="s8-tip" class="a" style="left:470px;top:{BADGE[1] - 30}px;padding:12px 20px;background:#FFF;color:#111;border-radius:12px;font-size:32px;font-weight:800;
       letter-spacing:.04em;white-space:nowrap;opacity:0;box-shadow:0 10px 24px rgba(0,0,0,.5)">NR. 21 DER WELT</div>
  <div id="s8-tag" class="a" style="left:96px;top:955px;font-size:30px;font-weight:800;letter-spacing:.2em;padding:6px 14px;background:#111;color:#FFF;opacity:0">NEUZUGANG · TSC HEUCHELHOF</div>
  {strip("s8-fn", 90, 1005, "DIMITRI", 64, RED, "#FFF", -3)}
  {strip("s8-ln", 90, 1083, "STEINMANN", 116, PAPER, "#111", -2, (8, 34, 2))}
  <div id="s8-stamp" class="a" style="left:300px;top:370px;transform-origin:50% 50%;opacity:0">
    <div style="transform:rotate(-7deg);border:7px solid {RED};color:{RED};padding:10px 26px 6px;font-weight:900;font-style:italic;font-size:76px;line-height:1;
         background:rgba(11,5,6,.88);white-space:nowrap">ZIEL: PLAYOFFS?</div></div>
  <div id="s8-fl" class="a" style="inset:0;background:#FFF;opacity:0"></div>""", """
  fadeIn("#s8-lbl", 0.0, 0.25);
  popIn("#s8-logo", 0.05, 0.42, 0.2);
  leftIn("#s8-t1", 0.12); leftIn("#s8-t2", 0.2);
  fadeIn("#s8-sub", 0.45, 0.4);
  leftIn("#s8-nach", T.nach, 0.34, -160, 0);
  // Neuzugang: Titel weg, Logo klein in die Ecke, Steinmann als Papier-Ausschnitt mit Blitz
  tl.to(["#s8-t1", "#s8-t2", "#s8-sub", "#s8-nach"], { opacity: 0, x: -80, duration: 0.2, ease: "power2.in", stagger: 0.03 }, T.neu - 0.15);
  tl.to("#s8-logo", { scale: 0.5, duration: 0.3, ease: "power3.inOut" }, T.neu - 0.1);
  tl.fromTo("#s8-band", { opacity: 1, x: 1700 }, { opacity: 1, x: 0, duration: 0.28, ease: "power3.out" }, T.neu);
  tl.fromTo("#s8-ghost", { x: 160, opacity: 0 }, { x: -200, opacity: 1, duration: T.end - T.neu, ease: "none" }, T.neu);
  tl.fromTo("#s8-st", { opacity: 0, y: 160, scale: 0.86, rotation: 5 }, { opacity: 1, y: 0, scale: 1, rotation: 0, duration: 0.42, ease: "back.out(1.5)" }, T.neu + 0.05);
  flash("#s8-fl", T.neu + 0.07, 0.8);
  fadeIn("#s8-tag", T.neu + 0.2, 0.2);
  leftIn("#s8-fn", T.dim, 0.34);
  leftIn("#s8-ln", T.stein, 0.38, -220);
  popIn("#s8-badge", T.stein + 0.25, 0.4, 0.2);
  popIn("#s8-tip", T.hover, 0.3, 0.5);
  tl.fromTo("#s8-num", { scale: 1 }, { keyframes: [{ scale: 1.3, duration: 0.12 }, { scale: 1, duration: 0.3 }], immediateRender: false }, T.n21);
  tl.to("#s8-tip", { opacity: 0, duration: 0.2 }, T.ziel - 0.3);
  tl.fromTo("#s8-stamp", { opacity: 0, scale: 2.4, rotation: -10 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.22, ease: "power4.in" }, T.ziel + 0.1);
  shake("#s8-st", T.ziel + 0.32, 8);
  tl.to(["#s8-lbl", "#s8-logo", "#s8-st", "#s8-badge", "#s8-tag", "#s8-fn", "#s8-ln", "#s8-stamp", "#s8-ghost"], { y: -80, opacity: 0, duration: 0.22, ease: "power2.in", stagger: 0.015 }, T.end - 0.3);
  tl.to("#s8-band", { x: -1700, duration: 0.24, ease: "power2.in" }, T.end - 0.26);
""", {"nach": W("nachgelegt:") - 0.05, "neu": W("Neuzugang") - 0.05, "dim": W("Dimitri") - 0.05, "stein": W("Steinmann") - 0.05,
      "hover": W("21") - 0.35, "n21": W("21"), "ziel": W("Ziel:")},
      f3d=["s8-logo", "s8-st", "s8-badge", "s8-tip", "s8-tag", "s8-fn", "s8-ln", "s8-stamp", "s8-nach"])
num_t = W("21")
SFX += [(a + 0.05, "pop", 0.6), (W("nachgelegt:"), "pop", 0.5), (W("Neuzugang"), "shutter", 0.9), (W("Steinmann") + 0.2, "pop", 0.5),
        (W("Ziel:") + 0.3, "boom", 0.35)]
move(W("Neuzugang") + 0.4, 700, 1010, 0.5)
move(W("Steinmann") + 0.25, BADGE[0] - 20, BADGE[1] + 40, 0.45)
click(num_t, BADGE[0] - 20, BADGE[1] + 40)
move(W("Ziel:") + 0.45, 640, 450, 0.4)

# ================================================================ 9 Ansage: 4:0
a, e = SEG["s9_score"]
CX, CY = 540, 735
scene("s9", a, e, f"""
  <div id="s9-l1" class="a big c" style="top:300px;font-size:104px">LETZTES DUELL</div>
  <div id="s9-l2" class="a lbl c" style="top:405px;font-size:40px">im Sportpark Nord</div>
  <div id="s9-score" class="a big c" style="top:505px;font-size:470px;text-shadow:0 20px 60px rgba(0,0,0,.6)">4:0</div>
  <svg id="s9-ring" class="a" style="left:0;top:0;overflow:visible" width="1080" height="1920" viewBox="0 0 1080 1920">
    <path id="s9-path" d="" fill="none" stroke="{RED}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <div id="s9-fu" class="a" style="left:0;width:1080px;top:975px;opacity:0;text-align:center">{strip("s9-fu-s", 0, 0, "FÜR UNS.", 110, RED, "#FFF", -3, (8, 40, 2), "position:relative;display:inline-block", hidden=False)}</div>
  <div id="s9-fl" class="a" style="inset:0;background:{RED};opacity:0"></div>""", """
  fadeIn("#s9-l1", 0.0, 0.3); fadeIn("#s9-l2", 0.2, 0.3);
  tl.set("#s9-score", { opacity: 0 }, 0);
  slam("#s9-score", T.four, 2.8);
  flash("#s9-fl", T.four + 0.2, 0.55);
  shake("#s9-score", T.four + 0.2, 22);
  const p = document.getElementById("s9-path"); p.setAttribute("d", RING);
  const L = p.getTotalLength();
  tl.set(p, { strokeDasharray: L, strokeDashoffset: L }, 0);
  tl.to(p, { strokeDashoffset: 0, duration: T.ringd, ease: "power1.inOut" }, T.ring);
  tl.fromTo("#s9-fu", { opacity: 0, scale: 0.4, rotation: -8 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.3, ease: "back.out(2.4)" }, T.fu);
  tl.to(["#s9-l1", "#s9-l2", "#s9-score", "#s9-ring", "#s9-fu"], { scale: 0.7, opacity: 0, duration: 0.22, ease: "power2.in", stagger: 0.02 }, T.end - 0.28);
""".replace("RING", "RINGD"), {"four": W("4") - 0.05, "ring": W("4") + 0.35, "fu": W("für", after=W("4")) - 0.05}, f3d=["s9-l1", "s9-score", "s9-fu"])
# Handgezeichneter Kreis, dem der Mauszeiger folgt (gleiche Punkte für Pfad und Zeiger)
pts = []
R0, R1, ROT = (380, 250), (400, 270), math.radians(-6)
for i in range(49):
    th = -math.pi * 0.6 + 2 * math.pi * 1.12 * i / 48
    f = i / 48
    rx, ry = R0[0] + (R1[0] - R0[0]) * f, R0[1] + (R1[1] - R0[1]) * f
    x, y = rx * math.cos(th), ry * math.sin(th)
    pts.append((CX + x * math.cos(ROT) - y * math.sin(ROT), CY + x * math.sin(ROT) + y * math.cos(ROT)))
ring_d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
src = open(f"{HERE}/compositions/s9.html").read().replace("RINGD", json.dumps(ring_d)).replace('"ringd"', '"ringd"')
t_ring, d_ring = W("4") + 0.35, 0.75
src = src.replace("T.ringd", f"{d_ring}")
open(f"{HERE}/compositions/s9.html", "w").write(src)
SFX += [(W("4") - 0.02, "boom", 0.8), (W("für", after=W("4")), "pop", 0.6)]
move(t_ring - 0.35, *pts[0], 0.3)
CUR.append(("path", t_ring, pts, d_ring, 0, ""))
move(t_ring + d_ring + 0.3, 880, 1300, 0.5, "sine.inOut")

# ================================================================ 10 Termin: Kalenderblatt, 13:00, Einlass, Eintritt frei
a, e = SEG["s10_termin"]
scene("s10", a, e, f"""
  <div id="s10-lbl" class="a lbl c" style="top:290px">Squash Bundesliga · Live</div>
  <div id="s10-cal" class="a" style="left:250px;top:345px;width:580px;height:530px;background:{PAPER};border-radius:26px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.65);opacity:0">
    <div id="s10-head" class="a big c" style="left:0;width:580px;top:0;height:130px;background:{RED};font-size:84px;line-height:138px">SAMSTAG</div>
    <div id="s10-d" class="a big" style="left:0;width:580px;text-align:center;top:142px;font-size:280px;color:#111;opacity:0">28</div>
    <div id="s10-m" class="a big" style="left:0;width:580px;text-align:center;top:410px;font-size:66px;color:{RED};opacity:0">NOVEMBER 2026</div>
  </div>
  <div id="s10-ok" class="a" style="left:740px;top:300px;width:130px;height:130px;border-radius:50%;background:#1DB954;border:6px solid #FFF;color:#FFF;font-size:78px;
       font-weight:900;display:flex;align-items:center;justify-content:center;opacity:0;box-shadow:0 12px 30px rgba(0,0,0,.5)">✓</div>
  <div id="s10-time" class="a" style="left:150px;top:900px;width:780px;height:120px;background:{RED};transform:skewX(-10deg);opacity:0;box-shadow:0 18px 40px rgba(0,0,0,.5)">
    <div class="big" style="transform:skewX(10deg);text-align:center;font-size:110px;line-height:126px">13:00 UHR</div></div>
  <div id="s10-c1" class="a" style="left:120px;top:1038px;opacity:0"><span class="chip">Einlass 12:00</span></div>
  <div id="s10-c2" class="a" style="left:560px;top:1038px;opacity:0"><span class="chip" style="background:#FFF;color:{RED};border-color:#FFF">Eintritt frei</span></div>""", """
  fadeIn("#s10-lbl", 0.0, 0.3);
  tl.fromTo("#s10-cal", { opacity: 0, y: 120, rotation: -4 }, { opacity: 1, y: 0, rotation: 0, duration: 0.42, ease: "back.out(1.6)" }, T.sa - 0.1);
  tl.fromTo("#s10-d", { opacity: 0, rotationX: -90, transformPerspective: 900 }, { opacity: 1, rotationX: 0, duration: 0.4, ease: "back.out(1.8)" }, T.d);
  upIn("#s10-m", T.m, 0.3, 40);
  tl.fromTo("#s10-time", { opacity: 0, x: -900 }, { opacity: 1, x: 0, duration: 0.36, ease: "power3.out" }, T.t);
  popIn("#s10-c1", T.c1); popIn("#s10-c2", T.c2);
  tap("#s10-cal", T.click, 1.04);
  popIn("#s10-ok", T.click + 0.1, 0.4, 0.2);
  tl.to(["#s10-lbl", "#s10-cal", "#s10-ok", "#s10-time", "#s10-c1", "#s10-c2"], { y: -90, opacity: 0, duration: 0.22, ease: "power2.in", stagger: 0.02 }, T.end - 0.3);
""", {"sa": W("Samstag,"), "d": W("28."), "m": W("November,"), "t": W("13") - 0.05, "c1": W("Einlass"), "c2": W("Eintritt"),
      "click": W("frei.") + 0.1}, f3d=["s10-cal", "s10-ok", "s10-c1", "s10-c2"])
SFX += [(W("Samstag,"), "pop", 0.6), (W("28."), "pop", 0.6), (W("13"), "pop", 0.6), (W("Einlass"), "pop", 0.5), (W("Eintritt"), "pop", 0.5),
        (W("frei.") + 0.2, "marimba", 0.35)]
move(W("13") + 0.2, 640, 700, 0.6)
move(W("Einlass") + 0.1, 600, 640, 0.5, "sine.inOut")
click(W("frei.") + 0.1, 600, 640)

# ================================================================ 11 Schluss: alle vier + Logos, „Seid live dabei“, Unterstützung, Termin, Schluss
a, e = SEG["s11_cta"]
G11 = [("kandra", 590, 540), ("svec", 560, 330), ("clain", 335, 540), ("thuerauf", 0, 480)]
DAB_Y = 900
HOP = [W("unterstützt") + 0.05 + k * 0.24 for k in range(4)]
scene("s11", a, e, f"""
  <div id="s11-l1" class="a" style="left:205px;top:290px;width:190px;height:190px;border-radius:50%;box-shadow:0 14px 36px rgba(0,0,0,.6);opacity:0"><img src="assets/logo_scf.png" style="width:100%;height:100%"></div>
  <div id="s11-vs" class="a big c" style="top:345px;font-size:96px;opacity:0">VS.</div>
  <div id="s11-l2" class="a" style="left:685px;top:290px;width:190px;height:190px;border-radius:50%;box-shadow:0 14px 36px rgba(0,0,0,.6);opacity:0"><img src="assets/logo_tsc.png" style="width:100%;height:100%"></div>
  <div id="s11-band" class="a" style="left:-200px;top:700px;width:1480px;height:330px;background:linear-gradient(90deg,#8E0E13,{RED} 50%,#8E0E13);transform:rotate(-7deg);opacity:0"></div>
  {group("s11-p", 1040, G11[:1]) + group("s11-p", 1075, G11[1:2], start=1) + group("s11-p", 1040, G11[2:], start=2)}
  <div id="s11-shade" class="a" style="left:0;top:720px;width:1080px;height:440px;background:linear-gradient(180deg,transparent,rgba(10,4,5,.92) 50%);opacity:0"></div>
  <div id="s11-m1" class="a big c" style="top:790px;font-size:120px;opacity:0">SEID LIVE</div>
  <div id="s11-m2" class="a big c" style="top:880px;font-size:190px;color:{RED};opacity:0;text-shadow:0 10px 30px rgba(0,0,0,.6)">DABEI!</div>
  <div id="s11-hs" class="a" style="left:0;width:1080px;top:905px;text-align:center;opacity:0">{strip("s11-hs-s", 0, 0, "2. HEIMSPIELTAG", 92, PAPER, "#111", -2, (8, 36, 2), "position:relative;display:inline-block", hidden=False)}</div>
  <div id="s11-btn" class="a" style="left:270px;top:{DAB_Y}px;width:540px;height:112px;border-radius:56px;background:#FFF;color:{RED};display:flex;align-items:center;justify-content:center;
       gap:16px;font-weight:900;font-style:italic;font-size:56px;box-shadow:0 18px 40px rgba(0,0,0,.55);opacity:0"><span id="s11-bt">ICH BIN DABEI</span><span id="s11-ck" style="font-style:normal;opacity:0">✓</span></div>
  <div id="s11-bar" class="a" style="left:110px;top:1032px;width:860px;height:96px;background:{RED};transform:skewX(-10deg);opacity:0">
    <div class="big" style="transform:skewX(10deg);text-align:center;font-size:74px;line-height:100px">SA 28.11. <span style="opacity:.6">|</span> 13:00 UHR</div></div>
  <div id="s11-adr" class="a c" style="top:1146px;font-size:32px;font-weight:600;letter-spacing:.06em;opacity:0">Sportpark Nord · Andernacher Str. 15 · 90411 Nürnberg</div>
  {"".join(f'<div id="s11-cf{i}" class="a" style="left:540px;top:{DAB_Y + 56}px;width:{14 + (i % 3) * 6}px;height:{10 + (i % 2) * 8}px;background:{RED if i % 2 else "#FFF"};opacity:0"></div>' for i in range(18))}""", """
  popIn("#s11-l1", 0.0, 0.4, 0.2); popIn("#s11-vs", 0.15, 0.3, 2); popIn("#s11-l2", 0.22, 0.4, 0.2);
  tl.fromTo("#s11-band", { opacity: 0, scaleX: 0.1 }, { opacity: 1, scaleX: 1, duration: 0.4, ease: "power3.out" }, 0.1);
  for (let i = 0; i < 4; i++) tl.fromTo(`#s11-p${i}`, { opacity: 0, y: 200, rotation: (i % 2 ? 6 : -6) }, { opacity: 1, y: 0, rotation: 0, duration: 0.45, ease: "back.out(1.5)" }, 0.25 + i * 0.12);
  fadeIn("#s11-shade", T.seid - 0.1, 0.3);
  upIn("#s11-m1", T.seid, 0.3, 50);
  slam("#s11-m2", T.dabei, 2.4);
  shake("#s11-m2", T.dabei + 0.2, 12);
  tl.to(["#s11-m1", "#s11-m2"], { opacity: 0, y: -40, duration: 0.22, ease: "power2.in" }, T.hop0 - 0.25);
  tl.to("#s11-shade", { opacity: 0.55, duration: 0.3 }, T.hop0 - 0.2);
  // „unterstützt unsere Spieler“: der Mauszeiger tippt jeden Spieler an, der Spieler hüpft
  const hop = [T.hop0, T.hop1, T.hop2, T.hop3], order = [3, 2, 0, 1];
  for (let k = 0; k < 4; k++) tl.fromTo(`#s11-p${order[k]}`, { y: 0 }, { keyframes: [{ y: -46, scaleY: 1.04, duration: 0.14, ease: "power2.out" }, { y: 0, scaleY: 1, duration: 0.2, ease: "bounce.out" }], immediateRender: false }, hop[k] + 0.04);
  tl.fromTo("#s11-hs", { opacity: 0, scale: 0.4, rotation: -8 }, { opacity: 1, scale: 1, rotation: 0, duration: 0.3, ease: "back.out(2.4)" }, T.hst);
  tl.to("#s11-hs", { opacity: 0, y: -40, duration: 0.22, ease: "power2.in" }, T.btn - 0.25);
  popIn("#s11-btn", T.btn, 0.4, 0.4);
  tl.fromTo("#s11-bar", { opacity: 0, x: -900 }, { opacity: 1, x: 0, duration: 0.36, ease: "power3.out" }, T.btn + 0.2);
  fadeIn("#s11-adr", T.adr, 0.4);
  tap("#s11-btn", T.click, 1.08);
  tl.to("#s11-btn", { backgroundColor: "#E3241B", color: "#FFFFFF", duration: 0.12 }, T.click + 0.05);
  tl.to("#s11-ck", { opacity: 1, duration: 0.1 }, T.click + 0.05);
  for (let i = 0; i < 18; i++) {
    const ang = (i / 18) * Math.PI * 2 + 0.3, r = 220 + (i % 4) * 60;
    tl.fromTo(`#s11-cf${i}`, { opacity: 1, x: 0, y: 0, rotation: 0 }, { opacity: 0, x: Math.cos(ang) * r, y: Math.sin(ang) * r * 0.7 + 60, rotation: 200 + i * 40, duration: 0.9, ease: "power2.out", immediateRender: false }, T.click + 0.05);
  }
  // Schluss: alle winken kurz mit einem Hüpfer
  for (let i = 0; i < 4; i++) tl.fromTo(`#s11-p${i}`, { y: 0, rotation: 0 }, { keyframes: [{ y: -30, rotation: (i % 2 ? 4 : -4), duration: 0.16 }, { y: 0, rotation: 0, duration: 0.3, ease: "bounce.out" }], immediateRender: false }, T.ciao + i * 0.06);
  tap("#s11-l1", T.ciao + 0.1, 1.1); tap("#s11-l2", T.ciao + 0.2, 1.1);
""", {"seid": W("seid"), "dabei": W("dabei"), "hop0": HOP[0], "hop1": HOP[1], "hop2": HOP[2], "hop3": HOP[3], "hst": W("zweiten", after=a),
      "btn": W("Wir"), "click": W("euch,", end=True) + 0.05, "adr": W("euer"), "ciao": W("Nord.", after=W("euer"), end=True) + 0.35},
      f3d=["s11-l1", "s11-l2", "s11-vs", "s11-p0", "s11-p1", "s11-p2", "s11-p3", "s11-m1", "s11-m2", "s11-hs", "s11-btn", "s11-adr"])
# Sticker-Köpfe (ungefähr), in der Reihenfolge Thürauf, Clain, Kandra, Svec
HEADS = [(265, 600), (499, 555), (790, 545), (800, 770)]
SFX += [(a + 0.02, "pop", 0.6), (a + 0.3, "shutter", 0.6), (W("dabei"), "pop", 0.8)]
move(W("Nord,", after=a) + 0.1, 700, 1150, 0.6, "sine.inOut")
for k, (hx, hy) in enumerate(HEADS):
    move(HOP[k] - 0.2, min(hx, 900), hy, 0.2, "power2.out")
    click(HOP[k], min(hx, 900), hy, snd=False)
SFX += [(W("zweiten", after=a), "pop", 0.5), (W("Wir"), "pop", 0.5)]
move(W("Wir") + 0.15, 610, DAB_Y + 70, 0.5)
click(W("euch,", end=True) + 0.05, 610, DAB_Y + 70, snd=True)
move(W("euer") + 0.2, 720, 1180, 0.5, "sine.inOut")
CUR.append(("wave", W("Nord.", after=W("euer"), end=True) + 0.35, 0, 0, 0, ""))

# ================================================================ Übergänge: kurzer roter Schrägwisch an Szenengrenzen
cuts = [SEG["s2_duell"][0], SEG["s8_gegner"][0], SEG["s9_score"][0], SEG["s10_termin"][0], SEG["s11_cta"][0]]
wp = "".join(f'<div id="wp{i}" class="a" style="left:-300px;top:-200px;width:900px;height:2400px;background:{RED};transform:skewX(-14deg) translateX(-1600px)"></div>' for i in range(len(cuts)))
scene("wipe", 0, END, wp, "".join(
    f'tl.fromTo("#wp{i}", {{ x: 0 }}, {{ x: 3200, duration: 0.42, ease: "power2.inOut", immediateRender: false }}, {c - 0.21:.3f});' for i, c in enumerate(cuts)), track=6)

# ================================================================ Mauszeiger (führt durchs Reel)
ripples = "".join(f'<div id="cr{i}" class="a" style="left:{x - 50}px;top:{y - 50}px;width:100px;height:100px;border-radius:50%;border:6px solid #FFF;opacity:0"></div>'
                  for i, (t, x, y) in enumerate(CLICKS))
cj = []
for kind, t, x, y, d, ease in CUR:
    if kind == "set":
        cj.append(f'tl.set("#cur", {{ x: {x}, y: {y} }}, 0);')
    elif kind == "show":
        cj.append(f'tl.to("#cur", {{ opacity: 1, duration: 0.2 }}, {t});')
    elif kind == "move":
        cj.append(f'tl.to("#cur", {{ x: {x}, y: {y}, duration: {d}, ease: "{ease}" }}, {t:.3f});')
    elif kind == "wave":
        cj.append(f'tl.fromTo("#cur", {{ rotation: 0 }}, {{ keyframes: [{{ rotation: -22, duration: 0.1 }}, {{ rotation: 18, duration: 0.12 }}, {{ rotation: -16, duration: 0.12 }}, {{ rotation: 12, duration: 0.12 }}, {{ rotation: 0, duration: 0.12 }}], immediateRender: false }}, {t:.3f});')
    elif kind == "path":
        pts_, dur = x, y
        step = dur / (len(pts_) - 1)
        cj.append(f'tl.to("#cur", {{ keyframes: {json.dumps([{"x": round(px, 1), "y": round(py, 1), "duration": round(step, 4)} for px, py in pts_[1:]])}, ease: "none" }}, {t:.3f});')
for i, (t, x, y) in enumerate(CLICKS):
    cj.append(f'tl.fromTo("#cur-in", {{ scale: 1 }}, {{ keyframes: [{{ scale: 0.78, duration: 0.07 }}, {{ scale: 1, duration: 0.16 }}], immediateRender: false }}, {t - 0.05:.3f});')
    cj.append(f'tl.fromTo("#cr{i}", {{ opacity: 0.95, scale: 0.2 }}, {{ opacity: 0, scale: 1.6, duration: 0.45, ease: "power2.out", immediateRender: false }}, {t:.3f});')
# verspieltes Wippen im Leerlauf
cj.append(f'tl.fromTo("#cur-in", {{ rotation: -4 }}, {{ rotation: 6, duration: 0.9, ease: "sine.inOut", yoyo: true, repeat: {int(END / 0.9)}, immediateRender: false }}, 0);')
cj.append(f'tl.to("#cur", {{ opacity: 0, duration: 0.3 }}, {END - 0.6:.3f});')
open(f"{HERE}/compositions/cursor.html", "w", encoding="utf-8").write(f"""<template>
  <style>#root {{ position:absolute; inset:0; overflow:hidden; pointer-events:none; }} #root .a {{ position:absolute; }}</style>
  <div id="root" data-composition-id="cursor" data-width="1080" data-height="1920" data-layout-allow-overlap>
    {ripples}
    <div id="cur" class="a" style="left:0;top:0;opacity:0"><div id="cur-in" style="transform-origin:4px 4px">
      <svg width="84" height="100" viewBox="0 0 28 33" style="display:block;overflow:visible">
        <path d="M2 2 L2 26 L8.2 20.4 L12.6 30.6 L17 28.7 L12.7 18.9 L21 18.6 Z" fill="rgba(0,0,0,.35)" transform="translate(1.6,2.2)"/>
        <path d="M2 2 L2 26 L8.2 20.4 L12.6 30.6 L17 28.7 L12.7 18.9 L21 18.6 Z" fill="#FFF" stroke="#111" stroke-width="1.8" stroke-linejoin="round"/>
      </svg></div></div>
  </div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join("  " + c for c in cj)}
  window.__timelines["cursor"] = tl;
  </script>
</template>
""")

# ================================================================ Korn + Vignette (deterministisch)
_noise = ("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence "
          "type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")
open(f"{HERE}/compositions/frame.html", "w").write(f"""<template>
  <style>#root {{ position:absolute; inset:0; pointer-events:none; overflow:hidden; }}</style>
  <div id="root" data-composition-id="frame" data-width="1080" data-height="1920" data-layout-ignore>
    <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%, transparent 55%, rgba(0,0,0,.55) 100%);"></div>
    <div id="fr-grain" style="position:absolute;inset:-64px;background-image:url(&quot;{_noise}&quot;);background-size:256px 256px;opacity:.09;mix-blend-mode:overlay;"></div>
  </div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  const H = (k, i) => {{ let x = Math.sin(k * 127.1 + i * 311.7) * 43758.5453; return x - Math.floor(x); }};
  const g = document.getElementById("fr-grain");
  const clock = {{ t: 0 }};
  tl.to(clock, {{ t: {END}, duration: {END}, ease: "none", onUpdate: () => {{ const k = Math.floor(clock.t * 12); g.style.transform = `translate(${{-H(k, 1) * 64}}px, ${{-H(k, 2) * 64}}px)`; }} }}, 0);
  window.__timelines["frame"] = tl;
  </script>
</template>
""")

# ================================================================ Untertitel: 1–3 Wörter, aktives Wort rot hinterlegt (nicht bei den Spielernamen)
HIDE = {"s4_thuerauf", "s5_clain", "s6_kandra", "s7_svec"}
SEID = W("seid"); DAB = W("dabei")
words = [w for w in WORDS if w["scene"] not in HIDE and not (w["scene"] == "s11_cta" and SEID - 0.01 <= w["start"] <= DAB + 0.01)
         and not (w["scene"] == "s9_score" and w["start"] >= W("für", after=W("4")) - 0.01)]
groups, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    if (len(cur) >= 3 or len(" ".join(x["text"] for x in cur)) >= 15 or re.search(r"[.!?:,]$", w["text"]) or not nxt
            or nxt["start"] - w["end"] >= 0.3 or nxt["scene"] != w["scene"]):
        groups.append(cur); cur = []
ch, cjs, wi = [], [], 0
for gi, g in enumerate(groups):
    ga = max(g[0]["start"] - 0.04, 0.05)
    nxt_a = groups[gi + 1][0]["start"] - 0.05 if gi + 1 < len(groups) else END
    gb = min(g[-1]["end"] + 0.35, nxt_a, SEG[g[-1]["scene"]][1] - 0.02)
    gb = max(gb, ga + 0.2)
    spans = []
    for w in g:
        spans.append(f'<span id="w{wi}" style="padding:0 10px;border-radius:8px">{w["text"].upper()}</span>')
        cjs.append(f'tl.set("#w{wi}", {{ backgroundColor: "{RED}" }}, {max(w["start"], ga):.3f});')
        if w is not g[-1]:
            cjs.append(f'tl.set("#w{wi}", {{ backgroundColor: "rgba(0,0,0,0)" }}, {max(g[g.index(w) + 1]["start"], ga + 0.01):.3f});')
        wi += 1
    ch.append(f'<div id="k{gi}" class="clip cap" data-start="{ga:.3f}" data-duration="{gb - ga:.3f}">{"".join(spans)}</div>')
    cjs.append(f'tl.fromTo("#k{gi}", {{ opacity: 0, scale: 0.8, rotationX: -70, transformPerspective: 700 }}, {{ opacity: 1, scale: 1, rotationX: 0, duration: {min(0.16, (gb - ga) / 3):.3f}, ease: "back.out(2.2)" }}, {ga:.3f});'
               f'tl.to("#k{gi}", {{ opacity: 0, duration: {min(0.06, (gb - ga) / 4):.3f} }}, {gb - min(0.06, (gb - ga) / 4):.3f});')
open(f"{HERE}/compositions/captions.html", "w", encoding="utf-8").write(f"""<template>
  <style>{FONTS}
  #root {{ position:absolute; inset:0; }}
  #root .cap {{ position:absolute; left:110px; width:860px; top:1238px; text-align:center; font-family:'BC', sans-serif; font-weight:900; font-style:italic;
          font-size:76px; line-height:1.05; color:#FFF; opacity:0; white-space:nowrap;
          text-shadow:0 5px 0 #000, 0 0 22px rgba(0,0,0,.9), 3px 3px 0 #000, -3px -3px 0 #000, 3px -3px 0 #000, -3px 3px 0 #000; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920" data-layout-allow-caption-zone>{"".join(ch)}</div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  {"".join(cjs)}
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
    <style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:{DARK}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
{hh}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{END}" data-track-index="7" data-track-kind="captions" data-width="1080" data-height="1920"></div>
      <div id="cursor" data-composition-id="cursor" data-composition-src="compositions/cursor.html" data-start="0" data-duration="{END}" data-track-index="8" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{END}" data-track-index="10"></audio>
      <div id="frame" data-composition-id="frame" data-composition-src="compositions/frame.html" data-start="0" data-duration="{END}" data-track-index="9" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
SFX = sorted(SFX)
SFX = [x for i, x in enumerate(SFX) if not any(abs(x[0] - y[0]) < 0.06 and x[1] == y[1] for y in SFX[:i])]
assert not any(f == "ding" for _, f, _ in SFX)  # keine Glocke (Wunsch)
json.dump([{"t": round(t, 3), "f": f, "g": g} for t, f, g in SFX if g > 0], open(f"{HERE}/assets/sfx.json", "w"), indent=0)
for fn, src in [("hyperframes.json", "hyperframes.json"), ("package.json", "package.json"), ("meta.json", "meta.json")]:
    open(f"{HERE}/{fn}", "w").write(open(os.path.join(HERE, "..", "video03-reel", src)).read().replace("otto-video03-reel", "scf-heimspiel02-reel"))
print(f"Reel: {END}s, {len(HOSTS)} Szenen, {len(groups)} Untertitel, {len(CLICKS)} Klicks, {len(SFX)} Soundeffekte")
