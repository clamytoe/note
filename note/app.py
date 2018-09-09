#!/usr/bin/env python3
"""
app.py

Note taking utility
"""
from .log_init import setup_logging
from .parser import get_params

logger = setup_logging()


def list_notes():
    print("Listing notes")


def display_stats():
    print("Displaying stats")


def main():
    params = get_params()

    # note and tags
    note = params.get("note")
    tags = params.get("tags")

    # edit note id
    note_id = params.get("note_id")

    # show notes and tags
    show_notes = params.get("show_notes")
    show_tags = params.get("show_tags")

    # stats
    stats_all = params.get("stats_all")
    stats_day = params.get("stats_day")
    stats_week = params.get("stats_week")
    stats_month = params.get("stats_month")
    stats_year = params.get("stats_year")

    if note:
        print(f"NOTE: {note}")

    if tags:
        print(f"TAGS: {tags}")

    if note_id:
        print(f"EDIT: {note_id}")

    if show_notes:
        print(f"SHOW NOTES: {show_notes}")

    if show_tags:
        print(f"SHOW TAGS: {show_tags}")

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
