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

    cur.close()
    os.remove(test_db_path)


def test_duplicate_note_creation():
    #test for note called "Test Note"
    original_db_file = helper.DATABASE_FILE
    test_db_path = "testFile.db"

    helper.DATABASE_FILE = test_db_path

    conn, cur = create_temp_db(test_db_path)

    response1 = client.post("/notes", json = {
        "name": "Test Note",
        "content": "Hello World",
        "date_created": "1/1/2026 1:00PM",
        "date_modified": "1/1/2026 1:00PM"
    })

    response2 = client.post("/notes", json = {
        "name": "Test Note",
        "content": "Hello World",
        "date_created": "1/1/2026 1:00PM",
        "date_modified": "1/1/2026 1:00PM"
    })

    assert response1.status_code == 200
    assert response2.status_code == 400
    assert response2.json() == {"detail": "A note with this name already exists"}

    helper.DATABASE_FILE = original_db_file
    
    cur.close()
    os.remove(test_db_path)


def test_get_all_notes_returns_empty_list():
    original_db_file = helper.DATABASE_FILE
    test_db_path = "testFile.db"

    helper.DATABASE_FILE = test_db_path

    conn, cur = create_temp_db(test_db_path)

    empty_response = client.get("/notes")

    assert empty_response.json() == []

    helper.DATABASE_FILE = original_db_file
        
    cur.close()
    os.remove(test_db_path)


def test_get_all_notes_return():
    original_db_file = helper.DATABASE_FILE
    test_db_path = "testFile.db"

    helper.DATABASE_FILE = test_db_path

    conn, cur = create_temp_db(test_db_path)

    note1_creation = client.post("/notes", json = {
        "name": "Note One",
        "content": "Hello World",
        "date_created": "1/1/2026 1:00PM",
        "date_modified": "1/1/2026 1:00PM"
    })
    assert note1_creation.status_code == 200

    note2_creation = client.post("/notes", json = {
        "name": "Note Two",
        "content": "Hello World",
        "date_created": "1/1/2026 1:00PM",
        "date_modified": "1/1/2026 1:00PM"
    })
    assert note2_creation.status_code == 200

    returned_notes = client.get("/notes")

    note_names = []
    for note in returned_notes.json():
        note_names.append(note["note_name"])

    assert len(returned_notes.json()) == 2
    assert "Note One" in note_names
    assert "Note Two" in note_names

    helper.DATABASE_FILE = original_db_file
            
    cur.close()
    os.remove(test_db_path)


def test_get_existing_note():
    original_db_file = helper.DATABASE_FILE
    test_db_path = "testFile.db"

    helper.DATABASE_FILE = test_db_path
    conn, cur = create_temp_db(test_db_path)

    #create new note to read
    create_response = client.post("/notes", json = {
        "name": "Test Note",
        "content": "Hello World",
        "date_created": "1/1/2026 1:00PM",
        "date_modified": "1/1/2026 1:00PM"
    })

    assert create_response.status_code == 200

    get_response = client.get("/note/Test Note")

    assert get_response.status_code == 200
    assert get_response.json()["note_name"] == "Test Note"
    assert get_response.json()["content"] == "Hello World"

    helper.DATABASE_FILE = original_db_file
    cur.close()
    os.remove(test_db_path)


def test_get_existing_note_failure():
    original_db_file = helper.DATABASE_FILE
    test_db_path = "testFile.db"

    helper.DATABASE_FILE = test_db_path
    conn, cur = create_temp_db(test_db_path)

    get_response = client.get("/note/Test Note")

    assert get_response.status_code == 404

    helper.DATABASE_FILE = original_db_file
    cur.close()
    os.remove(test_db_path)


def test_rename_note_does_not_exist():
    original_db_file = helper.DATABASE_FILE
    test_db_path = "testFile.db"

    helper.DATABASE_FILE = test_db_path
    conn, cur = create_temp_db(test_db_path)

    rename_response = client.put("/note/NoteOne/rename", json = {
        "new_name": "New Note Name",
        "date_modified": "1/1/2026 1:00PM"
    })

    assert rename_response.status_code == 404
    
    helper.DATABASE_FILE = original_db_file
    cur.close()
    os.remove(test_db_path)
    
