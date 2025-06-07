# Runa Formal Grammar Specification

This document defines the formal grammar for the Runa programming language using Extended Backus-Naur Form (EBNF).

## Notation

The grammar uses the following notation:
- `::=` means "is defined as"
- `|` means "or"
- `+` means "one or more occurrences"
- `*` means "zero or more occurrences"
- `?` means "zero or one occurrence"
- `( )` groups items together
- `[ ]` represents a character class
- `" "` encloses terminal strings
- `/* */` indicates comments

## Core Grammar

### Program Structure

```ebnf
/* Top-level program structure */
Program         ::= Statement+

/* Statements */
Statement       ::= Declaration
                  | Assignment
                  | Conditional
                  | Loop
                  | ProcessDefinition
                  | ReturnStatement
                  | DisplayStatement
                  | Block
                  | ImportStatement
                  | TryCatchStatement
                  | WhileLoop
                  | CommentLine
```

### Comments

```ebnf
CommentLine     ::= "#" [^\n]* "\n"
```

### Declarations and Assignments

```ebnf
/* Declarations */
Declaration     ::= "Let" Identifier OptionalType "be" Expression
                  | "Define" Identifier OptionalType "as" Expression
                  | "Define" Identifier OptionalType "as" "list" "containing" ExpressionList

/* Optional Type Annotation */
OptionalType    ::= ("(" Identifier ")")? 

/* Assignment */
Assignment      ::= "Set" Identifier "to" Expression
```

### Expressions

```ebnf
/* Basic expressions */
Expression      ::= Literal
                  | Identifier
                  | BinaryExpression
                  | FunctionCall
                  | ListExpression
                  | DictionaryExpression
                  | IndexAccess
                  | MemberAccess
                  | "(" Expression ")"
                  | "the" "sum" "of" "all" Identifier "in" Identifier
                  | "length" "of" Expression
                  | Expression "multiplied" "by" Expression
                  | Expression "plus" Expression
                  | Expression "minus" Expression
                  | Expression "divided" "by" Expression
                  | Expression "followed" "by" Expression
                  | Expression "at" "index" Expression
                  | "index" "of" Expression "in" Expression
                  | "convert" "to" Identifier "(" Expression ")"

/* Literals */
Literal         ::= StringLiteral
                  | NumberLiteral
                  | BooleanLiteral
                  | NullLiteral

StringLiteral   ::= '"' [^"]* '"'
                  | "'" [^']* "'"
NumberLiteral   ::= [0-9]+ ('.' [0-9]+)?
BooleanLiteral  ::= "true" | "false"
NullLiteral     ::= "null" | "none"

/* Binary expressions */
BinaryExpression ::= Expression Operator Expression

Operator        ::= "is" "greater" "than"
                  | "is" "less" "than"
                  | "is" "equal" "to"
                  | "is" "not" "equal" "to"
                  | "is" "greater" "than" "or" "equal" "to"
                  | "is" "less" "than" "or" "equal" "to"
                  | "and"
                  | "or"
                  | "contains"

/* Collections */
ListExpression  ::= "list" "containing" ExpressionList
                  | "[" ExpressionList "]"

ExpressionList  ::= Expression ("," Expression)* | ""

DictionaryExpression ::= "dictionary" "with" ":" INDENT KeyValuePair+ DEDENT
                      | "{" KeyValuePair ("," KeyValuePair)* "}"

KeyValuePair    ::= StringLiteral "as" Expression
                  | Identifier "as" Expression

/* Access Operations */
IndexAccess     ::= Identifier "[" Expression "]"
MemberAccess    ::= Identifier "." Identifier
```

### Control Structures

```ebnf
/* Control structures */
Conditional     ::= "If" Expression ":" Block ("Otherwise" "if" Expression ":" Block)* ("Otherwise" ":" Block)?

Loop            ::= "For" "each" Identifier "in" Expression ":" Block

WhileLoop       ::= "While" Expression ":" Block

Block           ::= INDENT Statement+ DEDENT
                  | "{" Statement+ "}"

/* Error handling */
TryCatchStatement ::= "Try" ":" Block "Catch" Identifier ":" Block
```

