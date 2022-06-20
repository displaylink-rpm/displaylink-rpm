#!/bin/bash

set -e

if [ "$OSVERSION" = "stream9" ]; then
    dnf install -y rpm-build make gcc glibc-devel.x86_64 glibc-devel.i686 wget git 'dnf-command(builddep)'
else
    dnf install -y gcc gcc-c++ glibc-devel.x86_64 glibc-devel.i686 libdrm-devel rpm-build make wget dnf-utils git --enablerepo=extras
fi

dnf builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

make $SPECIFICTARGET
