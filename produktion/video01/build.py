"""Baut Video 01: TTS-Sprecher (Piper), SRT-Untertitel, Szenen-Clips mit Zoom, Endvideos.

Aufruf:  python3 build.py [--voice thorsten] [--speed 1.0]
Voraussetzungen: pip install piper-tts numpy · ffmpeg · node + playwright · Stimmen in /home/user/tts/voices
"""
import argparse, io, os, re, subprocess, wave, json
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from piper import PiperVoice
from piper.config import SynthesisConfig
import scenes

ap = argparse.ArgumentParser()
ap.add_argument("--voice", default="thorsten")
ap.add_argument("--speed", type=float, default=1.55, help="length_scale: <1 = schneller")
ap.add_argument("--pitch", type=float, default=-2.0, help="Tonhöhe in Halbtönen (negativ = tiefer)")
ap.add_argument("--pauses", type=float, default=0.6, help="Faktor für alle Pausen")
ap.add_argument("--fps", type=int, default=25)
args = ap.parse_args()

OUT = "out"
FR = f"{OUT}/frames"
CL = f"{OUT}/clips"
os.makedirs(FR, exist_ok=True); os.makedirs(CL, exist_ok=True)

# Aussprache-Hilfen nur für die Stimme (Untertitel bleiben korrekt geschrieben)
SAY = {"Pychyl": "Pitschel", "Hershfield": "Hörschfield", "Sirois": "Siroa", "Piers Steel": "Piers Stiel",
       "Hal ": "Häl ", "wird's": "wird es", "Fuschia": "Fuschia", "95 Prozent": "fünfundneunzig Prozent",
       "Zehn-Minuten-Deal": "Zehn-Minuten-Diehl", "Deal": "Diehl", "Shannon": "Schännon", "Bennett": "Bennett",
       "Morgen-Otto": "Morgen Otto", "Übermorgen-Otto": "Übermorgen Otto", "Ruhr-Universität": "Ruhr Universität"}
P_SENT, P_LINE, P_LEAD, P_TAIL = (x * args.pauses for x in (0.38, 0.6, 0.3, 0.7))
MAXC = 80   # max. Zeichen pro Untertitel-Block (2 Zeilen à ~40)

voice = PiperVoice.load(f"/home/user/tts/voices/voice-de-{args.voice}-low/de-{args.voice}-low.onnx")
cfg = SynthesisConfig(length_scale=args.speed)


def tts(t):
    for a, b in SAY.items():
        t = t.replace(a, b)
    t = t.replace("„", "").replace("“", "").replace("–", ",")
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        voice.synthesize_wav(t, w, syn_config=cfg)
    buf.seek(0)
    with wave.open(buf, "rb") as r:
        sr = r.getframerate()
        a = np.frombuffer(r.readframes(r.getnframes()), dtype=np.int16)
    return squeeze(a, sr), sr


def squeeze(a, sr, keep=0.16, edge=0.03):
    """Stille am Rand kappen und interne Pausen (z. B. an Kommas) auf `keep` Sekunden kürzen -> flüssiger Redefluss."""
    hop = sr // 100
    n = len(a) // hop
    if n == 0:
        return a
    rms = np.sqrt(np.mean(a[: n * hop].astype(np.float32).reshape(n, hop) ** 2, axis=1)) + 1e-6
    loud = 20 * np.log10(rms) > 20 * np.log10(rms.max()) - 38
    idx = np.flatnonzero(loud)
    if len(idx) == 0:
        return a
    first, last = max(idx[0] - int(edge * 100), 0), min(idx[-1] + int(edge * 100) + 1, n)
    out, i = [], first
    while i < last:
        if loud[i]:
            out.append(a[i * hop:(i + 1) * hop]); i += 1
        else:
            j = i
            while j < last and not loud[j]:
                j += 1
            k = min(j - i, int(keep * 100))
            out.append(a[i * hop:(i + k) * hop]); i = j
    return np.concatenate(out)


def sentences(line):
    return [s for s in re.split(r"(?<=[.!?…])\s+(?=[A-ZÄÖÜ„])", line.strip()) if s]


def chunks(s):
    """Satz in Untertitel-Blöcke <= MAXC teilen, bevorzugt an Komma/Doppelpunkt nahe der Mitte."""
    if len(s) <= MAXC:
        return [s]
    mid = len(s) / 2
    cands = [m.end() for m in re.finditer(r"[,:;]\s", s)] or [m.end() for m in re.finditer(r"\s", s)]
    cut = min(cands, key=lambda i: abs(i - mid))
    return chunks(s[:cut].strip()) + chunks(s[cut:].strip())


def wrap(t, n=42):
    if len(t) <= n:
        return t
    words, best = t.split(), None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        score = max(len(a), len(b))
        if best is None or score < best[0]:
            best = (score, a + "\n" + b)
    return best[1]


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"


# ------------------------------------------------------------- Audio + Cues
audio, cues, timeline = [], [], []
sr = None
t = 0.0
for sc in scenes.SCENES:
    start = t
    if not sc["lines"]:
        sr = sr or 16000
        audio.append(np.zeros(int(sc["silent"] * sr), np.int16)); t += sc["silent"]
    else:
        seg = []
        def add_sil(sec):
            global t
            seg.append(np.zeros(int(round(sec * sr)), np.int16)); t += sec
        a0, sr = tts("Hallo.") if sr is None else (None, sr)
        add_sil(P_LEAD)
        for li, line in enumerate(sc["lines"]):
            ss = sentences(line)
            for si, s in enumerate(ss):
                a, sr = tts(s)
                dur = len(a) / sr
                parts = chunks(s)
                tot = sum(len(p) for p in parts)
                cs = t
                for p in parts:
                    d = dur * len(p) / tot
                    cues.append((cs, cs + d, p)); cs += d
                seg.append(a); t += dur
                if si < len(ss) - 1:
                    add_sil(P_SENT)
            add_sil(P_LINE if li < len(sc["lines"]) - 1 else P_TAIL)
        audio.extend(seg)
    timeline.append((sc["id"], start, t, sc["lines"][0] if sc["lines"] else ""))
    print(f"{sc['id']:<20} {start:7.2f} → {t:7.2f}")

