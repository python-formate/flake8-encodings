# stdlib
import ast
from textwrap import dedent

# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from flake8_encodings import Visitor

example_source = """

import builtins, io
import configparser

source = open("source.py")


def foo():

	result = builtins.open("source.py")
	result = io.open("source.py")
	result = open("source.py", encoding=None)


class F:

	def foo():
		result = open("source.py", encoding="utf-8")
		result = open("source.py", mode="rb")

	def read(mode: str = "r"):
		result = open("source.py", mode=mode)

class G:
	def bar():
		cfg = configparser.ConfigParser()
		cfg.read("tox.ini")

	def baz():
		from configparser import ConfigParser
		cfg = ConfigParser()
		cfg.read("tox.ini", encoding=None)
		cfg.read_dict({})
"""


def test_visitor(advanced_data_regression: AdvancedDataRegressionFixture):
	visitor = Visitor()
	visitor.visit(ast.parse(dedent(example_source)))
	advanced_data_regression.check(visitor.errors)


def test_visitor_with_jedi(tmp_pathplus: PathPlus, advanced_data_regression: AdvancedDataRegressionFixture):
	visitor = Visitor()

	(tmp_pathplus / "code.py").write_text(example_source)

	visitor.first_visit(ast.parse(dedent(example_source)), filename=tmp_pathplus / "code.py")
	advanced_data_regression.check(visitor.errors)
