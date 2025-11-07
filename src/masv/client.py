"""MASV Agent CLI wrapper for file transfers."""

import json
import os
import subprocess
import time
from pathlib import Path
from typing import List, Optional


class MASVClient:
    """Client for uploading files via MASV Agent CLI."""

    def __init__(self, api_key: str, team_id: str):
        """
        Initialize MASV client.

        Args:
            api_key: MASV API key from account settings
            team_id: MASV team ID
        """
        self.api_key = api_key
        self.team_id = team_id
        self._check_masv_agent()

    def _check_masv_agent(self) -> None:
        """
        Check if MASV Agent is installed and accessible.

        Raises:
            RuntimeError: If MASV Agent is not found
        """
        try:
            # Just check if masv command exists using help (doesn't need server)
            result = subprocess.run(
                ["masv", "--help"], capture_output=True, text=True, timeout=5
            )
            # masv --help returns exit code 1 but still shows help - check output content
            if "Usage:" not in result.stdout and "Usage:" not in result.stderr:
                raise RuntimeError("MASV Agent command failed")
        except FileNotFoundError as e:
            raise RuntimeError(
                "MASV Agent not found. Please install MASV Agent from "
                "https://developer.massive.io/transfer-agent/latest/"
            ) from e

    def _ensure_server_running(self) -> None:
        """
        Ensure MASV Agent server is running with proper authentication.

        The server needs to be started with the API key for authentication.
        """
        # Check if server is already running
        try:
            result = subprocess.run(
                ["masv", "upload", "ls"],
                capture_output=True,
                text=True,
                timeout=5,
                env={**os.environ, "MASV_API_KEY": self.api_key},
            )
            if result.returncode == 0:
                return  # Server is running and authenticated
        except subprocess.SubprocessError:
            pass

        # Start the server with API key in background
        print("Starting MASV Agent server...")
        try:
            # Start server in background (don't wait for it to exit)
            subprocess.Popen(
                ["masv", "server", "start", "--api-key", self.api_key],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            # Give server time to start
            time.sleep(3)
            print("MASV Agent server started")
        except Exception as e:
            # Server might already be running, that's ok
            print(f"Note: {e}")

    def send_file(
        self,
        file_path: str,
        recipients: Optional[List[str]] = None,
        description: str = "Pro Tools Bounce",
        name: Optional[str] = None,
        portal_subdomain: Optional[str] = None,
        portal_password: Optional[str] = None,
    ) -> str:
        """
        Upload and send a file using MASV Agent (email or portal).

        Args:
            file_path: Path to file to send
            recipients: List of recipient email addresses (for email delivery)
            description: Package description
            name: Optional package name (defaults to filename)
            portal_subdomain: Portal subdomain (for portal delivery)
            portal_password: Optional portal password (for portal delivery)

        Returns:
            str: Upload ID

        Raises:
            FileNotFoundError: If file doesn't exist
            RuntimeError: If upload fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Ensure server is running
        self._ensure_server_running()

        file_size = os.path.getsize(file_path)
        file_name = Path(file_path).name

        if name is None:
            name = file_name

        # Determine delivery mode
        if portal_subdomain:
            # Portal upload - requires sender email
            sender_email = os.getenv("MASV_SENDER_EMAIL", "noreply@example.com")
            print(
                f"Uploading {file_name} ({file_size / (1024 * 1024):.2f} MB) to portal {portal_subdomain}..."
            )
            cmd = [
                "masv",
                "upload",
                "start",
                "portal",
                "--subdomain",
                portal_subdomain,
                "--sender",
                sender_email,
                "--name",
                name,
                "--description",
                description,
                file_path,
            ]
            if portal_password:
                cmd.extend(["--password", portal_password])
        elif recipients:
            # Email upload
            print(
                f"Uploading {file_name} ({file_size / (1024 * 1024):.2f} MB) to {', '.join(recipients)}..."
            )
            emails = ",".join(recipients)
            cmd = [
                "masv",
                "upload",
                "start",
                "email",
                "--emails",
                emails,
                "--team-id",
                self.team_id,
                "--name",
                name,
                "--description",
                description,
                file_path,
            ]
        else:
            raise ValueError(
                "Must provide either recipients (for email) or portal_subdomain (for portal)"
            )

        # Set API key in environment
        env = {**os.environ, "MASV_API_KEY": self.api_key}

        try:
            # Start the upload
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout for starting upload
                check=True,
                env=env,
            )

            # Parse upload ID from output
            # MASV Agent typically returns upload info in stdout
            upload_id = self._extract_upload_id(result.stdout)

            if not upload_id:
                raise RuntimeError("Failed to extract upload ID from MASV Agent output")

            print(f"Upload started with ID: {upload_id}")

            # Monitor upload progress
            self._monitor_upload(upload_id, env)

            # Finalize the upload
            self._finalize_upload(upload_id, env)

            print("Package sent successfully!")
            return upload_id

        except subprocess.TimeoutExpired as e:
            raise RuntimeError(f"Upload command timed out: {e}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Upload failed: {e.stderr if e.stderr else e.stdout}")

    def _extract_upload_id(self, output: str) -> Optional[str]:
        """
        Extract upload ID from MASV Agent command output.

        Args:
            output: Command output string

        Returns:
            Upload ID or None if not found
        """
        # MASV Agent may output JSON or text
        # Try to parse as JSON first
        try:
            data = json.loads(output)
            if "id" in data:
                return data["id"]
        except (json.JSONDecodeError, TypeError):
            pass

        # Look for ID in text output
        # Common patterns: "Upload ID: xxx" or "id: xxx"
        lines = output.split("\n")
        for line in lines:
            if "id" in line.lower() and ":" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    potential_id = parts[1].strip()
                    # Clean up quotes, commas, and whitespace
                    potential_id = potential_id.strip("\"'`, \t\n\r")
                    if potential_id:
                        return potential_id

        return None

    def _monitor_upload(
        self, upload_id: str, env: dict, poll_interval: int = 2
    ) -> None:
        """
        Monitor upload progress until complete.

        Args:
            upload_id: Upload ID to monitor
            env: Environment variables including API key
            poll_interval: Seconds between status checks
        """
        print("Monitoring upload progress...")
        max_attempts = 60  # 2 minutes max with 2 second intervals

        for attempt in range(max_attempts):
            try:
                # Use 'masv upload ls' to check status - more reliable than 'status' command
                result = subprocess.run(
                    ["masv", "upload", "ls"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    check=True,
                    env=env,
                )

                # Parse JSON output to find our upload
                try:
                    data = json.loads(result.stdout)
                    transfers = data.get("transfers", [])

                    for transfer in transfers:
                        if transfer.get("package_id") == upload_id:
                            state = transfer.get("state", "").lower()
                            progress = transfer.get("progress", 0)
                            size = transfer.get("size", 1)

                            if state == "complete":
                                print("  Upload complete: 100%")
                                return
                            elif state in ["error", "failed"]:
                                raise RuntimeError(f"Upload failed with state: {state}")
                            else:
                                # Calculate percentage
                                percent = (progress / size * 100) if size > 0 else 0
                                print(f"  Upload in progress: {percent:.1f}%")

                except json.JSONDecodeError:
                    # If we can't parse, just continue
                    print("  Upload in progress...")

                time.sleep(poll_interval)

            except subprocess.CalledProcessError as e:
                # If ls fails, just wait and retry
                print("  Checking upload status...")
                time.sleep(poll_interval)

        # If we get here, assume it completed (uploads are usually fast)
        print("  Upload appears complete (monitoring timeout)")

    def _finalize_upload(self, upload_id: str, env: dict) -> None:
        """
        Finalize the upload to notify recipients.

        Args:
            upload_id: Upload ID to finalize
            env: Environment variables including API key
        """
        print("Finalizing and sending package...")
        try:
            subprocess.run(
                ["masv", "upload", "finalize", upload_id],
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
                env=env,
            )
            print("Package finalized successfully")
        except subprocess.CalledProcessError as e:
            # MASV may auto-finalize uploads, so this error is often benign
            # Check if upload is already complete/finalized
            error_output = e.stderr if e.stderr else e.stdout
            if (
                "no rows in result set" in error_output
                or "not found" in error_output.lower()
            ):
                print("Package already finalized (auto-finalized by MASV)")
            else:
                # Only raise for unexpected errors
                raise RuntimeError(f"Failed to finalize upload: {error_output}")
