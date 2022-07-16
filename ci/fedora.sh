#!/bin/bash

set -e

dnf install -y rpm-build make gcc glibc-devel.x86_64 glibc-devel.i686 wget git 'dnf-command(builddep)'

dnf builddep -y --spec ./displaylink.spec

make $SPECIFICTARGET
