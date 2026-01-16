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
- Database: MongoDB
- Architecture: Client <-> Main Server (FastAPI) <-> Database Server (MongoDB)
- Authentication: [TBD - To Be Decided]
- Encryption Libraries: [TBD - To Be Decided]

4. PROJECT STRUCTURE (Client Side - /src)
  /api
    - fileApi.js (File-related server calls)
    - folderApi.js (Folder-related server calls)
  /assets/icons
    - (SVG and JSX icons)
  /components
    /fileItem
      - FileItem.jsx (Main view component)
      - FileActionMenu.jsx (Menu view component)
      - FileIcon.jsx (Icon logic)
      - useFileActionMenu.js (Menu logic/state)
    /filesGrid
      - filesGrid.jsx (Grid layout container)
    /topBar
      /searchBar
        - searchBar.jsx, searchBar.css
      - topBar.jsx
    - fileUploader.jsx (Upload component)
  /hooks
    - useFilesUploader.js (Logic for file selection & FormData)
    - useFolder.js
  /models
    - fileItem.js
    - folderItem.js
    - Item.js (Class/Data structure definitions)
  /pages
    - mainPage.jsx

5. KEY CODE SNIPPETS
- Upload Logic: `useFilesUploader` hook uses `FormData` to prepare files for the API.
- Data Models: The project uses specific classes (Item.js) to structure file/folder data.

6. SECURITY FEATURES (Cyber Focus - Planned)
* Currently implemented: None.
* Planned Features:
    - Access Control (ACL): Sharing mechanism with read/write permissions for other users.
    - Secure File Upload: Magic number validation, file renaming to prevent execution.
    - Authentication & Authorization: Robust user identity management.
    - Data Encryption: (Optional/If time permits).

7. CURRENT STATUS
- Infrastructure: Basic React structure is ready.
- Active Task: Building the Basic GUI to display files using Material UI (MUI).
- Backend Status: Python FastAPI & MongoDB selected, but not fully connected yet.

8. ARCHITECTURE & CODING STANDARDS
- Philosophy: Clean Code & High Modularity.
- Guideline: Split complex components into smaller, focused sub-components.
- State Management: STRICT SEPARATION. All state (useState, useEffect) and logic must be extracted to Custom Hooks. Components should remain purely presentational (View only).
- Accessibility: Do NOT use ARIA attributes (keep JSX clean and focused on core logic).
- Structure: Keep related files (JSX, CSS/Styles, Sub-components, Hooks) grouped in feature folders.