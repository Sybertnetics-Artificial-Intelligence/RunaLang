EBNF Notation
============

The Runa grammar is specified using Extended Backus-Naur Form (EBNF). This page explains the notation used in the grammar.

Notation Guide
------------

The grammar uses the following notation:

- ``::=`` means "is defined as"
- ``|`` means "or" (alternative)
- ``+`` means "one or more occurrences"
- ``*`` means "zero or more occurrences"
- ``?`` means "zero or one occurrence" (optional)
- ``( )`` groups items together
- ``[ ]`` represents a character class
- ``" "`` encloses terminal strings (literals)
- ``/* */`` indicates comments

Examples
-------

Here are some examples to illustrate the notation:

- ``Statement ::= Declaration | Assignment`` means a Statement is either a Declaration or an Assignment.
- ``ExpressionList ::= Expression ("," Expression)*`` means an ExpressionList is an Expression followed by zero or more occurrences of a comma and another Expression.
- ``OptionalType ::= ("(" Identifier ")")?`` means an OptionalType is either nothing or an Identifier enclosed in parentheses.
- ``StringLiteral ::= "'" [^']* "'" | "\"" [^"]* "\""`` means a StringLiteral is either a sequence of characters enclosed in single quotes or a sequence of characters enclosed in double quotes.

Special Productions
-----------------

The grammar includes special productions for handling indentation:

- ``INDENT`` represents an increase in indentation level
- ``DEDENT`` represents a decrease in indentation level
- ``NEWLINE`` represents a newline character with consistent indentation

These productions are not represented by specific tokens in the source code but are inserted by the lexer to help the parser handle indentation-based block structure. 