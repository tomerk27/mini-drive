secure-drive/
├── backend/
│   ├── app/
│   │   ├── main.py                # נקודת הכניסה ל-FastAPI
│   │   ├── auth/
│   │   │   ├── routes.py          # התחברות, הרשמה, JWT
│   │   │   ├── utils.py           # פונקציות הצפנה, בדיקות סיסמה
│   │   ├── files/
│   │   │   ├── routes.py          # העלאה, הורדה, מחיקה, שיתוף
│   │   │   ├── encryption.py      # הצפנה/פענוח קבצים (AES)
│   │   ├── database.py            # חיבור ל-PostgreSQL
│   │   ├── models.py              # ORM (SQLAlchemy)
│   │   └── config.py              # משתני סביבה (סיסמאות, מפתחות)
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── FileUploader.tsx
│   │   │   ├── FileList.tsx
│   │   └── api/
│   │       ├── auth.ts
│   │       └── files.ts
│   ├── package.json
│   └── .env
