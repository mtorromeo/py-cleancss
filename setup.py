#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
import os, cleancss

README = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
	name='CleanCSS',
	author='Massimiliano Torromeo',
	author_email='massimiliano.torromeo@gmail.com',
	version=cleancss.version,
	url='http://github.com/mtorromeo/py-cleancss/',
	download_url = "http://github.com/mtorromeo/py-cleancss/tarball/v"+cleancss.version,
	py_modules=['cleancss'],
	description='Pythonic markup for css',
	long_description = open(README).read(),
	keywords=["css"],
	classifiers=[
		'License :: OSI Approved :: BSD License',
		"Development Status :: 5 - Production/Stable",
		'Programming Language :: Python'
	],
	license = "BSD License"
)
