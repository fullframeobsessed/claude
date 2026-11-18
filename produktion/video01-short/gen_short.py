"""YouTube Short zu Video 01 (1080x1920): Hook bis Versprechen + Schlusskarte mit Verweis auf die ganze Folge."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "video01"))
sys.path.insert(0, os.path.join(HERE, "..", "video01-hf"))
from art import _head_base, _face  # noqa: E402

DOKU = os.path.join(HERE, "..", "video01-doku")
CUTS = [(2.8, 8.74, 0.0), (11.34, 47.54, 5.94 - 0.06)]  # (von, bis, Ziel-Start) wie in assets/clip.mp4
CLIP = 42.166
CTA = 38.6           # ab hier Schlusskarte
AMBER, MUTED = "#E8C27A", "#8C8F96"
VID_TOP = 540
BAND = "left:48px;width:840px;"  # sichere Zone YouTube Shorts: x 48–888, y 288–1248

words = []
for w in json.load(open(f"{DOKU}/assets/words.json")):
    for a, b, off in CUTS:
        if a <= w["start"] < b:
            words.append({"text": w["text"], "start": round(w["start"] - a + off, 3), "end": round(min(w["end"], b) - a + off, 3)})
words = [w for w in words if w["start"] < CTA - 0.2]

# --- Untertitel: 2–3 Wörter, energisch, aktuelles Wort in Bernstein
groups, cur = [], []
for i, w in enumerate(words):
    cur.append(w)
    nxt = words[i + 1] if i + 1 < len(words) else None
    if len(cur) >= 3 or len(" ".join(x["text"] for x in cur + ([nxt] if nxt else []))) > 18 or re.search(r"[.!?:,]$", w["text"]) or not nxt or nxt["start"] - w["end"] > 0.3:
        groups.append(cur); cur = []
starts = [g[0]["start"] for g in groups] + [CTA]
ch, cj = [], []
for gi, g in enumerate(groups):
    a, b = max(starts[gi] - 0.03, 0.05), min(g[-1]["end"] + 0.2, starts[gi + 1] - 0.02)
    sp = " ".join(f'<span id="g{gi}w{k}">{w["text"]}</span>' for k, w in enumerate(g))
    ch.append(f'<div id="g{gi}" class="clip cap" data-start="{a:.3f}" data-duration="{b - a:.3f}">{sp}</div>')
    cj.append(f'tl.fromTo("#g{gi}", {{opacity:0, scale:0.92}}, {{opacity:1, scale:1, duration:0.12, ease:"power2.out"}}, {a:.3f});')
    for k, w in enumerate(g):
        cj.append(f'tl.set("#g{gi}w{k}", {{color:"{AMBER}"}}, {w["start"]:.3f}); tl.set("#g{gi}w{k}", {{color:"#FFFFFF"}}, {w["end"]:.3f});')
    cj.append(f'tl.to("#g{gi}", {{opacity:0, duration:0.08}}, {b - 0.08:.3f});')
os.makedirs(f"{HERE}/compositions", exist_ok=True)
open(f"{HERE}/compositions/caps.html", "w").write(f"""<template>
  <style>
  #root {{ position:absolute; inset:0; }}
  #root .cap {{ position:absolute; {BAND} top:{VID_TOP + 588 + 18}px; white-space:nowrap; text-align:center; font-family:'Oswald', sans-serif;
          font-weight:700; text-transform:uppercase; font-size:78px; line-height:1; color:#FFF; opacity:0;
          text-shadow:0 6px 0 #000, 0 0 30px rgba(0,0,0,.8); }}
  </style>
  <div id="root" data-composition-id="caps" data-width="1080" data-height="1920" data-layout-allow-caption-zone>
    {"".join(ch)}
  </div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  {"".join(cj)}
  window.__timelines["caps"] = tl;
  </script>
