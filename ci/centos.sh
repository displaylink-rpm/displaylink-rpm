#!/bin/bash

set -e

yum install -y gcc gcc-c++ glibc-devel.x86_64 libdrm-devel rpm-build make wget yum-utils git --enablerepo=extras

yum-builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

make $SPECIFICTARGET
