import socket
import threading
import os
import sys
import time

# Add project root to sys.path for shared module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.handlers.socket_handler import handle_client
from shared.protocol import CommandType, Field, pack, send_packet, receive_decrypted_packet
from app.handlers.heartbeat_handler import HeartbeatHandler
from app.services.system_metrics_service import SystemMetricsService

def heartbeat_loop():
    """Background thread to send heartbeats every 30 seconds."""
    print(f"[*] Starting Heartbeat loop for {settings.NODE_ID}...")
    while True:
        try:
            free_space = SystemMetricsService.get_free_space()
            HeartbeatHandler.send_heartbeat(free_space)
        except Exception as e:
            print(f"[!] Heartbeat Error: {e}")
        time.sleep(30)

def connect_to_main_server():
    """
    Acts as a Worker: Connects to the Main Server and waits for commands.
    """
    key = settings.STORAGE_ENCRYPTION_KEY.encode()
    
    while True:
        try:
            print(f"[*] Attempting to connect to Main Server at {settings.TRACKER_HOST}:9000...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((settings.TRACKER_HOST, 9000))
            
            # Registration
            reg_packet = pack(CommandType.REGISTER, {Field.NODE_ID: settings.NODE_ID})
            send_packet(sock, reg_packet, key)
            
            print(f"[+] Successfully connected and registered as {settings.NODE_ID}")
            
            # Stay connected and handle incoming commands from the Main Server
            from app.handlers.command_router import route_command
            
            while True:
                # Wait for orders (UPLOAD/DOWNLOAD/DELETE)
                decrypted_data = receive_decrypted_packet(sock, key)
                if not decrypted_data:
                    print("[!] Connection closed by Main Server.")
                    break
                
                # Process the command
                route_command(sock, decrypted_data)
                
        except Exception as e:
            print(f"[!] Connection failed: {e}. Retrying in 10 seconds...")
            time.sleep(10)
        finally:
            try:
                sock.close()
            except:
                pass

if __name__ == "__main__":
    # Start the heartbeat in the background as a daemon thread
    threading.Thread(target=heartbeat_loop, daemon=True).start()
    
    # Start the main worker connection
    connect_to_main_server()
