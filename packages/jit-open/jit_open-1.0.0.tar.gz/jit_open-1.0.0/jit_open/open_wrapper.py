from bz2 import open as bz2_open
from collections import defaultdict
from gzip import open as gzip_open
from sys import stdin, stdout

_type_open = defaultdict(lambda: open, {
    'bz2': bz2_open,
    'bzip2': bz2_open,
    'gz': gzip_open,
    'gzip': gzip_open})


def open_wrapper(name, mode='r', *args, **kwargs):
    """Open wrapper for different file types.

    :arg str name: File name.
    :arg str mode: Opening mode.
    """
    if name == '-':
        if any(c in mode for c in ('a', 'w', '+')):
            return stdout
        return stdin
    return _type_open[name.split('.')[-1]](name, mode, *args, **kwargs)
