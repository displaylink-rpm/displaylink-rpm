#!/bin/bash

dnf install -y gcc gcc-c++ libdrm-devel rpm-build make wget dnf-utils --enablerepo=extras

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

echo "Testing 'make srpm-github'"
make srpm-github

if [ $? -ne 0 ]; then exit 1; fi
make clean-all

echo "Testing 'make rpm-github'"
make rpm-github

if [ $? -ne 0 ]; then exit 1; fi
make clean-all

echo "Testing 'make all'"
make all

if [ $? -ne 0 ]; then exit 1; fi
make clean-all

echo "Testing 'make github-release'"
make github-release

if [ $? -ne 0 ]; then exit 1; fi
make clean-all
