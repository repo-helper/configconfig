#  This file is managed by 'repo_helper'. Don't edit it directly.

__all__ = ["extras_require"]

extras_require = {
		"sphinx": ["docutils", "sphinx<3.4.0,>=3.0.3", "sphinx-toolbox"],
		"testing": ["pytest"],
		"all": ["docutils", "pytest", "sphinx<3.4.0,>=3.0.3", "sphinx-toolbox"]
		}
