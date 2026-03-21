*** PROJECT CONTEXT: Google Drive Clone (Cyber Security Final Project) ***

1. OVERVIEW
- Type: Cyber Security High School Final Project.
- Goal: Build a secure cloud file storage system (Google Drive clone).
- Core Focus: Data security, secure file handling, and granular access control.
- Unique Feature (Planned): Advanced permission system allowing file/folder sharing with specific users (View/Edit roles).

2. TECH STACK (Frontend)
- Environment: Vite
- Framework: React 19
- Language: JavaScript (JSX)
- UI Library: Material UI (@mui/material, @mui/icons-material) + Emotion
- OAuth Library: @react-oauth/google (Google Identity Services)
- HTTP Client: Axios (Interceptors configured for auto-logout on 401)
- Routing: React Router Dom (v6)
- Styling: MUI ThemeProvider (Custom Light/Dark themes)

3. TECH STACK (Backend & Data)
- Server Framework: Python FastAPI
- Storage Server: Custom Python TCP Socket Server (Data Node)
- Database: MongoDB Atlas (Cloud)
- Database Driver: Motor (Async MongoDB driver)
- Data Validation: Pydantic (Schemas V2) + email-validator
- Security & Hashing: Passlib + Bcrypt (Secure Password Hashing)
- Token Management: python-jose (JWT generation & validation)
- File Handling: python-multipart
- Environment Management: python-dotenv
- Architecture: Client <-> Main Server (FastAPI) <-> Storage Server (Sockets)
- Authentication: JSON based (UserCreate Schema) + Bearer Token (JWT)

4. PROJECT STRUCTURE
.
├── client
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   │   └── vite.svg
│   ├── src
│   │   ├── api
│   │   │   ├── authApi.js
│   │   │   ├── axiosClient.js
│   │   │   ├── fileApi.js
│   │   │   └── folderApi.js
│   │   ├── App.jsx
│   │   ├── components
│   │   │   ├── authentication
│   │   │   │   ├── formsBox.jsx
│   │   │   │   ├── googleConnectionButton.jsx
│   │   │   │   ├── inputFields.jsx
│   │   │   │   └── submitButton.jsx
│   │   │   ├── filesGrid
│   │   │   │   └── filesGrid.jsx
│   │   │   ├── fileUploader.jsx
│   │   │   ├── item
│   │   │   │   ├── actionMenu.jsx
│   │   │   │   ├── item.jsx
│   │   │   │   └── itemIcon.jsx
│   │   │   └── topBar
│   │   │       ├── searchBar
│   │   │       │   └── searchBar.jsx
│   │   │       └── topBar.jsx
│   │   ├── context
│   │   │   └── auth
│   │   │       ├── authContext.js
│   │   │       └── authProvider.jsx
│   │   ├── hooks
│   │   │   ├── auth
│   │   │   │   ├── useLogin.js
│   │   │   │   └── useSignup.js
│   │   │   ├── useFilesUploader.js
│   │   │   ├── useFolder.js
│   │   │   └── useItemActionMenu.js
│   │   ├── main.jsx
│   │   ├── models
│   │   │   ├── fileItem.js
│   │   │   ├── folderItem.js
│   │   │   └── item.js
│   │   ├── pages
│   │   │   ├── dashboard.jsx
│   │   │   ├── loginPage.jsx
│   │   │   └── signupPage.jsx
│   │   └── routers
│   │       └── appRouter.jsx
│   └── vite.config.js
├── README.md
└── server
    ├── app
    │   ├── core
    │   │   ├── config.py
    │   │   ├── exceptions.py
    │   │   └── security.py
    │   ├── database.py
    │   ├── dependencies.py
    │   ├── models
    │   │   ├── item.py
    │   │   └── user.py
    │   ├── routes
    │   │   ├── auth.py
    │   │   └── items.py
    │   ├── schemas
    │   │   ├── item.py
    │   │   └── user.py
    │   ├── services
    │   │   ├── auth_service.py
    │   │   └── items_service.py
    │   └── utils
    │       ├── db_utils.py
    │       ├── item_utils.py
    │       ├── mappers.py
    │       └── time.py
    ├── main.py
    ├── requirements.txt

