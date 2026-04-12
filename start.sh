#!/bin/bash

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "[*] Starting API Server..."
cd "$ROOT/apps/api-server"
source venv/bin/activate
python main.py &
API_PID=$!
deactivate

echo "[*] Starting Storage Node..."
cd "$ROOT/apps/storage-node"
source venv/bin/activate
python main.py &
STORAGE_PID=$!
deactivate

echo "[*] Starting Web Client..."
cd "$ROOT/apps/web-client"
npm run dev &
CLIENT_PID=$!

echo ""
echo "[+] All services started:"
echo "    API Server   → PID $API_PID"
echo "    Storage Node → PID $STORAGE_PID"
echo "    Web Client   → PID $CLIENT_PID  (http://localhost:5173)"
echo ""
echo "Press Ctrl+C to stop all services."

trap "echo ''; echo '[*] Stopping...'; kill $API_PID $STORAGE_PID $CLIENT_PID 2>/dev/null; exit 0" INT
wait