full = np.concatenate(audio)
with wave.open(f"{OUT}/voice_raw.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(full.tobytes())
TOTAL = len(full) / sr
print(f"Gesamtlänge: {TOTAL/60:.2f} min")

# Sprecher-Spur: 48 kHz, leichte EQ, Lautheit für YouTube
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/voice_raw.wav", "-af",
                f"aresample=48000,rubberband=pitch={2 ** (args.pitch / 12):.4f}:formant=preserved,"
                "highpass=f=60,equalizer=f=150:t=q:w=1:g=2,equalizer=f=3000:t=q:w=1:g=2,loudnorm=I=-16:TP=-1.5:LRA=11",
                "-ar", "48000", "-c:a", "pcm_s24le", f"{OUT}/voiceover_video01.wav"], check=True)

with open(f"{OUT}/untertitel_video01.srt", "w", encoding="utf-8") as f:
    for i, (a, b, txt) in enumerate(cues, 1):
        f.write(f"{i}\n{ts(a)} --> {ts(min(b, TOTAL))}\n{wrap(txt)}\n\n")


# Wort-für-Wort-Hervorhebung (ASS) für die Vorschau-Version: aktuelles Wort in Orange
def ats(t):
    cs = int(round(t * 100))
    return f"{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}"


ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Otto,DejaVu Sans,54,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,-1,0,0,0,100,100,0,0,3,10,0,2,80,80,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open(f"{OUT}/untertitel_video01_karaoke.ass", "w", encoding="utf-8") as f:
    f.write(ASS_HEAD)
    for a, b, txt in cues:
        lines2 = wrap(txt).split("\n")
        words = [(li, w) for li, ln in enumerate(lines2) for w in ln.split()]
        weights = [len(w) + 2 for _, w in words]
        tot, t0 = sum(weights), a
        for k, (li, w) in enumerate(words):
            t1 = t0 + (b - a) * weights[k] / tot
            parts, prev = [], 0
            for j, (lj, wj) in enumerate(words):
                if j and lj != prev:
                    parts.append("\\N"); prev = lj
                elif j:
                    parts.append(" ")
                parts.append("{\\c&H1A7AFF&}" + wj + "{\\c&HFFFFFF&}" if j == k else wj)
            f.write(f"Dialogue: 0,{ats(t0)},{ats(min(t1, TOTAL))},Otto,,0,0,0,,{''.join(parts)}\n")
            t0 = t1

# Kapitelmarken (für YouTube-Beschreibung)
caps = {"s01_hook": "Otto hat eine Aufgabe", "s08_kap1": "Du bist nicht faul", "s13_kap2": "Der Kampf im Kopf",
        "s18_kap3": "Dein zukünftiges Ich ist ein Fremder", "s23_kap4": "Der Teufelskreis", "s26_kap5": "Was wirklich hilft"}
with open(f"{OUT}/kapitel.txt", "w", encoding="utf-8") as f:
    for sid, a, b, _ in timeline:
        if sid in caps:
            f.write(f"{int(a//60)}:{int(a%60):02d} {caps[sid]}\n")
json.dump(timeline, open(f"{OUT}/timeline.json", "w"), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ Bilder
for sc in scenes.SCENES:
    open(f"{FR}/{sc['id']}.svg", "w").write(sc["svg"])
subprocess.run(["node", "render.js", FR], check=True)

# ------------------------------------------------------------------- Clips
fps = args.fps
jobs = []
for i, (sid, a, b, _) in enumerate(timeline):
    f0, f1 = round(a * fps), round(b * fps)
    n = f1 - f0
    still = "kap" in sid or sid.startswith("s32") or sid.startswith("s34")
    z = "1" if still else (f"1+0.045*on/{n}" if i % 2 == 0 else f"1.045-0.045*on/{n}")
    vf = (f"scale=3840:2160,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1920x1080:fps={fps},"
          "format=yuv420p")
    jobs.append(["ffmpeg", "-v", "error", "-y", "-i", f"{FR}/{sid}.png", "-vf", vf, "-frames:v", str(n),
                 "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(fps), f"{CL}/{i:02d}_{sid}.mp4"])
with ThreadPoolExecutor(4) as ex:
    list(ex.map(lambda c: subprocess.run(c, check=True), jobs))

with open(f"{CL}/list.txt", "w") as f:
    for i, (sid, *_r) in enumerate(timeline):
        f.write(f"file '{i:02d}_{sid}.mp4'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{CL}/list.txt", "-c", "copy", f"{OUT}/video_stumm.mp4"], check=True)

# Clean-Version (für Final Cut) + Vorschau mit eingebrannten Untertiteln
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/video_stumm.mp4", "-i", f"{OUT}/voiceover_video01.wav",
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                f"{OUT}/video01_ohne_untertitel.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/video01_ohne_untertitel.mp4",
                "-vf", f"ass={OUT}/untertitel_video01_karaoke.ass",
                "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-c:a", "copy",
                f"{OUT}/video01_mit_untertiteln.mp4"], check=True)
print("fertig")
