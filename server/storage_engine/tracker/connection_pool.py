import threading

class ConnectionPool:
    """
    A thread-safe registry to store and manage active socket connections from Storage Nodes.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ConnectionPool, cls).__new__(cls)
                cls._instance.connections = {}  # {node_id: socket}
        return cls._instance

    def register_node(self, node_id: str, sock):
        with self._lock:
            # If node already exists, close old socket
            if node_id in self.connections:
                try:
                    self.connections[node_id].close()
                except:
                    pass
            self.connections[node_id] = sock
            print(f"[*] ConnectionPool: Registered node {node_id}")

    def get_node_socket(self, node_id: str):
        with self._lock:
            return self.connections.get(node_id)

    def remove_node(self, node_id: str):
        with self._lock:
            if node_id in self.connections:
                del self.connections[node_id]
                print(f"[*] ConnectionPool: Removed node {node_id}")

connection_pool = ConnectionPool()