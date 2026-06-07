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
        return False
    else:
        return True


