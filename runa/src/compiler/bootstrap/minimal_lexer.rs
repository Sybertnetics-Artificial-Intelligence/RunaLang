//! # Minimal Lexer - Runa Bootstrap Compiler
//!
//! This module provides the minimal lexical analysis functionality needed for the
//! Runa language bootstrap compiler. It implements a complete token-based lexer
//! that can handle the essential Runa syntax required for bootstrap compilation.
//!
//! ## Key Features
//! - Complete token recognition for bootstrap Runa syntax
//! - Keyword identification and classification
//! - Literal value parsing (strings, numbers, booleans)
//! - Operator and punctuation token recognition
//! - Error handling and position tracking
//! - Memory-efficient token streaming
//! - Integration points for AOTT system handoff
//!
//! ## Bootstrap Constraints
//! This lexer is designed to be minimal (5% of total compiler system) while
//! providing complete functionality for bootstrap compilation. It focuses on:
//! - Essential Runa syntax only
//! - Fast startup and low memory usage
//! - Clean handoff to full AOTT-based compiler
//! - Comprehensive error reporting for debugging
//!
//! ## Integration with AOTT
//! This lexer provides the foundation for transitioning to the AOTT execution
//! system by producing tokens that can be processed by the minimal parser and
//! eventually handed off to the full AOTT compilation pipeline.

use std::collections::HashMap;
use std::fmt;
use std::str::Chars;
use std::iter::Peekable;

/// Position information for tokens in source code
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Position {
    /// Line number (1-based)
    pub line: usize,
    /// Column number (1-based)
    pub column: usize,
    /// Absolute byte offset in source
    pub offset: usize,
}

impl Position {
    pub fn new() -> Self {
        Position {
            line: 1,
            column: 1,
            offset: 0,
        }
    }

    pub fn advance_line(&mut self) {
        self.line += 1;
        self.column = 1;
        self.offset += 1;
    }

    pub fn advance_column(&mut self) {
        self.column += 1;
        self.offset += 1;
    }
}

impl Default for Position {
    fn default() -> Self {
        Self::new()
    }
}

impl fmt::Display for Position {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}:{}", self.line, self.column)
    }
}

/// Token types recognized by the minimal lexer
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TokenType {
    // Literals
    StringLiteral(String),
    IntegerLiteral(i64),
    FloatLiteral(f64),
    BooleanLiteral(bool),
    
    // Identifiers and Keywords
    Identifier(String),
    Keyword(String),
    
    // Operators
    Plus,
    Minus,
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
    Not,
    
    // Assignment
    Assign,
    
    // Punctuation
    LeftParen,
    RightParen,
    LeftBrace,
    RightBrace,
    LeftBracket,
    RightBracket,
    Comma,
    Semicolon,
    Colon,
    Dot,
    Arrow,
    
    // Special
    Newline,
    Whitespace,
    Comment(String),
    
    // Control
    EndOfFile,
    Invalid(String),
}

