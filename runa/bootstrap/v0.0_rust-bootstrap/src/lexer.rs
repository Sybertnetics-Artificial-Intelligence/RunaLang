// Minimal Viable Lexer for Runa Bootstrap
// Only supports the MVL subset - no extra features

#[derive(Debug, Clone, PartialEq)]
pub enum TokenType {
    // Keywords
    Let,
    Be,
    If,
    Is,
    Otherwise,
    End,
    While,
    Less,
    Than,
    Greater,
    Process,
    Called,
    Takes,
    Returns,
    Type,
    As,
    Return,
    Add,
    To,

    // Literals
    Integer(i64),
    String(String),
    Identifier(String),

    // Punctuation
    Colon,
    Comma,
    LeftParen,
    RightParen,
    LeftBracket,
    RightBracket,
    Dot,

    // Special
    Newline,
    Eof,
}

pub struct Lexer {
    input: Vec<char>,
    position: usize,
    current_char: Option<char>,
}

impl Lexer {
    pub fn new(input: &str) -> Self {
        let chars: Vec<char> = input.chars().collect();
        let current_char = if chars.is_empty() { None } else { Some(chars[0]) };

        Lexer {
            input: chars,
            position: 0,
            current_char,
        }
    }

    fn advance(&mut self) {
        self.position += 1;
        if self.position >= self.input.len() {
            self.current_char = None;
        } else {
            self.current_char = Some(self.input[self.position]);
        }
    }

    fn peek(&self, offset: usize) -> Option<char> {
        let pos = self.position + offset;
        if pos < self.input.len() {
            Some(self.input[pos])
        } else {
            None
        }
    }

    fn skip_whitespace(&mut self) {
        while let Some(ch) = self.current_char {
            if ch == ' ' || ch == '\t' || ch == '\r' {
                self.advance();
            } else {
                break;
            }
        }
    }

    fn skip_comment(&mut self) {
        if self.current_char == Some('N') &&
           self.peek(1) == Some('o') &&
           self.peek(2) == Some('t') &&
           self.peek(3) == Some('e') &&
           self.peek(4) == Some(':') {
            // Skip until end of line
            while self.current_char.is_some() && self.current_char != Some('\n') {
                self.advance();
            }
        }
    }

    fn read_number(&mut self) -> i64 {
        let mut num_str = String::new();
        let mut is_negative = false;

        if self.current_char == Some('-') {
            is_negative = true;
            self.advance();
        }

        while let Some(ch) = self.current_char {
            if ch.is_ascii_digit() {
                num_str.push(ch);
                self.advance();
            } else {
                break;
            }
        }

        let value = num_str.parse::<i64>().unwrap_or(0);
        if is_negative { -value } else { value }
    }

