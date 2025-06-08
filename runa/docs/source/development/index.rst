Development Guide
===============

This section provides information for developers who want to contribute to the Runa programming language.

.. toctree::
   :maxdepth: 2
   
   contributing
   architecture
   roadmap
   testing
   tools

Getting Started
-------------

To get started with development, follow these steps:

1. Set up your development environment as described in :doc:`../installation`
2. Read the :doc:`contributing` guide to understand the development workflow
3. Explore the :doc:`architecture` to get a high-level overview of the codebase
4. Check the :doc:`roadmap` to see what needs to be implemented
5. Learn about the :doc:`testing` framework and how to write tests
6. Discover the available :doc:`tools` for development

Development Philosophy
--------------------

Runa follows these core development principles:

1. **Production-First Development**: Every line of code must be production-ready. No temporary, mock, placeholder, or "TODO" code.
2. **Zero Redundancy Principle**: Reuse existing functions and components whenever possible. Create new code only when no suitable existing solution exists.
3. **Current Functionality Preservation**: All existing system capabilities must be maintained during development.

Code Quality Standards
--------------------

- **Full Implementation**: Every function, class, and module must be completely implemented.
- **Error Handling**: Comprehensive error handling for all edge cases.
- **Input Validation**: Validate all inputs and parameters.
- **Documentation**: Complete docstrings and inline comments.
- **Testing**: Unit tests for all new code (95%+ coverage target). 