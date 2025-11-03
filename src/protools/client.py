"""Pro Tools Scripting API Client Wrapper."""

import grpc
import sys
import os

# Add generated directory to path
generated_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../generated")
)
sys.path.insert(0, generated_path)

# Import generated gRPC code
# Note: The proto file generates modules at PTSL/2025/06/0_pb2.py
try:
    from PTSL._2025._06 import _0_pb2 as ptsl_pb2
    from PTSL._2025._06 import _0_pb2_grpc as ptsl_pb2_grpc
except ImportError:
    # Alternative import path
    import importlib.util

    pb2_path = os.path.join(generated_path, "PTSL/2025/06/0_pb2.py")
    grpc_path = os.path.join(generated_path, "PTSL/2025/06/0_pb2_grpc.py")

    spec_pb2 = importlib.util.spec_from_file_location("ptsl_pb2", pb2_path)
    ptsl_pb2 = importlib.util.module_from_spec(spec_pb2)
    spec_pb2.loader.exec_module(ptsl_pb2)

    spec_grpc = importlib.util.spec_from_file_location("ptsl_pb2_grpc", grpc_path)
    ptsl_pb2_grpc = importlib.util.module_from_spec(spec_grpc)
    spec_grpc.loader.exec_module(ptsl_pb2_grpc)


class ProToolsClient:
    """Client for interacting with Pro Tools via the Scripting API."""

    def __init__(self, host="localhost", port=50051):
        """
        Initialize Pro Tools client.

        Args:
            host: Pro Tools Scripting API host (default: localhost)
            port: Pro Tools Scripting API port (default: 50051)
        """
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None

    def connect(self):
        """Establish connection to Pro Tools."""
        address = f"{self.host}:{self.port}"
        print(f"Connecting to Pro Tools at {address}...")

        self.channel = grpc.insecure_channel(address)
        self.stub = ptsl_pb2_grpc.PTSLStub(self.channel)

        print("Connected to Pro Tools!")

    def disconnect(self):
        """Close connection to Pro Tools."""
        if self.channel:
            self.channel.close()
            print("Disconnected from Pro Tools")

    def get_session_info(self):
        """
        Get information about the currently open Pro Tools session.

        Returns:
            dict: Session information including name, path, sample rate, etc.
        """
        # Create request header
        header = ptsl_pb2.RequestHeader(command=ptsl_pb2.GetSessionName, version=1)

        # Create request
        request = ptsl_pb2.Request(header=header)

        # Send request
        response = self.stub.SendGrpcRequest(request)

        if response.header.status != ptsl_pb2.ResponseStatus_Success:
            raise Exception(
                f"Failed to get session info: {response.response_error_json}"
            )

        # Parse response
        import json

        session_data = json.loads(response.response_body_json)

        return session_data

    def bounce_to_disk(self, output_path, file_name=None, **options):
        """
        Bounce/export the current Pro Tools session to disk.

        Args:
            output_path: Directory path where the bounce will be saved
            file_name: Name for the bounced file (optional, uses session name if not provided)
            **options: Additional bounce options:
                - file_type: Export file type (default: 'WAV')
                - bit_depth: Bit depth (default: 24)
                - sample_rate: Sample rate (default: 48000)
                - audio_format: Audio format (default: 'Interleaved')
                - offline_bounce: Use offline bounce (default: True)

        Returns:
            str: Path to the bounced file
        """
        # Set defaults
        file_type = options.get("file_type", "WAV")
        bit_depth = options.get("bit_depth", 24)
        sample_rate = options.get("sample_rate", 48000)
        offline_bounce = options.get("offline_bounce", True)

        # Get session name if file_name not provided
        if not file_name:
            session_info = self.get_session_info()
            file_name = session_info.get("session_name", "bounce")

        # Build export mix request
        import json

        request_body = {
            "file_name": file_name,
            "file_type": file_type,
            "location_info": {"file_destination": "Custom", "directory": output_path},
            "audio_info": {
                "export_format": "WAV",
                "bit_depth": bit_depth,
                "sample_rate": sample_rate,
                "delivery_format": "Interleaved",
            },
            "offline_bounce": offline_bounce,
            "mix_source_list": [{"source_type": "EntireMix"}],
        }

        # Create request header
        header = ptsl_pb2.RequestHeader(command=ptsl_pb2.ExportMix, version=1)

        # Create request
        request = ptsl_pb2.Request(
            header=header, request_body_json=json.dumps(request_body)
        )

        # Send request
        print(f"Bouncing to {output_path}/{file_name}...")
        response = self.stub.SendGrpcRequest(request)

        if response.header.status != ptsl_pb2.ResponseStatus_Success:
            error_msg = (
                response.response_error_json
                if response.response_error_json
                else "Unknown error"
            )
            raise Exception(f"Bounce failed: {error_msg}")

        bounce_path = os.path.join(output_path, f"{file_name}.{file_type.lower()}")
        print(f"Bounce complete: {bounce_path}")

        return bounce_path

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
