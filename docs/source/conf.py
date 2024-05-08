

from pathlib import Path
import sys


# Add source to PYTHONPATH
sys.path.insert(0, Path(__file__).parents[2].resolve().as_posix())


# Project
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = 'Cine'
copyright = '2024, Leon Matthews'
author = 'Leon Matthews'


# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.napoleon',                          # Google style docstrings
    'sphinx.ext.viewcode',
    'sphinxcontrib.spelling',                       # Add `make spelling` target
]

autosummary_generate = True
todo_include_todos = True


# General configuration
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
templates_path = ['_templates']
exclude_patterns = []


# HTML output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'alabaster'
html_static_path = ['_static']
