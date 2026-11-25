#!/bin/bash
# render.sh <dir-with-svgs>
D="$1"; cd "$D" || exit 1
for f in *.svg; do n="${f%.svg}"; P=$(cygpath -m "$PWD")
"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless=new --disable-gpu --hide-scrollbars --window-size=1320,800 --screenshot="$P/$n.png" "file:///$P/$f" >/dev/null 2>&1
done
ls *.png
