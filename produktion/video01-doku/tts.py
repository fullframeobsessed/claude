"""Erzählerstimme für die Doku-Probe: Piper Thorsten (high), tiefer + Studio-Kette, Wort-Zeiten per Whisper.

Ausgabe: assets/voice.wav, assets/words.json, assets/segments.json
Aufruf:  HF_HUB_DISABLE_XET=1 python3 tts.py [--pitch -5 --speed 1.2]
"""
import argparse, difflib, io, json, os, re, subprocess, sys, wave
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "video01"))
import scenes  # noqa: E402
from piper import PiperVoice  # noqa: E402
from piper.config import SynthesisConfig  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--model", default="/home/user/tts/hq/de_DE-thorsten-high.onnx")
ap.add_argument("--speaker", type=int, default=None)
ap.add_argument("--speed", type=float, default=1.2)
ap.add_argument("--pitch", type=float, default=-5.0)
args = ap.parse_args()

HERE = os.path.dirname(os.path.abspath(__file__))
A = f"{HERE}/assets"
SAY = {"wird's": "wird es"}
# Ablauf: stille Doku-Elemente zwischen den Sprecher-Szenen
PLAN = [("open", 3.4), "s01_hook", ("title", 3.2), "s02_bad", "s03_socken", "s04_pinguine",
        "s05_faul", "s06_nicht_faul", "s07_versprechen", ("chapter", 3.2)]
P_SENT, P_LINE, P_TAIL = 0.32, 0.5, 0.55

voice = PiperVoice.load(args.model)
cfg = SynthesisConfig(speaker_id=args.speaker, length_scale=args.speed, noise_scale=0.55, noise_w_scale=0.6)
by_id = {s["id"]: s for s in scenes.SCENES}


def synth(t):
    for a, b in SAY.items():
        t = t.replace(a, b)
    t = t.replace("„", "").replace("“", "")
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        voice.synthesize_wav(t, w, syn_config=cfg)
    buf.seek(0)
    with wave.open(buf, "rb") as r:
        sr = r.getframerate()
        a = np.frombuffer(r.readframes(r.getnframes()), np.int16)
    # Rand-Stille kappen, interne Pausen auf 0,22 s begrenzen
    hop = sr // 100
    n = len(a) // hop
    rms = np.sqrt(np.mean(a[: n * hop].astype(np.float32).reshape(n, hop) ** 2, axis=1)) + 1e-6
    loud = 20 * np.log10(rms) > 20 * np.log10(rms.max()) - 40
    idx = np.flatnonzero(loud)
    first, last = max(idx[0] - 3, 0), min(idx[-1] + 4, n)
    out, i = [], first
    while i < last:
        if loud[i]:
            out.append(a[i * hop:(i + 1) * hop]); i += 1
        else:
            j = i
            while j < last and not loud[j]:
                j += 1
            out.append(a[i * hop:(i + min(j - i, 22)) * hop]); i = j
    return np.concatenate(out), sr


audio, segs, sents, t, sr = [], [], [], 0.0, None
for item in PLAN:
    if isinstance(item, tuple):
        name, d = item
        segs.append({"id": name, "start": round(t, 3), "end": round(t + d, 3)})
        audio.append(("sil", d)); t += d
        continue
    sc = by_id[item]
    start = t
    for li, line in enumerate(sc["lines"]):
        ss = [s for s in re.split(r"(?<=[.!?…])\s+(?=[A-ZÄÖÜ„])", line) if s]
        for si, s in enumerate(ss):
            a, sr = synth(s)
            sents.append({"text": s, "start": t, "end": t + len(a) / sr})
            audio.append(("pcm", a)); t += len(a) / sr
            gap = P_SENT if si < len(ss) - 1 else (P_LINE if li < len(sc["lines"]) - 1 else P_TAIL)
            audio.append(("sil", gap)); t += gap
    segs.append({"id": item, "start": round(start, 3), "end": round(t, 3)})

pcm = np.concatenate([x if k == "pcm" else np.zeros(int(round(x * sr)), np.int16) for k, x in audio])
with wave.open(f"{A}/voice_raw.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())
STUDIO = ("highpass=f=55,lowpass=f=11500,equalizer=f=110:t=q:w=1.2:g=3,equalizer=f=300:t=q:w=1:g=-2,"
          "equalizer=f=3200:t=q:w=1.5:g=2,deesser=i=0.4,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,"
          "loudnorm=I=-16:TP=-1.5:LRA=7")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{A}/voice_raw.wav", "-af",
                f"aresample=48000,rubberband=pitch={2 ** (args.pitch / 12):.4f}:formant=preserved,{STUDIO}",
                "-ar", "48000", "-ac", "1", f"{A}/voice.wav"], check=True)

# ---- Wort-Zeiten: Skript-Wörter auf Whisper-Wörter ausrichten (Position, nicht Text)
import librosa  # noqa: E402
from faster_whisper import WhisperModel  # noqa: E402
y, _ = librosa.load(f"{A}/voice.wav", sr=16000)
model = WhisperModel("small", device="cpu", compute_type="int8")
wh = [w for s in model.transcribe(y, language="de", word_timestamps=True)[0] for w in s.words]
norm = lambda x: re.sub(r"[^\wäöüß]", "", x.lower())  # noqa: E731
script = [(w, s) for s in sents for w in s["text"].split()]
sm = difflib.SequenceMatcher(a=[norm(w) for w, _ in script], b=[norm(w.word) for w in wh], autojunk=False)
times = [None] * len(script)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        ww = wh[blk.b + k]
        times[blk.a + k] = (ww.start, ww.end)
words = []
for i, (w, s) in enumerate(script):
    if times[i] is None:  # nicht erkannt: innerhalb des Satzes proportional schätzen
        sw = s["text"].split(); j = sw.index(w) if w in sw else 0
        dur = s["end"] - s["start"]; a = s["start"] + dur * j / len(sw); times[i] = (a, a + dur / len(sw))
    words.append({"text": w, "start": round(times[i][0], 3), "end": round(times[i][1], 3)})
for i in range(1, len(words)):  # monoton machen
    words[i]["start"] = max(words[i]["start"], words[i - 1]["start"] + 0.02)
matched = sum(x is not None for x in times)
json.dump(words, open(f"{A}/words.json", "w"), ensure_ascii=False, indent=0)
json.dump(segs, open(f"{A}/segments.json", "w"), indent=1)
print(f"Gesamt {t:.2f}s · {len(words)} Wörter · {sm.ratio()*100:.0f}% Übereinstimmung mit Whisper")
for s in segs:
    print(f"  {s['id']:<18} {s['start']:6.2f} → {s['end']:6.2f}")
