#!/bin/bash

if (( 7 >= $(rpm -E %centos) ));
then
    yum localinstall -y --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-$(rpm -E %centos).noarch.rpm https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-$(rpm -E %centos).noarch.rpm
    yum install -y fakeroot rpm-build rpmdevtools kmodtool buildsys-build-rpmfusion akmods libdrm-devel
else
    dnf install -y --nogpgcheck https://dl.fedoraproject.org/pub/epel/epel-release-latest-$(rpm -E %centos).noarch.rpm
    dnf install -y --nogpgcheck https://mirrors.rpmfusion.org/free/el/rpmfusion-free-release-$(rpm -E %centos).noarch.rpm https://mirrors.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-$(rpm -E %centos).noarch.rpm
    dnf install -y dnf-plugins-core fakeroot rpm-build rpmdevtools kmodtool buildsys-build-rpmfusion akmods libdrm-devel
    dnf config-manager --enable powertools
fi
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

