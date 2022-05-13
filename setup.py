#! /usr/bin/env python

import os
from setuptools import setup, find_packages
import sys


PACKAGE = "mkdocs-databio"
REQDIR = "requirements"


def read_reqs(reqs_name):
    deps = []
    with open(os.path.join(REQDIR, "requirements-{}.txt".format(reqs_name)), 'r') as f:
        for l in f:
            if not l.strip():
                continue
            #deps.append(l.split("=")[0].rstrip("<>"))
            deps.append(l)
    return deps

extra = {}

extra["install_requires"] = read_reqs("all")

with open("mkdocs_plugin/_version.py", 'r') as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")


setup(
    name=PACKAGE,
    version=version,
    url='http://github.com/databio/mkdocs-databio/',
    license='BSD2',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    description='Databio theme for MkDocs',
    author='Nathan Sheffield',
    author_email='nathan@code.databio.org',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=2.7.9,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    entry_points={
        'mkdocs.themes': [
            'databio = mkdocs_databio',
        ],
        'mkdocs.plugins': [
            'databio = mkdocs_plugin.plugin:AutoDocumenter',
        ]
    },
    zip_safe=False,
    **extra
)
