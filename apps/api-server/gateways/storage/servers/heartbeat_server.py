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
        self.host = "0.0.0.0"
        self.port = 9001
        self.key = settings.STORAGE_ENCRYPTION_KEY.encode()

    def handle_heartbeat(self, conn: socket.socket, address):
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

                NodeRegistry.update_node_status(node_id, node_ip, node_port, capacity)

                ack = Packet(CommandType.HEARTBEAT, {Field.STATUS: 0})
                transport.send_packet(ack)
            else:
                print(f"[!] HeartbeatServer: Unexpected command from {node_ip}: {packet.command}")

        except ProtocolError as e:
            print(f"[!] HeartbeatServer Protocol Error from {node_ip}: {e}")
        except Exception as e:
            print(f"[!] HeartbeatServer Error from {node_ip}: {e}")
        finally:
            conn.close()

    def start(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((self.host, self.port))
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
