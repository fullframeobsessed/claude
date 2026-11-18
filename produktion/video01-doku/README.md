# Video 01 (Doku-Fassung): „Warum du alles aufschiebst (und es NICHTS mit Faulheit zu tun hat)“

**Länge:** 7:19 Min. · 1920×1080 · 30 fps · Kinobalken 2,35:1
**Erzähler:** „Arthur“ (ElevenLabs über Higgsfield), Studio-Bearbeitung, −16 LUFS Sprecherspur
**Look:** dunkle Räume mit Lichtkegeln, alter Film (Staub im Licht, Fussel, Kratzer, Flackern, Korn, Vignette, warmer Ton)

## Dateien
| Datei | Wofür |
|---|---|
| `otto_video01_mit_untertiteln.mp4` | Fertiges Video, Untertitel im unteren Kinobalken |
| `otto_video01_ohne_untertitel.mp4` | Für Final Cut (Stimme drin, keine Untertitel) |
| `untertitel_video01.srt` | Untertitel für Final Cut (`Ablage › Importieren › Untertitel`) oder YouTube |
| `assets/voice.wav` | Sprecherspur einzeln (wird lokal erzeugt, nicht im Repo) |
| `assets/arthur/*.mp3` | Die 23 Original-Aufnahmen von Arthur |

## In Final Cut fertigstellen
1. Projekt 1080p, **30p**, Stereo 48 kHz anlegen und `otto_video01_ohne_untertitel.mp4` importieren.
2. Untertitel: `Ablage › Importieren › Untertitel…` → `untertitel_video01.srt`.
3. **Musik (wichtig für den Doku-Effekt):** ruhiger, dunkler Klangteppich (Suchbegriffe „ambient“, „cinematic“, „documentary“), etwa 20–24 dB unter der Stimme. Bei den Kapitelkarten darf die Musik kurz aufgehen.
4. Optional Geräusche: leises Projektorrattern unter dem Kaltstart, ein tiefer „Boom“ auf „FAUL?“ und auf den Kapitelkarten.

## YouTube-Beschreibung (Vorschlag)
```
Du schiebst alles auf und hältst dich für faul? Die Forschung sagt: Du bist es nicht.
In dieser Folge erfährst du, warum dein Gehirn dich vor schlechten Gefühlen „schützt“,
warum du dein zukünftiges Ich wie einen Fremden behandelst – und welche 4 einfachen
Werkzeuge wirklich helfen.

0:00 Otto hat genau eine Aufgabe
0:53 Kapitel 1: Du bist nicht faul
2:06 Kapitel 2: Der Kampf im Kopf
3:21 Kapitel 3: Der Fremde
4:21 Kapitel 4: Der Teufelskreis
5:09 Kapitel 5: Der Ausweg
6:42 Otto ist nicht faul

Quellen
– Steel, P. (2007). The nature of procrastination. Psychological Bulletin, 133(1), 65–94.
– Sirois, F. & Pychyl, T. (2013). Procrastination and the priority of short-term mood regulation. Social and Personality Psychology Compass, 7(2), 115–127.
– Schlüter, C. et al. (2018). The structural and functional signature of action control. Psychological Science, 29(10), 1620–1630.
– Hershfield, H. E. et al. (2009). Neural correlates of self-continuity and its relation to temporal discounting. Social Cognitive and Affective Neuroscience, 4(1), 85–92.
– Wohl, M. J. A., Pychyl, T. A. & Bennett, S. H. (2010). I forgive myself, now I can study. Personality and Individual Differences, 48(7), 803–808.

Erzählstimme: KI-generiert.
```
> Hinweis: Viele Plattformen (auch YouTube) verlangen eine Kennzeichnung realistisch wirkender KI-Inhalte. Eine KI-Stimme bei einem Cartoon ist meist unkritisch, die Zeile „Erzählstimme: KI-generiert“ ist trotzdem eine saubere Lösung.

## Neu bauen
```bash
HF_HUB_DISABLE_XET=1 python3 voice_arthur.py   # Sprecherspur + Wort-Zeiten (aus assets/arthur/*.mp3)
python3 gen.py                                  # Szenen, Untertitel, SRT
./render_all.sh                                 # beide Videos rendern (~40 Min.)
```
Dateien: `gen.py` (Hook bis Kapitel 1, Kapitelkarten, Untertitel), `rest.py` (Szenen 9–34), `film.py` (Alter-Film-Effekte).
