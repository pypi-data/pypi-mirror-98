from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Librería para crear formularios en HTML desde Python.'
LONG_DESCRIPTION = 'Librería para crear formularios en HTML desde Python con funciones encadenadas'

# Setting up
setup(
    name="Formpy",
    version=VERSION,
    author="Diego Dueñez (diegoduenez)",
    author_email="diegoduenez03@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'html', 'forms', 'python forms', 'python html', 'forms generate'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)