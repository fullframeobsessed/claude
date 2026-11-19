"""Sprecherspur Reel (9:16): Hook (P1), 60-Sekunden-Teil (P2, Tempo so berechnet, dass er genau in den Timer passt), Schluss (P3).

Eingabe:  assets/arthur/P1.mp3 … P3.mp3
Ausgabe:  assets/voice.wav, assets/words.json, assets/segments.json
Aufruf:   HF_HUB_DISABLE_XET=1 python3 voice.py
"""
import argparse, difflib, json, os, re, subprocess, sys
import numpy as np, librosa, soundfile as sf

TX = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "texts.json")))


ap = argparse.ArgumentParser()
ap.add_argument("--tempo", type=float, default=1.2, help="Sprechtempo für Hook und Schluss")
ap.add_argument("--maxpause", type=float, default=0.22, help="längste erlaubte Pause innerhalb eines Kapitels (s, vor Tempo)")
args = ap.parse_args()

HERE = os.path.dirname(os.path.abspath(__file__))
A = f"{HERE}/assets"
SR = 48000
PIECES = TX["pieces"]
# Stille-Elemente (Sekunden, bereits im Endtempo). "lead" = stille Einleitung der folgenden Kapitelkarte.
PLAN = [("open", 0.25), ("P1", None), ("go", 0.3), ("P2", None), ("P3", None), ("endcard", 3.5)]
TIMER = 60.0  # Sekunden vom Timerstart (Ende "Los!") bis "Zeit um!"
GAP = 0.18  # Luft am Ende eines Kapitels
by_id = {k: {"lines": [v]} for k, v in TX["scenes"].items()}


def prep(path, tempo=None):
    """Laden, Ränder weich kappen (Einsatz der ersten Silbe bleibt erhalten), lange Pausen kürzen, Lautheit angleichen, Tempo."""
    y, _ = librosa.load(path, sr=SR, mono=True)
    iv = librosa.effects.split(y, top_db=48, frame_length=2048, hop_length=256)
    pre, post = int(0.12 * SR), int(0.10 * SR)
    a, b = max(iv[0][0] - pre, 0), min(iv[-1][1] + post, len(y))
    parts, last = [], None
    for s, e in iv:
        s, e = max(s, a), min(e, b)
        if last is not None:
            gap = s - last
            parts.append(np.zeros(min(gap, int(args.maxpause * SR)), np.float32))
        else:
            parts.append(y[a:s])
        parts.append(y[s:e]); last = e
    parts.append(y[last:b])
    z = np.concatenate(parts)
    fade = int(0.012 * SR)
    z[:fade] *= np.linspace(0, 1, fade); z[-fade:] *= np.linspace(1, 0, fade)
    tmp_in, tmp_out = f"{A}/_in.wav", f"{A}/_out.wav"
    sf.write(tmp_in, z, SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp_in, "-af",
                    f"rubberband=tempo={tempo or args.tempo}:pitch=1:formant=preserved:transients=smooth,loudnorm=I=-18:TP=-2:LRA=7",
                    "-ar", str(SR), "-ac", "1", tmp_out], check=True)
    out, _ = librosa.load(tmp_out, sr=SR, mono=True)
    os.remove(tmp_in); os.remove(tmp_out)
    return out


