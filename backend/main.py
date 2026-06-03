"""
Main application file for the Notes API.
Handles routing, database connection, and CRUD operations.
"""

from fastapi import FastAPI, HTTPException
import sqlite3

from config import DATABASE_FILE

app = FastAPI()

#Initialize database connection
connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()

# cursor.execute("DROP TABLE IF EXISTS Notes")


#Initialize notes table
cursor.execute('''CREATE TABLE IF NOT EXISTS Notes(
Name TEXT PRIMARY KEY NOT NULL,
Content TEXT NOT NULL,
"Date Created" TEXT NOT NULL)''')

#post request to add a note to the database
@app.post("/note/")
def add_note(name: str, content: str, date_created: str):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO Notes (Name, Content, 'Date Created') VALUES (?, ?, ?)", (name, content, date_created))
        conn.commit()
        conn.close()

        return {"Name": name, "Content": content, "Date Created": date_created}
    
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail = "A note with this name already exists")
    

#get request for contents of note with unique name
@app.get("/note/{note_name}")
def get_note(note_name: str):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Notes WHERE Name = ?", (note_name,))
    conn.commit()
    single_note = cur.fetchone()

    if single_note == None:
        raise HTTPException(status_code = 404, detail = "No note with name exists")
        
    return {"Note": single_note}


