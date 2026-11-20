"""Sprecherspur: Arthur-Take kürzen (Pausen ≤ MAXP), Tempo, Studio-Kette; Wortzeiten per Whisper → assets/words.json, assets/segments.json.
Aufruf: HF_HUB_DISABLE_XET=1 python3 voice.py"""
import difflib, json, re, subprocess
import numpy as np, librosa, soundfile as sf

A = "assets"; SR = 48000
TEMPO, MAXP, HEAD, TAIL = 1.07, 0.30, 0.12, 3.6
TX = json.load(open("texts.json"))

y, _ = librosa.load(f"{A}/arthur/voice_take1.mp3", sr=SR, mono=True)
# Vorlauf: Wortanfänge im Rohtake, vor denen eine längere Pause stehen soll (Spieler-Auftritte, Szenenwechsel)
from faster_whisper import WhisperModel  # noqa: E402
_wm = WhisperModel("small", device="cpu", compute_type="int8")
_raw = [w for s_ in _wm.transcribe(librosa.resample(y, orig_sr=SR, target_sr=16000), language="de", word_timestamps=True)[0] for s_ in [s_] for w in s_.words]
LONG = {"johannes": 0.55, "edwin": 0.75, "david": 0.75, "und": 0.75, "heuchelhof": 0.5, "aber": 0.45, "samstag": 0.45, "kommt": 0.45}
long_at = []
for i, w in enumerate(_raw):
    k = re.sub(r"[^\wäöüß]", "", w.word.lower())
    if k in LONG and (k != "und" or (i + 1 < len(_raw) and "armin" in _raw[i + 1].word.lower())) and (k != "heuchelhof" or i > 15):
        long_at.append((w.start, LONG[k]))
print("lange Pausen vor:", [round(t, 2) for t, _ in long_at])
iv = librosa.effects.split(y, top_db=42, frame_length=2048, hop_length=256)
# Wortanfänge mitten in einem Sprechstück: an der leisesten Stelle davor auftrennen
iv = [list(x) for x in iv]
for t, _ in long_at:
    c = int(t * SR)
    for k, (a, b) in enumerate(iv):
        if a + int(0.05 * SR) < c < b:
            lo, hi = c - int(0.12 * SR), c + int(0.02 * SR)
            rms = librosa.feature.rms(y=y[lo:hi], frame_length=512, hop_length=64)[0]
            cut = lo + int(np.argmin(rms)) * 64 + 256
            iv[k:k + 1] = [[a, cut], [cut, b]]
            break
parts = [y[max(iv[0][0] - int(0.04 * SR), 0):iv[0][0]]]
for k, (s, e) in enumerate(iv):
    if k:
        want = next((d for t, d in long_at if abs(t * SR - s) < 0.15 * SR), MAXP)
        parts.append(np.zeros(min(s - iv[k - 1][1], int(want * SR)) if want == MAXP else int(want * SR), np.float32))
    parts.append(y[s:e])
parts.append(y[iv[-1][1]:iv[-1][1] + int(0.08 * SR)])
sf.write(f"{A}/_in.wav", np.concatenate(parts), SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{A}/_in.wav", "-af",
                f"rubberband=tempo={TEMPO}:pitch=1:formant=preserved:transients=smooth,"
                f"adelay={int(HEAD*1000)},apad=pad_dur={TAIL},"
                "highpass=f=60,equalizer=f=120:t=q:w=1.2:g=2,deesser=i=0.3,"
                "acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150:makeup=1.5,loudnorm=I=-16:TP=-1.5:LRA=7",
                "-ar", str(SR), "-ac", "1", f"{A}/voice.wav"], check=True)
subprocess.run(["rm", "-f", f"{A}/_in.wav"])
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{A}/voice.wav"]))

from faster_whisper import WhisperModel  # noqa: E402
y16, _ = librosa.load(f"{A}/voice.wav", sr=16000)
wh = [w for s in WhisperModel("small", device="cpu", compute_type="int8").transcribe(y16, language="de", word_timestamps=True)[0] for w in s.words]
norm = lambda x: re.sub(r"[^\wäöüß]", "", x.lower())  # noqa: E731
script = [(w, sid) for sid, txt in TX.items() for w in txt.split()]
sm = difflib.SequenceMatcher(a=[norm(w) for w, _ in script], b=[norm(w.word) for w in wh], autojunk=False)
times = [None] * len(script)
for b in sm.get_matching_blocks():
    for k in range(b.size):
        times[b.a + k] = (wh[b.b + k].start, wh[b.b + k].end)
for i in range(len(script)):
    if times[i] is None:
        prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), HEAD)
        nxt = next((times[j][0] for j in range(i + 1, len(script)) if times[j]), prev + 0.4)
        times[i] = (prev + 0.02, max(prev + 0.12, nxt - 0.02))
# Wortanfänge am echten Einsatz ausrichten (Whisper liegt bei dieser Stimme bis ~0,5 s daneben)
on = librosa.effects.split(y16, top_db=35, frame_length=1024, hop_length=160) / 16000
on = [x for x in on if x[1] - x[0] > 0.15]  # Atmer ignorieren
starts_on = [a for a, b in on]
first = {}
for i, (w, sid) in enumerate(script):
    first.setdefault(sid, i)
for i in range(len(times)):
    a, b = times[i]
    if i in first.values() and i > 0:  # erstes Wort einer Szene: erster Einsatz nach dem Sprechstück des Vorgängerworts
        pa = times[i - 1][0]
        blk = next(((x, y_) for x, y_ in on if x - 0.05 <= pa < y_), None)
        c = next((x for x in starts_on if blk and x >= blk[1]), None)
        if c is not None and abs(c - a) < 1.0:
            a = c
    elif not any(x <= a < y_ for x, y_ in on):
        a = next((x for x in starts_on if x > a), a)
    times[i] = (a, max(b, a + 0.1))
for i in range(1, len(times)):
    if times[i][0] < times[i - 1][0] + 0.05:
        times[i] = (times[i - 1][0] + 0.05, max(times[i][1], times[i - 1][0] + 0.15))
words = [{"text": w, "start": round(a, 3), "end": round(b, 3), "scene": sid} for (w, sid), (a, b) in zip(script, times)]
ids = list(TX)
segs = []
for k, sid in enumerate(ids):
    a = 0.0 if k == 0 else round(next(w for w in words if w["scene"] == sid)["start"] - 0.12, 3)
    segs.append({"id": sid, "start": a})
for k in range(len(segs)):
    segs[k]["end"] = segs[k + 1]["start"] if k + 1 < len(segs) else round(dur, 3)
json.dump(words, open(f"{A}/words.json", "w"), ensure_ascii=False, indent=0)
json.dump(segs, open(f"{A}/segments.json", "w"), indent=1)
print(f"Gesamt {dur:.2f}s · {len(words)} Wörter · Übereinstimmung {sm.ratio()*100:.0f}%")
for s in segs:
    print(f"  {s['id']:<14} {s['start']:6.2f} → {s['end']:6.2f}")
