# Jot

A minimal, fast note-taking app

## Features

- Create, rename, edit, and delete notes
- Rich text editing (Quill) with autosave. Saves shortly after you stop typing, and again every 10 seconds regardless
- Fuzzy search across note names (Fuse.js)
- Editor state persists across page refresh (via session storage)
- Fully containerized with Docker for consistent setup

## Tech Stack

**Backend:** Python, FastAPI, SQLite
**Frontend:** Vanilla JavaScript (ES modules), HTML, CSS, Quill (rich text editor), Fuse.js (fuzzy search)
**Infrastructure:** Docker, Docker Compose, Nginx (serving the frontend)

## Current Scope

This is a **single-shared-notes** app. There is no authentication or per-user data separation. Every visitor reads and writes the same note store. This was a deliberate choice to focus on the core note-taking API, editor experience, and Docker-based deployment first.

**Planned next steps:**
- User accounts & authentication
- Per-user note isolation
- Automated API test suite

## Running with Docker (recommended)

From the project root:

```bash
docker-compose up --build
```

- Frontend: [http://localhost:8080](http://localhost:8080)
- Backend API: [http://localhost:8000](http://localhost:8000)
- Interactive API docs (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)

Notes are persisted to `backend/database.db` on your host machine via a bind mount, so your data survives container rebuilds (`docker-compose down` / `docker-compose up --build` again).

To stop everything:

```bash
docker-compose down
```

## Running Manually (without Docker)

**Backend:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at `http://127.0.0.1:8000`.

**Frontend:**

```bash
cd frontend/src
python3 -m http.server 5500
```

Then open `http://localhost:5500` in your browser.

> Note: the frontend's API base URL is set in `frontend/config.js`. It defaults to `http://127.0.0.1:8000`, matching the manual/Docker backend setup above.

## API Reference

All endpoints are served from the backend at `/`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/notes` | Create a new note. Body: `{ name, content, date_created, date_modified }`. Returns `400` if the name already exists. |
| `GET` | `/notes` | Return all notes (names and modification dates). |
| `GET` | `/note/{note_name}` | Return a single note's full contents. Returns `404` if it doesn't exist. |
| `PUT` | `/note/{note_name}/rename` | Rename a note. Body: `{ new_name, date_modified }`. Returns `409` if the new name is already taken. |
| `PUT` | `/note/{note_name}/modify` | Update a note's content. Body: `{ content, date_modified }`. |
| `DELETE` | `/note/{note_name}` | Delete a note. |

Note names are URL-encoded when used as path segments (they may contain spaces or special characters).

## Project Structure

```
Jot/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── main.py          # FastAPI app and routes
│   ├── config.py         # Configuration (database filename)
│   ├── helper.py          # Database access functions
│   └── requirements.txt
└── frontend/
    ├── Dockerfile
    ├── config.js          # Backend API base URL
    ├── images/
    └── src/
        ├── index.html
        ├── app.js         # UI logic and event listeners
        ├── helper.js       # API calls, search, and rendering helpers
        └── styles.css
```
## API Tests

The backend includes a pytest suite to validate all FastAPI endpoints.

### Running Tests

From the project root:

```bash
cd backend
pytest