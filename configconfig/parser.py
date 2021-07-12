#!/usr/bin/env python3
#
#  parser.py
"""
Configuration parser.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import tempfile
from typing import Any, List, Mapping, MutableMapping

# 3rd party
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from ruamel.yaml import YAML

# this package
from configconfig.metaclass import ConfigVarMeta
from configconfig.utils import make_schema
from configconfig.validator import validate_files

__all__ = ["Parser"]


class Parser:
	"""
	Base class for YAML configuration parsers.

	Custom parsing steps for each configuration variable can be implemented with methods in the form:

	.. code-block:: python

		def visit_<configuration value name>(
				self,
				raw_config_vars: Dict[str, Any],
				) -> Any: ...

	The method must return the value to set the configuration variable to,
	or raise an error in the case of invalid input.

	|

	.. latex:vspace:: -55px

	A final custom parsing step, useful when several values must be set at once,
	may be implemented in the ``custom_parsing`` method:

	.. code-block:: python

		def custom_parsing(
				self,
				raw_config_vars: Mapping[str, Any],
				parsed_config_vars: MutableMapping[str, Any],
				filename: PathPlus,
				) -> MutableMapping[str, Any]: ...

	This takes the mapping of raw configuration variables,
	the mapping of parsed variables (those set with the ``visit_<configuration value name>`` method),
	and the configuration file name. The method must return the ``parsed_config_vars``.
	"""

	config_vars: List[ConfigVarMeta]

	def __init__(self, allow_unknown_keys: bool = False):
		self.allow_unknown_keys = allow_unknown_keys

	def run(self, filename: PathLike):
		"""
		Parse configuration from the given file.

		:param filename: The filename of the YAML configuration file.
		"""

		filename = PathPlus(filename)

		if not filename.is_file():
			raise FileNotFoundError(str(filename))

		with tempfile.TemporaryDirectory() as tmpdir:
			tmpdir_p = PathPlus(tmpdir)
			schema_file = tmpdir_p / "schema.json"
			schema = make_schema(*self.config_vars)
			schema["additionalProperties"] = self.allow_unknown_keys
			schema_file.dump_json(schema)
			validate_files(schema_file, filename)

		parsed_config_vars: MutableMapping[str, Any] = {}

		with filename.open() as file:
			raw_config_vars: Mapping[str, Any] = YAML(typ="safe", pure=True).load(file)

		for var in self.config_vars:
			parsed_config_vars[var.__name__] = getattr(self, f"visit_{var.__name__}", var.get)(raw_config_vars)

		return self.custom_parsing(raw_config_vars, parsed_config_vars, filename)

	def custom_parsing(
			self,
			raw_config_vars: Mapping[str, Any],
			parsed_config_vars: MutableMapping[str, Any],
			filename: PathPlus,
			) -> MutableMapping[str, Any]:
		"""
		Custom parsing step.

		:param raw_config_vars: Mapping of raw configuration values loaded from the YAML configuration file.
		:param parsed_config_vars: Mapping of parsed configuration values.
		:param filename: The filename of the YAML configuration file.
		"""

		return parsed_config_vars
