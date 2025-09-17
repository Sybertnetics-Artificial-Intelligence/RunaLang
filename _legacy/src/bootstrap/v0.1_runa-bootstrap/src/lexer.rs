use anyhow::{anyhow, Result};

#[derive(Debug, Clone, PartialEq)]
pub enum TokenType {
    // Keywords
    Process,
    Let,
    Set,
    If,
    Otherwise,
    While,
    For,
    Each,
    In,
    Return,
    Break,
    Continue,
    From,
    Loop,
    Type,
    Called,
    That,
    Takes,
    Returns,
    As,
    Be,
    To,
    Is,
    End,
    Note,
    Import,
    Export,
    Match,
    When,
    WriteFile,
    ReadFile,
    List,
    Dictionary,
    Array,
    Containing,
    At,
    Index,
    Key,
    Add,
    Length,
    Of,

    // Operators (natural language)
    Plus,
    Minus,
    MultipliedBy,
    DividedBy,
    Modulo,
    IsGreaterThan,
    IsLessThan,
    IsEqualTo,
    IsNotEqualTo,
    And,
    Or,
    Not,

    // Literals
    Integer(i64),
    Float(f64),
    String(String),
    True,
    False,
    Nothing,

    // Identifiers
    Identifier(String),

    // Symbols
    Colon,
    Comma,
    Dot,
    LeftParen,
    RightParen,
    LeftBracket,
    RightBracket,
    Pipe,

    // Special
    Newline,
    Eof,
}

#[derive(Debug, Clone)]
pub struct Token {
    pub token_type: TokenType,
    pub line: usize,
    pub column: usize,
}

pub struct Lexer {
    input: Vec<char>,
    position: usize,
    line: usize,
    column: usize,
}

impl Lexer {
    pub fn new(input: &str) -> Self {
        Self {
            input: input.chars().collect(),
            position: 0,
            line: 1,
            column: 1,
        }
    }

    pub fn tokenize(&mut self) -> Result<Vec<Token>> {
        let mut tokens = Vec::new();

        while !self.is_at_end() {
            self.skip_whitespace_except_newline();

            if self.is_at_end() {
                break;
            }

            // Handle comments
            if self.peek_string("Note:") {
                self.skip_comment();
                continue;
            }

            // Check for newline
            if self.peek() == Some('\n') {
                self.advance();
                self.line += 1;
                self.column = 1;
                continue;
            }

            let token = self.next_token()?;
            if let Some(t) = token {
                tokens.push(t);
            }
        }

        tokens.push(Token {
            token_type: TokenType::Eof,
            line: self.line,
            column: self.column,
        });

        Ok(tokens)
    }

    fn next_token(&mut self) -> Result<Option<Token>> {
        let start_line = self.line;
        let start_column = self.column;

        let ch = match self.peek() {
            Some(c) => c,
            None => return Ok(None),
        };

        // Handle symbols
        match ch {
            ':' => {
                self.advance();
                return Ok(Some(Token {
                    token_type: TokenType::Colon,
                    line: start_line,
                    column: start_column,
                }));
            }
            ',' => {
                self.advance();
                return Ok(Some(Token {
                    token_type: TokenType::Comma,
                    line: start_line,
                    column: start_column,
                }));
            }
            '.' => {
                self.advance();
                return Ok(Some(Token {
                    token_type: TokenType::Dot,
                    line: start_line,
                    column: start_column,
                }));
            }
            '(' => {
                self.advance();
                return Ok(Some(Token {
                    token_type: TokenType::LeftParen,
                    line: start_line,
                    column: start_column,
                }));
            }
            ')' => {
                self.advance();
                return Ok(Some(Token {
                    token_type: TokenType::RightParen,
                    line: start_line,
                    column: start_column,
                }));
            }
            '[' => {
                self.advance();
                return Ok(Some(Token {
                    token_type: TokenType::LeftBracket,
                    line: start_line,
                    column: start_column,
                }));
            }
            ']' => {
                self.advance();
                return Ok(Some(Token {
                    token_type: TokenType::RightBracket,
                    line: start_line,
                    column: start_column,
                }));
            }
            '|' => {
                self.advance();
                return Ok(Some(Token {
                    token_type: TokenType::Pipe,
                    line: start_line,
                    column: start_column,
                }));
            }
            '"' => {
                return self.read_string_literal(start_line, start_column);
            }
            _ => {}
        }

        // Handle numbers
        if ch.is_ascii_digit() || (ch == '-' && self.peek_next().map_or(false, |c| c.is_ascii_digit())) {
            return self.read_number(start_line, start_column);
        }

        // Handle identifiers and keywords
        if ch.is_ascii_alphabetic() || ch == '_' {
            return self.read_identifier_or_keyword(start_line, start_column);
        }

        Err(anyhow!("Unexpected character '{}' at line {}, column {}", ch, start_line, start_column))
    }

