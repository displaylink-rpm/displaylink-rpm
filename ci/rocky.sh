#!/usr/bin/bash

dnf install -y gcc gcc-c++ libdrm-devel rpm-build make wget dnf-utils --enablerepo=extras

cd /base-src

dnf-builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

make
