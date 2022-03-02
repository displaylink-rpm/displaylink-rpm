#!/bin/bash
file=$1

startline=$(grep -n "add_pm_script()" "$file" | cut -d: -f1 | head -1)
endline=$(grep -n 'chmod 0755 /etc/zzz.d/resume/displaylink.sh' "$file" | cut -d: -f1 | head -1)

source <(
	tail -n +$startline $file | head -n +$(($endline - $startline + 4))
)
COREDIR=$(mktemp -d)
add_pm_script "systemd"

sed -i -e '1 s/^.*$/\#!\/usr\/bin\/bash/' "$COREDIR/suspend.sh"

cat "$COREDIR/suspend.sh"

rm -rf "$COREDIR"
