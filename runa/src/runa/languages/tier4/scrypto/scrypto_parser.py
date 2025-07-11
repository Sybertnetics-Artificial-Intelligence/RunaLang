"""
Scrypto language parser for asset-oriented smart contracts on Radix DLT.

This parser handles Rust-based syntax with Scrypto-specific extensions including:
- Blueprint definitions and component instantiation
- Resource creation and management (fungible/non-fungible tokens)
- Bucket and Vault operations for asset handling
- Badge-based authentication
- SBOR encoding and Radix Engine API calls
"""

import re
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass

from .scrypto_ast import *


class ScryptoLexer:
    """Lexer for Scrypto language tokens"""
    
    # Token types
    TOKEN_PATTERNS = [
        # Comments
        ('COMMENT_LINE', r'//.*'),
        ('COMMENT_BLOCK', r'/\*[\s\S]*?\*/'),
        
        # Keywords - Rust
        ('FN', r'\bfn\b'),
        ('PUB', r'\bpub\b'),
        ('STRUCT', r'\bstruct\b'),
        ('ENUM', r'\benum\b'),
        ('IMPL', r'\bimpl\b'),
        ('TRAIT', r'\btrait\b'),
        ('USE', r'\buse\b'),
        ('MOD', r'\bmod\b'),
        ('LET', r'\blet\b'),
        ('MUT', r'\bmut\b'),
        ('IF', r'\bif\b'),
        ('ELSE', r'\belse\b'),
        ('MATCH', r'\bmatch\b'),
        ('RETURN', r'\breturn\b'),
        ('SELF', r'\bself\b'),
        ('SUPER', r'\bsuper\b'),
        ('CRATE', r'\bcrate\b'),
        
        # Keywords - Scrypto specific
        ('BLUEPRINT', r'\bblueprint\b'),
        ('COMPONENT', r'\bcomponent\b'),
        ('RESOURCE', r'\bresource\b'),
        ('BUCKET', r'\bbucket\b'),
        ('VAULT', r'\bvault\b'),
        ('PROOF', r'\bproof\b'),
        
        # Attributes and macros
        ('ATTRIBUTE', r'#\[[^\]]*\]'),
        ('MACRO_CALL', r'[a-zA-Z_][a-zA-Z0-9_]*!'),
        
        # Literals
        ('DECIMAL_LITERAL', r'\d+\.\d+dec'),
        ('INTEGER_LITERAL', r'\d+[iu](?:8|16|32|64|128)?'),
        ('FLOAT_LITERAL', r'\d+\.\d+[f]?(?:32|64)?'),
        ('STRING_LITERAL', r'"(?:[^"\\]|\\.)*"'),
        ('CHAR_LITERAL', r"'(?:[^'\\]|\\.)'"),
        ('BOOLEAN_LITERAL', r'\b(?:true|false)\b'),
        
        # Identifiers and types
        ('RESOURCE_ADDRESS', r'resource_[a-z0-9]+'),
        ('COMPONENT_ADDRESS', r'component_[a-z0-9]+'),
        ('PACKAGE_ADDRESS', r'package_[a-z0-9]+'),
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        
        # Operators and punctuation
        ('ARROW', r'=>'),
        ('FAT_ARROW', r'=>'),
        ('SCOPE_RESOLUTION', r'::'),
        ('RANGE_INCLUSIVE', r'\.\.='),
        ('RANGE_EXCLUSIVE', r'\.\.'),
        ('EQ', r'=='),
        ('NE', r'!='),
        ('LE', r'<='),
        ('GE', r'>='),
        ('LT', r'<'),
        ('GT', r'>'),
        ('AND', r'&&'),
        ('OR', r'\|\|'),
        ('ASSIGN', r'='),
        ('PLUS_ASSIGN', r'\+='),
        ('MINUS_ASSIGN', r'-='),
        ('DOT', r'\.'),
        ('COMMA', r','),
        ('SEMICOLON', r';'),
        ('COLON', r':'),
        ('QUESTION', r'\?'),
        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MULTIPLY', r'\*'),
        ('DIVIDE', r'/'),
        ('MODULO', r'%'),
        ('AMPERSAND', r'&'),
        ('PIPE', r'\|'),
        ('CARET', r'\^'),
        ('TILDE', r'~'),
        ('BANG', r'!'),
        
        # Brackets and braces
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('LBRACKET', r'\['),
        ('RBRACKET', r'\]'),
        
        # Whitespace
        ('WHITESPACE', r'\s+'),
        ('NEWLINE', r'\n'),
    ]
    
    def __init__(self, text: str):
        self.text = text
        self.tokens = []
        self.current_pos = 0
        self.line = 1
        self.column = 1
    
    def tokenize(self) -> List[Dict[str, Any]]:
        """Tokenize the input text"""
        while self.current_pos < len(self.text):
            matched = False
            
            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.text, self.current_pos)
                
                if match:
                    value = match.group(0)
                    
                    if token_type not in ['WHITESPACE', 'COMMENT_LINE', 'COMMENT_BLOCK']:
                        self.tokens.append({
                            'type': token_type,
                            'value': value,
                            'line': self.line,
                            'column': self.column
                        })
                    
                    # Update position
                    self.current_pos = match.end()
                    if token_type == 'NEWLINE':
                        self.line += 1
                        self.column = 1
                    else:
                        self.column += len(value)
                    
                    matched = True
                    break
            
            if not matched:
                # Skip unrecognized character
                self.current_pos += 1
                self.column += 1
        
        return self.tokens


