/**
 * SoundFlow Script: Bounce and Send to MASV
 *
 * This script bounces the current Pro Tools session and uploads it to MASV.
 * You can either set recipients in the script or leave empty to be prompted.
 *
 * Installation:
 * 1. Open SoundFlow Panel in Pro Tools (Window > SoundFlow)
 * 2. Click "New" > "Script"
 * 3. Copy and paste this code
 * 4. Update PROJECT_PATH below to match your installation
 * 5. Optionally set RECIPIENTS for pre-configured emails
 * 6. Assign a keyboard shortcut (e.g., Cmd+Shift+M)
 *
 * Requirements:
 * - Pro Tools 2025.10+ with SoundFlow
 * - MASV Pro Tools Integration installed and configured
 * - MASV Agent installed
 */

// ============================================================================
// CONFIGURATION - UPDATE THESE VALUES!
// ============================================================================

const PROJECT_PATH =
  "/Users/cameronbriantarget/Local/camerontarget14/masv-protools-integration";

// Set your recipient emails here (comma-separated)
// Leave empty ('') to be prompted for recipients when running
const RECIPIENTS = ""; // e.g., 'client@example.com, producer@example.com'

// ============================================================================
// SCRIPT - No need to modify below this line
// ============================================================================

var commandLine;
if (RECIPIENTS && RECIPIENTS.trim() !== "") {
  // Use pre-configured recipients
  commandLine = PROJECT_PATH + '/run_bounce_and_send.sh "' + RECIPIENTS + '"';
} else {
  // Prompt for recipients (uses Python GUI or CLI)
  commandLine =
    'cd "' +
    PROJECT_PATH +
    '" && ./venv/bin/python3 src/bounce_and_send.py --cli';
}

// Execute in background mode to handle long-running process
sf.system.exec({
  commandLine: commandLine,
  executionMode: "Background",
});
