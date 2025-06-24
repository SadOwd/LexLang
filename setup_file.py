#!/usr/bin/env python

# -*- coding: utf-8 -*-

“”“Setup script for LexLang.”””

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(**file**).parent.resolve()

# Get the long description from the README file

long_description = (here / “README.md”).read_text(encoding=“utf-8”)

# Read requirements

def read_requirements(filename):
with open(filename, ‘r’, encoding=‘utf-8’) as f:
return [line.strip() for line in f if line.strip() and not line.startswith(’#’)]

requirements = read_requirements(‘requirements.txt’)

setup(
name=“lexlang”,
version=“0.1.0”,
author=“LexLang Contributors”,
author_email=“contact@lexlang.org”,
description=“Base lexicale éwé pour le traitement automatique du langage naturel”,
long_description=long_description,
long_description_content_type=“text/markdown”,
url=“https://github.com/votre-username/LexLang”,
project_urls={
“Bug Reports”: “https://github.com/votre-username/LexLang/issues”,
“Source”: “https://github.com/votre-username/LexLang”,
“Documentation”: “https://github.com/votre-username/LexLang/docs”,
},
packages=find_packages(exclude=[“tests”, “tests.*”]),
classifiers=[
“Development Status :: 3 - Alpha”,
“Intended Audience :: Developers”,
“Intended Audience :: Science/Research”,
“Topic :: Scientific/Engineering :: Artificial Intelligence”,
“Topic :: Text Processing :: Linguistic”,
“License :: OSI Approved :: MIT License”,
“Programming Language :: Python :: 3”,
“Programming Language :: Python :: 3.8”,
“Programming Language :: Python :: 3.9”,
“Programming Language :: Python :: 3.10”,
“Programming Language :: Python :: 3.11”,
“Natural Language :: French”,
“Natural Language :: English”,
],
keywords=“ewe, nlp, dictionary, african-languages, natural-language-processing, tokenization, pos-tagging”,
python_requires=”>=3.8, <4”,
install_requires=requirements,
extras_require={
“dev”: [
“pytest>=6.2.0”,
“pytest-cov>=2.12.0”,
“black>=21.0.0”,
“flake8>=3.9.0”,
“mypy>=0.910”,
],
“docs”: [
“mkdocs>=1.2.0”,
“mkdocs-material>=7.0.0”,
],
“api”: [
“fastapi>=0.68.0”,
“uvicorn>=0.15.0”,
],
},
entry_points={
“console_scripts”: [
“lexlang=lexlang.cli:main”,
],
},
include_package_data=True,
package_data={
“lexlang”: [
“data/dictionaries/*.json”,
“data/morphology/*.json”,
“data/phonetics/*.json”,
“data/corpus/*/*.txt”,
],
},
zip_safe=False,
)