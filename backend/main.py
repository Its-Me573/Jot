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
"Date Created" TEXT NOT NULL,
'Date Modified' TEXT NOT NULL)''')


#post request to add a note to the database
@app.post("/note/")
def add_note(name: str, content: str, date_created: str, date_modified: str):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO Notes (Name, Content, 'Date Created', 'Date Modified') VALUES (?, ?, ?, ?)", (name, content, date_created, date_modified))
        conn.commit()
        conn.close()

        return {"Name": name, "Content": content, "Date Created": date_created, "Date Modified": date_modified}
    
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail = "A note with this name already exists")


#get request for all note names
@app.get("/note/get_all_names")
def get_all_note_names():
    #returns each of the names o each of the rows of notes
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    cur.execute("Select * From Notes")
    all_notes = cur.fetchall()

    cur.close()
    return {"Notes": all_notes}

#get request for contents of note with unique name
@app.get("/note/{note_name}")
def get_note(note_name: str):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Notes WHERE Name = ?", (note_name,))
    single_note = cur.fetchone()

    if single_note == None:
        raise HTTPException(status_code = 404, detail = "No note with name exists")
        
    cur.close()
    return {"Note": single_note}


#put request to modify a note or create note if it does not exist, update date_modified
@app.put("/note/{note_name}")
def modify_note(note_name: str, content: str, date_modified: str):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    #Check if note exists
    cur.execute("SELECT * FROM Notes WHERE Name = ?", (note_name,))
    single_note = cur.fetchone()

    if single_note == None:
        conn.close()
        raise HTTPException(status_code = 404, detail = "No note with name exists")

    #Update only content and date_modified    
    cur.execute('''
        UPDATE Notes
        SET Content = ?, "Date Modified" = ?
        WHERE Name = ?
    ''', (content, date_modified, note_name))
    conn.commit()

    #return the note the stores the row modified
    cur.execute("SELECT * FROM Notes WHERE Name = ?", (note_name,))
    modified_note = cur.fetchone()
    conn.close()

    return {"Modified Note": modified_note}

#put endpoint that modifys a notes name only
@app.put("/note/{note_name}/rename")
def change_name(note_name: str, new_name: str):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()

    #Check if note exists
    cur.execute("SELECT * FROM Notes WHERE Name = ?", (note_name,))
    single_note = cur.fetchone()

    if single_note == None:
        conn.close()
        raise HTTPException(status_code = 404, detail = "No note with name exists")
    
    #Update only content and date_modified    
    cur.execute('''
        UPDATE Notes
        SET Name = ?
        WHERE Name = ?
    ''', (new_name, note_name))
    conn.commit()

    #return the note the stores the row modified
    cur.execute("SELECT * FROM Notes WHERE Name = ?", (new_name,))
    modified_note = cur.fetchone()
    conn.close()

    return {"Modified Note": modified_note}
