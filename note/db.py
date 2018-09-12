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
    tags text NOT NULL,
    date text NOT NULL
);
"""
Note = namedtuple("Note", "id note tags date")


def db_connect(db=DATABASE):
    return sqlite3.connect(db)


def check_db():
    try:
        with db_connect() as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_NOTES_TABLES_SQL)
        return True
    except Error as e:
        print(f"Could not connect to the database: {e}")
        return False


def next_id():
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM notes ORDER BY id DESC LIMIT 1")
        last = cursor.fetchone()
    return last[0] + 1 if last is not None else 1


def add_note(note):
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO notes (id, note, tags, date) VALUES "
            f"({note.id}, '{note.note}', '{note.tags}', '{note.date}');"
        )
        conn.commit()


def view_notes():
    with db_connect() as conn:
        cursor = conn.cursor()
        for row in cursor.execute('SELECT * FROM notes ORDER BY id DESC'):
            print(row)


def display_note(note):
    print(f"  ID: {note.id}")
    print(f"NOTE: {note.note}")
    print(f"TAGS: {note.tags}")
    print(f"DATE: {note.date}")


if __name__ == "__main__":
    if check_db():
        _id = next_id()
        note = Note(_id, "This is my first note", "sqlite3, python", str(datetime.today()))
        add_note(note)
        view_notes()
        print(f"NEXT RECORD: {next_id()}")
