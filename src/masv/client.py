"""MASV API Client for file transfers."""

import requests
import os
from pathlib import Path
from typing import List, Optional


class MASVClient:
    """Client for uploading files via MASV API."""

    def __init__(
        self, api_key: str, team_id: str, base_url: str = "https://api.massive.app/v1"
    ):
        """
        Initialize MASV client.

        Args:
            api_key: MASV API key from account settings
            team_id: MASV team ID
            base_url: MASV API base URL (default: https://api.massive.app/v1)
        """
        self.api_key = api_key
        self.team_id = team_id
        self.base_url = base_url

    def _headers(self, package_token: Optional[str] = None) -> dict:
        """
        Build request headers.

        Args:
            package_token: Optional package token for file operations

        Returns:
            dict: Request headers
        """
        headers = {"X-API-KEY": self.api_key, "Content-Type": "application/json"}
        if package_token:
            headers["X-Package-Token"] = package_token
        return headers

    def create_package(
        self, recipients: List[str], description: str = "Pro Tools Bounce"
    ) -> tuple:
        """
        Create a new MASV package.

        Args:
            recipients: List of recipient email addresses
            description: Package description

        Returns:
            tuple: (package_id, package_token)
        """
        url = f"{self.base_url}/teams/{self.team_id}/packages"
        payload = {
            "recipients": [{"email": email} for email in recipients],
            "description": description,
        }

        print(f"Creating MASV package for {', '.join(recipients)}...")
        response = requests.post(url, json=payload, headers=self._headers())
        response.raise_for_status()

        data = response.json()
        package_id = data["id"]
        package_token = data["token"]

        print(f"Package created: {package_id}")
        return package_id, package_token

    def upload_file(self, package_id: str, package_token: str, file_path: str) -> None:
        """
        Upload a file to a MASV package.

        Args:
            package_id: Package ID from create_package
            package_token: Package token from create_package
            file_path: Path to file to upload
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_size = os.path.getsize(file_path)
        file_name = Path(file_path).name

        print(f"Uploading {file_name} ({file_size / (1024 * 1024):.2f} MB)...")

        # Step 1: Add file to package
        add_file_url = f"{self.base_url}/packages/{package_id}/files"
        add_file_payload = {"name": file_name, "path": file_name, "size": file_size}

        response = requests.post(
            add_file_url, json=add_file_payload, headers=self._headers(package_token)
        )
        response.raise_for_status()
        file_data = response.json()
        file_id = file_data["id"]
        create_blueprint = file_data["create_blueprint"]

        # Step 2: Initialize multipart upload with S3
        s3_init_response = requests.post(
            create_blueprint["url"], data=create_blueprint["fields"]
        )
        s3_init_response.raise_for_status()

        # Step 3: Get upload URLs for chunks
        get_urls_url = f"{self.base_url}/packages/{package_id}/files/{file_id}"
        response = requests.post(get_urls_url, headers=self._headers(package_token))
        response.raise_for_status()

        upload_data = response.json()
        blueprints = upload_data["blueprints"]

        # Step 4: Upload file in chunks
        chunk_size = 5 * 1024 * 1024  # 5MB chunks
        parts = []

        with open(file_path, "rb") as f:
            for i, blueprint in enumerate(blueprints):
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                # Upload chunk to S3
                upload_response = requests.put(
                    blueprint["url"], data=chunk, headers=blueprint.get("headers", {})
                )
                upload_response.raise_for_status()

                parts.append(
                    {
                        "part_number": i + 1,
                        "etag": upload_response.headers["ETag"].strip('"'),
                    }
                )

                # Progress update
                progress = ((i + 1) / len(blueprints)) * 100
                print(f"  Progress: {progress:.1f}%")

        # Step 5: Finalize file upload
        finalize_file_url = (
            f"{self.base_url}/packages/{package_id}/files/{file_id}/finalize"
        )
        finalize_file_payload = {"parts": parts, "size": file_size}

        response = requests.post(
            finalize_file_url,
            json=finalize_file_payload,
            headers=self._headers(package_token),
        )
        response.raise_for_status()

        print(f"  Upload complete: {file_name}")

    def finalize_package(self, package_id: str, package_token: str) -> dict:
        """
        Finalize and send the package to recipients.

        Args:
            package_id: Package ID
            package_token: Package token

        Returns:
            dict: Package finalization response
        """
        url = f"{self.base_url}/packages/{package_id}/finalize"

        print("Finalizing and sending package...")
        response = requests.post(url, headers=self._headers(package_token))
        response.raise_for_status()

        print("Package sent successfully!")
        return response.json()

    def send_file(
        self,
        file_path: str,
        recipients: List[str],
        description: str = "Pro Tools Bounce",
    ) -> str:
        """
        Complete workflow: create package, upload file, and send.

        Args:
            file_path: Path to file to send
            recipients: List of recipient email addresses
            description: Package description

        Returns:
            str: Package ID
        """
        # Create package
        package_id, package_token = self.create_package(recipients, description)

        # Upload file
        self.upload_file(package_id, package_token, file_path)

        # Finalize and send
        self.finalize_package(package_id, package_token)

        return package_id
