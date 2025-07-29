//! The Runa lexer, responsible for turning source code into tokens.

use runa_common::token::{Token, TokenType};
use phf::phf_map;

static KEYWORDS: phf::Map<&'static str, TokenType> = phf_map! {
    // Variable declarations
    "Let" => TokenType::Let,
    "let" => TokenType::Let,
    "Define" => TokenType::Define,
    "define" => TokenType::Define,
    "Set" => TokenType::Set,
    "set" => TokenType::Set,
    "constant" => TokenType::Constant,
    
    // Control flow
    "If" => TokenType::If,
    "if" => TokenType::If,
    "Otherwise" => TokenType::Otherwise,
    "otherwise" => TokenType::Otherwise,
    "Unless" => TokenType::Unless,
    "unless" => TokenType::Unless,
    "When" => TokenType::When,
    "when" => TokenType::When,
    "Match" => TokenType::Match,
    "match" => TokenType::Match,
    "Switch" => TokenType::Switch,
    "switch" => TokenType::Switch,
    "Case" => TokenType::Case,
    "case" => TokenType::Case,
    "Default" => TokenType::Default,
    "default" => TokenType::Default,
    
    // Loops
    "For" => TokenType::For,
    "for" => TokenType::For,
    "each" => TokenType::Each,
    "in" => TokenType::In,
    "While" => TokenType::While,
    "while" => TokenType::While,
    "Do" => TokenType::Do,
    "do" => TokenType::Do,
    "Repeat" => TokenType::Repeat,
    "repeat" => TokenType::Repeat,
    "times" => TokenType::Times,
    "Loop" => TokenType::Loop,
    "loop" => TokenType::Loop,
    "forever" => TokenType::Forever,
    "from" => TokenType::From,
    "to" => TokenType::To,
    "step" => TokenType::Step,
    "by" => TokenType::By,
    
    // Functions/Processes
    "Process" => TokenType::Process,
    "process" => TokenType::Process,
    "called" => TokenType::Called,
    "that" => TokenType::That,
    "takes" => TokenType::Takes,
    "returns" => TokenType::Returns,
    "Return" => TokenType::Return,
    "return" => TokenType::Return,
    "Yield" => TokenType::Yield,
    "yield" => TokenType::Yield,
    "Display" => TokenType::Display,
    "display" => TokenType::Display,
    
    // Connecting words
    "be" => TokenType::Be,
    "as" => TokenType::As,
    "with" => TokenType::With,
    "and" => TokenType::And,
    "or" => TokenType::Or,
    "not" => TokenType::Not,
    "of" => TokenType::Of,
    "the" => TokenType::The,
    "a" => TokenType::A,
    "an" => TokenType::An,
    "else" => TokenType::Else,
    
    // Types and Data Structures
    "Type" => TokenType::Type,
    "type" => TokenType::Type,
    "Struct" => TokenType::Struct,
    "struct" => TokenType::Struct,
    "Enum" => TokenType::Enum,
    "enum" => TokenType::Enum,
    "Is" => TokenType::Is,
    "is" => TokenType::Is,
    "Are" => TokenType::Are,
    "are" => TokenType::Are,
    
    // Boolean literals
    "true" => TokenType::Boolean,
    "false" => TokenType::Boolean,
    "True" => TokenType::Boolean,
    "False" => TokenType::Boolean,
    
    // Operators (symbolic and word-based)
    "+" => TokenType::Plus,
    "plus" => TokenType::Plus,
    "Plus" => TokenType::Plus,
    "-" => TokenType::Minus,
    "minus" => TokenType::Minus,
    "Minus" => TokenType::Minus,
    "*" => TokenType::MultipliedBy,
    "multiplied by" => TokenType::MultipliedBy,
    "MultipliedBy" => TokenType::MultipliedBy,
    "/" => TokenType::DividedBy,
    "divided by" => TokenType::DividedBy,
    "DividedBy" => TokenType::DividedBy,
    "is equal to" => TokenType::IsEqualTo,
    "==" => TokenType::IsEqualTo,
    "is not equal to" => TokenType::IsNotEqualTo,
    "!=" => TokenType::IsNotEqualTo,
    "is greater than or equal to" => TokenType::IsGreaterThanOrEqualTo,
    ">=" => TokenType::IsGreaterThanOrEqualTo,
    "is less than or equal to" => TokenType::IsLessThanOrEqualTo,
    "<=" => TokenType::IsLessThanOrEqualTo,
    "is greater than" => TokenType::IsGreaterThan,
    ">" => TokenType::IsGreaterThan,
    "is less than" => TokenType::IsLessThan,
    "<" => TokenType::IsLessThan,
    "=" => TokenType::Assign,
    "called with" => TokenType::CalledWith,
    "Called with" => TokenType::CalledWith,
};

