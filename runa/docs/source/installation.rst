Installation
============

Requirements
-----------

Runa requires Python 3.11 or higher. The following dependencies are also required:

- pytest (for running tests)
- pytest-cov (for test coverage)
- black (for code formatting)
- flake8 (for code linting)
- mypy (for type checking)
- sphinx (for documentation generation)
- sphinx-rtd-theme (for documentation theme)

Installing from PyPI
-------------------

Once the package is available on PyPI, you can install it using pip:

.. code-block:: bash

   pip install runa-lang

For development, you can install additional dependencies:

.. code-block:: bash

   pip install runa-lang[dev]

Installing from Source
--------------------

To install from source, clone the repository and install using pip:

.. code-block:: bash

   git clone https://github.com/sybertnetics/runa.git
   cd runa
   pip install -e .

For development, install with development dependencies:

.. code-block:: bash

   pip install -e ".[dev]"

Verifying Installation
--------------------

To verify that Runa is installed correctly, you can run the following command:

.. code-block:: bash

   python -c "import runa.src.core; print(runa.src.core.__version__)"

You can also run the tests to ensure everything is working correctly:

.. code-block:: bash

   pytest -xvs

Using the Runa CLI
----------------

Runa comes with a command-line interface (CLI) that you can use to run Runa programs:

.. code-block:: bash

   # Tokenize a Runa file (currently supported)
   runa tokenize examples/hello_world.runa
   
   # Run a Runa program (coming soon)
   runa run examples/hello_world.runa 