# stdlib
import ast

# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from flake8_encodings import ClassVisitor, Visitor
from tests.example_source import example_source

try:
	# 3rd party
	import jedi  # type: ignore
	has_jedi = True
except ImportError:
	has_jedi = False


def test_visitor(advanced_data_regression: AdvancedDataRegressionFixture):
	visitor = Visitor()
	visitor.visit(ast.parse(example_source))
	advanced_data_regression.check(visitor.errors)


def test_visitor_with_jedi(tmp_pathplus: PathPlus, advanced_data_regression: AdvancedDataRegressionFixture):
	pytest.importorskip("jedi")

	visitor = ClassVisitor()

	(tmp_pathplus / "code.py").write_text(example_source)

	visitor.first_visit(ast.parse(example_source), filename=tmp_pathplus / "code.py")
	advanced_data_regression.check(visitor.errors)


def test_visitor_with_jedi_visit_method(
		tmp_pathplus: PathPlus, advanced_data_regression: AdvancedDataRegressionFixture
		):
	pytest.importorskip("jedi")

	visitor = ClassVisitor()

	(tmp_pathplus / "code.py").write_text(example_source)

	visitor.visit(ast.parse(example_source))
	advanced_data_regression.check(visitor.errors)


def test_classvisitor_importerror():
	if has_jedi:
		pytest.skip(reason="Requires that jedi isn't installed")

	with pytest.raises(
			ImportError, match="This class requires 'jedi' to be installed but it could not be imported."
			):
		ClassVisitor()
