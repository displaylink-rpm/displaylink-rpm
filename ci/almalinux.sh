#!/bin/bash

set -e

dnf install -y gcc gcc-c++ glibc-devel libdrm-devel rpm-build make wget dnf-utils git 'dnf-command(builddep)' --enablerepo=extras

dnf builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

make $SPECIFICTARGET
