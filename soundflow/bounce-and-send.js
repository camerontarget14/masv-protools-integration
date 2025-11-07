/**
 * SoundFlow Script: Bounce and Send to MASV (Simple Version)
 *
 * This script bounces the current Pro Tools session and uploads it to MASV.
 * Shows a Python GUI dialog for entering recipient emails.
 *
 * Installation:
 * 1. Open SoundFlow Panel in Pro Tools (Window > SoundFlow)
 * 2. Click "New" > "Script"
 * 3. Copy and paste this code
 * 4. Update PROJECT_PATH below to match your installation
 * 5. Assign a keyboard shortcut (e.g., Cmd+Shift+M)
 *
 * Requirements:
 * - Pro Tools 2025.10+ with SoundFlow
 * - MASV Pro Tools Integration installed and configured
 * - MASV Agent installed
 */

// ============================================================================
// CONFIGURATION - UPDATE THIS PATH!
// ============================================================================

const PROJECT_PATH = "/path/to/masv-protools-integration";

// ============================================================================
// SCRIPT - No need to modify below this line
// ============================================================================

var command =
  'cd "' + PROJECT_PATH + '" && ./venv/bin/python3 src/bounce_and_send.py';
sf.system.exec(command);
