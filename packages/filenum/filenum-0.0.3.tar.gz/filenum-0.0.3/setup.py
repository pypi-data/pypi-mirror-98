#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools,sys

if sys.version_info.major==2:
	with open("README.md", "r") as fh:
		long_description = fh.read()
else:
	with open("README.md", "r",encoding="utf8") as fh:
		long_description = fh.read()

setuptools.setup(
    name="filenum",
    version="0.0.3",
    author="Chen chuan",
    author_email="chenc224@163.com",
    description="file number in directory",
    long_description=long_description,
    long_description_content_type="text/markdown",
#   url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
#    python_requires='>=3.6',
    scripts=["filenum/filenum"],
)
