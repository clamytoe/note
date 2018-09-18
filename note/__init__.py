from .db import (db_add_note, db_check, db_delete_note, db_next_id, Note,
                 db_get_note, db_update_note, db_view_notes)
from .log_init import setup_logging
from .parser import get_params

__author__ = 'Martin Uribe'
__email__ = 'clamytoe@gmail.com'
__version__ = '0.1.0'
