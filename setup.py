# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in bloomvalley/__init__.py
from bloomvalley import __version__ as version

setup(
	name='bloomvalley',
	version=version,
	description='Website for Bloom Valley',
	author='Neil Lasrado',
	author_email='neil@bloomstack.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
