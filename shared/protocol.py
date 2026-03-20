import enum
from cryptography.fernet import Fernet

class CommandType(enum.IntEnum):
    UPLOAD = 1
    DOWNLOAD = 2
    DELETE = 3

HEADER_FIXED_SIZE = 13
DOWNLOAD_RESPONSE_SIZE = 9
BYTE_ORDER = 'big'

def encrypt_data(data: bytes, key: bytes) -> bytes:
    """Encrypts data using the provided key."""
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(data: bytes, key: bytes) -> bytes:
    """Decrypts data using the provided key."""
    f = Fernet(key)
    return f.decrypt(data)

def receive_exactly(sock, n):
    """Utility to receive exactly n bytes from a socket."""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def receive_packet(sock, length_size=4):
    """
    Reads a length prefix, then receives and returns the full message.
    """

    raw_length = receive_exactly(sock, length_size)

    if not raw_length:
        return None
    
    message_length = int.from_bytes(raw_length, byteorder=BYTE_ORDER)
    
    return receive_exactly(sock, message_length) 

def send_packet(sock, data, key):
    """Encrypts data, adds a 4-byte length prefix, and sends it."""
    encrypted_data = encrypt_data(data, key)
    length = len(encrypted_data)
    sock.sendall(length.to_bytes(4, byteorder=BYTE_ORDER) + encrypted_data)

def receive_decrypted_packet(sock, key):
    """Receives a length-prefixed packet and decrypts it."""
    encrypted_data = receive_packet(sock)
    if not encrypted_data:
        return None
    return decrypt_data(encrypted_data, key)

def pack_header(command: CommandType, filename: str, file_size: int) -> bytes:
    """                                                                                                                                                       
    Packs metadata into header.
    Structure: [Command(1B)] [FileSize(8B)] [Filename(Var)]                                                                              
    """

    cmd_bytes = int(command).to_bytes(1, byteorder=BYTE_ORDER)
    size_bytes = file_size.to_bytes(8, byteorder=BYTE_ORDER)
    filename_bytes = filename.encode('utf-8')

    return cmd_bytes + size_bytes + filename_bytes

def unpack_header(data: bytes):
    """
    Unpacks header into command, file_size, filename.
    """
    
    command_val = data[0]
    file_size = int.from_bytes(data[1:9], byteorder=BYTE_ORDER)
    filename = data[9:].decode('utf-8')

    return CommandType(command_val), file_size, filename

def pack_response(status_code: int) -> bytes:
    """1-byte response (0 for Success, 1 for Error)"""
    return status_code.to_bytes(1, byteorder=BYTE_ORDER)

def unpack_response(data: bytes) -> int:
    """Unpacks the 1-byte response"""
    return int.from_bytes(data, byteorder=BYTE_ORDER)

def pack_download_response(status_code: int, file_size: int) -> bytes:
    """
    Packs a response for a download request.
    Structure: [Status Code (1B)] [File Size (8B)]
    """
    
    status_bytes = pack_response(status_code)

    size_bytes = file_size.to_bytes(8, byteorder=BYTE_ORDER)
    
    return status_bytes + size_bytes

def unpack_download_response(data: bytes):
    """
    Unpacks exactly 9 bytes into (status_code, file_size).
    Structure: [Status(1B)] [FileSize(8B)]
    """
    if len(data) != DOWNLOAD_RESPONSE_SIZE:
        raise ValueError(f"Download response must be {DOWNLOAD_RESPONSE_SIZE} bytes. Got: {len(data)}")
    
    status_code = data[0]

    file_size = int.from_bytes(data[1:9], byteorder=BYTE_ORDER)

    return status_code, file_size