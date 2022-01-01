#!/bin/bash

dnf install -y rpm-build make gcc wget 'dnf-command(builddep)'

dnf builddep -y --spec ./displaylink.spec

make $(SPECIFICTARGET)
