#!/usr/bin/env python
"""
# Author: Xiong Lei
# Created Time : Sun 17 Nov 2019 03:37:47 PM CST

# File Name: setup.py
# Description:

"""
import pathlib
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name='scale_v2',
      version='2.0.1.dev',
      packages=find_packages(),
      description='Single-cell integrative Analysis via Latent feature Extraction',
      long_description=README,

      author='Lei Xiong',
      author_email='jsxlei@gmail.com',
      url='https://github.com/jsxlei/scale_v2',
      scripts=['SCALE.py'],
      install_requires=requirements,
      python_requires='>3.6.0',
      license='MIT',

      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX :: Linux',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
     ],
     )