impl fmt::Display for TokenType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            TokenType::StringLiteral(s) => write!(f, "STRING({})", s),
            TokenType::IntegerLiteral(n) => write!(f, "INTEGER({})", n),
            TokenType::FloatLiteral(n) => write!(f, "FLOAT({})", n),
            TokenType::BooleanLiteral(b) => write!(f, "BOOLEAN({})", b),
            TokenType::Identifier(s) => write!(f, "IDENTIFIER({})", s),
            TokenType::Keyword(s) => write!(f, "KEYWORD({})", s),
            TokenType::Plus => write!(f, "PLUS"),
            TokenType::Minus => write!(f, "MINUS"),
            TokenType::Multiply => write!(f, "MULTIPLY"),
            TokenType::Divide => write!(f, "DIVIDE"),
            TokenType::Modulo => write!(f, "MODULO"),
            TokenType::Power => write!(f, "POWER"),
            TokenType::Equal => write!(f, "EQUAL"),
            TokenType::NotEqual => write!(f, "NOT_EQUAL"),
            TokenType::Less => write!(f, "LESS"),
            TokenType::LessEqual => write!(f, "LESS_EQUAL"),
            TokenType::Greater => write!(f, "GREATER"),
            TokenType::GreaterEqual => write!(f, "GREATER_EQUAL"),
            TokenType::And => write!(f, "AND"),
            TokenType::Or => write!(f, "OR"),
            TokenType::Not => write!(f, "NOT"),
            TokenType::Assign => write!(f, "ASSIGN"),
            TokenType::LeftParen => write!(f, "LEFT_PAREN"),
            TokenType::RightParen => write!(f, "RIGHT_PAREN"),
            TokenType::LeftBrace => write!(f, "LEFT_BRACE"),
            TokenType::RightBrace => write!(f, "RIGHT_BRACE"),
            TokenType::LeftBracket => write!(f, "LEFT_BRACKET"),
            TokenType::RightBracket => write!(f, "RIGHT_BRACKET"),
            TokenType::Comma => write!(f, "COMMA"),
            TokenType::Semicolon => write!(f, "SEMICOLON"),
            TokenType::Colon => write!(f, "COLON"),
            TokenType::Dot => write!(f, "DOT"),
            TokenType::Arrow => write!(f, "ARROW"),
            TokenType::Newline => write!(f, "NEWLINE"),
            TokenType::Whitespace => write!(f, "WHITESPACE"),
            TokenType::Comment(s) => write!(f, "COMMENT({})", s),
            TokenType::EndOfFile => write!(f, "EOF"),
            TokenType::Invalid(s) => write!(f, "INVALID({})", s),
        }
    }
}

/// A token with its type, position, and raw text
#[derive(Debug, Clone, PartialEq)]
pub struct Token {
    pub token_type: TokenType,
    pub position: Position,
    pub raw_text: String,
}

impl Token {
    pub fn new(token_type: TokenType, position: Position, raw_text: String) -> Self {
        Token {
            token_type,
            position,
            raw_text,
        }
    }
}

impl fmt::Display for Token {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} at {}", self.token_type, self.position)
    }
}

/// Lexical analysis errors
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LexerError {
    UnterminatedString {
        position: Position,
        message: String,
    },
    InvalidNumber {
        position: Position,
        raw_text: String,
        message: String,
    },
    InvalidCharacter {
        position: Position,
        character: char,
        message: String,
    },
    InvalidEscape {
        position: Position,
        escape_sequence: String,
        message: String,
    },
    UnexpectedEndOfFile {
        position: Position,
        context: String,
    },
    InvalidToken {
        position: Position,
        raw_text: String,
        message: String,
    },
}

impl fmt::Display for LexerError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            LexerError::UnterminatedString { position, message } => {
                write!(f, "Unterminated string at {}: {}", position, message)
            }
            LexerError::InvalidNumber { position, raw_text, message } => {
                write!(f, "Invalid number '{}' at {}: {}", raw_text, position, message)
            }
            LexerError::InvalidCharacter { position, character, message } => {
                write!(f, "Invalid character '{}' at {}: {}", character, position, message)
            }
            LexerError::InvalidEscape { position, escape_sequence, message } => {
                write!(f, "Invalid escape sequence '{}' at {}: {}", escape_sequence, position, message)
            }
            LexerError::UnexpectedEndOfFile { position, context } => {
                write!(f, "Unexpected end of file at {} while parsing {}", position, context)
            }
            LexerError::InvalidToken { position, raw_text, message } => {
                write!(f, "Invalid token '{}' at {}: {}", raw_text, position, message)
            }
        }
    }
}

impl std::error::Error for LexerError {}

/// Result type for lexer operations
pub type LexerResult<T> = Result<T, LexerError>;

/// The minimal lexer for Runa bootstrap compilation
pub struct MinimalLexer {
    input: String,
    chars: Peekable<Chars<'static>>,
    position: Position,
    keywords: HashMap<String, String>,
    current_char: Option<char>,
    eof_reached: bool,
}

