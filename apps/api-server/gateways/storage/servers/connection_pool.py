import socket
import threading
from typing import Dict, Optional


class ConnectionPool:
    """
    Thread-safe registry that stores active socket connections from Storage Nodes.
    One persistent connection per node, with a per-node lock to serialize operations.
    """
    _instance = None
    _instance_lock = threading.Lock()
    _connections: Dict[str, socket.socket]
    _node_locks: Dict[str, threading.Lock]
    _pool_lock: threading.Lock

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(ConnectionPool, cls).__new__(cls)
                cls._instance._connections = {}
                cls._instance._node_locks = {}
                cls._instance._pool_lock = threading.Lock()
        return cls._instance

    def register_node(self, node_id: str, sock: socket.socket):
        with self._pool_lock:
            if node_id in self._connections:
                try:
                    self._connections[node_id].close()
                except Exception:
                    pass
            self._connections[node_id] = sock
            if node_id not in self._node_locks:
                self._node_locks[node_id] = threading.Lock()
            print(f"[*] ConnectionPool: Registered node {node_id}")

    def get_node_socket(self, node_id: str) -> Optional[socket.socket]:
        with self._pool_lock:
            return self._connections.get(node_id)

    def get_node_lock(self, node_id: str) -> Optional[threading.Lock]:
        with self._pool_lock:
            return self._node_locks.get(node_id)

    def remove_node(self, node_id: str):
        with self._pool_lock:
            if node_id in self._connections:
                try:
                    self._connections.pop(node_id).close()
                except Exception:
                    pass
                print(f"[*] ConnectionPool: Removed node {node_id}")


connection_pool = ConnectionPool()
