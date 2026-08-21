# Note API

## A RESTful Notes API built with FastAPI and SQLite.

This project is a RESTful Notes API built with FastAPI and SQLite. It supports creating, reading, updating, renaming, and deleting notes. 

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

- **POST /notes** — Create a new note  
- **GET /notes** — Get all notes  
- **GET /note/{note_name}** — Retrieve a single note  
- **PUT /note/{note_name}/modify** — Modify note content  
- **PUT /note/{note_name}/rename** — Rename a note  
- **DELETE /note/{note_name}** — Delete a note  

## Pydantic Models

Models are used when creating a note, renaming a note, or modifying a note's
content. The model data is sent as JSON in the request body.

### Creation Note

The Creation_Note model is used when creating a new note with POST /notes.

It accepts the following fields:

- **name** — Name of the note
- **content** — Content of the note. This field is optional.
- **date_created** — Date the note was created
- **date_modified** — Date the note was last modified

**Example Request**

```json
{
    "name": "shopping",
    "content": "milk, eggs, bread",
    "date_created": "2026-06-09",
    "date_modified": "2026-06-09"
}
```

### Name Modification Note

The Name_Modification_Note model is used when renaming a note with PUT /note/{note_name}/rename.

It accepts the following fields:

- **new_name** — The new name for the note
- **date_modified** — Date the note was last modified

Example Request
```json
{
    "new_name": "groceries",
    "date_modified": "2026-06-10"
}
```

### Content Modification Note

The Content_Modification_Note model is used when modifying a note's content with PUT /note/{note_name}/modify.

It accepts the following fields:

- **content** — The new content of the note
- **date_modified** — Date the note was last modified

Example Request
```json
{
    "content": "milk, eggs, bread, apples",
    "date_modified": "2026-06-10"
}
```

### Project Structure

```text
.
├── .gitignore    # Git ignore rules
├── config.py     # Configuration (e.g. database path)
├── helper.py     # Helper functions for CRUD operations
├── main.py       # FastAPI app and route definitions
└── README.md     # Project documentation
```

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