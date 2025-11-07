# MASV Pro Tools Integration

Automate bouncing Pro Tools sessions and sending them via MASV with a keyboard shortcut!

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
git clone <your-repo-url>
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

**For portal delivery:**
```bash
MASV_DELIVERY_MODE=portal
MASV_PORTAL_URL=yourclient
MASV_PORTAL_PASSWORD=secret
MASV_SENDER_EMAIL=you@example.com
```

### 4. Generate Pro Tools gRPC Code

```bash
./venv/bin/python -m grpc_tools.protoc \
  -I. \
  --python_out=./generated \
  --grpc_python_out=./generated \
  PTSL.2025.06.0.proto
```

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

MIT License

Pro Tools SDK files subject to Avid SDK license agreement.
