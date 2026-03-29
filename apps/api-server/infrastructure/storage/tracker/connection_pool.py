import asyncio
from typing import Dict, Tuple, Optional

class ConnectionPool:
    """
    An async-safe registry to store and manage active stream connections from Storage Nodes.
    """
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionPool, cls).__new__(cls)
            cls._instance.connections: Dict[str, Tuple[asyncio.StreamReader, asyncio.StreamWriter]] = {}
        return cls._instance

    async def register_node(self, node_id: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        async with self._lock:
            # If node already exists, close old connection
            if node_id in self.connections:
                _, old_writer = self.connections[node_id]
                try:
                    old_writer.close()
                    await old_writer.wait_closed()
                except:
                    pass
            self.connections[node_id] = (reader, writer)
            print(f"[*] ConnectionPool: Registered node {node_id}")

    async def get_node_streams(self, node_id: str) -> Optional[Tuple[asyncio.StreamReader, asyncio.StreamWriter]]:
        async with self._lock:
            return self.connections.get(node_id)

    async def remove_node(self, node_id: str):
        async with self._lock:
            if node_id in self.connections:
                _, writer = self.connections.pop(node_id)
                try:
                    writer.close()
                    await writer.wait_closed()
                except:
                    pass
                print(f"[*] ConnectionPool: Removed node {node_id}")

connection_pool = ConnectionPool()
