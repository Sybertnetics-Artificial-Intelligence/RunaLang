#!/usr/bin/env python3
"""
Setup script for the Runa programming language.

This script defines the package metadata and dependencies required to install
and run the Runa language.
"""

from setuptools import setup, find_packages
import os
import sys

# Read the version from the core module
about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "runa", "src", "core", "__init__.py"), encoding="utf-8") as f:
    exec(f.read(), about)

# Read the long description from README.md
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Define the required dependencies
install_requires = [
    "typing-extensions>=4.0.0",
    "colorama>=0.4.4",
]

# Define development dependencies
dev_requires = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "sphinx>=6.0.0",
    "sphinx-rtd-theme>=1.0.0",
]

# Define documentation dependencies
docs_requires = [
    "sphinx>=6.0.0",
    "sphinx-rtd-theme>=1.0.0",
    "sphinx-autodoc-typehints>=1.20.0",
]

# Check if we're running Python 3.11 or newer
if sys.version_info < (3, 11):
    sys.exit("Runa requires Python 3.11 or newer")

setup(
    name="runa-lang",
    version=about["__version__"],
    description="A natural language programming language for human-AI collaboration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sybertnetics",
    author_email="info@sybertnetics.com",
    url="https://github.com/sybertnetics/runa",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "runa=runa.src.cli.main:main",
        ],
    },
    python_requires=">=3.11",
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
        "docs": docs_requires,
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
    ],
    keywords="programming language, natural language, ai, compiler",
    license="MIT",
) 