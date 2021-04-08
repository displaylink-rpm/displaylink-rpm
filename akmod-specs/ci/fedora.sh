#!/bin/bash

dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
dnf install -y fakeroot rpm-build rpmdevtools kmodtool buildsys-build-rpmfusion-kerneldevpkgs-current akmods libdrm-devel
rpmdev-setuptree
cp /base-src/akmod-specs/*.spec /root/rpmbuild/SPECS
spectool -g -R /root/rpmbuild/SPECS/evdi.spec
export VERSION=5.4
pushd /root/rpmbuild/SOURCES
curl -LO https://www.synaptics.com/sites/default/files/exe_files/2021-04/DisplayLink%20USB%20Graphics%20Software%20for%20Ubuntu${VERSION}-EXE.zip
popd
spectool -g -R /root/rpmbuild/SPECS/displaylink.spec
rpmbuild -bb /root/rpmbuild/SPECS/evdi.spec
rpmbuild -bb /root/rpmbuild/SPECS/evdi-kmod.spec
QA_RPATHS=0x0004 rpmbuild -bb /root/rpmbuild/SPECS/displaylink.spec

