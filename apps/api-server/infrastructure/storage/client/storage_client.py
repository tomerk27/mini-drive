import asyncio
from typing import Optional, Generator, AsyncGenerator
from shared.protocol import CommandType, Field, Packet, AsyncSecureTransport, ProtocolError
from infrastructure.storage.tracker.connection_pool import connection_pool

class StorageClient:
    """
    Low-level driver for communicating with a Storage Node over async TCP streams.
    Fetches an active stream pair from the ConnectionPool.
    """
    def __init__(self, node_id: str, encryption_key: bytes):
        self.node_id = node_id
        self.key = encryption_key

    async def _get_streams(self):
        streams = await connection_pool.get_node_streams(self.node_id)
        if not streams:
            raise ConnectionError(f"Node {self.node_id} is not connected to the Main Server.")
        return streams

    async def upload(self, filename: str, file_size: int, file_stream) -> bool:
        """Streams a file through the persistent node stream."""
        reader, writer = await self._get_streams()
        transport = AsyncSecureTransport(reader, writer, self.key)
        
        try:
            # Send Header
            header = Packet(CommandType.UPLOAD, {
                Field.FILENAME: filename,
                Field.FILE_SIZE: file_size
            })
            await transport.send_packet(header)

            # Stream chunks
            # Note: file_stream might be sync or async. 
            # If it's from FastAPI (UploadFile), it has await file.read().
            # For simplicity, we assume it's a sync stream or we handle both.
            while True:
                # If it's a standard file object (sync)
                if asyncio.iscoroutinefunction(file_stream.read):
                    chunk = await file_stream.read(4096)
                else:
                    chunk = file_stream.read(4096)
                
                if not chunk:
                    break
                await transport.send_chunk(chunk)

            # Wait for ACK
            res = await transport.receive_packet()
            if not res:
                return False
            
            return res.fields.get(Field.STATUS) == 0
        except Exception as e:
            print(f"[!] StorageClient Upload Error for {self.node_id}: {e}")
            await connection_pool.remove_node(self.node_id)
            return False

    async def download_generator(self, filename: str) -> Tuple[Optional[AsyncGenerator[bytes, None]], int]:
        """Returns a generator that yields binary chunks through the persistent node stream."""
        reader, writer = await self._get_streams()
        transport = AsyncSecureTransport(reader, writer, self.key)
        
        try:
            # Send Download Request
            header = Packet(CommandType.DOWNLOAD, {Field.FILENAME: filename})
            await transport.send_packet(header)
            
            # Receive response header
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

                    # Send final ACK/NACK
                    status_code = 0 if bytes_read == file_size else 1
                    res_packet = Packet(CommandType.DOWNLOAD, {Field.STATUS: status_code})
                    await transport.send_packet(res_packet)
                except Exception as e:
                    print(f"[!] Download Stream Error for {self.node_id}: {e}")
                    await connection_pool.remove_node(self.node_id)
                    raise

            return chunk_generator(), file_size
        except Exception:
            await connection_pool.remove_node(self.node_id)
            raise

    async def delete(self, filename: str) -> bool:
        """Requests a file deletion through the persistent node stream."""
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

from typing import Tuple
