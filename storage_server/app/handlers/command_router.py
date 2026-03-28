from shared.protocol import CommandType, Field, unpack
from app.services.storage_service import StorageService

def route_command(client_socket, decrypted_data):
    """Unpacks the generic message and routes it to the appropriate service."""
    try:
        command, fields = unpack(decrypted_data)

        if command == CommandType.UPLOAD:
            StorageService.handle_upload(client_socket, fields)
        elif command == CommandType.DOWNLOAD:
            StorageService.handle_download(client_socket, fields)
        elif command == CommandType.DELETE:
            StorageService.handle_delete(client_socket, fields)
        else:
            print(f"[!] Unknown command: {command}")
            
    except Exception as e:
        print(f"[!] Error routing command: {e}")
