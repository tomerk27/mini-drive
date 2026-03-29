from shared.protocol import CommandType, AsyncSecureTransport, Packet
from app.services.storage_service import StorageService

async def route_command(transport: AsyncSecureTransport, packet: Packet):
    """Routes the packet to the appropriate service."""
    try:
        if packet.command == CommandType.UPLOAD:
            await StorageService.handle_upload(transport, packet.fields)
        elif packet.command == CommandType.DOWNLOAD:
            await StorageService.handle_download(transport, packet.fields)
        elif packet.command == CommandType.DELETE:
            await StorageService.handle_delete(transport, packet.fields)
        else:
            print(f"[!] Unknown command: {packet.command}")
            
    except Exception as e:
        print(f"[!] Error routing command: {e}")