impl MinimalLexer {
    /// Create a new minimal lexer from source code
    pub fn new(input: String) -> Self {
        let keywords = Self::initialize_keywords();
        
        // SAFETY: We ensure the input string lives for the duration of the lexer
        let static_input: &'static str = unsafe { std::mem::transmute(input.as_str()) };
        let chars = static_input.chars().peekable();
        
        let mut lexer = MinimalLexer {
            input,
            chars,
            position: Position::new(),
            keywords,
            current_char: None,
            eof_reached: false,
        };
        
        // Initialize first character
        lexer.advance_char();
        lexer
    }
    
    /// Initialize the keyword map with essential Runa keywords
    fn initialize_keywords() -> HashMap<String, String> {
        let mut keywords = HashMap::new();
        
        // Core language keywords
        keywords.insert("Process".to_string(), "Process".to_string());
        keywords.insert("Type".to_string(), "Type".to_string());
        keywords.insert("Import".to_string(), "Import".to_string());
        keywords.insert("Let".to_string(), "Let".to_string());
        keywords.insert("Return".to_string(), "Return".to_string());
        keywords.insert("If".to_string(), "If".to_string());
        keywords.insert("Else".to_string(), "Else".to_string());
        keywords.insert("For".to_string(), "For".to_string());
        keywords.insert("While".to_string(), "While".to_string());
        keywords.insert("Match".to_string(), "Match".to_string());
        keywords.insert("Throw".to_string(), "Throw".to_string());
        keywords.insert("Try".to_string(), "Try".to_string());
        keywords.insert("Catch".to_string(), "Catch".to_string());
        
        // Data type keywords
        keywords.insert("String".to_string(), "String".to_string());
        keywords.insert("Integer".to_string(), "Integer".to_string());
        keywords.insert("Float".to_string(), "Float".to_string());
        keywords.insert("Boolean".to_string(), "Boolean".to_string());
        keywords.insert("List".to_string(), "List".to_string());
        keywords.insert("Dictionary".to_string(), "Dictionary".to_string());
        
        // Boolean literals
        keywords.insert("True".to_string(), "True".to_string());
        keywords.insert("False".to_string(), "False".to_string());
        
        // Control flow
        keywords.insert("that".to_string(), "that".to_string());
        keywords.insert("takes".to_string(), "takes".to_string());
        keywords.insert("returns".to_string(), "returns".to_string());
        keywords.insert("called".to_string(), "called".to_string());
        keywords.insert("as".to_string(), "as".to_string());
        keywords.insert("be".to_string(), "be".to_string());
        keywords.insert("with".to_string(), "with".to_string());
        keywords.insert("is".to_string(), "is".to_string());
        
        keywords
    }
    
    /// Advance to the next character in the input
    fn advance_char(&mut self) {
        if self.eof_reached {
            self.current_char = None;
            return;
        }
        
        if let Some(ch) = self.chars.next() {
            self.current_char = Some(ch);
            
            if ch == '\n' {
                self.position.advance_line();
            } else {
                self.position.advance_column();
            }
        } else {
            self.current_char = None;
            self.eof_reached = true;
        }
    }
    
    /// Peek at the next character without advancing
    fn peek_char(&mut self) -> Option<char> {
        self.chars.peek().copied()
    }
    
    /// Skip whitespace characters (except newlines which are significant)
    fn skip_whitespace(&mut self) {
        while let Some(ch) = self.current_char {
            if ch.is_whitespace() && ch != '\n' {
                self.advance_char();
            } else {
                break;
            }
        }
    }
    
