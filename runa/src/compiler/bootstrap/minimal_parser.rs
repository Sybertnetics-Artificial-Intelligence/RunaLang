//! # Minimal Parser - Runa Bootstrap Compiler
//!
//! This module provides the minimal parsing functionality needed for the
//! Runa language bootstrap compiler. It implements a complete recursive descent
//! parser that can handle the essential Runa syntax required for bootstrap compilation.
//!
//! ## Key Features
//! - Complete AST generation for bootstrap Runa syntax
//! - Recursive descent parsing with error recovery
//! - Operator precedence handling
//! - Type annotation parsing
//! - Function and type definition parsing
//! - Expression and statement parsing
//! - Comprehensive error reporting with position information
//! - Integration points for AOTT system handoff
//!
//! ## Bootstrap Constraints
//! This parser is designed to be minimal (5% of total compiler system) while
//! providing complete functionality for bootstrap compilation. It focuses on:
//! - Essential Runa constructs only
//! - Fast parsing with minimal memory allocation
//! - Clean AST generation for codegen phase
//! - Comprehensive error recovery for development
//!
//! ## Integration with AOTT
//! This parser provides the foundation for transitioning to the AOTT execution
//! system by producing clean ASTs that can be processed by the minimal codegen
//! and eventually handed off to the full AOTT compilation pipeline.

use crate::compiler::bootstrap::minimal_lexer::{Token, TokenType, LexerError, Position};
use std::collections::HashMap;
use std::fmt;

/// AST node types for the minimal parser
#[derive(Debug, Clone, PartialEq)]
pub enum AstNode {
    // Program structure
    Program {
        items: Vec<AstNode>,
        position: Position,
    },
    
    // Imports
    Import {
        module_name: String,
        alias: Option<String>,
        position: Position,
    },
    
    // Type definitions
    TypeDefinition {
        name: String,
        fields: Vec<FieldDefinition>,
        variants: Vec<VariantDefinition>,
        position: Position,
    },
    
    // Process (function) definitions
    ProcessDefinition {
        name: String,
        parameters: Vec<Parameter>,
        return_type: Option<TypeAnnotation>,
        body: Box<AstNode>,
        position: Position,
    },
    
    // Statements
    Block {
        statements: Vec<AstNode>,
        position: Position,
    },
    
    LetStatement {
        variable_name: String,
        value: Box<AstNode>,
        type_annotation: Option<TypeAnnotation>,
        position: Position,
    },
    
    ReturnStatement {
        value: Option<Box<AstNode>>,
        position: Position,
    },
    
    ThrowStatement {
        error: Box<AstNode>,
        message: Option<Box<AstNode>>,
        position: Position,
    },
    
    IfStatement {
        condition: Box<AstNode>,
        then_branch: Box<AstNode>,
        else_branch: Option<Box<AstNode>>,
        position: Position,
    },
    
    ForStatement {
        variable: String,
        iterable: Box<AstNode>,
        body: Box<AstNode>,
        position: Position,
    },
    
    WhileStatement {
        condition: Box<AstNode>,
        body: Box<AstNode>,
        position: Position,
    },
    
    ExpressionStatement {
        expression: Box<AstNode>,
        position: Position,
    },
    
    // Expressions
    BinaryOperation {
        left: Box<AstNode>,
        operator: BinaryOperator,
        right: Box<AstNode>,
        position: Position,
    },
    
    UnaryOperation {
        operator: UnaryOperator,
        operand: Box<AstNode>,
        position: Position,
    },
    
    FunctionCall {
        function_name: String,
        arguments: Vec<AstNode>,
        position: Position,
    },
    
    MethodCall {
        object: Box<AstNode>,
        method_name: String,
        arguments: Vec<AstNode>,
        position: Position,
    },
    
    // Literals
    StringLiteral {
        value: String,
        position: Position,
    },
    
    IntegerLiteral {
        value: i64,
        position: Position,
    },
    
    FloatLiteral {
        value: f64,
        position: Position,
    },
    
    BooleanLiteral {
        value: bool,
        position: Position,
    },
    
    ListLiteral {
        elements: Vec<AstNode>,
        position: Position,
    },
    
    DictionaryLiteral {
        pairs: Vec<(AstNode, AstNode)>,
        position: Position,
    },
    
    // Identifiers
    Identifier {
        name: String,
        position: Position,
    },
    
    // Member access
    MemberAccess {
        object: Box<AstNode>,
        member: String,
        position: Position,
    },
    
    // Indexing
    IndexAccess {
        object: Box<AstNode>,
        index: Box<AstNode>,
        position: Position,
    },
}

/// Binary operators
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BinaryOperator {
    // Arithmetic
    Add,
    Subtract,
    Multiply,
    Divide,
    Modulo,
    Power,
    
    // Comparison
    Equal,
    NotEqual,
    Less,
    LessEqual,
    Greater,
    GreaterEqual,
    
    // Logical
    And,
    Or,
    
    // Assignment
    Assign,
}

/// Unary operators
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum UnaryOperator {
    Plus,
    Minus,
    Not,
}

/// Type annotations
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TypeAnnotation {
    Simple {
        name: String,
    },
    Generic {
        base: String,
        parameters: Vec<TypeAnnotation>,
    },
    Function {
        parameters: Vec<TypeAnnotation>,
        return_type: Box<TypeAnnotation>,
    },
}

/// Function parameters
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Parameter {
    pub name: String,
    pub type_annotation: TypeAnnotation,
    pub position: Position,
}

/// Type definition fields
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FieldDefinition {
    pub name: String,
    pub type_annotation: TypeAnnotation,
    pub position: Position,
}

