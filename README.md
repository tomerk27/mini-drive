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
- HTTP Client: Native Fetch
- Styling: MUI Components + custom CSS files (e.g., fileItem.css)

3. TECH STACK (Backend & Data)
- Server Framework: Python FastAPI
- Database: MongoDB Atlas (Cloud)
- Database Driver: Motor (Async MongoDB driver)
- Data Validation: Pydantic (Schemas)
- Security & Hashing: Passlib (Bcrypt)
- Environment Management: python-dotenv
- Architecture: Client <-> Main Server (FastAPI) <-> Database Server (MongoDB)
- Authentication: JSON based (UserCreate Schema)
- Encryption Libraries: Passlib (for password hashing)

4. PROJECT STRUCTURE (Client Side - /src)
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
│   │   │   ├── fileApi.js
│   │   │   └── folderApi.js
│   │   ├── App.jsx
│   │   ├── components
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
│   │   ├── hooks
│   │   │   ├── useFilesUploader.js
│   │   │   ├── useFolder.js
│   │   │   └── useItemActionMenu.js
│   │   ├── main.jsx
│   │   ├── models
│   │   │   ├── fileItem.js
│   │   │   ├── folderItem.js
│   │   │   └── item.js
│   │   └── pages
│   │       └── mainPage.jsx
│   └── vite.config.js
├── README.md
└── server
    ├── .env                  <-- New: Environment variables
    ├── app
    │   ├── database.py       <-- Implemented: MongoDB Connection
    │   ├── models
    │   │   └── user.py       <-- Implemented: DB Model (Internal)
    │   ├── schemas
    │   │   └── user.py       <-- Implemented: Pydantic Schemas (Input/Output)
    │   └── main.py
    ├── main.py
    └── requirements.txt
    
5. KEY CODE SNIPPETS
- Upload Logic: `useFilesUploader` hook uses `FormData` to prepare files for the API.
- Data Models: The project uses specific classes (Item.js) to structure file/folder data.
- Backend Architecture: Separation of Concerns (Schemas for API I/O, Models for DB storage).

6. SECURITY FEATURES (Cyber Focus - Planned)
* Currently implemented:
    - Separation of Input (Schema) vs Storage (Model) to prevent data pollution.
    - Environment variable protection for DB Credentials (.env).
* Planned Features:
    - Access Control (ACL): Sharing mechanism with read/write permissions for other users.
    - Secure File Upload: Magic number validation, file renaming to prevent execution.
    - Authentication & Authorization: Robust user identity management (JWT).

7. CURRENT STATUS & ROADMAP
- [x] Initialize Project Structure (Client/Server)
- [x] Client: Setup React + Vite environment
- [x] Server: Setup FastAPI environment
- [x] Server: Configure Virtual Environment (venv) & Dependencies
- [x] **Database: Connect to MongoDB Atlas (Async/Motor)**
- [x] **Server: Create User DB Model (models/user.py)**
- [x] **Server: Create User Schemas (schemas/user.py)**
- [ ] Server: Implement Authentication Logic (Router/Service/Repo)
- [ ] Client: Build Login/Register pages
- [ ] Core: Implement File Upload logic

8. ARCHITECTURE & CODING STANDARDS
- Philosophy: Clean Code & High Modularity.
- Guideline: Split complex components into smaller, focused sub-components.
- Backend Pattern: 
    - **Schemas:** Define what the API receives and returns (Validation).
    - **Models:** Define what is stored in MongoDB.
    - **Database:** Centralized async connection.
- State Management: STRICT SEPARATION. All state (useState, useEffect) and logic must be extracted to Custom Hooks.

9. HOW TO RUN (DEVELOPMENT)

A. Server Side (Python):
1. Navigate to server: `cd server`
2. Activate venv: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
   *(Ensure `motor`, `python-dotenv`, `pydantic[email]`, `passlib[bcrypt]` are included)*
4. Setup Env: Create `.env` file
5. Run: `uvicorn main:app --reload`
> Server runs on: http://127.0.0.1:8000

B. Client Side (React):
1. Navigate to client: `cd client`
2. Install packages: `npm install`
3. Run: `npm run dev`
> Client runs on: http://localhost:5173 (usually)