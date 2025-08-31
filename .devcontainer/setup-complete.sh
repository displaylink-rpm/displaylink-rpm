#!/bin/bash

# Minimal setup script for DisplayLink RPM Builder
set -e

echo "Setting up DisplayLink RPM Builder..."

# Install essential build dependencies
sudo dnf install -y --quiet \
    rpm-build \
    rpmdevtools \
    gcc \
    gcc-c++ \
    make \
    libdrm-devel \
    systemd-rpm-macros \
    git \
    wget

# Configure Git and RPM environment
git config --global --add safe.directory "${PWD}"
runuser -l vscode -c "rpmdev-setuptree" 2>/dev/null || true

echo "✅ Setup complete! Ready to build with: make github-release"
