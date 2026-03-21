from shared.protocol import receive_decrypted_packet
from app.handlers.command_router import route_command

def handle_client(client_socket, address, key):
    """Handles an individual client connection."""
    print(f"[*] Connection from {address[0]}:{address[1]}")
    
    try:
        # Receive and decrypt the meta packet (header + filename)
        decrypted_data = receive_decrypted_packet(client_socket, key)
        if not decrypted_data:
            return

        # Route the command
        route_command(client_socket, decrypted_data, key)
            
    except Exception as e:
        print(f"[!] Error handling client {address}: {e}")
    finally:
        print(f"[*] Closing connection with {address[0]}")
        client_socket.close()
