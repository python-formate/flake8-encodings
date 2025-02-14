#################
flake8-encodings
#################

.. start short_desc

**A Flake8 plugin to identify incorrect use of encodings.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/flake8-encodings/latest?logo=read-the-docs
	:target: https://flake8-encodings.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/python-formate/flake8-encodings/workflows/Docs%20Check/badge.svg
	:target: https://github.com/python-formate/flake8-encodings/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/python-formate/flake8-encodings/workflows/Linux/badge.svg
	:target: https://github.com/python-formate/flake8-encodings/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/python-formate/flake8-encodings/workflows/Windows/badge.svg
	:target: https://github.com/python-formate/flake8-encodings/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/python-formate/flake8-encodings/workflows/macOS/badge.svg
	:target: https://github.com/python-formate/flake8-encodings/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/python-formate/flake8-encodings/workflows/Flake8/badge.svg
	:target: https://github.com/python-formate/flake8-encodings/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/python-formate/flake8-encodings/workflows/mypy/badge.svg
	:target: https://github.com/python-formate/flake8-encodings/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/python-formate/flake8-encodings/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/python-formate/flake8-encodings/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/python-formate/flake8-encodings/master?logo=coveralls
	:target: https://coveralls.io/github/python-formate/flake8-encodings?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/python-formate/flake8-encodings?logo=codefactor
	:target: https://www.codefactor.io/repository/github/python-formate/flake8-encodings
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/flake8-encodings
	:target: https://pypi.org/project/flake8-encodings/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/flake8-encodings?logo=python&logoColor=white
	:target: https://pypi.org/project/flake8-encodings/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/flake8-encodings
	:target: https://pypi.org/project/flake8-encodings/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/flake8-encodings
	:target: https://pypi.org/project/flake8-encodings/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/flake8-encodings?logo=anaconda
	:target: https://anaconda.org/domdfcoding/flake8-encodings
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/flake8-encodings?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/flake8-encodings
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/python-formate/flake8-encodings
	:target: https://github.com/python-formate/flake8-encodings/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/python-formate/flake8-encodings
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-formate/flake8-encodings/v0.5.1
	:target: https://github.com/python-formate/flake8-encodings/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/python-formate/flake8-encodings
	:target: https://github.com/python-formate/flake8-encodings/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2025
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/flake8-encodings
	:target: https://pypi.org/project/flake8-encodings/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``flake8-encodings`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install flake8-encodings

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels https://conda.anaconda.org/conda-forge
		$ conda config --add channels https://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install flake8-encodings

.. end installation


In version 0.5.1 and above the functionality for checking classes
(``configparser.ConfigParser`` and ``pathlib.Path`` for now)
requires the ``classes`` extra to be installed:

.. code-block:: bash

	$ python3 -m pip install flake8-encodings[classes]

The checks for classes are slower and CPU intensive,
so only enable them if you use the classes in question.



Motivation
-------------

Developers using macOS or Linux may forget that the default encoding
is not always UTF-8.

For example, ``long_description = open("README.md").read()`` in
``setup.py`` is a common mistake. Many Windows users cannot install
the package if there is at least one non-ASCII character (e.g. emoji)
in the ``README.md`` file which is encoded in UTF-8.

For example, 489 packages of the 4000 most downloaded packages from
PyPI used non-ASCII characters in README. And 82 packages of them
cannot be installed from source package when the locale encoding is
ASCII. [1]_ They used the default encoding to read README or TOML
file.

Even Python experts assume that default encoding is UTF-8.
It creates bugs that happen only on Windows. See [2]_, [3]_, [4]_,
and [5]_ for example.

`PEP 597 <https://www.python.org/dev/peps/pep-0597>`_ proposed adding a new ``EncodingWarning`` to Python,
which can be used in conjunction with this tool to identify issues at runtime.


.. [1] "Packages can't be installed when encoding is not UTF-8"
       (https://github.com/methane/pep597-pypi-ascii)

.. [2] Packaging tutorial in packaging.python.org didn't specify
       encoding to read a ``README.md``
       (https://github.com/pypa/packaging.python.org/pull/682)

.. [3] ``json.tool`` had used locale encoding to read JSON files.
       (https://bugs.python.org/issue33684)

.. [4] site: Potential UnicodeDecodeError when handling pth file
       (https://bugs.python.org/issue33684)

.. [5] pypa/pip: "Installing packages fails if Python 3 installed
       into path with non-ASCII characters"
       (https://github.com/pypa/pip/issues/9054)
