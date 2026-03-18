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

7. CURRENT STATUS & ROADMAP
- [ ] **Storage: Implement Dedicated Storage Server (Socket-based)**
    - [ ] Design custom binary protocol for file transfer.
    - [ ] Implement TCP Socket Listener on Storage Server.
    - [ ] Integrate Socket Client in Main Server (Forwarding uploads).
- [ ] Core: Folder Creation & Navigation Logic
- [ ] Core: File Download
- [ ] Security: Implement File Sharing (Permissions)

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