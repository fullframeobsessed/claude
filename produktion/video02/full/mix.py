"""Tonmischung Video 02 (Test): Stimme + Musik aus Video 01 (Ducking) + Soundeffekte aus assets/sfx.json."""
import json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
A = f"{HERE}/assets"
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{A}/voice.wav"]))
sfx = json.load(open(f"{A}/sfx.json"))

# Effekte vorbereiten: Stille am Anfang weg, Spitze auf -3 dBFS
for name in sorted({s["f"] for s in sfx}):
    src = f"{A}/sfx/{name}.mp3"
    det = subprocess.run(["ffmpeg", "-i", src, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    peak = float(re.search(r"max_volume: ([-\d.]+) dB", det).group(1))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af",
                    f"silenceremove=start_periods=1:start_threshold=-60dB,volume={-3 - peak:.1f}dB,aresample=48000",
                    "-ac", "2", f"{A}/_{name}.wav"], check=True)

inp, flt = [], []
for i, s in enumerate(sfx):
    inp += ["-i", f"{A}/_{s['f']}.wav"]
    ms = int(s["t"] * 1000)
    flt.append(f"[{i}:a]volume={s['g']},adelay={ms}|{ms}[e{i}]")
flt.append("".join(f"[e{i}]" for i in range(len(sfx))) + f"amix=inputs={len(sfx)}:normalize=0,apad=whole_dur={dur}[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[out]", "-t", str(dur),
                "-ar", "48000", "-ac", "2", f"{A}/sfx_spur.wav"], check=True)

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{A}/music.mp3", "-af",
                f"atrim=0:{dur},afade=t=in:st=0:d=1.5,afade=t=out:st={dur - 3}:d=3,loudnorm=I=-24:TP=-3,aresample=48000",
                "-ac", "2", f"{A}/musik_bett.wav"], check=True)
fc = ("[0:a]aformat=channel_layouts=stereo,asplit=2[vo][sc];[1:a]volume=0.55[mu];"
      "[mu][sc]sidechaincompress=threshold=0.02:ratio=5:attack=25:release=450:makeup=1[duck];"
      "[2:a]volume=0.5[fx];[vo][duck][fx]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{A}/voice.wav", "-i", f"{A}/musik_bett.wav", "-i", f"{A}/sfx_spur.wav",
                "-filter_complex", fc, "-map", "[out]", "-ar", "48000", f"{A}/mix.wav"], check=True)
for SRCV, DST in [(f"{HERE}/video_cap_stumm.mp4", f"{HERE}/otto_video02_mit_untertiteln.mp4"), (f"{HERE}/video_nocap_stumm.mp4", f"{HERE}/otto_video02_ohne_untertitel.mp4")]:
    if os.path.exists(SRCV):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRCV, "-i", f"{A}/mix.wav", "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", DST], check=True)
for name in {s["f"] for s in sfx}:
    os.remove(f"{A}/_{name}.wav")
print(f"{len(sfx)} Effekte gemischt")
