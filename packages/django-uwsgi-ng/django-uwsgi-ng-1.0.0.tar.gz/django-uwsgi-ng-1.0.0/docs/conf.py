# -*- coding: utf-8 -*-

import sys
import os
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

sys.path.insert(0, os.path.abspath('..'))
from django_uwsgi import __version__


extensions = [
    'sphinx.ext.intersphinx',
    'releases',
]

releases_issue_uri = "https://edugit.org/AlekSIS/libs/django-uwsgi-ng/-/issues/%s"
releases_release_uri = "https://edugit.org/AlekSIS/libs/django-uwsgi-ng/-/tree/%s"

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'django-uwsgi-ng'
copyright = u'2016, Eugene MechanisM'

version = __version__
release = __version__

exclude_patterns = ['_build']

pygments_style = 'sphinx'

html_static_path = ['_static']

htmlhelp_basename = 'django-uwsgidoc'

latex_elements = {

}

latex_documents = [
    ('index', 'django-uwsgi-ng.tex', u'django-uwsgi-ng Documentation',
     u'Eugene MechanisM', 'manual'),
]

man_pages = [
    ('index', 'django-uwsgi-ng', u'django-uwsgi-ng Documentation',
     [u'Eugene MechanisM'], 1)
]

texinfo_documents = [
    ('index', 'django-uwsgi-ng', u'django-uwsgi-ng Documentation',
     u'Eugene MechanisM', 'django-uwsgi-ng', 'One line description of project.',
     'Miscellaneous'),
]
intersphinx_mapping = {'uwsgi': ('http://uwsgi-docs.readthedocs.org/en/latest/', None)}
