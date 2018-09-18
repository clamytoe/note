#!/usr/bin/env python3
"""
app.py

Note taking utility
"""
from note import (db_add_note, db_check, db_delete_note, get_params, db_next_id,
                  Note, setup_logging, db_get_note, db_update_note, db_view_notes)

logger = setup_logging()


def add_note(note):
    db_add_note(note)
    print(f"Added note: {note.date} {note.time}")
    print(f"[{note.id}] {note.note}")
    print(f"[{', '.join(note.tags)}]")


def delete_note(delete_id):
    print(f"You are about to delete note:")
    print(db_get_note(delete_id))
    answer = input("Are you sure? (y/[n]) ")
    if answer.lower().startswith("y"):
        db_delete_note(delete_id)
        print(f"Note #{delete_id} was deleted.")
    else:
        print(f"Deletion of note #{delete_id} aborted!")


def display_stats():
    print("Displaying stats")


def edit_note(note_id):
    _id, note, tags, date, time = db_get_note(note_id)
    print(f"EDITING NOTE #{_id}:")
    print(f"  (n)ote: {note}")
    print(f"  (t)ags: {tags}")
    print(f"  (d)ate: {date}")
    print(f"  (h)our: {time}")
    choice = input("Which would you like to edit (n/t/d/h)? ")
    if choice.lower().startswith("n"):
        note = input(f"{note}: ")
    elif choice.lower().startswith("t"):
        tags = input(f"{tags}: ")
    elif choice.lower().startswith("d"):
        date = input(f"{date}: ")
    elif choice.lower().startswith("h"):
        time = input(f"{time}: ")
    else:
        print("Edit aborted!")
        exit()

    db_update_note(Note(_id, note, tags, date, time))


def list_notes(note_id, limit):
    print("Listing notes")
    if note_id == -1:
        for note in db_view_notes(limit):
            print(note)
    else:
        print(db_get_note(note_id))


def main():
    params = get_params()
    print(params)

    # note and tags
    note = params.get("note")
    tags = params.get("tags")
    date = params.get("date")
    time = params.get("time")

    # delete note id
    delete_id = params.get("delete_id")

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

        if delete_id:
            delete_note(delete_id)

        if edit_id:
            edit_note(edit_id)

        if note_id:
            list_notes(note_id, show_limit)


if __name__ == "__main__":
    main()
