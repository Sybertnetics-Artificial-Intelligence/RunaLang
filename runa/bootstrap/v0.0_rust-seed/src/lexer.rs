#[derive(Debug, Clone, PartialEq)]
pub enum TokenType {
    // Keywords
    Let,
    Be,
    Set,
    To,
    Print,

    // Control flow
    If,
    Otherwise,
    End,
    While,
    Return,

    // Function definition
    Process,
    Called,
    That,
    Takes,
    Returns,

    // List operations
    List,
    Containing,
    And,

    // Punctuation
    LeftParen,
    RightParen,
    Comma,
    Colon,

    // Arithmetic operators
    Plus,
    Minus,

    // Comparison operators (natural language)
    IsEqualTo,
    IsNotEqualTo,
    IsLessThan,
    IsGreaterThan,

    // Literals
    Integer(i64),
    StringLiteral(String),
    Identifier(String),

    // End of file
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

    pub fn tokenize(&mut self) -> Result<Vec<Token>, String> {
        let mut tokens = Vec::new();

        while !self.is_at_end() {
            self.skip_whitespace();

            if self.is_at_end() {
                break;
            }

            let token = self.next_token()?;
            tokens.push(token);
        }

        tokens.push(Token {
            token_type: TokenType::Eof,
            line: self.line,
            column: self.column,
        });

        Ok(tokens)
    }

    fn next_token(&mut self) -> Result<Token, String> {
        let line = self.line;
        let column = self.column;

        let ch = self.current_char();

        if ch.is_ascii_alphabetic() || ch == '_' {
            return self.read_identifier_or_keyword();
        }

        if ch.is_ascii_digit() {
            return self.read_integer();
        }

        if ch == '"' {
            return self.read_string_literal();
        }

        // Handle punctuation
        let token_type = match ch {
            '(' => {
                self.advance();
                TokenType::LeftParen
            }
            ')' => {
                self.advance();
                TokenType::RightParen
            }
            ',' => {
                self.advance();
                TokenType::Comma
            }
            ':' => {
                self.advance();
                TokenType::Colon
            }
            _ => return Err(format!("Unexpected character '{}' at line {}, column {}", ch, line, column)),
        };

        Ok(Token {
            token_type,
            line,
            column,
        })
    }

    fn read_identifier_or_keyword(&mut self) -> Result<Token, String> {
        let line = self.line;
        let column = self.column;
        let mut value = String::new();

        while !self.is_at_end() && (self.current_char().is_ascii_alphanumeric() || self.current_char() == '_') {
            value.push(self.current_char());
            self.advance();
        }

        let token_type = match value.as_str() {
            "Let" => TokenType::Let,
            "be" => TokenType::Be,
            "Set" => TokenType::Set,
            "to" => TokenType::To,
            "Print" => TokenType::Print,
            "If" => TokenType::If,
            "Otherwise" => TokenType::Otherwise,
            "End" => TokenType::End,
            "While" => TokenType::While,
            "Return" => TokenType::Return,
            "Process" => TokenType::Process,
            "called" => TokenType::Called,
            "that" => TokenType::That,
            "takes" => TokenType::Takes,
            "returns" => TokenType::Returns,
            "list" => TokenType::List,
            "containing" => TokenType::Containing,
            "and" => TokenType::And,
            "plus" => TokenType::Plus,
            "minus" => TokenType::Minus,
            "is" => {
                // Handle multi-word comparison operators
                if self.peek_ahead_matches(&["equal", "to"]) {
                    self.advance_word(); // consume "equal"
                    self.advance_word(); // consume "to"
                    TokenType::IsEqualTo
                } else if self.peek_ahead_matches(&["not", "equal", "to"]) {
                    self.advance_word(); // consume "not"
                    self.advance_word(); // consume "equal"
                    self.advance_word(); // consume "to"
                    TokenType::IsNotEqualTo
                } else if self.peek_ahead_matches(&["less", "than"]) {
                    self.advance_word(); // consume "less"
                    self.advance_word(); // consume "than"
                    TokenType::IsLessThan
                } else if self.peek_ahead_matches(&["greater", "than"]) {
                    self.advance_word(); // consume "greater"
                    self.advance_word(); // consume "than"
                    TokenType::IsGreaterThan
                } else {
                    TokenType::Identifier(value)
                }
            }
            _ => TokenType::Identifier(value),
        };

        Ok(Token {
            token_type,
            line,
            column,
        })
    }

