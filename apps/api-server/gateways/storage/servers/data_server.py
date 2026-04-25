import socket
import threading
from core.config import settings
from shared.protocol import CommandType, Field, Packet, SecureTransport, ProtocolError
from gateways.storage.servers.connection_pool import connection_pool


class DataServer:
    """
    TCP listener that waits for Storage Nodes to connect and register.
    Maintains persistent socket connections used for UPLOAD/DOWNLOAD/DELETE operations.
    Each incoming connection is handled in a dedicated daemon thread.
    """
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = settings.STORAGE_SERVER_PORT
        self.key = settings.STORAGE_ENCRYPTION_KEY.encode()

    def _enable_keepalive(self, conn: socket.socket):
        conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        if hasattr(socket, "TCP_KEEPIDLE"):
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
        if hasattr(socket, "TCP_KEEPINTVL"):
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
        if hasattr(socket, "TCP_KEEPCNT"):
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

    def handle_connection(self, conn: socket.socket, address):
        transport = SecureTransport(conn, self.key)
        try:
            packet = transport.receive_packet()
            if not packet:
                conn.close()
                return

            if packet.command == CommandType.REGISTER:
                node_id = packet.fields.get(Field.NODE_ID)
                if node_id:
                    self._enable_keepalive(conn)
                    connection_pool.register_node(node_id, conn)
                    print(f"[*] DataServer: Node {node_id} reported for duty from {address[0]}")
                    # Keep conn open — StorageClient will use it for future commands.
                    # When the socket dies, the next failed operation will remove it from the pool.
                    return

            conn.close()
        except Exception as e:
            print(f"[!] DataServer Error during registration from {address[0]}: {e}")
            conn.close()

    def start(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.host, self.port))
        server_sock.listen(10)
        print(f"[*] DataServer is listening on {self.host}:{self.port} (waiting for nodes...)")

        while True:
            try:
                conn, address = server_sock.accept()
                threading.Thread(
                    target=self.handle_connection,
                    args=(conn, address),
                    daemon=True
                ).start()
            except Exception as e:
                print(f"[!] DataServer accept error: {e}")
