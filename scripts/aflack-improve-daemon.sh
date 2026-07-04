#!/usr/bin/env bash
# Autonomous improvement daemon tick.
# Safe by design: runs the distill/propose loop only. It NEVER generates paid
# media, publishes, or edits skill/rule files. Intended to be invoked by cron or
# launchd on a schedule (e.g., every 6h) for the "Damon SDLC" background loop.
set -euo pipefail

PROJECT_ROOT="${AFLACK_ROOT:-/Users/ace/aflack}"
cd "$PROJECT_ROOT"

# shellcheck disable=SC1091
source .venv/bin/activate

NICHE="${AFLACK_NICHE:-gta6-ai-persona-gaming}"
LOG_DIR="$PROJECT_ROOT/.aiwg/working/daemon-logs"
mkdir -p "$LOG_DIR"
TS="$(date -u +%Y%m%dT%H%M%SZ)"

echo "[$TS] improve-cycle niche=$NICHE" >> "$LOG_DIR/improve.log"
aflack improve-cycle --niche "$NICHE" >> "$LOG_DIR/improve.log" 2>&1
echo "[$TS] done" >> "$LOG_DIR/improve.log"
