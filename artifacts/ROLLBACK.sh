#!/bin/sh
set -eu
TARGET="${1:?usage: ROLLBACK.sh /path/to/MahjongCopilot-copy}"
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
git -C "$TARGET" apply --reverse --binary "$SCRIPT_DIR/DIFF_FILE"
echo "ROLLBACK_OK target=$TARGET restored=upstream/main"
