from shared.protocol import CommandType, unpack_header
from app.services.storage_service import StorageService

def route_command(client_socket, decrypted_data, key):
    """Unpacks the header and routes the command to the appropriate service."""
    try:
        command, file_size, filename = unpack_header(decrypted_data)

        if command == CommandType.UPLOAD:
            StorageService.handle_upload(client_socket, filename, file_size, key)
        elif command == CommandType.DOWNLOAD:
            StorageService.handle_download(client_socket, filename, key)
        elif command == CommandType.DELETE:
            StorageService.handle_delete(client_socket, filename, key)
        else:
            print(f"[!] Unknown command: {command}")
            
    except Exception as e:
        print(f"[!] Error routing command: {e}")
