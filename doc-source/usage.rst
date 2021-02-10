========
Usage
========

This library provides the Flake8 plugin ``flake8-encodings``  to identify incorrect use of encodings.


Flake8 codes
--------------

.. flake8-codes:: flake8_encodings

	ENC001
	ENC002
	ENC003
	ENC004


``ENC003`` and ``ENC004`` are used in cases where the encoding is omitted (or is explicitly :py:obj:`None`) but the mode cannot be determined. The file might be opened in binary mode, in which case the encoding argument is ignored, or in text mode, in which case an encoding should be given.

Pre-commit hook
----------------

``flake8-encodings`` can also be used as a ``pre-commit`` hook
See `pre-commit <https://github.com/pre-commit/pre-commit>`_ for instructions

Sample ``.pre-commit-config.yaml``:

.. pre-commit:flake8:: 0.0.0
