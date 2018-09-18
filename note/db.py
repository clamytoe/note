import sqlite3
from collections import namedtuple
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


def db_action(sql, respond=False, data=None):
    with db_connect() as conn:
        cursor = conn.cursor()
        if data:
            result = cursor.execute(sql, data)
        else:
            result = cursor.execute(sql)
        conn.commit()
    if respond:
        return result


def db_add_note(note):
    tags = ", ".join(note.tags)
    sql = f"""
    INSERT INTO notes
    VALUES (
        {note.id}, 
        '{note.note}', 
        '{tags}', 
        '{note.date}', 
        '{note.time}'
    );"""
    db_action(sql)


def db_connect(db=DATABASE):
    check_dir()
    return sqlite3.connect(db)


def db_check():
    try:
        db_action(CREATE_NOTES_TABLES_SQL)
        return True
    except Error as e:
        print(f"Could not connect to the database: {e}")
        return False


def db_delete_note(note_id):
    db_action(f"DELETE FROM notes WHERE id LIKE {note_id}")


def db_get_note(note_id):
    sql = f"SELECT * FROM notes WHERE id LIKE {note_id}"
    result = db_action(sql, respond=True)
    return result.fetchone()


def db_next_id():
    sql = "SELECT id FROM notes ORDER BY id DESC LIMIT 1"
    result = db_action(sql, respond=True)
    last = result.fetchone()
    return last[0] + 1 if last is not None else 1


def db_update_note(note):
    sql = f"""
    UPDATE notes
    SET id = ?,
        note = ?,
        tags = ?,
        date = ?,
        time = ?
    WHERE id LIKE {note.id}
    """
    db_action(sql, data=note)


def db_view_notes(limit):
    sql = f"SELECT * FROM notes ORDER BY id DESC LIMIT {limit}"
    return db_action(sql, respond=True)
