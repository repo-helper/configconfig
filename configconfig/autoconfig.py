#!/usr/bin/env python3
#
#  autoconfig.py
"""
A Sphinx directive for documenting configuration variables in Python.

Provides the :rst:dir:`autoconfig` directive to document configuration variables automatically,
the :rst:dir:`conf` directive to document configuration manually,
and the :rst:role:`conf` role to link to a :rst:dir:`conf` directive.
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
from typing import Any, Dict, List, Type

# 3rd party
from docutils import nodes
from docutils.parsers.rst.directives import unchanged
from docutils.statemachine import ViewList
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.ext.autodoc.importer import import_module, import_object
from sphinx.util.docutils import SphinxDirective
from sphinx_toolbox.utils import Purger

# this package
from configconfig import __version__
from configconfig.configvar import ConfigVar
from configconfig.metaclass import ConfigVarMeta

__all__ = ["AutoConfigDirective", "conf_node_purger", "parse_conf_node", "setup"]

conf_node_purger = Purger("all_conf_nodes")


class AutoConfigDirective(SphinxDirective):
	"""

	"""

	has_content: bool = True
	required_arguments: int = 1
	# the fully qualified name of the ConfigVar object,
	# or the name of the module if :category: given
	option_spec = {"category": unchanged}

	def run(self) -> List[nodes.Node]:
		"""

		"""

		config_var: str = self.arguments[0]
		node_list = []

		if "category" in self.options:
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
					continue
				elif var_obj.category == category:
					node_list.append(self.document_config_var(var_obj))
		else:
			module_name, class_ = config_var.rsplit(".", 1)
			var_obj = import_object(module_name, [class_])[3]
			if not issubclass(var_obj, ConfigVar):
				raise TypeError("'autoconfig' can only be used with 'ConfigVar' subclasses.")

			node_list.append(self.document_config_var(var_obj))

		return node_list

	def document_config_var(self, var_obj: Type[ConfigVar]) -> nodes.paragraph:
		"""

		:param var_obj:
		"""

		docstring = var_obj.make_documentation()

		targetid = f'autoconfig-{self.env.new_serialno("autoconfig"):d}'
		targetnode = nodes.section(ids=[targetid])

		content = docstring.replace("\t", "    ")
		view = ViewList(content.split("\n"))
		config_node = nodes.paragraph(rawsource=content)
		self.state.nested_parse(view, self.content_offset, config_node)

		conf_node_purger.add_node(self.env, config_node, targetnode, self.lineno)

		return config_node


def parse_conf_node(env: BuildEnvironment, text: str, node: nodes.Node) -> str:
	"""

	:param env:
	:param text:
	:param node:
	"""

	args = text.split("^")
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
	Setup Sphinx Extension

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
