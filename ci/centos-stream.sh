#!/bin/bash

set -e

dnf install -y rpm-build make gcc glibc-devel.x86_64 wget git 'dnf-command(builddep)'

dnf builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

make $SPECIFICTARGET
