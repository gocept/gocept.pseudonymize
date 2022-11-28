# Copyright (c) 2013-2022 gocept gmbh & co. kg
# See also LICENSE.txt

# This should be only one line. If it must be multi-line, indent the second
# line onwards to keep the PKG-INFO file format intact.
"""Pseudonymize data like text, email addresses or license tags.
"""

from setuptools import find_packages
from setuptools import setup


def read(name):
    """Read a file."""
    with open(name) as f:
        return f.read()


setup(
    name='gocept.pseudonymize',
    version='3.0.dev0',

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
    url='https://github.com/gocept/gocept.pseudonymize',

    keywords='Pseudonymization',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: German',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
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
