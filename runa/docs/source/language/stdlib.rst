Standard Library
===============

The Runa Standard Library provides core functionality for all Runa programs.
It is organized into modules that offer essential operations and data structures.

Core Module
----------

The Core module provides essential types and operations used by all Runa programs.

Builtins
~~~~~~~~

Basic operations available to all Runa programs:

.. code-block:: runa

   # Type operations
   type(value)               # Returns the type of a value
   is_null(value)            # Checks if value is null
   is_boolean(value)         # Checks if value is a boolean
   is_number(value)          # Checks if value is a number
   is_string(value)          # Checks if value is a string
   is_list(value)            # Checks if value is a list
   is_dictionary(value)      # Checks if value is a dictionary
   is_function(value)        # Checks if value is a function
   
   # Conversion functions
   to_boolean(value)         # Converts value to boolean
   to_integer(value)         # Converts value to integer
   to_float(value)           # Converts value to float
   to_string(value)          # Converts value to string
   
   # Collection operations
   length(collection)        # Returns the length of a collection
   keys(dictionary)          # Returns the keys of a dictionary
   values(dictionary)        # Returns the values of a dictionary
   entries(dictionary)       # Returns the entries of a dictionary as [key, value] pairs
   has_key(dictionary, key)  # Checks if dictionary has a key
   
   # String operations
   split(string, delimiter)  # Splits string by delimiter
   join(list, separator)     # Joins list elements with separator
   trim(string)              # Removes whitespace from start/end of string
   starts_with(string, prefix) # Checks if string starts with prefix
   ends_with(string, suffix) # Checks if string ends with suffix
   
   # Object operations
   has_property(object, name) # Checks if object has a property
   get_property(object, name) # Gets object property
   set_property(object, name, value) # Sets object property

Error Handling
~~~~~~~~~~~~~

Error types and error handling utilities:

.. code-block:: runa

   # Error creation
   create_error(message)
   create_type_error(message, expected_type, actual_type)
   create_value_error(message, invalid_value)
   create_reference_error(message, reference_name)
   create_syntax_error(message, source, line, column)
   create_range_error(message, value, min, max)
   create_io_error(message, operation, path)
   create_import_error(message, module_name)
   create_assertion_error(message, expression)
   create_not_implemented_error(message, feature)
   
   # Error utilities
   throw(error)              # Throws an error
   assert(condition, message) # Asserts a condition
   error_to_string(error)    # Converts error to string
   format_stack_trace(error) # Formats the stack trace of an error
   
   # Helper assertions
   assert_type(value, expected_type, message)
   assert_range(value, min, max, message)
   assert_not_null(value, message)

Try-catch blocks are used to handle errors:

.. code-block:: runa

   Try:
       # Code that might throw an error
       Let result = potentially_dangerous_operation()
   Catch error:
       # Handle the error
       Print("An error occurred: " + error_to_string(error))
       # Do recovery operations

Module System
~~~~~~~~~~~~

Module loading and namespace management:

.. code-block:: runa

   # Module operations
   load_module(module_path)
   import_module(module_path)
   import_from(module_path, symbols)
   register_exports(exports)
   get_module_name()
   get_module_path()
   
   # Namespace management
   create_namespace(name, parent)
   add_to_namespace(namespace, name, value)
   get_from_namespace(namespace, name)
   resolve_name(name, namespace)

Import and export syntax:

.. code-block:: runa

   # Importing a module
   Import module_name
   
   # Importing specific symbols
   From module_name Import symbol1, symbol2
   
   # Exporting symbols
   export {
       function1,
       function2,
       constant1
   }

IO Module
--------

The IO module provides input/output operations for files and streams.

File Operations
~~~~~~~~~~~~~

Functions for working with files:

.. code-block:: runa

   # Reading files
   read_file(path)           # Reads entire file as string
   read_file_binary(path)    # Reads entire file as binary data
   read_lines(path)          # Reads file as list of lines
   
   # Writing files
   write_file(path, content)  # Writes string to file
   write_file_binary(path, data) # Writes binary data to file
   append_file(path, content) # Appends string to file
   
   # File management
   file_exists(path)         # Checks if file exists
   delete_file(path)         # Deletes a file
   rename_file(old_path, new_path) # Renames a file
   copy_file(source, target) # Copies a file
   
   # Directory operations
   create_directory(path)    # Creates a directory
   list_directory(path)      # Lists directory contents
   is_directory(path)        # Checks if path is a directory

Stream Operations
~~~~~~~~~~~~~~

Functions for working with streams:

