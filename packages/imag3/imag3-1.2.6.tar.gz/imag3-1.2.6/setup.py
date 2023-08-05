#!/usr/bin/env python3

# Note!
# ' are required, do not use any '.

# setup.
from setuptools import setup, find_packages
setup(
	name='imag3',
	version='1.2.6',
	description='Some description.',
	url='http://github.com/vandenberghinc/imag3',
	author='Daan van den Bergh',
	author_email='vandenberghinc.contact@gmail.com',
	license='MIT',
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	install_requires=[
            'cl1',
            'dev0s',
            'syst3m',
            'r3sponse',
            'netw0rk',
        ],)