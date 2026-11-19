#!/bin/bash
set -e
cd "$(dirname "$0")"
CLI=/root/.claude/skills/hyperframes/scripts/plugin-cli.mjs
python3 gen.py
node $CLI render > render_cap.log 2>&1
cp "$(ls -t renders/*.mp4 | head -1)" video_cap_stumm.mp4
python3 gen.py --nocap
node $CLI render > render_nocap.log 2>&1
cp "$(ls -t renders/*.mp4 | head -1)" video_nocap_stumm.mp4
python3 gen.py
python3 mix.py
echo FERTIG
