"""Saubere, rauschfreie Soundeffekte per Synthese (ersetzen die verrauschten KI-Effekte pop/tick/typing).
Aufruf: python3 synth.py <zielordner>  ->  pop.mp3, tick.mp3, typing.mp3
"""
import subprocess, sys, numpy as np, soundfile as sf

SR = 48000
out = sys.argv[1]
rng = np.random.default_rng(7)


def t_(d):
    return np.arange(int(d * SR)) / SR


def plop(d=0.22):
    t = t_(d)
    f = 260 + 900 * np.exp(-t / 0.018)                 # schneller Tonhöhen-Abfall = „Plop“
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = (1 - np.exp(-t / 0.0015)) * np.exp(-t / 0.045)
    return env * (np.sin(ph) + 0.25 * np.sin(2 * ph))


def tick(f0):
    t = t_(0.05)
    env = (1 - np.exp(-t / 0.0004)) * np.exp(-t / 0.006)
    return env * (np.sin(2 * np.pi * f0 * t) + 0.5 * np.sin(2 * np.pi * f0 * 1.7 * t))


def key():
    t = t_(0.05)
    f = rng.uniform(1800, 3200)
    hi = np.exp(-t / 0.004) * np.sin(2 * np.pi * f * t)
    lo = np.exp(-t / 0.012) * np.sin(2 * np.pi * rng.uniform(160, 240) * t)
    return (1 - np.exp(-t / 0.0005)) * (0.6 * hi + 0.8 * lo) * rng.uniform(0.6, 1.0)


def place(total, events):
    y = np.zeros(int(total * SR))
    for at, s in events:
        i = int(at * SR); y[i:i + len(s)] += s[:len(y) - i]
    return y


def save(name, y):
    y = y / np.abs(y).max() * 0.7
    sf.write(f"{out}/_{name}.wav", y.astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{out}/_{name}.wav", "-b:a", "192k", f"{out}/{name}.mp3"], check=True)
    subprocess.run(["rm", f"{out}/_{name}.wav"])


save("pop", plop())
save("tick", place(4.2, [(i * 1.0, tick(2600 if i % 2 == 0 else 2100)) for i in range(5)]))
ev, at = [], 0.0
while at < 2.9:
    ev.append((at, key())); at += rng.uniform(0.07, 0.17)
save("typing", place(3.0, ev))
print("pop, tick, typing neu erzeugt in", out)
