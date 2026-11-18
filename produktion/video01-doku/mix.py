"""Tonmischung Video 01: Stimme + Hintergrundmusik (mit Ducking) + Mausklicks auf Text-Einblendungen.

Eingabe:  assets/voice.wav, assets/music.mp3, assets/click1-3.mp3, compositions/*.html, index.html
Ausgabe:  assets/mix.wav, assets/musik_bett.wav, assets/klicks.wav, assets/sfx_times.json,
          und die beiden Videos mit neuer Tonspur (*_mit_musik.mp4)
"""
import json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
A = f"{HERE}/assets"

# ---------- Einblendezeiten der Texte aus den Szenen lesen
TEXT_IDS = r"^(d1-st|d1-ltname|d3-s[abc]|d4-say|d4-faul|d5-du|d5-wg|k09-num|k09-gl|k09-fin|k10-q0|k10-lt|k11-w\d|k12-r\d|" \
           r"k14-l[ap]|k15-st|k16-txt|k17-b|k19-lt|k20-eq|k21-q\d|k24-q|k25-[ab]|k2[789]-ht|k30-ht|k27-lt|k27-n|k28-tag|" \
           r"k29-sl|k30-w|k31-[ab]|k34-ch)$"
idx = open(f"{HERE}/index.html").read()
hosts = {m[0]: float(m[1]) for m in re.findall(r'data-composition-id="(\w+)" data-composition-src="compositions/\w+\.html" data-start="([\d.]+)"', idx)}
times = []
for cid, start in hosts.items():
    src = open(f"{HERE}/compositions/{cid}.html").read()
    m = re.search(r"const T = (\{.*?\});", src)
    T = json.loads(m.group(1)) if m else {}
    ev = lambda e: eval(e.replace("T.", "T_"), {}, {f"T_{k}": v for k, v in T.items()})  # noqa: E731
    for sel, expr in re.findall(r'(?:fadeIn|type)\("#([\w-]+)",\s*(?:\d+,\s*)?([^,)]+)', src):
        if re.match(TEXT_IDS, sel):
            try:
                times.append((round(start + ev(expr) + 0.04, 3), sel))
            except Exception:
                pass
    if re.search(rf'id="{cid}-t" class="t cond"', src):  # Kapitelkarten
        times.append((round(start + 0.3, 3), f"{cid}-t"))
    if cid == "d2":
        times.append((round(start + 0.1, 3), "d2-t"))
times.sort()
clicks, last = [], -9
for t, sel in times:  # nie dichter als 0,7 s
    if t - last >= 0.7:
        clicks.append({"t": t, "id": sel, "v": len(clicks) % 3 + 1}); last = t
json.dump(clicks, open(f"{A}/sfx_times.json", "w"), indent=0)
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{A}/voice.wav"]))
print(f"{len(clicks)} Klicks · Stimme {dur:.1f}s")

# ---------- Klickspur (jede Variante zuerst auf gleiche Spitze normalisieren, Stille davor/danach kappen)
for v in (1, 2, 3):
    det = subprocess.run(["ffmpeg", "-i", f"{A}/click{v}.mp3", "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    peak = float(re.search(r"max_volume: ([-\d.]+) dB", det).group(1))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{A}/click{v}.mp3", "-af",
                    f"silenceremove=start_periods=1:start_threshold=-50dB,atrim=0:0.35,afade=t=out:st=0.25:d=0.1,"
                    f"highpass=f=250,aresample=48000,volume={-3 - peak:.1f}dB", "-ac", "1", f"{A}/_c{v}.wav"], check=True)
inp, flt = [], []
for i, c in enumerate(clicks):
    inp += ["-i", f"{A}/_c{c['v']}.wav"]
    flt.append(f"[{i}:a]adelay={int(c['t'] * 1000)}|{int(c['t'] * 1000)}[k{i}]")
flt.append("".join(f"[k{i}]" for i in range(len(clicks))) + f"amix=inputs={len(clicks)}:normalize=0,apad=whole_dur={dur}[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[out]", "-t", str(dur),
                "-ar", "48000", "-ac", "1", f"{A}/klicks.wav"], check=True)

# ---------- Musikbett: auf Videolänge, sanfte Blenden, Lautheit fürs Unterlegen
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{A}/music.mp3", "-af",
                f"atrim=0:{dur},afade=t=in:st=0:d=2.5,afade=t=out:st={dur - 5}:d=5,loudnorm=I=-24:TP=-3,aresample=48000",
                "-ac", "2", f"{A}/musik_bett.wav"], check=True)

# ---------- Mischung: Musik duckt unter der Stimme (Sidechain), Klicks dezent darüber
fc = ("[0:a]aformat=channel_layouts=stereo,asplit=2[vo][sc];"
      "[1:a]volume=0.55[mu];"
      "[mu][sc]sidechaincompress=threshold=0.02:ratio=5:attack=25:release=450:makeup=1[duck];"
      "[2:a]aformat=channel_layouts=stereo,volume=0.32[kl];"
      "[vo][duck][kl]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{A}/voice.wav", "-i", f"{A}/musik_bett.wav", "-i", f"{A}/klicks.wav",
                "-filter_complex", fc, "-map", "[out]", "-ar", "48000", f"{A}/mix.wav"], check=True)

# ---------- Neue Tonspur in die fertigen Videos (Bild wird nur kopiert, nicht neu gerendert)
for n in ("mit_untertiteln", "ohne_untertitel"):
    src = f"{HERE}/otto_video01_{n}.mp4"
    if os.path.exists(src) and os.path.getmtime(src) > os.path.getmtime(f"{A}/voice.wav"):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", f"{A}/mix.wav", "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart",
                        f"{HERE}/otto_video01_{n}_mit_musik.mp4"], check=True)
        print("→", f"otto_video01_{n}_mit_musik.mp4")
for v in (1, 2, 3):
    os.remove(f"{A}/_c{v}.wav")
