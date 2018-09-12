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


def display_stats():
    print("Displaying stats")


def edit_note(note_id):
    _id, note, tags, date = db_get_note(note_id)
    print(f"EDITING NOTE #{_id}:")
    print(f"  (n)ote: {note}")
    print(f"  (t)ags: {tags}")
    print(f"  (d)ate: {date}")
    choice = input("Which would you like to edit ([n]/t/d)? ")
    if choice.lower().startswith("t"):
        print(f"{tags}: ")
    elif choice.lower().startswith("d"):
        print(f"{date}: ")
    else:
        print(f"{note}: ")


def list_notes(limit):
    print("Listing notes")
    db_view_notes(limit)


def main():
    params = get_params()

    # note and tags
    note = params.get("note")
    date = params.get("date")
    tags = params.get("tags")

    # edit note id
    note_id = params.get("note_id")

    # show notes and tags
    show_notes = params.get("show_notes")
    show_tags = params.get("show_tags")
    show_limit = params.get("show_limit")

    # stats
    stats_all = params.get("stats_all")
    stats_day = params.get("stats_day")
    stats_week = params.get("stats_week")
    stats_month = params.get("stats_month")
    stats_year = params.get("stats_year")

    tags = ", ".join(tags) if tags else None

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
            new_note = Note(db_next_id(), note, tags, date)
            add_note(new_note)

        if show_notes:
            list_notes(show_limit)

        if note_id:
            edit_note(note_id)


if __name__ == "__main__":
    main()
