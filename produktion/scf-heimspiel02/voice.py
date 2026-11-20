"""Sprecherspur aus Arthur-Stücken zusammensetzen, Pausen kürzen, Tempo, Studio-Kette; Wortzeiten per Whisper.
Stücke: Hook „Der zweite Heimspieltag …“, Haupttake, „David Kandra“ (neu, deutsch), neuer Schluss.
Ausgabe: assets/voice.wav, assets/words.json, assets/segments.json · Aufruf: HF_HUB_DISABLE_XET=1 python3 voice.py"""
import difflib, json, re, subprocess
import numpy as np, librosa, soundfile as sf

A = "assets"; SR = 48000
TEMPO, MAXP, HEAD, TAIL = 1.07, 0.28, 0.12, 2.6
TX = json.load(open("texts.json"))
T1 = f"{A}/arthur/voice_take1.mp3"
# (Datei, von, bis) in Sekunden der Quelle (None = ganze Datei, Ränder werden gekappt), danach Pause in s (vor Tempo)
PIECES = [
    (f"{A}/arthur/hook_b.mp3", None, None, 0.40),       # „Der zweite Heimspieltag in der Squash-Bundesliga!“
    (T1, 3.25, 7.60, 0.38),     # Der SCF Nürnberg empfängt den TSC Heuchelhof.
    (T1, 8.22, 11.12, 0.55),    # Das ist unser Team für den zweiten Heimspieltag:
    (T1, 11.64, 13.05, 0.75),   # Johannes Thürauf.
    (T1, 13.60, 14.84, 0.75),   # Edwin Clain.
    (f"{A}/arthur/kandra_a.mp3", None, None, 0.75),   # David Kandra. (deutsch, neu)
    (T1, 17.26, 18.58, 0.50),   # Und Armin Hameed.
    (T1, 19.37, 21.22, 0.30),   # Heuchelhof hat nachgelegt:
    (T1, 21.79, 25.76, 0.32),   # Neuzugang Dimitri Steinmann ist die Nummer 21 der Welt.
    (T1, 26.36, 28.72, 0.45),   # Das Ziel: die Playoffs.
    (T1, 29.52, 32.04, 0.42),   # Aber das letzte Duell im Sportpark Nord?
    (T1, 32.68, 34.17, 0.45),   # Vier zu null für uns.
    (T1, 34.78, 38.99, 0.30),   # Samstag, 28. November, 13 Uhr.
    (T1, 39.68, 41.11, 0.26),   # Einlass ab zwölf,
    (T1, 41.37, 42.45, 0.45),   # Eintritt frei.
    (f"{A}/arthur/ende_a.mp3", 0.0, 11.0, 0.0),        # Kommt in den Sportpark Nord, … euer Sportpark Nord. (ohne „ciao“)
]


def piece(path, a, b):
    y, _ = librosa.load(path, sr=SR, mono=True)
    if a is not None:
        y = y[int(a * SR):int(b * SR)]
    iv = librosa.effects.split(y, top_db=42, frame_length=1024, hop_length=128)
    out = [y[max(iv[0][0] - int(0.02 * SR), 0):iv[0][0]]]
    for k, (s, e) in enumerate(iv):
        if k:
            out.append(np.zeros(min(s - iv[k - 1][1], int(MAXP * SR)), np.float32))
        out.append(y[s:e])
    out.append(y[iv[-1][1]:iv[-1][1] + int(0.05 * SR)])
    z = np.concatenate(out)
    f = int(0.006 * SR); z[:f] *= np.linspace(0, 1, f); z[-f:] *= np.linspace(1, 0, f)
    return z / (np.sqrt(np.mean(z[np.abs(z) > 0.02] ** 2)) + 1e-9) * 0.12   # Stücke auf gleiche Lautheit


chunks = []
for path, a, b, gap in PIECES:
    z = piece(path, a, b)
    if gap < 0 and chunks:  # Überblendung (nahtlos): kurzes Crossfade mit dem Ende des vorherigen Stücks
        n = int(-gap * SR)
        chunks.append(z)
        prev = chunks[-2]
        xf = np.linspace(0, 1, n)
        prev[-n:] = prev[-n:] * (1 - xf) + z[:n] * xf
        chunks[-1] = z[n:]
    else:
        chunks.append(z)
        chunks.append(np.zeros(int(max(gap, 0) * SR), np.float32))
