#!/usr/bin/env python3
#
#  __init__.py
"""
A Flake8 plugin to identify incorrect use of encodings.

.. seealso:: :pep:`597` -- Add optional EncodingWarning
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
from typing import Dict, Iterator, List, Tuple, Type

# 3rd party
from domdf_python_tools.utils import posargs2kwargs

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020-2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["Visitor", "Plugin", "kwargs_from_node"]

ENC001 = "ENC001 no encoding specified for 'open'."
ENC002 = "ENC002 'encoding=None' used for 'open'."
ENC003 = "ENC003 no encoding specified for 'open' with unknown mode."
ENC004 = "ENC004 'encoding=None' used for 'open' with unknown mode."


def kwargs_from_node(node: ast.Call) -> Dict[str, ast.AST]:
	args: List[ast.AST] = node.args
	keywords: List[ast.keyword] = node.keywords

	kwargs = {kw.arg: kw.value for kw in keywords}

	return posargs2kwargs(args, open, kwargs)


class Visitor(ast.NodeVisitor):
	"""
	AST visitor to identify incorrect use of encodings.
	"""

	def __init__(self) -> None:
		#: The list of Flake8 errors identified by the visitor.
		self.errors: List[Tuple[int, int, str]] = []

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
			print(kwargs["mode"])
			if isinstance(kwargs["mode"],
							ast.Constant) and 'b' in kwargs["mode"].value:  # pragma: no cover (<py38)
				return
			elif isinstance(kwargs["mode"], ast.Str) and 'b' in kwargs["mode"].s:  # pragma: no cover (py38+)
				return
			else:
				unknown_mode = True

		if "encoding" not in kwargs:
			self.errors.append((
					node.lineno,
					node.col_offset,
					ENC003 if unknown_mode else ENC001,
					))

		elif isinstance(kwargs["encoding"], (ast.Constant, ast.NameConstant)):
			if kwargs["encoding"].value is None:
				self.errors.append((
						node.lineno,
						node.col_offset,
						ENC004 if unknown_mode else ENC002,
						))

	def visit_Call(self, node: ast.Call):
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


class Plugin:
	"""
	A Flake8 plugin to identify incorrect use of encodings.

	:param tree: The abstract syntax tree (AST) to check.
	"""

	name: str = __name__
	version: str = __version__  #: The plugin version

	def __init__(self, tree: ast.AST):
		self._tree = tree

	def run(self) -> Iterator[Tuple[int, int, str, Type["Plugin"]]]:
		"""
		Traverse the Abstract Syntax Tree and check calls to :func:`open`.

		Yields a tuple of (line number, column offset, error message, type(self))
		"""

		visitor = Visitor()
		visitor.visit(self._tree)

		for line, col, msg in visitor.errors:
			yield line, col, msg, type(self)