</template>
""")

# --- Oberfläche: Titel oben, Rahmen um die Szene, Schlusskarte
NOISE = ("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence "
         "type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")
head = f'<svg viewBox="-150 -180 300 300" width="420" height="400">{_head_base()}{_face("smirk")}</svg>'
open(f"{HERE}/compositions/ui.html", "w").write(f"""<template>
  <style>
  #root {{ position:absolute; inset:0; font-family:'Inter', sans-serif; color:#FFF; }}
  #root .t {{ position:absolute; {BAND} text-align:center; }}
  #root .cond {{ font-family:'Oswald', sans-serif; font-weight:700; text-transform:uppercase; line-height:1; }}
  </style>
  <div id="root" data-composition-id="ui" data-width="1080" data-height="1920">
    <div id="ui-k" class="t" style="top:300px;font-size:30px;font-weight:800;letter-spacing:.4em;color:{AMBER};">OTTO NORMALPSYCHE</div>
    <div id="ui-t" class="t cond" style="top:345px;font-size:82px;">WARUM DU<br>ALLES AUFSCHIEBST</div>
    <div style="position:absolute;left:0;right:0;top:{VID_TOP - 4}px;height:2px;background:rgba(255,255,255,.25);"></div>
    <div style="position:absolute;left:0;right:0;top:{VID_TOP + 588 + 2}px;height:2px;background:rgba(255,255,255,.25);"></div>
    <div id="end" style="position:absolute;inset:0;background:#0B0C0E;opacity:0;">
      <div style="position:absolute;left:258px;top:290px;">{head}</div>
      <div id="end-q" class="t cond" style="top:700px;font-size:104px;">UND DER<br><span style="color:{AMBER}">TRICK?</span></div>
      <div id="end-a" class="t" style="top:935px;font-size:36px;font-weight:800;letter-spacing:.08em;">DIE GANZE FOLGE</div>
      <div id="end-b" class="t" style="top:985px;font-size:36px;font-weight:800;letter-spacing:.08em;">JETZT AUF DEM KANAL</div>
      <div id="end-arrow" class="t cond" style="top:1035px;font-size:96px;color:{AMBER};">↓</div>
      <div id="end-h" class="t" style="top:1160px;font-size:40px;font-weight:700;color:{MUTED};">@ottonormalpsyche</div>
    </div>
    <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%, transparent 50%, rgba(0,0,0,.6) 100%);"></div>
    <div style="position:absolute;inset:0;background-image:url(&quot;{NOISE}&quot;);background-size:256px 256px;opacity:.10;mix-blend-mode:overlay;"></div>
  </div>
  <script>
  const tl = gsap.timeline({{ paused: true }});
  tl.fromTo("#ui-t", {{ opacity: 0, scale: 1.08 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, 0);
  tl.fromTo("#ui-k", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0.1);
  tl.to("#end", {{ opacity: 1, duration: 0.3, ease: "power2.inOut" }}, {CTA});
  tl.fromTo("#end-q", {{ opacity: 0, scale: 1.1 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, {CTA + 0.25});
  tl.fromTo(["#end-a", "#end-b"], {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35, stagger: 0.15 }}, {CTA + 0.7});
  tl.fromTo("#end-arrow", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }}, {CTA + 1.1});
  tl.fromTo("#end-h", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {CTA + 1.3});
  window.__timelines["ui"] = tl;
  </script>
</template>
""")

open(f"{HERE}/index.html", "w").write(f"""<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0B0C0E; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{CLIP}" data-width="1080" data-height="1920">
      <video id="clip" class="clip" src="assets/clip.mp4" data-start="0" data-duration="{CLIP}" data-track-index="0" data-has-audio="true" playsinline
             style="position:absolute;left:0;top:{VID_TOP}px;width:1080px;height:588px;object-fit:cover;"></video>
      <div id="ui" data-composition-id="ui" data-composition-src="compositions/ui.html" data-start="0" data-duration="{CLIP}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="caps" data-composition-id="caps" data-composition-src="compositions/caps.html" data-start="0" data-duration="{CTA}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920"></div>
    </div>
    <script>window.__timelines["main"] = gsap.timeline({{ paused: true }});</script>
  </body>
</html>
""")
for fn in ("hyperframes.json", "package.json", "meta.json"):
    open(f"{HERE}/{fn}", "w").write(open(f"{DOKU}/{fn}").read().replace("otto-video01-doku", "otto-video01-short"))
print(f"Short: {CLIP}s, {len(words)} Wörter, {len(groups)} Untertitel-Gruppen")
