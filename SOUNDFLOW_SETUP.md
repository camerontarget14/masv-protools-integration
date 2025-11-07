# SoundFlow Setup Guide

**Run "Bounce and Send" directly from within Pro Tools using the SoundFlow panel!**

This is the **recommended method** for triggering the bounce and send workflow. SoundFlow is built into Pro Tools 2025.10+ and allows you to run custom scripts with keyboard shortcuts directly from the Pro Tools interface.

## Prerequisites

- **Pro Tools 2025.10 or later** (SoundFlow is built-in)
- **MASV Pro Tools Integration** installed and configured (this project)
- **SoundFlow AI or Pro subscription** ($10-20/month)

> **Important:** While SoundFlow is built into Pro Tools 2025.10+, **creating custom scripts requires a paid subscription**. The free tier only includes pre-built macros, not custom script development.

## Why SoundFlow?

✅ **Native to Pro Tools** - No external apps needed  
✅ **Keyboard shortcuts** - Assign any hotkey you want  
✅ **Search panel** - Type to find and run commands  
✅ **Professional workflow** - Used by major studios worldwide  

---

## Setup Instructions

### Step 1: Enable SoundFlow in Pro Tools

1. **Open Pro Tools 2025.10+**

2. **Access the SoundFlow Panel**
   - Go to: `Window > SoundFlow`
   - Or click the SoundFlow icon in the right sidebar of the Edit window

3. **Sign in to SoundFlow**
   - Create a free account or sign in
   - Follow the guided setup

### Step 2: Install the Bounce and Send Script

We provide two versions:

#### Option A: GUI Version (Shows Dialog)
Shows the Python GUI dialog for entering recipients each time.

1. **Open the script file**
   - Navigate to: `soundflow/bounce-and-send.js`
   - Open in a text editor

2. **Update the project path**
   - Find this line near the top:
     ```javascript
     const PROJECT_PATH = '/Users/YOUR_USERNAME/path/to/masv-protools-integration';
     ```
   - Replace with your actual path (use the full absolute path)
   - Example:
     ```javascript
     const PROJECT_PATH = '/Users/john/Projects/masv-protools-integration';
     ```

3. **Create a new script in SoundFlow**
   - In the SoundFlow panel, click **"New"**
   - Select **"Script"**
   - Name it: `Bounce and Send to MASV`
   - Select or create a package (folder) to organize it

4. **Copy the script code**
   - Copy the entire contents of `soundflow/bounce-and-send.js`
   - Paste into the SoundFlow script editor
   - Click **"Save"**

#### Option B: Pre-configured Recipients (Recommended)
Set recipients in the script - no dialog needed.

1. **Use the advanced script file**
   - Open: `soundflow/bounce-and-send-advanced.js`
   - Update `PROJECT_PATH` as in Option A
   - **Update the RECIPIENTS line:**
     ```javascript
     const RECIPIENTS = 'client@example.com, producer@example.com';
     ```
   - Leave empty (`''`) to show GUI dialog instead
   
2. **Follow steps 3-4 from Option A** to add to SoundFlow

**Tip:** Create multiple scripts with different recipient lists for different clients!

### Step 3: Assign a Keyboard Shortcut

1. **In the SoundFlow panel**, find your "Bounce and Send" script

2. **Click on the script** to select it

3. **Add a trigger**
   - Look for "Triggers" or "Keyboard Shortcut" section
   - Click **"Add Trigger"**
   - Press your desired key combination (e.g., `Cmd+Shift+M` for "MASV")

4. **Limit to Pro Tools** (optional)
   - Set the trigger to only work when Pro Tools is active
   - This prevents conflicts with other apps

5. **Save** your trigger

---

## Usage

### Method 1: Keyboard Shortcut
1. Open a Pro Tools session with content
2. Press your assigned hotkey (e.g., `Cmd+Shift+M`)
3. Enter recipient emails in the dialog
4. Wait for bounce and upload to complete
5. Recipients receive MASV download link

### Method 2: SoundFlow Panel
1. Open the SoundFlow panel (`Window > SoundFlow`)
2. Type "bounce" in the search field
3. Click "Bounce and Send to MASV" in the results
4. Enter recipient emails
5. Done!

### Method 3: Command/Macro Search
1. Press `Cmd+K` (or your configured search shortcut)
2. Type "bounce and send"
3. Press Enter
4. Enter recipient emails