class ScryptoParser:
    """
    Parser for Scrypto language.
    
    Handles Rust-based syntax with Scrypto-specific extensions for
    asset-oriented programming constructs.
    """
    
    def __init__(self, tokens: List[Dict[str, Any]]):
        self.tokens = tokens
        self.current_pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def parse(self) -> ScryptoProgram:
        """Parse tokens into Scrypto AST"""
        return self.parse_program()
    
    def peek_token(self, offset: int = 0) -> Optional[Dict[str, Any]]:
        """Peek at token at offset from current position"""
        pos = self.current_pos + offset
        return self.tokens[pos] if pos < len(self.tokens) else None
    
    def advance_token(self):
        """Move to next token"""
        if self.current_pos < len(self.tokens) - 1:
            self.current_pos += 1
            self.current_token = self.tokens[self.current_pos]
        else:
            self.current_token = None
    
    def expect_token(self, token_type: str) -> Dict[str, Any]:
        """Expect specific token type and advance"""
        if not self.current_token or self.current_token['type'] != token_type:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token['type'] if self.current_token else 'EOF'}")
        
        token = self.current_token
        self.advance_token()
        return token
    
    def parse_program(self) -> ScryptoProgram:
        """Parse complete Scrypto program"""
        packages = []
        use_statements = []
        
        while self.current_token:
            if self.current_token['type'] == 'USE':
                use_statements.append(self.parse_use_statement())
            elif self.current_token['type'] == 'ATTRIBUTE':
                # Skip standalone attributes
                self.advance_token()
            else:
                # Parse as part of default package
                if not packages:
                    packages.append(ScryptoPackage(
                        name="default",
                        version="1.0.0",
                        blueprints=[],
                        dependencies=[]
                    ))
                
                if self.current_token['type'] == 'BLUEPRINT':
                    packages[0].blueprints.append(self.parse_blueprint())
                elif self.current_token['type'] == 'STRUCT':
                    # Handle struct definitions
                    self.parse_struct()
                elif self.current_token['type'] == 'ENUM':
                    # Handle enum definitions
                    self.parse_enum()
                else:
                    self.advance_token()
        
        return ScryptoProgram(
            packages=packages,
            use_statements=use_statements
        )
    
    def parse_use_statement(self) -> ScryptoUseStatement:
        """Parse use statement"""
        self.expect_token('USE')
        
        path_parts = []
        while self.current_token and self.current_token['type'] == 'IDENTIFIER':
            path_parts.append(self.current_token['value'])
            self.advance_token()
            
            if self.current_token and self.current_token['type'] == 'SCOPE_RESOLUTION':
                self.advance_token()
            else:
                break
        
        path = "::".join(path_parts)
        alias = None
        is_glob = False
        
        if self.current_token and self.current_token['value'] == 'as':
            self.advance_token()
            alias = self.expect_token('IDENTIFIER')['value']
        elif self.current_token and self.current_token['value'] == '*':
            is_glob = True
            self.advance_token()
        
        self.expect_token('SEMICOLON')
        
        return ScryptoUseStatement(
            path=path,
            alias=alias,
            is_glob=is_glob
        )
    
    def parse_blueprint(self) -> ScryptoBlueprint:
        """Parse blueprint definition"""
        # Skip 'blueprint' keyword if present
        if self.current_token and self.current_token['type'] == 'BLUEPRINT':
            self.advance_token()
        
        # Parse attributes
        attributes = []
        while self.current_token and self.current_token['type'] == 'ATTRIBUTE':
            attributes.append(self.current_token['value'])
            self.advance_token()
        
        # Parse struct definition (component state)
        self.expect_token('STRUCT')
        name = self.expect_token('IDENTIFIER')['value']
        
        state_struct = self.parse_struct_body(name)
        
        # Parse impl block
        methods = []
        instantiate_functions = []
        
        if self.current_token and self.current_token['type'] == 'IMPL':
            self.advance_token()
            self.expect_token('IDENTIFIER')  # struct name
            self.expect_token('LBRACE')
            
            while self.current_token and self.current_token['type'] != 'RBRACE':
                if self.current_token['type'] == 'PUB':
                    method = self.parse_method()
                    if method.is_instantiate:
                        instantiate_functions.append(method)
                    else:
                        methods.append(method)
                else:
                    self.advance_token()
            
            self.expect_token('RBRACE')
        
        return ScryptoBlueprint(
            name=name,
            state_struct=state_struct,
            methods=methods,
            instantiate_functions=instantiate_functions
        )
    
    def parse_struct(self) -> ScryptoStruct:
        """Parse struct definition"""
        self.expect_token('STRUCT')
        name = self.expect_token('IDENTIFIER')['value']
        return self.parse_struct_body(name)
    
    def parse_struct_body(self, name: str) -> ScryptoStruct:
        """Parse struct body"""
        self.expect_token('LBRACE')
        
        fields = []
        while self.current_token and self.current_token['type'] != 'RBRACE':
            if self.current_token['type'] == 'PUB':
                self.advance_token()
                field_name = self.expect_token('IDENTIFIER')['value']
                self.expect_token('COLON')
                field_type = self.parse_type()
                
                fields.append(ScryptoStructField(
                    name=field_name,
                    field_type=field_type,
                    visibility="pub"
                ))
                
                if self.current_token and self.current_token['type'] == 'COMMA':
                    self.advance_token()
            else:
                self.advance_token()
        
        self.expect_token('RBRACE')
        
        return ScryptoStruct(
            name=name,
            fields=fields
        )
    
    def parse_enum(self) -> ScryptoEnum:
        """Parse enum definition"""
        self.expect_token('ENUM')
        name = self.expect_token('IDENTIFIER')['value']
        self.expect_token('LBRACE')
        
        variants = []
        while self.current_token and self.current_token['type'] != 'RBRACE':
            if self.current_token['type'] == 'IDENTIFIER':
                variant_name = self.current_token['value']
                self.advance_token()
                
                variants.append(ScryptoEnumVariant(
                    name=variant_name,
                    fields=[]
                ))
                
                if self.current_token and self.current_token['type'] == 'COMMA':
                    self.advance_token()
            else:
                self.advance_token()
        
        self.expect_token('RBRACE')
        
        return ScryptoEnum(
            name=name,
            variants=variants
        )
    
    def parse_method(self) -> ScryptoMethod:
        """Parse method definition"""
        visibility = "pub"
        if self.current_token and self.current_token['type'] == 'PUB':
            self.advance_token()
        
        self.expect_token('FN')
        name = self.expect_token('IDENTIFIER')['value']
        
        # Parse parameters
        self.expect_token('LPAREN')
        parameters = []
        
        while self.current_token and self.current_token['type'] != 'RPAREN':
            if self.current_token['type'] == 'IDENTIFIER':
                param_name = self.current_token['value']
                self.advance_token()
                self.expect_token('COLON')
                param_type = self.parse_type()
                
                parameters.append(ScryptoParameter(
                    name=param_name,
                    param_type=param_type
                ))
                
                if self.current_token and self.current_token['type'] == 'COMMA':
                    self.advance_token()
            else:
                self.advance_token()
        
        self.expect_token('RPAREN')
        
        # Parse return type
        return_type = None
        if self.current_token and self.current_token['type'] == 'ARROW':
            self.advance_token()
            return_type = self.parse_type()
        
        # Parse method body
        body = self.parse_block()
        
        return ScryptoMethod(
            name=name,
            parameters=parameters,
            return_type=return_type,
            body=body,
            visibility=visibility,
            is_instantiate=(name == "instantiate" or name.startswith("new"))
        )
    
    def parse_type(self) -> ScryptoType:
        """Parse type annotation"""
        if not self.current_token:
            raise SyntaxError("Expected type annotation")
        
        type_name = self.current_token['value']
        self.advance_token()
        
        # Handle generic types
        generics = []
        if self.current_token and self.current_token['type'] == 'LT':
            self.advance_token()
            while self.current_token and self.current_token['type'] != 'GT':
                generics.append(self.parse_type())
                if self.current_token and self.current_token['type'] == 'COMMA':
                    self.advance_token()
            self.expect_token('GT')
        
        return ScryptoType(
            name=type_name,
            generics=generics
        )
    
    def parse_block(self) -> ScryptoBlock:
        """Parse block of statements"""
        self.expect_token('LBRACE')
        
        statements = []
        while self.current_token and self.current_token['type'] != 'RBRACE':
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        self.expect_token('RBRACE')
        
        return ScryptoBlock(statements=statements)
    
    def parse_statement(self) -> Optional[ScryptoStatement]:
        """Parse statement"""
        if not self.current_token:
            return None
        
        if self.current_token['type'] == 'LET':
            return self.parse_let_statement()
        elif self.current_token['type'] == 'RETURN':
            return self.parse_return_statement()
        else:
            # Parse as expression statement
            expr = self.parse_expression()
            if expr and self.current_token and self.current_token['type'] == 'SEMICOLON':
                self.advance_token()
                return ScryptoExpressionStatement(expression=expr)
            elif expr:
                return ScryptoExpressionStatement(expression=expr)
        
        return None
    
    def parse_let_statement(self) -> ScryptoLetStatement:
        """Parse let statement"""
        self.expect_token('LET')
        
        is_mutable = False
        if self.current_token and self.current_token['type'] == 'MUT':
            is_mutable = True
            self.advance_token()
        
        name = self.expect_token('IDENTIFIER')['value']
        
        type_annotation = None
        if self.current_token and self.current_token['type'] == 'COLON':
            self.advance_token()
            type_annotation = self.parse_type()
        
        value = None
        if self.current_token and self.current_token['type'] == 'ASSIGN':
            self.advance_token()
            value = self.parse_expression()
        
        if self.current_token and self.current_token['type'] == 'SEMICOLON':
            self.advance_token()
        
        return ScryptoLetStatement(
            name=name,
            type_annotation=type_annotation,
            value=value,
            is_mutable=is_mutable
        )
    
    def parse_return_statement(self) -> ScryptoReturnStatement:
        """Parse return statement"""
        self.expect_token('RETURN')
        
        value = None
        if self.current_token and self.current_token['type'] != 'SEMICOLON':
            value = self.parse_expression()
        
        if self.current_token and self.current_token['type'] == 'SEMICOLON':
            self.advance_token()
        
        return ScryptoReturnStatement(value=value)
    
    def parse_expression(self) -> Optional[ScryptoExpression]:
        """Parse expression"""
        return self.parse_primary_expression()
    
    def parse_primary_expression(self) -> Optional[ScryptoExpression]:
        """Parse primary expression"""
        if not self.current_token:
            return None
        
        # Parse literals
        if self.current_token['type'] in ['INTEGER_LITERAL', 'FLOAT_LITERAL', 'DECIMAL_LITERAL']:
            value = self.current_token['value']
            literal_type = "decimal" if "dec" in value else "integer" if self.current_token['type'] == 'INTEGER_LITERAL' else "float"
            self.advance_token()
            return ScryptoLiteralExpression(value=value, literal_type=literal_type)
        
        elif self.current_token['type'] == 'STRING_LITERAL':
            value = self.current_token['value'][1:-1]  # Remove quotes
            self.advance_token()
            return ScryptoLiteralExpression(value=value, literal_type="string")
        
        elif self.current_token['type'] == 'BOOLEAN_LITERAL':
            value = self.current_token['value'] == 'true'
            self.advance_token()
            return ScryptoLiteralExpression(value=value, literal_type="boolean")
        
        # Parse identifiers and method calls
        elif self.current_token['type'] == 'IDENTIFIER':
            name = self.current_token['value']
            self.advance_token()
            
            # Check for method call
            if self.current_token and self.current_token['type'] == 'LPAREN':
                return self.parse_function_call(name)
            elif self.current_token and self.current_token['type'] == 'DOT':
                # Method call on identifier
                receiver = ScryptoIdentifierExpression(name=name)
                return self.parse_method_call(receiver)
            else:
                return ScryptoIdentifierExpression(name=name)
        
        # Parse macro calls
        elif self.current_token['type'] == 'MACRO_CALL':
            macro_name = self.current_token['value'][:-1]  # Remove '!'
            self.advance_token()
            
            arguments = []
            if self.current_token and self.current_token['type'] == 'LPAREN':
                self.advance_token()
                while self.current_token and self.current_token['type'] != 'RPAREN':
                    if self.current_token['type'] == 'STRING_LITERAL':
                        arguments.append(self.current_token['value'])
                        self.advance_token()
                    if self.current_token and self.current_token['type'] == 'COMMA':
                        self.advance_token()
                self.expect_token('RPAREN')
            
            return ScryptoMacroCall(macro_name=macro_name, arguments=arguments)
        
        else:
            # Skip unknown tokens
            self.advance_token()
            return None
    
    def parse_function_call(self, function_name: str) -> ScryptoFunctionCallExpression:
        """Parse function call"""
        self.expect_token('LPAREN')
        
        arguments = []
        while self.current_token and self.current_token['type'] != 'RPAREN':
            arg = self.parse_expression()
            if arg:
                arguments.append(arg)
            
            if self.current_token and self.current_token['type'] == 'COMMA':
                self.advance_token()
        
        self.expect_token('RPAREN')
        
        return ScryptoFunctionCallExpression(
            function_name=function_name,
            arguments=arguments
        )
    
    def parse_method_call(self, receiver: ScryptoExpression) -> ScryptoMethodCallExpression:
        """Parse method call"""
        self.expect_token('DOT')
        method_name = self.expect_token('IDENTIFIER')['value']
        
        arguments = []
        if self.current_token and self.current_token['type'] == 'LPAREN':
            self.advance_token()
            while self.current_token and self.current_token['type'] != 'RPAREN':
                arg = self.parse_expression()
                if arg:
                    arguments.append(arg)
                
                if self.current_token and self.current_token['type'] == 'COMMA':
                    self.advance_token()
            self.expect_token('RPAREN')
        
        return ScryptoMethodCallExpression(
            receiver=receiver,
            method_name=method_name,
            arguments=arguments
        )


