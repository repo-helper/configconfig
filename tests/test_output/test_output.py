# 3rd party
import pytest
from bs4 import BeautifulSoup
from coincidence.selectors import min_version, only_version
from sphinx.application import Sphinx
from sphinx_toolbox.testing import HTMLRegressionFixture


def test_build_example(testing_app: Sphinx):
	testing_app.build()
	testing_app.build()


@min_version("3.7")
@pytest.mark.parametrize(
		"page", [
				"autoconfig.html",
				], indirect=True
		)
def test_html_output(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	"""
	Parametrize new files here rather than as their own function.
	"""

	html_regression.check(page, jinja2=True)


@only_version("3.6")
@pytest.mark.parametrize(
		"page", [
				"autoconfig.html",
				], indirect=True
		)
def test_html_output_py36(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	"""
	Parametrize new files here rather than as their own function.
	"""

	html_regression.check(page)
