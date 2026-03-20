import socket
import threading
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared import (
    unpack_header,
    receive_decrypted_packet,
    CommandType
)
from actions import handle_upload, handle_download

load_dotenv()
STORAGE_ENCRYPTION_KEY = os.getenv("STORAGE_ENCRYPTION_KEY", "").encode()

PORT = 9000
HOST = "0.0.0.0"

def handle_client(client_socket, address):
    """Handles an individual client connection."""
    print(f"[*] Connection from {address[0]}:{address[1]}")
    
    try:
        # Receive and decrypt the meta packet (header + filename)
        decrypted_data = receive_decrypted_packet(client_socket, STORAGE_ENCRYPTION_KEY)
        if not decrypted_data:
            return

        # Unpack metadata
        command, file_size, filename = unpack_header(decrypted_data)

        # Route the command
        if command == CommandType.UPLOAD:
            handle_upload(client_socket, filename, file_size, STORAGE_ENCRYPTION_KEY)
        elif command == CommandType.DOWNLOAD:
            handle_download(client_socket, filename, STORAGE_ENCRYPTION_KEY)
        else:
            print(f"[!] Unknown command: {command}")
            
    except Exception as e:
        print(f"[!] Error handling client {address}: {e}")
    finally:
        print(f"[*] Closing connection with {address[0]}")
        client_socket.close()

def start_server():
    """Initializes the server socket and listens for incoming connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
        print(f"[*] Storage Server (Encrypted) is alive and listening on {HOST}:{PORT}")

        while True:
            client_sock, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_sock, address))
            client_thread.start()
            
    except Exception as e:
        print(f"[!] Server Startup Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()