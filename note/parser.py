import argparse
from datetime import datetime
from sys import stderr


def get_params():
    """Argument parser."""
    today, time = str(datetime.today()).split(".")[0].split()
    parser = argparse.ArgumentParser(
        prog="note",
        description="Note Taking Utility"
    )
    subparsers = parser.add_subparsers(
        title='commands',
        description='valid commands',
        help='additional help available for each'
    )

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument(
        "note",
        help="The note to be entered"
    )
    add_parser.add_argument(
        "-d", "--date",
        default=today,
        help="The date in YYYY-MM-DD format"
    )
    add_parser.add_argument(
        "--time",
        default=time,
        help="The time in HH:MM:SS format"
    )
    add_parser.add_argument(
        "-t", "--tag",
        dest="tags",
        action="append",
        help="Add a category tag for the note",
        required=False
    )

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument(
        "delete_id",
        type=int,
        help="Delete the selected note"
    )

    edit_parser = subparsers.add_parser("edit")
    edit_parser.add_argument(
        "edit_id",
        type=int,
        help="Edit the selected note"
    )

    list_parser = subparsers.add_parser("show")
    list_parser.add_argument(
        "-n", "--note",
        dest="note_id",
        type=int,
        default=-1,
        help="Show a specific note by providing its id",
        required=False
    )
    list_parser.add_argument(
        "-l", "--limit",
        dest="show_limit",
        type=int,
        default=10,
        help="Limit the amount of notes returned, defaults to 10",
        required=False
    )

    stats_parser = subparsers.add_parser("stats")
    stats_parser.add_argument(
        "-a", "--all",
        dest="stats_all",
        action="store_true",
        help="Display statistics for all entries",
        required=False
    )
    stats_parser.add_argument(
        "-d", "--day",
        dest="stats_day",
        action="store_true",
        help="Display running statistics for the current day",
        required=False
    )
    stats_parser.add_argument(
        "-w", "--week",
        dest="stats_week",
        action="store_true",
        help="Display statistics for the current week",
        required=False
    )
    stats_parser.add_argument(
        "-m", "--month",
        dest="stats_month",
        action="store_true",
        help="Display statistics for the current month",
        required=False
    )
    stats_parser.add_argument(
        "-y", "--year",
        dest="stats_year",
        action="store_true",
        help="Display statistics for the current year",
        required=False
    )

    kwargs = vars(parser.parse_args())
    if not kwargs:
        parser.print_help(stderr)
        exit(1)

    return kwargs
