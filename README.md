# MASV Pro Tools Integration

One-button bounce and upload to MASV from Pro Tools.

<img width="678" alt="Screenshot 2025-11-08 at 8 47 50 PM" src="https://github.com/user-attachments/assets/e7fdea2a-bed6-4e11-a849-c6501300eecd" />

## ⚠️ Pro Tools SDK Required

**SDK files NOT included.** Download the [Pro Tools Scripting SDK](https://www.avid.com/alliance-partner-program/pro-tools-integration) from Avid and accept their license before proceeding.

## Prerequisites

- Pro Tools 2022.12+
- [MASV Agent](https://developer.massive.io/transfer-agent/latest/)
- MASV account with API credentials
- Python 3.8+

## Quick Setup

### 1. Install Dependencies

```bash
git clone https://github.com/camerontarget14/masv-protools-integration/
cd masv-protools-integration
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
brew install masv-agent  # or download from link above
```

### 2. Configure MASV

```bash
cp .env.example .env
# Edit .env with your credentials:
# - MASV_API_KEY (from https://app.massive.io/settings/developers)
# - MASV_TEAM_ID
# - MASV_DELIVERY_MODE (email or portal)
```

<img width="769" height="408" alt="Screenshot 2025-11-08 at 8 48 34 PM" src="https://github.com/user-attachments/assets/6ad15f07-abb6-4ece-ba1b-c6f691c0f0d0" />

### 3. Setup Pro Tools SDK

1. Download [Pro Tools Scripting SDK](https://www.avid.com/alliance-partner-program/pro-tools-integration) from Avid
2. Extract `PTSL.2025.06.0.proto` to project root
3. Generate Python code:
   ```bash
   python -m grpc_tools.protoc \
     -I. \
     --python_out=./generated \
     --grpc_python_out=./generated \
     PTSL.2025.06.0.proto
   ```
4. Fix generated imports in `generated/PTSL/2025/06/0_pb2_grpc.py`:
   
   Replace line 6:
   ```python
   from PTSL.2025.06 import 0_pb2 as PTSL_dot_2025_dot_06_dot_0__pb2
   ```
   
   With:
   ```python
   import importlib.util, os
   _pb2_path = os.path.join(os.path.dirname(__file__), '0_pb2.py')
   _spec = importlib.util.spec_from_file_location("PTSL_dot_2025_dot_06_dot_0__pb2", _pb2_path)
   PTSL_dot_2025_dot_06_dot_0__pb2 = importlib.util.module_from_spec(_spec)
   _spec.loader.exec_module(PTSL_dot_2025_dot_06_dot_0__pb2)
   ```

5. Verify:
   ```bash
   python -c "from src.protools import ProToolsClient; print('✓ Ready!')"
   ```

### 4. Setup Keyboard Shortcut

**Apple Shortcuts (macOS):**
1. Open Shortcuts app → New shortcut
2. Add "Run Shell Script" action
3. Paste: `/path/to/masv-protools-integration/run_bounce_and_send.sh`
4. Add keyboard shortcut (e.g., ⌘⇧M)

**Keyboard Maestro:**
1. New macro with hotkey trigger
2. Add "Execute Shell Script" action
3. Paste script path above

## Usage

1. Open Pro Tools session
2. Press your keyboard shortcut
3. Enter recipient email (or portal URL if first time)
4. Script automatically bounces and uploads

## Delivery Modes

**Email mode** (prompt each time):
```bash
MASV_DELIVERY_MODE=email
```

**Portal mode** (auto-upload to default):
```bash
MASV_DELIVERY_MODE=portal
MASV_PORTAL_URL=clientname
MASV_PORTAL_PASSWORD=secret123
MASV_SENDER_EMAIL=your@email.com
```

**Portal mode** (prompt for URL each time):
```bash
MASV_DELIVERY_MODE=portal
MASV_PORTAL_URL=          # Leave empty
MASV_PORTAL_PASSWORD=secret123
MASV_SENDER_EMAIL=your@email.com
```

## Troubleshooting

**"MASV Agent not found"**
```bash
which masv  # Should show /opt/homebrew/bin/masv
```

**"Pro Tools not connecting"**
- Ensure Pro Tools 2022.12+ is running with a session open
- Port 31416 must be available

**"Portal authorization required"**
- Set `MASV_PORTAL_PASSWORD` in `.env`

## License

MIT License - integration code only.

Pro Tools SDK subject to Avid's separate license agreement.
