# stdlib
import ast

# 3rd party
from coincidence.regressions import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from flake8_encodings import Plugin
from tests.example_source import example_source


def test_plugin(tmp_pathplus: PathPlus, advanced_data_regression: AdvancedDataRegressionFixture):
	(tmp_pathplus / "code.py").write_text(example_source)

	plugin = Plugin(ast.parse(example_source), filename=str(tmp_pathplus / "code.py"))
	advanced_data_regression.check(list("{}:{}: {}".format(*r) for r in plugin.run()))
