#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ._metadata import (__author__, __license__, __name__, __summary__,
                        __version__)
from .macropragma import main
