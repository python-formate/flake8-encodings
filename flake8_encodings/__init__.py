#!/usr/bin/env python3
#
#  __init__.py
"""
A Flake8 plugin to identify incorrect use of encodings.

.. seealso:: :pep:`597` -- Add optional EncodingWarning

.. TODO::

	Add support for checking e.g. logging.basicConfig(filename="log.txt").
	It has no encoding parameter before 3.9.
	Instead an open stream must be used, with the encoding set there.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import ast
from typing import Dict, List, Optional

# 3rd party
import flake8_helper
from domdf_python_tools.utils import posargs2kwargs

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020-2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.1.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["Visitor", "Plugin", "kwargs_from_node"]

ENC001 = "ENC001 no encoding specified for 'open'."
ENC002 = "ENC002 'encoding=None' used for 'open'."
ENC003 = "ENC003 no encoding specified for 'open' with unknown mode."
ENC004 = "ENC004 'encoding=None' used for 'open' with unknown mode."


def kwargs_from_node(node: ast.Call) -> Dict[str, ast.AST]:
	"""
	Returns a mapping of argument names to the AST nodes representing their values, for the given function call.

	:param node:
	"""

	args: List[ast.expr] = node.args
	keywords: List[ast.keyword] = node.keywords

	kwargs = {kw.arg: kw.value for kw in keywords}

	return posargs2kwargs(args, open, kwargs)  # type: ignore


def mode_is_binary(mode: ast.AST) -> Optional[bool]:
	"""
	Returns whether the mode of the call to :func:`open` is binary.

	Returns :py:obj:`None` if the mode cannot be determined.

	:param mode:
	"""

	if isinstance(mode, ast.Constant):  # pragma: no cover (<py38)
		return 'b' in mode.value
	elif isinstance(mode, ast.Str):  # pragma: no cover (py38+)
		return 'b' in mode.s
	else:
		return None


class Visitor(flake8_helper.Visitor):
	"""
	AST visitor to identify incorrect use of encodings.
	"""

	def check_encoding(self, node: ast.Call):
		"""
		Check the call represented by the given AST node is using encodings correctly.
		"""
		kwargs = kwargs_from_node(node)

		# print(node.lineno, node.col_offset)
		# print(node.args, node.keywords)
		# print(kwargs_from_node(node))

		unknown_mode = False

		if "mode" in kwargs:
			is_binary = mode_is_binary(kwargs["mode"])

			if is_binary:
				return
			elif is_binary is None:
				unknown_mode = True

		if "encoding" not in kwargs:
			self.report_error(node, ENC003 if unknown_mode else ENC001)

		elif isinstance(kwargs["encoding"], (ast.Constant, ast.NameConstant)):
			if kwargs["encoding"].value is None:
				self.report_error(node, ENC004 if unknown_mode else ENC002)

	def visit_Call(self, node: ast.Call):  # noqa: D102
		if isinstance(node.func, ast.Name):

			if node.func.id == "open":
				# print(node.func.id)
				self.check_encoding(node)

		elif isinstance(node.func, ast.Attribute):
			if isinstance(node.func.value, ast.Name):

				if node.func.value.id in {"builtins", "io"} and node.func.attr == "open":
					# print(".".join((node.func.value.id, node.func.attr)))
					self.check_encoding(node)
					return

		self.generic_visit(node)


class Plugin(flake8_helper.Plugin[Visitor]):
	"""
	A Flake8 plugin to identify incorrect use of encodings.

	:param tree: The abstract syntax tree (AST) to check.
	"""

	name: str = __name__
	version: str = __version__  #: The plugin version
	visitor_class = Visitor
