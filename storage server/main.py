import socket
import threading
import os
import sys

# Add project root to sys.path for shared module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.handlers.socket_handler import handle_client

def start_server():
    """Initializes the server socket and listens for incoming connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((settings.HOST, settings.PORT))
        server_socket.listen(10)
        print(f"[*] Storage Server (Encrypted) is alive and listening on {settings.HOST}:{settings.PORT}")

        key = settings.STORAGE_ENCRYPTION_KEY.encode()

        while True:
            client_sock, address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_sock, address, key)
            )
            client_thread.start()
            
    except Exception as e:
        print(f"[!] Server Startup Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
