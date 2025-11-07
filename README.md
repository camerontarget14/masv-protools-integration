# MASV Pro Tools Integration

Automate bouncing Pro Tools sessions and sending them via MASV file transfer with a keyboard shortcut!

## Features

- Keyboard shortcut support via Keyboard Maestro or Automator
- Programmatic bouncing via Pro Tools Scripting SDK
- Automatic MASV upload with real-time progress
- Dual delivery modes: email recipients or MASV portals
- Session-relative bounces saved to Bounced Files folder

## Prerequisites

1. Pro Tools 2022.12+ (Scripting SDK works automatically)
2. MASV Agent - https://developer.massive.io/transfer-agent/latest/
3. MASV Account with API access
4. Python 3.8+
5. Keyboard Maestro or macOS Automator

## Quick Setup

### 1. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install MASV Agent

```bash
brew install masv-agent
# Or download from: https://developer.massive.io/transfer-agent/latest/
```

### 3. Configure

```bash
cp .env.example .env
nano .env
```

Set your credentials and delivery mode (email or portal).

### 4. Generate gRPC Code

```bash
./venv/bin/python -m grpc_tools.protoc -I. --python_out=./generated --grpc_python_out=./generated PTSL.2025.06.0.proto
```

## Usage

Run the shell script:

```bash
/path/to/masv-protools-integration/run_bounce_and_send.sh
```

### Keyboard Maestro Setup

1. Create new macro
2. Trigger: Your hotkey (e.g., Cmd+Shift+M)
3. Action: Execute Shell Script
4. Script: `/path/to/masv-protools-integration/run_bounce_and_send.sh`
5. Available in: Pro Tools

### Automator Setup

1. New Quick Action
2. Run Shell Script action
3. Script: `/path/to/masv-protools-integration/run_bounce_and_send.sh`
4. Assign keyboard shortcut in System Settings

## Delivery Modes

**Email:**
```bash
MASV_DELIVERY_MODE=email
MASV_DEFAULT_RECIPIENTS=client@example.com
```

**Portal:**
```bash
MASV_DELIVERY_MODE=portal
MASV_PORTAL_URL=yourclient
MASV_PORTAL_PASSWORD=secret
MASV_SENDER_EMAIL=you@example.com
```

## License

MIT License

## Support

For issues or questions, please open a GitHub issue.
