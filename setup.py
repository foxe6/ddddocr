#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/2 15:41
# @Author  : sml2h3
# @Site    :
# @File    : setup.py
# @Software: PyCharm
# @Description:

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ddddocrgpu",
    version="1.4.8",
    author="sml2h3",
    description="带带弟弟OCR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/foxe6/ddddocrgpu",
    packages=find_packages(where='.', exclude=(), include=('*',)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'onnxruntime-gpu', 'Pillow', 'opencv-python-headless'],
    python_requires='<3.11',
    include_package_data=True,
    install_package_data=True,
)
