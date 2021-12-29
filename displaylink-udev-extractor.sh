#!/bin/bash
file=$1

# Get systemd_start_stop_functions()
startline=$(grep -n "systemd_start_stop_functions()" "$file" | cut -d: -f1 | head -1)
endline=$(grep -m2 -n "^EOF$" "$file" | tail -n1 | cut -d: -f1 | head -1)

source <(
	tail -n +$startline $file | head -n +$(($endline - $startline)) &&
	echo "}" # close the function op
)

# Get displaylink_bootstrapper_code()
startline=$(grep -n "displaylink_bootstrapper_code()" "$file" | cut -d: -f1 | head -1)
endline=$(grep -n "chmod 0744 \"\$filename\"" "$file" | tail -n1 | cut -d: -f1 | head -1)

source <(
	tail -n +$startline $file | head -n +$(($endline - $startline)) &&
	echo "}" # close the function op
)

COREDIR=$(mktemp -d)
create_bootstrapper_code "systemd" "/usr/libexec/displaylink/udev.sh"

sed -i -e '1 s/^.*$/\#!\/usr\/bin\/bash/' "$COREDIR/udev.sh"

cat "$COREDIR/udev.sh"

rm -rf "$COREDIR"
