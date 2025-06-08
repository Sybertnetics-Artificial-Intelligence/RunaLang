"""
Runa Language Formal EBNF Grammar

This module defines the formal grammar for the Runa programming language
using Extended Backus-Naur Form (EBNF). The grammar is used by the parser
to validate and process Runa source code.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple, Union


class GrammarError(Exception):
    """Exception raised for errors in the grammar specification."""
    pass


@dataclass
class Production:
    """
    Represents a grammar production rule with a name and expansion.
    
    Attributes:
        name: The name of the production rule
        expansion: The expansion of the rule in EBNF
        description: A description of what this rule represents
    """
    
    name: str
    expansion: str
    description: str = ""


class Grammar:
    """
    Represents the complete grammar of the Runa language.
    
    This class holds all the production rules of the language grammar and
    provides methods to validate and work with the grammar.
    """
    
    def __init__(self):
        """Initialize a new grammar."""
        self.productions: Dict[str, Production] = {}
        self.terminals: Set[str] = set()
        self.non_terminals: Set[str] = set()
        
        # Add the core grammar productions
        self._add_core_productions()
        
        # Validate the grammar
        self._validate()
    
    def _add_core_productions(self):
        """Add all the core production rules of the Runa grammar."""
        
        # Program structure
        self._add_production(
            "Program",
            "Statement+",
            "Top-level program structure"
        )
        
        # Statements
        self._add_production(
            "Statement",
            "Declaration | Assignment | Conditional | Loop | ProcessDefinition | " +
            "ReturnStatement | DisplayStatement | Block | ImportStatement | " +
            "TryCatchStatement | WhileLoop | CommentLine",
            "A statement in the Runa language"
        )
        
        # Comments
        self._add_production(
            "CommentLine",
            r'"#" [^\n]* "\n"',
            "A single-line comment"
        )
        
        # Declarations
        self._add_production(
            "Declaration",
            '"Let" Identifier OptionalType "be" Expression | ' +
            '"Define" Identifier OptionalType "as" Expression | ' +
            '"Define" Identifier OptionalType "as" "list" "containing" ExpressionList',
            "A variable declaration"
        )
        
        # Optional type annotation
        self._add_production(
            "OptionalType",
            '("(" Identifier ")")? ',
            "An optional type annotation"
        )
        
        # Assignment
        self._add_production(
            "Assignment",
            '"Set" Identifier "to" Expression',
            "An assignment statement"
        )
        
        # Expressions
        self._add_production(
            "Expression",
            'Literal | Identifier | BinaryExpression | FunctionCall | ' +
            'ListExpression | DictionaryExpression | IndexAccess | MemberAccess | ' +
            '"(" Expression ")" | "the" "sum" "of" "all" Identifier "in" Identifier | ' +
            '"length" "of" Expression | Expression "multiplied" "by" Expression | ' +
            'Expression "plus" Expression | Expression "minus" Expression | ' +
            'Expression "divided" "by" Expression | Expression "followed" "by" Expression | ' +
            'Expression "at" "index" Expression | "index" "of" Expression "in" Expression | ' +
            '"convert" "to" Identifier "(" Expression ")"',
            "An expression"
        )
        
        # Literals
        self._add_production(
            "Literal",
            'StringLiteral | NumberLiteral | BooleanLiteral | NullLiteral',
            "A literal value"
        )
        
        self._add_production(
            "StringLiteral",
            r'"\'" [^\']* "\'" | "\"" [^"]* "\""',
            "A string literal"
        )
        
        self._add_production(
            "NumberLiteral",
            r'[0-9]+ ("." [0-9]+)?',
            "A number literal"
        )
        
        self._add_production(
            "BooleanLiteral",
            '"true" | "false"',
            "A boolean literal"
        )
        
        self._add_production(
            "NullLiteral",
            '"null" | "none"',
            "A null literal"
        )
        
        # Binary expressions
        self._add_production(
            "BinaryExpression",
            'Expression Operator Expression',
            "A binary expression"
        )
        
        self._add_production(
            "Operator",
            '"is" "greater" "than" | "is" "less" "than" | "is" "equal" "to" | ' +
            '"is" "not" "equal" "to" | "is" "greater" "than" "or" "equal" "to" | ' +
            '"is" "less" "than" "or" "equal" "to" | "and" | "or" | "contains"',
            "An operator in a binary expression"
        )
        
        # Collections
        self._add_production(
            "ListExpression",
            '"list" "containing" ExpressionList | "[" ExpressionList "]"',
            "A list expression"
        )
        
        self._add_production(
            "ExpressionList",
            'Expression ("," Expression)* | ""',
            "A list of expressions"
        )
        
        self._add_production(
            "DictionaryExpression",
            '"dictionary" "with" ":" INDENT KeyValuePair+ DEDENT | ' +
            '"{" KeyValuePair ("," KeyValuePair)* "}"',
            "A dictionary expression"
        )
        
        self._add_production(
            "KeyValuePair",
            'StringLiteral "as" Expression | Identifier "as" Expression',
            "A key-value pair in a dictionary"
        )
        
        # Access operations
        self._add_production(
            "IndexAccess",
            'Identifier "[" Expression "]"',
            "An index access operation"
        )
        
        self._add_production(
            "MemberAccess",
            'Identifier "." Identifier',
            "A member access operation"
        )
        
        # Control structures
        self._add_production(
            "Conditional",
            '"If" Expression ":" Block ("Otherwise" "if" Expression ":" Block)* ' +
            '("Otherwise" ":" Block)?',
            "A conditional statement"
        )
        
        self._add_production(
            "Loop",
            '"For" "each" Identifier "in" Expression ":" Block',
            "A loop statement"
        )
        
        self._add_production(
            "WhileLoop",
            '"While" Expression ":" Block',
            "A while loop statement"
        )
        
        self._add_production(
            "Block",
            'INDENT Statement+ DEDENT | "{" Statement+ "}"',
            "A block of statements"
        )
        
        # Error handling
        self._add_production(
            "TryCatchStatement",
            '"Try" ":" Block "Catch" Identifier ":" Block',
            "A try-catch statement"
        )
        
        # Functions
        self._add_production(
            "ProcessDefinition",
            '"Process" "called" StringLiteral "that" "takes" ParameterList ' +
            '("returns" "(" Identifier ")")? ":" Block',
            "A function definition"
        )
        
        self._add_production(
            "ParameterList",
            'Identifier OptionalType ("and" Identifier OptionalType)* | ' +
            'Identifier OptionalType ("," Identifier OptionalType)* | ""',
            "A list of function parameters"
        )
        
        self._add_production(
            "ReturnStatement",
            '"Return" Expression',
            "A return statement"
        )
        
        self._add_production(
            "FunctionCall",
            'Identifier "with" NamedArguments | ' +
            'Identifier "with" ":" INDENT NamedArguments DEDENT | ' +
            'Identifier "(" ExpressionList ")"',
            "A function call"
        )
        
        self._add_production(
            "NamedArguments",
            'NamedArgument ("and" NamedArgument)* | ' +
            'NamedArgument (NEWLINE NamedArgument)* | ""',
            "A list of named arguments"
        )
        
        self._add_production(
            "NamedArgument",
            'Identifier "as" Expression',
            "A named argument"
        )
        
        # Input/Output operations
        self._add_production(
            "DisplayStatement",
            '"Display" Expression ("with" "message" Expression)?',
            "A display statement"
        )
        
        self._add_production(
            "InputStatement",
            '"input" "with" "prompt" StringLiteral',
            "An input statement"
        )
        
        # Modules
        self._add_production(
            "ImportStatement",
            '"Import" "module" StringLiteral | "Import" Identifier "from" "module" StringLiteral',
            "An import statement"
        )
        
        # Identifiers
        self._add_production(
            "Identifier",
            r'[a-zA-Z_][a-zA-Z0-9_]* ("." [a-zA-Z_][a-zA-Z0-9_]*)* | ' +
            r'[a-zA-Z_][a-zA-Z0-9_]* (" " [a-zA-Z_][a-zA-Z0-9_]*)+',
            "An identifier"
        )
        
        # AI-specific grammar extensions
        self._add_production(
            "ModelDefinition",
            '"Define" "neural" "network" StringLiteral ":" ModelBlock',
            "A neural network model definition"
        )
        
        self._add_production(
            "ModelBlock",
            'INDENT ModelStatement+ DEDENT',
            "A block of model statements"
        )
        
        self._add_production(
            "ModelStatement",
            '"Input" "layer" "accepts" Expression | ' +
            '"Use" "convolutional" "layers" "starting" "with" NumberLiteral "filters" | ' +
            '"Double" "filters" "at" "each" "downsampling" | ' +
            '"Include" "residual" "connections" | ' +
            '"Output" "layer" "has" NumberLiteral "classes" "with" Identifier "activation"',
            "A statement in a model definition"
        )
        
        # Training configuration
        self._add_production(
            "TrainingConfig",
            '"Configure" "training" "for" Identifier ":" TrainingBlock',
            "A training configuration"
        )
        
        self._add_production(
            "TrainingBlock",
            'INDENT TrainingStatement+ DEDENT',
            "A block of training statements"
        )
        
        self._add_production(
            "TrainingStatement",
            '"Use" "dataset" StringLiteral "with" Expression | ' +
            '"Apply" Expression "for" "augmentation" | ' +
            '"Use" Identifier "optimizer" "with" "learning" "rate" NumberLiteral | ' +
            '"Train" "for" NumberLiteral "epochs" "or" "until" Expression | ' +
            '"Save" "best" "model" "based" "on" Expression',
            "A statement in a training configuration"
        )
        
        # Knowledge integration extensions
        self._add_production(
            "KnowledgeQuery",
            '"knowledge" "." "query" "(" StringLiteral ")" | ' +
            '"knowledge" "." Identifier "(" ExpressionList ")"',
            "A knowledge query"
        )
        
        # Special productions
        self._add_production(
            "INDENT",
            '/* increase of indentation level */',
            "An increase in indentation level"
        )
        
        self._add_production(
            "DEDENT",
            '/* decrease of indentation level */',
            "A decrease in indentation level"
        )
        
        self._add_production(
            "NEWLINE",
            '/* newline character with consistent indentation */',
            "A newline with consistent indentation"
        )
        
    def _add_production(self, name: str, expansion: str, description: str = ""):
        """
        Add a production rule to the grammar.
        
        Args:
            name: The name of the production rule
            expansion: The expansion of the rule in EBNF
            description: A description of what this rule represents
        """
        self.productions[name] = Production(name, expansion, description)
        self.non_terminals.add(name)
    
    def _validate(self):
        """
        Validate the grammar for completeness and consistency.
        
        Raises:
            GrammarError: If the grammar is invalid
        """
        # Extract all non-terminals from the grammar
        referenced_non_terminals = set()
        for production in self.productions.values():
            # Find all symbols that look like non-terminals in the expansion
            for word in production.expansion.split():
                if word.isalpha() and word[0].isupper() and word != "INDENT" and word != "DEDENT" and word != "NEWLINE":
                    referenced_non_terminals.add(word)
        
        # Check for undefined non-terminals
        for non_terminal in referenced_non_terminals:
            if non_terminal not in self.productions:
                raise GrammarError(f"Undefined non-terminal: {non_terminal}")
        
        # Check for unreachable non-terminals
        if "Program" not in self.productions:
            raise GrammarError("Missing starting production: Program")
            
        reachable = set()
        self._find_reachable("Program", reachable)
        
        for non_terminal in self.non_terminals:
            if non_terminal not in reachable:
                raise GrammarError(f"Unreachable non-terminal: {non_terminal}")
    
    def _find_reachable(self, start: str, reachable: Set[str]):
        """
        Find all non-terminals reachable from the given start symbol.
        
        Args:
            start: The starting non-terminal
            reachable: Set to store reachable non-terminals
        """
        if start in reachable:
            return
        
        reachable.add(start)
        
        if start not in self.productions:
            return
        
        production = self.productions[start]
        for word in production.expansion.split():
            if word.isalpha() and word[0].isupper() and word != "INDENT" and word != "DEDENT" and word != "NEWLINE":
                self._find_reachable(word, reachable)
    
    def get_all_productions(self) -> List[Production]:
        """
        Get all production rules in the grammar.
        
        Returns:
            A list of all production rules
        """
        return list(self.productions.values())
    
    def get_production(self, name: str) -> Optional[Production]:
        """
        Get a specific production rule by name.
        
        Args:
            name: The name of the production rule
            
        Returns:
            The production rule, or None if not found
        """
        return self.productions.get(name)
    
    def to_ebnf_string(self) -> str:
        """
        Convert the grammar to a formatted EBNF string.
        
        Returns:
            The formatted EBNF grammar string
        """
        result = []
        
        # Add a header
        result.append("# Runa Language EBNF Grammar\n")
        
        # Group productions by category
        categories = {
            "Program Structure": ["Program", "Statement"],
            "Comments": ["CommentLine"],
            "Declarations and Assignments": ["Declaration", "Assignment", "OptionalType"],
            "Expressions": ["Expression", "Literal", "StringLiteral", "NumberLiteral", 
                           "BooleanLiteral", "NullLiteral", "BinaryExpression", "Operator"],
            "Collections": ["ListExpression", "ExpressionList", "DictionaryExpression", "KeyValuePair"],
            "Access Operations": ["IndexAccess", "MemberAccess"],
            "Control Structures": ["Conditional", "Loop", "WhileLoop", "Block", "TryCatchStatement"],
            "Functions": ["ProcessDefinition", "ParameterList", "ReturnStatement", 
                         "FunctionCall", "NamedArguments", "NamedArgument"],
            "I/O Operations": ["DisplayStatement", "InputStatement"],
            "Modules": ["ImportStatement"],
            "Identifiers": ["Identifier"],
            "AI Extensions": ["ModelDefinition", "ModelBlock", "ModelStatement", 
                             "TrainingConfig", "TrainingBlock", "TrainingStatement"],
            "Knowledge Integration": ["KnowledgeQuery"],
            "Special Productions": ["INDENT", "DEDENT", "NEWLINE"]
        }
        
        # Add productions by category
        for category, production_names in categories.items():
            result.append(f"\n## {category}\n")
            
            for name in production_names:
                if name in self.productions:
                    prod = self.productions[name]
                    if prod.description:
                        result.append(f"/* {prod.description} */")
                    result.append(f"{name} ::= {prod.expansion}\n")
        
        return "\n".join(result)


# Create the grammar instance
RUNA_GRAMMAR = Grammar()


def get_grammar() -> Grammar:
    """
    Get the Runa language grammar.
    
    Returns:
        The grammar instance
    """
    return RUNA_GRAMMAR


def get_ebnf_string() -> str:
    """
    Get the formatted EBNF string of the Runa grammar.
    
    Returns:
        The formatted EBNF grammar string
    """
    return RUNA_GRAMMAR.to_ebnf_string()


# Export the grammar as an EBNF file
def export_grammar_to_file(file_path: str):
    """
    Export the grammar to a file in EBNF format.
    
    Args:
        file_path: The path to the output file
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(get_ebnf_string()) 