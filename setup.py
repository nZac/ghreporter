#!/usr/bin/env python
from setuptools import setup

with open(".version") as fh:
    version = fh.readline()

with open("README.rst") as fh:
    long_description = fh.read()

setup(
    name="ghreport",
    version=version,
    description="Report on statistics from Github and Github Enterprise.",
    long_description=long_description,
    author="Nicholas Zaccardi",
    author_email="nicholas.zaccardi@ndus.edu",
    url="https://github.com/nZac/ghreport/",
    packages=[
        "src/ghreport",
        "src/gh"
    ],
    install_requires=[
        "requests==2.3.0"
    ],
    license="Apache 2.0",
    classifiers=[]
)
