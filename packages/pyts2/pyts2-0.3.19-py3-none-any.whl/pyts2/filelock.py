# Copyright (c) 2009, Evan Fosmark
# Copyright (c) 2018-2020 Kevin Murray
# This is the filelock module off pypi or https://github.com/dmfrey/FileLock
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import time
import errno
import random

DEFAULT_TIMEOUT = int(os.environ.get("TSTK_TIMEOUT", 10))


class FileLockException(Exception):
    """Exception for file locking. Raised when unable to acquire file lock, via :func:`~FileLock.acquire`."""
    pass


class FileLock(object):
    """
    A file locking mechanism that has context-manager support so
    you can use it in a with statement. This should be relatively cross
    compatible as it doesn't rely on msvcrt or fcntl for the locking.
    Can be used either through :func:`~acquire` or ``with FileLock():``.
    """

    def __init__(self, file_name, timeout=DEFAULT_TIMEOUT, delay=.05):
        """
        :param file_name: Path of file to lock.
        :type file_name: str
        :param timeout: Seconds to wait for locking process to complete. Defaults to ``TSTK_TIMEOUT`` environment variable, if set. 
        :type timeout: numeric, optional
        :param delay: Seconds to wait between checking for file availability. Defaults to 0.5 seconds.
        :type delay: numeric, optional
        """
        if timeout is not None and delay is None:
            raise ValueError("If timeout is not None, then delay must not be None.")
        self.is_locked = False
        self.lockfile = "%s.lock" % file_name
        self.file_name = file_name
        self.timeout = timeout
        self.delay = delay

    def acquire(self):
        """ Acquire the lock, if possible. If the lock is in use, it check again
            every ``delay`` seconds. It does this until it either gets the lock or
            exceeds ``timeout`` number of seconds, in which case it throws
            an exception.

            :raises FileLockException: Unable to acquire lock.
        """
        time.sleep(random.randrange(1, 10) / 1000)  # 1-10 millisec delay
        start_time = time.time()
        while True:
            try:
                self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                self.is_locked = True  # moved to ensure tag only when locked
                break
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                if self.timeout is None:
                    raise FileLockException(f"Could not acquire lock on {self.file_name}")
                if (time.time() - start_time) >= self.timeout:
                    raise FileLockException(f"Timeout occured after {self.timeout} seconds on {self.file_name}.")
                time.sleep(self.delay)

    def release(self):
        """ Get rid of the lock by deleting the lockfile.
            When working in a ``with`` statement, this gets automatically
            called at the end.
        """
        if self.is_locked:
            os.close(self.fd)
            os.unlink(self.lockfile)
            self.is_locked = False

    def __enter__(self):
        """ Activated when used in the with statement.
            Should automatically acquire a lock to be used in the with block.

            :return: Returns :class:`.FileLock` object for use within the with block.
        """
        if not self.is_locked:
            self.acquire()
        return self

    def __exit__(self, type, value, traceback):
        """ Activated at the end of the with statement.
            It automatically releases the lock if it isn't locked.
        """
        if self.is_locked:
            self.release()

    def __del__(self):
        """ Make sure that the FileLock instance doesn't leave a lockfile
            lying around.
        """
        self.release()
