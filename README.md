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
- HTTP Client: Axios (Interceptors configured for auto-logout on 401)
- Routing: React Router Dom (v6)
- Styling: MUI ThemeProvider (Custom Light/Dark themes)

3. TECH STACK (Backend & Data)
- Server Framework: Python FastAPI
- Database: MongoDB Atlas (Cloud)
- Database Driver: Motor (Async MongoDB driver)
- Data Validation: Pydantic (Schemas V2) + email-validator
- Security & Hashing: Passlib + Bcrypt (Secure Password Hashing)
- Token Management: python-jose (JWT generation & validation)
- File Handling: python-multipart
- Environment Management: python-dotenv
- Architecture: Client <-> Main Server (FastAPI) <-> Database Server (MongoDB)
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
- **Data Mapping (DTOs):** `mappers.py` acts as a translation layer, converting MongoDB's internal `_id` (ObjectId) to a clean string `id` for the frontend, preventing data leaks and Pydantic validation errors.
- **Axios Interceptors:** Automatic handling of expired tokens (401 Unauthorized) by clearing storage and redirecting to Login, ensuring a secure user session lifecycle.

6. SECURITY FEATURES (Cyber Focus)
* Currently implemented:
    - **NoSQL Injection Prevention:** Pydantic schemas strictly type-check inputs.
    - **Secure File Upload:** - Ownership verification checks (User cannot upload content to an ID they don't own).
        - Separation of Metadata (Init) and Binary Data (Content).
    - **Authentication:** JWT (Bearer Token) with Expiration.
    - **Password Hashing:** Bcrypt.
    - **Auto-Logout:** Frontend intercepts 401 errors to prevent usage with stale tokens.
* Planned Features:
    - Access Control (ACL): Sharing mechanism with read/write permissions.
    - Magic Number Validation: verifying actual file types on the server side.

7. CURRENT STATUS & ROADMAP
- [x] Initialize Project Structure (Client/Server)
- [x] Database: Connect to MongoDB Atlas (Async/Motor)
- [x] Auth: Registration & Login (JWT + Bcrypt)
- [x] Client: Login/Register UI & Logic
- [x] **Architecture: Implement Service/Repository Pattern for Items**
- [x] **Core: Secure File Upload (Two-Step Init/Content Flow)**
- [x] **Core: Data Mappers (MongoDB -> Frontend DTOs)**
- [x] **Client: Dashboard & File Grid UI**
- [x] **Client: Token Expiration Handling (Interceptors)**
- [ ] Core: Folder Creation & Navigation Logic
- [ ] Core: File Download
- [ ] Security: Implement File Sharing (Permissions)

8. ARCHITECTURE & CODING STANDARDS
- Backend Pattern: 
    - **Routes:** Endpoint definition (I/O).
    - **Services:** Business logic & DB transactions.
    - **Mappers:** converting DB models to Response schemas.
    - **Schemas:** Pydantic V2 definitions.
- Frontend:
    - **Hooks:** Logic separation (e.g., `useFilesUploader`).
    - **API Layer:** Centralized Axios calls.

9. HOW TO RUN (DEVELOPMENT)

A. Server Side (Python):
1. Navigate to server: `cd server`
2. Activate venv.
3. Install dependencies: `pip install -r requirements.txt`
4. Setup `.env` (MONGO_URL, SECRET_KEY).
5. Run: `uvicorn main:app --reload`
> Docs: http://127.0.0.1:8000/docs

B. Client Side (React):
1. Navigate to client: `cd client`
2. Install: `npm install`
3. Setup `.env` (`VITE_API_URL=http://127.0.0.1:8000`).
4. Run: `npm run dev`
> App: http://localhost:5173