========
Usage
========

This library provides the Flake8 plugin ``flake8-encodings``  to identify incorrect use of encodings.


Flake8 codes
--------------

**ENC00X**: checks for :func:`open`, :func:`builtins.open <open>` and :func:`io.open`.

.. flake8-codes:: flake8_encodings

	ENC001
	ENC002
	ENC003
	ENC004

``ENC003`` and ``ENC004`` are used in cases where the encoding is omitted (or is explicitly :py:obj:`None`) but the mode cannot be determined. The file might be opened in binary mode, in which case the encoding argument is ignored, or in text mode, in which case an encoding should be given.

**ENC01X**: checks for :meth:`configparser.ConfigParser.read`.

.. flake8-codes:: flake8_encodings

	ENC011
	ENC012

.. versionadded:: 0.2.1

Examples
^^^^^^^^^^

.. code-block:: python

	import configparser

	open("README.rst").read()  # ENC001 no encoding specified for 'open'.
	open("README.rst", encoding=None).read()  # ENC002 'encoding=None' used for 'open'.
	open("README.rst", mode="rb").read()  # OK
	open("README.rst", mode="rb", encoding=None).read()  # OK


	def foo(mode: str = "r"):
		open("README.rst", mode=mode).read()  # ENC003 no encoding specified for 'open' with unknown mode.
		open("README.rst", mode=mode, encoding=None).read()  # ENC004 'encoding=None' used for 'open' with unknown mode.


	def load_config(filename: str):
		cfg = configparser.ConfigParser()
		cfg.read(filename)  # ENC011
		# cfg.read(filename, encoding=None)  # ENC012


Pre-commit hook
----------------

``flake8-encodings`` can also be used as a ``pre-commit`` hook
See `pre-commit <https://github.com/pre-commit/pre-commit>`_ for instructions

Sample ``.pre-commit-config.yaml``:

.. pre-commit:flake8:: 0.2.1
