#!/usr/bin/env python3
"""
Setup script for Runa Programming Language
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, '..', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read version from version file
def get_version():
    version_file = os.path.join(this_directory, 'src', 'runa', '_version.py')
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            exec(f.read())
            return locals()['__version__']
    return '0.1.0'

setup(
    name='runa-lang',
    version=get_version(),
    author='SyberSuite AI Development Team',
    author_email='dev@sybersuite.ai',
    description='Runa Programming Language - Natural language programming for AI agents',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sybersuite/runa',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.11',
    install_requires=[
        'typing-extensions>=4.7.1',
        'dataclasses>=0.8',
        'enum34>=1.1.10; python_version<"3.4"',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.7.0',
            'flake8>=6.0.0',
            'mypy>=1.5.1',
            'sphinx>=7.1.2',
        ],
        'ai': [
            'torch>=2.0.0',
            'transformers>=4.30.0',
            'neo4j>=5.10.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'runa=runa.cli:main',
            'runa-repl=runa.repl:main',
            'runa-compile=runa.compiler:main',
            'runa-vm=runa.vm:main',
        ],
    },
    include_package_data=True,
    package_data={
        'runa': [
            'stdlib/*.runa',
            'examples/*.runa',
            'grammar/*.ebnf',
        ],
    },
    zip_safe=False,
) 