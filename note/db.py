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
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    note TEXT NOT NULL,
    date TEXT NOT NULL,
    time TEXT NOT NULL
);"""
CREATE_TAGS_TABLES_SQL = """
-- tags table
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER NOT NULL PRIMARY KEY,
    tag TEXT NOT NULL
);"""
CREATE_TAGGED_TABLES_SQL = """
-- tagged notes table
CREATE TABLE IF NOT EXISTS tagged (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    note_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY (note_id) REFERENCES notes (id),
    FOREIGN KEY (tag_id) REFERENCES tags (id)
);
"""
NewTag = namedtuple("New", "tag")


def db_action(conn, sql, respond=False, data=None):
    cursor = conn.cursor()

    if data:
        result = cursor.execute(sql, data)
    else:
        result = cursor.execute(sql)

    if respond:
        return result


def db_add_note(conn, note):
    sql = "INSERT INTO notes ('note', 'date', 'time') VALUES (?, ?, ?)"
    return db_action(conn, sql, data=note, respond=True).lastrowid


def db_add_tag(conn, tag):
    tag = tag.replace(",", "")
    tag_id = db_get_tag_id(conn, tag)
    if tag_id:
        return tag_id
    else:
        sql = "INSERT INTO tags ('tag') VALUES (?)"
        tag = NewTag(tag)
        return db_action(conn, sql, data=tag, respond=True).lastrowid


def db_add_tagged(conn, tagged):
    sql = "INSERT INTO tagged ('note_id', 'tag_id') VALUES (?, ?)"
    return db_action(conn, sql, data=tagged, respond=True)


def db_connect(db=DATABASE):
    if not path.exists(NOTES_HOME):
        makedirs(NOTES_HOME)

    conn = sqlite3.connect(db)

    if db_table_check(conn):
        return conn
    else:
        exit(1)


def db_table_check(conn):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_NOTES_TABLES_SQL)
            cursor.execute(CREATE_TAGS_TABLES_SQL)
            cursor.execute(CREATE_TAGGED_TABLES_SQL)
        conn.commit()
        return True
    except Error as e:
        print(f"Could not connect to the database: {e}")
        return False


def db_delete_note(conn, note_id):
    db_action(conn, f"DELETE FROM notes WHERE id LIKE {note_id}")
    db_action(conn, f"DELETE FROM tagged WHERE note_id LIKE {note_id}")


def db_delete_tag(conn, tag_id):
    db_action(conn, f"DELETE FROM tags WHERE id LIKE {tag_id}")
    db_action(conn, f"DELETE FROM tagged WHERE tag_id LIKE {tag_id}")


def db_get_note(conn, note_id):
    sql = f"SELECT * FROM notes WHERE id LIKE {note_id}"
    result = db_action(conn, sql, respond=True)
    return result.fetchone()


def db_get_all_tags(conn):
    return db_action(conn, f"SELECT tag FROM tags", respond=True).fetchall()


def db_get_tag(conn, tag_id):
    sql = f"SELECT * FROM tags WHERE id LIKE '{tag_id}'"
    result = db_action(conn, sql, respond=True).fetchone()
    if result:
        return result
    else:
        return None


def db_get_tag_id(conn, tag):
    sql = f"SELECT id FROM tags WHERE tag LIKE '{tag}'"
    result = db_action(conn, sql, respond=True).fetchone()
    if result:
        return result[0]
    else:
        return None


def db_get_tag_name(conn, tag_id):
    sql = f"SELECT tag FROM tags WHERE id LIKE '{tag_id}'"
    result = db_action(conn, sql, respond=True).fetchone()
    if result:
        return result[0]
    else:
        return None


def db_get_tagged_by_note(conn, note_id):
    sql = f"SELECT * FROM tagged WHERE note_id LIKE {note_id}"
    result = db_action(conn, sql, respond=True)
    return result.fetchall()


def db_get_tagged_by_tag(conn, tag_id):
    sql = f"SELECT * FROM tagged WHERE tag_id LIKE {tag_id}"
    result = db_action(conn, sql, respond=True)
    return result.fetchall()


def db_update_note(conn, note_id, note):
    sql = f"""
    UPDATE notes
    SET note = ?,
        date = ?,
        time = ?
    WHERE id LIKE {note_id}
    """
    db_action(conn, sql, data=note)


def db_update_tag(conn, tag_id, tag):
    sql = f"UPDATE tags SET tag = ? WHERE id LIKE {tag_id}"
    tag = NewTag(tag)
    db_action(conn, sql, data=tag)


def db_view(conn, table, limit=10):
    order = "DESC" if table == "notes" else ""
    sql = f"SELECT * FROM {table} ORDER BY id {order} LIMIT {limit}"
    return db_action(conn, sql, respond=True)
