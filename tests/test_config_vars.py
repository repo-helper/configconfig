# stdlib
import os
from typing import Any, Dict, List, Type, Union

# 3rd party
import pytest

# this package
from configconfig.configvar import ConfigVar
from configconfig.testing import (
		BoolFalseTest,
		BoolTrueTest,
		DictTest,
		DirectoryTest,
		EnumTest,
		ListTest,
		OptionalStringTest,
		RequiredStringTest,
		test_list_int,
		test_list_str
		)
from tests.configuration import (
		additional_ignore,
		additional_requirements_files,
		additional_setup_args,
		author,
		conda_channels,
		conda_description,
		console_scripts,
		copyright_years,
		default_python_versions,
		docker_name,
		docker_shields,
		docs_dir,
		email,
		enable_conda,
		enable_docs,
		enable_pre_commit,
		enable_releases,
		enable_tests,
		exclude_files,
		extra_sphinx_extensions,
		extras_require,
		html_context,
		html_theme_options,
		import_name,
		intersphinx_mapping,
		keywords,
		manifest_additional,
		modname,
		pkginfo_extra,
		platforms,
		preserve_custom_theme,
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
		subclassed,
		tests_dir,
		tox_build_requirements,
		tox_requirements,
		tox_testenv_extras,
		travis_additional_requirements,
		travis_extra_install_post,
		travis_extra_install_pre,
		travis_pypi_secure,
		travis_site,
		travis_ubuntu_version,
		username
		)


class Test_author(RequiredStringTest):
	config_var = author
	test_value = "Dom"


class Test_email(RequiredStringTest):
	config_var = email
	test_value = "dominic@example.com"


class Test_username(RequiredStringTest):
	config_var = username
	test_value = "domdfcoding"


class Test_short_desc(RequiredStringTest):
	config_var = short_desc
	test_value = "This is a short description of my project."


class Test_travis_pypi_secure(OptionalStringTest):
	config_var = travis_pypi_secure
	test_value = "123abc"


class Test_tox_testenv_extras(OptionalStringTest):
	config_var = tox_testenv_extras
	test_value = "docs"


class Test_docker_name(OptionalStringTest):
	config_var = docker_name
	test_value = "manylinux2014"


class Test_rtfd_author:

	@pytest.mark.parametrize(
			"value, expects",
			[
					(
							{"rtfd_author": "Dominic Davis-Foster and Joe Bloggs"},
							"Dominic Davis-Foster and Joe Bloggs",
							),
					({"author": "Dom"}, "Dom"),
					(
							{"author": "Dom", "rtfd_author": "Dominic Davis-Foster and Joe Bloggs"},
							"Dominic Davis-Foster and Joe Bloggs",
							),
					],
			)
	def test_success(self, value: Dict[str, str], expects: str):
		assert rtfd_author.get(value) == expects

	def test_no_value(self):
		with pytest.raises(ValueError, match="A value for 'author' is required."):
			rtfd_author.get()

	@pytest.mark.parametrize(
			"wrong_value, match",
			[
					({"rtfd_author": 1234}, "'rtfd_author' must be a <class 'str'>"),
					({"rtfd_author": True}, "'rtfd_author' must be a <class 'str'>"),
					({"rtfd_author": test_list_int}, "'rtfd_author' must be a <class 'str'>"),
					({"rtfd_author": test_list_str}, "'rtfd_author' must be a <class 'str'>"),
					({"modname": "repo_helper"}, "A value for 'author' is required."),
					({}, "A value for 'author' is required."),
					],
			)
	def test_errors(self, wrong_value: Dict[str, Any], match: str):
		with pytest.raises(ValueError, match=match):
			rtfd_author.get(wrong_value)


def test_modname():
	assert modname.get({"modname": "repo_helper"}) == "repo_helper"

	with pytest.raises(ValueError, match="A value for 'modname' is required."):
		modname.get()


