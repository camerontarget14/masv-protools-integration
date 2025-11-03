#!/usr/bin/env python3
"""Test that all imports work correctly."""

print("Testing imports...")

try:
    from src.protools import ProToolsClient

    print("✓ ProToolsClient imported successfully")
except Exception as e:
    print(f"✗ ProToolsClient import failed: {e}")
    exit(1)

try:
    from src.masv import MASVClient

    print("✓ MASVClient imported successfully")
except Exception as e:
    print(f"✗ MASVClient import failed: {e}")
    exit(1)

print("\n✓ All imports successful!")
print("\nNext steps:")
print("1. Configure your .env file with MASV credentials")
print("2. Make sure Pro Tools is running with a session open")
print("3. Enable Pro Tools Scripting (if required for your version)")
print("4. Run: python3 src/bounce_and_send.py --cli")
