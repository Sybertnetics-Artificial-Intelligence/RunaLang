Welcome to Runa Programming Language's documentation!
================================================

Runa is a revolutionary programming language designed to bridge human thought patterns with machine execution. Named after Norse runes that encoded knowledge and meaning, Runa features pseudocode-like syntax that resembles natural language while maintaining the precision needed for computational execution.

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   introduction
   installation
   language/index
   api/index
   examples/index
   grammar/index
   development/index

Core Features
------------

- **Natural Language Syntax**: Code that reads like English while maintaining computational precision
- **AI-Native Design**: Built specifically for AI systems to reason with and generate
- **Knowledge Integration**: Direct interface with knowledge graphs and semantic systems
- **Universal Code Generation**: Transpile to multiple target languages (Python, Java, C++, etc.)
- **Type System**: Strong, static typing with powerful type inference

Getting Started
--------------

.. code-block:: bash

   # Once we have a package ready
   pip install runa-lang

Basic Example
------------

.. code-block:: text

   # This is a Runa program
   Let user name be "Alex"
   Let user age be 28

   If user age is greater than 21:
       Display user name with message "is an adult"
   Otherwise:
       Display user name with message "is underage"

   Process called "Calculate Total Price" that takes items and tax rate:
       Let subtotal be the sum of all prices in items
       Let tax amount be subtotal multiplied by tax rate
       Return subtotal plus tax amount

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 