"""Setzt die Higgsfield/ElevenLabs-Aufnahmen (Stimme „Arthur“) zur Doku-Sprecherspur zusammen.

Eingabe:  assets/arthur/A.mp3 … D.mp3 (je ein Stück aus einer oder mehreren Szenen)
Ausgabe:  assets/voice.wav, assets/words.json, assets/segments.json (gleiches Format wie tts.py)
Aufruf:   HF_HUB_DISABLE_XET=1 python3 voice_arthur.py
"""
import difflib, json, os, re, subprocess, sys
import numpy as np
import librosa

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "video01"))
import scenes  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
A = f"{HERE}/assets"
SR = 48000
PLAN = [("open", 3.4), ("A", ["s01_hook"]), ("title", 3.2), ("B", ["s02_bad", "s03_socken", "s04_pinguine"]),
        ("C", ["s05_faul", "s06_nicht_faul"]), ("D", ["s07_versprechen"]), ("s08_kap1", 3.4),
        ("E", ["s09_zahlen"]), ("F", ["s10_zitat"]), ("G", ["s11_wolke", "s12_flucht"]),
        ("lead", 1.6), ("H", ["s13_kap2"]), ("I", ["s14_gehirn"]), ("J", ["s15_bochum"]), ("K", ["s16_knopf", "s17_waage"]),
        ("lead", 1.6), ("L", ["s18_kap3", "s19_morgenotto"]), ("M", ["s20_scans"]), ("N", ["s21_uebergabe", "s22_kette"]),
        ("lead", 1.6), ("O", ["s23_kap4", "s24_kreis"]), ("P", ["s25_fertigmachen"]),
        ("lead", 1.6), ("Q", ["s26_kap5"]), ("R", ["s27_vergeben"]), ("S", ["s28_benennen"]), ("T", ["s29_schritt"]),
        ("U", ["s30_timer"]), ("V", ["s31_jetzt"]), ("s32_spaeter", 2.6), ("W", ["s33_deadline"]), ("s34_endcard", 10.0)]
GAP = 0.45  # Luft zwischen zwei Stücken
by_id = {s["id"]: s for s in scenes.SCENES}


def load_trimmed(p):
    y, _ = librosa.load(p, sr=SR, mono=True)
    yt, idx = librosa.effects.trim(y, top_db=40)
    a, b = max(idx[0] - int(0.03 * SR), 0), min(idx[1] + int(0.08 * SR), len(y))
    return y[a:b]


chunks, segs, pieces, t, lead = [], [], [], 0.0, None
for name, val in PLAN:
    if isinstance(val, (int, float)):
        if name == "lead":  # Stille, die zur nächsten Szene (Kapitelkarte) gehört
            lead = t
        else:
            segs.append({"id": name, "start": round(t, 3), "end": round(t + val, 3)})
        chunks.append(np.zeros(int(val * SR), np.float32)); t += val
        continue
    y = load_trimmed(f"{A}/arthur/{name}.mp3")
    pieces.append({"name": name, "scenes": val, "start": t, "end": t + len(y) / SR, "lead": lead}); lead = None
    chunks.append(y); t += len(y) / SR
    chunks.append(np.zeros(int(GAP * SR), np.float32)); t += GAP

import soundfile as sf  # noqa: E402
sf.write(f"{A}/voice_raw.wav", np.concatenate(chunks), SR)
# Sanfte Studio-Kette: keine Tonhöhenänderung, etwas Wärme, gezähmte S-Laute, Sendelautheit
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{A}/voice_raw.wav", "-af",
                "highpass=f=60,equalizer=f=120:t=q:w=1.2:g=2,deesser=i=0.3,"
                "acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150:makeup=1.5,loudnorm=I=-16:TP=-1.5:LRA=7",
                "-ar", str(SR), "-ac", "1", f"{A}/voice.wav"], check=True)

# ---- Wort-Zeiten (Whisper) auf Skript-Wörter ausrichten
from faster_whisper import WhisperModel  # noqa: E402
y16, _ = librosa.load(f"{A}/voice.wav", sr=16000)
wh = [w for s in WhisperModel("small", device="cpu", compute_type="int8").transcribe(y16, language="de", word_timestamps=True)[0] for w in s.words]
norm = lambda x: re.sub(r"[^\wäöüß]", "", x.lower())  # noqa: E731
script = []  # (wort, szene, stück)
for p in pieces:
    for sid in p["scenes"]:
        for w in " ".join(by_id[sid]["lines"]).split():
            script.append((w, sid, p))
sm = difflib.SequenceMatcher(a=[norm(w) for w, _, _ in script], b=[norm(w.word) for w in wh], autojunk=False)
times = [None] * len(script)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        times[blk.a + k] = (wh[blk.b + k].start, wh[blk.b + k].end)
for i in range(len(script)):  # Lücken linear zwischen Nachbarn auffüllen
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

# Szenengrenzen innerhalb eines Stücks: kurz vor dem ersten Wort der nächsten Szene
for p in pieces:
    bounds = [p["lead"] if p["lead"] is not None else p["start"]]
    for sid in p["scenes"][1:]:
        first = next(w for w in words if w["scene"] == sid)
        bounds.append(round(first["start"] - 0.15, 3))
    bounds.append(p["end"] + GAP)
    for k, sid in enumerate(p["scenes"]):
        segs.append({"id": sid, "start": round(bounds[k], 3), "end": round(bounds[k + 1], 3)})
segs.sort(key=lambda s: s["start"])
json.dump([{k: v for k, v in w.items() if k != "scene"} for w in words], open(f"{A}/words.json", "w"), ensure_ascii=False, indent=0)
json.dump(segs, open(f"{A}/segments.json", "w"), indent=1)
print(f"Gesamt {t:.2f}s · {len(words)} Wörter · Whisper-Übereinstimmung {sm.ratio()*100:.0f}%")
for s in segs:
    print(f"  {s['id']:<18} {s['start']:6.2f} → {s['end']:6.2f}")
