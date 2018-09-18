#!/usr/bin/env python3
"""
app.py

Note taking utility
"""
from note import (db_add_note, db_check, db_connect, db_display_note, get_params,
                  db_next_id, Note, setup_logging, db_get_note, db_view_notes)

logger = setup_logging()


def add_note(note):
    db_add_note(note)
    print(f"  ID: {note.id}")
    print(f"Note: {note.note}")
    print(f"Tags: {', '.join(note.tags)}")
    print(f"Date: {note.date}")
    print(f"time: {note.time}")


def display_stats():
    print("Displaying stats")


def edit_note(note_id):
    _id, note, tags, date, time = db_get_note(note_id)
    print(f"EDITING NOTE #{_id}:")
    print(f"  (n)ote: {note}")
    print(f"  (t)ags: {tags}")
    print(f"  (d)ate: {date}")
    print(f"  (h)our: {time}")
    choice = input("Which would you like to edit ([n]/t/d/h)? ")
    if choice.lower().startswith("t"):
        print(f"{tags}: ")
    elif choice.lower().startswith("d"):
        print(f"{date}: ")
    elif choice.lower().startswith("h"):
        print(f"{time}: ")
    else:
        print(f"{note}: ")


def list_notes(note_id, limit):
    print("Listing notes")
    db_view_notes(note_id, limit)


def main():
    params = get_params()
    print(params)

    # note and tags
    note = params.get("note")
    tags = params.get("tags")
    date = params.get("date")
    time = params.get("time")

    # edit note id
    edit_id = params.get("edit_id")

    # show notes and tags
    note_id = params.get("note_id")
    show_limit = params.get("show_limit")

    # stats
    stats_all = params.get("stats_all")
    stats_day = params.get("stats_day")
    stats_week = params.get("stats_week")
    stats_month = params.get("stats_month")
    stats_year = params.get("stats_year")

    tags = tags if tags else None

    if stats_all:
        print(f"STATS ALL: {stats_all}")

    if stats_day:
        print(f"STATS ALL: {stats_day}")

    if stats_week:
        print(f"STATS ALL: {stats_week}")

    if stats_month:
        print(f"STATS ALL: {stats_month}")

    if stats_year:
        print(f"STATS ALL: {stats_year}")

    if db_check():
        if note:
            new_note = Note(db_next_id(), note, tags, date, time)
            add_note(new_note)

        if note_id:
            print(f"Showing note: {note_id}")
            list_notes(note_id, show_limit)

        if edit_id:
            edit_note(edit_id)


if __name__ == "__main__":
    main()
