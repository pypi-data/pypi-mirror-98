.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://github.com/IMIO/collective.pivot/workflows/Tests/badge.svg
    :target: https://github.com/IMIO/collective.pivot/actions?query=workflow%3ATests
    :alt: CI Status

.. image:: https://coveralls.io/repos/github/IMIO/collective.pivot/badge.svg?branch=main
    :target: https://coveralls.io/github/IMIO/collective.pivot?branch=main
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/collective.pivot.svg
    :target: https://pypi.python.org/pypi/collective.pivot/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.pivot.svg
    :target: https://pypi.python.org/pypi/collective.pivot
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.pivot.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.pivot.svg
    :target: https://pypi.python.org/pypi/collective.pivot/
    :alt: License


================
collective.pivot
================

Plone plugin which makes a connection to the CGT's DB PIVOT.
This one display listing and details of various tourist offers.
It's also possible to add filters.


Translations
------------

This product has been translated into

- French


Installation
------------

Install collective.pivot by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.pivot


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/imio/collective.pivot/issues
- Source Code: https://github.com/imio/collective.pivot


License
-------

The project is licensed under the GPLv2.
