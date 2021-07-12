#!/usr/bin/env python3
#
#  validator.py
"""
Validate values obtained from the ``YAML`` file and coerce into the appropriate return types.
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
#  validate based on https://github.com/yaccob/ytools
#  Copyright (c) Jakob Stemberger <yaccob@gmx.net>
#  Apache 2.0 Licensed
#

# stdlib
import pathlib
from typing import Any, Dict, Iterable, List, Optional, Union

# 3rd party
import jsonschema  # type: ignore
from domdf_python_tools.typing import PathLike
from domdf_python_tools.utils import strtobool
from ruamel.yaml import YAML
from typing_extensions import NoReturn
from typing_inspect import get_origin, is_literal_type  # type: ignore

# this package
from configconfig.metaclass import ConfigVarMeta
from configconfig.utils import RawConfigVarsType, check_union, get_literal_values, optional_getter

__all__ = ["Validator", "validate_files"]


class Validator:
	"""
	Methods are named ``visit_<type>``.
	"""

	def __init__(self, config_var: ConfigVarMeta):
		self.config_var = config_var

	_dtypes = {
			str: "str",
			int: "int",
			float: "float",
			bool: "bool",
			}

	def validate(self, raw_config_vars: Optional[RawConfigVarsType] = None) -> Any:
		"""
		Validate the configuration value.

		:param raw_config_vars:

		:returns: The validated value.
		"""

		if raw_config_vars is None:
			raw_config_vars = {}

		if self.config_var.rtype is None:
			self.config_var.rtype = self.config_var.dtype

		if self.config_var.dtype in self._dtypes:
			return getattr(self, f"visit_{self._dtypes[self.config_var.dtype]}")(raw_config_vars)

		elif get_origin(self.config_var.dtype) in {list, List}:
			return self.visit_list(raw_config_vars)

		elif get_origin(self.config_var.dtype) in {dict, Dict}:
			return self.visit_dict(raw_config_vars)

		elif get_origin(self.config_var.dtype) is Union:
			return self.visit_union(raw_config_vars)

		elif is_literal_type(self.config_var.dtype):
			return self.visit_literal(raw_config_vars)

		else:
			self.unknown_type()

	def _visit_str_number(self, raw_config_vars: RawConfigVarsType) -> Union[str, int, float]:
		obj = optional_getter(raw_config_vars, self.config_var, self.config_var.required)

		if not isinstance(obj, self.config_var.dtype):
			raise ValueError(f"'{self.config_var.__name__}' must be a {self.config_var.dtype}") from None

		return obj

	def visit_str(self, raw_config_vars: RawConfigVarsType) -> str:
		"""
		Used to validate and convert :class:`str` values.

		:param raw_config_vars:
		"""

		return self.config_var.rtype(self._visit_str_number(raw_config_vars))

	def visit_int(self, raw_config_vars: RawConfigVarsType) -> int:
		"""
		Used to validate and convert :class:`int` values.

		:param raw_config_vars:
		"""

		return self.config_var.rtype(self._visit_str_number(raw_config_vars))

	def visit_float(self, raw_config_vars: RawConfigVarsType) -> float:
		"""
		Used to validate and convert :class:`float` values.

		:param raw_config_vars:
		"""

		return self.config_var.rtype(self._visit_str_number(raw_config_vars))

	def visit_bool(self, raw_config_vars: RawConfigVarsType) -> bool:
		"""
		Used to validate and convert :class:`bool` values.

		:param raw_config_vars:
		"""

		obj = optional_getter(raw_config_vars, self.config_var, self.config_var.required)

		if not isinstance(obj, (int, bool, str)):
			raise ValueError(
					f"'{self.config_var.__name__}' must be one of {(int, bool, str)}, "
					f"not {type(obj)}"
					) from None

		return self.config_var.rtype(strtobool(obj))

	def visit_list(self, raw_config_vars: RawConfigVarsType) -> List:
		"""
		Used to validate and convert :class:`list` values.

		:param raw_config_vars:
		"""

		# Lists of strings, numbers, Unions and Literals
		buf = []

		data = optional_getter(raw_config_vars, self.config_var, self.config_var.required)
		if isinstance(data, str) or not isinstance(data, Iterable):
			raise ValueError(
					f"'{self.config_var.__name__}' must be a List of {self.config_var.dtype.__args__[0]}"
					) from None

		if get_origin(self.config_var.dtype.__args__[0]) is Union:
			for obj in data:
				if not check_union(obj, self.config_var.dtype.__args__[0]):
					raise ValueError(
							f"'{self.config_var.__name__}' must be a "
							f"List of {self.config_var.dtype.__args__[0]}"
							) from None

		elif is_literal_type(self.config_var.dtype.__args__[0]):
			for obj in data:
				# if isinstance(obj, str):
				# 	obj = obj.lower()
				if obj not in get_literal_values(self.config_var.dtype.__args__[0]):
					raise ValueError(
							f"Elements of '{self.config_var.__name__}' must be "
							f"one of {get_literal_values(self.config_var.dtype.__args__[0])}"
							) from None
		else:
			for obj in data:
				if not check_union(obj, self.config_var.dtype):
					raise ValueError(
							f"'{self.config_var.__name__}' must be a List of {self.config_var.dtype.__args__[0]}"
							) from None

		try:
			for obj in data:
				if self.config_var.rtype.__args__[0] in {int, str, float, bool}:
					buf.append(self.config_var.rtype.__args__[0](obj))
				else:
					buf.append(obj)

			return buf

		except ValueError:
			raise ValueError(
					f"Values in '{self.config_var.__name__}' must be {self.config_var.rtype.__args__[0]}"
					) from None

	def visit_dict(self, raw_config_vars: RawConfigVarsType) -> Dict:
		"""
		Used to validate and convert :class:`dict` values.

		:param raw_config_vars:
		"""

		# Dict[str, str]
		if self.config_var.dtype == Dict[str, str]:
			obj = optional_getter(raw_config_vars, self.config_var, self.config_var.required)
			if not isinstance(obj, dict):
				raise ValueError(f"'{self.config_var.__name__}' must be a dictionary") from None

			return {str(k): str(v) for k, v in obj.items()}

		# Dict[str, Any]
		elif self.config_var.dtype == Dict[str, Any]:
			obj = optional_getter(raw_config_vars, self.config_var, self.config_var.required)
			if not isinstance(obj, dict):
				raise ValueError(f"'{self.config_var.__name__}' must be a dictionary") from None

			return obj

		# Dict[str, List[str]
		elif self.config_var.dtype == Dict[str, List[str]]:
			obj = optional_getter(raw_config_vars, self.config_var, self.config_var.required)
			if not isinstance(obj, dict):
				raise ValueError(f"'{self.config_var.__name__}' must be a dictionary") from None

			return {str(k): [str(i) for i in v] for k, v in obj.items()}

		else:
			self.unknown_type()

	def visit_union(self, raw_config_vars: RawConfigVarsType) -> Any:
		"""
		Used to validate and convert :class:`typing.Union` values.

		:param raw_config_vars:
		"""

		obj = optional_getter(raw_config_vars, self.config_var, self.config_var.required)
		if not check_union(obj, self.config_var.dtype):
			raise ValueError(
					f"'{self.config_var.__name__}' must be one of {self.config_var.dtype.__args__}, "
					f"not {type(obj)}"
					) from None

		try:
			return self.config_var.rtype(obj)
		except ValueError:
			raise ValueError(
					f"'{self.config_var.__name__}' must be {self.config_var.rtype.__args__}, "
					f"not {type(obj)}"
					) from None

	def visit_literal(self, raw_config_vars: RawConfigVarsType) -> Any:
		"""
		Used to validate and convert :class:`typing.Literal` values.

		:param raw_config_vars:
		"""

		obj = optional_getter(raw_config_vars, self.config_var, self.config_var.required)
		# if isinstance(obj, str):
		# 	obj = obj.lower()
		if obj not in get_literal_values(self.config_var.dtype):
			raise ValueError(
					f"'{self.config_var.__name__}' must be one of {get_literal_values(self.config_var.dtype)}"
					) from None

		return obj

	def unknown_type(self) -> NoReturn:
		"""
		Called when the desired type has no visitor.
		"""

		print(self.config_var)
		print(self.config_var.dtype)
		print(get_origin(self.config_var.dtype))
		raise NotImplementedError


def validate_files(
		schemafile: PathLike,
		*datafiles: PathLike,
		encoding: str = "utf-8",
		) -> None:
	r"""
	Validate the given datafiles against the given schema.

	:param schemafile: The ``json`` or ``yaml`` formatted schema to validate with.
	:param \*datafiles: The ``json`` or ``yaml`` files to validate.
	:param encoding: Encoding to open the files with.

	.. versionadded:: 0.4.0
	"""

	schemafile = pathlib.Path(schemafile)

	yaml = YAML(typ="safe", pure=True)
	schema = yaml.load(schemafile.read_text(encoding=encoding))

	for filename in datafiles:
		for document in yaml.load_all(pathlib.Path(filename).read_text(encoding=encoding)):
			try:
				jsonschema.validate(document, schema, format_checker=jsonschema.FormatChecker())
			except jsonschema.exceptions.ValidationError as e:
				e.filename = str(filename)
				raise e