    fn read_identifier_or_keyword(&mut self, start_line: usize, start_column: usize) -> Result<Option<Token>> {
        let mut word = String::new();

        while let Some(ch) = self.peek() {
            if ch.is_ascii_alphanumeric() || ch == '_' {
                word.push(ch);
                self.advance();
            } else {
                break;
            }
        }

        // Check for multi-word keywords and operators (case-sensitive for proper interop)
        let token_type = match word.as_str() {
            "Process" => TokenType::Process,
            "Let" => TokenType::Let,
            "Set" => TokenType::Set,
            "If" => TokenType::If,
            "Otherwise" => TokenType::Otherwise,
            "While" => TokenType::While,
            "For" => TokenType::For,
            "Each" => TokenType::Each,
            "in" => TokenType::In,
            "Return" => TokenType::Return,
            "Break" => TokenType::Break,
            "Continue" => TokenType::Continue,
            "from" => TokenType::From,
            "loop" => TokenType::Loop,
            "Type" => TokenType::Type,
            "called" => TokenType::Called,
            "that" => TokenType::That,
            "takes" => TokenType::Takes,
            "returns" => TokenType::Returns,
            "as" => TokenType::As,
            "be" => TokenType::Be,
            "to" => TokenType::To,
            "is" => {
                // Check for multi-word operators (case-insensitive)
                self.skip_whitespace_except_newline();
                if self.peek_string_case_insensitive("greater than") {
                    self.advance_by("greater than".len());
                    TokenType::IsGreaterThan
                } else if self.peek_string_case_insensitive("less than") {
                    self.advance_by("less than".len());
                    TokenType::IsLessThan
                } else if self.peek_string_case_insensitive("equal to") {
                    self.advance_by("equal to".len());
                    TokenType::IsEqualTo
                } else if self.peek_string_case_insensitive("not equal to") {
                    self.advance_by("not equal to".len());
                    TokenType::IsNotEqualTo
                } else {
                    TokenType::Is
                }
            }
            "plus" => TokenType::Plus,
            "minus" => TokenType::Minus,
            "multiplied" => {
                self.skip_whitespace_except_newline();
                if self.peek_string_case_insensitive("by") {
                    self.advance_by(2);
                    TokenType::MultipliedBy
                } else {
                    return Err(anyhow!("Expected 'by' after 'multiplied'"));
                }
            }
            "divided" => {
                self.skip_whitespace_except_newline();
                if self.peek_string_case_insensitive("by") {
                    self.advance_by(2);
                    TokenType::DividedBy
                } else {
                    return Err(anyhow!("Expected 'by' after 'divided'"));
                }
            }
            "modulo" => TokenType::Modulo,
            "and" => TokenType::And,
            "or" => TokenType::Or,
            "not" => TokenType::Not,
            "End" => TokenType::End,
            "Note" => TokenType::Note,
            "Import" => TokenType::Import,
            "Export" => TokenType::Export,
            "Match" => TokenType::Match,
            "When" => TokenType::When,
            "WriteFile" => TokenType::WriteFile,
            "ReadFile" => TokenType::ReadFile,
            "List" => TokenType::List,
            "Dictionary" => TokenType::Dictionary,
            "Array" => TokenType::Array,
            "containing" => TokenType::Containing,
            "at" => TokenType::At,
            "index" => TokenType::Index,
            "key" => TokenType::Key,
            "Add" => {
                // Special handling for "Add X to end of Y" pattern
                // We need to prevent "end" from being tokenized as End keyword in this context
                TokenType::Add
            }
            "length" => TokenType::Length,
            "of" => TokenType::Of,
            "true" => TokenType::True,
            "false" => TokenType::False,
            "nothing" => TokenType::Nothing,
            _ => TokenType::Identifier(word.clone()),
        };

        Ok(Some(Token {
            token_type,
            line: start_line,
            column: start_column,
        }))
    }