    /// Scan a string literal with escape sequence handling
    fn scan_string_literal(&mut self, quote_char: char) -> LexerResult<String> {
        let start_pos = self.position;
        let mut value = String::new();
        
        // Skip opening quote
        self.advance_char();
        
        while let Some(ch) = self.current_char {
            if ch == quote_char {
                // End of string
                self.advance_char();
                return Ok(value);
            } else if ch == '\\' {
                // Handle escape sequences
                self.advance_char();
                
                match self.current_char {
                    Some('n') => {
                        value.push('\n');
                        self.advance_char();
                    }
                    Some('t') => {
                        value.push('\t');
                        self.advance_char();
                    }
                    Some('r') => {
                        value.push('\r');
                        self.advance_char();
                    }
                    Some('\\') => {
                        value.push('\\');
                        self.advance_char();
                    }
                    Some('"') => {
                        value.push('"');
                        self.advance_char();
                    }
                    Some('\'') => {
                        value.push('\'');
                        self.advance_char();
                    }
                    Some(escape_char) => {
                        return Err(LexerError::InvalidEscape {
                            position: self.position,
                            escape_sequence: format!("\\{}", escape_char),
                            message: format!("Unknown escape sequence '\\{}'", escape_char),
                        });
                    }
                    None => {
                        return Err(LexerError::UnexpectedEndOfFile {
                            position: self.position,
                            context: "string literal escape sequence".to_string(),
                        });
                    }
                }
            } else if ch == '\n' {
                return Err(LexerError::UnterminatedString {
                    position: start_pos,
                    message: "String literal cannot span multiple lines".to_string(),
                });
            } else {
                value.push(ch);
                self.advance_char();
            }
        }
        
        Err(LexerError::UnterminatedString {
            position: start_pos,
            message: format!("Unterminated string literal starting with '{}'", quote_char),
        })
    }
    
    /// Scan a numeric literal (integer or float)
    fn scan_numeric_literal(&mut self) -> LexerResult<TokenType> {
        let start_pos = self.position;
        let mut number_text = String::new();
        let mut is_float = false;
        
        // Collect digits and decimal point
        while let Some(ch) = self.current_char {
            if ch.is_ascii_digit() {
                number_text.push(ch);
                self.advance_char();
            } else if ch == '.' && !is_float && self.peek_char().map_or(false, |c| c.is_ascii_digit()) {
                is_float = true;
                number_text.push(ch);
                self.advance_char();
            } else {
                break;
            }
        }
        
        if number_text.is_empty() {
            return Err(LexerError::InvalidNumber {
                position: start_pos,
                raw_text: number_text,
                message: "Empty number literal".to_string(),
            });
        }
        
        if is_float {
            match number_text.parse::<f64>() {
                Ok(value) => Ok(TokenType::FloatLiteral(value)),
                Err(_) => Err(LexerError::InvalidNumber {
                    position: start_pos,
                    raw_text: number_text,
                    message: "Invalid floating-point number format".to_string(),
                }),
            }
        } else {
            match number_text.parse::<i64>() {
                Ok(value) => Ok(TokenType::IntegerLiteral(value)),
                Err(_) => Err(LexerError::InvalidNumber {
                    position: start_pos,
                    raw_text: number_text,
                    message: "Invalid integer number format or out of range".to_string(),
                }),
            }
        }
    }
    
    /// Scan an identifier or keyword
    fn scan_identifier(&mut self) -> LexerResult<TokenType> {
        let mut identifier = String::new();
        
        // First character must be letter or underscore
        if let Some(ch) = self.current_char {
            if ch.is_alphabetic() || ch == '_' {
                identifier.push(ch);
                self.advance_char();
            } else {
                return Err(LexerError::InvalidCharacter {
                    position: self.position,
                    character: ch,
                    message: "Identifier must start with letter or underscore".to_string(),
                });
            }
        }
        
        // Subsequent characters can be alphanumeric or underscore
        while let Some(ch) = self.current_char {
            if ch.is_alphanumeric() || ch == '_' {
                identifier.push(ch);
                self.advance_char();
            } else {
                break;
            }
        }
        
        // Check if it's a keyword
        if let Some(keyword) = self.keywords.get(&identifier) {
            // Handle boolean literals specially
            if keyword == "True" {
                Ok(TokenType::BooleanLiteral(true))
            } else if keyword == "False" {
                Ok(TokenType::BooleanLiteral(false))
            } else {
                Ok(TokenType::Keyword(keyword.clone()))
            }
        } else {
            Ok(TokenType::Identifier(identifier))
        }
    }
    
