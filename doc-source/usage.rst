========
Usage
========

This library provides the Flake8 plugin ``flake8-encodings``  to identify incorrect use of encodings.


Flake8 codes
--------------

:bold-title:`ENC00X`: checks for :func:`open`, :func:`builtins.open <open>` and :func:`io.open`.

.. flake8-codes:: flake8_encodings

	ENC001
	ENC002
	ENC003
	ENC004

``ENC003`` and ``ENC004`` are used in cases where the encoding is omitted (or is explicitly :py:obj:`None`) but the mode cannot be determined. The file might be opened in binary mode, in which case the encoding argument is ignored, or in text mode, in which case an encoding should be given.


:bold-title:`ENC01X`: checks for :meth:`configparser.ConfigParser.read`.

.. flake8-codes:: flake8_encodings

	ENC011
	ENC012

.. versionadded:: 0.2.0
.. versionchanged:: 0.4.0  These codes now require the ``classes`` extra to be installed [1]_.


:bold-title:`ENC02X`: checks for :meth:`pathlib.Path.open`, :meth:`read_text() <pathlib.Path.read_text>` and :meth:`write_text() <pathlib.Path.write_text>`.

.. flake8-codes:: flake8_encodings

	ENC021
	ENC022
	ENC023
	ENC024
	ENC025
	ENC026

.. versionadded:: 0.3.0
.. versionchanged:: 0.4.0  These codes now require the ``classes`` extra to be installed [1]_.

.. [1] Install using ``python3 -m pip install flake8-encodings[classes]``


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

	def manipulate_file(filename):
		path = pathlib.Path(filename)

		path.write_text("Hello world")  # ENC025

		with path.open("a") as fp:  # ENC021
			f.write("\nHello everyone")

		print(path.read_text(encoding=None))  # ENC024


Pre-commit hook
----------------

``flake8-encodings`` can also be used as a ``pre-commit`` hook
See `pre-commit <https://github.com/pre-commit/pre-commit>`_ for instructions

Sample ``.pre-commit-config.yaml``:

.. pre-commit:flake8:: 0.4.0
