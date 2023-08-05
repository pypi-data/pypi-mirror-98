# Copyright (c) 2018 Kevin Murray <kdmfoss@gmail.com>
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime as dt
from signal import *
import sys
import warnings
import os
import os.path as op
from zipfile import ZipFile, ZIP_STORED
import re
import json
import pathlib
from pathlib import Path


def nowarnings(func):
    """ Decorator to always ignore warnings from a given function.

    :param func: Function to decorate
    :type func: function
    :return: Wrapped function
    :rtype: function
    """
    def wrapped(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)
    return wrapped


def find_files(base):
    """ Generator to iterate over a directory.

    :param base: Path to iterate over.
    :return: Yields paths to files in directory, or path given if path provided was to a single file.
    """
    if os.path.exists(base) and os.path.isfile(base):
        yield Path(base)
    for root, dirs, files in os.walk(base):
        for file in files:
            yield Path(root, file)


class CatchSignalThenExit(object):
    """Context manager to catch any signals, then exit. Primarily used to
    prevent early external termination of critical processes. ::

        with CatchSignalThenExit(exit=True, returncode=1):
            do_something_critical()

    In the above, if the program receives some signal (SIG{ABRT,INT,TERM,HUP}) during the
    body of the with statement, then at the close of the with statement, exit with status 1.
    """

    def __init__(self, signals=[SIGABRT, SIGINT, SIGTERM, SIGHUP], exit=True, returncode=1):
        """
        :param signals: Signals to catch
        :type signals: list of :class:`signal` signal types
        :param exit: If a signal is caught, exit script when object exits? (i.e. end of a with block)
        :type exit: bool
        :param returncode: Code to return when exiting, only used if ``exit=True``
        :type returncode: int
        """
        self.signals = signals
        self.exit = exit
        self.returncode = returncode
        self.caught = False

    def handler(self, *args):
        r""" Handles signals.

        :param \*args: Unused arguments from exceptions if provided
        """
        print("Caught signal, will terminate when finished", file=sys.stderr)
        self.caught = True

    def __enter__(self):
        for sig in self.signals:
            try:
                signal(sig, self.handler)
            except ValueError:
                pass

    def __exit__(self, *args):
        if self.exit and self.caught:
            sys.exit(self.returncode)


def XbyY2XY(xbyy):
    """Converts a string like ``10x20`` into a tuple: ``(10, 20)``

    :param xbyy: String to convert.
    :type xbyy: str
    :return: Tuple from string.
    :rtype: tuple

    >>> XbyY2XY("10x20")
    (10, 20)
    >>> XbyY2XY("1X2")
    (1, 2)
    >>> XbyY2XY((1, 2)) # Pass pre-tupleised coords through
    (1, 2)
    """
    if isinstance(xbyy, tuple) and len(xbyy) == 2:
        return xbyy
    m = re.match(r"(\d+)x(\d+)", xbyy, re.I)
    if m is None:
        raise ValueError(str(xbyy) + " doesn't appear to be in XxY format")
    return (int(m[1]), int(m[2]))


def index2rowcol(index, rows, cols, order="colsright"):
    """Converts an index to an x and y within a rows by cols grid, filed in order
    Everything is zero-based, and coordinates are from top left (a la matricies)

    :param index: Index to convert
    :type index: int
    :param rows: Rows of target grid
    :type rows: int
    :param cols: Cols of target grid
    :type cols: int
    :param order: Unimplemented. Only accepts ``colsright``, other orderings to be implemented.
    :type order: str, optional

    >>> index2rowcol(10, 5, 5) # first row, 3rd col
    (0, 2)
    >>> index2rowcol(1, 5, 5, "colsright") # 2nd row, first col
    (1, 0)
    >>> index2rowcol(25, 5, 5, "colsright") # past end of matrix
    Traceback (most recent call last):
    ...
    ValueError: index is larger than it should be given rowsXcols

    """
    if index >= rows * cols:
        raise ValueError("index is larger than it should be given rowsXcols")
    order = order.lower()
    index = int(index)
    if order == "colsright":
        return (index % rows, index // rows)
    elif order == "colsleft":
        raise NotImplementedError("colsleft not done yet")
    elif order == "rowsdown":
        raise NotImplementedError("rowsdown not done yet")
    elif order == "rowsup":
        raise NotImplementedError("rowsup not done yet")
    else:
        raise ValueError("Bad order")


class PathAwareJsonEncoder(json.JSONEncoder):
    """ Extends :class:``json.JSONEncoder`` to encode paths.
    """
    def default(self, obj):
        """ Encodes Path objects as strings to allow JSON serialisation.

        :param obj: Object to encode.
        :type obj: :class:`pathlib.Path`
        :return: JSON-serialisable version of ``obj``
        :rtype: str
        """
        if isinstance(obj, Path):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