def parse_scrypto(source_code: str) -> ScryptoAST:
    """
    Parse Scrypto source code into AST.
    
    Args:
        source_code: Scrypto source code string
        
    Returns:
        ScryptoAST: Parsed AST representation
        
    Raises:
        SyntaxError: If source code contains syntax errors
    """
    try:
        # Tokenize
        lexer = ScryptoLexer(source_code)
        tokens = lexer.tokenize()
        
        if not tokens:
            # Empty program
            return ScryptoAST(ScryptoProgram())
        
        # Parse
        parser = ScryptoParser(tokens)
        program = parser.parse()
        
        return ScryptoAST(program)
        
    except Exception as e:
        raise SyntaxError(f"Scrypto parsing error: {str(e)}")


# Example usage and testing
if __name__ == "__main__":
    sample_code = '''
    use scrypto::prelude::*;
    
    #[derive(ScryptoSbor)]
    pub struct GumballMachine {
        gumball_vault: Vault,
        collected_xrd: Vault,
        price: Decimal,
    }
    
    impl GumballMachine {
        pub fn instantiate(price: Decimal) -> ComponentAddress {
            let gumball_bucket = ResourceBuilder::new_fungible()
                .metadata("name", "Gumball")
                .metadata("symbol", "GUM")
                .create_with_initial_supply(100);
            
            Self {
                gumball_vault: Vault::with_bucket(gumball_bucket),
                collected_xrd: Vault::new(RADIX_TOKEN),
                price,
            }
            .instantiate()
            .globalize()
        }
        
        pub fn buy_gumball(&mut self, payment: Bucket) -> Bucket {
            let gumball = self.gumball_vault.take(1);
            self.collected_xrd.put(payment);
            gumball
        }
    }
    '''
    
    try:
        ast = parse_scrypto(sample_code)
        print("✅ Successfully parsed Scrypto code")
        print(f"Found {len(ast.get_all_blueprints())} blueprints")
    except Exception as e:
        print(f"❌ Parsing failed: {e}") 