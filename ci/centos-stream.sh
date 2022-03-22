#!/bin/bash

if [ "$OSVERSION" = "stream9" ]; then
    dnf install -y rpm-build make gcc wget git 'dnf-command(builddep)'
else
    dnf install -y gcc gcc-c++ libdrm-devel rpm-build make wget dnf-utils git --enablerepo=extras
fi

dnf builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

make $SPECIFICTARGET
