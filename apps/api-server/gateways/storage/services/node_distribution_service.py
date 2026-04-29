"""
High-level helpers for sending files to and from storage nodes.

Used by both items_service (upload/download during normal operation) and
RepairService (re-replication after a node failure).
"""

import hashlib
import io
from typing import Optional
from core.config import settings
from core.exceptions import StorageServerError
from gateways.storage.client.storage_client import StorageClient

# Pre-encode the key once so it doesn't get re-encoded on every call.
STORAGE_KEY = settings.STORAGE_ENCRYPTION_KEY.encode()


def _get_client(node_id: str) -> StorageClient:
    """Returns a StorageClient configured with the shared encryption key."""
    return StorageClient(node_id=node_id, encryption_key=STORAGE_KEY)


def send_file_to_nodes(
    node_id_list: list[str], filename: str, file_size: int, file_stream
) -> tuple[bool, str | None]:
    """
    Uploads a file sequentially to every node in node_id_list.

    Reads all bytes upfront so the same data can be sent to multiple nodes
    without seeking back to the start of the stream each time.

    Args:
        node_id_list: Nodes to upload to (typically the surviving replicas during repair).
        filename: Physical filename to store on each node.
        file_size: Total byte count (informational — the stream length is used for upload).
        file_stream: File-like object with the data to upload.

    Returns:
        (True, sha256_hex) if at least one node succeeded; (False, None) otherwise.
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
    Downloads a file from a storage node and verifies its integrity.

    Computes a SHA-256 hash of the downloaded bytes and compares it to the
    expected hash stored in the DB. This catches silent data corruption on
    the node's disk or in transit.

    Args:
        node_id: The node to download from.
        filename: Physical filename on the node.
        expected_hash: SHA-256 hex digest recorded at upload time.

    Returns:
        The raw file bytes if the download succeeds and the hash matches.

    Raises:
        StorageServerError: If the file is not found, the hash doesn't match,
            or the download fails for any other reason.
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
    """
    Requests deletion of a physical file from a storage node.

    Failures are logged but not re-raised, since the DB record is already
    gone by the time this is called and cleanup is best-effort.
    """
    client = _get_client(node_id)
    try:
        return client.delete(filename)
    except Exception as e:
        print(f"[!] NodeDistributionService Delete Error for node {node_id}: {e}")
        return False
