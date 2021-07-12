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

# this package
from configconfig.utils import basic_schema, get_json_type

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
	__name__: str

	def __new__(cls, name: str, bases, dct: Dict):  # noqa: D102
		x = cast("ConfigVar", super().__new__(cls, name, bases, dct))

		def get(name, default):
			return dct.get(name, getattr(x, name, default))

		x.dtype = get("dtype", Any)

		if "rtype" in dct:
			x.rtype = dct["rtype"]
		elif getattr(x, "rtype", Any) != Any:
			pass
		else:
			x.rtype = x.dtype

		x.required = get("required", False)
		x.default = get("default", '')
		x.validator = get("validator", lambda y: y)  # type: ignore
		x.category = get("category", "other")
		x.__name__ = dct.get("name", dct.get("__name__", x.__name__))

		return x

	def get_schema_entry(cls, schema: Optional[Dict] = None) -> Dict[str, Any]:
		"""
		Returns the JSON schema entry for this configuration value.

		:param schema:

		:return: Dictionary representation of the JSON schema.
		"""

		if schema is None:
			schema = {
					**basic_schema,
					"properties": {},
					"required": [],
					}

		dtype = get_json_type(cls.dtype)
		if dtype is NotImplemented:
			raise NotImplementedError(cls.__name__, cls.dtype)
		else:
			schema["properties"][cls.__name__] = dtype

		if cls.required:
			schema["required"].append(cls.__name__)

		for line in (cls.__doc__ or '').split("\n\n"):
			line = ' '.join([p.strip() for p in line.split('\n') if p.strip()])
			if line:
				schema["properties"][cls.__name__]["description"] = line
				break

		return schema

	@property
	def schema_entry(cls) -> Dict[str, Any]:  # noqa: D102
		return cls.get_schema_entry()

	def __call__(cls, raw_config_vars: Dict[str, Any]) -> Any:  # type: ignore  # noqa: D102
		"""
		Alias for :meth:`ConfigVar.get <.ConfigVar.get>`.

		Returns the value of the :class:`~configconfig.configvar.ConfigVar`.

		:param raw_config_vars: Dictionary to obtain the value from.

		:rtype: See the :attr:`ConfigVar.rtype <.ConfigVar.rtype>` attribute.
		"""

		return cls.get(raw_config_vars)

	@abstractmethod
	def get(cls, raw_config_vars: Mapping[str, Any]):  # pragma: no cover  # noqa: D102
		return NotImplemented

	def __repr__(self) -> str:
		"""
		Return a string representation of the :class:`~.ConfigVarMeta` class.
		"""

		return f"<ConfigVar {self.__name__!r}>"
