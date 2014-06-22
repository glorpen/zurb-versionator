#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup
import imp
import glob

here = os.path.dirname(os.path.abspath(__file__))
pkg = "compass_stylesheets"

version = imp.load_source(pkg, os.path.join(here, '__init__.py')).__version__

here = os.path.dirname(__file__)
f = open(os.path.join(here, "README.rst"), "rt")
readme = f.read()
f.close()

setup(
    name='compass-stylesheets',
    version=version,
    description='The most advanced responsive front-end framework in the world. Quickly create prototypes and production code for sites and apps that work on any kind of device',
    long_description=readme,
    author='Chris Eppstein',
    author_email = "chris@eppsteins.net",
    maintainer = "Arkadiusz Dzięgiel",
    maintainer_email = "arkadiusz.dziegiel@glorpen.pl",
    url='http://compass-style.org/',
    packages=[pkg],
    package_dir={pkg:"."},
    package_data={pkg: list(glob.glob("stylesheets/*.scss"))+list(glob.glob("stylesheets/*/*.scss"))+list(glob.glob("stylesheets/*/*/*.scss"))+list(glob.glob("stylesheets/*/*/*/*.scss"))},
    include_package_data = True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
    ]
)