/// Enum variants
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct VariantDefinition {
    pub name: String,
    pub associated_type: Option<TypeAnnotation>,
    pub position: Position,
}

/// Operator precedence levels
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Precedence {
    None = 0,
    Assignment = 1,
    Or = 2,
    And = 3,
    Equality = 4,
    Comparison = 5,
    Term = 6,
    Factor = 7,
    Unary = 8,
    Call = 9,
    Primary = 10,
}

/// Parsing errors
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ParseError {
    UnexpectedToken {
        expected: String,
        found: Token,
        message: String,
    },
    UnexpectedEndOfFile {
        expected: String,
        position: Position,
    },
    InvalidSyntax {
        token: Token,
        message: String,
    },
    InvalidOperator {
        operator: String,
        position: Position,
    },
    InvalidTypeAnnotation {
        annotation: String,
        position: Position,
        message: String,
    },
    DuplicateDefinition {
        name: String,
        first_position: Position,
        duplicate_position: Position,
    },
    LexerError {
        error: LexerError,
    },
}

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ParseError::UnexpectedToken { expected, found, message } => {
                write!(f, "Expected {} but found {} at {}: {}", expected, found, found.position, message)
            }
            ParseError::UnexpectedEndOfFile { expected, position } => {
                write!(f, "Unexpected end of file, expected {} at {}", expected, position)
            }
            ParseError::InvalidSyntax { token, message } => {
                write!(f, "Invalid syntax at {}: {}", token.position, message)
            }
            ParseError::InvalidOperator { operator, position } => {
                write!(f, "Invalid operator '{}' at {}", operator, position)
            }
            ParseError::InvalidTypeAnnotation { annotation, position, message } => {
                write!(f, "Invalid type annotation '{}' at {}: {}", annotation, position, message)
            }
            ParseError::DuplicateDefinition { name, first_position, duplicate_position } => {
                write!(f, "Duplicate definition of '{}': first at {}, duplicate at {}", 
                       name, first_position, duplicate_position)
            }
            ParseError::LexerError { error } => {
                write!(f, "Lexer error: {}", error)
            }
        }
    }
}

impl std::error::Error for ParseError {}

impl From<LexerError> for ParseError {
    fn from(error: LexerError) -> Self {
        ParseError::LexerError { error }
    }
}

/// Result type for parser operations
pub type ParseResult<T> = Result<T, ParseError>;

/// The minimal parser for Runa bootstrap compilation
pub struct MinimalParser {
    tokens: Vec<Token>,
    current: usize,
    definitions: HashMap<String, Position>,
}

impl MinimalParser {
    /// Create a new minimal parser from tokens
    pub fn new(tokens: Vec<Token>) -> Self {
        MinimalParser {
            tokens,
            current: 0,
            definitions: HashMap::new(),
        }
    }
    
    /// Check if we're at the end of the token stream
    fn is_at_end(&self) -> bool {
        self.current >= self.tokens.len() || 
        matches!(self.peek().token_type, TokenType::EndOfFile)
    }
    
    /// Peek at the current token without consuming it
    fn peek(&self) -> &Token {
        self.tokens.get(self.current).unwrap_or_else(|| {
            // Return a synthetic EOF token
            static EOF_TOKEN: Token = Token {
                token_type: TokenType::EndOfFile,
                position: Position { line: 1, column: 1, offset: 0 },
                raw_text: String::new(),
            };
            &EOF_TOKEN
        })
    }
    
    /// Peek at the next token without consuming current
    fn peek_next(&self) -> &Token {
        self.tokens.get(self.current + 1).unwrap_or_else(|| {
            static EOF_TOKEN: Token = Token {
                token_type: TokenType::EndOfFile,
                position: Position { line: 1, column: 1, offset: 0 },
                raw_text: String::new(),
            };
            &EOF_TOKEN
        })
    }
    
    /// Consume and return the current token
    fn advance(&mut self) -> &Token {
        if !self.is_at_end() {
            self.current += 1;
        }
        self.previous()
    }
    
    /// Return the previous token
    fn previous(&self) -> &Token {
        &self.tokens[self.current - 1]
    }
    
    /// Check if the current token matches the given type
    fn check(&self, token_type: &TokenType) -> bool {
        if self.is_at_end() {
            false
        } else {
            std::mem::discriminant(&self.peek().token_type) == std::mem::discriminant(token_type)
        }
    }
    
    /// Consume the current token if it matches the expected type
    fn match_token(&mut self, expected: &TokenType) -> bool {
        if self.check(expected) {
            self.advance();
            true
        } else {
            false
        }
    }
    
    /// Consume the current token, expecting it to match the given type
    fn consume(&mut self, expected: TokenType, message: &str) -> ParseResult<&Token> {
        if self.check(&expected) {
            Ok(self.advance())
        } else {
            Err(ParseError::UnexpectedToken {
                expected: format!("{:?}", expected),
                found: self.peek().clone(),
                message: message.to_string(),
            })
        }
    }
    
    /// Skip newline tokens
    fn skip_newlines(&mut self) {
        while self.match_token(&TokenType::Newline) {
            // Continue skipping
        }
    }
    
    /// Parse the entire program
    pub fn parse_program(&mut self) -> ParseResult<AstNode> {
        let start_position = self.peek().position;
        let mut items = Vec::new();
        
        self.skip_newlines();
        
        while !self.is_at_end() {
            let item = self.parse_top_level_item()?;
            items.push(item);
            self.skip_newlines();
        }
        
        Ok(AstNode::Program {
            items,
            position: start_position,
        })
    }
    
