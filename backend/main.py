"""
Main application file for the Notes API.
Handles routing, database connection, and CRUD operations.
"""
import sqlite3
import helper

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import DATABASE_FILE

from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#For initial note creation
class Creation_Note(BaseModel):
    name: str
    content: str | None = None
    date_created: str
    date_modified: str


#For Name Modification
class Name_Modification_Note(BaseModel):
    new_name: str
    date_modified: str


#For content modification
class Content_Modification_Note(BaseModel):
    content: str
    date_modified: str


#Initialize database connection
connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()


#Initialize notes table
cursor.execute('''CREATE TABLE IF NOT EXISTS Notes(
Name TEXT PRIMARY KEY NOT NULL,
Content TEXT NOT NULL,
"Date Created" TEXT NOT NULL,
'Date Modified' TEXT NOT NULL)''')


#post request to add a note to the database, using Creation_Note model
@app.post("/note/")
def add_note(new_note: Creation_Note):
    if helper.does_note_exist(new_note.name):
        raise HTTPException(status_code = 400, detail = "A note with this name already exists")

    return helper.add_single_note(new_note.name, new_note.content, new_note.date_created, new_note.date_modified)



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


#put request to modify a note
@app.put("/note/{note_name}")
def modify_note(note_name: str, modified_Note: Content_Modification_Note):
    if not helper.does_note_exist(note_name):
            raise HTTPException(status_code = 404, detail = "No note with name exists")

    return helper.modify_note(modified_Note.content, modified_Note.date_modified, note_name)


#put endpoint that modifys a notes name only
#rewrite this function to use a model, the Change_Note name modal
@app.put("/note/{note_name}/rename")
def change_name(note_name: str, new_name: str):
    if not helper.does_note_exist(note_name):
        raise HTTPException(status_code = 404, detail = "No note with name exists")
    
    return helper.change_note_name(new_name, note_name)


#delete note endpoint
#this functnion will stay the exact same
@app.delete("/note/{note_name}")
def delete_note(note_name: str):
    if not helper.does_note_exist(note_name):
        raise HTTPException(status_code = 404, detail = "No note with name exists")
    
    return helper.delete_note(note_name)