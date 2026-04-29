"""
Singleton registry of persistent TCP sockets to storage nodes.
The DataServer stores each node's connection here so upload/download
commands can be routed without opening a new socket every time.
"""

import socket
import threading
from typing import Dict, Optional


class ConnectionPool:
    """
    Thread-safe, singleton registry of live storage-node connections.

    Each storage node holds exactly one persistent TCP socket to the API server.
    This pool maps node IDs to those sockets and provides a per-node lock so
    concurrent UPLOAD/DOWNLOAD commands to the same node don't interleave.
    """

    _instance = None
    _instance_lock = threading.Lock()
    _connections: Dict[str, socket.socket]
    _node_locks: Dict[str, threading.Lock]
    _pool_lock: threading.Lock

    def __new__(cls):
        """
        Ensures only one ConnectionPool ever exists (singleton pattern).

        The outer _instance_lock prevents two threads from both seeing
        _instance as None and each creating their own pool.
        """
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(ConnectionPool, cls).__new__(cls)
                cls._instance._connections = {}
                cls._instance._node_locks = {}
                cls._instance._pool_lock = threading.Lock()
        return cls._instance

    def register_node(self, node_id: str, sock: socket.socket):
        """
        Stores a new socket for a node, replacing any previous connection.

        Called by the DataServer when a storage node sends a REGISTER packet.
        If the node reconnects after a drop, the stale socket is closed first
        to avoid resource leaks.

        Args:
            node_id: Unique identifier of the connecting storage node.
            sock: The live TCP socket for this node.
        """
        with self._pool_lock:
            # Close the old socket if this node is re-registering after a disconnect.
            if node_id in self._connections:
                try:
                    self._connections[node_id].close()
                except Exception:
                    pass
            self._connections[node_id] = sock
            # Create a lock for this node only once — reuse it on reconnects.
            if node_id not in self._node_locks:
                self._node_locks[node_id] = threading.Lock()
            print(f"[*] ConnectionPool: Registered node {node_id}")

    def get_node_socket(self, node_id: str) -> Optional[socket.socket]:
        """
        Returns the live socket for the given node, or None if not connected.

        Args:
            node_id: The node to look up.

        Returns:
            The node's TCP socket, or None if the node is not registered.
        """
        with self._pool_lock:
            return self._connections.get(node_id)

    def get_node_lock(self, node_id: str) -> Optional[threading.Lock]:
        """
        Returns the per-node lock used to serialize commands to that node.

        Callers acquire this lock before sending a command so that two
        concurrent operations (e.g. upload + delete) don't write to the
        same socket at the same time.

        Args:
            node_id: The node whose lock to retrieve.

        Returns:
            A threading.Lock for the node, or None if the node is not registered.
        """
        with self._pool_lock:
            return self._node_locks.get(node_id)

    def remove_node(self, node_id: str):
        """
        Closes and removes a node's socket from the pool.

        Called when a node is marked OFFLINE so the dead socket is cleaned up
        and future lookups correctly return None.

        Args:
            node_id: The node to deregister.
        """
        with self._pool_lock:
            if node_id in self._connections:
                try:
                    # pop() removes the entry and close() releases the OS socket.
                    self._connections.pop(node_id).close()
                except Exception:
                    pass
                print(f"[*] ConnectionPool: Removed node {node_id}")


# Module-level singleton — import this instance everywhere instead of calling ConnectionPool().
connection_pool = ConnectionPool()
