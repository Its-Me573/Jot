import sys
sys.path.insert(0, "../")

from main import app
import helper
import sqlite3
import os

from fastapi.testclient import TestClient

client = TestClient(app)


def create_temp_db(database_path):
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS Notes(
        Name TEXT PRIMARY KEY NOT NULL,
        Content TEXT NOT NULL,
        "Date Created" TEXT NOT NULL,
        'Date Modified' TEXT NOT NULL)''')

    return conn, cur

def test_note_creation():
    original_db_file = helper.DATABASE_FILE
    test_db_path = "testFile.db"

    helper.DATABASE_FILE = test_db_path

    conn, cur = create_temp_db(test_db_path)

    response = client.post("/notes", json = {
            "name": "Test Note",
            "content": "Hello World",
            "date_created": "1/1/2026 1:00PM",
            "date_modified": "1/1/2026 1:00PM"
    })

    assert response.status_code == 200
    assert response.json()["note_name"] == "Test Note"

    helper.DATABASE_FILE = original_db_file

    cur.close
    os.remove(test_db_path)