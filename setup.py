#!/bin/env python3

from setuptools import setup

setup(
    name='pycsk',
    version = '0.1.0',
    packages = ['pycsk'],
    entry_points = {
      'console_scripts': [
          'csk = pycsk.__main__:main'
      ]},
    install_requires = [
      'sty',
      'appdirs'
    ],
    license = 'MIT',
    url = 'https://github.com/mohsaad/pydarksky',
    author='Mohammad Saad',
    author_email='me@mohsaad.com'
)
