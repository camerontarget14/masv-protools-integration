#!/usr/bin/env python3
"""
Bounce and Send - Pro Tools to MASV Integration

This script bounces the current Pro Tools session and uploads it to MASV.
Can be triggered manually or via Keyboard Maestro.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Try to import tkinter, but make it optional
try:
    import tkinter as tk
    from tkinter import messagebox, simpledialog

    HAS_GUI = True
except ImportError:
    HAS_GUI = False
    print("Note: GUI not available (tkinter not installed). Using CLI mode.")

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.protools import ProToolsClient
from src.masv import MASVClient


class BounceAndSendApp:
    """Main application for bouncing Pro Tools sessions and sending via MASV."""

    def __init__(self):
        """Initialize the application."""
        # Load environment variables
        load_dotenv()

        self.masv_api_key = os.getenv("MASV_API_KEY")
        self.masv_team_id = os.getenv("MASV_TEAM_ID")
        self.protools_host = os.getenv("PROTOOLS_HOST", "localhost")
        self.protools_port = int(os.getenv("PROTOOLS_PORT", "50051"))

        # Bounce settings
        self.bounce_format = os.getenv("DEFAULT_BOUNCE_FORMAT", "WAV")
        self.bit_depth = int(os.getenv("DEFAULT_BIT_DEPTH", "24"))
        self.sample_rate = int(os.getenv("DEFAULT_SAMPLE_RATE", "48000"))

        # Bounce output directory
        self.bounce_dir = os.path.expanduser("~/Desktop/ProTools_Bounces")
        os.makedirs(self.bounce_dir, exist_ok=True)

    def validate_config(self):
        """Validate that all required configuration is present."""
        if not self.masv_api_key:
            raise ValueError("MASV_API_KEY not found in .env file")
        if not self.masv_team_id:
            raise ValueError("MASV_TEAM_ID not found in .env file")

    def bounce_and_send(self, recipients):
        """
        Main workflow: bounce Pro Tools session and send to MASV.

        Args:
            recipients: List of recipient email addresses
        """
        try:
            # Validate configuration
            self.validate_config()

            # Connect to Pro Tools
            print("=" * 60)
            print("BOUNCE AND SEND TO MASV")
            print("=" * 60)

            with ProToolsClient(self.protools_host, self.protools_port) as pt:
                # Get session info
                session_info = pt.get_session_info()
                session_name = session_info.get("session_name", "untitled")
                print(f"\nSession: {session_name}")

                # Bounce to disk
                print(f"\nBouncing to: {self.bounce_dir}")
                bounce_path = pt.bounce_to_disk(
                    self.bounce_dir,
                    file_name=session_name,
                    file_type=self.bounce_format,
                    bit_depth=self.bit_depth,
                    sample_rate=self.sample_rate,
                )

            # Upload to MASV
            print(f"\nSending to: {', '.join(recipients)}")
            masv = MASVClient(self.masv_api_key, self.masv_team_id)
            package_id = masv.send_file(
                bounce_path, recipients, description=f"Pro Tools Bounce: {session_name}"
            )

            print("\n" + "=" * 60)
            print(f"✓ SUCCESS!")
            print(f"  File: {bounce_path}")
            print(f"  Package ID: {package_id}")
            print(f"  Recipients: {', '.join(recipients)}")
            print("=" * 60)

            return bounce_path, package_id

        except Exception as e:
            print(f"\n✗ ERROR: {str(e)}")
            raise

    def run_cli(self):
        """Run in command-line mode."""
        print("Pro Tools Bounce and Send to MASV")
        print("-" * 40)

        # Get recipients
        recipients_input = input(
            "\nEnter recipient email addresses (comma-separated): "
        )
        recipients = [
            email.strip() for email in recipients_input.split(",") if email.strip()
        ]

        if not recipients:
            print("No recipients provided. Exiting.")
            return

        # Execute bounce and send
        self.bounce_and_send(recipients)

    def run_gui(self):
        """Run with GUI dialog."""
        root = tk.Tk()
        root.withdraw()  # Hide main window

        # Get recipients via dialog
        recipients_str = simpledialog.askstring(
            "Bounce and Send",
            "Enter recipient email addresses\n(comma-separated):",
            parent=root,
        )

        if not recipients_str:
            messagebox.showinfo("Cancelled", "No recipients provided.")
            return

        recipients = [
            email.strip() for email in recipients_str.split(",") if email.strip()
        ]

        try:
            # Execute bounce and send
            bounce_path, package_id = self.bounce_and_send(recipients)

            # Show success message
            messagebox.showinfo(
                "Success!",
                f"Bounce sent successfully!\n\n"
                f"File: {Path(bounce_path).name}\n"
                f"Package ID: {package_id}\n"
                f"Recipients: {', '.join(recipients)}",
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to bounce and send:\n\n{str(e)}")


def main():
    """Main entry point."""
    app = BounceAndSendApp()

    # Check if running in GUI mode (default) or CLI mode
    if "--cli" in sys.argv or not HAS_GUI:
        app.run_cli()
    else:
        if not HAS_GUI:
            print(
                "Error: GUI mode requires tkinter. Use --cli flag or install tkinter."
            )
            sys.exit(1)
        app.run_gui()


if __name__ == "__main__":
    main()
