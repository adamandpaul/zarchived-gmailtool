import sys
import os
import shlex
autoclass_content = 'both'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]
templates_path = ['_templates']
ource_suffix = '.rst'
master_doc = 'index'
project = u'gmailtool'
copyright = u'2017, Adam Terrey'
author = u'Adam Terrey'
version = '1.0.dev1'
release = '1.0.dev1'
language = None
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
htmlhelp_basename = 'gmailtool'
"""
latex_elements = {}
latex_documents = [
  (master_doc, 'ArtExperimental.tex', u'art.experimental',
   u'ArtExperimental Documentation', 'documentation'),
]
man_pages = [
    (master_doc, 'artexperimental', u'art.experimental documentation',
     [author], 1)
]
texinfo_documents = [
  (master_doc, 'AccountsMonster', u'Accounts Monster Documentation',
   author, 'AccountsMonster', 'One line description of project.',
   'Miscellaneous'),
]
"""
