#!/usr/bin/env python3
"""Test script to find available Pro Tools outputs."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.protools import ProToolsClient


def main():
    """Query Pro Tools for available information."""
    try:
        with ProToolsClient() as pt:
            print("Connected to Pro Tools!")
            print()

            # Get session info
            session_info = pt.get_session_info()
            print(f"Session: {session_info.get('session_name', 'Unknown')}")
            print()

            # Try to get track list to see what outputs tracks are using
            print("Attempting to get track list...")
            import importlib.util
            import json

            # Import the protobuf module the same way the client does
            generated_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "generated")
            )
            pb2_path = os.path.join(generated_path, "PTSL/2025/06/0_pb2.py")
            spec_pb2 = importlib.util.spec_from_file_location("ptsl_pb2", pb2_path)
            ptsl_pb2 = importlib.util.module_from_spec(spec_pb2)
            spec_pb2.loader.exec_module(ptsl_pb2)

            header = ptsl_pb2.RequestHeader(
                command=ptsl_pb2.CId_GetTrackList, version=1, session_id=pt.session_id
            )

            request_body = {}
            request = ptsl_pb2.Request(
                header=header, request_body_json=json.dumps(request_body)
            )

            response = pt.stub.SendGrpcRequest(request)

            if response.header.status == ptsl_pb2.TStatus_Completed:
                track_data = json.loads(response.response_body_json)
                print("Track List Response:")
                print(json.dumps(track_data, indent=2))
            else:
                print(f"Failed to get track list: {response.response_error_json}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
