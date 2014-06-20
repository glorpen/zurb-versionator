#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import re
import os

pkgname = "zurb_versionator"

with open(os.path.join(os.path.dirname(__file__),"src",pkgname,"__init__.py"),"rt") as i:
    version = re.match('^__version__\s+=\s+"(.*)"$', i.read()).group(1)

setup(
    name='zurb-versionator',
    version=version,
    description='ZURB automatic packager',
    author='Arkadiusz Dzięgiel',
    author_email = "arkadiusz.dziegiel@glorpen.pl",
    maintainer = "Arkadiusz Dzięgiel",
    maintainer_email = "arkadiusz.dziegiel@glorpen.pl",
    packages=[pkgname],
    package_dir={pkgname:"src/"+pkgname},
    package_data={pkgname: ['resources/tpl/*.py']},
    include_package_data = True,
    classifiers=[
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3'
    ]
)
