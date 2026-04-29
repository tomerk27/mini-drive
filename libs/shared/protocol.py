"""
Shared binary communication protocol for CyberDrive.

Defines the TLV (Type-Length-Value) message format, command/field enums,
and both sync and async encrypted transport classes used by the API server
and storage nodes to talk to each other.

TLV packet layout:
    [Command (1 byte)] [[FieldID (1 byte)] [Length (4 bytes)] [Value (variable)] ...]

All data is encrypted with Fernet (AES-128-CBC + HMAC) before being sent
over the wire, and prefixed with a 4-byte big-endian length header.
"""

import asyncio
import enum
import struct
from cryptography.fernet import Fernet
from typing import Dict, Any, Tuple, Optional


class CommandType(enum.IntEnum):
    """Top-level command codes — the first byte of every TLV packet."""
    UPLOAD = 1
    DOWNLOAD = 2
    DELETE = 3
    HEARTBEAT = 4
    REGISTER = 5


class Field(enum.IntEnum):
    """Field IDs used inside a TLV packet to label each value."""
    STATUS = 1      # 0 = success, non-zero = error
    FILE_SIZE = 2   # file or chunk size in bytes
    FILENAME = 3    # logical filename stored on the node
    NODE_ID = 4     # unique string identifier for the storage node
    NODE_PORT = 5   # port the node listens on
    CAPACITY = 6    # free disk space on the node in bytes


# All multi-byte integers use big-endian byte order throughout the protocol.
BYTE_ORDER = 'big'


class ProtocolError(Exception):
    """Raised when a packet cannot be parsed or is structurally invalid."""
    pass


