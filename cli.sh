#!/usr/bin/env bash
set -euo pipefail

# ensure uv is available
command -v uv >/dev/null || \
    { echo "uv not found" >&2; exit 127; }

# get script directory
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)"

# verify cli exists
[[ -f "$SCRIPT_DIR/cli.py" ]] || \
    { echo "cli.py not found at $SCRIPT_DIR" >&2; exit 1; }

exec uv run "$SCRIPT_DIR/cli.py" "$@"