pub struct Lexer<'a> {
    source: &'a str,
    tokens: Vec<Token>,
    start: usize,
    current: usize,
    line: usize,
    indent_stack: Vec<usize>,
}

impl<'a> Lexer<'a> {
    pub fn new(source: &'a str) -> Self {
        Lexer {
            source,
            tokens: Vec::new(),
            start: 0,
            current: 0,
            line: 1,
            indent_stack: vec![0],
        }
    }

    pub fn scan_tokens(&mut self) -> Result<Vec<Token>, String> {
        // A bit of a hack to handle files that don't start with a newline
        if !self.source.starts_with('\n') && !self.source.is_empty() {
             let temp_source = format!("\n{}", self.source);
             let mut lexer = Lexer::new(&temp_source);
             return lexer.scan_tokens();
        }

        while !self.is_at_end() {
            // Check for indentation changes at the start of a line
            if self.peek() == Some('\n') {
                self.advance(); // consume newline
                self.add_token(TokenType::Newline);
                self.line += 1;
                
                let mut indent_level = 0;
                while self.peek() == Some(' ') {
                    self.advance();
                    indent_level += 1;
                }

                self.handle_indentation(indent_level)?;
                self.start = self.current; // Reset start for the next token
                continue;
            }
            
            self.scan_token()?;
        }
        
        // Close any remaining open blocks at EOF
        while self.indent_stack.len() > 1 {
            self.indent_stack.pop();
            self.add_token_at(TokenType::Dedent, self.tokens.last().map_or(0, |t| t.column));
        }

        self.add_token(TokenType::Eof);
        Ok(self.tokens.clone())
    }


    fn scan_token(&mut self) -> Result<(), String> {
        self.start = self.current;
        let c = self.advance();
        match c {
            '(' => self.add_token(TokenType::LParen),
            ')' => self.add_token(TokenType::RParen),
            '{' => self.add_token(TokenType::LBrace),
            '}' => self.add_token(TokenType::RBrace),
            '[' => self.add_token(TokenType::LBracket),
            ']' => self.add_token(TokenType::RBracket),
            ':' => self.add_token(TokenType::Colon),
            ',' => self.add_token(TokenType::Comma),
            '.' => self.add_token(TokenType::Dot),
            '|' => self.add_token(TokenType::Pipe),

            // Ignore whitespace
            ' ' | '\r' | '\t' => {}

            '\n' => {
                self.add_token(TokenType::Newline);
                self.line += 1;
            }
            
            '#' => {
                // Skip comments until end of line
                while self.peek() != Some('\n') && !self.is_at_end() {
                    self.advance();
                }
            }

            '"' => self.string()?,

            _ => {
                // For identifiers, keywords, and operators
                if c.is_ascii_alphabetic() || "+-*/=!<>&|".contains(c) {
                    self.current -= 1; // Backtrack to include the first char
                    self.identifier_or_operator()?;
                } else if c.is_ascii_digit() {
                    self.current -= 1; // Backtrack
                    self.number()?;
                } else {
                     return Err(format!(
                        "Unexpected character '{}' at line {}",
                        c, self.line
                    ));
                }
            }
        };
        Ok(())
    }
    
