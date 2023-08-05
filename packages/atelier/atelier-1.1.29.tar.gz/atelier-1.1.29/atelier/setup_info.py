# Copyright 2013-2021 Rumma & Ko Ltd
# License: BSD, see LICENSE for more details.

# This module has no docstring because it is to be execfile'd
# from `setup.py`, `atelier/__init__.py` and possibly some external
# tools, too.

install_requires = ['invoke', 'argh', 'six',
                    'future', 'Babel',
                    'python_dateutil', 'Sphinx', 'rstgen']
install_requires.append('sphinx_rtd_theme')
# trying to fix #3246
tests_require = ['gitpython', 'pytest-cov']

# Explicitly install `importlib` under Python 2.6. Thanks to
# http://stackoverflow.com/questions/9418064
try:
    import importlib
except ImportError:
    install_requires.append('importlib')

SETUP_INFO = dict(
    name='atelier',
    version='1.1.29',
    install_requires=install_requires,
    tests_require=tests_require,
    scripts=['scripts/per_project'],
    description="A collection of tools for software artists",
    license='BSD-2-Clause',
    test_suite='tests',
    author='Luc Saffre',
    author_email='luc@lino-framework.org',
    url="https://lino-framework.gitlab.io/atelier",
    long_description="""\

`atelier` is a collection of tools for managing and maintaining Python software
projects.

It contains:

- some general Python utilities
  (`atelier.utils <https://lino-framework.gitlab.io/atelier/api/atelier.utils.html>`_)
- some Sphinx extensions
  (`atelier.sphinxconf <https://lino-framework.gitlab.io/atelier/api/atelier.sphinxconf.html>`_)
- a library of invoke commands
  (`atelier.invlib <https://lino-framework.gitlab.io/atelier/api/atelier.invlib.html>`_)
- a minimalistic project management
  (`atelier.projects <https://lino-framework.gitlab.io/atelier/api/atelier.projects.html>`_)

The central project homepage is https://lino-framework.gitlab.io/atelier

""",
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3.7
Framework :: Sphinx :: Extension
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent""".splitlines())

SETUP_INFO.update(packages=[n for n in """
atelier
atelier.sphinxconf
atelier.invlib
""".splitlines() if n])

SETUP_INFO.update(package_data=dict())


def add_package_data(package, *patterns):
    l = SETUP_INFO['package_data'].setdefault(package, [])
    l.extend(patterns)
    return l


add_package_data('atelier.sphinxconf', '*.html')
