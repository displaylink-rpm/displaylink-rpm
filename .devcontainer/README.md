# DisplayLink RPM Builder

Minimal devcontainer for building DisplayLink RPM packages.

## Quick Start

1. Open in VS Code dev container
2. Wait for automatic setup to complete
3. Build: `make github-release`

## Build Commands

- `make github-release` - Build with latest EVDI (recommended)
- `make` - Build with bundled EVDI
- `make clean` - Clean build artifacts

Built packages will be in `x86_64/` and workspace root.
