# Copyright (c) 2013-2017 gocept gmbh & co. kg
# See also LICENSE.txt

# This should be only one line. If it must be multi-line, indent the second
# line onwards to keep the PKG-INFO file format intact.
"""Pseudonymize data like text, email addresses or license tags.
"""

from setuptools import setup, find_packages


def read(name):
    """Read a file."""
    with open(name) as f:
        return f.read()


setup(
    name='gocept.pseudonymize',
    version='2.0.1',

    install_requires=[
        'setuptools',
    ],

    extras_require={
        'test': [
            'mock',
        ],
    },

    entry_points={
        'console_scripts': [
            # 'binary-name = gocept.pseudonymize.module:function'
        ],
    },

    author='gocept <mail@gocept.com>',
    author_email='mail@gocept.com',
    license='MIT',
    url='https://bitbucket.org/gocept/gocept.pseudonymize/',

    keywords='Pseudonymization',
    classifiers="""\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: System Administrators
Operating System :: OS Independent
Topic :: Security :: Cryptography
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Text Processing :: Filters
Topic :: Utilities
License :: OSI Approved :: MIT License
Natural Language :: German
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: Implementation :: CPython
Programming Language :: Python :: Implementation :: PyPy
"""[:-1].split('\n'),
    description=__doc__.strip(),
    long_description='\n\n'.join([
        '.. contents::',
        read('README.rst'),
        read('HACKING.rst'),
        read('CHANGES.rst'),
    ]),
    namespace_packages=['gocept'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
)
