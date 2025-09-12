use anyhow::Result;
use std::path::Path;
use crate::utils::diagnostics::DiagnosticEngine;

#[derive(Debug, Clone, PartialEq)]
pub enum TokenType {
    // Literals
    Integer(i64),
    Float(f64),
    String(String),
    Boolean(bool),
    
    // Identifiers and Keywords
    Identifier(String),
    
    // Keywords
    Process,
    Called,
    That,
    Takes,
    Returns,
    End,
    Type,
    Let,
    Be,
    Set,
    To,
    If,
    Otherwise,
    For,
    Each,
    In,
    While,
    Match,
    When,
    Return,
    Import,
    From,
    
    // Operators
    Plus,
    Minus,
    Multiply,
    Divide,
    Modulo,
    Equal,
    NotEqual,
    LessThan,
    LessThanEqual,
    GreaterThan,
    GreaterThanEqual,
    And,
    Or,
    Not,
    
    // Delimiters
    LeftParen,
    RightParen,
    LeftBracket,
    RightBracket,
    Comma,
    Colon,
    As,
    Is,
    With,
    Dot,
    
    // Special
    Newline,
    Eof,
}

#[derive(Debug, Clone)]
pub struct Token {
    pub token_type: TokenType,
    pub line: usize,
    pub column: usize,
    pub length: usize,
}

pub struct Lexer<'a> {
    input: &'a str,
    position: usize,
    current_char: Option<char>,
    line: usize,
    column: usize,
    file_path: &'a Path,
}

impl<'a> Lexer<'a> {
    pub fn new(input: &'a str, file_path: &'a Path) -> Self {
        let mut lexer = Self {
            input,
            position: 0,
            current_char: input.chars().next(),
            line: 1,
            column: 1,
            file_path,
        };
        lexer
    }
    
    pub fn tokenize(&mut self, diagnostic_engine: &mut DiagnosticEngine) -> Result<Vec<Token>> {
        let mut tokens = Vec::new();
        
        loop {
            match self.next_token(diagnostic_engine)? {
                Some(token) => {
                    if matches!(token.token_type, TokenType::Eof) {
                        tokens.push(token);
                        break;
                    }
                    tokens.push(token);
                }
                None => break,
            }
        }
        
        Ok(tokens)
    }
    
    fn next_token(&mut self, _diagnostic_engine: &mut DiagnosticEngine) -> Result<Option<Token>> {
        self.skip_whitespace();
        
        if self.current_char.is_none() {
            return Ok(Some(self.create_token(TokenType::Eof, 0)));
        }
        
        let start_line = self.line;
        let start_column = self.column;
        
        match self.current_char.unwrap() {
            // Single character tokens
            '(' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::LeftParen,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            ')' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::RightParen,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            '[' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::LeftBracket,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            ']' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::RightBracket,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            ',' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Comma,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            ':' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Colon,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            '.' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Dot,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            '+' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Plus,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            '-' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Minus,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            '*' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Multiply,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            '/' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Divide,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            '%' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Modulo,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            '\n' => {
                self.advance();
                Ok(Some(Token {
                    token_type: TokenType::Newline,
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
            // String literals
            '"' => self.read_string(),
            // Numbers
            '0'..='9' => self.read_number(),
            // Identifiers and keywords
            'a'..='z' | 'A'..='Z' | '_' => self.read_identifier_or_keyword(),
            // Unknown character
            ch => {
                self.advance();
                // In a real implementation, we'd report an error here
                Ok(Some(Token {
                    token_type: TokenType::Identifier(ch.to_string()),
                    line: start_line,
                    column: start_column,
                    length: 1,
                }))
            }
        }
    }
    
    fn advance(&mut self) {
        if let Some(ch) = self.current_char {
            self.position += ch.len_utf8();
            if ch == '\n' {
                self.line += 1;
                self.column = 1;
            } else {
                self.column += 1;
            }
            self.current_char = self.input[self.position..].chars().next();
        }
    }
    
    fn skip_whitespace(&mut self) {
        while let Some(ch) = self.current_char {
            if ch.is_whitespace() && ch != '\n' {
                self.advance();
            } else {
                break;
            }
        }
    }
    
    fn read_string(&mut self) -> Result<Option<Token>> {
        let start_line = self.line;
        let start_column = self.column;
        self.advance(); // Skip opening quote
        
        let mut value = String::new();
        while let Some(ch) = self.current_char {
            if ch == '"' {
                self.advance(); // Skip closing quote
                return Ok(Some(Token {
                    token_type: TokenType::String(value),
                    line: start_line,
                    column: start_column,
                    length: self.column - start_column,
                }));
            }
            value.push(ch);
            self.advance();
        }
        
        // Unterminated string - in real implementation, report error
        Ok(Some(Token {
            token_type: TokenType::String(value),
            line: start_line,
            column: start_column,
            length: self.column - start_column,
        }))
    }
    
    fn read_number(&mut self) -> Result<Option<Token>> {
        let start_line = self.line;
        let start_column = self.column;
        let mut number_str = String::new();
        
        while let Some(ch) = self.current_char {
            if ch.is_ascii_digit() || ch == '.' {
                number_str.push(ch);
                self.advance();
            } else {
                break;
            }
        }
        
        if number_str.contains('.') {
            let value: f64 = number_str.parse().unwrap_or(0.0);
            Ok(Some(Token {
                token_type: TokenType::Float(value),
                line: start_line,
                column: start_column,
                length: number_str.len(),
            }))
        } else {
            let value: i64 = number_str.parse().unwrap_or(0);
            Ok(Some(Token {
                token_type: TokenType::Integer(value),
                line: start_line,
                column: start_column,
                length: number_str.len(),
            }))
        }
    }
    
    fn read_identifier_or_keyword(&mut self) -> Result<Option<Token>> {
        let start_line = self.line;
        let start_column = self.column;
        let mut identifier = String::new();
        
        while let Some(ch) = self.current_char {
            if ch.is_alphanumeric() || ch == '_' {
                identifier.push(ch);
                self.advance();
            } else {
                break;
            }
        }
        
        let token_type = match identifier.as_str() {
            "Process" => TokenType::Process,
            "called" => TokenType::Called,
            "that" => TokenType::That,
            "takes" => TokenType::Takes,
            "returns" => TokenType::Returns,
            "End" => TokenType::End,
            "Type" => TokenType::Type,
            "Let" => TokenType::Let,
            "be" => TokenType::Be,
            "Set" => TokenType::Set,
            "to" => TokenType::To,
            "If" => TokenType::If,
            "Otherwise" => TokenType::Otherwise,
            "For" => TokenType::For,
            "Each" => TokenType::Each,
            "in" => TokenType::In,
            "While" => TokenType::While,
            "Match" => TokenType::Match,
            "When" => TokenType::When,
            "Return" => TokenType::Return,
            "Import" => TokenType::Import,
            "from" => TokenType::From,
            "as" => TokenType::As,
            "is" => TokenType::Is,
            "with" => TokenType::With,
            "true" => TokenType::Boolean(true),
            "false" => TokenType::Boolean(false),
            _ => TokenType::Identifier(identifier.clone()),
        };
        
        Ok(Some(Token {
            token_type,
            line: start_line,
            column: start_column,
            length: identifier.len(),
        }))
    }
    
    fn create_token(&self, token_type: TokenType, length: usize) -> Token {
        Token {
            token_type,
            line: self.line,
            column: self.column,
            length,
        }
    }
}