@pytest.mark.parametrize(
		"wrong_value, match",
		[
				({"modname": 1234}, "'modname' must be a <class 'str'>"),
				({"modname": True}, "'modname' must be a <class 'str'>"),
				({"modname": test_list_int}, "'modname' must be a <class 'str'>"),
				({"modname": test_list_str}, "'modname' must be a <class 'str'>"),
				({"username": "domdfcoding"}, "A value for 'modname' is required."),
				({}, "A value for 'modname' is required."),
				],
		)
def test_modname_errors(wrong_value: Dict[str, Any], match: str):
	with pytest.raises(ValueError, match=match):
		modname.get(wrong_value)


class Test_conda_description:

	@pytest.mark.parametrize(
			"value, expects",
			[
					(
							{"conda_description": "This is a short description of my project."},
							"This is a short description of my project.",
							),
					(
							{"short_desc": "This is a short description of my project."},
							"This is a short description of my project.",
							),
					(
							{
									"short_desc": "A short description",
									"conda_description": "This is a short description of my project.",
									},
							"This is a short description of my project.",
							),
					],
			)
	def test_success(self, value: Dict[str, str], expects: str):
		assert conda_description.get(value) == expects

	def test_no_value(self):
		with pytest.raises(ValueError, match="A value for 'short_desc' is required"):
			conda_description.get()

	@pytest.mark.parametrize(
			"wrong_value, match",
			[
					({"conda_description": 1234}, "'conda_description' must be a <class 'str'>"),
					({"conda_description": True}, "'conda_description' must be a <class 'str'>"),
					({"conda_description": test_list_int}, "'conda_description' must be a <class 'str'>"),
					({"conda_description": test_list_str}, "'conda_description' must be a <class 'str'>"),
					({"modname": "repo_helper"}, "A value for 'short_desc' is required."),
					({}, "A value for 'short_desc' is required."),
					],
			)
	def test_errors(self, wrong_value: Dict[str, Any], match: str):
		with pytest.raises(ValueError, match=match):
			conda_description.get(wrong_value)


def test_copyright_years():
	assert copyright_years.get({"copyright_years": "2014-2019"}) == "2014-2019"
	assert copyright_years.get({"copyright_years": 2020}) == "2020"

	with pytest.raises(ValueError, match="A value for 'copyright_years' is required."):
		copyright_years.get()


@pytest.mark.parametrize(
		"wrong_value, match",
		[
				(
						{"copyright_years": test_list_int},
						r"'copyright_years' must be one of \(<class 'str'>, <class 'int'>\), not <class 'list'>",
						),
				(
						{"copyright_years": test_list_str},
						r"'copyright_years' must be one of \(<class 'str'>, <class 'int'>\), not <class 'list'>",
						),
				({"username": "domdfcoding"}, "A value for 'copyright_years' is required."),
				({}, "A value for 'copyright_years' is required."),
				],
		)
def test_copyright_years_errors(wrong_value: Dict[str, Any], match: str):
	with pytest.raises(ValueError, match=match):
		copyright_years.get(wrong_value)


def test_repo_name():
	assert repo_name.get({"repo_name": "repo_helper"}) == "repo_helper"
	assert repo_name.get({"modname": "repo_helper"}) == "repo_helper"
	assert repo_name.get({"modname": "the_modname"}) == "the_modname"
	assert repo_name.get({"modname": "the_modname", "repo_name": "repo_helper"}) == "repo_helper"

	with pytest.raises(ValueError, match="A value for 'modname' is required."):
		repo_name.get()


@pytest.mark.parametrize(
		"wrong_value, match",
		[
				({"repo_name": 1234}, "'repo_name' must be a <class 'str'>"),
				({"repo_name": True}, "'repo_name' must be a <class 'str'>"),
				({"repo_name": test_list_int}, "'repo_name' must be a <class 'str'>"),
				({"repo_name": test_list_str}, "'repo_name' must be a <class 'str'>"),
				({"username": "domdfcoding"}, "A value for 'modname' is required."),
				({}, "A value for 'modname' is required."),
				],
		)
