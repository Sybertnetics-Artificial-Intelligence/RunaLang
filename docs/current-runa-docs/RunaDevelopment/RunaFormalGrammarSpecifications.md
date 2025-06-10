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
                  | MatchStatement
                  | TypeDefinition
                  | AnnotationBlock
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
OptionalType    ::= ("(" TypeExpression ")")? 

/* Assignment */
Assignment      ::= "Set" Identifier "to" Expression
```

### Type System

```ebnf
/* Type Definitions */
TypeDefinition  ::= "Type" Identifier TypeParameters? "is" TypeExpression
                  | "Type" Identifier TypeParameters? "is" "Interface" "with" ":" INDENT InterfaceMembers DEDENT
                  | "Type" Identifier TypeParameters? "is" VariantDefinition

TypeParameters  ::= "[" TypeParameter ("," TypeParameter)* "]"

TypeParameter   ::= Identifier (":" TypeConstraint)?

TypeConstraint  ::= Identifier ("+" Identifier)*

TypeExpression  ::= BasicType
                  | GenericType
                  | UnionType
                  | IntersectionType
                  | FunctionType
                  | OptionalType

BasicType       ::= "Integer" | "Float" | "String" | "Boolean" | "Any" | "None"

GenericType     ::= Identifier "[" TypeExpression ("," TypeExpression)* "]"

UnionType       ::= TypeExpression ("OR" TypeExpression)+

IntersectionType ::= TypeExpression ("AND" TypeExpression)+

FunctionType    ::= "Function" "[" TypeExpression ("," TypeExpression)* "," TypeExpression "]"

OptionalType    ::= "Optional" "[" TypeExpression "]"

InterfaceMembers ::= InterfaceMember+

InterfaceMember ::= Identifier "as" TypeExpression

VariantDefinition ::= "|" VariantCase ("|" VariantCase)*

VariantCase     ::= Identifier ("with" ParameterList)?
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
                  | LambdaExpression
                  | PipelineExpression
                  | AsyncExpression
                  | AwaitExpression
                  | TypeAssertion

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
                  | "is" "of" "type"

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

/* Functional Programming */
LambdaExpression ::= "lambda" ParameterList ":" Expression

PipelineExpression ::= Expression "|>" Identifier

/* Asynchronous Programming */
AsyncExpression ::= "async" Expression

AwaitExpression ::= "await" Expression

/* Type Operations */
TypeAssertion   ::= Expression "as" TypeExpression
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

/* Pattern Matching */
MatchStatement  ::= "Match" Expression ":" INDENT MatchCase+ DEDENT

MatchCase       ::= "When" Pattern ("If" Expression)? ":" Block

Pattern         ::= LiteralPattern
                  | IdentifierPattern
                  | ListPattern
                  | DictionaryPattern
                  | VariantPattern
                  | TypePattern
                  | WildcardPattern

LiteralPattern  ::= Literal

IdentifierPattern ::= Identifier

ListPattern     ::= "list" "containing" PatternList
                  | "[" PatternList "]"

PatternList     ::= Pattern ("," Pattern)* | ""

DictionaryPattern ::= "dictionary" "with" ":" INDENT PatternKeyValuePair+ DEDENT
                    | "{" PatternKeyValuePair ("," PatternKeyValuePair)* "}"

PatternKeyValuePair ::= StringLiteral "as" Pattern

VariantPattern  ::= Identifier ("with" PatternParameterList)?

PatternParameterList ::= Identifier "as" Pattern ("and" Identifier "as" Pattern)*

TypePattern     ::= Identifier "of" "type" TypeExpression

WildcardPattern ::= "_"
```

### Functions

```ebnf
/* Function definition and calls */
ProcessDefinition ::= ("Async")? "Process" "called" StringLiteral TypeParameters? "that" "takes" ParameterList ("returns" TypeExpression)? ":" Block

ParameterList   ::= Identifier OptionalType ("and" Identifier OptionalType)* 
                  | Identifier OptionalType ("," Identifier OptionalType)*
                  | ""

ReturnStatement ::= "Return" Expression

FunctionCall    ::= Identifier TypeArguments? "with" NamedArguments
                  | Identifier TypeArguments? "with" ":" INDENT NamedArguments DEDENT
                  | Identifier "(" ExpressionList ")"

