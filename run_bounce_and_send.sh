#!/bin/bash
# Interactive wrapper script with GUI prompt

# Set PATH to include Homebrew and common locations
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use absolute paths
PYTHON="${SCRIPT_DIR}/venv/bin/python3"
SCRIPT="${SCRIPT_DIR}/src/bounce_and_send.py"

# Load .env to check delivery mode and defaults
if [ -f "${SCRIPT_DIR}/.env" ]; then
    DELIVERY_MODE=$(grep "^MASV_DELIVERY_MODE=" "${SCRIPT_DIR}/.env" | cut -d'=' -f2)
    PORTAL_URL=$(grep "^MASV_PORTAL_URL=" "${SCRIPT_DIR}/.env" | cut -d'=' -f2)
    DEFAULT_RECIPIENTS=$(grep "^MASV_DEFAULT_RECIPIENTS=" "${SCRIPT_DIR}/.env" | cut -d'=' -f2)
fi

# Change to project directory
cd "$SCRIPT_DIR"

# Check delivery mode and prompt accordingly
if [ "$DELIVERY_MODE" = "portal" ]; then
    # Portal mode - always prompt but show default if configured
    if [ -n "$PORTAL_URL" ]; then
        # Default portal configured - show it in dialog
        DEFAULT_PORTAL="https://${PORTAL_URL}.portal.massive.io"
    else
        # No default - show example
        DEFAULT_PORTAL="https://yourportal.portal.massive.io"
    fi

    PORTAL_INPUT=$(osascript -e "Tell application \"System Events\" to display dialog \"Enter MASV Portal URL:\" default answer \"$DEFAULT_PORTAL\" with title \"MASV Bounce and Send\"" -e 'text returned of result' 2>/dev/null)

    if [ -z "$PORTAL_INPUT" ]; then
        osascript -e 'display notification "Cancelled by user" with title "MASV Bounce and Send"'
        exit 0
    fi

    # Extract subdomain from URL (handle both full URL and subdomain-only)
    if [[ "$PORTAL_INPUT" =~ ^https?:// ]]; then
        # Full URL provided - extract subdomain
        PORTAL_SUBDOMAIN=$(echo "$PORTAL_INPUT" | sed -E 's|https?://([^.]+)\..*|\1|')
    else
        # Just subdomain provided
        PORTAL_SUBDOMAIN="$PORTAL_INPUT"
    fi

    # Set portal URL for this run
    export MASV_PORTAL_URL="$PORTAL_SUBDOMAIN"

    # Run for portal mode
    "$PYTHON" "$SCRIPT" --cli
else
    # Email mode - always prompt but show default if configured
    if [ -n "$DEFAULT_RECIPIENTS" ]; then
        DEFAULT_TEXT="$DEFAULT_RECIPIENTS"
    else
        DEFAULT_TEXT=""
    fi

    RECIPIENT=$(osascript -e "Tell application \"System Events\" to display dialog \"Enter recipient email address:\" default answer \"$DEFAULT_TEXT\" with title \"MASV Bounce and Send\"" -e 'text returned of result' 2>/dev/null)

    if [ -z "$RECIPIENT" ]; then
        osascript -e 'display notification "Cancelled by user" with title "MASV Bounce and Send"'
        exit 0
    fi

    # Run the Python script with recipient
    echo "$RECIPIENT" | "$PYTHON" "$SCRIPT" --cli
fi
