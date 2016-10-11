#!/bin/bash

yum install -y gcc rpm-build make wget yum-utils --enablerepo=extras

cd /base-src

yum-builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

make
