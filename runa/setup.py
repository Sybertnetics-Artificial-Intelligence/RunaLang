#!/usr/bin/env python3
"""
Setup configuration for Runa - AI-First Universal Translation Platform

This setup file allows for easy development installation and testing.
"""

from setuptools import setup, find_packages

setup(
    name="runa",
    version="0.1.0",
    description="AI-First Universal Translation Platform with Natural Language Syntax",
    long_description=open("runa/README.md").read(),
    long_description_content_type="text/markdown",
    author="Sybertnetics",
    python_requires=">=3.8",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=[
        # No external dependencies yet - pure Python implementation
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "runa=runa.cli:main",  # Future CLI entry point
        ],
    },
    project_urls={
        "Documentation": "https://github.com/sybertnetics/runa",
        "Source": "https://github.com/sybertnetics/runa",
        "Tracker": "https://github.com/sybertnetics/runa/issues",
    },
) 