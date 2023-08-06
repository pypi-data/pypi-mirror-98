#!/usr/bin/env python

from __future__ import absolute_import
import sys

# from distutils.core import setup
from setuptools import setup, find_packages
from os import path
import io
from os.path import join, dirname

sys.path.append(join(dirname(__file__), "EyesLibraryExtended"))

exec(compile(open("EyesLibraryExtended/version.py").read(), "EyesLibraryExtended/version.py", "exec"))

with io.open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="robotframework-eyeslibraryextended",
    version=__version__,
    description="Visual verification testing library for Robot Framework using Applitool python SDK eye-selenium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jis Thomas",
    author_email="<jisthomas@gmail.com>",
    url="https://github.com/JisThomas14/EyesLibraryExtended",
    license="Apache License 2.0",
    keywords="robotframework testing testautomation eyes-selenium selenium appium visual-verification ultrafastgrid classicrunner applitool",
    platforms="any",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Framework :: Robot Framework :: Library",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
    ],
    install_requires=[
        "robotframework > 3.0, < 4",
        "eyes-selenium >= 4.1.25",
        "six > 1.0.0, < 2",
        "robotframework-seleniumlibrary",
        "robotframework-appiumlibrary",
    ],
    packages=find_packages(exclude=["tests", "docs"]),
)
