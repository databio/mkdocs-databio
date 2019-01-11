from setuptools import setup, find_packages
import sys


VERSION = '1.0.1'

# 2to3
if sys.version_info >= (3, ):
    extra["use_2to3"] = True


setup(
    name="mkdocs-databio",
    version=VERSION,
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
    install_requires=['mkdocs>=1.0'],
    python_requires='>=2.7.9,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    entry_points={
        'mkdocs.themes': [
            'databio = mkdocs_databio',
        ],
        'mkdocs.plugins': [
            'databio = mkdocs_plugin.plugin:AutoDocumenter',
        ]
    },
    zip_safe=False
)
