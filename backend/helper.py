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
    return {"note_name": single_note[0], "content": single_note[1], "date_created": single_note[2], "date_modified": single_note[3]}

#return all notes
def return_all_notes():
    conn, cur = open_db()
    cur.execute("Select * From Notes")
    all_notes = cur.fetchall()
    cur.close()
    return all_notes

#add a note to the database
def add_single_note(note_name: str, content: str, date_created: str, date_modified: str):
    conn, cur = open_db()
    cur.execute("INSERT INTO Notes (Name, Content, 'Date Created', 'Date Modified') VALUES (?, ?, ?, ?)", (note_name, content, date_created, date_modified))
    conn.commit()
    conn.close()
    return return_note(note_name)

#modify note without modifying name
def modify_note(content: str, date_modified: str, note_name: str):
    conn, cur = open_db()
    cur.execute('''
        UPDATE Notes
        SET Content = ?, "Date Modified" = ?
        WHERE Name = ?
    ''', (content, date_modified, note_name))
    conn.commit()
    cur.close()

    return return_note(note_name)


def change_note_name(new_name: str, note_name: str):
    conn, cur = open_db()
    cur.execute('''
        UPDATE Notes
        SET Name = ?
        WHERE Name = ?
    ''', (new_name, note_name))
    conn.commit()
    cur.close()
    return return_note(new_name)

def delete_note(note_name: str):
    conn, cur = open_db()
    cur.execute("DELETE FROM Notes WHERE Name = ?", (note_name,))
    conn.commit()
    cur.close()
    return return_all_notes()
