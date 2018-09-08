"""
test_note.py

Tests for note.
"""
import logging

from note import app

logging.disable(logging.CRITICAL)


def test_main(capfd):
    app.main()
    output = capfd.readouterr()[0]
    assert output.strip() == "Successfully installed your project file: note"
