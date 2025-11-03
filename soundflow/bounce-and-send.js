/**
 * SoundFlow Script: Bounce and Send to MASV
 *
 * This script bounces the current Pro Tools session and uploads it to MASV.
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
 */

// ============================================================================
// CONFIGURATION - UPDATE THIS PATH!
// ============================================================================

const PROJECT_PATH = '/Users/YOUR_USERNAME/path/to/masv-protools-integration';

// ============================================================================
// SCRIPT - No need to modify below this line
// ============================================================================

async function bounceAndSend() {
  try {
    // Show notification that process is starting
    sf.notification.show({
      title: 'Bounce and Send',
      message: 'Starting bounce to MASV...',
      type: 'info'
    });

    // Build the command to run the Python script
    const pythonPath = `${PROJECT_PATH}/venv/bin/python3`;
    const scriptPath = `${PROJECT_PATH}/src/bounce_and_send.py`;

    // Change to project directory and run the script
    const command = `cd "${PROJECT_PATH}" && "${pythonPath}" "${scriptPath}"`;

    // Execute the bounce and send script
    // This will show the GUI dialog for entering recipients
    const result = sf.system.exec({
      commandLine: command,
      executionMode: 'Background'
    });

    // The Python script handles the rest:
    // 1. Shows dialog for recipient emails
    // 2. Connects to Pro Tools and bounces
    // 3. Uploads to MASV
    // 4. Shows success/error notification

    log.info('Bounce and Send script launched successfully');

  } catch (error) {
    // Show error notification
    sf.notification.show({
      title: 'Bounce and Send Error',
      message: `Failed to launch: ${error.message}`,
      type: 'error'
    });

    log.error('Bounce and Send error:', error);
  }
}

// Run the function
bounceAndSend();
