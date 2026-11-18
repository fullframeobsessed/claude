#!/bin/bash
# Rendert Video 01 (Doku) mit und ohne eingebrannte Untertitel.
set -e
cd "$(dirname "$0")"
CLI=/root/.claude/skills/hyperframes/scripts/plugin-cli.mjs
python3 gen.py
node $CLI render > render_cap.log 2>&1
cp "$(ls -t renders/*.mp4 | head -1)" otto_video01_mit_untertiteln.mp4
python3 gen.py --nocap
node $CLI render > render_nocap.log 2>&1
cp "$(ls -t renders/*.mp4 | head -1)" otto_video01_ohne_untertitel.mp4
python3 gen.py
echo FERTIG
