#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .

mkdir -p "$HOME/.local/bin"
ln -sf "$(pwd)/.venv/bin/labweave" "$HOME/.local/bin/labweave"

echo "Kali LabWeave installed."
echo "Symlink created at: $HOME/.local/bin/labweave"
echo "If needed, add this to PATH: export PATH=\"\$HOME/.local/bin:\$PATH\""
echo "Run: labweave doctor"
