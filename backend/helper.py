from fastapi import FastAPI, HTTPException
import sqlite3

from config import DATABASE_FILE

#helper to open database
def open_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    return conn, cur

def does_note_exist(note_name: str):
    conn, cur = open_db()
    cur.execute("SELECT EXISTS(SELECT 1 FROM Notes WHERE Name = ?)", (note_name,))

    if cur.fetchone()[0] == 0:
        cur.close()
        return False
    else:
        cur.close()
        return True

#return a single note
def return_note(note_name: str):
    conn, cur = open_db()
    cur.execute("SELECT * FROM Notes WHERE Name = ?", (note_name,))
    single_note = cur.fetchone()
    cur.close()
    return single_note

#return all notes
def return_all_notes():
    conn, cur = open_db()
    cur.execute("Select * From Notes")
    all_notes = cur.fetchall()
    cur.close()
    return all_notes

