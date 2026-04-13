import hashlib
import asyncio
from core.config import settings
from core.exceptions import StorageServerError
from gateways.storage.client.storage_client import StorageClient

STORAGE_KEY = settings.STORAGE_ENCRYPTION_KEY.encode()


class _HashingWrapper:
    """
    Wraps a file stream to compute a SHA-256 hash during the first read pass.
    Supports both sync and async .read() methods.
    """
    def __init__(self, stream, sha256: hashlib.sha256):
        self._stream = stream
        self._sha256 = sha256

    async def read(self, size: int) -> bytes:
        if asyncio.iscoroutinefunction(self._stream.read):
            chunk = await self._stream.read(size)
        else:
            chunk = self._stream.read(size)
        if chunk:
            self._sha256.update(chunk)
        return chunk


def _get_client(node_id: str) -> StorageClient:
    return StorageClient(node_id=node_id, encryption_key=STORAGE_KEY)


async def send_file_to_nodes(
    node_id_list: list[str], filename: str, file_size: int, file_stream
) -> tuple[bool, str | None]:
    """
    Uploads a file to each node in node_id_list.
    The SHA-256 hash is calculated on the first upload and reused for subsequent nodes.
    Returns (success, sha256_hex).
    """
    sha256 = hashlib.sha256()
    hash_locked = False
    results = []

    for node_id in node_id_list:
        try:
            if hasattr(file_stream, 'seek'):
                file_stream.seek(0)

            wrapper = _HashingWrapper(file_stream, sha256) if not hash_locked else file_stream
            client = _get_client(node_id)
            success = await client.upload(filename, file_size, wrapper)
            hash_locked = True
            results.append(success)
        except Exception as e:
            print(f"[!] NodeDistributionService Upload Error for node {node_id}: {e}")
            results.append(False)

    final_success = any(results)
    return final_success, sha256.hexdigest() if final_success else None


async def get_file_from_node(node_id: str, filename: str, expected_hash: str):
    """
    Downloads a file from a node and streams it back as an async generator.
    Verifies size and SHA-256 integrity after streaming completes.
    """
    client = _get_client(node_id)

    try:
        chunk_gen, file_size = await client.download_generator(filename)
        if not chunk_gen:
            raise StorageServerError("File not found on storage node")

        async def verified_generator():
            sha256 = hashlib.sha256()
            total_bytes = 0

            try:
                async for chunk in chunk_gen:
                    sha256.update(chunk)
                    total_bytes += len(chunk)
                    yield chunk

                if total_bytes != file_size:
                    raise StorageServerError("Incomplete download from storage node")

                if expected_hash != sha256.hexdigest():
                    print(f"[!] Integrity check failed for {filename}")
                    raise StorageServerError("File integrity verification failed")

            except Exception as e:
                print(f"[!] Download Stream Error: {e}")
                raise StorageServerError("Error streaming file from storage")

        return verified_generator()

    except Exception as e:
        print(f"[!] NodeDistributionService Download Error: {e}")
        raise StorageServerError()


async def delete_file_from_node(node_id: str, filename: str) -> bool:
    """Requests a file deletion from a specific node."""
    client = _get_client(node_id)
    try:
        return await client.delete(filename)
    except Exception as e:
        print(f"[!] NodeDistributionService Delete Error for node {node_id}: {e}")
        return False
