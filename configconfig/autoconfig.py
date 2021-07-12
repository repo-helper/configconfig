#!/usr/bin/env python3
#
#  autoconfig.py
"""
A Sphinx directive for documenting YAML configuration values.

Provides the :rst:dir:`autoconfig` directive to document configuration
values automatically, the :rst:dir:`conf` directive to document them manually,
and the :rst:role:`conf` role to link to a :rst:dir:`conf` directive.

.. extras-require:: sphinx
	:pyproject:


Usage
---------

.. rst:directive:: autoconfig

	Directive to automatically document an YAML configuration value.

	Takes a single argument, either the fully qualified name of the :class:`~.ConfigVar` object,
	or the name of the module if the ``:category:`` option is given.

	.. rst:directive:option:: category
		:type: string

		(optional) The category of options to document.


.. rst:directive:: conf

	Directive to document an YAML configuration value.


.. rst:role:: conf

	Role to add a cross-reference to a :rst:dir:`conf` or :rst:dir:`autoconfig` directive.


.. latex:clearpage::

API Reference
---------------
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
#  ``.. conf::`` directive and ``:conf:`` role based on Tox's documentation.
#  From https://github.com/tox-dev/tox/blob/master/docs/conf.py
#  MIT Licensed
#

# stdlib
import warnings
from typing import Any, Dict, Sequence, Type

# 3rd party
from docutils import nodes  # nodep
from docutils.parsers.rst.directives import unchanged  # nodep
from docutils.statemachine import StringList  # nodep
from sphinx import addnodes  # nodep
from sphinx.application import Sphinx  # nodep
from sphinx.environment import BuildEnvironment  # nodep
from sphinx.ext.autodoc.importer import import_module, import_object  # nodep
from sphinx.util.docutils import SphinxDirective  # nodep
from sphinx_toolbox.utils import Purger  # nodep

# this package
from configconfig import __version__
from configconfig.configvar import ConfigVar
from configconfig.metaclass import ConfigVarMeta

__all__ = ["AutoConfigDirective", "conf_node_purger", "parse_conf_node", "setup"]

conf_node_purger = Purger("all_conf_nodes")


class AutoConfigDirective(SphinxDirective):
	"""
	Sphinx directive to automatically document an YAML configuration value.
	"""

	has_content: bool = True
	required_arguments: int = 1
	# the fully qualified name of the ConfigVar object,
	# or the name of the module if :category: given
	option_spec = {"category": unchanged}

	def run(self) -> Sequence[nodes.Node]:  # type: ignore
		"""
		Process the content of the directive.
		"""

		config_var: str = self.arguments[0]

		if "category" in self.options:
			node_list = []
			module = import_module(config_var)

			if hasattr(module, "__all__"):
				module_all = module.__all__
			else:
				module_all = module.__dict__

			category = self.options["category"]

			# TODO: category header
			# 			header = f"""\
			# ={'='*len(category)}
			# {category.capitalize()}
			# ={'='*len(category)}
			#
			# """
			# 			content = header.replace("\t", "    ")
			# 			view = ViewList(content.split("\n"))
			# 			config_node = nodes.paragraph(rawsource=content)
			# 			self.state.nested_parse(view, self.content_offset, config_node)

			for class_ in module_all:
				var_obj: Type[ConfigVar] = getattr(module, class_)

				if not (isinstance(var_obj, ConfigVarMeta) and issubclass(var_obj, ConfigVar)):
					continue  # pragma: no cover
				elif var_obj.category == category:
					node_list.append(self.document_config_var(var_obj))

			return node_list

		else:
			module_name, class_ = config_var.rsplit('.', 1)
			var_obj = import_object(module_name, [class_])[3]
			if not issubclass(var_obj, ConfigVar):
				warnings.warn("'autoconfig' can only be used with 'ConfigVar' subclasses.")
				return []

			return [self.document_config_var(var_obj)]

	def document_config_var(self, var_obj: Type[ConfigVar]) -> nodes.paragraph:
		"""
		Document the given configuration value.

		:param var_obj:
		"""

		docstring = var_obj.make_documentation()

		targetid = f'autoconfig-{self.env.new_serialno("autoconfig"):d}'
		targetnode = nodes.section(ids=[targetid])

		content = docstring.replace('\t', "    ")
		view = StringList(content.split('\n'))
		config_node = nodes.paragraph(rawsource=content)
		self.state.nested_parse(view, self.content_offset, config_node)

		conf_node_purger.add_node(self.env, config_node, targetnode, self.lineno)

		return config_node


def parse_conf_node(env: BuildEnvironment, text: str, node: addnodes.desc_signature) -> str:
	"""
	Parse the content of a :rst:dir:`conf` directive.

	:param env: The Sphinx build environment.
	:param text: The content of the directive.
	:param node: The docutils node class.
	"""

	args = text.split('^')
	name = args[0].strip()

	node += addnodes.literal_strong(name, name)

	if len(args) > 2:
		default = f"={args[2].strip()}"
		node += nodes.literal(text=default)

	if len(args) > 1:
		content = f"({args[1].strip()})"
		node += addnodes.compact_paragraph(text=content)

	return name  # this will be the link


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup Sphinx Extension.

	:param app: The Sphinx app
	"""

	app.add_directive("autoconfig", AutoConfigDirective)
	app.connect("env-purge-doc", conf_node_purger.purge_nodes)

	app.add_object_type(
			directivename="conf",
			rolename="conf",
			objname="configuration value",
			indextemplate="pair: %s; configuration value",
			parse_node=parse_conf_node,
			)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}