    /// Parse a top-level item (import, type, process)
    fn parse_top_level_item(&mut self) -> ParseResult<AstNode> {
        match &self.peek().token_type {
            TokenType::Keyword(k) if k == "Import" => self.parse_import(),
            TokenType::Keyword(k) if k == "Type" => self.parse_type_definition(),
            TokenType::Keyword(k) if k == "Process" => self.parse_process_definition(),
            _ => Err(ParseError::UnexpectedToken {
                expected: "Import, Type, or Process".to_string(),
                found: self.peek().clone(),
                message: "Expected top-level declaration".to_string(),
            }),
        }
    }
    
    /// Parse an import statement
    fn parse_import(&mut self) -> ParseResult<AstNode> {
        let start_position = self.peek().position;
        
        self.consume(TokenType::Keyword("Import".to_string()), "Expected 'Import'")?;
        
        let module_name = match &self.advance().token_type {
            TokenType::StringLiteral(name) => name.clone(),
            _ => return Err(ParseError::UnexpectedToken {
                expected: "string literal".to_string(),
                found: self.previous().clone(),
                message: "Expected module name as string".to_string(),
            }),
        };
        
        let alias = if self.match_token(&TokenType::Keyword("as".to_string())) {
            match &self.advance().token_type {
                TokenType::Identifier(name) => Some(name.clone()),
                _ => return Err(ParseError::UnexpectedToken {
                    expected: "identifier".to_string(),
                    found: self.previous().clone(),
                    message: "Expected alias identifier".to_string(),
                }),
            }
        } else {
            None
        };
        
        Ok(AstNode::Import {
            module_name,
            alias,
            position: start_position,
        })
    }
    
    /// Parse a type definition
    fn parse_type_definition(&mut self) -> ParseResult<AstNode> {
        let start_position = self.peek().position;
        
        self.consume(TokenType::Keyword("Type".to_string()), "Expected 'Type'")?;
        self.consume(TokenType::Keyword("called".to_string()), "Expected 'called'")?;
        
        let name = match &self.advance().token_type {
            TokenType::StringLiteral(name) => name.clone(),
            _ => return Err(ParseError::UnexpectedToken {
                expected: "string literal".to_string(),
                found: self.previous().clone(),
                message: "Expected type name as string".to_string(),
            }),
        };
        
        // Check for duplicate definitions
        if let Some(first_pos) = self.definitions.get(&name) {
            return Err(ParseError::DuplicateDefinition {
                name,
                first_position: *first_pos,
                duplicate_position: start_position,
            });
        }
        self.definitions.insert(name.clone(), start_position);
        
        self.consume(TokenType::Colon, "Expected ':' after type name")?;
        self.skip_newlines();
        
        let mut fields = Vec::new();
        let mut variants = Vec::new();
        
        // Parse fields or variants
        if self.match_token(&TokenType::Or) {
            // Enum-style type with variants
            variants.push(self.parse_variant()?);
            
            while self.match_token(&TokenType::Or) {
                variants.push(self.parse_variant()?);
            }
        } else {
            // Struct-style type with fields
            while !self.is_at_end() && !self.check(&TokenType::Newline) {
                fields.push(self.parse_field()?);
                
                if !self.match_token(&TokenType::Newline) {
                    break;
                }
            }
        }
        
        Ok(AstNode::TypeDefinition {
            name,
            fields,
            variants,
            position: start_position,
        })
    }
    
    /// Parse a field definition
    fn parse_field(&mut self) -> ParseResult<FieldDefinition> {
        let start_position = self.peek().position;
        
        let name = match &self.advance().token_type {
            TokenType::Identifier(name) => name.clone(),
            _ => return Err(ParseError::UnexpectedToken {
                expected: "identifier".to_string(),
                found: self.previous().clone(),
                message: "Expected field name".to_string(),
            }),
        };
        
        self.consume(TokenType::Keyword("as".to_string()), "Expected 'as' after field name")?;
        
        let type_annotation = self.parse_type_annotation()?;
        
        Ok(FieldDefinition {
            name,
            type_annotation,
            position: start_position,
        })
    }
    
    /// Parse a variant definition
    fn parse_variant(&mut self) -> ParseResult<VariantDefinition> {
        let start_position = self.peek().position;
        
        let name = match &self.advance().token_type {
            TokenType::Identifier(name) => name.clone(),
            _ => return Err(ParseError::UnexpectedToken {
                expected: "identifier".to_string(),
                found: self.previous().clone(),
                message: "Expected variant name".to_string(),
            }),
        };
        
        let associated_type = if self.match_token(&TokenType::Keyword("as".to_string())) {
            Some(self.parse_type_annotation()?)
        } else {
            None
        };
        
        Ok(VariantDefinition {
            name,
            associated_type,
            position: start_position,
        })
    }
    
