#!/usr/bin/env bash
dnf install -y rpmlint
cd /root/rpmbuild/RPMS
rpmlint ../SPECS && dnf install -y $(rpm -E %_arch)/evdi-*.rpm $(rpm -E %_arch)/akmod-evdi-*.rpm $(rpm -E %_arch)/displaylink-*.rpm noarch/displaylink-*.rpm \
  && dnf remove -y evdi
