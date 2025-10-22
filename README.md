# BragBoard API

This is a FastAPI backend for the BragBoard application.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn sqlalchemy psycopg2-binary passlib python-jose bcrypt
    ```

2.  **Create a PostgreSQL database named `project_db`.**

3.  **Update the database URL in `backend/database.py`:**
    ```python
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:yourpassword@localhost/project_db"
    ```

## Running the application

```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
