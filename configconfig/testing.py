#!/usr/bin/env python3
#
#  testing.py
"""
Helpers for testing :class:`~configconfig.configvar.ConfigVar`.

.. extras-require:: testing
	:pyproject:

.. versionadded:: 0.2.0
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from abc import ABC
from typing import Any, Dict, List, Type

# 3rd party
import pytest  # nodep

# this package
from configconfig.configvar import ConfigVar

__all__ = [
		"ConfigVarTest",
		"NotIntTest",
		"NotBoolTest",
		"NotStrTest",
		"ListTest",
		"DirectoryTest",
		"BoolTrueTest",
		"BoolFalseTest",
		"RequiredStringTest",
		"OptionalStringTest",
		"EnumTest",
		"DictTest",
		"test_list_int",
		"test_list_str",
		]

test_list_int = [1, 2, 3, 4]
test_list_str = ['a', 'b', 'c', 'd']


class ConfigVarTest(ABC):
	r"""
	Base class for tests of :class:`~configconfig.configvar.ConfigVar`\s.
	"""

	#: The :class:`~configconfig.configvar.ConfigVar` under test.
	config_var: Type[ConfigVar]


class NotIntTest(ConfigVarTest):
	r"""
	Mixin to add tests for :class:`~configconfig.configvar.ConfigVar`\s
	that can't be integers.
	"""  # noqa: D400

	def test_error_int(self):
		"""
		Checks that the :class:`~configconfig.configvar.ConfigVar`
		raises a :class:`ValueError` when passed an :class:`int`.
		"""  # noqa: D400

		with pytest.raises(ValueError):  # noqa: PT011
			self.config_var.get({self.config_var.__name__: 1234})


class NotBoolTest(ConfigVarTest):
	r"""
	Mixin to add tests for :class:`~configconfig.configvar.ConfigVar`\s
	that can't be boolean values.
	"""  # noqa: D400

	def test_error_bool(self):
		"""
		Checks that the :class:`~configconfig.configvar.ConfigVar`
		raises a :class:`ValueError` when passed a :class:`bool`.
		"""  # noqa: D400

		with pytest.raises(ValueError):  # noqa: PT011
			self.config_var.get({self.config_var.__name__: True})


class NotStrTest(ConfigVarTest):
	r"""
	Mixin to add tests for :class:`~configconfig.configvar.ConfigVar`\s
	that can't be strings.
	"""  # noqa: D400

	def test_error_str(self):  # noqa: D102
		"""
		Checks that the :class:`~configconfig.configvar.ConfigVar`
		raises a :class:`ValueError` when passed a :class:`str`.
		"""  # noqa: D400

		with pytest.raises(ValueError):  # noqa: PT011
			self.config_var.get({self.config_var.__name__: "a string"})


class ListTest(NotStrTest, NotBoolTest, NotIntTest, ConfigVarTest):
	"""
	Test for list configuration values.
	"""

	#: A value that is valid and should be returned unchanged.
	test_value: List[str]

	#: The default value that should be returned when no valid is given.
	default_value: List[str] = []

	different_key_value: Dict[str, Any] = {"username": "domdfcoding"}
	r"""
	A dictionary containing one or more keys that are not the keys
	used by the :class:`~configconfig.configvar.ConfigVar`
	"""

	def test_success(self):  # noqa: D102
		"""
		Checks that the :class:`~configconfig.configvar.ConfigVar` can correctly parse various :class:`list` values.
		"""

		assert self.config_var.get({self.config_var.__name__: self.test_value}) == self.test_value
		assert self.config_var.get({self.config_var.__name__: []}) == []
		assert self.config_var.get(self.different_key_value) == self.default_value
		assert self.config_var.get() == self.default_value
		assert self.config_var.get({}) == self.default_value


class DirectoryTest(NotBoolTest, NotIntTest, ConfigVarTest):
	"""
	Test for configuration values which represent directories.
	"""

	#: A value that is valid and should be returned unchanged.
	test_value: str

	#: The default value that should be returned when no valid is given.
	default_value: str

	different_key_value: Dict[str, Any] = {"username": "domdfcoding"}
	r"""
	A dictionary containing one or more keys that are not the keys
	used by the :class:`~configconfig.configvar.ConfigVar`
	"""

	def test_success(self):  # noqa: D102
		"""
		Checks that the :class:`~configconfig.configvar.ConfigVar` can correctly parse various directory values.
		"""

		assert self.config_var.get({self.config_var.__name__: self.test_value}) == self.test_value
		assert self.config_var.get(self.different_key_value) == self.default_value
		assert self.config_var.get() == self.default_value
		assert self.config_var.get({}) == self.default_value

	def test_error_list_int(self):
		"""
		Checks that the :class:`~configconfig.configvar.ConfigVar`
		raises a :class:`ValueError` when passed a :class:`str`.
		"""  # noqa: D400

		with pytest.raises(ValueError, match="'.*' must be a <class 'str'>"):  # noqa: PT011
			self.config_var.get({self.config_var.__name__: test_list_int})

	def test_error_list_str(self):
		"""
		Checks that the :class:`~configconfig.configvar.ConfigVar`
		raises a :class:`ValueError` when passed a :class:`str`.
		"""  # noqa: D400

		with pytest.raises(ValueError):  # noqa: PT011
			self.config_var.get({self.config_var.__name__: test_list_str})


class BoolTrueTest(ConfigVarTest):
	"""
	Test for boolean configuration values which default to :py:obj:`True`.
	"""

	different_key_value: Dict[str, Any] = {"username": "domdfcoding"}
	r"""
	A dictionary containing one or more keys that are not the keys
	used by the :class:`~configconfig.configvar.ConfigVar`
	"""

	@property
	def true_values(self) -> List[Dict[str, Any]]:
		"""
		A list of values which should be considered :py:obj:`True`
		by the :class:`~configconfig.configvar.ConfigVar`.
		"""  # noqa: D400

		return [
				{self.config_var.__name__: True},
				{self.config_var.__name__: 1},
				{self.config_var.__name__: 200},
				{self.config_var.__name__: -1},
				{self.config_var.__name__: "True"},
				self.different_key_value,
				{},
				]

	@property
	def false_values(self) -> List[Dict[str, Any]]:
		"""
		A list of values which should be considered :py:obj:`False`
		by the :class:`~configconfig.configvar.ConfigVar`.
		"""  # noqa: D400

		return [
				{self.config_var.__name__: 0},
				{self.config_var.__name__: False},
				{self.config_var.__name__: "False"},
				]

	def test_empty_get(self):  # noqa: D102
		assert self.config_var.get()

	def test_true(self):  # noqa: D102
		for true_value in self.true_values:
			assert self.config_var.get(true_value)

	def test_false(self):  # noqa: D102
		for false_value in self.false_values:
			assert not self.config_var.get(false_value)

	@property
	def wrong_values(self) -> List[Dict[str, Any]]:
		"""
		A list of values which should are of the wrong type.
		"""

		return [
				{self.config_var.__name__: "a string"},
				{self.config_var.__name__: test_list_int},
				{self.config_var.__name__: test_list_str},
				]

	def test_errors(self):  # noqa: D102
		for wrong_value in self.wrong_values:
			with pytest.raises(ValueError):  # noqa: PT011
				self.config_var.get(wrong_value)


class BoolFalseTest(BoolTrueTest):
	"""
	Test for boolean configuration values which default to :py:obj:`False`.
	"""

	different_key_value: Dict[str, Any] = {"username": "domdfcoding"}
	r"""
	A dictionary containing one or more keys that are not the keys
	used by the :class:`~configconfig.configvar.ConfigVar`
	"""

	@property
	def true_values(self) -> List[Dict[str, Any]]:  # noqa: D102
		return [
				{self.config_var.__name__: True},
				{self.config_var.__name__: 1},
				{self.config_var.__name__: 200},
				{self.config_var.__name__: -1},
				{self.config_var.__name__: "True"},
				]

	@property
	def false_values(self) -> List[Dict[str, Any]]:  # noqa: D102
		return [
				{self.config_var.__name__: 0},
				{self.config_var.__name__: False},
				{self.config_var.__name__: "False"},
				self.different_key_value,
				{},
				]

	def test_empty_get(self):  # noqa: D102
		assert not self.config_var.get()


class RequiredStringTest(ConfigVarTest):
	"""
	Test for string configuration values which are required.
	"""

	#: A value that is valid and should be returned unchanged.
	test_value: str

	def test_empty_get(self):  # noqa: D102
		with pytest.raises(ValueError):  # noqa: PT011
			self.config_var.get()

	def test_success(self):  # noqa: D102
		assert self.config_var.get({self.config_var.__name__: self.test_value}) == self.test_value

	@property
	def wrong_values(self) -> List[Dict[str, Any]]:
		"""
		A list of values which should are of the wrong type.
		"""

		return [
				{self.config_var.__name__: 1234},
				{self.config_var.__name__: True},
				{self.config_var.__name__: test_list_int},
				{self.config_var.__name__: test_list_str},
				]

	def test_errors(self):  # noqa: D102
		for wrong_value in self.wrong_values:
			with pytest.raises(ValueError):  # noqa: PT011
				self.config_var.get(wrong_value)


class OptionalStringTest(RequiredStringTest):
	"""
	Test for string configuration values which are optional.
	"""

	#: The default value that should be returned when no valid is given.
	default_value: str = ''

	different_key_value: Dict[str, Any] = {"sphinx_html_theme": "alabaster"}
	r"""
	A dictionary containing one or more keys that are not the keys
	used by the :class:`~configconfig.configvar.ConfigVar`
	"""

	def test_empty_get(self):  # noqa: D102
		assert self.config_var.get() == self.default_value
		assert self.config_var.get({}) == self.default_value

	def test_success(self):  # noqa: D102
		assert self.config_var.get({self.config_var.__name__: ''}) == ''
		assert self.config_var.get(self.different_key_value) == self.default_value
		super().test_success()

	@property
	def wrong_values(self) -> List[Dict[str, Any]]:  # noqa: D102
		return [
				{self.config_var.__name__: 1234},
				{self.config_var.__name__: True},
				{self.config_var.__name__: test_list_int},
				{self.config_var.__name__: test_list_str},
				]

	def test_errors(self):  # noqa: D102
		for wrong_value in self.wrong_values:
			with pytest.raises(ValueError):  # noqa: PT011
				self.config_var.get(wrong_value)


class EnumTest(RequiredStringTest):
	"""
	Test for :class:`~enum.Enum` configuration values.
	"""

	#: A list of values which are of the correct type but are invalid.
	non_enum_values: List[Any]

	#: The default value that should be returned when no valid is given.
	default_value: str

	def test_empty_get(self):  # noqa: D102
		assert self.config_var.get() == self.default_value
		assert self.config_var.get({}) == self.default_value

	def test_non_enum(self):  # noqa: D102
		for non_enum in self.non_enum_values:
			with pytest.raises(ValueError):  # noqa: PT011
				self.config_var.get({self.config_var.__name__: non_enum})

	def test_errors(self):  # noqa: D102
		wrong_values: List[Dict[str, Any]] = [
				{self.config_var.__name__: 1234},
				{self.config_var.__name__: True},
				{self.config_var.__name__: test_list_int},
				{self.config_var.__name__: test_list_str},
				]
		for wrong_value in wrong_values:
			with pytest.raises(ValueError):  # noqa: PT011
				self.config_var.get(wrong_value)


class DictTest(NotStrTest, NotBoolTest, NotIntTest, ConfigVarTest):
	"""
	Test for dictionary configuration values.
	"""

	#: A value that is valid and should be returned unchanged.
	test_value: Dict[str, Any]

	#: The default value that should be returned when no valid is given.
	default_value: Dict[str, Any] = {}

	different_key_value: Dict[str, Any] = {"sphinx_html_theme": "alabaster"}
	r"""
	A dictionary containing one or more keys that are not the keys
	used by the :class:`~configconfig.configvar.ConfigVar`
	"""

	def test_success(self):  # noqa: D102
		assert self.config_var.get({self.config_var.__name__: self.test_value}) == self.test_value
		assert self.config_var.get({self.config_var.__name__: {}}) == {}
		assert self.config_var.get(self.different_key_value) == self.default_value
		assert self.config_var.get() == self.default_value
		assert self.config_var.get({}) == self.default_value

	def test_error_list_int(self):  # noqa: D102
		with pytest.raises(ValueError):  # noqa: PT011
			self.config_var.get({self.config_var.__name__: test_list_int})
