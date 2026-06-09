# Note API

## A RESTful Notes API built with FastAPI and SQLite.

This project is a RESTful Notes API built with FastAPI and SQLite. It supports creating, reading, updating, renaming, and deleting notes. I built it to practice backend development and to learn how to structure a small API using Python and SQL.

## Features
- **Create notes**
- **Get all note names**
- **Retrieve a single note**
- **Update note content**
- **Rename notes**
- **Delete notes**

## Installation

1. Clone the repository:
   git clone <https://github.com/Its-Me573/fastapi-NotesAPI.git>

2. Install dependencies:
   pip install fastapi uvicorn

3. Run the server:
   uvicorn main:app --reload

## API Endpoints

- **POST /note** — Create a new note  
- **GET /note/get_all_names** — Get all note names  
- **GET /note/{note_name}** — Retrieve a single note  
- **PUT /note/{note_name}** — Update note content  
- **PUT /note/{note_name}/rename** — Rename a note  
- **DELETE /note/{note_name}** — Delete a note  

## Example Request / Response

### GET /note/{note_name}

**Request**
GET /note/shopping
**Response**
{
  "note_name": "shopping",
  "content": "milk, eggs, bread",
  "date_created": "2026-06-09",
  "date_modified": "2026-06-09"
}

## Project Structure

.
├── .gitignore    # Git ignore rules
├── config.py     # Configuration (e.g. database path)
├── helper.py     # Helper functions for CRUD operations
├── main.py       # FastAPI app and route definitions
└── README.md     # Project documentation

## Future Improvements

These are potential enhancements if the project were expanded:

- Add authentication for private notes
- Add tests for core endpoints
- Improve error handling and validation
- Split helper.py into modules if the project grows

## Tech Stack

- Python
- FastAPI
- SQLite

## License
This project is licensed under the MIT License.