from shared.protocol import receive_decrypted_packet
from app.handlers.command_router import route_command
from app.core.config import settings

def handle_client(client_socket, address):
    """Handles an individual client connection."""
    print(f"[*] Connection from {address[0]}:{address[1]}")
    
    try:
        # Fetch key only when calling protocol functions
        key = settings.STORAGE_ENCRYPTION_KEY.encode()

        # Receive and decrypt the meta packet
        decrypted_data = receive_decrypted_packet(client_socket, key)
        if not decrypted_data:
            return

        # Route the command
        route_command(client_socket, decrypted_data)
            
    except Exception as e:
        print(f"[!] Error handling client {address}: {e}")
    finally:
        print(f"[*] Closing connection with {address[0]}")
        client_socket.close()
