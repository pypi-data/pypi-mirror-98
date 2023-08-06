#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""
This module contains MyAMS.js package
"""
import os
from setuptools import setup, find_packages


DOCS = os.path.join(os.path.dirname(__file__),
                    'docs')

README = os.path.join(DOCS, 'README.txt')
HISTORY = os.path.join(DOCS, 'HISTORY.txt')

version = '1.3.3'
long_description = open(README).read() + '\n\n' + open(HISTORY).read()

data_dir = 'pkg'
data_files = [(d, [os.path.join(d, f) for f in files])
              for d, folders, files in os.walk(data_dir)]

tests_require = [
    'pyramid_zcml',
    'zope.exceptions'
]

setup(name='myams_js',
      version=version,
      description="MyAMS.js extension framework",
      long_description=long_description,
      classifiers=[
          "License :: OSI Approved :: Zope Public License",
          "Development Status :: 4 - Beta",
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='Pyramid PyAMS',
      author='Thierry Florac',
      author_email='tflorac@ulthar.net',
      url='https://pyams.readthedocs.io',
      license='ZPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=[],
      include_package_data=True,
      package_data={
          '': ['*.zcml', '*.txt', '*.pt', '*.pot', '*.po', '*.mo',
               '*.png', '*.gif', '*.jpeg', '*.jpg', '*.css', '*.js',
               '*.ttf', '*.eot', '*.woff', '*.woff2', '*.svg']
      },
      data_files=data_files,
      zip_safe=False,
      # uncomment this to be able to run tests with setup.py
      # test_suite="myams_js.tests.test_utilsdocs.test_suite",
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'fanstatic',
          'pyams_utils >= 1.2.0'
      ],
      entry_points={
          'fanstatic.libraries': [
              'myams = myams_js:library'
          ]
      })
