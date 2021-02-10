# stdlib
import ast
from textwrap import dedent

# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture

# this package
from flake8_encodings import Visitor


def test_visitor(advanced_data_regression: AdvancedDataRegressionFixture):
	example_source = """

	import builtins, io

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

	"""

	visitor = Visitor()
	visitor.visit(ast.parse(dedent(example_source)))
	advanced_data_regression.check(visitor.errors)
