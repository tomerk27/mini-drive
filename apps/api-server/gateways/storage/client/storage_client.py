import asyncio
from typing import Optional, Tuple, AsyncGenerator
from shared.protocol import CommandType, Field, Packet, AsyncSecureTransport, ProtocolError
from gateways.storage.servers.connection_pool import connection_pool

# Errors that mean the TCP connection itself is dead and the node must re-register.
# Protocol-level or application-level errors should NOT evict a healthy connection.
_FATAL_CONNECTION_ERRORS = (OSError, asyncio.IncompleteReadError, EOFError)


class StorageClient:
    """
    Low-level driver for communicating with a Storage Node over async TCP streams.
    Fetches an active stream pair from the ConnectionPool.
    """
    def __init__(self, node_id: str, encryption_key: bytes):
        self.node_id = node_id
        self.key = encryption_key

    async def _get_streams(self) -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        streams = await connection_pool.get_node_streams(self.node_id)
        if not streams:
            raise ConnectionError(f"Node {self.node_id} is not connected to the main server.")
        return streams

    async def upload(self, filename: str, file_size: int, file_stream) -> bool:
        """Streams a file through the persistent node connection."""
        reader, writer = await self._get_streams()
        transport = AsyncSecureTransport(reader, writer, self.key)

        try:
            header = Packet(CommandType.UPLOAD, {
                Field.FILENAME: filename,
                Field.FILE_SIZE: file_size
            })
            await transport.send_packet(header)

            while True:
                if asyncio.iscoroutinefunction(file_stream.read):
                    chunk = await file_stream.read(4096)
                else:
                    chunk = file_stream.read(4096)

                if not chunk:
                    break
                await transport.send_chunk(chunk)

            res = await transport.receive_packet()
            if not res:
                return False

            return res.fields.get(Field.STATUS) == 0
        except Exception as e:
            print(f"[!] StorageClient Upload Error for {self.node_id}: {e}")
            if isinstance(e, _FATAL_CONNECTION_ERRORS):
                await connection_pool.remove_node(self.node_id)
            return False

    async def download_generator(self, filename: str) -> Tuple[Optional[AsyncGenerator[bytes, None]], int]:
        """Returns an async generator that yields binary chunks from the node."""
        reader, writer = await self._get_streams()
        transport = AsyncSecureTransport(reader, writer, self.key)

        try:
            header = Packet(CommandType.DOWNLOAD, {Field.FILENAME: filename})
            await transport.send_packet(header)

            res_header = await transport.receive_packet()
            if not res_header:
                return None, 0

            status = res_header.fields.get(Field.STATUS)
            file_size = res_header.fields.get(Field.FILE_SIZE)

            if status != 0:
                return None, 0

            async def chunk_generator():
                try:
                    bytes_read = 0
                    while bytes_read < file_size:
                        chunk = await transport.receive_chunk()
                        if not chunk:
                            break
                        yield chunk
                        bytes_read += len(chunk)

                    status_code = 0 if bytes_read == file_size else 1
                    res_packet = Packet(CommandType.DOWNLOAD, {Field.STATUS: status_code})
                    await transport.send_packet(res_packet)
                except Exception as e:
                    print(f"[!] Download Stream Error for {self.node_id}: {e}")
                    if isinstance(e, _FATAL_CONNECTION_ERRORS):
                        await connection_pool.remove_node(self.node_id)
                    raise

            return chunk_generator(), file_size
        except Exception as e:
            if isinstance(e, _FATAL_CONNECTION_ERRORS):
                await connection_pool.remove_node(self.node_id)
            raise

    async def delete(self, filename: str) -> bool:
        """Requests a file deletion through the persistent node connection."""
        reader, writer = await self._get_streams()
        transport = AsyncSecureTransport(reader, writer, self.key)

        try:
            header = Packet(CommandType.DELETE, {Field.FILENAME: filename})
            await transport.send_packet(header)

            res = await transport.receive_packet()
            if not res:
                return False

            return res.fields.get(Field.STATUS) == 0
        except Exception as e:
            print(f"[!] StorageClient Delete Error for {self.node_id}: {e}")
            await connection_pool.remove_node(self.node_id)
            return False
