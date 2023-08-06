# -*- coding: utf-8 -*-
# @Time    : 2021/3/10 1:34 下午
# @Author  : john
# @Site    : 
# @File    : setup.py
# @Software: PyCharm
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="pcacode",
    version="1.0.0",
    author="john",
    author_email="john19940404@live.com",
    description="这是一个从文本中找地名信息和地区码的库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/YHjohn/pcacode",

    packages=setuptools.find_namespace_packages(
                     include=["pcacode", "pcacode.*"]),
    install_requires = ["openpyxl"],
    include_package_data=True ,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)