import asyncio
from core.config import settings
from shared.protocol import CommandType, Field, Packet, AsyncSecureTransport, ProtocolError
from gateways.storage.servers.connection_pool import connection_pool


class DataServer:
    """
    Async TCP listener on the main server that waits for Storage Nodes to connect.
    Maintains persistent connections used for UPLOAD/DOWNLOAD/DELETE operations.
    """
    def __init__(self):
        self.host = "0.0.0.0"
        self.port = settings.STORAGE_SERVER_PORT
        self.key = settings.STORAGE_ENCRYPTION_KEY.encode()

    async def handle_registration(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Waits for the node to identify itself via a REGISTER packet."""
        address = writer.get_extra_info('peername')
        transport = AsyncSecureTransport(reader, writer, self.key)

        try:
            packet = await transport.receive_packet()
            if not packet:
                writer.close()
                await writer.wait_closed()
                return

            if packet.command == CommandType.REGISTER:
                node_id = packet.fields.get(Field.NODE_ID)
                if node_id:
                    await connection_pool.register_node(node_id, reader, writer)
                    print(f"[*] DataServer: Node {node_id} reported for duty from {address[0]}")
                    return  # Keep the writer open — used for future commands

            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print(f"[!] DataServer Error during registration from {address[0]}: {e}")
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass

    async def start(self):
        """Starts the async listener loop."""
        server = await asyncio.start_server(self.handle_registration, self.host, self.port)
        addr = server.sockets[0].getsockname()
        print(f"[*] DataServer is listening on {addr} (waiting for nodes...)")

        async with server:
            await server.serve_forever()
