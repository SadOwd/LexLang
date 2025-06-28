#!/usr/bin/env python3
"""Setup script for LexLang package."""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="lexlang",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="LexLang Team",
    author_email="contact@lexlang.org",
    description="Advanced NLP toolkit for Ewe language processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lexlang/lexlang",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "black>=21.9.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
            "jupyter>=1.0.0"
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "lexlang=lexlang.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "lexlang": ["data/**/*", "configs/**/*"],
    },
)
