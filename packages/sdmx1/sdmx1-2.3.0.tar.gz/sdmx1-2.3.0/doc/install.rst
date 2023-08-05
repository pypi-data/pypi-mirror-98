Installation
************

Dependencies
============

:mod:`sdmx` is a pure `Python <https://python.org>`_ package requiring Python 3.7 or higher, which can be installed:

- from `the Python website <https://www.python.org/downloads/>`_, or
- using a scientific Python distribution that includes other packages useful
  for data analysis, such as
  `Anaconda <https://store.continuum.io/cshop/anaconda/>`_,
  `Canopy <https://www.enthought.com/products/canopy/>`_, or
  others listed on `the Python wiki
  <https://wiki.python.org/moin/PythonDistributions>`_.

:mod:`sdmx` also depends on:

- `pandas <http://pandas.pydata.org>`_ for data structures,
- `pydantic <https://pydantic-docs.helpmanual.io>`_ to implement the IM,

  - :mod:`sdmx` is currently not compatible with pydantic >= 1.8; see :pull:`62`.

- `requests <https://pypi.python.org/pypi/requests/>`_ for HTTP requests, and
- `lxml <http://www.lxml.de>`_ for XML processing.

Optional dependencies for extra features
----------------------------------------

- for ``cache``, allowing the caching of SDMX messages in memory, MongoDB,
  Redis, and more: `requests-cache <https://requests-cache.readthedocs.io>`_.
- for ``docs``, to build the documentation: `sphinx <https://sphinx-doc.org>`_
  and `IPython <https://ipython.org>`_.
- for ``tests``, to run the test suite: `pytest <https://pytest.org>`_, and
  `requests-mock <https://requests-mock.readthedocs.io>`_.

Instructions
============

0. (optional) If using Anaconda, use ``source activate [ENV]`` to activate the
   environment in which to install :mod:`sdmx`.
1. From the command line, issue::

    $ pip install sdmx1

   To also install optional dependencies, use commands like::

    $ pip install sdmx1[cache]             # just requests-cache
    $ pip install sdmx1[cache,docs,tests]  # all extras

From source
-----------

1. Download the latest code:

   - `from PyPI <https://pypi.org/project/sdmx1/#files>`_,
   - `from Github <https://github.com/khaeru/sdmx>`_ as a zip archive, or
   - by cloning the Github respository::

     $ git clone git@github.com:khaeru/sdmx.git

2. In the package directory, issue::

    $ pip install --editable .

   or::

    $ python setup.py install

   To also install optional dependencies, use commands like::

    $ pip install --editable .[cache]             # just requests-cache
    $ pip install --editable .[cache,docs,tests]  # all extras


.. note:: The pip ``--editable`` flag is recommended for development, so that changes to your code are reflected the next time :mod:`sdmx` is imported.

Running tests
=============

Install from source, including the ``tests`` optional dependencies.
Then, in the package directory, issue::

    $ py.test

By default, tests that involve retrieving data over the network are skipped. To
also run these tests, use::

    $ py.test --remote-data

pytest offers many command-line options to control test invocation; see ``py.test --help`` or the `documentation <https://pytest.org>`_.
