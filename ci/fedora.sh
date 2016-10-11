#!/bin/bash

dnf install -y rpm-build make gcc wget 'dnf-command(builddep)'

cd /base-src

dnf builddep -y --spec ./displaylink.spec

make