class Packet:
    """
    Encapsulates a single TLV-based binary message.

    Structure: [Command(1B)] [ [FieldID(1B)] [Length(4B)] [Value(Var)] ... ]

    Args:
        command: The command type for this packet (e.g. UPLOAD, HEARTBEAT).
        fields: Optional dict mapping Field IDs to their values.
    """
    def __init__(self, command: CommandType, fields: Dict[Field, Any] = None):
        self.command = command
        self.fields = fields or {}

    def pack(self) -> bytes:
        """
        Serializes this packet into raw bytes ready for encryption and sending.

        Returns:
            The packed binary representation of the packet.

        Raises:
            TypeError: If a field value is not str, int, or bytes.
        """
        data = int(self.command).to_bytes(1, byteorder=BYTE_ORDER)
        for field_id, value in self.fields.items():
            # Encode each value type into bytes before adding TLV framing.
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
        """
        Deserializes raw bytes back into a Packet object.

        Args:
            data: Raw decrypted bytes from the wire.

        Returns:
            A Packet with command and fields populated.

        Raises:
            ProtocolError: If the bytes are empty or cannot be parsed.
        """
        if not data:
            raise ProtocolError("Empty data for unpacking")

        try:
            command = CommandType(data[0])
            fields = {}
            offset = 1
            # Walk through each TLV field: 1 byte ID, 4 bytes length, N bytes value.
            while offset < len(data):
                field_id = Field(data[offset])
                length = int.from_bytes(data[offset+1:offset+5], byteorder=BYTE_ORDER)
                value_bytes = data[offset+5:offset+5+length]

                # Decode numeric fields as ints, string fields as UTF-8, others as raw bytes.
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
    Handles Fernet-encrypted packet transmission over a synchronous blocking socket.

    Each message is encrypted, then prefixed with a 4-byte big-endian length
    before being sent. This class is used by the HeartbeatServer and StorageClient
    on the API server side (sync context).

    Args:
        sock: An already-connected socket.socket object.
        key: The Fernet encryption key as raw bytes.
    """
    def __init__(self, sock, key: bytes):
        self.sock = sock
        self.fernet = Fernet(key)

    def _send_raw(self, data: bytes):
        """Prepends a 4-byte length header and sends all bytes on the socket."""
        length = len(data)
        self.sock.sendall(length.to_bytes(4, byteorder=BYTE_ORDER) + data)

    def _receive_raw(self) -> Optional[bytes]:
        """Reads the 4-byte length header then reads exactly that many bytes."""
        raw_length = self._receive_exactly(4)
        if not raw_length:
            return None
        length = int.from_bytes(raw_length, byteorder=BYTE_ORDER)
        return self._receive_exactly(length)

    def _receive_exactly(self, n: int) -> Optional[bytes]:
        """
        Reads exactly n bytes from the socket, looping until all arrive.

        Returns None if the connection is closed before n bytes are received.
        """
        data = b''
        while len(data) < n:
            packet = self.sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def send_packet(self, packet: Packet):
        """Encrypts and sends a TLV Packet over the socket."""
        data = packet.pack()
        encrypted = self.fernet.encrypt(data)
        self._send_raw(encrypted)

    def receive_packet(self) -> Optional[Packet]:
        """Receives, decrypts, and parses a TLV Packet from the socket."""
        encrypted = self._receive_raw()
        if not encrypted:
            return None
        decrypted = self.fernet.decrypt(encrypted)
        return Packet.unpack(decrypted)

    def send_chunk(self, chunk: bytes):
        """Sends a raw encrypted chunk without TLV framing (used for file streaming)."""
        encrypted = self.fernet.encrypt(chunk)
        self._send_raw(encrypted)

    def receive_chunk(self) -> Optional[bytes]:
        """Receives a raw encrypted chunk without TLV framing (used for file streaming)."""
        encrypted = self._receive_raw()
        if not encrypted:
            return None
        return self.fernet.decrypt(encrypted)


class AsyncSecureTransport:
    """
    Handles Fernet-encrypted packet transmission over an asyncio stream.

    Drop-in async equivalent of SecureTransport. Used everywhere in the
    storage node (which is fully async) and in the DataServer's async paths.

    Args:
        reader: asyncio.StreamReader for the connection.
        writer: asyncio.StreamWriter for the connection.
        key: The Fernet encryption key as raw bytes.
    """
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, key: bytes):
        self.reader = reader
        self.writer = writer
        self.fernet = Fernet(key)

    async def _send_raw(self, data: bytes):
        """Prepends a 4-byte length header and writes all bytes to the stream."""
        length = len(data)
        self.writer.write(length.to_bytes(4, byteorder=BYTE_ORDER) + data)
        await self.writer.drain()

    async def _receive_raw(self) -> Optional[bytes]:
        """Reads the 4-byte length header then reads exactly that many bytes."""
        try:
            raw_length = await self.reader.readexactly(4)
            length = int.from_bytes(raw_length, byteorder=BYTE_ORDER)
            return await self.reader.readexactly(length)
        except (asyncio.IncompleteReadError, ConnectionResetError):
            # Connection closed cleanly or reset — caller should treat this as EOF.
            return None

    async def send_packet(self, packet: Packet):
        """Encrypts and sends a TLV Packet over the async stream."""
        data = packet.pack()
        encrypted = self.fernet.encrypt(data)
        await self._send_raw(encrypted)

    async def receive_packet(self) -> Optional[Packet]:
        """Receives, decrypts, and parses a TLV Packet from the async stream."""
        encrypted = await self._receive_raw()
        if not encrypted:
            return None
        decrypted = self.fernet.decrypt(encrypted)
        return Packet.unpack(decrypted)

    async def send_chunk(self, chunk: bytes):
        """Sends a raw encrypted chunk without TLV framing (used for file streaming)."""
        encrypted = self.fernet.encrypt(chunk)
        await self._send_raw(encrypted)

    async def receive_chunk(self) -> Optional[bytes]:
        """Receives a raw encrypted chunk without TLV framing (used for file streaming)."""
        encrypted = await self._receive_raw()
        if not encrypted:
            return None
        return self.fernet.decrypt(encrypted)
