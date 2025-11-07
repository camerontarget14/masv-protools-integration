#!/usr/bin/env python3
"""Test complete workflow: bounce and send to MASV."""

import os
import sys

from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.masv import MASVClient
from src.protools import ProToolsClient


def main():
    """Test the complete workflow."""
    load_dotenv()

    # Configuration
    masv_api_key = os.getenv("MASV_API_KEY")
    masv_team_id = os.getenv("MASV_TEAM_ID")
    protools_host = os.getenv("PROTOOLS_HOST", "localhost")
    protools_port = int(os.getenv("PROTOOLS_PORT", "31416"))

    # Test recipient - change this to a real email to test
    recipients = ["test@example.com"]  # Change to your email for testing

    print("=" * 60)
    print("TESTING COMPLETE WORKFLOW")
    print("=" * 60)
    print(f"Recipients: {', '.join(recipients)}")
    print()

    try:
        # Step 1: Bounce from Pro Tools
        print("Step 1: Bouncing from Pro Tools...")
        with ProToolsClient(protools_host, protools_port) as pt:
            session_info = pt.get_session_info()
            session_name = session_info.get("session_name", "untitled")
            print(f"  Session: {session_name}")

            bounce_path = pt.bounce_to_disk(
                output_path="",  # Not used - bounces to session folder
                file_name=session_name,
                file_type="WAV",
                bit_depth=24,
                sample_rate=48000,
            )
            print(f"  Bounced to: {bounce_path}")

        # Step 2: Upload to MASV
        print("\nStep 2: Uploading to MASV...")
        masv = MASVClient(masv_api_key, masv_team_id)
        package_id = masv.send_file(
            bounce_path, recipients, description=f"Pro Tools Bounce: {session_name}"
        )

        print("\n" + "=" * 60)
        print("✓ SUCCESS!")
        print(f"  File: {bounce_path}")
        print(f"  Package ID: {package_id}")
        print(f"  Recipients: {', '.join(recipients)}")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
