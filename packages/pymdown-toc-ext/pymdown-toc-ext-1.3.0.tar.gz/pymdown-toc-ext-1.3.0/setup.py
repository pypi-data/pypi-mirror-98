# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pymdown_toc_ext']
install_requires = \
['Markdown>=3.2,<4.0']

entry_points = \
{u'markdown.extensions': ['toc_ext = pymdown_toc_ext:TocExtExtension']}

setup_kwargs = {
    'name': 'pymdown-toc-ext',
    'version': '1.3.0',
    'description': 'An extension for Python-Markdown which extends the built-in toc extension with additional capabilities to customize the generated table of contents.',
    'long_description': None,
    'author': 'Benjamin Dobell',
    'author_email': 'benjamin.dobell@glassechidna.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Benjamin-Dobell/pymdown-toc-ext',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