    fn handle_indentation(&mut self, level: usize) -> Result<(), String> {
        let current_indent = *self.indent_stack.last().unwrap();
        if level > current_indent {
            self.indent_stack.push(level);
            self.add_token(TokenType::Indent);
        } else if level < current_indent {
            while self.indent_stack.last().unwrap() > &level {
                self.indent_stack.pop();
                self.add_token(TokenType::Dedent);
            }
            if self.indent_stack.last().unwrap() != &level {
                return Err("Inconsistent indentation.".to_string());
            }
        }
        Ok(())
    }

    fn identifier_or_operator(&mut self) -> Result<(), String> {
        // Greedily match longest possible operator first
        let remaining_source = &self.source[self.current..];
        let mut longest_match: Option<(&'static str, &TokenType)> = None;

        for (text, token_type) in KEYWORDS.entries() {
            if remaining_source.starts_with(text) {
                if longest_match.is_none() || text.len() > longest_match.unwrap().0.len() {
                    longest_match = Some((text, token_type));
                }
            }
        }

        if let Some((text, token_type)) = longest_match {
            self.current += text.len();
            self.add_token(token_type.clone());
            return Ok(());
        }

        // If no operator/keyword, it must be an identifier
        self.identifier()
    }


    fn identifier(&mut self) -> Result<(), String> {
        while self.peek().map_or(false, |c| c.is_ascii_alphanumeric() || c == '_') {
            self.advance();
        }

        // This is now only for true identifiers, not keywords
        self.add_token(TokenType::Identifier);

        Ok(())
    }

    fn string(&mut self) -> Result<(), String> {
        while let Some(c) = self.peek() {
            if c == '"' {
                break;
            }
            if c == '\n' {
                self.line += 1;
            }
            self.advance();
        }

        if self.is_at_end() {
            return Err("Unterminated string.".to_string());
        }

        // The closing ".
        self.advance();

        // Trim the surrounding quotes.
        let value = self.source[self.start + 1..self.current - 1].to_string();
        self.add_token_with_lexeme(TokenType::String, value);
        Ok(())
    }

    fn number(&mut self) -> Result<(), String> {
        // Important: Advance past the first digit we already saw
        self.advance();
        while self.peek().map_or(false, |c| c.is_ascii_digit()) {
            self.advance();
        }

        // Look for a fractional part.
        if self.peek() == Some('.') && self.peek_next().map_or(false, |c| c.is_ascii_digit()) {
            // Consume the "."
            self.advance();

            while self.peek().map_or(false, |c| c.is_ascii_digit()) {
                self.advance();
            }
            self.add_token(TokenType::Float);
        } else {
            self.add_token(TokenType::Integer);
        }

        Ok(())
    }

    fn add_token(&mut self, token_type: TokenType) {
        let lexeme = self.source[self.start..self.current].to_string();
        self.add_token_with_lexeme(token_type, lexeme);
    }
    
    fn add_token_with_lexeme(&mut self, token_type: TokenType, lexeme: String) {
        self.tokens.push(Token {
            token_type,
            lexeme,
            line: self.line,
            column: self.start, // Placeholder column for now
        });
    }

    fn add_token_at(&mut self, token_type: TokenType, column: usize) {
        self.tokens.push(Token {
            token_type,
            lexeme: "".to_string(), // Indent/Dedent have no lexeme
            line: self.line,
            column,
        });
    }

    fn is_at_end(&self) -> bool {
        self.current >= self.source.len()
    }

    fn advance(&mut self) -> char {
        let c = self.source.chars().nth(self.current).unwrap();
        self.current += 1;
        c
    }

    fn peek(&self) -> Option<char> {
        if self.is_at_end() {
            return None;
        }
        self.source.chars().nth(self.current)
    }

    fn peek_next(&self) -> Option<char> {
        if self.current + 1 >= self.source.len() {
            return None;
        }
        self.source.chars().nth(self.current + 1)
    }
} 