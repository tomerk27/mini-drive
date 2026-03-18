import socket
import threading
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared import (
    unpack_header, 
    HEADER_FIXED_SIZE,
    CommandType
)

from actions import handle_upload, handle_download

PORT = 9000
HOST = "0.0.0.0"

def receive_exactly(sock, n):
    """Utility to receive exactly n bytes from a socket."""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def handle_client(client_socket, address):
    """Handles an individual client connection."""
    print(f"[*] Connection from {address[0]}:{address[1]}")
    
    try:
        # Read the 13-byte header
        header_data = receive_exactly(client_socket, HEADER_FIXED_SIZE)
        if not header_data:
            return

        # Unpack metadata
        command, name_len, file_size = unpack_header(header_data)

        # Read the filename
        filename_data = receive_exactly(client_socket, name_len)
        if not filename_data:
            return
        filename = filename_data.decode('utf-8')

        # Route the command
        if command == CommandType.UPLOAD:
            handle_upload(client_socket, filename, file_size)
        elif command == CommandType.DOWNLOAD:
            handle_download(client_socket, filename)
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
        print(f"[*] Storage Server is alive and listening on {HOST}:{PORT}")

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
