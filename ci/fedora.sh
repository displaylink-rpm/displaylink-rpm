#!/bin/bash

set -e

DNFCMD="dnf"
SPECFLAG="--spec "
#ARCH="$(uname -m)"

if [ "$OSVERSION" = "rawhide" ] || [ "$((OSVERSION + 0))" -gt 40 ]; then
	DNFCMD="dnf5"
	SPECFLAG=""
fi

$DNFCMD install -y rpm-build make gcc gcc-c++ libdrm-devel systemd-rpm-macros glibc-devel wget git "$DNFCMD-command(builddep)"

$DNFCMD builddep -y $SPECFLAG./displaylink.spec

make $SPECIFICTARGET