    /// Scan a comment (Note: style)
    fn scan_comment(&mut self) -> LexerResult<TokenType> {
        let mut comment = String::new();
        
        // Skip "Note:"
        if self.current_char == Some('N') {
            let mut temp = String::new();
            for _ in 0..5 {
                if let Some(ch) = self.current_char {
                    temp.push(ch);
                    self.advance_char();
                } else {
                    break;
                }
            }
            
            if temp == "Note:" {
                // Collect rest of line
                while let Some(ch) = self.current_char {
                    if ch == '\n' {
                        break;
                    }
                    comment.push(ch);
                    self.advance_char();
                }
                
                Ok(TokenType::Comment(comment.trim().to_string()))
            } else {
                // Not a comment, backtrack and treat as identifier
                // This is a simplification - in a production lexer we'd handle this better
                Err(LexerError::InvalidToken {
                    position: self.position,
                    raw_text: temp,
                    message: "Invalid token sequence".to_string(),
                })
            }
        } else {
            Err(LexerError::InvalidCharacter {
                position: self.position,
                character: self.current_char.unwrap_or('\0'),
                message: "Expected 'Note:' for comment".to_string(),
            })
        }
    }
    
    /// Scan the next token from the input
    pub fn next_token(&mut self) -> LexerResult<Token> {
        // Skip whitespace (but preserve newlines)
        self.skip_whitespace();
        
        let token_start = self.position;
        
        match self.current_char {
            None => {
                Ok(Token::new(
                    TokenType::EndOfFile,
                    token_start,
                    "".to_string(),
                ))
            }
            
            Some('\n') => {
                self.advance_char();
                Ok(Token::new(
                    TokenType::Newline,
                    token_start,
                    "\n".to_string(),
                ))
            }
            
            Some('"') => {
                let value = self.scan_string_literal('"')?;
                Ok(Token::new(
                    TokenType::StringLiteral(value.clone()),
                    token_start,
                    format!("\"{}\"", value),
                ))
            }
            
            Some('\'') => {
                let value = self.scan_string_literal('\'')?;
                Ok(Token::new(
                    TokenType::StringLiteral(value.clone()),
                    token_start,
                    format!("'{}'", value),
                ))
            }
            
            Some(ch) if ch.is_ascii_digit() => {
                let token_type = self.scan_numeric_literal()?;
                let raw_text = match &token_type {
                    TokenType::IntegerLiteral(n) => n.to_string(),
                    TokenType::FloatLiteral(n) => n.to_string(),
                    _ => unreachable!(),
                };
                Ok(Token::new(token_type, token_start, raw_text))
            }
            
            Some(ch) if ch.is_alphabetic() || ch == '_' => {
                // Special case for "Note:" comments
                if ch == 'N' && self.input[self.position.offset..].starts_with("Note:") {
                    let token_type = self.scan_comment()?;
                    let raw_text = match &token_type {
                        TokenType::Comment(c) => format!("Note: {}", c),
                        _ => unreachable!(),
                    };
                    Ok(Token::new(token_type, token_start, raw_text))
                } else {
                    let token_type = self.scan_identifier()?;
                    let raw_text = match &token_type {
                        TokenType::Identifier(s) => s.clone(),
                        TokenType::Keyword(s) => s.clone(),
                        TokenType::BooleanLiteral(true) => "True".to_string(),
                        TokenType::BooleanLiteral(false) => "False".to_string(),
                        _ => unreachable!(),
                    };
                    Ok(Token::new(token_type, token_start, raw_text))
                }
            }
            
            // Single-character tokens
            Some('+') => {
                self.advance_char();
                Ok(Token::new(TokenType::Plus, token_start, "+".to_string()))
            }
            Some('-') => {
                // Check for arrow (->) 
                if self.peek_char() == Some('>') {
                    self.advance_char();
                    self.advance_char();
                    Ok(Token::new(TokenType::Arrow, token_start, "->".to_string()))
                } else {
                    self.advance_char();
                    Ok(Token::new(TokenType::Minus, token_start, "-".to_string()))
                }
            }
            Some('*') => {
                self.advance_char();
                Ok(Token::new(TokenType::Multiply, token_start, "*".to_string()))
            }
            Some('/') => {
                self.advance_char();
                Ok(Token::new(TokenType::Divide, token_start, "/".to_string()))
            }
            Some('%') => {
                self.advance_char();
                Ok(Token::new(TokenType::Modulo, token_start, "%".to_string()))
            }
            Some('^') => {
                self.advance_char();
                Ok(Token::new(TokenType::Power, token_start, "^".to_string()))
            }
            
            // Comparison operators
            Some('=') => {
                if self.peek_char() == Some('=') {
                    self.advance_char();
                    self.advance_char();
                    Ok(Token::new(TokenType::Equal, token_start, "==".to_string()))
                } else {
                    self.advance_char();
                    Ok(Token::new(TokenType::Assign, token_start, "=".to_string()))
                }
            }
            Some('!') => {
                if self.peek_char() == Some('=') {
                    self.advance_char();
                    self.advance_char();
                    Ok(Token::new(TokenType::NotEqual, token_start, "!=".to_string()))
                } else {
                    self.advance_char();
                    Ok(Token::new(TokenType::Not, token_start, "!".to_string()))
                }
            }
            Some('<') => {
                if self.peek_char() == Some('=') {
                    self.advance_char();
                    self.advance_char();
                    Ok(Token::new(TokenType::LessEqual, token_start, "<=".to_string()))
                } else {
                    self.advance_char();
                    Ok(Token::new(TokenType::Less, token_start, "<".to_string()))
                }
            }
            Some('>') => {
                if self.peek_char() == Some('=') {
                    self.advance_char();
                    self.advance_char();
                    Ok(Token::new(TokenType::GreaterEqual, token_start, ">=".to_string()))
                } else {
                    self.advance_char();
                    Ok(Token::new(TokenType::Greater, token_start, ">".to_string()))
                }
            }
            
            // Logical operators
            Some('&') => {
                if self.peek_char() == Some('&') {
                    self.advance_char();
                    self.advance_char();
                    Ok(Token::new(TokenType::And, token_start, "&&".to_string()))
                } else {
                    Err(LexerError::InvalidCharacter {
                        position: token_start,
                        character: '&',
                        message: "Single '&' not supported, use '&&' for logical AND".to_string(),
                    })
                }
            }
            Some('|') => {
                if self.peek_char() == Some('|') {
                    self.advance_char();
                    self.advance_char();
                    Ok(Token::new(TokenType::Or, token_start, "||".to_string()))
                } else {
                    Err(LexerError::InvalidCharacter {
                        position: token_start,
                        character: '|',
                        message: "Single '|' not supported, use '||' for logical OR".to_string(),
                    })
                }
            }
            
            // Punctuation
            Some('(') => {
                self.advance_char();
                Ok(Token::new(TokenType::LeftParen, token_start, "(".to_string()))
            }
            Some(')') => {
                self.advance_char();
                Ok(Token::new(TokenType::RightParen, token_start, ")".to_string()))
            }
            Some('{') => {
                self.advance_char();
                Ok(Token::new(TokenType::LeftBrace, token_start, "{".to_string()))
            }
            Some('}') => {
                self.advance_char();
                Ok(Token::new(TokenType::RightBrace, token_start, "}".to_string()))
            }
            Some('[') => {
                self.advance_char();
                Ok(Token::new(TokenType::LeftBracket, token_start, "[".to_string()))
            }
            Some(']') => {
                self.advance_char();
                Ok(Token::new(TokenType::RightBracket, token_start, "]".to_string()))
            }
            Some(',') => {
                self.advance_char();
                Ok(Token::new(TokenType::Comma, token_start, ",".to_string()))
            }
            Some(';') => {
                self.advance_char();
                Ok(Token::new(TokenType::Semicolon, token_start, ";".to_string()))
            }
            Some(':') => {
                self.advance_char();
                Ok(Token::new(TokenType::Colon, token_start, ":".to_string()))
            }
            Some('.') => {
                self.advance_char();
                Ok(Token::new(TokenType::Dot, token_start, ".".to_string()))
            }
            
            // Invalid character
            Some(ch) => {
                self.advance_char();
                Err(LexerError::InvalidCharacter {
                    position: token_start,
                    character: ch,
                    message: format!("Unexpected character '{}'", ch),
                })
            }
        }
    }
    