---

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  You press hotkey in Pro Tools                               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  SoundFlow script executes                                   │
│  └─> Launches Python "Bounce and Send" app                   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Dialog appears for recipient emails                         │
│  (Either Python GUI or SoundFlow dialog)                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Pro Tools bounces the session                               │
│  └─> Via Pro Tools Scripting SDK                             │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  File uploads to MASV                                        │
│  └─> Via MASV API                                            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  Success notification                                        │
│  Recipients receive download link                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Customization

### Change Default Recipients

Edit the advanced script to include default recipients:

```javascript
const DEFAULT_RECIPIENTS = 'client@example.com, producer@example.com';
```

### Change Bounce Settings

Edit `.env` in the project root:

```bash
DEFAULT_BOUNCE_FORMAT=WAV
DEFAULT_BIT_DEPTH=24
DEFAULT_SAMPLE_RATE=48000
```

### Change Output Directory

By default, bounces are saved to `~/Desktop/ProTools_Bounces/`

To change this, edit `src/bounce_and_send.py`:

```python
self.bounce_dir = os.path.expanduser("~/Music/Bounces")
```

---

## Troubleshooting

### Script doesn't appear in SoundFlow panel

**Solution:**
- Make sure you saved the script
- Check that it's in a package under "My Packages"
- Refresh the SoundFlow panel

### "Command not found" or path errors

**Solution:**
1. Verify the `PROJECT_PATH` in the script is correct
2. Use the full absolute path (no `~` or relative paths)
3. Test the path in Terminal:
   ```bash
   ls /Users/YOUR_USERNAME/path/to/masv-protools-integration
   ```

### Hotkey doesn't work

**Solution:**
- Check that the trigger is enabled (green indicator)
- Verify no conflicting shortcuts in Pro Tools or macOS
- Make sure Pro Tools is the active application
- Try a different key combination

### Python GUI dialog doesn't appear

**Solution:**
- Check that the virtual environment exists: `ls venv/`
- Test the script manually:
  ```bash
  cd /path/to/masv-protools-integration
  source venv/bin/activate
  python3 src/bounce_and_send.py
  ```
- Check Console.app for error messages

### Pro Tools connection fails

**Solution:**
- Enable Pro Tools Scripting in Preferences:
  - `Setup > Preferences > EUCON`
  - ☑ Enable EUCON & Pro Tools Scripting API
  - Restart Pro Tools

---

## Advanced: Multiple Recipient Presets

Create multiple SoundFlow scripts for different recipient groups:

### Script 1: "Send to Client"
```javascript
const PROJECT_PATH = '/path/to/masv-protools-integration';
const recipients = 'client@example.com';
// ... rest of script with hardcoded recipients
```
Hotkey: `Cmd+Shift+C`

### Script 2: "Send to Producer"
```javascript
const PROJECT_PATH = '/path/to/masv-protools-integration';
const recipients = 'producer@studio.com';
// ... rest of script
```
Hotkey: `Cmd+Shift+P`

### Script 3: "Send to Team"
```javascript
const PROJECT_PATH = '/path/to/masv-protools-integration';
const recipients = 'client@example.com, producer@studio.com, engineer@studio.com';
// ... rest of script
```
Hotkey: `Cmd+Shift+T`

---

## SoundFlow Pricing

### Free Tier (Included with Pro Tools 2025.10+)
- ✅ Access to the SoundFlow panel
- ✅ 1,700+ pre-built macros
- ✅ Keyboard shortcuts for pre-built macros
- ❌ Cannot create custom scripts

### AI Tier ($10/month)
- ✅ Everything in Free
- ✅ **Custom scripts and macros** (required for this integration)
- ✅ AI Session Assistant

### Pro Tier ($12/month)
- ✅ Everything in Free
- ✅ **Custom scripts and macros** (required for this integration)
- ✅ Stream Deck integration
- ✅ Mobile app control
- ✅ MIDI/OSC triggers

### Pro AI Tier ($20/month)
- ✅ All features from both AI and Pro tiers

**For this integration, you need AI ($10/mo) or Pro ($12/mo) tier minimum.**

💡 **Free Alternative:** If you don't want to pay for SoundFlow, use the [Standalone GUI method](README.md#method-2-standalone-gui) instead - it's completely free!

---

## Alternative Methods

If you don't have Pro Tools 2025.10+, see:
- [README.md](README.md) - For standalone GUI or command-line usage

---

## Resources

- **SoundFlow Documentation**: https://soundflow.org/docs
- **SoundFlow Forum**: https://forum.soundflow.org/
- **Pro Tools Scripting SDK**: https://developer.avid.com/scripting/
- **MASV API Docs**: https://developer.massive.io/

---

## Need Help?

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.
