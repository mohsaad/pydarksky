#!/bin/env python3

from os import path
from setuptools import setup

current_dir = path.abspath(path.dirname(__file__))
with open(path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pycsk',
    version = '0.1.2',
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
    author_email='mohammad.saad@outlook.com',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
