#!/bin/bash

dnf install -y gcc rpm-build make wget dnf-utils --enablerepo=extras

cd /base-src

dnf-builddep -y ./displaylink.spec

chown `id -u`:`id -g` -R .

make $(SPECIFICTARGET)
