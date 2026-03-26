import socket
import threading
import asyncio
from common import settings
from shared.protocol import (
    CommandType, 
    Field, 
    pack, 
    unpack, 
    send_packet, 
    receive_decrypted_packet
)
from services.tracker_service import TrackerService

class TrackerServer:
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 9001
        self.key = settings.STORAGE_ENCRYPTION_KEY.encode()

    def handle_node(self, client_socket, address):
        """Processes a single heartbeat pulse from a storage node."""
        node_ip = address[0]
        
        try:
            # Receive and decrypt the pulse
            decrypted_data = receive_decrypted_packet(client_socket, self.key)
            if not decrypted_data:
                return

            # Unpack the TLV data
            command, fields = unpack(decrypted_data)

            if command == CommandType.HEARTBEAT:
                node_id = fields.get(Field.NODE_ID)
                node_port = fields.get(Field.NODE_PORT)
                capacity = fields.get(Field.CAPACITY)

                # Update MongoDB (Since this is a thread, we must create an event loop for async DB calls)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(
                    TrackerService.update_node_status(node_id, node_ip, node_port, capacity)
                )
                loop.close()

                # Send ACK back to the node
                ack_packet = pack(CommandType.HEARTBEAT, {Field.STATUS: 0})
                send_packet(client_socket, ack_packet, self.key)
            else:
                print(f"[!] Tracker received invalid command: {command}")
                
        except Exception as e:
            print(f"[!] Tracker Error handling node {node_ip}: {e}")
        finally:
            client_socket.close()

    def start(self):
        """Starts the raw TCP listener for incoming heartbeats."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(10)
            print(f"[*] Tracker Brain is alive and listening for nodes on {self.host}:{self.port}")

            while True:
                client_sock, address = server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_node, 
                    args=(client_sock, address)
                )
                client_thread.start()
                
        except Exception as e:
            print(f"[!] Tracker Server Startup Error: {e}")
        finally:
            server_socket.close()
