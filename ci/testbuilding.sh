#!/bin/bash

set -e

dnf install -y gcc gcc-c++ glibc-devel libdrm-devel rpm-build make wget dnf-utils 'dnf-command(builddep)' git --enablerepo=extras

dnf builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

if [ -z ${SPECIFICTARGET+x} ]; then
echo "Testing 'make srpm'"
make srpm

make clean-all

echo "Testing 'make rpm'"
make rpm

make clean-all

echo "Testing 'make all'"
make all

make clean-all
fi

echo "Testing 'make srpm-github'"
make srpm-github

make clean-all

echo "Testing 'make rpm-github'"
make rpm-github

make clean-all

echo "Testing 'make github-release'"
make github-release

make clean-all
