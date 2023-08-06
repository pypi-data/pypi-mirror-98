#!/usr/bin/env python

from setuptools import setup#, find_packages

classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
]

setup(
    name='pijavski',
    version='0.0.4',
    description='Python CFFI bindings for Pijavski C++ function to calculate minimum of a given function.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    #url='',
    author='Santiago Velasquez',
    author_email='js.velasquez123@gmail.com',
    #license='GNU',
    lincese_file='LICENSE',
    classifiers=classifiers,
    #packages=find_packages(),
    py_modules=['pijavski'],
    package_dir={'':'src'},
    install_requires=['cffi>=1.0.0'],
    setup_requires=['cffi>=1.0.0'],
    cffi_modules=['./src/pij_build.py:ffibuilder'],
)
