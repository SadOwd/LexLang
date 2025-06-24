"""
LexLang - Setup configuration
Installation et configuration du package LexLang
"""

from setuptools import setup, find_packages
import os

# Lecture du README pour la description longue
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Lecture des requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="lexlang",
    version="1.0.0",
    author="SadOwd",
    author_email="lexlang.project@gmail.com",
    description="Base lexicale publique multilingue pour français et langues africaines",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/SadOwd/LexLang",
    project_urls={
        "Bug Tracker": "https://github.com/SadOwd/LexLang/issues",
        "Documentation": "https://github.com/SadOwd/LexLang/docs",
        "Source Code": "https://github.com/SadOwd/LexLang",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: French",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.2",
            "pytest-cov>=4.1.0",
            "pytest-flask>=1.2.0",
            "black>=23.9.1",
            "flake8>=6.1.0",
            "mypy>=1.6.0",
        ],
        "ml": [
            "scikit-learn>=1.3.1",
            "transformers>=4.34.0",
            "torch>=2.0.0",
        ],
        "production": [
            "gunicorn>=21.2.0",
            "redis>=5.0.0",
            "psycopg2-binary>=2.9.7",
        ]
    },
    entry_points={
        "console_scripts": [
            "lexlang-api=src.api.lexical_api:main",
            "lexlang-import=src.utils.data_manager:main",
            "lexlang-setup=scripts.setup_database:main",
        ],
    },
    include_package_data=True,
    package_data={
        "lexlang": [
            "data/raw/**/*",
            "config/*.yaml",
            "config/*.json",
        ],
    },
    zip_safe=False,
    keywords=[
        "nlp",
        "linguistics",
        "african-languages",
        "french",
        "lexical-database",
        "tokenization",
        "multilingual",
        "open-source",
        "api",
        "text-processing"
    ],
)
