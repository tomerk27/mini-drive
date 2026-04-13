import asyncio
from core.config import settings
from shared.protocol import CommandType, Field, Packet, AsyncSecureTransport, ProtocolError
from gateways.storage.services.node_registry import NodeRegistry


class HeartbeatServer:
    """
    Async TCP server that listens for periodic heartbeat pulses from storage nodes.
    Each heartbeat updates the node's status and available capacity in the database.
    """
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = 9001
        self.key = settings.STORAGE_ENCRYPTION_KEY.encode()

    async def handle_heartbeat(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
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

                await NodeRegistry.update_node_status(node_id, node_ip, node_port, capacity)

                ack = Packet(CommandType.HEARTBEAT, {Field.STATUS: 0})
                await transport.send_packet(ack)
            else:
                print(f"[!] HeartbeatServer: Unexpected command from {node_ip}: {packet.command}")

        except ProtocolError as e:
            print(f"[!] HeartbeatServer Protocol Error from {node_ip}: {e}")
        except Exception as e:
            print(f"[!] HeartbeatServer Error from {node_ip}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def start(self):
        """Starts the async TCP listener for incoming heartbeats."""
        server = await asyncio.start_server(self.handle_heartbeat, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f"[*] HeartbeatServer is listening on {addr}")

        async with server:
            await server.serve_forever()
