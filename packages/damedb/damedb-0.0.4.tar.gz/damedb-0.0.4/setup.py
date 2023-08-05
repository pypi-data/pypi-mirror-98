#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (C) 2021  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with DameDB; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(name='damedb',
      version='0.0.4',
      description='Learning Databases in Python from tests by David Arroyo MEnéndez',
      long_description= long_description,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
      ],
      keywords='python3, libraries, databases',
      url='http://github.com/davidam/damedb',
      author='David Arroyo Menéndez',
      author_email='davidam@gmail.com',
      license='GPLv3',
      packages=[
          'damedb',
          'damedb.files',
          'damedb.tests'
      ],
      namespace_packages=[
          'damedb',
          'damedb.files',
          'damedb.tests',
      ],
      install_requires=[
          'mongoengine',
          'mysql-connector',
          'pysqlite3',
          'postgres',
      ],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      include_package_data=True,
      zip_safe=False)