    /// Tokenize the entire input and return a vector of tokens
    pub fn tokenize(&mut self) -> LexerResult<Vec<Token>> {
        let mut tokens = Vec::new();
        
        loop {
            let token = self.next_token()?;
            let is_eof = matches!(token.token_type, TokenType::EndOfFile);
            
            tokens.push(token);
            
            if is_eof {
                break;
            }
        }
        
        Ok(tokens)
    }
    
    /// Filter tokens to remove whitespace and comments (for parsing)
    pub fn filter_tokens(tokens: Vec<Token>) -> Vec<Token> {
        tokens
            .into_iter()
            .filter(|token| {
                !matches!(
                    token.token_type,
                    TokenType::Whitespace | TokenType::Comment(_)
                )
            })
            .collect()
    }
    
    /// Get lexer statistics for debugging
    pub fn get_statistics(&self) -> LexerStatistics {
        LexerStatistics {
            current_position: self.position,
            eof_reached: self.eof_reached,
            input_length: self.input.len(),
            keywords_count: self.keywords.len(),
        }
    }
}

/// Statistics about the lexer state
#[derive(Debug, Clone)]
pub struct LexerStatistics {
    pub current_position: Position,
    pub eof_reached: bool,
    pub input_length: usize,
    pub keywords_count: usize,
}