chunks, segs, pieces, t, lead = [], [], [], 0.0, None
for name, d in PLAN:
    if not name.startswith("P"):  # Stille
        if name == "lead":
            lead = t
        else:
            segs.append({"id": name, "start": round(t, 3), "end": round(t + d, 3)})
        chunks.append(np.zeros(int(d * SR), np.float32)); t += d
        continue
    if name == "P2":
        t_go = t - 0.3  # Timer startet mit Beginn der "go"-Pause
        raw = prep(f"{A}/arthur/P2.mp3", 1.0)
        target = TIMER - (t - t_go) - 0.45
        y = prep(f"{A}/arthur/P2.mp3", len(raw) / SR / target)
        print(f"P2: {len(raw)/SR:.2f}s → Tempo {len(raw)/SR/target:.3f}")
    else:
        y = prep(f"{A}/arthur/{name}.mp3")
    if name == "P3":  # P3 beginnt exakt bei Timer = 0
        pad = t_go + TIMER - t
        chunks.append(np.zeros(int(max(pad, 0) * SR), np.float32)); t += max(pad, 0)
        segs.append({"id": "timer", "start": round(t_go, 3), "end": round(t, 3)})
    pieces.append({"name": name, "scenes": PIECES[name], "start": t, "end": t + len(y) / SR, "lead": lead}); lead = None
    chunks.append(y); t += len(y) / SR
    chunks.append(np.zeros(int(GAP * SR), np.float32)); t += GAP

sf.write(f"{A}/voice_raw.wav", np.concatenate(chunks), SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{A}/voice_raw.wav", "-af",
                "highpass=f=60,equalizer=f=120:t=q:w=1.2:g=2,deesser=i=0.3,"
                "acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150:makeup=1.5,loudnorm=I=-16:TP=-1.5:LRA=7",
                "-ar", str(SR), "-ac", "1", f"{A}/voice.wav"], check=True)

# ---- Wort-Zeiten (Whisper) → Skript-Wörter
from faster_whisper import WhisperModel  # noqa: E402
y16, _ = librosa.load(f"{A}/voice.wav", sr=16000)
wh = [w for s in WhisperModel("small", device="cpu", compute_type="int8").transcribe(y16, language="de", word_timestamps=True)[0] for w in s.words]
norm = lambda x: re.sub(r"[^\wäöüß]", "", x.lower())  # noqa: E731
script = [(w, sid, p) for p in pieces for sid in p["scenes"] for w in " ".join(by_id[sid]["lines"]).split()]
sm = difflib.SequenceMatcher(a=[norm(w) for w, _, _ in script], b=[norm(w.word) for w in wh], autojunk=False)
times = [None] * len(script)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        times[blk.a + k] = (wh[blk.b + k].start, wh[blk.b + k].end)
for i in range(len(script)):
    if times[i] is None:
        prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), script[i][2]["start"])
        nxt = next((times[j][0] for j in range(i + 1, len(script)) if times[j]), script[i][2]["end"])
        times[i] = (prev, max(prev + 0.1, (prev + nxt) / 2))
words = []
for (w, sid, p), (a, b) in zip(script, times):
    a = min(max(a, p["start"]), p["end"])
    words.append({"text": w, "start": round(a, 3), "end": round(max(b, a + 0.05), 3), "scene": sid})
for i in range(1, len(words)):
    words[i]["start"] = max(words[i]["start"], words[i - 1]["start"] + 0.02)
for p in pieces:
    bounds = [p["lead"] if p["lead"] is not None else p["start"]]
    for sid in p["scenes"][1:]:
        bounds.append(round(next(w for w in words if w["scene"] == sid)["start"] - 0.12, 3))
    bounds.append(p["end"] + GAP)
    for k, sid in enumerate(p["scenes"]):
        segs.append({"id": sid, "start": round(bounds[k], 3), "end": round(bounds[k + 1], 3)})
segs.sort(key=lambda s: s["start"])
json.dump([{k: v for k, v in w.items() if k != "scene"} for w in words], open(f"{A}/words.json", "w"), ensure_ascii=False, indent=0)
json.dump(segs, open(f"{A}/segments.json", "w"), indent=1)
print(f"Gesamt {t:.2f}s ({int(t // 60)}:{int(t % 60):02d}) · {len(words)} Wörter · Whisper-Übereinstimmung {sm.ratio()*100:.0f}%")
for s in segs:
    print(f"  {s['id']:<18} {s['start']:6.2f} → {s['end']:6.2f}")
