"""
setup.py

Setup for installing the package.
"""
from setuptools import setup, find_packages
from os import path
from io import open

import note

VERSION = note.__version__
AUTHOR = note.__author__
EMAIL = note.__email__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="note",
    version=VERSION,
    description="Facilitates with jotting down what you've done or learned each day. (note)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clamytoe/note",
    author=AUTHOR,
    author_email=EMAIL,
    classifiers=[
        # How mature is this project? Common values are
        #   1 - Planning
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        #   6 - Mature
        #   7 - Inactive
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="python utility note",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=["pytest>=3.7.4"],
    license="MIT",
    entry_points={
        "console_scripts": [
            "note=note.app:main"
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/clamytoe/note/issues',
        'Source': 'https://github.com/clamytoe/note/',
    },
)
