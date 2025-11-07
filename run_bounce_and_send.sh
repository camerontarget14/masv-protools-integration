#!/bin/bash
# Wrapper script to call bounce_and_send.py

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use absolute paths
PYTHON="${SCRIPT_DIR}/venv/bin/python3"
SCRIPT="${SCRIPT_DIR}/src/bounce_and_send.py"

# Get recipient email from argument or environment variable
RECIPIENT="${1:-${MASV_RECIPIENT}}"

# Change to project directory
cd "$SCRIPT_DIR"

# Run the Python script
if [ -n "$RECIPIENT" ]; then
    echo "$RECIPIENT" | "$PYTHON" "$SCRIPT" --cli
else
    "$PYTHON" "$SCRIPT" --cli
fi