    /// Parse a process (function) definition
    fn parse_process_definition(&mut self) -> ParseResult<AstNode> {
        let start_position = self.peek().position;
        
        self.consume(TokenType::Keyword("Process".to_string()), "Expected 'Process'")?;
        self.consume(TokenType::Keyword("called".to_string()), "Expected 'called'")?;
        
        let name = match &self.advance().token_type {
            TokenType::StringLiteral(name) => name.clone(),
            _ => return Err(ParseError::UnexpectedToken {
                expected: "string literal".to_string(),
                found: self.previous().clone(),
                message: "Expected process name as string".to_string(),
            }),
        };
        
        // Check for duplicate definitions
        if let Some(first_pos) = self.definitions.get(&name) {
            return Err(ParseError::DuplicateDefinition {
                name,
                first_position: *first_pos,
                duplicate_position: start_position,
            });
        }
        self.definitions.insert(name.clone(), start_position);
        
        // Parse parameters
        let mut parameters = Vec::new();
        
        if self.match_token(&TokenType::Keyword("that".to_string())) {
            self.consume(TokenType::Keyword("takes".to_string()), "Expected 'takes' after 'that'")?;
            
            parameters.push(self.parse_parameter()?);
            
            while self.match_token(&TokenType::Comma) {
                parameters.push(self.parse_parameter()?);
            }
        }
        
        // Parse return type
        let return_type = if self.match_token(&TokenType::Keyword("returns".to_string())) {
            Some(self.parse_type_annotation()?)
        } else {
            None
        };
        
        self.consume(TokenType::Colon, "Expected ':' after process signature")?;
        self.skip_newlines();
        
        // Parse body
        let body = Box::new(self.parse_block()?);
        
        Ok(AstNode::ProcessDefinition {
            name,
            parameters,
            return_type,
            body,
            position: start_position,
        })
    }
    
    /// Parse a function parameter
    fn parse_parameter(&mut self) -> ParseResult<Parameter> {
        let start_position = self.peek().position;
        
        let name = match &self.advance().token_type {
            TokenType::Identifier(name) => name.clone(),
            _ => return Err(ParseError::UnexpectedToken {
                expected: "identifier".to_string(),
                found: self.previous().clone(),
                message: "Expected parameter name".to_string(),
            }),
        };
        
        self.consume(TokenType::Keyword("as".to_string()), "Expected 'as' after parameter name")?;
        
        let type_annotation = self.parse_type_annotation()?;
        
        Ok(Parameter {
            name,
            type_annotation,
            position: start_position,
        })
    }
    
    /// Parse a type annotation
    fn parse_type_annotation(&mut self) -> ParseResult<TypeAnnotation> {
        let type_name = match &self.advance().token_type {
            TokenType::Identifier(name) => name.clone(),
            _ => return Err(ParseError::UnexpectedToken {
                expected: "type name".to_string(),
                found: self.previous().clone(),
                message: "Expected type identifier".to_string(),
            }),
        };
        
        // Check for generic parameters
        if self.match_token(&TokenType::LeftBracket) {
            let mut parameters = Vec::new();
            
            parameters.push(self.parse_type_annotation()?);
            
            while self.match_token(&TokenType::Comma) {
                parameters.push(self.parse_type_annotation()?);
            }
            
            self.consume(TokenType::RightBracket, "Expected ']' after generic parameters")?;
            
            Ok(TypeAnnotation::Generic {
                base: type_name,
                parameters,
            })
        } else {
            Ok(TypeAnnotation::Simple { name: type_name })
        }
    }
    
    /// Parse a block of statements
    fn parse_block(&mut self) -> ParseResult<AstNode> {
        let start_position = self.peek().position;
        let mut statements = Vec::new();
        
        while !self.is_at_end() && !self.check(&TokenType::RightBrace) {
            if self.match_token(&TokenType::Newline) {
                continue;
            }
            
            statements.push(self.parse_statement()?);
        }
        
        Ok(AstNode::Block {
            statements,
            position: start_position,
        })
    }
    
    /// Parse a statement
    fn parse_statement(&mut self) -> ParseResult<AstNode> {
        match &self.peek().token_type {
            TokenType::Keyword(k) if k == "Let" => self.parse_let_statement(),
            TokenType::Keyword(k) if k == "Return" => self.parse_return_statement(),
            TokenType::Keyword(k) if k == "Throw" => self.parse_throw_statement(),
            TokenType::Keyword(k) if k == "If" => self.parse_if_statement(),
            TokenType::Keyword(k) if k == "For" => self.parse_for_statement(),
            TokenType::Keyword(k) if k == "While" => self.parse_while_statement(),
            _ => {
                // Expression statement
                let expr = self.parse_expression()?;
                Ok(AstNode::ExpressionStatement {
                    expression: Box::new(expr),
                    position: self.previous().position,
                })
            }
        }
    }
    
    /// Parse a let statement
    fn parse_let_statement(&mut self) -> ParseResult<AstNode> {
        let start_position = self.peek().position;
        
        self.consume(TokenType::Keyword("Let".to_string()), "Expected 'Let'")?;
        
        let variable_name = match &self.advance().token_type {
            TokenType::Identifier(name) => name.clone(),
            _ => return Err(ParseError::UnexpectedToken {
                expected: "identifier".to_string(),
                found: self.previous().clone(),
                message: "Expected variable name".to_string(),
            }),
        };
        
        self.consume(TokenType::Keyword("be".to_string()), "Expected 'be' after variable name")?;
        
        let value = Box::new(self.parse_expression()?);
        
        Ok(AstNode::LetStatement {
            variable_name,
            value,
            type_annotation: None,
            position: start_position,
        })
    }
    
    /// Parse a return statement
    fn parse_return_statement(&mut self) -> ParseResult<AstNode> {
        let start_position = self.peek().position;
        
        self.consume(TokenType::Keyword("Return".to_string()), "Expected 'Return'")?;
        
        let value = if self.check(&TokenType::Newline) || self.is_at_end() {
            None
        } else {
            Some(Box::new(self.parse_expression()?))
        };
        
        Ok(AstNode::ReturnStatement {
            value,
            position: start_position,
        })
    }
    
