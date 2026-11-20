# SCF Nürnberg: Reel „Frankenderby“ (2. Heimspieltag, 28.11.2026)

Instagram-Reel (1080×1920, 30 fps, ca. 43 s) für das Squash-Bundesliga-Heimspiel **SCF Nürnberg vs. TSC Heuchelhof**,
Sa 28.11.2026, 13:00 Uhr, Sportpark Nord Nürnberg. Skript und Faktencheck: [`SKRIPT.md`](SKRIPT.md).

**Ergebnis:** `scf_heimspiel02_reel.mp4` (−14 LUFS, Stimme „Arthur“, Musik, Effekte, eingebrannte Untertitel)

## Bausteine
| Datei | Inhalt |
|---|---|
| `assets/src/` | Originalfotos, Logos, Flyer (PDF) |
| `assets/cut/<name>_raw.png` | Freistellung von Higgsfield (enthielt teils den Gegner) |
| `assets/cut/<name>.png` | Nur der SCF-Spieler mit Schläger (Gegner per SAM entfernt, `tools/sam_cut.py`) |
| `assets/sticker_<name>.png` | Papier-Ausschnitt-Look mit weißem Schnittrand und Schatten (`tools/sticker.py`) |
| `assets/logo_scf.png`, `assets/logo_tsc.png` | Runde Logo-Badges |
| `assets/arthur/voice_take1.mp3` | Sprachaufnahme Arthur (ElevenLabs über Higgsfield) |
| `assets/music.mp3` | Musik (ElevenLabs Music, instrumental, 129 BPM) |
| `assets/sfx/` | Klick, Plop, Tick, Boom, Glocke, Kamera-Auslöser (synthetisch) |

## Ablauf
```bash
HF_HUB_DISABLE_XET=1 python3 voice.py   # Sprecherspur kürzen/tempo + Wortzeiten (assets/words.json, segments.json)
./render.sh                              # gen.py → mix.py → HyperFrames-Render → Ton anlegen
```
Szenen, Mauszeiger-Weg, Untertitel und Soundeffekte stehen alle in `gen.py` (Positionen in px, Zeiten an gesprochene Wörter gekoppelt).

## Hinweise
- Armin Hameed ist ab Oberschenkel weich ausgeblendet: Auf dem Foto überkreuzen sich seine Beine mit denen des Gegners.
- Text liegt in der Instagram-Sicherheitszone (y 270–1248 px, x 65–1015 px); darunter nur Spieler/Deko.
