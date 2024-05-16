#!/bin/bash

set -e

DNFCMD="dnf"
SPECFLAG="--spec "

if [ "$OSVERSION" = "rawhide" ] || [ "$((OSVERSION+0))" -gt 40 ]; then
    DNFCMD="dnf5"
    SPECFLAG=""
fi

$DNFCMD install -y rpm-build make gcc gcc-c++ libdrm-devel systemd-rpm-macros glibc-devel.x86_64 wget git $DNFCMD-command\(builddep\)

$DNFCMD builddep -y $SPECFLAG./displaylink.spec

make $SPECIFICTARGET