.. code-block:: runa

   # Text streams
   open_text_stream(path, mode) # Opens a text stream
   read_line(stream)         # Reads a line from text stream
   write_line(stream, text)  # Writes a line to text stream
   
   # Binary streams
   open_binary_stream(path, mode) # Opens a binary stream
   read_bytes(stream, count) # Reads bytes from binary stream
   write_bytes(stream, data) # Writes bytes to binary stream
   
   # Network streams
   open_tcp_connection(host, port) # Opens a TCP connection
   
   # Stream management
   close_stream(stream)      # Closes a stream
   flush_stream(stream)      # Flushes a stream's buffer

Collections Module
---------------

The Collections module provides data structures and algorithms.

List Operations
~~~~~~~~~~~~~

Functions for working with lists:

.. code-block:: runa

   # List creation and manipulation
   create_list(size, init_value) # Creates a list of given size
   concat(list1, list2)      # Concatenates two lists
   slice(list, start, end)   # Returns a slice of a list
   
   # List searching and filtering
   find(list, predicate)     # Finds first element matching predicate
   filter(list, predicate)   # Filters list by predicate
   map(list, transform)      # Maps list elements using transform function
   reduce(list, reducer, initial) # Reduces list using reducer function
   
   # List sorting
   sort(list)                # Sorts a list in-place
   sorted(list)              # Returns a sorted copy of a list
   reverse(list)             # Reverses a list in-place

Dictionary Operations
~~~~~~~~~~~~~~~~~~

Functions for working with dictionaries:

.. code-block:: runa

   # Dictionary creation and manipulation
   create_dict()             # Creates an empty dictionary
   merge(dict1, dict2)       # Merges two dictionaries
   
   # Dictionary iteration
   map_dict(dict, transform) # Maps dictionary entries
   filter_dict(dict, predicate) # Filters dictionary entries

Advanced Collections
~~~~~~~~~~~~~~~~~

Specialized data structures:

.. code-block:: runa

   # Set operations
   create_set()              # Creates an empty set
   add(set, value)           # Adds value to set
   remove(set, value)        # Removes value from set
   contains(set, value)      # Checks if set contains value
   union(set1, set2)         # Returns union of two sets
   intersection(set1, set2)  # Returns intersection of two sets
   difference(set1, set2)    # Returns difference of two sets
   
   # Queue operations
   create_queue()            # Creates an empty queue
   enqueue(queue, value)     # Adds value to queue
   dequeue(queue)            # Removes and returns value from queue
   peek(queue)               # Returns value from queue without removing
   
   # Priority queue operations
   create_priority_queue()   # Creates an empty priority queue
   enqueue_with_priority(queue, value, priority) # Adds with priority
   dequeue_highest(queue)    # Removes and returns highest priority

Math Module
---------

The Math module provides mathematical functions and utilities.

Constants
~~~~~~~~

Mathematical constants:

.. code-block:: runa

   PI                        # π (3.14159...)
   E                         # e (2.71828...)
   TAU                       # τ (6.28318...)
   PHI                       # φ (1.61803...)
   SQRT2                     # √2 (1.41421...)
   INFINITY                  # ∞
   NAN                       # Not a Number

Arithmetic Functions
~~~~~~~~~~~~~~~~~

Basic arithmetic operations:

.. code-block:: runa

   abs(x)                    # Absolute value
   min(x, y)                 # Minimum of x and y
   max(x, y)                 # Maximum of x and y
   floor(x)                  # Largest integer not greater than x
   ceil(x)                   # Smallest integer not less than x
   round(x)                  # Rounds x to nearest integer
   trunc(x)                  # Truncates x to integer
   sqrt(x)                   # Square root of x
   pow(x, y)                 # x raised to power y
   exp(x)                    # e raised to power x
   log(x)                    # Natural logarithm of x
   log10(x)                  # Base-10 logarithm of x
   log2(x)                   # Base-2 logarithm of x

Trigonometric Functions
~~~~~~~~~~~~~~~~~~~~

Trigonometric operations:

.. code-block:: runa

   sin(x)                    # Sine of x
   cos(x)                    # Cosine of x
   tan(x)                    # Tangent of x
   asin(x)                   # Arc sine of x
   acos(x)                   # Arc cosine of x
   atan(x)                   # Arc tangent of x
   atan2(y, x)               # Arc tangent of y/x
   degrees(x)                # Converts radians to degrees
   radians(x)                # Converts degrees to radians

Statistical Functions
~~~~~~~~~~~~~~~~~~

Statistical operations:

.. code-block:: runa

   mean(list)                # Arithmetic mean of list
   median(list)              # Median of list
   mode(list)                # Mode of list
   variance(list)            # Variance of list
   std_dev(list)             # Standard deviation of list
   percentile(list, p)       # pth percentile of list

Random Functions
~~~~~~~~~~~~~

Random number generation:

.. code-block:: runa

   random()                  # Random number between 0 and 1
   random_int(min, max)      # Random integer between min and max
   random_float(min, max)    # Random float between min and max
   random_choice(list)       # Random element from list
   random_shuffle(list)      # Shuffles list in-place 