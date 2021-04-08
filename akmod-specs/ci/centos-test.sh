#!/usr/bin/env bash
cd /root/rpmbuild/RPMS
if (( 7 >= $(rpm -E %centos) ));
then
    yum install -y $(rpm -E %_arch)/evdi-*.rpm $(rpm -E %_arch)/akmod-evdi-*.rpm $(rpm -E %_arch)/displaylink-*.rpm noarch/displaylink-*.rpm \
  && yum remove -y evdi
else
    dnf install -y $(rpm -E %_arch)/evdi-*.rpm $(rpm -E %_arch)/akmod-evdi-*.rpm $(rpm -E %_arch)/displaylink-*.rpm noarch/displaylink-*.rpm \
  && dnf remove -y evdi
fi
