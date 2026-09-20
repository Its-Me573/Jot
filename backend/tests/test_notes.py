import sys
sys.path.insert(0, "../")

from main import app
import helper
import sqlite3
import os

from fastapi.testclient import TestClient

client = TestClient(app)


#each endpoint test will create a temporary .db file, test and then delete that file and revert helper.database_file back to its original value.
def test_note_creation():
    original_db_file = helper.DATABASE_FILE
    test_db_path = "testFile.db"

    helper.DATABASE_FILE = "testFile.db"

    connection = sqlite3.connect(test_db_path)
    cursor = connection.cursor()

    #Initialize notes table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Notes(
    Name TEXT PRIMARY KEY NOT NULL,
    Content TEXT NOT NULL,
    "Date Created" TEXT NOT NULL,
    'Date Modified' TEXT NOT NULL)''')

    #Temp database has been created correctly from here on

    response = client.post("/notes", json = {
        "name": "Test Note",
        "content": "Hello World",
        "date_created": "1/1/2026 1:00PM",
        "date_modified": "1/1/2026 1:00PM"
    })

    assert response.status_code == 200
    assert response.json()["note_name"] == "Test Note"

    helper.DATABASE_FILE = original_db_file
    os.remove(test_db_path)