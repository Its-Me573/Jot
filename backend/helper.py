from fastapi import FastAPI, HTTPException
import sqlite3

from config import DATABASE_FILE

#helper to open database
def open_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    return conn, cur
