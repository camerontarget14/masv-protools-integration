/**
 * SoundFlow Script: Bounce and Send to MASV (Advanced)
 *
 * This is an advanced version that prompts for recipients directly in SoundFlow
 * without showing the Python GUI dialog.
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

// Optional: Set default recipients (comma-separated)
const DEFAULT_RECIPIENTS = ''; // e.g., 'client@example.com, producer@example.com'

// ============================================================================
// SCRIPT - No need to modify below this line
// ============================================================================

async function bounceAndSendAdvanced() {
  try {
    // Prompt user for recipient emails using SoundFlow dialog
    const recipientsInput = await sf.dialog.textInput({
      title: 'Bounce and Send to MASV',
      message: 'Enter recipient email addresses (comma-separated):',
      defaultValue: DEFAULT_RECIPIENTS,
      placeholder: 'email1@example.com, email2@example.com'
    });

    // Check if user cancelled
    if (!recipientsInput || recipientsInput.trim() === '') {
      sf.notification.show({
        title: 'Cancelled',
        message: 'No recipients provided',
        type: 'info'
      });
      return;
    }

    // Clean up recipients list
    const recipients = recipientsInput
      .split(',')
      .map(email => email.trim())
      .filter(email => email.length > 0);

    if (recipients.length === 0) {
      sf.notification.show({
        title: 'Error',
        message: 'No valid recipients provided',
        type: 'error'
      });
      return;
    }

    // Show notification that process is starting
    sf.notification.show({
      title: 'Bounce and Send',
      message: `Bouncing and sending to ${recipients.length} recipient(s)...`,
      type: 'info'
    });

    // Build the command to run the Python script in CLI mode with recipients
    const pythonPath = `${PROJECT_PATH}/venv/bin/python3`;
    const scriptPath = `${PROJECT_PATH}/src/bounce_and_send.py`;
    const recipientsArg = recipients.join(',');

    // Create a wrapper command that pipes the recipients to the script
    const command = `cd "${PROJECT_PATH}" && echo "${recipientsArg}" | "${pythonPath}" "${scriptPath}" --cli`;

    // Execute the bounce and send script
    const result = sf.system.exec({
      commandLine: command,
      executionMode: 'Background'
    });

    log.info(`Bounce and Send started for recipients: ${recipientsArg}`);

    // Show completion notification
    // Note: The actual completion happens asynchronously
    // The Python script will show its own success/error notifications

  } catch (error) {
    // Show error notification
    sf.notification.show({
      title: 'Bounce and Send Error',
      message: `Failed: ${error.message}`,
      type: 'error'
    });

    log.error('Bounce and Send error:', error);
  }
}

// Run the function
bounceAndSendAdvanced();