impl fmt::Display for LexerStatistics {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "LexerStats {{ position: {}, eof: {}, input_len: {}, keywords: {} }}",
            self.current_position, self.eof_reached, self.input_length, self.keywords_count
        )
    }
}

/// Bootstrap integration functions for AOTT handoff
impl MinimalLexer {
    /// Create lexer with AOTT integration metadata
    pub fn new_with_aott_integration(
        input: String,
        metadata: Option<HashMap<String, String>>,
    ) -> Self {
        let mut lexer = Self::new(input);
        
        // Add AOTT-specific keywords if provided
        if let Some(meta) = metadata {
            if let Some(extra_keywords) = meta.get("extra_keywords") {
                for keyword in extra_keywords.split(',') {
                    let keyword = keyword.trim().to_string();
                    lexer.keywords.insert(keyword.clone(), keyword);
                }
            }
        }
        
        lexer
    }
    
    /// Extract tokens for AOTT tier promotion analysis
    pub fn extract_promotion_candidates(&mut self) -> LexerResult<Vec<Token>> {
        let tokens = self.tokenize()?;
        
        // Filter for tokens that might indicate hot code paths
        let candidates: Vec<Token> = tokens
            .into_iter()
            .filter(|token| {
                matches!(
                    token.token_type,
                    TokenType::Keyword(ref k) if k == "Process" || k == "For" || k == "While"
                )
            })
            .collect();
        
        Ok(candidates)
    }
    
