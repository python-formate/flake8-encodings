# stdlib
import ast

# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from flake8_encodings import Visitor
from tests.example_source import example_source


def test_visitor(advanced_data_regression: AdvancedDataRegressionFixture):
	visitor = Visitor()
	visitor.visit(ast.parse(example_source))
	advanced_data_regression.check(visitor.errors)


def test_visitor_with_jedi(tmp_pathplus: PathPlus, advanced_data_regression: AdvancedDataRegressionFixture):
	visitor = Visitor()

	(tmp_pathplus / "code.py").write_text(example_source)

	visitor.first_visit(ast.parse(example_source), filename=tmp_pathplus / "code.py")
	advanced_data_regression.check(visitor.errors)