    fn read_number(&mut self, start_line: usize, start_column: usize) -> Result<Option<Token>> {
        let mut num_str = String::new();
        let mut is_float = false;

        // Handle negative sign
        if self.peek() == Some('-') {
            num_str.push('-');
            self.advance();
        }

        while let Some(ch) = self.peek() {
            if ch.is_ascii_digit() {
                num_str.push(ch);
                self.advance();
            } else if ch == '.' && !is_float && self.peek_next().map_or(false, |c| c.is_ascii_digit()) {
                is_float = true;
                num_str.push(ch);
                self.advance();
            } else {
                break;
            }
        }

        let token_type = if is_float {
            let value = num_str.parse::<f64>()
                .map_err(|_| anyhow!("Invalid float literal: {}", num_str))?;
            TokenType::Float(value)
        } else {
            let value = num_str.parse::<i64>()
                .map_err(|_| anyhow!("Invalid integer literal: {}", num_str))?;
            TokenType::Integer(value)
        };

        Ok(Some(Token {
            token_type,
            line: start_line,
            column: start_column,
        }))
    }

    fn read_string_literal(&mut self, start_line: usize, start_column: usize) -> Result<Option<Token>> {
        self.advance(); // Skip opening quote
        let mut value = String::new();

        while let Some(ch) = self.peek() {
            if ch == '"' {
                self.advance();
                return Ok(Some(Token {
                    token_type: TokenType::String(value),
                    line: start_line,
                    column: start_column,
                }));
            } else if ch == '\\' {
                self.advance();
                if let Some(escaped) = self.peek() {
                    match escaped {
                        'n' => value.push('\n'),
                        't' => value.push('\t'),
                        'r' => value.push('\r'),
                        '\\' => value.push('\\'),
                        '"' => value.push('"'),
                        _ => {
                            value.push('\\');
                            value.push(escaped);
                        }
                    }
                    self.advance();
                }
            } else {
                value.push(ch);
                self.advance();
                if ch == '\n' {
                    self.line += 1;
                    self.column = 1;
                }
            }
        }

        Err(anyhow!("Unterminated string literal starting at line {}", start_line))
    }

    fn skip_comment(&mut self) {
        // Skip "Note:"
        self.advance_by(5);

        // Skip until end of line
        while let Some(ch) = self.peek() {
            if ch == '\n' {
                break;
            }
            self.advance();
        }
    }

    fn skip_whitespace_except_newline(&mut self) {
        while let Some(ch) = self.peek() {
            if ch == ' ' || ch == '\t' || ch == '\r' {
                self.advance();
            } else {
                break;
            }
        }
    }

    fn peek(&self) -> Option<char> {
        if self.position < self.input.len() {
            Some(self.input[self.position])
        } else {
            None
        }
    }

    fn peek_next(&self) -> Option<char> {
        if self.position + 1 < self.input.len() {
            Some(self.input[self.position + 1])
        } else {
            None
        }
    }

    fn peek_string(&self, s: &str) -> bool {
        let chars: Vec<char> = s.chars().collect();
        if self.position + chars.len() > self.input.len() {
            return false;
        }

        for (i, &ch) in chars.iter().enumerate() {
            if self.input[self.position + i] != ch {
                return false;
            }
        }
        true
    }

    fn peek_string_case_insensitive(&self, s: &str) -> bool {
        let chars: Vec<char> = s.chars().collect();
        if self.position + chars.len() > self.input.len() {
            return false;
        }

        for (i, ch) in chars.iter().enumerate() {
            if self.input[self.position + i].to_lowercase().to_string() != ch.to_lowercase().to_string() {
                return false;
            }
        }
        true
    }

    fn advance(&mut self) {
        if self.position < self.input.len() {
            self.position += 1;
            self.column += 1;
        }
    }

    fn advance_by(&mut self, n: usize) {
        for _ in 0..n {
            self.advance();
        }
    }

    fn is_at_end(&self) -> bool {
        self.position >= self.input.len()
    }
}