from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.7.2'
DESCRIPTION = 'Simple File Configuration Parse. Python alternative to creating custom save/config files!'
LONG_DESCRIPTION = 'Simple File Configuration Parse. Export or Import data easily. Python alternative to creating custom save/config files, and export any data to disk quickly and smoothly!'

# Setting up
setup(
    name="sfcparse",
    version=VERSION,
    author="aaronater10",
    author_email="<admin@dunnts.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'ini file', 'config', 'text file', 'cfg', 'conf', 'save file', 'config file', 'sfcparse', 'aaronater10', 'db', 'database', 'simple', 'configuration', 'alternative', 'data', 'import'],
    license = 'MIT',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)