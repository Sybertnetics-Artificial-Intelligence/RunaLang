Syntax
======

Basic Syntax
-----------

Runa's syntax is designed to resemble natural language while maintaining the precision needed for computational execution. This makes it both easy to read for humans and easy to generate for AI systems.

Comments
-------

Comments in Runa are denoted by the hash symbol (#) and continue until the end of the line:

.. code-block:: text

   # This is a comment
   Let x be 42  # This is an inline comment

Identifiers
----------

Identifiers in Runa can be single words or multiple words separated by spaces:

.. code-block:: text

   Let user name be "John"  # "user name" is a multi-word identifier
   Let age be 30            # "age" is a single-word identifier

Indentation
----------

Runa uses indentation to denote blocks of code, similar to Python. Consistent indentation is required:

.. code-block:: text

   If age is greater than 18:
       Display "You are an adult"  # Indented block
       Let status be "adult"       # Same indentation level
   Otherwise:
       Display "You are a minor"   # Indented block in the else clause

Statements
---------

Each statement in Runa typically occupies a single line, though complex statements may span multiple lines with proper indentation:

.. code-block:: text

   Let greeting be "Hello, World!"  # A simple statement
   
   Process called "Calculate Total" that takes price and tax rate:
       Let tax amount be price multiplied by tax rate
       Return price plus tax amount
   # A complex statement spanning multiple lines

Literals
-------

Runa supports various literal types:

.. code-block:: text

   Let string value be "Hello"       # String literal with double quotes
   Let another string be 'World'     # String literal with single quotes
   Let number be 42                  # Integer literal
   Let float number be 3.14          # Floating-point literal
   Let is valid be true              # Boolean literal (true)
   Let is invalid be false           # Boolean literal (false)
   Let empty value be null           # Null literal
   Let alternative empty be none     # Alternative null literal

Operators
--------

Runa uses natural language phrases as operators:

.. code-block:: text

   Let sum be a plus b               # Addition
   Let difference be a minus b       # Subtraction
   Let product be a multiplied by b  # Multiplication
   Let quotient be a divided by b    # Division
   
   Let is adult be age is greater than 18  # Comparison
   Let is same be name is equal to "John"  # Equality check
   Let is different be x is not equal to y # Inequality check
   
   Let both valid be a and b         # Logical AND
   Let either valid be a or b        # Logical OR

Punctuation
----------

Runa uses minimal punctuation:

- Colons (`:`) to denote the beginning of a block
- Commas (`,`) to separate items in lists
- Parentheses (`()`) for grouping and function calls
- Brackets (`[]`) for indexing
- Braces (`{}`) for dictionary literals

Line Continuation
---------------

Long expressions can be continued on the next line with proper indentation:

.. code-block:: text

   Let long expression be first part plus
       second part plus
       third part 