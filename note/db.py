import sqlite3
from collections import namedtuple
from datetime import datetime
from os import makedirs, path
from sqlite3 import Error

HOME = path.expanduser("~")
DB_NAME = "notes.db"
NOTES_HOME = path.join(HOME, ".notes")
DATABASE = path.join(NOTES_HOME, DB_NAME)
CREATE_NOTES_TABLES_SQL = """
-- notes table
CREATE TABLE IF NOT EXISTS notes (
    id integer PRIMARY KEY,
    note text NOT NULL,
    tags text,
    date text NOT NULL,
    time text NOT NULL
);
"""
Note = namedtuple("Note", "id note tags date time")


def check_dir():
    if not path.exists(NOTES_HOME):
        makedirs(NOTES_HOME)


def db_connect(db=DATABASE):
    check_dir()
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
        tags = ", ".join(note.tags)
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO notes (id, note, tags, date, time) VALUES "
            f"({note.id}, '{note.note}', '{tags}', '{note.date}', '{note.time}');"
        )
        conn.commit()


def db_get_note(note_id):
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM notes WHERE id LIKE {note_id}')
        return cursor.fetchone()


def db_view_notes(note_id, limit):
    _id = note_id if note_id != -1 else None
    with db_connect() as conn:
        cursor = conn.cursor()
        if _id:
            sql = f"SELECT * FROM notes WHERE id LIKE {_id}"
            print(cursor.execute(sql).fetchone())
        else:
            sql = f"SELECT * FROM notes ORDER BY id DESC LIMIT {limit}"
            for i, row in enumerate(cursor.execute(sql)):
                print(row)


def db_display_note(note):
    print(f"  ID: {note.id}")
    print(f"NOTE: {note.note}")
    print(f"TAGS: {note.tags}")
    print(f"DATE: {note.date}")


if __name__ == "__main__":
    db = "test.db"
    note = "This is my first note"
    tags = "sqlite3 python".split()
    today, time = str(datetime.today()).split(".")[0].split()
    if db_check(db):
        _id = db_next_id()
        new_note = Note(_id, note, tags, today, time)
        db_add_note(new_note)
        db_view_notes()
        print(f"NEXT RECORD: {db_next_id()}")
