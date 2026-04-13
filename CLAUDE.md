# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A secure Google Drive clone built as a Cyber Security high school final project. Features distributed file storage with 3-way replication, self-healing on node failure, JWT authentication, and granular access control (OWNER/EDITOR/VIEWER).

## Running the Services

All three services must run independently. The current monorepo paths (after refactoring from `server/`, `storage_server/`, `client/`) are:

**API Server** (`apps/api-server/`):
```bash
cd apps/api-server
pip install -r requirements.txt
python main.py
```
Required `.env`: `MONGO_URL`, `SECRET_KEY`, `STORAGE_ENCRYPTION_KEY`

**Storage Node** (`apps/storage-node/`):
```bash
cd apps/storage-node
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py
```
Required `.env`: `HOST=127.0.0.1`, `PORT=5001` (unique per node), `TRACKER_HOST`, `TRACKER_PORT=9001`, `STORAGE_ENCRYPTION_KEY` (must match API server)
> To run multiple nodes: use different `PORT` values and different working directories.

**Web Client** (`apps/web-client/`):
```bash
cd apps/web-client
npm install
npm run dev       # Dev server at localhost:5173
npm run build     # Production build
npm run lint      # ESLint
```

## Architecture

```
Web Client (React/Vite)
    │ REST API
    ▼
API Server (FastAPI)
    ├── Tracker (port 9001) — receives heartbeats from storage nodes every 30s
    ├── Data Server (port 9000) — maintains persistent connections, routes file commands
    └── Maintenance Loop (every 60s) — detects dead nodes (>2min silent), triggers repair
    │
    ├── MongoDB Atlas — users, items, nodes, sharing metadata
    │
    └── Storage Nodes (N × persistent TCP workers)
            ├── Sends heartbeats with free disk space
            ├── Receives UPLOAD/DOWNLOAD/DELETE commands
            └── Stores files in local data/ directory
```

### Communication Protocol

`libs/shared/protocol.py` defines the TLV (Type-Length-Value) binary protocol used between the API server and storage nodes. All communication is Fernet (AES-128) encrypted.

- **TLV format**: `[Command(1B)] [[FieldID(1B)][Length(4B)][Value(var)]...]`
- **Commands**: UPLOAD, DOWNLOAD, DELETE, HEARTBEAT, REGISTER
- **Transport classes**: `SecureTransport` (sync), `AsyncSecureTransport` (async, used everywhere now)
- File payloads stream as raw encrypted chunks separate from control packets

### File Upload Flow

1. Client POSTs to `/items/upload/init` → creates FileModel (status=PENDING)
2. Client POSTs file content to `/items/upload/{item_id}/content`
3. `items_service` asks `TrackerService` for 3 best nodes (by free space)
4. `storage_service` sends UPLOAD command to all 3 nodes concurrently (3-way replication)
5. DB updated with `node_ids` list and SHA256 `file_hash`

### Self-Healing Flow

1. Node stops sending heartbeats → maintenance loop marks it OFFLINE
2. `RepairService` finds files with the dead `node_id`
3. For each affected file: downloads from a surviving node, uploads to a new healthy node
4. DB updated: dead node removed, replacement node added — always maintains 3 replicas

### API Server Layering

```
api/routes/       →  HTTP endpoints (auth, items, user)
services/         →  Business logic (items, auth, share, repair)
gateways/
  repositories/   →  MongoDB data access (Motor async driver)
  storage/
    tracker/      →  TrackerServer (manages node registry + heartbeats)
    client/       →  StorageClient (sends commands to nodes)
    services/     →  TrackerService, StorageService, RepairService
models/           →  Pydantic models (User, Item, File, Folder, Node)
```

## Architectural Standards (from GEMINI.md)

- **Clean Architecture**: Strict separation — Transport/gateways (Handlers) → Business Logic (Services) → Data/Models. Do not mix protocol logic with service logic.
- **Single Responsibility**: If a function handles both networking and disk I/O, flag it for refactoring.
- **Proactive Refactoring**: If a requested feature would damage architectural integrity, point it out and suggest a cleaner alternative before implementing.
- **Placement Precision**: Always specify the exact file path, class, and method/line where a change belongs.

## `--git` Shortcut

When the user types `--git`, autonomously:
1. Run `git status` and `git diff HEAD`
2. Stage all relevant changes
3. Check `git log -n 5` to match commit message style
4. Commit with a concise professional message describing the "why" and "what"
5. Push to the current branch
6. Report a brief summary of the commit and push status
