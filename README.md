# MASV Pro Tools Integration

**Automate bouncing Pro Tools sessions and sending them via MASV file transfer - triggered directly from within Pro Tools!**

## Features

- **Trigger from within Pro Tools** using SoundFlow panel (Pro Tools 2025.10+)
- **Keyboard shortcut support** - assign any hotkey you want
- **Programmatic bouncing** via Pro Tools Scripting SDK
- **Automatic MASV upload** - no manual file transfers
- **Multiple recipients** - send to clients, producers, team members
- **Fast workflow** - bounce and send in one action

## Prerequisites

### For SoundFlow Integration (Pro Tools 2025.10+)
1. **Pro Tools 2025.10+** (SoundFlow built-in)
2. **SoundFlow AI or Pro subscription** ($10-20/month) - Required for custom scripts
3. **MASV Agent** - Official MASV uploader ([Download here](https://developer.massive.io/transfer-agent/latest/))
4. **MASV Account** with API access
5. **Python 3.8+**

> **Note:** SoundFlow's free tier includes 1,700+ pre-built macros but does not allow custom scripts. Custom script creation requires a paid subscription.

### For Alternative Methods (without SoundFlow)
1. **Pro Tools 2022.12+** with Scripting SDK enabled
2. **MASV Agent** - Official MASV uploader ([Download here](https://developer.massive.io/transfer-agent/latest/))
3. **MASV Account** with API access
4. **Python 3.8+**

## Setup

### 1. Clone and Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Install MASV Agent

**MASV Agent is required for optimized file transfers.**

Download and install from: https://developer.massive.io/transfer-agent/latest/

**Platform-specific installation:**
- **macOS**: Download the .dmg installer and drag MASV Agent to Applications
- **Windows**: Download and run the .exe installer
- **Linux**: Follow the installation guide for your distribution
- **Docker**: Available for cross-platform deployment

**Verify installation:**
```bash
masv --version
```

### 3. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
# - Get MASV API key from https://massive.io account settings
# - Get MASV Team ID from MASV dashboard
```

### 4. Generate gRPC Code from Proto Files

```bash
# Generate Python code from Pro Tools proto files
./venv/bin/python -m grpc_tools.protoc \
  -I. \
  --python_out=./generated \
  --grpc_python_out=./generated \
  PTSL.2025.06.0.proto

# Fix generated import (protoc creates invalid Python syntax with numeric paths)
# This replaces the invalid import line in the generated file
sed -i '' 's/from PTSL\.2025\.06 import 0_pb2/# Fixed import\nimport sys, os, importlib.util\n_pb2_path = os.path.join(os.path.dirname(__file__), '\''0_pb2.py'\'')\n_spec = importlib.util.spec_from_file_location("PTSL_dot_2025_dot_06_dot_0__pb2", _pb2_path)\nPTSL_dot_2025_dot_06_dot_0__pb2 = importlib.util.module_from_spec(_spec)\n_spec.loader.exec_module(PTSL_dot_2025_dot_06_dot_0__pb2)\n# Original:/' generated/PTSL/2025/06/0_pb2_grpc.py
```

### 5. Pro Tools Scripting Setup

**No preferences needed!** The Pro Tools Scripting SDK works automatically if:
- You have **Pro Tools 2022.12 or later** (including Artist, Studio, Ultimate, or even the free Intro version)
- Pro Tools is **running with a session open**

The gRPC server starts automatically on port **31416** when Pro Tools launches.

## Usage

### Method 1: SoundFlow Panel (Pro Tools 2025.10+)

**Run directly from within Pro Tools with a keyboard shortcut!**

See **[SOUNDFLOW_SETUP.md](SOUNDFLOW_SETUP.md)** for complete setup instructions.

**Quick steps:**
1. Open SoundFlow panel in Pro Tools (`Window > SoundFlow`)
2. Create a new script using `soundflow/bounce-and-send.js`
3. Assign a keyboard shortcut (e.g., `Cmd+Shift+M`)
4. Press your hotkey anytime to bounce and send!

**Benefits:**
- Native to Pro Tools - no external apps needed
- Keyboard shortcuts work inside Pro Tools
- Professional workflow used by major studios

**Cost:** Requires SoundFlow AI ($10/mo) or Pro ($12/mo) subscription for custom scripts

---

### Method 2: Command Line -- FREE

```bash
source venv/bin/activate
python3 src/bounce_and_send.py --cli
```

Prompts for recipient emails in the terminal.

**Benefits:**
- No subscription required
- Works with any Pro Tools version
- No GUI dependencies needed
- Simple and reliable

**Note:** GUI mode requires tkinter. Use `--cli` flag to avoid GUI dependencies.

---





## Project Structure

```
.
├── PTSL.proto                        # Pro Tools Protocol Buffer definitions
├── PTSL.2025.06.0.proto             # Version-specific definitions
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variable template
├── generated/                        # Generated gRPC code (gitignored)
├── soundflow/                        # SoundFlow scripts for Pro Tools
│   ├── bounce-and-send.js           # Basic SoundFlow script
│   └── bounce-and-send-advanced.js  # Advanced with SoundFlow dialogs
├── src/
│   ├── protools/                    # Pro Tools client wrapper
│   ├── masv/                        # MASV Agent CLI wrapper
│   └── bounce_and_send.py           # Main application
├── SOUNDFLOW_SETUP.md               # SoundFlow integration guide
└── TROUBLESHOOTING.md               # Common issues and fixes
```

## Quick Start

1. **Setup** (one-time):
   ```bash
   # Install Python dependencies
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # Install MASV Agent
   # Download from: https://developer.massive.io/transfer-agent/latest/
   # Verify: masv --version

   # Generate gRPC code
   ./venv/bin/python -m grpc_tools.protoc -I. --python_out=./generated --grpc_python_out=./generated PTSL.2025.06.0.proto

   # Configure credentials
   cp .env.example .env
   # Edit .env with your MASV API key and Team ID
   ```

2. **Enable Pro Tools Scripting**:
   - Setup > Preferences > EUCON
   - Enable "Enable EUCON & Pro Tools Scripting API"
   - Restart Pro Tools

3. **Run**:
   ```bash
   source venv/bin/activate
   python3 src/bounce_and_send.py
   ```

4. **Set up SoundFlow integration** (Pro Tools 2025.10+):
   - See [SOUNDFLOW_SETUP.md](SOUNDFLOW_SETUP.md) for in-Pro-Tools triggering
   - Assign a keyboard shortcut and bounce/send directly from Pro Tools!

## Why MASV Agent?

This project now uses the **official MASV Agent CLI** instead of direct REST API calls, providing:

- **Optimized transfer speeds** - MASV Agent is specifically tuned for performance
- **Automatic retry logic** - Handles network interruptions gracefully
- **Better error handling** - Production-tested reliability
- **Official support** - Maintained by MASV with regular updates
- **Consistent with MASV ecosystem** - Same tool used across platforms

## Which Method Should I Use?

| Method | Pro Tools Version | Cost | Trigger Location | Best For |
|--------|------------------|------|------------------|----------|
| **Command Line** ⭐ | Any version | Free | Terminal | Most users - simple and reliable |
| **SoundFlow** | 2025.10+ | $10-20/mo | Inside Pro Tools | Power users with existing subscription |

## License

Pro Tools SDK files are subject to Avid SDK license agreement.
