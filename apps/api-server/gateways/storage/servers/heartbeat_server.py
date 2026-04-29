"""
heartbeat_server.py

Listens on port 9001 for heartbeat packets sent by storage nodes every 30 s.
Each heartbeat carries the node's ID, port, and free disk space.  The server
updates NodeRegistry with this information so the API server always knows which
nodes are alive and how much capacity they have.

A node that stops sending heartbeats for more than 2 minutes is marked OFFLINE
by the maintenance loop, which then triggers self-healing re-replication.

Each connection is short-lived: accept → read packet → send ACK → close.
A daemon thread is used for each connection so the accept loop stays responsive.
"""

import socket
import threading
from core.config import settings
from shared.protocol import CommandType, Field, Packet, SecureTransport, ProtocolError
from gateways.storage.services.node_registry import NodeRegistry


class HeartbeatServer:
    """
    TCP server that listens for periodic heartbeat pulses from storage nodes.
    Each heartbeat is handled in a short-lived daemon thread and updates the
    node's status and available capacity in the database.
    """
    def __init__(self):
        # Bind to all interfaces so nodes on any network can reach the tracker
        self.host = "0.0.0.0"
        # Port 9001 is the well-known tracker port; nodes read this from their .env
        self.port = 9001
        # Convert the Fernet key string to bytes for SecureTransport
        self.key = settings.STORAGE_ENCRYPTION_KEY.encode()

    def handle_heartbeat(self, conn: socket.socket, address: tuple):
        """
        Processes one heartbeat connection from a storage node.

        Reads a single HEARTBEAT packet, updates the node's status in the
        registry, and sends back an ACK.  The connection is always closed after
        this exchange — heartbeats are not persistent.

        Args:
            conn: The accepted socket from the storage node.
            address: (ip, port) tuple of the connecting node.

        Raises:
            ProtocolError: Logged and silently dropped if the packet is malformed.
        """
        node_ip = address[0]
        transport = SecureTransport(conn, self.key)
        try:
            packet = transport.receive_packet()
            if not packet:
                return

            if packet.command == CommandType.HEARTBEAT:
                node_id = packet.fields.get(Field.NODE_ID)
                node_port = packet.fields.get(Field.NODE_PORT)
                capacity = packet.fields.get(Field.CAPACITY)

                # Refresh the node's last-seen timestamp and free-space reading
                NodeRegistry.update_node_status(node_id, node_ip, node_port, capacity)

                # STATUS=0 means OK; the node doesn't act on the ACK but expects one
                ack = Packet(CommandType.HEARTBEAT, {Field.STATUS: 0})
                transport.send_packet(ack)
            else:
                print(f"[!] HeartbeatServer: Unexpected command from {node_ip}: {packet.command}")

        except ProtocolError as e:
            print(f"[!] HeartbeatServer Protocol Error from {node_ip}: {e}")
        except Exception as e:
            print(f"[!] HeartbeatServer Error from {node_ip}: {e}")
        finally:
            # Heartbeat connections are always short-lived — close after each exchange
            conn.close()

    def start(self):
        """
        Binds the server socket and enters the accept loop.

        The backlog is set to 50 because many nodes may send heartbeats at the
        same time (all on a 30 s cycle).  Each is dispatched to a daemon thread
        so the accept loop is never blocked.
        """
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.host, self.port))
        # High backlog because heartbeats from all nodes can arrive simultaneously
        server_sock.listen(50)
        print(f"[*] HeartbeatServer is listening on {self.host}:{self.port}")

        while True:
            try:
                conn, address = server_sock.accept()
                threading.Thread(
                    target=self.handle_heartbeat,
                    args=(conn, address),
                    daemon=True
                ).start()
            except Exception as e:
                print(f"[!] HeartbeatServer accept error: {e}")
