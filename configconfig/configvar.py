#!/usr/bin/env python3
#
#  configvar.py
"""
Base class for ``YAML`` configuration values.
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
from textwrap import dedent, indent
from typing import Any, Callable, Dict, Optional, Type

# 3rd party
from typing_inspect import is_literal_type  # type: ignore

# this package
from configconfig.metaclass import ConfigVarMeta
from configconfig.utils import get_yaml_type, tab
from configconfig.validator import Validator

__all__ = ["ConfigVar"]


class ConfigVar(metaclass=ConfigVarMeta):
	"""
	Base class for ``YAML`` configuration values.

	The class docstring should be the description of the config var, with an example,
	and the name of the class should be the variable name.

	If you would prefer a more Pythonic naming approach the variable name can
	be configured with the ``name`` class variable.

	**Example:**

	.. code-block:: python

		class platforms(ConfigVar):
			\"\"\"
			A case-insensitive list of platforms to perform tests for.

			Example:

			.. code-block:: yaml

				platforms:
				  - Windows
				  - macOS
				  - Linux

			These values determine the GitHub test workflows to enable,
			and the Trove classifiers used on PyPI.
			\"\"\"

			dtype = List[Literal["Windows", "macOS", "Linux"]]
			default: List[str] = ["Windows", "macOS", "Linux"]
			category: str = "packaging"

	"""

	dtype: Type
	"""
	The allowed type or types in the ``YAML`` configuration file.
	"""

	rtype: Type
	"""
	The variable type passed to Jinja2.
	If ``None`` :attr:`~configconfig.configvar.ConfigVar.dtype` is used.
	Ignored for ``dtype=bool``.
	"""

	required: bool
	"""
	Flag to indicate whether the configuration value is required. Default :py:obj:`False`.
	"""

	default: Any
	"""
	Flag to indicate whether the configuration value is required. Defaults to ``''`` if unset.
	"""

	category: str
	"""
	The category the :class:`~configconfig.configvar.ConfigVar` is listed under in the documentation.
	"""

	@classmethod
	def validator(cls, value: Any) -> Any:
		"""
		Function to call to validate the values.

		* The callable must have a single required argument (the value).
		* Should raise :exc:`ValueError` if values are invalid, and return the values if they are valid.
		* May change the values (e.g. make lowercase) before returning.
		"""

		return value

	def __new__(cls, raw_config_vars: Dict[str, Any]) -> Any:
		# Exists purely so mypy knows about the signature
		return cls.get(raw_config_vars)  # pragma: no cover

	@classmethod
	def get(cls, raw_config_vars: Optional[Dict[str, Any]] = None) -> Any:
		"""
		Returns the value of this :class:`~configconfig.configvar.ConfigVar`

		:param raw_config_vars: Dictionary to obtain the value from.

		:rtype: See the ``rtype`` attribute.
		"""

		return cls.validator(cls.validate(raw_config_vars))

	@classmethod
	def validate(cls, raw_config_vars: Optional[Dict[str, Any]] = None) -> Any:
		"""
		Validate the value obtained from the ``YAML`` file and coerce into the appropriate return type.

		:param raw_config_vars: Dictionary to obtain the value from.

		:rtype: See the ``rtype`` attribute.
		"""

		if raw_config_vars is None:
			raw_config_vars = {}

		if cls.rtype is None:
			cls.rtype = cls.dtype

		validator = Validator(cls)
		return validator.validate(raw_config_vars)

	@classmethod
	def make_documentation(cls):
		docstring = cls.__doc__ or ''
		docstring = (indent(dedent(docstring), tab))

		if not docstring.startswith("\n"):
			docstring = "\n" + docstring

		buf = f"""
.. conf:: {cls.__name__}
{docstring}

	**Required**: {'yes' if cls.required else 'no'}

"""

		if not cls.required:
			if cls.default == []:
				buf += "\t**Default**: [ ]\n\n"
			elif cls.default == {}:
				buf += "\t**Default**: { }\n\n"
			elif isinstance(cls.default, Callable):  # type: ignore
				buf += f"\t**Default**: The value of :conf:`{cls.default.__name__}`\n\n"
			elif isinstance(cls.default, bool):
				buf += f"\t**Default**: :py:obj:`{cls.default}`\n\n"
			elif isinstance(cls.default, str):
				if cls.default == '':
					buf += "\t**Default**: <blank>\n\n"
				else:
					buf += f"\t**Default**: ``{cls.default}``\n\n"
			else:
				buf += f"\t**Default**: {cls.default}\n\n"

		buf += f"\t**Type**: {get_yaml_type(cls.dtype)}"

		if is_literal_type(cls.dtype):
			valid_values = ", ".join(f"``{x}``" for x in cls.dtype.__args__)
			buf += f"\n\n\t**Allowed values**: {valid_values}"
		elif hasattr(cls.dtype, "__args__") and is_literal_type(cls.dtype.__args__[0]):
			valid_values = ", ".join(f"``{x}``" for x in cls.dtype.__args__[0].__args__)
			buf += f"\n\n\t**Allowed values**: {valid_values}"

		return buf