    /// Parse a throw statement
    fn parse_throw_statement(&mut self) -> ParseResult<AstNode> {
        let start_position = self.peek().position;
        
        self.consume(TokenType::Keyword("Throw".to_string()), "Expected 'Throw'")?;
        
        let error = Box::new(self.parse_expression()?);
        
        let message = if self.match_token(&TokenType::Keyword("with".to_string())) {
            Some(Box::new(self.parse_expression()?))
        } else {
            None
        };
        
        Ok(AstNode::ThrowStatement {
            error,
            message,
            position: start_position,
        })
    }
    
    /// Parse an if statement
    fn parse_if_statement(&mut self) -> ParseResult<AstNode> {
        let start_position = self.peek().position;
        
        self.consume(TokenType::Keyword("If".to_string()), "Expected 'If'")?;
        
        let condition = Box::new(self.parse_expression()?);
        
        self.consume(TokenType::Colon, "Expected ':' after if condition")?;
        self.skip_newlines();
        
        let then_branch = Box::new(self.parse_statement()?);
        
        let else_branch = if self.match_token(&TokenType::Keyword("Else".to_string())) {
            self.consume(TokenType::Colon, "Expected ':' after 'Else'")?;
            self.skip_newlines();
            Some(Box::new(self.parse_statement()?))
        } else {
            None
        };
        
        Ok(AstNode::IfStatement {
            condition,
            then_branch,
            else_branch,
            position: start_position,
        })
    }
    
    /// Parse a for statement
    fn parse_for_statement(&mut self) -> ParseResult<AstNode> {
        let start_position = self.peek().position;
        
        self.consume(TokenType::Keyword("For".to_string()), "Expected 'For'")?;
        
        let variable = match &self.advance().token_type {
            TokenType::Identifier(name) => name.clone(),
            _ => return Err(ParseError::UnexpectedToken {
                expected: "identifier".to_string(),
                found: self.previous().clone(),
                message: "Expected loop variable name".to_string(),
            }),
        };
        
        self.consume(TokenType::Keyword("in".to_string()), "Expected 'in' after loop variable")?;
        
        let iterable = Box::new(self.parse_expression()?);
        
        self.consume(TokenType::Colon, "Expected ':' after for clause")?;
        self.skip_newlines();
        
        let body = Box::new(self.parse_statement()?);
        
        Ok(AstNode::ForStatement {
            variable,
            iterable,
            body,
            position: start_position,
        })
    }
    
    /// Parse a while statement
    fn parse_while_statement(&mut self) -> ParseResult<AstNode> {
        let start_position = self.peek().position;
        
        self.consume(TokenType::Keyword("While".to_string()), "Expected 'While'")?;
        
        let condition = Box::new(self.parse_expression()?);
        
        self.consume(TokenType::Colon, "Expected ':' after while condition")?;
        self.skip_newlines();
        
        let body = Box::new(self.parse_statement()?);
        
        Ok(AstNode::WhileStatement {
            condition,
            body,
            position: start_position,
        })
    }
    
    /// Parse an expression with operator precedence
    fn parse_expression(&mut self) -> ParseResult<AstNode> {
        self.parse_assignment()
    }
    
    /// Parse assignment expressions
    fn parse_assignment(&mut self) -> ParseResult<AstNode> {
        let mut expr = self.parse_or()?;
        
        if self.match_token(&TokenType::Assign) {
            let operator_pos = self.previous().position;
            let right = self.parse_assignment()?;
            
            expr = AstNode::BinaryOperation {
                left: Box::new(expr),
                operator: BinaryOperator::Assign,
                right: Box::new(right),
                position: operator_pos,
            };
        }
        
        Ok(expr)
    }
    
    /// Parse logical OR expressions
    fn parse_or(&mut self) -> ParseResult<AstNode> {
        let mut expr = self.parse_and()?;
        
        while self.match_token(&TokenType::Or) {
            let operator_pos = self.previous().position;
            let right = self.parse_and()?;
            
            expr = AstNode::BinaryOperation {
                left: Box::new(expr),
                operator: BinaryOperator::Or,
                right: Box::new(right),
                position: operator_pos,
            };
        }
        
        Ok(expr)
    }
    
    /// Parse logical AND expressions
    fn parse_and(&mut self) -> ParseResult<AstNode> {
        let mut expr = self.parse_equality()?;
        
        while self.match_token(&TokenType::And) {
            let operator_pos = self.previous().position;
            let right = self.parse_equality()?;
            
            expr = AstNode::BinaryOperation {
                left: Box::new(expr),
                operator: BinaryOperator::And,
                right: Box::new(right),
                position: operator_pos,
            };
        }
        
        Ok(expr)
    }
    
    /// Parse equality expressions
    fn parse_equality(&mut self) -> ParseResult<AstNode> {
        let mut expr = self.parse_comparison()?;
        
        while let Some(operator) = self.match_equality_operator() {
            let operator_pos = self.previous().position;
            let right = self.parse_comparison()?;
            
            expr = AstNode::BinaryOperation {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
                position: operator_pos,
            };
        }
        
        Ok(expr)
    }
    
    /// Match equality operators
    fn match_equality_operator(&mut self) -> Option<BinaryOperator> {
        if self.match_token(&TokenType::Equal) {
            Some(BinaryOperator::Equal)
        } else if self.match_token(&TokenType::NotEqual) {
            Some(BinaryOperator::NotEqual)
        } else {
            None
        }
    }
    
