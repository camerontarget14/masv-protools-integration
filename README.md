# (WIP) MASV Pro Tools Integration

Automate bouncing Pro Tools sessions and sending them via MASV with a keyboard shortcut.

<img width="678" height="401" alt="Screenshot 2025-11-08 at 8 47 50 PM" src="https://github.com/user-attachments/assets/e7fdea2a-bed6-4e11-a849-c6501300eecd" />


!! This integration needs a proper trigger, options include integration with "Sound Flow" a third-party automation tool that is now built into protools !!

## ⚠️ Pro Tools SDK License Agreement Required

**This project does NOT include Pro Tools SDK files.** You must download the Pro Tools Scripting SDK directly from Avid and agree to their license terms before using this integration. See [Setup section](#4-download-and-setup-pro-tools-sdk-files) for details.

## Features

- **Keyboard shortcut triggered** - One hotkey to bounce and send
- **GUI prompt for recipients** - Dialog box asks for email each time
- **Dual delivery modes** - Email recipients or MASV portals
- **Real-time progress** - See upload percentage
- **Session-organized** - Bounces saved to session's Bounced Files folder
- **Pro Tools SDK integration** - Programmatic bouncing

## Prerequisites

1. **Pro Tools 2022.12+** (Scripting SDK enabled automatically)
2. **MASV Agent** - https://developer.massive.io/transfer-agent/latest/
3. **MASV Account** with API credentials
4. **Python 3.8+**
5. **Apple Shortcuts** or **Keyboard Maestro** (for keyboard shortcut)

## Setup

### 1. Install Dependencies

```bash
# Clone repository
git clone https://github.com/camerontarget14/masv-protools-integration/
cd masv-protools-integration

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Install MASV Agent

```bash
# macOS with Homebrew
brew install masv-agent

# Or download installer
# https://developer.massive.io/transfer-agent/latest/
```

Verify installation:
```bash
masv --help
```

### 3. Configure Credentials

```bash
cp .env.example .env
nano .env
```

**Required settings:**
- `MASV_API_KEY` - From https://app.massive.io/settings/developers
- `MASV_TEAM_ID` - From MASV dashboard
- `MASV_DELIVERY_MODE` - Set to `email` or `portal`

**For email delivery:**
```bash
MASV_DELIVERY_MODE=email
```

<img width="769" height="408" alt="Screenshot 2025-11-08 at 8 48 34 PM" src="https://github.com/user-attachments/assets/6ad15f07-abb6-4ece-ba1b-c6f691c0f0d0" />


**For portal delivery:**
```bash
MASV_DELIVERY_MODE=portal
MASV_PORTAL_URL=yourclient
MASV_PORTAL_PASSWORD=secret
MASV_SENDER_EMAIL=you@example.com
```

### 4. Download and Setup Pro Tools SDK Files

**IMPORTANT:** This integration requires the Pro Tools Scripting SDK files, which are NOT included in this repository. You must download them directly from Avid and agree to their license terms.

#### Download the SDK:
1. Visit the [Avid Pro Tools SDK page](https://www.avid.com/alliance-partner-program/pro-tools-integration)
2. Sign in or create an Avid developer account
3. Download the **Pro Tools Scripting SDK** (version 2025.06.0 or later)
4. Review and accept Avid's SDK license agreement

#### Extract the Proto File:
After downloading, locate the protobuf definition file:
- Look for: `PTSL.2025.06.0.proto` (or similar version)
- Copy it to the root of this project directory

#### Generate Python gRPC Code:
Once you have the `.proto` file, generate the Python code:

```bash
# Make sure you're in the project directory with venv activated
source venv/bin/activate

# Generate the gRPC Python files
python -m grpc_tools.protoc \
  -I. \
  --python_out=./generated \
  --grpc_python_out=./generated \
  PTSL.2025.06.0.proto
```

This will create:
- `generated/PTSL/2025/06/0_pb2.py` - Protocol buffer definitions
- `generated/PTSL/2025/06/0_pb2_grpc.py` - gRPC client/server code

#### Fix Import Issues in Generated Files:
The generated `0_pb2_grpc.py` file will have an import statement that doesn't work in Python (because of numeric folder names). You need to fix it:

1. Open `generated/PTSL/2025/06/0_pb2_grpc.py`
2. Find line 6: `from PTSL.2025.06 import 0_pb2 as PTSL_dot_2025_dot_06_dot_0__pb2`
3. Replace it with:
```python
import importlib.util
import os

# Import 0_pb2 using importlib since the path contains numbers
_pb2_path = os.path.join(os.path.dirname(__file__), '0_pb2.py')
_spec = importlib.util.spec_from_file_location("PTSL_dot_2025_dot_06_dot_0__pb2", _pb2_path)
PTSL_dot_2025_dot_06_dot_0__pb2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PTSL_dot_2025_dot_06_dot_0__pb2)
```

**Why this step is needed:** The Pro Tools SDK uses folder names with numbers (2025/06), which creates invalid Python import paths. This workaround uses `importlib` to load the module directly.

### 5. Verify Setup

Test that the SDK files are properly configured:

```bash
python -c "from src.protools import ProToolsClient; print('SDK setup successful!')"
```

If you see "SDK setup successful!", you're ready to go!

## Setting Up Keyboard Shortcut

### Option 1: Apple Shortcuts (Recommended for macOS)

1. Open **Shortcuts** app
2. Click **+** to create new shortcut
3. Search for and add **Run Shell Script** action
4. Set **Pass input:** to "as arguments"
5. Paste this script:
   ```bash
   /Users/YOUR_USERNAME/path/to/masv-protools-integration/run_bounce_and_send.sh
   ```
   (Update path to match your installation)
6. Click the shortcut name at top and rename to "Bounce to MASV"
7. Click the info button (ⓘ) in top right
8. Enable **Pin in Menu Bar** (optional)
9. Add **Keyboard Shortcut** (e.g., ⌘⇧M)
10. Under **Use As**, enable **Quick Action**

**To use:**
- Press your keyboard shortcut from anywhere (including Pro Tools)
- Enter recipient email in the dialog
- Script bounces and uploads automatically

### Option 2: Keyboard Maestro

1. Create new macro
2. Set trigger to your hotkey (e.g., ⌘⇧M)
3. Add action: **Execute Shell Script**
4. Paste:
   ```bash
   /Users/YOUR_USERNAME/path/to/masv-protools-integration/run_bounce_and_send.sh
   ```
5. Set **Available in:** to "Pro Tools" only

## Usage Workflow

### Email Mode
1. **Open Pro Tools session** and work on your project
2. **Press your keyboard shortcut** (e.g., ⌘⇧M)
3. **Dialog appears** - Enter recipient email address
4. **Script runs automatically:**
   - Connects to Pro Tools
   - Bounces mix to session's Bounced Files folder
   - Uploads to MASV with progress display
   - Sends to recipient email
5. **Success notification** - Package ID and destination shown

### Portal Mode
1. **Open Pro Tools session** and work on your project
2. **Press your keyboard shortcut** (e.g., ⌘⇧M)
3. **If portal URL not configured:**
   - Dialog appears asking for portal URL
   - Enter full URL: `https://yourportal.portal.massive.io`
   - Or just subdomain: `yourportal`
