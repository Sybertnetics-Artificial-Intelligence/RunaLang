"""
Standard Library for Runa Programming Language.

The Runa standard library provides core functionality for all Runa programs,
organized into the following modules:
- core: Essential types and operations
- io: Input/output operations
- collections: Data structures and algorithms
- math: Mathematical functions and utilities
"""

from . import core
from . import io
from . import collections
from . import math

__all__ = [
    'core',
    'io',
    'collections',
    'math'
] 