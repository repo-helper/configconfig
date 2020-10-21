# 3rd party
import pytest
from pytest_regressions.data_regression import DataRegressionFixture

# this package
from configconfig.metaclass import ConfigVarMeta
from configconfig.utils import make_schema
from tests.configuration import (
		additional_setup_args,
		author,
		console_scripts,
		copyright_years,
		docker_name,
		docker_shields,
		docs_dir,
		email,
		enable_docs,
		enable_pre_commit,
		enable_releases,
		enable_tests,
		extra_sphinx_extensions,
		extras_require,
		html_context,
		html_theme_options,
		imgbot_ignore,
		import_name,
		intersphinx_mapping,
		keywords,
		manifest_additional,
		modname,
		mypy_deps,
		mypy_plugins,
		on_pypi,
		platforms,
		preserve_custom_theme,
		pure_python,
		py_modules,
		pypi_name,
		python_deploy_version,
		python_versions,
		repo_name,
		rtfd_author,
		setup_pre,
		short_desc,
		source_dir,
		sphinx_conf_epilogue,
		sphinx_conf_preamble,
		sphinx_html_theme,
		stubs_package,
		tox_build_requirements,
		tox_requirements,
		tox_testenv_extras,
		username
		)


@pytest.mark.parametrize(
		"configvar",
		[
				python_versions,
				manifest_additional,
				extras_require,
				platforms,
				rtfd_author,
				preserve_custom_theme,
				sphinx_html_theme,
				]
		)
def test_get_schema_entry(configvar: ConfigVarMeta, data_regression: DataRegressionFixture):
	data_regression.check(configvar.schema_entry)
	data_regression.check(configvar.get_schema_entry())


def test_make_schema(data_regression: DataRegressionFixture):
	data_regression.check(
			make_schema(
					author,
					email,
					username,
					modname,
					copyright_years,
					repo_name,
					pypi_name,
					import_name,
					keywords,
					short_desc,
					source_dir,
					pure_python,
					stubs_package,
					on_pypi,
					enable_tests,
					enable_releases,
					enable_pre_commit,
					docker_shields,
					docker_name,
					manifest_additional,
					py_modules,
					console_scripts,
					setup_pre,
					additional_setup_args,
					platforms,
					rtfd_author,
					preserve_custom_theme,
					sphinx_html_theme,
					extra_sphinx_extensions,
					intersphinx_mapping,
					sphinx_conf_preamble,
					sphinx_conf_epilogue,
					html_theme_options,
					html_context,
					enable_docs,
					docs_dir,
					imgbot_ignore,
					mypy_deps,
					mypy_plugins,
					python_deploy_version,
					python_versions,
					tox_requirements,
					tox_build_requirements,
					tox_testenv_extras,
					)
			)
