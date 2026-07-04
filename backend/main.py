"""
Main application file for the Notes API.
Handles routing, database connection, and CRUD operations.
"""

from fastapi import FastAPI, HTTPException
import sqlite3

from config import DATABASE_FILE
import helper

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Initialize database connection
connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()

#Initialize notes table
cursor.execute('''CREATE TABLE IF NOT EXISTS Notes(
Name TEXT PRIMARY KEY NOT NULL,
Content TEXT NOT NULL,
"Date Created" TEXT NOT NULL,
'Date Modified' TEXT NOT NULL)''')

#post request to add a note to the database
@app.post("/note/")
def add_note(note_name: str, content: str, date_created: str, date_modified: str):
    if helper.does_note_exist(note_name):
        raise HTTPException(status_code=400, detail = "A note with this name already exists")
    
    return helper.add_single_note(note_name, content, date_created, date_modified)

#get request for all notes
@app.get("/notes")
def get_all_notes():
    return helper.return_all_notes()

#get request for contents of note with unique name
@app.get("/note/{note_name}")
def get_note(note_name: str):
    if not helper.does_note_exist(note_name):
        raise HTTPException(status_code = 404, detail = "No note with name exists")
    
    return helper.return_note(note_name)

#put request to modify a note or create note if it does not exist, update date_modified
@app.put("/note/{note_name}")
def modify_note(note_name: str, content: str, date_modified: str):
    if not helper.does_note_exist(note_name):
        raise HTTPException(status_code = 404, detail = "No note with name exists")
    
    return helper.modify_note(content, date_modified, note_name)

#put endpoint that modifys a notes name only
@app.put("/note/{note_name}/rename")
def change_name(note_name: str, new_name: str):
    if not helper.does_note_exist(note_name):
        raise HTTPException(status_code = 404, detail = "No note with name exists")
    
    return helper.change_note_name(new_name, note_name)

#delete note endpoint
@app.delete("/note/{note_name}")
def delete_note(note_name: str):
    if not helper.does_note_exist(note_name):
        raise HTTPException(status_code = 404, detail = "No note with name exists")
    
    return helper.delete_note(note_name)
