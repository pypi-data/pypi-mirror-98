.. image:: https://img.shields.io/pypi/v/jaraco.test.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/jaraco.test.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/jaraco.test

.. image:: https://github.com/jaraco/jaraco.test/workflows/tests/badge.svg
   :target: https://github.com/jaraco/jaraco.test/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. .. image:: https://readthedocs.org/projects/jaracotest/badge/?version=latest
..    :target: https://jaracotest.readthedocs.io/en/latest/?badge=latest

Plugins
=======

The 'enabler' plugin allows configuration of plugins if present, but omits the settings if the plugin is not present. For example, to configure black to be enabled if the plugin is present, but not when it is not, add the following to your pyproject.toml::

    [jaraco.test.pytest.plugins.black]
    addopts = "--black"
