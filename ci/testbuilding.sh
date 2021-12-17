#!/usr/bin/bash

dnf install -y gcc gcc-c++ libdrm-devel rpm-build make wget dnf-utils --enablerepo=extras

cd /base-src

dnf-builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

echo "Testing 'make srpm'"
make srpm


if [ $? -ne 0 ]; then exit 1; fi
make clean-all

echo "Testing 'make rpm'"
make rpm

if [ $? -ne 0 ]; then exit 1; fi
make clean-all

echo "Testing 'make srpm-unbundled'"
make srpm-unbundled

if [ $? -ne 0 ]; then exit 1; fi
make clean-all

echo "Testing 'make rpm-unbundled'"
make rpm-unbundled

if [ $? -ne 0 ]; then exit 1; fi
make clean-all

echo "Testing 'make all'"
make all

if [ $? -ne 0 ]; then exit 1; fi
make clean-all

echo "Testing 'make unbundled'"
make unbundled

if [ $? -ne 0 ]; then exit 1; fi
make clean-all
