#!/usr/bin/env bash
cd /root/rpmbuild/RPMS
dnf install -y $(rpm -E %_arch)/evdi-*.rpm $(rpm -E %_arch)/akmod-evdi-*.rpm $(rpm -E %_arch)/displaylink-*.rpm noarch/displaylink-*.rpm \
  && dnf remove -y evdi
