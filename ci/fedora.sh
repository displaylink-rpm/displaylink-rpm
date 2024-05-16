#!/bin/bash

set -e

DNFCMD="dnf5"
SPECFLAG=""

if [ "$OSVERSION" = "39" ]; then
    DNFCMD="dnf"
    SPECFLAG="--spec "
fi

$DNFCMD install -y rpm-build make gcc gcc-c++ libdrm-devel systemd-rpm-macros glibc-devel.x86_64 wget git $DNFCMD-command\(builddep\)

$DNFCMD builddep -y $SPECFLAG./displaylink.spec

make $SPECIFICTARGET
