#!/bin/bash

# Ensure OpenClaw CLI is in PATH for cron jobs
export PATH="/usr/local/bin:$PATH"

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Path to the Python script
PYTHON_SCRIPT="$SCRIPT_DIR/daily_self_review.py"

# Execute the Python script and capture its output
SUMMARY=$(python3 "$PYTHON_SCRIPT")

# Send the summary to the OpenClaw session
# Using 'agent:main:main' as the sessionKey to target the main session.
openclaw message send --channel telegram --target "8217045820" --message "$SUMMARY"
