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
- HTTP Client: Axios (Interceptors configured)
- Routing: React Router Dom (v6)
- Styling: MUI ThemeProvider (Custom Light/Dark themes)

3. TECH STACK (Backend & Data)
- Server Framework: Python FastAPI
- Database: MongoDB Atlas (Cloud)
- Database Driver: Motor (Async MongoDB driver)
- Data Validation: Pydantic (Schemas) + email-validator
- Security & Hashing: Passlib + Bcrypt (Secure Password Hashing)
- **Token Management: python-jose (JWT generation & validation)**
- Environment Management: python-dotenv
- Architecture: Client <-> Main Server (FastAPI) <-> Database Server (MongoDB)
- Authentication: JSON based (UserCreate Schema) + **Bearer Token (JWT)**

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
    │   ├── models
    │   │   └── user.py
    │   ├── routes
    │   │   └── auth.py
    │   ├── schemas
    │   │   └── user.py
    │   ├── services
    │   │   └── auth_service.py
    │   └── utils
    ├── main.py
    └── requirements.txt

5. KEY CODE SNIPPETS
- **Shared Forms Component:** `FormsBox` is used for both Login and Signup to adhere to DRY (Don't Repeat Yourself) principles, dynamically rendering fields based on `mode` prop.
- **Custom Google Icon:** Hand-crafted SVG component to maintain brand colors within MUI buttons.
- **Backend Architecture:** Separation of Concerns (Schemas for API I/O, Models for DB storage).

6. SECURITY FEATURES (Cyber Focus)
* Currently implemented:
    - **NoSQL Injection Prevention:** Utilizing Pydantic schemas to strictly type-check inputs (preventing operator injection attacks).
    - **Separation of Concerns:** Input (Schema) vs Storage (Model) to prevent data pollution.
    - **Environment Protection:** DB Credentials and SECRET_KEY stored securely in `.env`.
    - **Password Hashing:** Passwords are never stored in plain text; using Bcrypt for strong hashing.
    - **Input Validation:** Strict typing and email validation using Pydantic.
    - **JWT Authentication:** Secure stateless authentication using signed JSON Web Tokens.
* Planned Features:
    - Access Control (ACL): Sharing mechanism with read/write permissions for other users.
    - Secure File Upload: Magic number validation, file renaming to prevent execution.
    - Middleware: Protect routes using JWT validation.

7. CURRENT STATUS & ROADMAP
- [x] Initialize Project Structure (Client/Server)
- [x] Client: Setup React + Vite environment
- [x] Server: Setup FastAPI environment
- [x] Database: Connect to MongoDB Atlas (Async/Motor)
- [x] Server: Create User DB Model & Schemas
- [x] Server: Implement Registration Logic (Route/Service/Repo)
- [x] Server: Implement Password Hashing (Bcrypt)
- [x] Server: Implement Login Logic (JWT Token generation)
- [x] **Client: Setup React Router & Theme Provider**
- [x] **Client: Build Login/Register pages (UI & Logic complete)**
- [x] **Client: Implement Shared Form Components (FormsBox)**
- [ ] Core: Implement File Upload logic
- [ ] Client: Build Dashboard/Main Page

8. ARCHITECTURE & CODING STANDARDS
- Philosophy: Clean Code & High Modularity.
- Guideline: Split complex components into smaller, focused sub-components.
- Backend Pattern: 
    - **Schemas:** Define what the API receives and returns (Validation).
    - **Models:** Define what is stored in MongoDB.
    - **Services:** Business logic (hashing, checks).
    - **Database:** Centralized async connection.
- State Management: STRICT SEPARATION. All state (useState, useEffect) and logic must be extracted to Custom Hooks.

9. HOW TO RUN (DEVELOPMENT)

A. Server Side (Python):
1. Navigate to server: `cd server`
2. Activate venv: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Setup Env: Create `.env` file with `MONGO_URL`, `DB_NAME`, and `SECRET_KEY`.
5. Run: `uvicorn main:app --reload`
> Server runs on: http://127.0.0.1:8000
> API Docs (Swagger): http://127.0.0.1:8000/docs

B. Client Side (React):
1. Navigate to client: `cd client`
2. Install packages: `npm install`
3. Setup Env: Create `.env` file with `VITE_API_URL=http://127.0.0.1:8000`.
4. Run: `npm run dev`
> Client runs on: http://localhost:5173