#!/usr/bin/env python3
#
#  utils.py
"""
Utility functions
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
import copy
import sys
from enum import EnumMeta
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Type, TypeVar, Union

# 3rd party
from typing_extensions import Literal
from typing_inspect import is_literal_type  # type: ignore

if TYPE_CHECKING:
	# this package
	from configconfig.metaclass import ConfigVarMeta

if sys.version_info >= (3, 8):  # pragma: no cover (<py38)

	# stdlib
	from typing import get_args, get_origin

else:  # pragma: no cover (>=py38)

	# stdlib
	import collections.abc

	# 3rd party
	from typing_inspect import get_origin

	def get_args(tp):
		"""Get type arguments with all substitutions performed.

		For unions, basic simplifications used by Union constructor are performed.
		Examples::
			get_args(Dict[str, int]) == (str, int)
			get_args(int) == ()
			get_args(Union[int, Union[T, int], str][int]) == (int, str)
			get_args(Union[int, Tuple[T, int]][str]) == (int, Tuple[str, int])
			get_args(Callable[[], T][int]) == ([], int)
		"""
		if hasattr(tp, "__args__"):
			res = tp.__args__
			if get_origin(tp) is collections.abc.Callable and res[0] is not Ellipsis:
				res = (list(res[:-1]), res[-1])
			return res
		return ()


__all__ = ["optional_getter", "get_yaml_type", "make_schema", "check_union", "get_json_type", "tab"]

tab = "\t"
UnionType = type(Union)
GenericAliasType = type(List)


def optional_getter(raw_config_vars: Dict[str, Any], cls: "ConfigVarMeta", required: bool) -> Any:
	"""

	:param raw_config_vars:
	:param cls:
	:param required:
	"""

	if required:
		try:
			return raw_config_vars[cls.__name__]
		except KeyError:
			raise ValueError(f"A value for '{cls.__name__}' is required.") from None
	else:

		if cls.__name__ in raw_config_vars:
			return raw_config_vars[cls.__name__]
		else:
			if isinstance(cls.default, Callable):  # type: ignore
				return copy.deepcopy(cls.default(raw_config_vars))
			else:
				return copy.deepcopy(cls.default)


yaml_type_lookup = {
		str: "String",
		int: "Integer",
		float: "Float",
		bool: "Boolean",
		list: "Sequence",
		dict: "Mapping",
		Any: "anything",
		}


def get_yaml_type(type_: Type) -> str:
	"""
	Get the YAML type that corresponds to the given Python type.

	:param type_:
	"""

	if type_ in yaml_type_lookup:
		return yaml_type_lookup[type_]

	elif get_origin(type_) is Union:
		dtype = " or ".join(yaml_type_lookup[x] for x in type_.__args__)
		return dtype

	elif get_origin(type_) in {list, List}:
		inner_types = (get_yaml_type(x) for x in get_args(type_) if not isinstance(x, TypeVar))
		dtype = " or ".join(inner_types)
		if dtype:
			return f"Sequence of {dtype}"
		else:
			return "Sequence"

	elif get_origin(type_) in {dict, Dict}:
		args = get_args(type_)
		if not args or any(isinstance(t, TypeVar) for t in args):
			return "Mapping"
		else:
			dtype = " to ".join(get_yaml_type(x) for x in get_args(type_))
			return f"Mapping of {dtype}"

	elif is_literal_type(type_):
		types = [y for y in type_.__args__]
		return " or ".join(repr(x) for x in types)

	elif isinstance(type_, EnumMeta):
		return " or ".join([repr(x._value_) for x in type_])  # type: ignore

	else:
		return str(type_)


def make_schema(*configuration_variables: "ConfigVarMeta") -> Dict[str, Any]:
	"""
	Create a ``JSON`` schema from a list of :class:`~configconfig.class.ConfigVar` classes.

	:param configuration_variables:

	:return: Dictionary representation of the ``JSON`` schema.
	"""

	schema = {
			"$schema": "http://json-schema.org/schema#",
			"type": "object",
			"properties": {},
			"required": [],
			"additionalProperties": False,
			}

	for var in configuration_variables:
		schema = var.get_schema_entry(schema)

	return schema


def check_union(obj: Any, dtype: Union[GenericAliasType, UnionType]):  # type: ignore
	r"""
	Check if the type of ``obj`` is one of the types in a :class:`typing.Union`, :class:`typing.List` etc.

	:param obj:
	:param dtype:
	:type dtype: :class:`~typing.Union`\, :class:`~typing.List`\, etc.
	"""

	return isinstance(obj, dtype.__args__)  # type: ignore


def get_json_type(type_: Type) -> Dict[str, Union[str, List, Dict]]:
	"""
	Get the type for the JSON schema that corresponds to the given Python type.

	:param type_:
	"""

	if type_ in json_type_lookup:
		return {"type": json_type_lookup[type_]}

	elif get_origin(type_) is Union:
		return {"type": [get_json_type(t)["type"] for t in type_.__args__]}

	elif get_origin(type_) in {list, List}:
		args = get_args(type_)
		if args:

			items = get_json_type(args[0])

			if items is NotImplemented:
				return {"type": "array"}
			elif "type" in items:
				return {"type": "array", "items": items}
			elif "enum" in items:
				return {"type": "array", "items": items}
			else:
				return {"type": "array"}

		return {"type": "array"}

	elif get_origin(type_) in {dict, Dict}:
		return {"type": "object"}

	elif get_origin(type_) is Literal:
		return {"enum": [x for x in type_.__args__]}

	elif isinstance(type_, EnumMeta):
		return {"enum": [x._value_ for x in type_]}  # type: ignore

	elif type_ is bool:
		return {"type": ["boolean", "string"]}

	else:
		return NotImplemented


json_type_lookup = {
		str: "string",
		int: "number",
		float: "number",
		dict: "object",
		list: "array",
		}
