#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open('README.md') as f:
    README = f.read()

with open('dj_pkcs7/version.py') as f:
    __version__ = ''
    exec(f.read())  # set __version__

with open('requirements-dev.txt') as f:
    test_requires = f.read()

setup(
    name='dj_pkcs7',
    version=__version__,
    description='Django PKCS7 parser',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/rhab/dj-pkcs7',
    author='Robert Habermann',
    author_email='mail@rhab.de',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Communications :: Email',
        'Topic :: Security :: Cryptography',
    ],
    keywords='smime cryptography pkcs7 email S/MIME encrypt sign',
    packages=find_packages(exclude=['demo', '*_test.py', 'tests', 'test_*.py']),
    include_package_data=True,
    platforms=["all"],
    install_requires=['Django', 'asn1crypto', 'extract-msg'],
    setup_requires=['pytest-runner'],
    tests_require=test_requires,
    test_suite='tests',
    extras_require={
        'test': test_requires
    },
    zip_safe=False,
)
