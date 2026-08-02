# URL Shortener

This project is a simple URL shortener built with a FastAPI backend and a React/Vite frontend. The backend accepts a long URL, generates a short unique code, stores the mapping, and redirects users to the original URL when the short link is visited.

## Project Overview

The application follows a simple flow:

1. The user submits a long URL through the API.
2. The backend generates a short code.
3. The mapping between the short code and the original URL is stored.
4. The short code can later be used to redirect the user to the original URL.

## Project Structure

- App/API: FastAPI backend
  - main.py: application entry point
  - routes/: API endpoints for shortening, redirecting, health checks, and stats
  - services/: business logic for URL creation and lookup
  - models.py: database models
  - database.py: database connection and session setup
  - schemas.py: request/response schemas
- Client: React + Vite frontend
  - FE is in progress.

## Backend Logic

The backend exposes endpoints to:

- shorten a URL
- redirect a short code to the original URL
- retrieve URL stats
- check backend health

The core idea is to store a record such as:

- short_code
- original_url
- created_at
- expires_at
- click_count

When the short link is visited, the backend looks up the short code and redirects to the stored original URL.

## Setup Instructions

### 1. Backend setup

Navigate to the backend folder:

```bash
cd App
```

Create and activate a Python virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If you want to run lint checks as well:

```bash
pip install -r requirements-dev.txt
```

### 2. Environment configuration

Create an environment file in App with your database settings if needed. Example:

```env
DATABASE_URL=sqlite:///./url_shortener.db
```

Or configure SQL Server values if you are using SQL Server.

### 3. Run the backend

```bash
cd API
uvicorn main:app --host 127.0.0.1 --port 8000
```

The API will be available at:

- http://127.0.0.1:8000/docs

## Frontend Status

FE is in progress.
