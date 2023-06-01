# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# add path of source tree so autodoc can load the docstrings
import os
import sys
sys.path.insert(0, os.path.abspath('../src/'))

project = 'hps_align'
copyright = '2023, HPS Collaboratoin'
author = 'HPS Collaboratoin'

# we can have the GitHub actions overwrite this value when building
#  the documentation from a specific tag, so we leave it as 'local'
release = 'local'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.autodoc', # generate docs from docstrings
        'sphinx.ext.napoleon', # support NumPy style docstrings
        'sphinx_click',
        ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = [] 
