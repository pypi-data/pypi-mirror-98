#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports
import os

from setuptools import setup


# Read functions
def safe_read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""


def title_safe_read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).readline()
    except IOError:
        return ""

# Does not work
#from .macropragma._metadata import (__author__, __license__, __name__, __version__)
exec(open('macropragma/_metadata.py').read())
# Setup
setup(
    name=__name__,
    version=__version__,
    description=title_safe_read("README.md"),
    author=__author__,
    author_email="jerzy.jamroz@gmail.com",
    license=__license__,
    url="https://pypi.org/project/macropragma/",
    long_description=safe_read("README.md"),
    long_description_content_type="text/markdown",
    packages=[__name__],
    install_requires=["pyyaml>=5.0.0", "argparse>=1.1"],
    classifiers=['Programming Language :: Python :: 3',],
    python_requires='>=3.0',
    keywords='macro, pragma, macropragma, epics, database, db, substitution, template',
    # test_suite="nose.collector",
)