def test_repo_name_errors(wrong_value: Dict[str, Any], match: str):
	with pytest.raises(ValueError, match=match):
		repo_name.get(wrong_value)


def test_pypi_name():
	assert pypi_name.get({"pypi_name": "repo_helper"}) == "repo_helper"
	assert pypi_name.get({"modname": "repo_helper"}) == "repo_helper"
	assert pypi_name.get({"modname": "the_modname"}) == "the_modname"
	assert pypi_name.get({"modname": "the_modname", "pypi_name": "repo_helper"}) == "repo_helper"

	with pytest.raises(ValueError, match="A value for 'modname' is required."):
		pypi_name.get()


@pytest.mark.parametrize(
		"wrong_value, match",
		[
				({"pypi_name": 1234}, "'pypi_name' must be a <class 'str'>"),
				({"pypi_name": True}, "'pypi_name' must be a <class 'str'>"),
				({"pypi_name": test_list_int}, "'pypi_name' must be a <class 'str'>"),
				({"pypi_name": test_list_str}, "'pypi_name' must be a <class 'str'>"),
				({}, "A value for 'modname' is required."),
				],
		)
def test_pypi_name_errors(wrong_value: Dict[str, Any], match: str):
	with pytest.raises(ValueError, match=match):
		pypi_name.get(wrong_value)


def test_import_name():
	assert import_name.get({"import_name": "repo_helper"}) == "repo_helper"
	assert import_name.get({"modname": "repo_helper"}) == "repo_helper"
	assert import_name.get({"modname": "repo-helper"}) == "repo_helper"
	assert import_name.get({"import_name": "repo-helper"}) == "repo_helper"
	assert import_name.get({"modname": "the_modname"}) == "the_modname"
	assert import_name.get({"modname": "the_modname", "import_name": "repo_helper"}) == "repo_helper"

	with pytest.raises(ValueError, match="A value for 'modname' is required."):
		import_name.get()


@pytest.mark.parametrize(
		"wrong_value, match",
		[
				({"import_name": 1234}, "'import_name' must be a <class 'str'>"),
				({"import_name": True}, "'import_name' must be a <class 'str'>"),
				({"import_name": test_list_int}, "'import_name' must be a <class 'str'>"),
				({"import_name": test_list_str}, "'import_name' must be a <class 'str'>"),
				({}, "A value for 'modname' is required."),
				],
		)
def test_import_name_errors(wrong_value: Dict[str, Any], match: str):
	with pytest.raises(ValueError, match=match):
		import_name.get(wrong_value)


class Test_enable_tests(BoolTrueTest):
	config_var = enable_tests


class Test_enable_releases(BoolTrueTest):
	config_var = enable_releases


class Test_enable_pre_commit(BoolTrueTest):
	config_var = enable_pre_commit


class Test_enable_docs(BoolTrueTest):
	config_var = enable_docs


class Test_enable_conda(BoolTrueTest):
	config_var = enable_conda


class Test_docker_shields(BoolFalseTest):
	config_var = docker_shields


class Test_preserve_custom_theme(BoolFalseTest):
	config_var = preserve_custom_theme


class Test_source_dir(DirectoryTest):
	config_var = source_dir
	test_value = "src"
	default_value = ''

	def test_success(self):
		assert self.config_var.get({self.config_var.__name__: self.test_value}) == self.test_value + os.sep
		assert self.config_var.get({"username": "domdfcoding"}) == self.default_value
		assert self.config_var.get() == self.default_value
		assert self.config_var.get({}) == self.default_value


class Test_docs_dir(DirectoryTest):
	config_var = docs_dir
	test_value = "documentation"
	default_value = "doc-source"


class Test_tests_dir(DirectoryTest):
	config_var = tests_dir
	test_value = "test"
	default_value = "tests"


class Test_keywords(ListTest):
	config_var = keywords
	test_value = ["version control", "git", "template"]


