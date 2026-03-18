import enum

class CommandType(enum.IntEnum):
    UPLOAD = 1
    DOWNLOAD = 2
    DELETE = 3

HEADER_FIXED_SIZE = 13
DOWNLOAD_RESPONSE_SIZE = 9
BYTE_ORDER = 'big'

def pack_header(command: CommandType, filename: str, file_size: int) -> bytes:
    """                                                                                                                                                       │
    Packs metadata into a 13-byte header + encoded filename.                                                                                                  │
    Structure: [Command(1B)] [FilenameLength(4B)] [FileSize(8B)] [Filename(Var)]                                                                              │
    """

    filename_bytes = filename.encode('utf-8')
    filename_len = len(filename_bytes)

    cmd_bytes = int(command).to_bytes(1, byteorder=BYTE_ORDER)
    name_len_bytes = filename_len.to_bytes(4, byteorder=BYTE_ORDER)
    size_bytes = file_size.to_bytes(8, byteorder=BYTE_ORDER)

    return cmd_bytes + name_len_bytes + size_bytes + filename_bytes

def unpack_header(data: bytes):
    """                                                                                                                                                       │
    Unpacks exactly 13 bytes into (command, filename_length, file_size).                                                                                      │
    """
    if len(data) != HEADER_FIXED_SIZE:
       raise ValueError(f"Header must be exactly {HEADER_FIXED_SIZE} bytes. Received: {len(data)}")
    
    command_val = data[0]
    name_len = int.from_bytes(data[1:5], byteorder=BYTE_ORDER)
    file_size = int.from_bytes(data[5:13], byteorder=BYTE_ORDER)

    return CommandType(command_val), name_len, file_size

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