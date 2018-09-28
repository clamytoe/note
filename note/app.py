#!/usr/bin/env python3
"""
app.py

Note taking utility
"""
import re
from collections import namedtuple
from math import ceil
from os import name, system

from note import (DATABASE, db_add_note, db_add_tag, db_add_tagged, db_connect,
                  db_delete_note, db_delete_tag, get_params, db_get_note,
                  db_get_all_tags, db_get_tag, db_get_tag_id, db_get_tag_name,
                  db_get_tagged_by_note, db_update_note, db_update_tag, db_view,
                  setup_logging)

CONN = db_connect(DATABASE)
logger = setup_logging()
PATT = re.compile(r"#\w+")
Note = namedtuple("Note", "id note date time")
Tag = namedtuple("Tag", "id tag")
Tagged = namedtuple("Tagged", "id note_id tag_id")


def add_note(note, date, time):
    clear_screen()
    tags = re.findall(PATT, note)

    try:
        note_id = db_add_note(CONN, (note, date, time))
        print(f"NOTE [{note_id}] added")
        add_tags(tags)
        CONN.commit()
    except Exception as e:
        CONN.rollback()
        print(e)
        exit(1)

    print(f"Added note: {date} {time}")
    print(f"[{note_id}] {note}")
    print(f"[{', '.join(tags)}]")


def add_tags(tags, note_id=None):
    print(tags)
    for tag in tags:
        tag_id = db_add_tag(CONN, tag)
        if note_id:
            tagged = (note_id, tag_id)
            db_add_tagged(CONN, tagged)


def clear_screen():
    """
    Clears the screen
    :return: None
    """
    _ = system('cls' if name == 'nt' else 'clear')


def delete_note(note_id):
    clear_screen()
    print(f"You are about to delete note:")
    print(db_get_note(CONN, note_id))
    answer = input("Are you sure? (y/[n]) ")
    if answer.lower().startswith("y"):
        db_delete_note(CONN, note_id)
        CONN.commit()
        print(f"Note #{note_id} was deleted.")
    else:
        print(f"Deletion of note #{note_id} aborted!")


def delete_tag(tag_id):
    clear_screen()
    print(f"You are about to delete tag:")
    print(db_get_tag_name(CONN, tag_id))
    answer = input("Are you sure? (y/[n]) ")
    if answer.lower().startswith("y"):
        db_delete_tag(CONN, tag_id)
        CONN.commit()
        print(f"Tag #{tag_id} was deleted.")
    else:
        print(f"Deletion of tag #{tag_id} aborted!")


def display_note(note, tags, truncate=True):
    tags = " ".join(tags)

    if truncate:
        desc = note.note[:46] + "..."
        result = f"{note.id:<5}{desc:<50} {note.date:<10} {note.time:<8} {tags:<}"
    else:
        wrap = ceil(len(note.note) / 50)
        result = f"{note.id:<5}{note.note[:50]:<50} {note.date:<10} {note.time:<8} {tags:<}\n"
        start = 50
        for _ in range(1, wrap):
            stop = start + 50
            result += f"{' ':<5}{note.note[start:stop]:<50}\n"
            start += 50

    print(result)


def display_stats():
    clear_screen()
    print("Displaying stats")


def edit_note(note_id):
    clear_screen()
    _id, note, date, time = db_get_note(CONN, note_id)
    all_tags = get_tags(_id)
    print(f"EDITING NOTE #{_id}:")
    print(f"  (n)ote: {note}")
    print(f"  (t)ags: {' '.join(all_tags)}")
    print(f"  (d)ate: {date}")
    print(f"  (h)our: {time}")
    choice = input("Which would you like to edit (n/t/d/h)? ")
    if choice.lower().startswith("n"):
        note = input(f"{note}: ")
    elif choice.lower().startswith("t"):
        clear_screen()
        print("Which tag would you like to modify? ")
        for i, tag in enumerate(all_tags):
            print(f"[{i:>2}] {tag}")
        asnswer = input("Note #: ")
        update_tag(all_tags[int(asnswer)])
        exit()
    elif choice.lower().startswith("d"):
        date = input(f"{date}: ")
    elif choice.lower().startswith("h"):
        time = input(f"{time}: ")
    else:
        print("Edit aborted!")
        exit()

    db_update_note(CONN, note_id, (note, date, time))
    CONN.commit()


def edit_tag(tag_id):
    clear_screen()
    tag = Tag(*db_get_tag(CONN, tag_id))

    all_tags = [t[0] for t in db_get_all_tags(CONN)]
    try:
        while True:
            new_tag = input(f"{tag.tag}: ")
            if new_tag in all_tags:
                print(f"Tag {new_tag} already exists!")
            elif not new_tag.startswith("#"):
                print("Tag names must start with a #")
            else:
                break

        db_update_tag(CONN, tag_id, new_tag)
        CONN.commit()
        print(f"{tag.tag} successfully changed to {new_tag}")
    except KeyboardInterrupt:
        print("\nAborted by user!")
        exit()


def update_tag(tag):
    tag_id = db_get_tag_id(CONN, tag)
    edit_tag(tag_id)


def get_note(db_note):
    return Note(*db_note)


def get_tags(note_id):
    _tagged = db_get_tagged_by_note(CONN, note_id)
    tagged = [Tagged(*_t) for _t in _tagged]
    return [db_get_tag_name(CONN, _tag.tag_id) for _tag in tagged]


def list_notes(note_id, limit):
    clear_screen()
    heading = f"{'ID':<5}{'NOTE':<50} {'DATE':<10} {'TIME':<8} {'TAGS':<}"
    print(heading)

    if note_id == -1:
        for _note in db_view(CONN, "notes", limit):
            note = get_note(_note)
            note_id = note.id
            tags = get_tags(note_id)
            display_note(note, tags)
    else:
        _note = db_get_note(CONN, note_id)
        note = get_note(_note)
        tags = get_tags(note.id)
        display_note(note, tags, truncate=False)


def list_tags(limit):
    clear_screen()
    print("Listing tags")
    for tag in db_view(CONN, "tags", limit):
        print(tag)


def main():
    params = get_params()
    print(params)

    # note and tags
    note = params.get("note")
    date = params.get("date")
    time = params.get("time")

    # delete note or tag
    del_note = params.get("delete_note")
    del_tag = params.get("delete_tag")

    # edit note or tag
    edit_note_id = params.get("edit_note")
    edit_tag_id = params.get("edit_tag")

    # show notes and tags
    note_id = params.get("note_id")
    show_tags = params.get("show_tags")
    show_limit = params.get("show_limit")

    # stats
    stats_all = params.get("stats_all")
    stats_day = params.get("stats_day")
    stats_week = params.get("stats_week")
    stats_month = params.get("stats_month")
    stats_year = params.get("stats_year")

    # logic
    if note:
        add_note(note, date, time)

    if del_note:
        delete_note(del_note)

    if del_tag:
        delete_tag(del_tag)

    if edit_note_id:
        edit_note(edit_note_id)

    if edit_tag_id:
        edit_tag(edit_tag_id)

    if show_tags:
        print("Showing tags!!!")
        list_tags(show_limit)
    elif note_id and not show_tags:
        list_notes(note_id, show_limit)

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


if __name__ == "__main__":
    main()
