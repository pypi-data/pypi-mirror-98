#!/usr/bin/env python3

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

requirements = []
with open(path.join(here, "requirements.txt"), "r") as infile:
    requirements = [line for line in infile.read().split("\n") if line]

setup(
    name="idling_at_home",
    version="2021.0",
    description="Start Folding&Home when your computer is idle.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NFJones/idling-at-home",
    author="Neil F Jones",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="folding home folding&home",
    packages=["idling_at_home"],
    python_requires=">=3.5, <4",
    entry_points={"console_scripts": ["idling-at-home = idling_at_home.main:main"]},
    install_requires=requirements,
)
