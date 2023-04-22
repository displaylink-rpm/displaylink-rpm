#!/bin/bash
file=$1

startline=$(grep -n "create_pm_script()" "$file" | cut -d: -f1 | head -1)
endline=$(grep -n 'chmod 0755 /etc/zzz.d/resume/displaylink.sh' "$file" | cut -d: -f1 | head -1)

source <(
	tail -n +$startline $file | head -n +$(($endline - $startline + 5))
)
COREDIR=$(mktemp -d)
create_pm_script "systemd" "$COREDIR"

sed -i -e '1 s/^.*$/\#!\/usr\/bin\/bash/' "$COREDIR/suspend.sh"

cat "$COREDIR/suspend.sh"

rm -rf "$COREDIR"
