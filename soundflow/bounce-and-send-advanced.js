/**
 * SoundFlow Script: Bounce and Send to MASV (Pre-configured Recipients)
 *
 * This version allows you to set recipients in the script - no dialog needed.
 * Perfect for creating multiple shortcuts for different clients!
 *
 * Installation:
 * 1. Open SoundFlow Panel in Pro Tools (Window > SoundFlow)
 * 2. Click "New" > "Script"
 * 3. Copy and paste this code
 * 4. Update PROJECT_PATH below to match your installation
 * 5. Update RECIPIENTS with your email addresses
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

const PROJECT_PATH = "/path/to/masv-protools-integration";

// Set your recipient emails here (comma-separated)
// Leave empty ('') to show the GUI dialog instead
const RECIPIENTS = ""; // e.g., 'client@example.com, producer@example.com'

// ============================================================================
// SCRIPT - No need to modify below this line
// ============================================================================

var command;
if (RECIPIENTS && RECIPIENTS.trim() !== "") {
  command =
    'cd "' +
    PROJECT_PATH +
    '" && echo "' +
    RECIPIENTS +
    '" | ./venv/bin/python3 src/bounce_and_send.py --cli';
} else {
  command =
    'cd "' + PROJECT_PATH + '" && ./venv/bin/python3 src/bounce_and_send.py';
}

sf.system.exec(command);
