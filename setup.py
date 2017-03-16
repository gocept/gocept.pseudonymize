# Copyright (c) 2013-2015 gocept gmbh & co. kg
# See also LICENSE.txt

# This should be only one line. If it must be multi-line, indent the second
# line onwards to keep the PKG-INFO file format intact.
"""Pseudonymize data like text, email addresses or license tags.
"""

from setuptools import setup, find_packages
import glob
import os.path


def project_path(*names):
    return os.path.join(os.path.dirname(__file__), *names)


def read(*names):
    return open(project_path(*names)).read()


setup(
    name='gocept.pseudonymize',
    version='0.5.dev0',

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
    license='ZPL 2.1',
    url='https://bitbucket.org/gocept/gocept.pseudonymize/',

    keywords='Pseudonymization',
    classifiers="""\
License :: OSI Approved :: Zope Public License
Programming Language :: Python
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