    fn read_string(&mut self) -> String {
        let mut value = String::new();
        self.advance(); // Skip opening quote

        while let Some(ch) = self.current_char {
            if ch == '"' {
                self.advance(); // Skip closing quote
                break;
            } else if ch == '\\' {
                self.advance();
                if let Some(escaped) = self.current_char {
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
            }
        }

        value
    }

    fn read_identifier(&mut self) -> String {
        let mut id = String::new();

        while let Some(ch) = self.current_char {
            if ch.is_ascii_alphanumeric() || ch == '_' {
                id.push(ch);
                self.advance();
            } else {
                break;
            }
        }

        id
    }

    pub fn next_token(&mut self) -> TokenType {
        loop {
            self.skip_whitespace();

            if self.current_char.is_none() {
                return TokenType::Eof;
            }

            // Check for comments
            if self.current_char == Some('N') &&
               self.peek(1) == Some('o') &&
               self.peek(2) == Some('t') &&
               self.peek(3) == Some('e') &&
               self.peek(4) == Some(':') {
                self.skip_comment();
                continue;
            }

            let ch = self.current_char.unwrap();

            // Handle newlines
            if ch == '\n' {
                self.advance();
                return TokenType::Newline;
            }

            // Handle punctuation
            match ch {
                ':' => {
                    self.advance();
                    return TokenType::Colon;
                }
                ',' => {
                    self.advance();
                    return TokenType::Comma;
                }
                '(' => {
                    self.advance();
                    return TokenType::LeftParen;
                }
                ')' => {
                    self.advance();
                    return TokenType::RightParen;
                }
                '[' => {
                    self.advance();
                    return TokenType::LeftBracket;
                }
                ']' => {
                    self.advance();
                    return TokenType::RightBracket;
                }
                '.' => {
                    self.advance();
                    return TokenType::Dot;
                }
                '"' => {
                    return TokenType::String(self.read_string());
                }
                '-' => {
                    if self.peek(1).map_or(false, |c| c.is_ascii_digit()) {
                        return TokenType::Integer(self.read_number());
                    } else {
                        self.advance();
                        continue; // Skip unknown character
                    }
                }
                _ if ch.is_ascii_digit() => {
                    return TokenType::Integer(self.read_number());
                }
                _ if ch.is_ascii_alphabetic() || ch == '_' => {
                    let id = self.read_identifier();

                    // Check for keywords
                    return match id.as_str() {
                        "Let" => TokenType::Let,
                        "be" => TokenType::Be,
                        "If" => TokenType::If,
                        "is" => TokenType::Is,
                        "Otherwise" => TokenType::Otherwise,
                        "End" => TokenType::End,
                        "While" => TokenType::While,
                        "less" => TokenType::Less,
                        "than" => TokenType::Than,
                        "greater" => TokenType::Greater,
                        "Process" => TokenType::Process,
                        "called" => TokenType::Called,
                        "takes" => TokenType::Takes,
                        "returns" => TokenType::Returns,
                        "Type" => TokenType::Type,
                        "as" => TokenType::As,
                        "Return" => TokenType::Return,
                        "add" => TokenType::Add,
                        "to" => TokenType::To,
                        _ => TokenType::Identifier(id),
                    };
                }
                _ => {
                    // Skip unknown characters
                    self.advance();
                    continue;
                }
            }
        }
    }

    pub fn tokenize(&mut self) -> Vec<TokenType> {
        let mut tokens = Vec::new();

        loop {
            let token = self.next_token();
            if token == TokenType::Eof {
                tokens.push(token);
                break;
            }
            tokens.push(token);
        }

        tokens
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_integers() {
        let mut lexer = Lexer::new("123 -45 0");
        assert_eq!(lexer.next_token(), TokenType::Integer(123));
        assert_eq!(lexer.next_token(), TokenType::Integer(-45));
        assert_eq!(lexer.next_token(), TokenType::Integer(0));
    }

    #[test]
    fn test_strings() {
        let mut lexer = Lexer::new(r#""hello" "world\n""#);
        assert_eq!(lexer.next_token(), TokenType::String("hello".to_string()));
        assert_eq!(lexer.next_token(), TokenType::String("world\n".to_string()));
    }

    #[test]
    fn test_keywords() {
        let mut lexer = Lexer::new("Let x be 5");
        assert_eq!(lexer.next_token(), TokenType::Let);
        assert_eq!(lexer.next_token(), TokenType::Identifier("x".to_string()));
        assert_eq!(lexer.next_token(), TokenType::Be);
        assert_eq!(lexer.next_token(), TokenType::Integer(5));
    }

    #[test]
    fn test_if_statement() {
        let mut lexer = Lexer::new("If x is 1:\n    End If");
        assert_eq!(lexer.next_token(), TokenType::If);
        assert_eq!(lexer.next_token(), TokenType::Identifier("x".to_string()));
        assert_eq!(lexer.next_token(), TokenType::Is);
        assert_eq!(lexer.next_token(), TokenType::Integer(1));
        assert_eq!(lexer.next_token(), TokenType::Colon);
        assert_eq!(lexer.next_token(), TokenType::Newline);
        assert_eq!(lexer.next_token(), TokenType::End);
        assert_eq!(lexer.next_token(), TokenType::If);
    }

    #[test]
    fn test_comments() {
        let mut lexer = Lexer::new("Let x be 5\nNote: This is a comment\nLet y be 10");
        assert_eq!(lexer.next_token(), TokenType::Let);
        assert_eq!(lexer.next_token(), TokenType::Identifier("x".to_string()));
        assert_eq!(lexer.next_token(), TokenType::Be);
        assert_eq!(lexer.next_token(), TokenType::Integer(5));
        assert_eq!(lexer.next_token(), TokenType::Newline);
        assert_eq!(lexer.next_token(), TokenType::Newline); // Comment becomes newline
        assert_eq!(lexer.next_token(), TokenType::Let);
        assert_eq!(lexer.next_token(), TokenType::Identifier("y".to_string()));
        assert_eq!(lexer.next_token(), TokenType::Be);
        assert_eq!(lexer.next_token(), TokenType::Integer(10));
    }
}