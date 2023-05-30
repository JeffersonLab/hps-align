Building Docs
=============

Building sphinx-based documentation locally is rather 
simple once you have the setup done correctly.

Sphinx is available on PyPI, so one can::

    pip install Sphinx

Then one can build the documentation from the root of this repository.::

    sphinx-build docs _site

Sphinx Primer
-------------
While doxygen puts pretty much all documentation into the form
of comments inside of the source files, sphinx steps away from
this and allows the user to define where documentation for specific
groups of code should be. This means the user can define the organization
of the code documentation as well as intersperse the documentation
generated from the code docstrings with manually written documentation.

Looking at the rst files in the docs directory will give you some
examples on how to tell sphinx to insert the documentation for
a specific module, class, or function.

Technically, we are using the 
`sphinx-autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_ 
plugin to generate the documentation from the python docstrings.

Doc Strings
-----------
The sphinx configuration assumes that the docstrings follow
the `NumPy docstring format <https://numpydoc.readthedocs.io/en/latest/format.html>`_
and the raw documentation files (`*.rst` files) are
`ReStructured Text <https://github.com/ralsina/rst-cheatsheet/blob/master/rst-cheatsheet.rst>`_.
