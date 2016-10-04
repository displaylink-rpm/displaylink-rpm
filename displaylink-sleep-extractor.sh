#/bin/bash
file=$1

startline=$(grep -n "add_pm_script()" "$file" | cut -d: -f1 |head -1)
endline=$(grep -n 'chmod 0755 $COREDIR/suspend.sh' "$file" | cut -d: -f1 |head -1)

source <(
	tail -n +$startline $file | head -n +$(($endline - $startline)) &&
	echo "}" # close the function op
)
COREDIR=$(mktemp -d)
add_pm_script "systemd"

cat "$COREDIR/suspend.sh"

rm -rf "$COREDIR"
