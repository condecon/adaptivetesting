import os
import sys
from sphinx.application import Sphinx
sys.path.insert(0, os.path.abspath('../'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'adaptivetesting'
copyright = '2025, Jonas Engicht'
author = 'Jonas Engicht'
release = '2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = []

autoclass_content = 'both'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_css_files = [
    'main.css',
]
html_logo = "_static/logo.svg"
html_theme_options = {
    "navigation_depth": -1,
    "repository_url": "https://github.com/condecon/adaptivetesting",
    "use_issues_button": True

}




def setup(app: Sphinx):
    app.add_css_file("main.css")
