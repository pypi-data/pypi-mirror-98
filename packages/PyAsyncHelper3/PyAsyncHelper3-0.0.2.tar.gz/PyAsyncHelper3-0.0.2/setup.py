# -*- coding: utf-8 -*-
# @Time    :
# @Author  : shellvv
# @Site    :
# @File    : setup.py
# @Software: PyCharm
# @Description:

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "PyAsyncHelper3",
    version = "0.0.2",
    author = "shellvv",
    author_email = "shellvv@yeah.com",
    description ="dispatcher base on async",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "http://gitee.com/shellvv/PyAsyncHelper3",
    packages = setuptools.find_packages(),
    zip_safe=False,
    install_requires=[
            'pyhelper3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)