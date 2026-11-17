# Video 01: Rohschnitt mit Stimme und Untertiteln

**„Warum du alles aufschiebst (und es NICHTS mit Faulheit zu tun hat)“**
Länge: **6:05 Min.** · 1080p · 25 fps · Stimme: Piper „Thorsten“ (Open Source, offline erzeugt)

## Dateien (`out/`)
| Datei | Wofür |
|---|---|
| `video01_mit_untertiteln.mp4` | **Vorschau** zum Anschauen, Untertitel eingebrannt |
| `video01_ohne_untertitel.mp4` | **Für Final Cut:** Bild + Stimme, ohne Untertitel |
| `voiceover_video01.wav` | Sprecherspur einzeln (48 kHz, 24 Bit, auf -16 LUFS normalisiert) |
| `untertitel_video01.srt` | Untertitel als Datei, auch für den YouTube-Upload |
| `kapitel.txt` | Kapitelmarken mit echten Zeiten, für die YouTube-Beschreibung |
| `frames/*.png` | Alle 34 Szenenbilder einzeln (1920×1080) |
| `stimmproben_alle_6.m4a` | Alle 6 verfügbaren deutschen Stimmen zum Vergleich |

> Die großen Video- und Audiodateien liegen nicht im Git-Repo, sondern nur lokal in `out/`. Mit `python3 build.py` lassen sie sich jederzeit neu bauen.

## Import in Final Cut Pro
1. **Neues Projekt:** 1080p HD, 25p, Stereo 48 kHz.
2. **Video importieren:** `Ablage › Importieren › Medien…` → `video01_ohne_untertitel.mp4`
3. **Untertitel importieren:** `Ablage › Importieren › Untertitel…` → `untertitel_video01.srt`
   Die Untertitel landen als eigene Rolle „SRT“ in der Timeline. Stil, Größe und Position passt du im Untertitel-Inspektor an.
4. **Musik:** leichte, verspielte Hintergrundmusik etwa 18–22 dB unter der Stimme. Bei der Stimme lässt sich in FCP „Ducking“ per Audio-Inspektor einstellen.
5. **Szenen tauschen:** Willst du eine Szene durch das KI-Otto-Bild oder eine Animation ersetzen, findest du die passenden Zeiten in `out/timeline.json`.
6. **Export:** `Bereitstellen › Datei exportieren`, H.264, für YouTube. Die SRT-Datei separat bei YouTube hochladen (dann sind die Untertitel ein- und ausschaltbar).

## Neu bauen / ändern
```bash
python3 build.py                      # Standard: Stimme thorsten, Tempo 1.2
python3 build.py --voice karlsson     # andere Stimme
python3 build.py --speed 1.3          # langsamer sprechen
```
- **Text ändern:** in `scenes.py`. Jede Zeile in `lines` ist ein Untertitel-Block.
- **Aussprache korrigieren:** im Wörterbuch `SAY` in `build.py`.
- **Kanalname im Abspann:** Variable `CHANNEL` in `scenes.py`.

## Ehrliche Einordnung
- **Stimme:** Thorsten ist eine gute kostenlose Stimme, aber hörbar synthetisch (16 kHz, „low“-Qualität). Für den echten Upload empfehle ich deine eigene Stimme oder eine Premium-KI-Stimme (z. B. über Higgsfield, sobald Credits da sind). Das Timing passt sich automatisch an, wenn die Stimme neu erzeugt wird.
- **Bilder:** Das sind meine Vektor-Zeichnungen von Otto, noch nicht der KI-Otto. Die Bewegung ist ein langsamer Zoom pro Szene, also ein **Animatic/Rohschnitt** und noch keine volle Animation.
