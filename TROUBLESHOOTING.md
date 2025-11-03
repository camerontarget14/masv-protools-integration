# Troubleshooting Guide

Common issues and their solutions for the MASV Pro Tools Integration.

## Pro Tools Connection Issues

### Error: "Failed to connect to Pro Tools"

**Symptoms:**
- Script reports connection failure to localhost:50051
- Error message about gRPC connection refused

**Solutions:**

1. **Verify Pro Tools Scripting is Enabled**
   ```
   Pro Tools > Setup > Preferences > EUCON
   ☑ Enable EUCON & Pro Tools Scripting API
   ```
   Restart Pro Tools after enabling.

2. **Check Pro Tools is Running**
   - Pro Tools must be running with a session open
   - The Scripting API only starts when Pro Tools is active

3. **Verify Port Availability**
   ```bash
   lsof -i :50051
   ```
   Should show Pro Tools listening on port 50051

4. **Check Firewall Settings**
   - macOS: System Settings > Network > Firewall
   - Ensure localhost connections are not blocked

### Error: "Session not found" or "No session open"

**Solution:**
- Open a Pro Tools session before running the script
- The Scripting API requires an active session to perform operations

## MASV Upload Issues

### Error: "MASV_API_KEY not found"

**Solution:**
1. Verify `.env` file exists in project root
2. Check it contains:
   ```
   MASV_API_KEY=your_actual_key_here
   MASV_TEAM_ID=your_actual_team_id_here
   ```
3. Get credentials from: https://massive.io > Account Settings > API

### Error: "HTTP 401 Unauthorized"

**Solution:**
- Your API key is invalid or expired
- Generate a new API key from MASV dashboard
- Update `.env` file with new key

### Error: "HTTP 403 Forbidden"

**Solution:**
- Your API key doesn't have permission to create packages
- Check team permissions in MASV dashboard
- Ensure you're using a Team API key, not a Portal key

### Upload Stalls or Times Out

**Solutions:**
1. **Check Internet Connection**
   ```bash
   ping massive.app
   ```

2. **File Size Issues**
   - MASV supports large files, but check your account limits
   - Very large files may take significant time

3. **Network Firewall**
   - Corporate networks may block large uploads
   - Try from a different network

## Python/Environment Issues

### Error: "ModuleNotFoundError: No module named 'grpc'"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Verify you see (venv) in your prompt
# Then reinstall dependencies
pip install -r requirements.txt
```

### Error: "Python version not supported"

**Solution:**
- This project requires Python 3.8+
- Check version: `python3 --version`
- Install newer Python if needed: https://www.python.org/downloads/

### Import Errors with Generated gRPC Code

**Solution:**
```bash
# Regenerate the gRPC code
./venv/bin/python -m grpc_tools.protoc \
  -I. \
  --python_out=./generated \
  --grpc_python_out=./generated \
  PTSL.2025.06.0.proto

# Verify files were created
ls -la generated/PTSL/2025/06/
```

## Keyboard Maestro Issues

### Hotkey Does Nothing

**Solutions:**

1. **Check Keyboard Maestro is Running**
   - Look for KM icon in menu bar
   - Ensure macro is enabled (green light)

2. **Verify Macro Scope**
   - If set to "Pro Tools only", make sure Pro Tools is frontmost
   - Try setting to "All Applications" for testing

3. **Check Script Path**
   - Open macro in KM Editor
   - Verify the full absolute path is correct
   - No `~` or relative paths

4. **Test Script Directly**
   ```bash
   cd /path/to/masv-protools-integration
   ./bounce_and_send.sh
   ```

### Script Runs But No GUI Appears

**Solution:**
- The script might be running in CLI mode
- Edit `bounce_and_send.sh` and ensure it calls:
  ```bash
  python3 src/bounce_and_send.py
  # NOT: python3 src/bounce_and_send.py --cli
  ```

## Bounce/Export Issues

### Error: "Export failed" or "Bounce failed"

**Solutions:**

1. **Check Session Playback Range**
   - Ensure there's a selection or session has content
   - Pro Tools needs content to bounce

2. **Disk Space**
   ```bash
   df -h ~/Desktop/ProTools_Bounces
   ```
   - Ensure sufficient space for bounce file

3. **Output Directory Permissions**
   ```bash
   ls -ld ~/Desktop/ProTools_Bounces
   ```
   - Should be writable by your user

4. **Pro Tools Bounce Settings**
   - Some bounce settings may not be supported via API
   - Try adjusting `.env` settings:
     ```
     DEFAULT_BOUNCE_FORMAT=WAV
     DEFAULT_BIT_DEPTH=24
     DEFAULT_SAMPLE_RATE=48000
     ```

## General Debugging

### Enable Verbose Logging

Add this to the top of `src/bounce_and_send.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Components Individually

**Test Pro Tools Connection:**
```python
from src.protools import ProToolsClient
pt = ProToolsClient()
pt.connect()
info = pt.get_session_info()
print(info)
pt.disconnect()
```

**Test MASV Upload:**
```python
from src.masv import MASVClient
masv = MASVClient('your_api_key', 'your_team_id')
# Create a small test file
import os
with open('/tmp/test.txt', 'w') as f:
    f.write('test')
masv.send_file('/tmp/test.txt', ['your@email.com'])
```

## Getting Help

If you're still experiencing issues:

1. **Check the README**: [README.md](README.md)
2. **Review Pro Tools SDK Docs**: Download from https://developer.avid.com/scripting/
3. **Check MASV API Docs**: https://developer.massive.io/
4. **Create an Issue**: Include:
   - Error message (full traceback)
   - Pro Tools version
   - Python version (`python3 --version`)
   - Operating system
   - Steps to reproduce