    fn read_integer(&mut self) -> Result<Token, String> {
        let line = self.line;
        let column = self.column;
        let mut value = String::new();

        while !self.is_at_end() && self.current_char().is_ascii_digit() {
            value.push(self.current_char());
            self.advance();
        }

        match value.parse::<i64>() {
            Ok(num) => Ok(Token {
                token_type: TokenType::Integer(num),
                line,
                column,
            }),
            Err(_) => Err(format!("Invalid integer '{}' at line {}, column {}", value, line, column)),
        }
    }

    fn read_string_literal(&mut self) -> Result<Token, String> {
        let line = self.line;
        let column = self.column;
        let mut value = String::new();

        // Consume opening quote
        self.advance();

        while !self.is_at_end() && self.current_char() != '"' {
            let ch = self.current_char();
            if ch == '\\' {
                // Handle escape sequences
                self.advance();
                if !self.is_at_end() {
                    match self.current_char() {
                        'n' => value.push('\n'),
                        't' => value.push('\t'),
                        'r' => value.push('\r'),
                        '\\' => value.push('\\'),
                        '"' => value.push('"'),
                        _ => {
                            value.push('\\');
                            value.push(self.current_char());
                        }
                    }
                    self.advance();
                }
            } else {
                value.push(ch);
                self.advance();
            }
        }

        if self.is_at_end() {
            return Err(format!("Unterminated string literal at line {}, column {}", line, column));
        }

        // Consume closing quote
        self.advance();

        Ok(Token {
            token_type: TokenType::StringLiteral(value),
            line,
            column,
        })
    }

    fn skip_whitespace(&mut self) {
        while !self.is_at_end() {
            let ch = self.current_char();
            if ch.is_whitespace() {
                if ch == '\n' {
                    self.line += 1;
                    self.column = 1;
                } else {
                    self.column += 1;
                }
                self.position += 1;
            } else {
                break;
            }
        }
    }

    fn current_char(&self) -> char {
        if self.is_at_end() {
            '\0'
        } else {
            self.input[self.position]
        }
    }

    fn advance(&mut self) {
        if !self.is_at_end() {
            if self.current_char() == '\n' {
                self.line += 1;
                self.column = 1;
            } else {
                self.column += 1;
            }
            self.position += 1;
        }
    }

    fn is_at_end(&self) -> bool {
        self.position >= self.input.len()
    }

    fn peek_ahead_matches(&self, words: &[&str]) -> bool {
        let mut pos = self.position;

        // Skip whitespace
        while pos < self.input.len() && self.input[pos].is_whitespace() {
            pos += 1;
        }

        for &word in words {
            // Skip whitespace before each word
            while pos < self.input.len() && self.input[pos].is_whitespace() {
                pos += 1;
            }

            // Check if we can match this word
            let word_chars: Vec<char> = word.chars().collect();
            for &ch in &word_chars {
                if pos >= self.input.len() || self.input[pos] != ch {
                    return false;
                }
                pos += 1;
            }

            // Make sure the word ends (next char is not alphanumeric)
            if pos < self.input.len() && self.input[pos].is_ascii_alphanumeric() {
                return false;
            }
        }

        true
    }

    fn advance_word(&mut self) {
        // Skip whitespace
        while !self.is_at_end() && self.current_char().is_whitespace() {
            self.advance();
        }

        // Advance through the word
        while !self.is_at_end() && (self.current_char().is_ascii_alphanumeric() || self.current_char() == '_') {
            self.advance();
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_keywords() {
        let mut lexer = Lexer::new("Let be Print");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::Let);
        assert_eq!(tokens[1].token_type, TokenType::Be);
        assert_eq!(tokens[2].token_type, TokenType::Print);
        assert_eq!(tokens[3].token_type, TokenType::Eof);
    }

    #[test]
    fn test_identifier() {
        let mut lexer = Lexer::new("x variable_name");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::Identifier("x".to_string()));
        assert_eq!(tokens[1].token_type, TokenType::Identifier("variable_name".to_string()));
        assert_eq!(tokens[2].token_type, TokenType::Eof);
    }

