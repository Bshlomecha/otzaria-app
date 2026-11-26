#!/bin/bash
# render.sh <dir-with-html>  —  כל דף HTML לתמונה 1440x900 (Edge headless).
# 01-three-modes נבנה מן התמונות האחרות, ולכן הוא אחרון.
D="$1"; cd "$D" || exit 1
P=$(cygpath -m "$PWD")
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
shot() { "$EDGE" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1440,900 --virtual-time-budget=3000 --screenshot="$P/$1.png" "file:///$P/$1.html" >/dev/null 2>&1; }
for f in [0-9]*.html; do n="${f%.html}"; [ "$n" = "01-three-modes" ] && continue; shot "$n"; done
shot 01-three-modes
ls *.png
