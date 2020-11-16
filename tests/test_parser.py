# stdlib
import pathlib
from typing import Any, Dict, Iterable, List, Tuple

# 3rd party
from domdf_python_tools.paths import PathPlus
from pytest_regressions.data_regression import DataRegressionFixture

# this package
from configconfig.parser import Parser
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


class DemoParser(Parser):

	config_vars = [
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
			]

	def custom_parsing(self, raw_config_vars, parsed_config_vars, filename: PathPlus):
		# Packaging
		extras_require, additional_requirements_files = parse_extras(raw_config_vars, filename.parent)
		parsed_config_vars["extras_require"] = extras_require
		parsed_config_vars["additional_requirements_files"] = additional_requirements_files

		# Python Versions
		parsed_config_vars["min_py_version"] = min_py_version = min(parsed_config_vars["python_versions"])
		if parsed_config_vars["python_deploy_version"] < min_py_version:
			parsed_config_vars["python_deploy_version"] = min_py_version

		# Tox
		tox_py_versions = get_tox_python_versions(parsed_config_vars["python_versions"])
		parsed_config_vars["tox_py_versions"] = tox_py_versions
		tox_travis_versions = get_tox_travis_python_versions(
				parsed_config_vars["python_versions"], tox_py_versions
				)
		gh_actions_versions = get_gh_actions_python_versions(
				parsed_config_vars["python_versions"], tox_py_versions
				)

		# Travis
		tox_travis_versions[parsed_config_vars["python_deploy_version"]] += ", mypy"
		parsed_config_vars["tox_travis_versions"] = tox_travis_versions
		parsed_config_vars["gh_actions_versions"] = gh_actions_versions

		return parsed_config_vars


def parse_extras(raw_config_vars: Dict[str, Any], repo_path: pathlib.Path) -> Tuple[Dict, List[str]]:

	additional_requirements_files = raw_config_vars.get("additional_requirements_files", [])

	extras_require = raw_config_vars.get("extras_require", {})

	all_extras = []

	for extra, requires in extras_require.items():
		if isinstance(requires, str):
			if (repo_path / requires).is_file():
				# a path to the requirements file from the repo root
				extras_require[extra] = [
						x for x in (repo_path / requires).read_text(encoding="UTF-8").split('\n') if x
						]
				if requires not in additional_requirements_files:
					additional_requirements_files.append(requires)
			else:
				# A single requirement
				extras_require[extra] = [requires]

		all_extras += [x.replace(' ', '') for x in extras_require[extra]]

	all_extras = sorted(set(all_extras))

	extras_require["all"] = all_extras

	return extras_require, additional_requirements_files


def get_tox_python_versions(python_versions: Iterable[str]) -> List[str]:
	"""
	Prepares the list of Python versions to use as tox testenv names.

	:param python_versions: List of Python versions to run tests for.
	"""

	tox_py_versions = []

	for py_version in python_versions:
		py_version = str(py_version).replace('.', '')
		if not py_version.startswith("py"):
			py_version = f"py{py_version}"
		tox_py_versions.append(py_version)

	return tox_py_versions


def get_tox_travis_python_versions(
		python_versions: Iterable[str],
		tox_py_versions: Iterable[str],
		) -> Dict[str, str]:
	"""
	Prepares the mapping of Python versions to tox testenvs for use with Travis.

	:param python_versions: List of Python versions to run tests for.
	:param tox_py_versions: The list of tox testenvs for the Python versions.
	"""

	tox_travis_matrix: Dict[str, str] = {}

	for py_version, tox_py_version in zip(python_versions, tox_py_versions):
		tox_travis_matrix[str(py_version)] = f"{tox_py_version}, build"

	return tox_travis_matrix


def get_gh_actions_python_versions(
		python_versions: Iterable[str],
		tox_py_versions: Iterable[str],
		) -> Dict[str, str]:
	"""
	Prepares the mapping of Python versions to tox testenvs for use with GitHub actions.

	:param python_versions: List of Python versions to run tests for.
	:param tox_py_versions: The list of tox testenvs for the Python versions.
	"""

	tox_travis_matrix: Dict[str, str] = {}

	for py_version, tox_py_version in zip(python_versions, tox_py_versions):
		if tox_py_version != "docs":
			tox_travis_matrix[str(py_version)] = f"{tox_py_version}, build"

	return tox_travis_matrix


def test_parser(data_regression: DataRegressionFixture):
	parser = DemoParser()
	filename = PathPlus(__file__).parent / "config_file.yml"
	data_regression.check(parser.run(filename))
