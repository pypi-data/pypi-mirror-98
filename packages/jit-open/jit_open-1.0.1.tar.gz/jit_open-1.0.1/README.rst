Just in time open files.
========================

This package provides a way to delay opening files until the something is
written to the file handle. This can be convenient when opening a large number
of files of which most of them will not be frequently used. To deal with
resource limits a queue is used from which, when full, the least frequent file
is closed.


Installation
------------

The software is distributed via PyPI_, it can be installed with ``pip``:

::

   pip install jit_open

From source
~~~~~~~~~~~

The source is hosted on GitHub_, to install the latest development version, use
the following commands.

::

   git clone https://git.lumc.nl/j.f.j.laros/jit-open
   cd jit_open
   pip install .


Usage
-----

In the following example, only the file ``used.txt`` is created.

.. code:: python

   >>> from jit_open import Handle, Queue
   >>>
   >>> queue = Queue()
   >>> used = Handle("used.txt", queue)
   >>> unused = Handle("unused.txt", queue)
   >>>
   >>> used.write("line 1\n")
   >>> used.write("line 2\n")


Library
-------

The library provides the ``Handle`` and ``Queue`` classes.


.. _PyPI: https://pypi.python.org/pypi/jit-open
.. _GitHub: https://github.com/jfjlaros/jit-open.git
