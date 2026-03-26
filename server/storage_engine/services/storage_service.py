import hashlib
from common import settings
from common import StorageServerError
from storage_engine import StorageClient

# Load encryption key from settings
STORAGE_KEY = getattr(settings, "STORAGE_ENCRYPTION_KEY", "").encode()

def _get_client(node_id: str):
    """Returns an initialized StorageClient pointing to a specific connected node."""
    return StorageClient(
        node_id=node_id,
        encryption_key=STORAGE_KEY
    )

def send_file_to_storage(node_id: str, filename: str, file_size: int, file_stream):
    """
    Orchestrates file upload to a specific node.
    Returns (Success: bool, SHA256_Hash: str).
    """
    sha256 = hashlib.sha256()

    class HashingStream:
        def __init__(self, stream):
            self.stream = stream

        def read(self, size):
            chunk = self.stream.read(size)
            if chunk:
                sha256.update(chunk)
            return chunk

    client = _get_client(node_id)
    try:
        hashing_stream = HashingStream(file_stream)
        success = client.upload(filename, file_size, hashing_stream)
        file_hash = sha256.hexdigest() if success else None
        return success, file_hash
    except Exception as e:
        print(f"[!] Storage Service Upload Error: {e}")
        return False, None

def get_file_from_storage(node_id: str, filename: str, expected_hash: str):
    """
    Orchestrates file download from a specific node.
    Returns a generator that yields binary chunks.
    """
    client = _get_client(node_id)
    
    try:
        chunk_gen, file_size = client.download_generator(filename)
        if not chunk_gen:
            raise StorageServerError("File not found on storage node")

        def verified_generator():
            sha256 = hashlib.sha256()
            total_bytes = 0
            
            try:
                for chunk in chunk_gen:
                    sha256.update(chunk)
                    total_bytes += len(chunk)
                    yield chunk

                if total_bytes != file_size:
                    raise StorageServerError("Incomplete download from storage node")

                actual_hash = sha256.hexdigest()
                if expected_hash != actual_hash:
                    print(f"[!] INTEGRITY ERROR for {filename}!")
                    raise StorageServerError("File integrity verification failed")

            except Exception as e:
                print(f"[!] Download Stream Error: {e}")
                raise StorageServerError("Error streaming file from storage")

        return verified_generator()

    except Exception as e:
        print(f"[!] Storage Service Download Error: {e}")
        raise StorageServerError()

def delete_file_from_storage(node_id: str, filename: str) -> bool:
    """
    Requests a file deletion from a specific node.
    """
    client = _get_client(node_id)
    try:
        return client.delete(filename)
    except Exception as e:
        print(f"[!] Storage Service Delete Error: {e}")
        return False
