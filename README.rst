#############
configconfig
#############

.. start short_desc

**Load and validate YAML configuration files.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/configconfig/latest?logo=read-the-docs
	:target: https://configconfig.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/repo-helper/configconfig/workflows/Docs%20Check/badge.svg
	:target: https://github.com/repo-helper/configconfig/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/repo-helper/configconfig/workflows/Linux/badge.svg
	:target: https://github.com/repo-helper/configconfig/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/repo-helper/configconfig/workflows/Windows/badge.svg
	:target: https://github.com/repo-helper/configconfig/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/repo-helper/configconfig/workflows/macOS/badge.svg
	:target: https://github.com/repo-helper/configconfig/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/repo-helper/configconfig/workflows/Flake8/badge.svg
	:target: https://github.com/repo-helper/configconfig/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/repo-helper/configconfig/workflows/mypy/badge.svg
	:target: https://github.com/repo-helper/configconfig/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/repo-helper/configconfig/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/repo-helper/configconfig/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/repo-helper/configconfig/master?logo=coveralls
	:target: https://coveralls.io/github/repo-helper/configconfig?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/repo-helper/configconfig?logo=codefactor
	:target: https://www.codefactor.io/repository/github/repo-helper/configconfig
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/configconfig
	:target: https://pypi.org/project/configconfig/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/configconfig?logo=python&logoColor=white
	:target: https://pypi.org/project/configconfig/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/configconfig
	:target: https://pypi.org/project/configconfig/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/configconfig
	:target: https://pypi.org/project/configconfig/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/configconfig?logo=anaconda
	:target: https://anaconda.org/domdfcoding/configconfig
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/configconfig?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/configconfig
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/repo-helper/configconfig
	:target: https://github.com/repo-helper/configconfig/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/repo-helper/configconfig
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/repo-helper/configconfig/v0.6.2
	:target: https://github.com/repo-helper/configconfig/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/repo-helper/configconfig
	:target: https://github.com/repo-helper/configconfig/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2023
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/configconfig
	:target: https://pypi.org/project/configconfig/
	:alt: PyPI - Downloads

.. end shields

|

Installation
--------------

.. start installation

``configconfig`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install configconfig

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels https://conda.anaconda.org/conda-forge
		$ conda config --add channels https://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install configconfig

.. end installation