    /// Generate lexer metadata for AOTT optimization
    pub fn generate_aott_metadata(&self) -> HashMap<String, String> {
        let mut metadata = HashMap::new();
        
        metadata.insert("lexer_version".to_string(), "minimal_bootstrap".to_string());
        metadata.insert("input_length".to_string(), self.input.len().to_string());
        metadata.insert("keyword_count".to_string(), self.keywords.len().to_string());
        metadata.insert("position".to_string(), format!("{}:{}", self.position.line, self.position.column));
        
        metadata
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_tokenization() {
        let source = r#"Process called "test" that takes x as Integer returns Integer:
            Let result be x + 1
            Return result"#;

        let mut lexer = MinimalLexer::new(source.to_string());
        let tokens = lexer.tokenize().expect("Failed to tokenize");

        // Verify we have tokens
        assert!(!tokens.is_empty());

        // Should have more than just EOF
        assert!(tokens.len() > 1);

        // Last token should be EOF
        assert!(matches!(tokens.last().unwrap().token_type, TokenType::EndOfFile));

        // Check for key tokens that should be present
        let has_process = tokens.iter().any(|t| matches!(t.token_type, TokenType::Keyword(ref k) if k == "Process"));
        assert!(has_process, "Should contain Process keyword");

        let has_string = tokens.iter().any(|t| matches!(t.token_type, TokenType::StringLiteral(_)));
        assert!(has_string, "Should contain string literal 'test'");

        let has_identifier = tokens.iter().any(|t| matches!(t.token_type, TokenType::Identifier(ref s) if s == "x"));
        assert!(has_identifier, "Should contain identifier 'x'");

        let has_plus = tokens.iter().any(|t| matches!(t.token_type, TokenType::Plus));
        assert!(has_plus, "Should contain Plus operator");

        let has_integer_literal = tokens.iter().any(|t| matches!(t.token_type, TokenType::IntegerLiteral(1)));
        assert!(has_integer_literal, "Should contain integer literal 1");

        // Check for keyword tokens
        let keyword_count = tokens.iter()
            .filter(|t| matches!(t.token_type, TokenType::Keyword(_)))
            .count();
        assert!(keyword_count >= 6, "Should have at least 6 keywords: Process, called, that, takes, as, returns, Let, Return");

        // Check for newlines (significant in Runa)
        let newline_count = tokens.iter()
            .filter(|t| matches!(t.token_type, TokenType::Newline))
            .count();
        assert!(newline_count >= 2, "Should have at least 2 newlines");

        // Verify token positions are reasonable
        for (i, token) in tokens.iter().enumerate() {
            assert!(token.position.line >= 1, "Token {} should have valid line number", i);
            assert!(token.position.column >= 1, "Token {} should have valid column number", i);
        }
    }
    
    #[test]
    fn test_keyword_recognition() {
        let source = "Process Type Import Let Return";
        let mut lexer = MinimalLexer::new(source.to_string());
        let tokens = lexer.tokenize().expect("Failed to tokenize");
        
        let keywords: Vec<&Token> = tokens
            .iter()
            .filter(|t| matches!(t.token_type, TokenType::Keyword(_)))
            .collect();
        
        assert_eq!(keywords.len(), 5);
    }
    
    #[test]
    fn test_string_literals() {
        let source = r#""hello world" 'single quotes'"#;
        let mut lexer = MinimalLexer::new(source.to_string());
        let tokens = lexer.tokenize().expect("Failed to tokenize");
        
        let strings: Vec<&Token> = tokens
            .iter()
            .filter(|t| matches!(t.token_type, TokenType::StringLiteral(_)))
            .collect();
        
        assert_eq!(strings.len(), 2);
    }
    
    #[test]
    fn test_numeric_literals() {
        let source = "42 3.14 -17";
        let mut lexer = MinimalLexer::new(source.to_string());
        let tokens = lexer.tokenize().expect("Failed to tokenize");
        
        let numbers: Vec<&Token> = tokens
            .iter()
            .filter(|t| {
                matches!(
                    t.token_type,
                    TokenType::IntegerLiteral(_) | TokenType::FloatLiteral(_)
                )
            })
            .collect();
        
        assert_eq!(numbers.len(), 2); // -17 is tokenized as minus and 17
    }
    
    #[test]
    fn test_error_handling() {
        let source = r#""unterminated string"#;
        let mut lexer = MinimalLexer::new(source.to_string());
        let result = lexer.tokenize();
        
        assert!(result.is_err());
        assert!(matches!(result.unwrap_err(), LexerError::UnterminatedString { .. }));
    }
}