    #[test]
    fn test_integer() {
        let mut lexer = Lexer::new("42 123");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::Integer(42));
        assert_eq!(tokens[1].token_type, TokenType::Integer(123));
        assert_eq!(tokens[2].token_type, TokenType::Eof);
    }

    #[test]
    fn test_complete_statement() {
        let mut lexer = Lexer::new("Let x be 42");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::Let);
        assert_eq!(tokens[1].token_type, TokenType::Identifier("x".to_string()));
        assert_eq!(tokens[2].token_type, TokenType::Be);
        assert_eq!(tokens[3].token_type, TokenType::Integer(42));
        assert_eq!(tokens[4].token_type, TokenType::Eof);
    }

    #[test]
    fn test_arithmetic_operators() {
        let mut lexer = Lexer::new("plus minus");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::Plus);
        assert_eq!(tokens[1].token_type, TokenType::Minus);
        assert_eq!(tokens[2].token_type, TokenType::Eof);
    }

    #[test]
    fn test_arithmetic_expression() {
        let mut lexer = Lexer::new("Let x be 1 plus 2");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::Let);
        assert_eq!(tokens[1].token_type, TokenType::Identifier("x".to_string()));
        assert_eq!(tokens[2].token_type, TokenType::Be);
        assert_eq!(tokens[3].token_type, TokenType::Integer(1));
        assert_eq!(tokens[4].token_type, TokenType::Plus);
        assert_eq!(tokens[5].token_type, TokenType::Integer(2));
        assert_eq!(tokens[6].token_type, TokenType::Eof);
    }

    #[test]
    fn test_conditional_keywords() {
        let mut lexer = Lexer::new("If Otherwise End");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::If);
        assert_eq!(tokens[1].token_type, TokenType::Otherwise);
        assert_eq!(tokens[2].token_type, TokenType::End);
        assert_eq!(tokens[3].token_type, TokenType::Eof);
    }

    #[test]
    fn test_comparison_operators() {
        let mut lexer = Lexer::new("is equal to");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::IsEqualTo);
        assert_eq!(tokens[1].token_type, TokenType::Eof);
    }

    #[test]
    fn test_full_conditional() {
        let mut lexer = Lexer::new("If x is equal to 5");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::If);
        assert_eq!(tokens[1].token_type, TokenType::Identifier("x".to_string()));
        assert_eq!(tokens[2].token_type, TokenType::IsEqualTo);
        assert_eq!(tokens[3].token_type, TokenType::Integer(5));
        assert_eq!(tokens[4].token_type, TokenType::Eof);
    }

    #[test]
    fn test_function_keywords() {
        let mut lexer = Lexer::new("Process called that takes returns");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::Process);
        assert_eq!(tokens[1].token_type, TokenType::Called);
        assert_eq!(tokens[2].token_type, TokenType::That);
        assert_eq!(tokens[3].token_type, TokenType::Takes);
        assert_eq!(tokens[4].token_type, TokenType::Returns);
        assert_eq!(tokens[5].token_type, TokenType::Eof);
    }

    #[test]
    fn test_punctuation() {
        let mut lexer = Lexer::new("():,");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::LeftParen);
        assert_eq!(tokens[1].token_type, TokenType::RightParen);
        assert_eq!(tokens[2].token_type, TokenType::Colon);
        assert_eq!(tokens[3].token_type, TokenType::Comma);
        assert_eq!(tokens[4].token_type, TokenType::Eof);
    }

    #[test]
    fn test_string_literal() {
        let mut lexer = Lexer::new("\"hello world\"");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::StringLiteral("hello world".to_string()));
        assert_eq!(tokens[1].token_type, TokenType::Eof);
    }

    #[test]
    fn test_string_with_escapes() {
        let mut lexer = Lexer::new("\"hello\\nworld\"");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::StringLiteral("hello\nworld".to_string()));
        assert_eq!(tokens[1].token_type, TokenType::Eof);
    }

    #[test]
    fn test_list_keywords() {
        let mut lexer = Lexer::new("list containing and");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::List);
        assert_eq!(tokens[1].token_type, TokenType::Containing);
        assert_eq!(tokens[2].token_type, TokenType::And);
        assert_eq!(tokens[3].token_type, TokenType::Eof);
    }

    #[test]
    fn test_natural_list() {
        let mut lexer = Lexer::new("a list containing 1, 2, and 3");
        let tokens = lexer.tokenize().unwrap();

        assert_eq!(tokens[0].token_type, TokenType::Identifier("a".to_string()));
        assert_eq!(tokens[1].token_type, TokenType::List);
        assert_eq!(tokens[2].token_type, TokenType::Containing);
        assert_eq!(tokens[3].token_type, TokenType::Integer(1));
        assert_eq!(tokens[4].token_type, TokenType::Comma);
        assert_eq!(tokens[5].token_type, TokenType::Integer(2));
        assert_eq!(tokens[6].token_type, TokenType::Comma);
        assert_eq!(tokens[7].token_type, TokenType::And);
        assert_eq!(tokens[8].token_type, TokenType::Integer(3));
        assert_eq!(tokens[9].token_type, TokenType::Eof);
    }
}