#!/bin/bash

dnf install -y gcc gcc-c++ libdrm-devel rpm-build make wget dnf-utils --enablerepo=extras

dnf-builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

make $(SPECIFICTARGET)
