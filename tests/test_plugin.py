# stdlib
import ast

# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture
from domdf_python_tools.paths import PathPlus

# this package
from flake8_encodings import Plugin
from tests.example_source import example_source

try:
	# 3rd party
	import jedi  # type: ignore[import]  # noqa: F401
	has_jedi = True
except ImportError:
	has_jedi = False

skip_reason = "Output differs depending on jedi availability"


@pytest.mark.parametrize(
		"has_jedi",
		[
				pytest.param(True, id="has_jedi", marks=pytest.mark.skipif(not has_jedi, reason=skip_reason)),
				pytest.param(False, id="no_jedi", marks=pytest.mark.skipif(has_jedi, reason=skip_reason)),
				]
		)
def test_plugin(
		tmp_pathplus: PathPlus,
		advanced_data_regression: AdvancedDataRegressionFixture,
		has_jedi: bool,
		):
	(tmp_pathplus / "code.py").write_text(example_source)

	plugin = Plugin(ast.parse(example_source), filename=str(tmp_pathplus / "code.py"))
	advanced_data_regression.check(list("{}:{}: {}".format(*r) for r in plugin.run()))
