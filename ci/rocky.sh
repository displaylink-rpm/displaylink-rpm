#!/bin/bash

set -e

dnf install -y gcc gcc-c++ glibc-devel.x86_64 glibc-devel.i686 libdrm-devel rpm-build make wget dnf-utils git 'dnf-command(builddep)' --enablerepo=extras

dnf builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

make $SPECIFICTARGET
