#! /usr/bin/env python3

from setuptools import setup

setup(
    name="TopSim",
    packages=["topsim"],
    scripts=["topsim-cli"],
    version="0.1",
    description="Search the most similar strings against the query in Python 3.",
    author="Chuancong Gao",
    author_email="chuancong@gmail.com",
    url="https://github.com/chuanconggao/TopSim",
    download_url="https://github.com/chuanconggao/TopSim/tarball/0.1",
    keywords=[
        "similarity search",
        "string"
    ],
    license="MIT",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">= 3",
    install_requires=[
        "docopt >= 0.6.2",
    ]
)
