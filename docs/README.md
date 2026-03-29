*** PROJECT CONTEXT: Google Drive Clone (Cyber Security Final Project) ***

1. OVERVIEW
- Type: Cyber Security High School Final Project.
- Goal: Build a secure cloud file storage system (Google Drive clone).
- Core Focus: Data security, secure file handling, and granular access control.
- Architecture: Persistent Worker Architecture (Distributed).

2. TECH STACK (Frontend)
- Framework: React 19 (Vite)
- UI Library: Material UI (@mui/material)
- HTTP Client: Axios (Interceptors for 401 handling)
- Routing: React Router Dom (v6)

3. TECH STACK (Backend & Data)
- Server Framework: Python FastAPI (Main Server)
- Storage Server: Custom Python TCP Socket Worker (Node)
- Protocol: Secure TLV (Type-Length-Value) over TCP
- Database: MongoDB Atlas (Cloud)
- Encryption: Fernet (AES-128) for all data in transit

4. PROJECT STRUCTURE
.
├── client/             # React Frontend
├── server/             # Main API Server & Tracker
├── storage_server/     # Storage Node Worker
└── shared/             # Unified TLV Protocol

5. DISTRIBUTED STORAGE SYSTEM ROADMAP (STATUS)
- [x] **Phase 1: Architecture Shift & Node Registration**
    - [x] Main Server acts as "Tracker" managing persistent sockets.
    - [x] Nodes register themselves on startup.
- [x] **Phase 2: Heartbeat & Metrics**
    - [x] Nodes report free space and health every 30s.
    - [x] Tracker marks dead nodes OFFLINE automatically.
- [x] **Phase 3: Data Replication**
    - [x] Files are stored on **3 different nodes** simultaneously.
- [x] **Phase 4: Self-Healing**
    - [x] Reactive repair: When a node dies, the system automatically redistributes its files to healthy nodes.
- [ ] **Phase 5: Load Balancing & Optimization**
    - [ ] Round-robin download selection.

6. HOW TO RUN (DEVELOPMENT)

A. Main API Server:
1. `cd server`
2. `pip install -r requirements.txt`
3. Setup `.env`: `MONGO_URL`, `SECRET_KEY`, `STORAGE_ENCRYPTION_KEY`.
4. `python main.py`

B. Storage Node (Worker):
1. `cd storage_server`
2. `python3 -m venv venv`
3. `source venv/bin/activate`
4. `pip install -r requirements.txt`
5. Setup `.env`:
   - `HOST=127.0.0.1` (Local listener)
   - `PORT=5001` (Unique port for each node)
   - `TRACKER_HOST=127.0.0.1` (Main server IP)
   - `TRACKER_PORT=9001`
   - `STORAGE_ENCRYPTION_KEY=...` (Must match Main Server)
6. `python main.py`
*Note: To run multiple nodes, use different PORT numbers and different folders.*

C. Client Side (React):
1. `cd client`
2. `npm install`
3. `npm run dev`
