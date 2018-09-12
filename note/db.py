import sqlite3
from collections import namedtuple
from datetime import datetime
from sqlite3 import Error

DATABASE = "notes.db"
CREATE_NOTES_TABLES_SQL = """
-- notes table
CREATE TABLE IF NOT EXISTS notes (
    id integer PRIMARY KEY,
    note text NOT NULL,
    tags text,
    date text NOT NULL
);
"""
Note = namedtuple("Note", "id note tags date")


def db_connect(db=DATABASE):
    return sqlite3.connect(db)


def db_check():
    try:
        with db_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_NOTES_TABLES_SQL)
        return True
    except Error as e:
        print(f"Could not connect to the database: {e}")
        return False


def db_next_id():
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM notes ORDER BY id DESC LIMIT 1")
        last = cursor.fetchone()
    return last[0] + 1 if last is not None else 1


def db_add_note(note):
    with db_connect() as conn:
        print(f"RECEIVED TAGS: {note.tags} TYPE: {type(note.tags)}")
        tags = ", ".join(note.tags)
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO notes (id, note, tags, date) VALUES "
            f"({note.id}, '{note.note}', '{tags}', '{note.date}');"
        )
        conn.commit()


def db_get_note(note_id):
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM notes WHERE id = {note_id}')
        return cursor.fetchone()


def db_view_notes(limit):
    with db_connect() as conn:
        cursor = conn.cursor()
        for i, row in enumerate(cursor.execute('SELECT * FROM notes ORDER BY id DESC')):
            if i < limit:
                print(row)


def db_display_note(note):
    print(f"  ID: {note.id}")
    print(f"NOTE: {note.note}")
    print(f"TAGS: {note.tags}")
    print(f"DATE: {note.date}")


if __name__ == "__main__":
    if db_check():
        _id = db_next_id()
        note = Note(_id, "This is my first note", "sqlite3, python", str(datetime.today()))
        db_add_note(note)
        db_view_notes()
        print(f"NEXT RECORD: {db_next_id()}")
