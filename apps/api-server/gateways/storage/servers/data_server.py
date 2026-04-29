"""
data_server.py

Listens on port 9000 for incoming TCP connections from storage nodes.
When a node connects it sends a REGISTER packet identifying itself; the
DataServer stores that socket in the connection pool so StorageClient can
reuse it for UPLOAD/DOWNLOAD/DELETE commands later.

Each accepted connection is handled in its own daemon thread.  The socket
stays open indefinitely — if it dies, the next failed storage operation
will remove the stale entry from the pool.
"""

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
        # Bind to all interfaces so nodes on any network can reach this server
        self.host = "0.0.0.0"
        self.port = settings.STORAGE_SERVER_PORT
        # Convert the Fernet key string to bytes for SecureTransport
        self.key = settings.STORAGE_ENCRYPTION_KEY.encode()

    def _enable_keepalive(self, conn: socket.socket):
        """
        Activates TCP keepalive on a registered node socket.

        Keepalive probes detect silently-dropped connections so stale sockets
        are caught before the next storage command fails.  Intervals are tuned
        conservatively: first probe after 60 s, then every 10 s, give up after 5.

        Args:
            conn: The connected socket to configure.
        """
        conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # TCP_KEEPIDLE / KEEPINTVL / KEEPCNT are Linux-only; skip on macOS/Windows
        if hasattr(socket, "TCP_KEEPIDLE"):
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
        if hasattr(socket, "TCP_KEEPINTVL"):
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
        if hasattr(socket, "TCP_KEEPCNT"):
            conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

    def handle_connection(self, conn: socket.socket, address: tuple):
        """
        Handles a single incoming connection from a storage node.

        Expects the first packet to be a REGISTER command containing the node's
        ID.  On success the socket is handed off to the connection pool and kept
        open for future UPLOAD/DOWNLOAD/DELETE commands.  Any other command or
        failure closes the socket immediately.

        Args:
            conn: The accepted client socket.
            address: (ip, port) tuple of the connecting node.
        """
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
                    # Leave the socket open — StorageClient reuses it for all future commands.
                    # When the socket dies, the next failed operation removes it from the pool.
                    return

            # Any unexpected command from an unregistered connection is rejected
            conn.close()
        except Exception as e:
            print(f"[!] DataServer Error during registration from {address[0]}: {e}")
            conn.close()

    def start(self):
        """
        Binds the server socket and enters the accept loop.

        Spawns a daemon thread per connection so the accept loop is never
        blocked waiting for a node to finish its registration handshake.
        """
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow fast restarts without waiting for the OS to release the port
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