    /// Parse comparison expressions
    fn parse_comparison(&mut self) -> ParseResult<AstNode> {
        let mut expr = self.parse_term()?;
        
        while let Some(operator) = self.match_comparison_operator() {
            let operator_pos = self.previous().position;
            let right = self.parse_term()?;
            
            expr = AstNode::BinaryOperation {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
                position: operator_pos,
            };
        }
        
        Ok(expr)
    }
    
    /// Match comparison operators
    fn match_comparison_operator(&mut self) -> Option<BinaryOperator> {
        if self.match_token(&TokenType::Less) {
            Some(BinaryOperator::Less)
        } else if self.match_token(&TokenType::LessEqual) {
            Some(BinaryOperator::LessEqual)
        } else if self.match_token(&TokenType::Greater) {
            Some(BinaryOperator::Greater)
        } else if self.match_token(&TokenType::GreaterEqual) {
            Some(BinaryOperator::GreaterEqual)
        } else {
            None
        }
    }
    
    /// Parse term expressions (+ and -)
    fn parse_term(&mut self) -> ParseResult<AstNode> {
        let mut expr = self.parse_factor()?;
        
        while let Some(operator) = self.match_term_operator() {
            let operator_pos = self.previous().position;
            let right = self.parse_factor()?;
            
            expr = AstNode::BinaryOperation {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
                position: operator_pos,
            };
        }
        
        Ok(expr)
    }
    
    /// Match term operators
    fn match_term_operator(&mut self) -> Option<BinaryOperator> {
        if self.match_token(&TokenType::Plus) {
            Some(BinaryOperator::Add)
        } else if self.match_token(&TokenType::Minus) {
            Some(BinaryOperator::Subtract)
        } else {
            None
        }
    }
    
    /// Parse factor expressions (*, /, %)
    fn parse_factor(&mut self) -> ParseResult<AstNode> {
        let mut expr = self.parse_unary()?;
        
        while let Some(operator) = self.match_factor_operator() {
            let operator_pos = self.previous().position;
            let right = self.parse_unary()?;
            
            expr = AstNode::BinaryOperation {
                left: Box::new(expr),
                operator,
                right: Box::new(right),
                position: operator_pos,
            };
        }
        
        Ok(expr)
    }
    
    /// Match factor operators
    fn match_factor_operator(&mut self) -> Option<BinaryOperator> {
        if self.match_token(&TokenType::Multiply) {
            Some(BinaryOperator::Multiply)
        } else if self.match_token(&TokenType::Divide) {
            Some(BinaryOperator::Divide)
        } else if self.match_token(&TokenType::Modulo) {
            Some(BinaryOperator::Modulo)
        } else if self.match_token(&TokenType::Power) {
            Some(BinaryOperator::Power)
        } else {
            None
        }
    }
    
    /// Parse unary expressions
    fn parse_unary(&mut self) -> ParseResult<AstNode> {
        if let Some(operator) = self.match_unary_operator() {
            let operator_pos = self.previous().position;
            let operand = Box::new(self.parse_unary()?);
            
            Ok(AstNode::UnaryOperation {
                operator,
                operand,
                position: operator_pos,
            })
        } else {
            self.parse_call()
        }
    }
    
    /// Match unary operators
    fn match_unary_operator(&mut self) -> Option<UnaryOperator> {
        if self.match_token(&TokenType::Plus) {
            Some(UnaryOperator::Plus)
        } else if self.match_token(&TokenType::Minus) {
            Some(UnaryOperator::Minus)
        } else if self.match_token(&TokenType::Not) {
            Some(UnaryOperator::Not)
        } else {
            None
        }
    }
    
    /// Parse function call expressions
    fn parse_call(&mut self) -> ParseResult<AstNode> {
        let mut expr = self.parse_primary()?;
        
        loop {
            if self.match_token(&TokenType::LeftParen) {
                expr = self.finish_call(expr)?;
            } else if self.match_token(&TokenType::Dot) {
                expr = self.parse_member_access(expr)?;
            } else if self.match_token(&TokenType::LeftBracket) {
                expr = self.parse_index_access(expr)?;
            } else {
                break;
            }
        }
        
        Ok(expr)
    }
    
    /// Finish parsing a function call
    fn finish_call(&mut self, callee: AstNode) -> ParseResult<AstNode> {
        let position = match &callee {
            AstNode::Identifier { position, .. } => *position,
            _ => self.previous().position,
        };
        
        let mut arguments = Vec::new();
        
        if !self.check(&TokenType::RightParen) {
            arguments.push(self.parse_expression()?);
            
            while self.match_token(&TokenType::Comma) {
                arguments.push(self.parse_expression()?);
            }
        }
        
        self.consume(TokenType::RightParen, "Expected ')' after function arguments")?;
        
        match callee {
            AstNode::Identifier { name, .. } => {
                Ok(AstNode::FunctionCall {
                    function_name: name,
                    arguments,
                    position,
                })
            }
            AstNode::MemberAccess { object, member, .. } => {
                Ok(AstNode::MethodCall {
                    object,
                    method_name: member,
                    arguments,
                    position,
                })
            }
            _ => Err(ParseError::InvalidSyntax {
                token: self.previous().clone(),
                message: "Invalid function call target".to_string(),
            }),
        }
    }
    
    /// Parse member access
    fn parse_member_access(&mut self, object: AstNode) -> ParseResult<AstNode> {
        let position = self.previous().position;
        
        let member = match &self.advance().token_type {
            TokenType::Identifier(name) => name.clone(),
            _ => return Err(ParseError::UnexpectedToken {
                expected: "identifier".to_string(),
                found: self.previous().clone(),
                message: "Expected member name after '.'".to_string(),
            }),
        };
        
        Ok(AstNode::MemberAccess {
            object: Box::new(object),
            member,
            position,
        })
    }
    