5. KEY CODE SNIPPETS
- **Secure Two-Step Upload:** Implemented a secure flow where metadata is initialized first (`POST /init`), creating a reserved DB entry. Content is uploaded only after validation (`PUT /content`) using the generated ID.
- **Data Mapping (DTOs):** `mappers.py` acts as a translation layer, converting MongoDB's internal `_id` (ObjectId) to a clean string `id` for the frontend.
- **Google OAuth Integration (Client):** Implemented `GoogleOAuthProvider` and `<GoogleLogin />` component. Retrieves ID Token successfully from Google but awaits backend verification logic.

6. SECURITY FEATURES (Cyber Focus)
* Currently implemented:
    - **NoSQL Injection Prevention:** Pydantic schemas strictly type-check inputs.
    - **Secure File Upload:** Ownership verification checks & Metadata/Content separation.
    - **Authentication:** JWT (Bearer Token) with Expiration.
    - **Password Hashing:** Bcrypt.
* Planned Features:
    - **Secure Google Auth:** Backend verification of Google ID Tokens (preventing client-side spoofing).
    - **Distributed Storage Architecture:** Decoupling physical storage from the API server using a custom binary protocol over TCP sockets.
    - Access Control (ACL): Sharing mechanism.
    - Magic Number Validation.

7. DISTRIBUTED STORAGE SYSTEM ROADMAP (Distributed Computing)
To transform the current single-node storage architecture into a robust Distributed Storage System, the following step-by-step implementation plan will be executed. This will provide fault tolerance, high availability, and scalability.

- [ ] **Phase 1: Architecture Shift & Node Registration (Control Plane)**
    - [ ] Update the Main API Server to act as a "Tracker" (NameNode) managing multiple storage nodes.
    - [ ] Implement a Heartbeat protocol: Storage nodes periodically ping the Main Server to report their health (IP, Port, Available Capacity).
    - [ ] Create a `StorageNode` collection in MongoDB to track active nodes dynamically.

- [ ] **Phase 2: Metadata Management & Intelligent Routing**
    - [ ] Update the MongoDB `ItemModel` to map each file to a list of `node_ids` holding that file.
    - [ ] Modify the Main Server's `StorageService` to route uploads/downloads dynamically by selecting an available node from the DB, removing the hardcoded IP/Port.

- [ ] **Phase 3: Data Replication & Upload Strategy**
    - [ ] Define a Replication Factor (e.g., RF=2 or RF=3) to ensure files are stored on multiple physical nodes.
    - [ ] Implement replication logic: The Main Server streams the file to a Primary Node, which then forwards it to Replica Nodes, or the Main Server orchestrates multi-node uploads directly.
    - [ ] Ensure database metadata is only finalized when replication is confirmed.

- [ ] **Phase 4: Fault Tolerance & Self-Healing**
    - [ ] Main Server detects offline nodes via missed heartbeats and marks them "Offline".
    - [ ] Implement an async Background Worker: Periodically scan for files whose replica count has fallen below the Replication Factor.
    - [ ] Trigger automated "Healing": Instruct a healthy node to transfer the missing file to another available node to restore redundancy.

- [ ] **Phase 5: Load Balancing & Advanced File Sharding**
    - [ ] Route client downloads using Round-Robin or Least-Connections to distribute bandwidth.
    - [ ] File Chunking (Optional): Split large files into smaller encrypted chunks distributed across different nodes (similar to BitTorrent/HDFS) to allow parallel downloading and better space utilization.

8. ARCHITECTURE & CODING STANDARDS
- Backend Pattern: Routes -> Services -> Mappers -> Schemas.
- Storage Architecture: Main Server (API Gateway) acts as a proxy, streaming data to isolated Storage Nodes via raw TCP sockets.
- Frontend: Hooks, Context API, and Centralized Axios calls.

9. HOW TO RUN (DEVELOPMENT)

A. Server Side (Python):
1. Navigate to server: `cd server`
2. Activate venv.
3. Install dependencies: `pip install -r requirements.txt`
4. Setup `.env` (MONGO_URL, SECRET_KEY).
5. Run: `uvicorn main:app --reload`

B. Client Side (React):
1. Navigate to client: `cd client`
2. Install: `npm install`
3. Setup `.env`:
   - `VITE_API_URL=http://127.0.0.1:8000`
   - `VITE_GOOGLE_CLIENT_ID=your-google-client-id`
4. **Google Cloud Config:** Ensure `http://localhost:5173` AND `http://127.0.0.1:5173` are added to "Authorized JavaScript origins".
5. Run: `npm run dev`