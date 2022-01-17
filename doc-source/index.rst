#################
flake8-encodings
#################

.. start short_desc

.. documentation-summary::
	:meta:

.. end short_desc

.. only:: html

	.. seealso:: :pep:`597` -- Add optional EncodingWarning

.. start shields

.. only:: html

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

	.. |docs| rtfd-shield::
		:project: flake8-encodings
		:alt: Documentation Build Status

	.. |docs_check| actions-shield::
		:workflow: Docs Check
		:alt: Docs Check Status

	.. |actions_linux| actions-shield::
		:workflow: Linux
		:alt: Linux Test Status

	.. |actions_windows| actions-shield::
		:workflow: Windows
		:alt: Windows Test Status

	.. |actions_macos| actions-shield::
		:workflow: macOS
		:alt: macOS Test Status

	.. |actions_flake8| actions-shield::
		:workflow: Flake8
		:alt: Flake8 Status

	.. |actions_mypy| actions-shield::
		:workflow: mypy
		:alt: mypy status

	.. |requires| image:: https://dependency-dash.herokuapp.com/github/python-formate/flake8-encodings/badge.svg
		:target: https://dependency-dash.herokuapp.com/github/python-formate/flake8-encodings/
		:alt: Requirements Status

	.. |coveralls| coveralls-shield::
		:alt: Coverage

	.. |codefactor| codefactor-shield::
		:alt: CodeFactor Grade

	.. |pypi-version| pypi-shield::
		:project: flake8-encodings
		:version:
		:alt: PyPI - Package Version

	.. |supported-versions| pypi-shield::
		:project: flake8-encodings
		:py-versions:
		:alt: PyPI - Supported Python Versions

	.. |supported-implementations| pypi-shield::
		:project: flake8-encodings
		:implementations:
		:alt: PyPI - Supported Implementations

	.. |wheel| pypi-shield::
		:project: flake8-encodings
		:wheel:
		:alt: PyPI - Wheel

	.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/flake8-encodings?logo=anaconda
		:target: https://anaconda.org/domdfcoding/flake8-encodings
		:alt: Conda - Package Version

	.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/flake8-encodings?label=conda%7Cplatform
		:target: https://anaconda.org/domdfcoding/flake8-encodings
		:alt: Conda - Platform

	.. |license| github-shield::
		:license:
		:alt: License

	.. |language| github-shield::
		:top-language:
		:alt: GitHub top language

	.. |commits-since| github-shield::
		:commits-since: v0.5.0
		:alt: GitHub commits since tagged version

	.. |commits-latest| github-shield::
		:last-commit:
		:alt: GitHub last commit

	.. |maintained| maintained-shield:: 2022
		:alt: Maintenance

	.. |pypi-downloads| pypi-shield::
		:project: flake8-encodings
		:downloads: month
		:alt: PyPI - Downloads

.. end shields

Installation
---------------

.. start installation

.. installation:: flake8-encodings
	:pypi:
	:github:
	:anaconda:
	:conda-channels: conda-forge, domdfcoding

.. end installation

.. latex:vspace:: 20px

In version 0.5.0 and above the functionality for checking classes
(:class:`~configparser.ConfigParser` and :class:`~.pathlib.Path` for now)
requires the ``classes`` extra to be installed:

.. prompt:: bash

	python3 -m pip install flake8-encodings[classes]

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

:pep:`597` proposed adding a new ``EncodingWarning`` to Python,
which can be used in conjunction with this tool to identify issues at runtime.


Contents
-------------

.. html-section::


.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:glob:

	usage
	Source
	license

.. sidebar-links::
	:caption: Links
	:github:
	:pypi: flake8-encodings

	Contributing Guide<https://contributing-to-formate.readthedocs.io>


.. start links

.. only:: html

	View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

	:github:repo:`Browse the GitHub Repository <python-formate/flake8-encodings>`

.. end links


Footnotes
-------------

.. html-section::

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