### Functions

```ebnf
/* Function definition and calls */
ProcessDefinition ::= "Process" "called" StringLiteral "that" "takes" ParameterList ("returns" "(" Identifier ")")? ":" Block

ParameterList   ::= Identifier OptionalType ("and" Identifier OptionalType)* 
                  | Identifier OptionalType ("," Identifier OptionalType)*
                  | ""

ReturnStatement ::= "Return" Expression

FunctionCall    ::= Identifier "with" NamedArguments
                  | Identifier "with" ":" INDENT NamedArguments DEDENT
                  | Identifier "(" ExpressionList ")"

NamedArguments  ::= NamedArgument ("and" NamedArgument)*
                  | NamedArgument (NEWLINE NamedArgument)*
                  | ""

NamedArgument   ::= Identifier "as" Expression
```

### Input/Output Operations

```ebnf
/* Display statement */
DisplayStatement ::= "Display" Expression ("with" "message" Expression)?

/* Input statement */
InputStatement  ::= "input" "with" "prompt" StringLiteral
```

### Modules

```ebnf
/* Import statements */
ImportStatement ::= "Import" "module" StringLiteral
                  | "Import" Identifier "from" "module" StringLiteral
```

### Identifiers

```ebnf
/* Identifiers */
Identifier      ::= [a-zA-Z_][a-zA-Z0-9_]* ("." [a-zA-Z_][a-zA-Z0-9_]*)*
                  | [a-zA-Z_][a-zA-Z0-9_]* (" " [a-zA-Z_][a-zA-Z0-9_]*)+
```

## AI-Specific Grammar Extensions

```ebnf
/* AI Model Definition */
ModelDefinition ::= "Define" "neural" "network" StringLiteral ":" ModelBlock

ModelBlock      ::= INDENT ModelStatement+ DEDENT

ModelStatement  ::= "Input" "layer" "accepts" Expression
                  | "Use" "convolutional" "layers" "starting" "with" NumberLiteral "filters"
                  | "Double" "filters" "at" "each" "downsampling"
                  | "Include" "residual" "connections"
                  | "Output" "layer" "has" NumberLiteral "classes" "with" Identifier "activation"

/* Training Configuration */
TrainingConfig  ::= "Configure" "training" "for" Identifier ":" TrainingBlock

TrainingBlock   ::= INDENT TrainingStatement+ DEDENT

TrainingStatement ::= "Use" "dataset" StringLiteral "with" Expression
                    | "Apply" Expression "for" "augmentation"
                    | "Use" Identifier "optimizer" "with" "learning" "rate" NumberLiteral
                    | "Train" "for" NumberLiteral "epochs" "or" "until" Expression
                    | "Save" "best" "model" "based" "on" Expression
```

## Knowledge Integration Extensions

```ebnf
/* Knowledge Query */
KnowledgeQuery  ::= "knowledge" "." "query" "(" StringLiteral ")"
                  | "knowledge" "." Identifier "(" ExpressionList ")"
```

## Special Productions

```ebnf
/* Whitespace handling */
INDENT          ::= /* increase of indentation level */
DEDENT          ::= /* decrease of indentation level */
NEWLINE         ::= /* newline character with consistent indentation */
```

## Examples

Here are some examples of Runa code that follows this grammar:

### Variable Declaration and Assignment
```
Let user name be "Alex"
Let user age be 28
Set user name to user name followed by " Smith"
```

### Control Flow
```
If user age is greater than 21:
    Display "Adult user"
Otherwise:
    Display "Minor user"
```

### Function Definition and Call
```
Process called "Calculate Area" that takes width and height:
    Return width multiplied by height

Let rectangle area be Calculate Area with width as 5 and height as 10
```

### List Operations
```
Let colors be list containing "red", "green", "blue"
For each color in colors:
    Display color
```

This formal grammar specification provides a comprehensive definition of the Runa programming language syntax.