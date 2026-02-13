#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2022 ffgiff <ffgiff@gmail.com>
#
# SPDX-License-Identifier: MIT

dnf install -y rpmlint
cd /root/rpmbuild/RPMS
rpmlint ../SPECS && dnf install -y $(rpm -E %_arch)/evdi-*.rpm $(rpm -E %_arch)/akmod-evdi-*.rpm $(rpm -E %_arch)/displaylink-*.rpm noarch/displaylink-*.rpm \
  && dnf remove -y evdi
