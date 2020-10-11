# 3rd party
import pytest
from bs4 import BeautifulSoup  # type: ignore
from pytest_regressions.file_regression import FileRegressionFixture
from sphinx_toolbox.testing import check_html_regression


def test_build_example(testing_app):
	testing_app.build()
	testing_app.build()


@pytest.mark.parametrize(
		"page", [
				"autoconfig.html",
				], indirect=True
		)
def test_html_output(page: BeautifulSoup, file_regression: FileRegressionFixture):
	"""
	Parametrize new files here rather than as their own function.
	"""

	check_html_regression(page, file_regression)
