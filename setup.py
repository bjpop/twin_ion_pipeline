#!/usr/bin/env python

from setuptools import setup

setup(
    name='twin_ion',
    version='0.0.1',
    author='Bernie Pope',
    author_email='bjpope@unimelb.edu.au',
    packages=['src'],
    entry_points={
        'console_scripts': ['twin_ion = src.main:main']
    },
    url='https://github.com/bjpop/twin_ion',
    license='LICENSE.txt',
    description='XXX fix description.',
    long_description=open('README.md').read(),
    install_requires=[
        "ruffus == 2.6.3",
        "drmaa == 0.7.6",
        "PyYAML == 3.11"
    ],
)
