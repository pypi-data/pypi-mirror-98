# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 10:44:17 2021

@author: hamza_shoukat
"""

import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name = "calche",
        version = "0.0.1",
        description='Python Distribution Utilities',
        author='Hamza shoukat',
        author_email='hamza_shoukat@diyatech.com',
        long_description = long_description,
        long_description_context_type = "text/markdown",
        url='https://github.com/hamzashoukat94/pythonAPP',
        packages=setuptools.find_packages(),
        python_requires = ">=3.6",
        classifier = [
                "Programming language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",]
        )