4. **If portal URL is configured in `.env`:**
   - No prompt - uses default portal automatically
5. **Script runs automatically:**
   - Connects to Pro Tools
   - Bounces mix to session's Bounced Files folder
   - Uploads to MASV with progress display
   - Sends to configured portal
6. **Success notification** - Package ID and portal destination shown

## Delivery Modes

### Email Mode
Send directly to email recipients - you'll be prompted each time:
```bash
MASV_DELIVERY_MODE=email
```
**Behavior:** Dialog asks for recipient email every time you run the script.

### Portal Mode with Default Portal
Upload to the same portal every time automatically:
```bash
MASV_DELIVERY_MODE=portal
MASV_PORTAL_URL=clientname
MASV_PORTAL_PASSWORD=secret123
MASV_SENDER_EMAIL=your@email.com
```
**Behavior:** No prompt - sends directly to configured portal.

### Portal Mode without Default (Ad-Hoc)
Prompt for different portals each time:
```bash
MASV_DELIVERY_MODE=portal
MASV_PORTAL_URL=
MASV_PORTAL_PASSWORD=secret123
MASV_SENDER_EMAIL=your@email.com
```
**Behavior:** Dialog asks for portal URL every time. You can enter:
- Full URL: `https://client1.portal.massive.io`
- Just subdomain: `client1`

**Tip:** Leave `MASV_PORTAL_URL` empty if you work with multiple portals and want to choose each time.

## Project Structure

```
.
├── run_bounce_and_send.sh          # Main shell script (use this!)
├── .env.example                     # Template
├── requirements.txt                 # Python dependencies
├── PTSL.2025.06.0.proto            # Pro Tools SDK definitions
├── generated/                       # gRPC code (auto-generated)
└── src/
    ├── bounce_and_send.py          # Main application
    ├── protools/client.py          # Pro Tools gRPC client
    └── masv/client.py              # MASV Agent wrapper
```

## Troubleshooting

### "MASV Agent not found"
Ensure `/opt/homebrew/bin` is in your PATH. The script adds it automatically, but verify:
```bash
which masv
# Should show: /opt/homebrew/bin/masv
```

### "Pro Tools not connecting"
- Ensure Pro Tools 2022.12+ is running
- Open a session (SDK only works with session open)
- Port 31416 should be available

### "Portal authorization required"
Set `MASV_PORTAL_PASSWORD` in `.env` file

### Script works in terminal but not with keyboard shortcut
The shell script sets PATH automatically. If still failing, check the script has execute permissions:
```bash
chmod +x run_bounce_and_send.sh
```

## Why This Approach?

- **One-key workflow** - Fastest way to bounce and send
- **GUI prompt** - Flexibility to change recipients
- **No subscription needed** - Free with Apple Shortcuts
- **Pro Tools native** - Works from within Pro Tools
- **Session organized** - Bounces stay with source files

## License

MIT License - applies to this integration code only.

**Pro Tools SDK files are NOT included in this repository.** The Pro Tools Scripting SDK is subject to Avid's SDK license agreement. You must download the SDK directly from Avid and agree to their terms separately. This project simply provides integration code that uses the SDK once you have obtained it legally.
