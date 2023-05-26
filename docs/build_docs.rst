Building Docs
=============

Building sphinx-based documentation locally is rather 
simple once you have the setup done correctly.

Sphinx is available on PyPI, so one can::

    pip install Sphinx

Then one can build the documentation from the root of this repository.::

    sphinx-build docs docs/html


Doc Strings
-----------
The sphinx configuration assumes that the docstrings follow
the `NumPy docstring format <https://numpydoc.readthedocs.io/en/latest/format.html>`_
and the raw documentation files (`*.rst` files) are
`ReStructured Text <https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst>`_.