class Test_setup_pre(ListTest):
	config_var = setup_pre
	test_value = ["import datetime"]


class Test_travis_extra_install_pre(ListTest):
	config_var = travis_extra_install_pre
	test_value = ["a string"]


class Test_travis_extra_install_post(ListTest):
	config_var = travis_extra_install_post
	test_value = ["a string"]


class Test_additional_ignore(ListTest):
	config_var = additional_ignore
	test_value = ["*.pyc"]


class Test_pkginfo_extra(ListTest):
	config_var = pkginfo_extra
	test_value = ["a string"]


class Test_exclude_files(ListTest):
	config_var = exclude_files
	test_value = ["conf", "tox"]


class Test_travis_additional_requirements(ListTest):
	config_var = travis_additional_requirements
	test_value = ["pbr"]


class Test_conda_channels(ListTest):
	config_var = conda_channels
	test_value = ["domdfcoding", "conda-forge", "bioconda"]


class Test_extra_sphinx_extensions(ListTest):
	config_var = extra_sphinx_extensions
	test_value = ["sphinxcontrib.httpdomain"]


class Test_intersphinx_mapping(ListTest):
	config_var = intersphinx_mapping
	test_value = ["'rtd': ('https://docs.readthedocs.io/en/latest/', None)"]


class Test_sphinx_conf_preamble(ListTest):
	config_var = sphinx_conf_preamble
	test_value = [
			"import datetime",
			"now = datetime.datetime.now()",
			"strftime = now.strftime('%H:%M')",
			"print(f'Starting building docs at {strftime}.')",
			]


class Test_sphinx_conf_epilogue(ListTest):
	config_var = sphinx_conf_epilogue
	test_value = [
			"time_taken = datetime.datetime.now() - now",
			"strftime = time_taken.strftime('%H:%M')",
			"print(f'Finished building docs at {strftime}.')",
			]


class Test_manifest_additional(ListTest):
	config_var = manifest_additional
	test_value = ["recursive-include: repo_helper/templates *"]


class Test_tox_requirements(ListTest):
	config_var = tox_requirements
	test_value = ["flake8"]


class Test_tox_build_requirements(ListTest):
	config_var = tox_build_requirements
	test_value = ["setuptools"]


class Test_py_modules(ListTest):
	config_var = py_modules
	test_value = ["domdf_spreadsheet_tools"]


class Test_console_scripts(ListTest):
	config_var = console_scripts
	test_value = ["repo_helper = repo_helper.__main__:main"]


class Test_additional_requirements_files(ListTest):
	config_var = additional_requirements_files
	test_value = ["submodule/requirements.txt"]


class Test_sphinx_html_theme(EnumTest):
	config_var = sphinx_html_theme
	test_value = "alabaster"
	# default_value = "sphinx_rtd_theme"
	default_value = "domdf_sphinx_theme"
	non_enum_values = ["sphinx-typo3-theme", "a string"]


class Test_travis_site(EnumTest):
	config_var = travis_site
	test_value = "org"
	default_value = "com"
	non_enum_values = ["net", "a string"]


class Test_travis_ubuntu_version(EnumTest):
	config_var = travis_ubuntu_version
	test_value = "bionic"
	default_value = "focal"
	non_enum_values = ["groovy", "wiley", "18.04", 18.04, "a string"]


