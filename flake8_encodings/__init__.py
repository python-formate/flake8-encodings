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
import configparser
import tempfile
from typing import Iterator, Optional, Tuple, Type

# 3rd party
import flake8_helper
import jedi  # type: ignore
from astatine import get_attribute_name, kwargs_from_node
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020-2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.2.2"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["Visitor", "Plugin"]

ENC001 = "ENC001 no encoding specified for 'open'."
ENC002 = "ENC002 'encoding=None' used for 'open'."
ENC003 = "ENC003 no encoding specified for 'open' with unknown mode."
ENC004 = "ENC004 'encoding=None' used for 'open' with unknown mode."

ENC011 = "ENC011 no encoding specified for 'configparser.ConfigParser.read'."
ENC012 = "ENC012 'encoding=None' used for 'configparser.ConfigParser.read'."

jedi.settings.fast_parser = False


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

	def __init__(self):
		super().__init__()
		self.filename = PathPlus("<unknown>")
		self.jedi_script = jedi.Script('')

	def first_visit(self, node: ast.AST, filename: PathPlus):
		"""
		Like :meth:`ast.NodeVisitor.visit`, but configures type inference.

		:param node:
		:param filename: The path to Python source file the AST node was generated from.
		"""

		self.filename = PathPlus(filename)
		self.jedi_script = jedi.Script(self.filename.read_text(), path=self.filename)
		self.visit(node)

	def check_open_encoding(self, node: ast.Call):
		"""
		Check the call represented by the given AST node is using encodings correctly.

		This function checks :func:`open`, :func:`builtins.open <open>` and :func:`io.open`.
		"""

		kwargs = kwargs_from_node(node, open)

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

	check_encoding = check_open_encoding  # deprecated

	def check_configparser_encoding(self, node: ast.Call):
		"""
		Check the call represented by the given AST node is using encodings correctly.

		This function checks :meth:`configparser.ConfigParser.read`.
		"""

		kwargs = kwargs_from_node(node, configparser.ConfigParser.read)

		if "encoding" not in kwargs:
			self.report_error(node, ENC011)

		elif isinstance(kwargs["encoding"], (ast.Constant, ast.NameConstant)):
			if kwargs["encoding"].value is None:
				self.report_error(node, ENC012)

	def visit_Call(self, node: ast.Call):  # noqa: D102

		if isinstance(node.func, ast.Name):

			if node.func.id == "open":
				# print(node.func.id)
				self.check_encoding(node)
				return

		elif isinstance(node.func, ast.Attribute):
			if isinstance(node.func.value, ast.Name):

				if node.func.value.id in {"builtins", "io"} and node.func.attr == "open":
					self.check_open_encoding(node)
					return

			if isinstance(node.func.value, ast.Str):  # pragma: no cover
				# Attribute on a string
				return self.generic_visit(node)

			elif self.filename.as_posix() == "<unknown>":
				# no jedi source (run with .visit() or from memory)
				return self.generic_visit(node)

			else:
				inferred_types = self.jedi_script.infer(node.lineno, node.func.col_offset)

				inferred_name: jedi.api.classes.Name
				for inferred_name in inferred_types:
					if (
							inferred_name.full_name == "configparser.ConfigParser"
							and tuple(get_attribute_name(node.func))[-1] == "read"
							):
						self.check_configparser_encoding(node)

					# TODO: pathlib.Path etc.

		self.generic_visit(node)


class Plugin(flake8_helper.Plugin[Visitor]):
	"""
	A Flake8 plugin to identify incorrect use of encodings.

	:param tree: The abstract syntax tree (AST) to check.
	"""

	name: str = __name__
	version: str = __version__  #: The plugin version
	visitor_class = Visitor

	def __init__(self, tree: ast.AST, filename: PathLike):
		super().__init__(tree)
		self.filename = PathPlus(filename)

	def run(self) -> Iterator[Tuple[int, int, str, Type["Plugin"]]]:  # noqa: D102

		original_cache_dir = jedi.settings.cache_directory

		with tempfile.TemporaryDirectory() as cache_directory:
			jedi.settings.cache_directory = cache_directory

			visitor = Visitor()
			visitor.first_visit(self._tree, self.filename)

			for line, col, msg in visitor.errors:
				yield line, col, msg, type(self)

		jedi.settings.cache_directory = original_cache_dir
