from .db import (DATABASE, db_add_note, db_add_tag, db_add_tagged, db_connect,
                 db_delete_note, db_delete_tag, db_get_all_tags, db_get_note,
                 db_get_tag_id, db_get_tag, db_get_tag_name, db_get_tagged_by_note,
                 db_get_tagged_by_tag, db_update_note, db_update_tag, db_view)
from .log_init import setup_logging
from .parser import get_params

__author__ = 'Martin Uribe'
__email__ = 'clamytoe@gmail.com'
__version__ = '0.1.1'
