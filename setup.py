from setuptools import setup, find_packages

VERSION = '1.0.1'

setup(
    name="mkdocs-databio",
    version=VERSION,
    url='http://github.com/databio/mkdocs-databio/',
    license='BSD',
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
            'dbp = mkdocs_plugin.plugin:AutoDocumenter',
        ]
    },
    zip_safe=False
)