sf.write(f"{A}/_in.wav", np.concatenate(chunks), SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{A}/_in.wav", "-af",
                f"rubberband=tempo={TEMPO}:pitch=1:formant=preserved:transients=smooth,"
                f"adelay={int(HEAD*1000)},apad=pad_dur={TAIL},"
                "highpass=f=60,equalizer=f=120:t=q:w=1.2:g=2,deesser=i=0.3,"
                "acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150:makeup=1.5,loudnorm=I=-16:TP=-1.5:LRA=7",
                "-ar", str(SR), "-ac", "1", f"{A}/voice.wav"], check=True)
subprocess.run(["rm", "-f", f"{A}/_in.wav"])
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{A}/voice.wav"]))

# ---- Wortzeiten: Whisper, an Skriptwörter angeglichen und an echte Einsätze gerückt
PROMPT = "Heimspieltag, SCF Nürnberg, TSC Heuchelhof, Johannes Thürauf, Edwin Clain, David Kandra, Armin Hameed, Dimitri Steinmann, Glascourt"
ALIAS = {"klain": "clain", "daphid": "david", "dafid": "david", "kandre": "kandra", "hamid": "hameed", "glaskurt": "glascourt", "tschau": "ciao"}
from faster_whisper import WhisperModel  # noqa: E402
y16, _ = librosa.load(f"{A}/voice.wav", sr=16000)
wh = [w for s in WhisperModel("small", device="cpu", compute_type="int8").transcribe(y16, language="de", word_timestamps=True, initial_prompt=PROMPT)[0] for w in s.words]
print("Whisper:", " ".join(w.word.strip() for w in wh))
norm = lambda x: re.sub(r"[^\wäöüß]", "", x.lower())  # noqa: E731
script = [(w, sid) for sid, txt in TX.items() for w in txt.split()]
sm = difflib.SequenceMatcher(a=[norm(w) for w, _ in script], b=[ALIAS.get(norm(w.word), norm(w.word)) for w in wh], autojunk=False)
times = [None] * len(script)
for b in sm.get_matching_blocks():
    for k in range(b.size):
        times[b.a + k] = (wh[b.b + k].start, wh[b.b + k].end)
for i in range(len(script)):
    if times[i] is None:
        prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), HEAD)
        nxt = next((times[j][0] for j in range(i + 1, len(script)) if times[j]), prev + 0.4)
        times[i] = (prev + 0.02, max(prev + 0.12, nxt - 0.02))
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
        # erster Einsatz nach einer echten Pause (≥ 0,3 s), nicht nach einer Mikro-Lücke im selben Wort
        c = next((on[j][0] for j in range(1, len(on)) if blk and on[j][0] >= blk[1] and on[j][0] - on[j - 1][1] >= 0.3), None)
        if c is not None and abs(c - a) < 1.0:
            a = c
    elif not any(x <= a < y_ for x, y_ in on):
        a = next((x for x in starts_on if x > a), a)
    times[i] = (a, max(b, a + 0.1))
for i in range(1, len(times)):
    if times[i][0] < times[i - 1][0] + 0.05:
        times[i] = (times[i - 1][0] + 0.05, max(times[i][1], times[i - 1][0] + 0.15))
words = [{"text": w, "start": round(a, 3), "end": round(b, 3), "scene": sid} for (w, sid), (a, b) in zip(script, times)]
segs = []
for k, sid in enumerate(TX):
    a = 0.0 if k == 0 else round(next(w for w in words if w["scene"] == sid)["start"] - 0.12, 3)
    segs.append({"id": sid, "start": a})
for k in range(len(segs)):
    segs[k]["end"] = segs[k + 1]["start"] if k + 1 < len(segs) else round(dur, 3)
json.dump(words, open(f"{A}/words.json", "w"), ensure_ascii=False, indent=0)
json.dump(segs, open(f"{A}/segments.json", "w"), indent=1)
print(f"Gesamt {dur:.2f}s · {len(words)} Wörter · Übereinstimmung {sm.ratio()*100:.0f}%")
for s in segs:
    print(f"  {s['id']:<14} {s['start']:6.2f} → {s['end']:6.2f}")
