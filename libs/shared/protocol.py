import asyncio
import enum
import struct
from cryptography.fernet import Fernet
from typing import Dict, Any, Tuple, Optional

class CommandType(enum.IntEnum):
    UPLOAD = 1
    DOWNLOAD = 2
    DELETE = 3
    HEARTBEAT = 4
    REGISTER = 5

class Field(enum.IntEnum):
    STATUS = 1
    FILE_SIZE = 2
    FILENAME = 3
    NODE_ID = 4
    NODE_PORT = 5
    CAPACITY = 6

BYTE_ORDER = 'big'

class ProtocolError(Exception):
    pass

class Packet:
    """
    Encapsulates a TLV-based binary message.
    Structure: [Command(1B)] [ [FieldID(1B)] [Length(4B)] [Value(Var)] ... ]
    """
    def __init__(self, command: CommandType, fields: Dict[Field, Any] = None):
        self.command = command
        self.fields = fields or {}

    def pack(self) -> bytes:
        data = int(self.command).to_bytes(1, byteorder=BYTE_ORDER)
        for field_id, value in self.fields.items():
            if isinstance(value, str):
                val_bytes = value.encode('utf-8')
            elif isinstance(value, int):
                val_bytes = value.to_bytes(8, byteorder=BYTE_ORDER)
            elif isinstance(value, bytes):
                val_bytes = value
            else:
                raise TypeError(f"Unsupported value type in pack: {type(value)}")

            data += int(field_id).to_bytes(1, byteorder=BYTE_ORDER)
            data += len(val_bytes).to_bytes(4, byteorder=BYTE_ORDER)
            data += val_bytes
        return data

    @classmethod
    def unpack(cls, data: bytes) -> 'Packet':
        if not data:
            raise ProtocolError("Empty data for unpacking")

        try:
            command = CommandType(data[0])
            fields = {}
            offset = 1
            while offset < len(data):
                field_id = Field(data[offset])
                length = int.from_bytes(data[offset+1:offset+5], byteorder=BYTE_ORDER)
                value_bytes = data[offset+5:offset+5+length]
                
                if field_id in (Field.FILE_SIZE, Field.NODE_PORT, Field.CAPACITY, Field.STATUS):
                    fields[field_id] = int.from_bytes(value_bytes, byteorder=BYTE_ORDER)
                elif field_id in (Field.FILENAME, Field.NODE_ID):
                    fields[field_id] = value_bytes.decode('utf-8')
                else:
                    fields[field_id] = value_bytes
                offset += 5 + length
            return cls(command, fields)
        except (ValueError, IndexError) as e:
            raise ProtocolError(f"Failed to unpack packet: {e}")

class SecureTransport:
    """
    Handles encrypted packet transmission over a synchronous socket.
    """
    def __init__(self, sock, key: bytes):
        self.sock = sock
        self.fernet = Fernet(key)

    def _send_raw(self, data: bytes):
        length = len(data)
        self.sock.sendall(length.to_bytes(4, byteorder=BYTE_ORDER) + data)

    def _receive_raw(self) -> Optional[bytes]:
        raw_length = self._receive_exactly(4)
        if not raw_length:
            return None
        length = int.from_bytes(raw_length, byteorder=BYTE_ORDER)
        return self._receive_exactly(length)

    def _receive_exactly(self, n: int) -> Optional[bytes]:
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def send_packet(self, packet: Packet):
        data = packet.pack()
        encrypted = self.fernet.encrypt(data)
        self._send_raw(encrypted)

    def receive_packet(self) -> Optional[Packet]:
        encrypted = self._receive_raw()
        if not encrypted:
            return None
        decrypted = self.fernet.decrypt(encrypted)
        return Packet.unpack(decrypted)

    def send_chunk(self, chunk: bytes):
        """Sends a raw encrypted chunk without TLV (used for file streaming)."""
        encrypted = self.fernet.encrypt(chunk)
        self._send_raw(encrypted)

    def receive_chunk(self) -> Optional[bytes]:
        """Receives a raw encrypted chunk without TLV (used for file streaming)."""
        encrypted = self._receive_raw()
        if not encrypted:
            return None
        return self.fernet.decrypt(encrypted)

class AsyncSecureTransport:
    """
    Handles encrypted packet transmission over an asynchronous stream.
    """
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, key: bytes):
        self.reader = reader
        self.writer = writer
        self.fernet = Fernet(key)

    async def _send_raw(self, data: bytes):
        length = len(data)
        self.writer.write(length.to_bytes(4, byteorder=BYTE_ORDER) + data)
        await self.writer.drain()

    async def _receive_raw(self) -> Optional[bytes]:
        try:
            raw_length = await self.reader.readexactly(4)
            length = int.from_bytes(raw_length, byteorder=BYTE_ORDER)
            return await self.reader.readexactly(length)
        except (asyncio.IncompleteReadError, ConnectionResetError):
            return None

    async def send_packet(self, packet: Packet):
        data = packet.pack()
        encrypted = self.fernet.encrypt(data)
        await self._send_raw(encrypted)

    async def receive_packet(self) -> Optional[Packet]:
        encrypted = await self._receive_raw()
        if not encrypted:
            return None
        decrypted = self.fernet.decrypt(encrypted)
        return Packet.unpack(decrypted)

    async def send_chunk(self, chunk: bytes):
        """Sends a raw encrypted chunk without TLV (used for file streaming)."""
        encrypted = self.fernet.encrypt(chunk)
        await self._send_raw(encrypted)

    async def receive_chunk(self) -> Optional[bytes]:
        """Receives a raw encrypted chunk without TLV (used for file streaming)."""
        encrypted = await self._receive_raw()
        if not encrypted:
            return None
        return self.fernet.decrypt(encrypted)