class Test_platforms:
	config_var: Type[ConfigVar] = platforms
	test_value = ["Windows", "macOS", "Linux"]
	default_value = ["Windows", "macOS", "Linux"]
	non_enum_values = [
			["Windows", "macOS", "BSD"],
			["BSD"],
			["win32"],
			["posix"],
			["a string"],
			]

	def test_empty_get(self):
		assert self.config_var.get() == self.default_value
		assert self.config_var.get({}) == self.default_value

	def test_non_enum(self):
		for non_enum in self.non_enum_values:
			with pytest.raises(
					ValueError,
					match=r"Elements of 'platforms' must be one of \('Windows', 'macOS', 'Linux'\)",
					):
				self.config_var.get({self.config_var.__name__: non_enum})

	def test_success(self):
		assert self.config_var.get({"platforms": ["Windows"]}) == ["Windows"]
		assert self.config_var.get({"platforms": ["macOS"]}) == ["macOS"]
		assert self.config_var.get({"platforms": ["Linux"]}) == ["Linux"]
		assert self.config_var.get({"platforms": ["Linux", "macOS"]}) == ["Linux", "macOS"]
		assert self.config_var.get({"platforms": ["macOS", "Windows"]}) == ["macOS", "Windows"]
		assert self.config_var.get({"platforms": ["Windows", "macOS", "Linux"]}) == ["Windows", "macOS", "Linux"]

	must_be_list = r"'platforms' must be a List of typing.*\.Literal\['Windows', 'macOS', 'Linux']"

	@pytest.mark.parametrize(
			"wrong_value, match",
			[
					({config_var.__name__: "a string"}, must_be_list),
					({config_var.__name__: "Windows"}, must_be_list),
					({config_var.__name__: "windows"}, must_be_list),
					({config_var.__name__: "Linux"}, must_be_list),
					({config_var.__name__: "linux"}, must_be_list),
					({config_var.__name__: "macOS"}, must_be_list),
					({config_var.__name__: "macos"}, must_be_list),
					({config_var.__name__: 1234}, must_be_list),
					({config_var.__name__: True}, must_be_list),
					(
							{config_var.__name__: test_list_int},
							r"Elements of 'platforms' must be one of \('Windows', 'macOS', 'Linux'\)",
							),
					],
			)
	def test_errors(self, wrong_value: Dict[str, Any], match: str):
		with pytest.raises(ValueError, match=match):
			self.config_var.get(wrong_value)


class Test_python_deploy_version(OptionalStringTest):
	config_var = python_deploy_version
	test_value = "3.8"
	default_value = "3.6"

	@property
	def wrong_values(self) -> List[Dict[str, Any]]:  # noqa: D102
		return [
				{self.config_var.__name__: test_list_int},
				{self.config_var.__name__: test_list_str},
				]

	def test_success(self):
		assert self.config_var.get({self.config_var.__name__: 3.8}) == "3.8"
		assert self.config_var.get({self.config_var.__name__: "pypy3"}) == "pypy3"
		super().test_success()


class Test_python_versions(ListTest):
	config_var = python_versions
	test_value = ["3.6", "3.7", "pypy3"]
	default_value = ["3.6"]

	def test_success(self):
		assert self.config_var.get({self.config_var.__name__: ["3.6", 3.7, "pypy3"]}) == self.test_value
		assert python_versions.get({"python_deploy_version": 3.8}) == ["3.8"]
		assert python_versions.get({"python_deploy_version": "3.8"}) == ["3.8"]
		super().test_success()


class Test_additional_setup_args(DictTest):
	config_var = additional_setup_args
	test_value = {"key": "value"}

	def test_success(self):
		assert self.config_var.get({self.config_var.__name__: self.test_value}) == {"key": "value"}
		assert self.config_var.get({self.config_var.__name__: {"key": "'value'"}}) == {"key": "'value'"}
		assert self.config_var.get({self.config_var.__name__: {}}) == {}
		assert self.config_var.get({"username": "domdfcoding"}) == {}
		assert self.config_var.get() == {}
		assert self.config_var.get({}) == {}


class Test_extras_require(DictTest):
	config_var = extras_require
	test_value = {"key2": "value2"}


class Test_html_theme_options(DictTest):
	config_var = html_theme_options
	test_value = {"key3": "value3"}


class Test_html_context(DictTest):
	config_var = html_context
	test_value = {"key4": "value4"}


def test_subclassing():
	assert subclassed.dtype == List[Union[str, float]]
	assert subclassed.rtype == List[str]
	assert subclassed.default == default_python_versions
	assert subclassed.category == "python versions"
