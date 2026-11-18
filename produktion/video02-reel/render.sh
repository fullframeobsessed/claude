#!/bin/bash
set -e
cd "$(dirname "$0")"
CLI=/root/.claude/skills/hyperframes/scripts/plugin-cli.mjs
python3 gen.py
node $CLI render > render.log 2>&1
cp "$(ls -t renders/*.mp4 | head -1)" video_stumm.mp4
python3 mix.py
echo FERTIG
