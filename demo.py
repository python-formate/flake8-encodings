open("README.rst").read()  # ENC001 no encoding specified for 'open'.
open("README.rst", encoding=None).read()  # ENC002 'encoding=None' used for 'open'.
open("README.rst", mode="rb").read()  # OK
open("README.rst", mode="rb", encoding=None).read()  # OK


def foo(mode: str = 'r'):
	open("README.rst", mode=mode).read()  # ENC003 no encoding specified for 'open' with unknown mode.
	open("README.rst", mode=mode,
			encoding=None).read()  # ENC004 'encoding=None' used for 'open' with unknown mode.


# stdlib
import logging

logging.basicConfig()
