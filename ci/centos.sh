#!/bin/bash

yum install -y gcc gcc-c++ libdrm-devel rpm-build make wget yum-utils git --enablerepo=extras

yum-builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

make $SPECIFICTARGET
