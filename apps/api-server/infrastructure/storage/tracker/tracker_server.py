import asyncio
from core.config import settings
from shared.protocol import CommandType, Field, Packet, AsyncSecureTransport, ProtocolError
from infrastructure.storage.services.tracker_service import TrackerService

class TrackerServer:
    """
    Async TCP server that listens for heartbeats from storage nodes.
    """
    def __init__(self, main_loop=None):
        self.host = "0.0.0.0"
        self.port = 9001
        self.key = settings.STORAGE_ENCRYPTION_KEY.encode()
        # main_loop is no longer strictly needed if we are already in an async environment,
        # but kept for backward compatibility if needed.
        self.main_loop = main_loop or asyncio.get_event_loop()

    async def handle_node(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Processes a single heartbeat pulse from a storage node."""
        address = writer.get_extra_info('peername')
        node_ip = address[0]
        transport = AsyncSecureTransport(reader, writer, self.key)
        
        try:
            packet = await transport.receive_packet()
            if not packet:
                return

            if packet.command == CommandType.HEARTBEAT:
                node_id = packet.fields.get(Field.NODE_ID)
                node_port = packet.fields.get(Field.NODE_PORT)
                capacity = packet.fields.get(Field.CAPACITY)

                # Call the service to update node status
                await TrackerService.update_node_status(node_id, node_ip, node_port, capacity)

                # Send ACK back to the node
                ack_packet = Packet(CommandType.HEARTBEAT, {Field.STATUS: 0})
                await transport.send_packet(ack_packet)
            else:
                print(f"[!] Tracker received invalid command: {packet.command}")
                
        except ProtocolError as e:
            print(f"[!] Protocol Error handling node {node_ip}: {e}")
        except Exception as e:
            print(f"[!] Tracker Error handling node {node_ip}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def start(self):
        """Starts the async TCP listener for incoming heartbeats."""
        server = await asyncio.start_server(self.handle_node, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f"[*] Tracker Brain is alive and listening for nodes on {addr}")

        async with server:
            await server.serve_forever()