TypeArguments   ::= "[" TypeExpression ("," TypeExpression)* "]"

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
ImportStatement ::= "Import" "module" StringLiteral ("as" StringLiteral)?
                  | "Import" Identifier "from" "module" StringLiteral
```

### Identifiers

```ebnf
/* Identifiers */
Identifier      ::= [a-zA-Z_][a-zA-Z0-9_]* ("." [a-zA-Z_][a-zA-Z0-9_]*)*
                  | [a-zA-Z_][a-zA-Z0-9_]* (" " [a-zA-Z_][a-zA-Z0-9_]*)+
```

## AI-to-AI Communication Annotations

```ebnf
/* Annotation System */
AnnotationBlock ::= ReasoningBlock
                  | ImplementationBlock
                  | UncertaintyBlock
                  | KnowledgeReferenceBlock
                  | RequestClarificationBlock
                  | ExplainabilityBlock
                  | AbstractionLevelBlock
                  | VerificationBlock
                  | SymbolicBlock
                  | TaskSpecificationBlock
                  | ProgressTrackingBlock
                  | TranslationBlock
                  | ErrorHandlingProtocolBlock
                  | NaturalToFormalBlock

ReasoningBlock  ::= "@Reasoning" ":" INDENT FreeText DEDENT "@End_Reasoning"

ImplementationBlock ::= "@Implementation" ":" INDENT Statement+ DEDENT "@End_Implementation"

UncertaintyBlock ::= "@Uncertainty" ":" Expression ("with" "confidence" NumberLiteral)?

KnowledgeReferenceBlock ::= "@KnowledgeReference" ":" INDENT KnowledgeFields DEDENT "@End_KnowledgeReference"

KnowledgeFields ::= KnowledgeField+

KnowledgeField  ::= Identifier ":" Expression

RequestClarificationBlock ::= "@Request_Clarification" ":" INDENT FreeText DEDENT "@End_Request"

ExplainabilityBlock ::= "@Why" ":" StringLiteral

AbstractionLevelBlock ::= "@Abstraction_Level" ":" Identifier INDENT Statement+ DEDENT "@End_Abstraction_Level"

VerificationBlock ::= "@Verify" ":" INDENT VerifyStatement+ DEDENT "@End_Verify"

VerifyStatement ::= "Assert" Expression

SymbolicBlock   ::= "@Symbolic" ":" INDENT FreeText DEDENT "@End_Symbolic"

TaskSpecificationBlock ::= "@Task" ":" INDENT TaskFields DEDENT "@End_Task"

TaskFields      ::= TaskField+

TaskField       ::= Identifier ":" Expression

ProgressTrackingBlock ::= "@Progress" ":" INDENT ProgressFields DEDENT "@End_Progress"

ProgressFields  ::= ProgressField+

ProgressField   ::= Identifier ":" Expression

TranslationBlock ::= "@Translation_Note" ":" INDENT TranslationFields DEDENT "@End_Translation_Note"

TranslationFields ::= TranslationField+

TranslationField ::= Identifier ":" Expression

ErrorHandlingProtocolBlock ::= "@Error_Handling" ":" INDENT ErrorFields DEDENT "@End_Error_Handling"

ErrorFields     ::= ErrorField+

ErrorField      ::= Identifier ":" Expression

NaturalToFormalBlock ::= "@Natural_To_Formal" ":" INDENT NaturalFields DEDENT "@End_Natural_To_Formal"

NaturalFields   ::= NaturalField+

NaturalField    ::= Identifier ":" Expression

FreeText        ::= [^@]*  /* Any text until next @ symbol */
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

### Pattern Matching
```
Match user status:
    When "admin":
        Display "Full access granted"
    When "user":
        Display "Limited access granted"
    When _:
        Display "Access denied"
```

### Type Definitions
```
Type Result[T] is T OR String

Type Person is Dictionary with:
    name as String
    age as Integer
    email as String
```

### Asynchronous Programming
```
Async Process called "Fetch Data" that takes url:
    Let response be await http get with url as url
    Return response
```

### AI-to-AI Annotations
```
@Reasoning:
    Using quicksort because the dataset is small and partially ordered
@End_Reasoning

@Implementation:
    Process called "Sort Data" that takes data:
        # Implementation here
@End_Implementation
```

This formal grammar specification provides a comprehensive definition of the Runa programming language syntax, including all core features, advanced language constructs, AI-specific extensions, and AI-to-AI communication annotations.