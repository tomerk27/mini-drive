"""
Dispatches incoming TLV commands from the API server to the correct handler.
"""

from shared.protocol import CommandType, SecureTransport, Packet
from services.storage_service import StorageService


def route_command(transport: SecureTransport, packet: Packet):
    """
    Routes a received packet to the appropriate StorageService handler.

    Called for every packet received on the persistent connection to the
    API server DataServer. Unknown commands are logged and ignored.

    Args:
        transport: The encrypted transport for sending responses back.
        packet: The decoded TLV packet with command type and fields.
    """
    try:
        if packet.command == CommandType.UPLOAD:
            StorageService.handle_upload(transport, packet.fields)
        elif packet.command == CommandType.DOWNLOAD:
            StorageService.handle_download(transport, packet.fields)
        elif packet.command == CommandType.DELETE:
            StorageService.handle_delete(transport, packet.fields)
        else:
            print(f"[!] Unknown command: {packet.command}")

    except Exception as e:
        print(f"[!] Error routing command: {e}")
