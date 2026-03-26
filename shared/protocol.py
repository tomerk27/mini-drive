import enum
from cryptography.fernet import Fernet

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

# Encryption/Decryption
def encrypt_data(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(data)

# Socket helpers
def receive_exactly(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def receive_packet(sock, length_size=4):
    raw_length = receive_exactly(sock, length_size)
    if not raw_length:
        return None
    message_length = int.from_bytes(raw_length, byteorder=BYTE_ORDER)
    return receive_exactly(sock, message_length) 

def send_packet(sock, data, key):
    encrypted_data = encrypt_data(data, key)
    length = len(encrypted_data)
    sock.sendall(length.to_bytes(4, byteorder=BYTE_ORDER) + encrypted_data)

def receive_decrypted_packet(sock, key):
    encrypted_data = receive_packet(sock)
    if not encrypted_data:
        return None
    return decrypt_data(encrypted_data, key)

# Unified TLV Packing
def pack(command: CommandType, fields: dict) -> bytes:
    """
    Packs a command and its fields into a TLV-based binary message.
    Structure: [Command(1B)] [ [FieldID(1B)] [Length(4B)] [Value(Var)] ... ]
    """
    packet = int(command).to_bytes(1, byteorder=BYTE_ORDER)
    
    for field_id, value in fields.items():
        if isinstance(value, str):
            val_bytes = value.encode('utf-8')
        elif isinstance(value, int):
            val_bytes = value.to_bytes(8, byteorder=BYTE_ORDER)
        elif isinstance(value, bytes):
            val_bytes = value
        else:
            raise TypeError(f"Unsupported value type in pack: {type(value)}")

        packet += int(field_id).to_bytes(1, byteorder=BYTE_ORDER)
        packet += len(val_bytes).to_bytes(4, byteorder=BYTE_ORDER)
        packet += val_bytes
        
    return packet

def unpack(data: bytes):
    """
    Unpacks a TLV-based binary message into (Command, FieldsDict).
    """
    if not data:
        return None, {}

    command = CommandType(data[0])
    fields = {}
    
    offset = 1
    while offset < len(data):
        field_id = Field(data[offset])
        length = int.from_bytes(data[offset+1:offset+5], byteorder=BYTE_ORDER)
        value_bytes = data[offset+5:offset+5+length]
        
        # Heuristic to convert back to int/str based on Field ID
        if field_id in (Field.FILE_SIZE, Field.NODE_PORT, Field.CAPACITY, Field.STATUS):
            fields[field_id] = int.from_bytes(value_bytes, byteorder=BYTE_ORDER)
        elif field_id in (Field.FILENAME, Field.NODE_ID):
            fields[field_id] = value_bytes.decode('utf-8')
        else:
            fields[field_id] = value_bytes
            
        offset += 5 + length
        
    return command, fields