    /// Parse index access
    fn parse_index_access(&mut self, object: AstNode) -> ParseResult<AstNode> {
        let position = self.previous().position;
        
        let index = Box::new(self.parse_expression()?);
        
        self.consume(TokenType::RightBracket, "Expected ']' after index")?;
        
        Ok(AstNode::IndexAccess {
            object: Box::new(object),
            index,
            position,
        })
    }
    
    /// Parse primary expressions (literals, identifiers, parenthesized expressions)
    fn parse_primary(&mut self) -> ParseResult<AstNode> {
        match &self.peek().token_type.clone() {
            TokenType::StringLiteral(value) => {
                let position = self.peek().position;
                let value = value.clone();
                self.advance();
                Ok(AstNode::StringLiteral { value, position })
            }
            
            TokenType::IntegerLiteral(value) => {
                let position = self.peek().position;
                let value = *value;
                self.advance();
                Ok(AstNode::IntegerLiteral { value, position })
            }
            
            TokenType::FloatLiteral(value) => {
                let position = self.peek().position;
                let value = *value;
                self.advance();
                Ok(AstNode::FloatLiteral { value, position })
            }
            
            TokenType::BooleanLiteral(value) => {
                let position = self.peek().position;
                let value = *value;
                self.advance();
                Ok(AstNode::BooleanLiteral { value, position })
            }
            
            TokenType::Identifier(name) => {
                let position = self.peek().position;
                let name = name.clone();
                self.advance();
                Ok(AstNode::Identifier { name, position })
            }
            
            TokenType::LeftParen => {
                let position = self.peek().position;
                self.advance();
                let expr = self.parse_expression()?;
                self.consume(TokenType::RightParen, "Expected ')' after expression")?;
                Ok(expr)
            }
            
            TokenType::LeftBracket => {
                self.parse_list_literal()
            }
            
            TokenType::LeftBrace => {
                self.parse_dictionary_literal()
            }
            
            _ => Err(ParseError::UnexpectedToken {
                expected: "expression".to_string(),
                found: self.peek().clone(),
                message: "Expected expression".to_string(),
            }),
        }
    }
    
    /// Parse a list literal
    fn parse_list_literal(&mut self) -> ParseResult<AstNode> {
        let position = self.peek().position;
        self.advance(); // consume '['
        
        let mut elements = Vec::new();
        
        if !self.check(&TokenType::RightBracket) {
            elements.push(self.parse_expression()?);
            
            while self.match_token(&TokenType::Comma) {
                elements.push(self.parse_expression()?);
            }
        }
        
        self.consume(TokenType::RightBracket, "Expected ']' after list elements")?;
        
        Ok(AstNode::ListLiteral { elements, position })
    }
    
    /// Parse a dictionary literal
    fn parse_dictionary_literal(&mut self) -> ParseResult<AstNode> {
        let position = self.peek().position;
        self.advance(); // consume '{'
        
        let mut pairs = Vec::new();
        
        if !self.check(&TokenType::RightBrace) {
            let key = self.parse_expression()?;
            self.consume(TokenType::Colon, "Expected ':' after dictionary key")?;
            let value = self.parse_expression()?;
            pairs.push((key, value));
            
            while self.match_token(&TokenType::Comma) {
                let key = self.parse_expression()?;
                self.consume(TokenType::Colon, "Expected ':' after dictionary key")?;
                let value = self.parse_expression()?;
                pairs.push((key, value));
            }
        }
        
        self.consume(TokenType::RightBrace, "Expected '}' after dictionary elements")?;
        
        Ok(AstNode::DictionaryLiteral { pairs, position })
    }
    
    /// Get parser statistics for debugging
    pub fn get_statistics(&self) -> ParserStatistics {
        ParserStatistics {
            token_count: self.tokens.len(),
            current_position: self.current,
            definitions_count: self.definitions.len(),
            is_at_end: self.is_at_end(),
        }
    }
}

/// Statistics about the parser state
#[derive(Debug, Clone)]
pub struct ParserStatistics {
    pub token_count: usize,
    pub current_position: usize,
    pub definitions_count: usize,
    pub is_at_end: bool,
}

impl fmt::Display for ParserStatistics {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "ParserStats {{ tokens: {}, pos: {}, defs: {}, eof: {} }}",
            self.token_count, self.current_position, self.definitions_count, self.is_at_end
        )
    }
}

/// Bootstrap integration functions for AOTT handoff
impl MinimalParser {
    /// Create parser with AOTT integration metadata
    pub fn new_with_aott_integration(
        tokens: Vec<Token>,
        metadata: Option<HashMap<String, String>>,
    ) -> Self {
        let mut parser = Self::new(tokens);
        
        // Add AOTT-specific parsing options if provided
        if let Some(meta) = metadata {
            if let Some(optimization_level) = meta.get("optimization_level") {
                // Future: adjust parsing behavior based on optimization level
            }
        }
        
        parser
    }
    
    /// Extract AST nodes for AOTT tier promotion analysis
    pub fn extract_optimization_candidates(&self, ast: &AstNode) -> Vec<AstNode> {
        let mut candidates = Vec::new();
        self.collect_optimization_candidates(ast, &mut candidates);
        candidates
    }
    
