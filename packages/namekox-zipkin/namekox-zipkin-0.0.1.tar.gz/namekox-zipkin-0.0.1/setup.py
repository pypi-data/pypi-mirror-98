#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import unicode_literals


import os


from codecs import open
from setuptools import find_packages, setup


curdir = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(curdir, 'READIT.md'), 'rb', 'utf-8').read()

setup(
    name='namekox-zipkin',
    version='0.0.1',
    description='namekox zipkin',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='forcemain',
    url='https://forcemain.github.io/',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=["namekox-core", "py_zipkin==0.20.2"],
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)