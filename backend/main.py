"""
Main application file for the Notes API.
Handles routing, database connection, and CRUD operations.
"""

from fastapi import FastAPI
import sqlite3

from config import DATABASE_FILE

app = FastAPI()

#Initialize database connection
connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()

#Initialize notes table
cursor.execute('''CREATE TABLE IF NOT EXISTS Notes(
Name TEXT PRIMARY KEY NOT NULL,
Content TEXT NOT NULL,
"Date Created" TEXT UNIQUE NOT NULL)''')