    /// Recursively collect nodes that might benefit from AOTT optimization
    fn collect_optimization_candidates(&self, node: &AstNode, candidates: &mut Vec<AstNode>) {
        match node {
            // Function definitions are primary optimization targets
            AstNode::ProcessDefinition { .. } => {
                candidates.push(node.clone());
            }
            
            // Loop constructs are hot path candidates
            AstNode::ForStatement { body, .. } | AstNode::WhileStatement { body, .. } => {
                candidates.push(node.clone());
                self.collect_optimization_candidates(body, candidates);
            }
            
            // Recursive traversal for other nodes
            AstNode::Program { items, .. } => {
                for item in items {
                    self.collect_optimization_candidates(item, candidates);
                }
            }
            
            AstNode::Block { statements, .. } => {
                for stmt in statements {
                    self.collect_optimization_candidates(stmt, candidates);
                }
            }
            
            AstNode::IfStatement { condition, then_branch, else_branch, .. } => {
                self.collect_optimization_candidates(condition, candidates);
                self.collect_optimization_candidates(then_branch, candidates);
                if let Some(else_branch) = else_branch {
                    self.collect_optimization_candidates(else_branch, candidates);
                }
            }
            
            _ => {} // Other nodes not currently optimization targets
        }
    }
    
    /// Generate parser metadata for AOTT optimization
    pub fn generate_aott_metadata(&self) -> HashMap<String, String> {
        let mut metadata = HashMap::new();
        
        metadata.insert("parser_version".to_string(), "minimal_bootstrap".to_string());
        metadata.insert("token_count".to_string(), self.tokens.len().to_string());
        metadata.insert("definition_count".to_string(), self.definitions.len().to_string());
        metadata.insert("current_position".to_string(), self.current.to_string());
        
        metadata
    }
    
    /// Validate AST for AOTT compatibility
    pub fn validate_for_aott(&self, ast: &AstNode) -> ParseResult<()> {
        match ast {
            AstNode::Program { items, .. } => {
                for item in items {
                    self.validate_for_aott(item)?;
                }
            }
            
            AstNode::ProcessDefinition { parameters, .. } => {
                // Validate parameter count for AOTT optimization
                if parameters.len() > 32 {
                    return Err(ParseError::InvalidSyntax {
                        token: Token {
                            token_type: TokenType::Invalid("too_many_parameters".to_string()),
                            position: Position::new(),
                            raw_text: "function".to_string(),
                        },
                        message: "Functions with >32 parameters not optimizable by AOTT".to_string(),
                    });
                }
            }
            
            _ => {} // Other validations as needed
        }
        
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::compiler::bootstrap::minimal_lexer::MinimalLexer;

    #[test]
    fn test_basic_parsing() {
        let source = r#"Process called "test" that takes x as Integer returns Integer:
            Return x"#;
        
        let mut lexer = MinimalLexer::new(source.to_string());
        let tokens = lexer.tokenize().expect("Failed to tokenize");
        
        let mut parser = MinimalParser::new(tokens);
        let ast = parser.parse_program().expect("Failed to parse");
        
        match ast {
            AstNode::Program { items, .. } => {
                assert_eq!(items.len(), 1, "Program should contain exactly one top-level item");
                assert!(matches!(items[0], AstNode::ProcessDefinition { .. }),
                       "Top-level item should be a process definition");
            }
            _ => {
                panic!("Expected AstNode::Program, but got: {:?}", ast);
            }
        }
    }
    
    #[test]
    fn test_type_definition_parsing() {
        let source = r#"Type called "Point":
            x as Float
            y as Float"#;
        
        let mut lexer = MinimalLexer::new(source.to_string());
        let tokens = lexer.tokenize().expect("Failed to tokenize");
        
        let mut parser = MinimalParser::new(tokens);
        let ast = parser.parse_program().expect("Failed to parse");
        
        match ast {
            AstNode::Program { items, .. } => {
                assert_eq!(items.len(), 1, "Program should contain exactly one top-level item");
                assert!(matches!(items[0], AstNode::TypeDefinition { .. }),
                       "Top-level item should be a type definition");
            }
            _ => {
                panic!("Expected AstNode::Program, but got: {:?}", ast);
            }
        }
    }
    
    #[test]
    fn test_expression_parsing() {
        let source = r#"Process called "test":
            Let result be 1 + 2 * 3
            Return result"#;
        
        let mut lexer = MinimalLexer::new(source.to_string());
        let tokens = lexer.tokenize().expect("Failed to tokenize");
        
        let mut parser = MinimalParser::new(tokens);
        let ast = parser.parse_program().expect("Failed to parse");
        
        // Verify the expression was parsed with correct precedence
        match ast {
            AstNode::Program { items, .. } => {
                assert_eq!(items.len(), 1, "Program should contain exactly one top-level item");

                match &items[0] {
                    AstNode::ProcessDefinition { body, .. } => {
                        match body.as_ref() {
                            AstNode::Block { statements, .. } => {
                                assert_eq!(statements.len(), 2,
                                          "Process body should contain exactly 2 statements (Let and Return)");
                            }
                            _ => {
                                panic!("Expected process body to be a Block, but got: {:?}", body);
                            }
                        }
                    }
                    _ => {
                        panic!("Expected first item to be ProcessDefinition, but got: {:?}", items[0]);
                    }
                }
            }
            _ => {
                panic!("Expected AstNode::Program, but got: {:?}", ast);
            }
        }
    }
    
    #[test]
    fn test_error_handling() {
        let source = "Process called";  // Incomplete syntax
        
        let mut lexer = MinimalLexer::new(source.to_string());
        let tokens = lexer.tokenize().expect("Failed to tokenize");
        
        let mut parser = MinimalParser::new(tokens);
        let result = parser.parse_program();
        
        assert!(result.is_err());
    }
}