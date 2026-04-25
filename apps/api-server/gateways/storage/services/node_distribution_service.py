import hashlib
import io
from typing import Optional
from core.config import settings
from core.exceptions import StorageServerError
from gateways.storage.client.storage_client import StorageClient

STORAGE_KEY = settings.STORAGE_ENCRYPTION_KEY.encode()


def _get_client(node_id: str) -> StorageClient:
    return StorageClient(node_id=node_id, encryption_key=STORAGE_KEY)


def send_file_to_nodes(
    node_id_list: list[str], filename: str, file_size: int, file_stream
) -> tuple[bool, str | None]:
    """
    Uploads a file to each node in node_id_list.
    Reads all bytes upfront to compute SHA-256 and allow reuse across nodes.
    Returns (success, sha256_hex).
    """
    if hasattr(file_stream, 'seek'):
        file_stream.seek(0)
    data = file_stream.read()
    sha256 = hashlib.sha256(data).hexdigest()

    results = []
    for node_id in node_id_list:
        try:
            client = _get_client(node_id)
            success = client.upload(filename, len(data), io.BytesIO(data))
            results.append(success)
        except Exception as e:
            print(f"[!] NodeDistributionService Upload Error for node {node_id}: {e}")
            results.append(False)

    final_success = any(results)
    return final_success, sha256 if final_success else None


def get_file_from_node(node_id: str, filename: str, expected_hash: str) -> Optional[bytes]:
    """
    Downloads a file from a node and verifies its SHA-256 integrity.
    Returns the raw bytes on success, raises StorageServerError on failure.
    """
    client = _get_client(node_id)
    try:
        data = client.download(filename)
        if data is None:
            raise StorageServerError("File not found on storage node")

        actual_hash = hashlib.sha256(data).hexdigest()
        if expected_hash != actual_hash:
            print(f"[!] Integrity check failed for {filename}")
            raise StorageServerError("File integrity verification failed")

        return data
    except StorageServerError:
        raise
    except Exception as e:
        print(f"[!] NodeDistributionService Download Error: {e}")
        raise StorageServerError()


def delete_file_from_node(node_id: str, filename: str) -> bool:
    """Requests a file deletion from a specific node."""
    client = _get_client(node_id)
    try:
        return client.delete(filename)
    except Exception as e:
        print(f"[!] NodeDistributionService Delete Error for node {node_id}: {e}")
        return False
