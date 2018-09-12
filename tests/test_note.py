"""
test_note.py

Tests for note.
"""
import pytest
import logging

from note import app, get_params

logging.disable(logging.CRITICAL)


@pytest.fixture
def parser():
    return get_params()


def test_main():
    with pytest.raises(SystemExit):
        app.main()
