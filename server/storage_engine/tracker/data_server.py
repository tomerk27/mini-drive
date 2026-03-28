import socket
import threading
from common.core.config import settings
from shared.protocol import ( CommandType, Field, unpack, receive_decrypted_packet )
from storage_engine.tracker.connection_pool import connection_pool

class DataServer:
    """
    TCP Listener on the Main Server that waits for Storage Nodes to connect.
    Maintains persistent connections for UPLOAD/DOWNLOAD operations.
    """
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 9000
        self.key = getattr(settings, "STORAGE_ENCRYPTION_KEY", "").encode()

    def handle_initial_connection(self, client_socket, address):
        """Waits for the node to identify itself via a REGISTER packet."""
        try:
            # Receive and decrypt the registration packet
            decrypted_data = receive_decrypted_packet(client_socket, self.key)
            if not decrypted_data:
                client_socket.close()
                return

            # Unpack and verify registration
            command, fields = unpack(decrypted_data)
            if command == CommandType.REGISTER:
                node_id = fields.get(Field.NODE_ID)
                if node_id:
                    # Add to pool and keep socket open!
                    connection_pool.register_node(node_id, client_socket)
                    print(f"[*] DataServer: Node {node_id} reported for duty from {address[0]}")
                    return # Do NOT close the socket, we need it for later
                
            client_socket.close()
        except Exception as e:
            print(f"[!] DataServer Error during registration from {address[0]}: {e}")
            client_socket.close()

    def start(self):
        """Starts the listener loop."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(20)
            print(f"[*] Main Data Listener is alive on {self.host}:{self.port} (Waiting for nodes...)")

            while True:
                client_sock, address = server_socket.accept()
                # Use a small timeout for the registration phase
                client_sock.settimeout(10)
                
                # Hand off to a thread to register the node
                t = threading.Thread(
                    target=self.handle_initial_connection, 
                    args=(client_sock, address)
                )
                t.daemon = True
                t.start()
                
        except Exception as e:
            print(f"[!] DataServer Startup Error: {e}")
        finally:
            server_socket.close()
