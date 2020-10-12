#!/usr/bin/env python3
#
#  metaclass.py
"""
Metaclass for configuration values.
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
from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Dict, Mapping, Optional, Type, cast

# 3rd party
from typing_inspect import get_origin  # type: ignore

# this package
from configconfig.utils import get_json_type

__all__ = ["ConfigVarMeta"]

if TYPE_CHECKING:
	# this package
	from configconfig.configvar import ConfigVar


class ConfigVarMeta(type):
	"""
	Metaclass for configuration values.
	"""

	dtype: Type
	rtype: Type
	required: bool
	default: Any
	validator: Callable
	category: str

	def __new__(cls, name, bases, dct):
		x = cast("ConfigVar", super().__new__(cls, name, bases, dct))

		x.dtype = dct.get("dtype", Any)

		if "rtype" in dct:
			x.rtype = dct["rtype"]
		else:
			x.rtype = x.dtype

		x.required = dct.get("required", False)
		x.default = dct.get("default", '')
		x.validator = dct.get("validator", lambda y: y)  # type: ignore
		x.category = dct.get("category", "other")
		x.__name__ = dct.get("name", dct.get("__name__", x.__name__))  # type: ignore

		return x

	def get_schema_entry(cls, schema: Optional[Dict] = None) -> Dict[str, Any]:
		"""
		Returns the JSON schema entry for this configuration value.

		:param schema:

		:return: Dictionary representation of the JSON schema.
		"""

		if schema is None:
			schema = {
					"$schema": "http://json-schema.org/schema#",
					"type": "object",
					"properties": {},
					"required": [],
					}

		schema["properties"][cls.__name__] = get_json_type(cls.dtype)

		if cls.required:
			schema["required"].append(cls.__name__)

		return schema

	@property
	def schema_entry(cls) -> Dict[str, Any]:
		return cls.get_schema_entry()

	def __call__(cls, raw_config_vars: Dict[str, Any]) -> Any:  # type: ignore
		return cls.get(raw_config_vars)

	@abstractmethod
	def get(cls, raw_config_vars: Mapping[str, Any]):  # pragma: no cover
		return NotImplemented

	def __repr__(self) -> str:
		return f"<ConfigVar {self.__name__!r}>"
