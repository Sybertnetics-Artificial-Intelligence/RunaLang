//! The Runa lexer, responsible for turning source code into a stream of tokens.
//! This is a production-ready implementation that correctly handles multi-word
//! keywords, indentation, and precise source location tracking.

use runa_common::token::{Token, TokenType};
use phf::phf_map;

// Single-word keywords - case-insensitive lookup
static KEYWORDS: phf::Map<&'static str, TokenType> = phf_map! {
    // Variable declarations
    "let" => TokenType::Let,
    "define" => TokenType::Define,
    "set" => TokenType::Set,
    "constant" => TokenType::Constant,
    
    // Control flow
    "if" => TokenType::If,
    "otherwise" => TokenType::Otherwise,
    "unless" => TokenType::Unless,
    "when" => TokenType::When,
    "match" => TokenType::Match,
    "switch" => TokenType::Switch,
    "case" => TokenType::Case,
    "default" => TokenType::Default,
    
    // Loops
    "for" => TokenType::For,
    "each" => TokenType::Each,
    "in" => TokenType::In,
    "while" => TokenType::While,
    "do" => TokenType::Do,
    "repeat" => TokenType::Repeat,
    "times" => TokenType::Times,
    "loop" => TokenType::Loop,
    "forever" => TokenType::Forever,
    "from" => TokenType::From,
    "to" => TokenType::To,
    "step" => TokenType::Step,
    "by" => TokenType::By,
    
    // Functions/Processes
    "process" => TokenType::Process,
    "called" => TokenType::Called,
    "that" => TokenType::That,
    "takes" => TokenType::Takes,
    "returns" => TokenType::Returns,
    "return" => TokenType::Return,
    "yield" => TokenType::Yield,
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

    // Indexing and Access
    "get" => TokenType::Get,
    "item" => TokenType::Item,
    "first" => TokenType::First,
    "last" => TokenType::Last,
    "key" => TokenType::Key,
    "value" => TokenType::Value,
    "index" => TokenType::Index,
    "at" => TokenType::AtWord,
    
    // Comments
    "note" => TokenType::Note,
    "end" => TokenType::End,
    
    // Types and Data Structures
    "type" => TokenType::Type,
    "struct" => TokenType::Struct,
    "enum" => TokenType::Enum,
    "list" => TokenType::List,
    "containing" => TokenType::Containing,
    "dictionary" => TokenType::Dictionary,
    "is" => TokenType::Is,
    "are" => TokenType::Are,
    
    // Boolean literals
    "true" => TokenType::Boolean,
    "false" => TokenType::Boolean,
    
    // Single-word operators
    "plus" => TokenType::Plus,
    "minus" => TokenType::Minus,
    "modulo" => TokenType::Modulo,
    
    // Function call keywords
    "call" => TokenType::Call,
    "invoke" => TokenType::Invoke,
    "execute" => TokenType::Execute,
};

// Multi-word operators and keywords - ordered from longest to shortest for maximal munch
static MULTI_WORD_OPERATORS: &[(&str, TokenType)] = &[
    // Multi-word comparison operators (longest first)
    ("is greater than or equal to", TokenType::IsGreaterThanOrEqualTo),
    ("is less than or equal to", TokenType::IsLessThanOrEqualTo),
    ("is not equal to", TokenType::IsNotEqualTo),
    ("is greater than", TokenType::IsGreaterThan),
    ("is less than", TokenType::IsLessThan),
    ("is equal to", TokenType::IsEqualTo),
    ("is not", TokenType::IsNot),  // Natural negation: "is not active"
    
    // Multi-word mathematical operators
    ("multiplied by", TokenType::MultipliedBy),
    ("divided by", TokenType::DividedBy),
    ("to the power of", TokenType::ToThePowerOf),
    
    // String concatenation operators
    ("followed by", TokenType::FollowedBy),
    ("concatenated with", TokenType::FollowedBy),
    ("joined with", TokenType::FollowedBy),

    
    // Function call syntax
    ("called with", TokenType::CalledWith),
];

pub struct Lexer<'a> {
    source: &'a str,
    chars: std::str::Chars<'a>,
    tokens: Vec<Token>,
    
    start_pos: usize,
    current_pos: usize,
    
    line: usize,
    column: usize,
    
    indent_stack: Vec<usize>,
    at_line_start: bool,
}

impl<'a> Lexer<'a> {
    pub fn new(source: &'a str) -> Self {
        Lexer {
            source,
            chars: source.chars(),
            tokens: Vec::new(),
            start_pos: 0,
            current_pos: 0,
            line: 1,
            column: 1,
            indent_stack: vec![0], // Base indentation is 0
            at_line_start: true,
        }
    }

    pub fn scan_tokens(&mut self) -> Result<Vec<Token>, String> {
        while let Some(_) = self.peek() {
            // Handle indentation at the start of each line
            if self.at_line_start {
                self.handle_indentation()?;
                self.at_line_start = false;
            }

            // Re-peek after indentation handling to get the correct character
            let Some(c) = self.peek() else { break; };
            self.start_pos = self.current_pos;
            
            match c {
                // Single-character tokens
                '(' => { self.advance(); self.add_token(TokenType::LParen); }
                ')' => { self.advance(); self.add_token(TokenType::RParen); }
                '{' => { self.advance(); self.add_token(TokenType::LBrace); }
                '}' => { self.advance(); self.add_token(TokenType::RBrace); }
                '[' => { self.advance(); self.add_token(TokenType::LBracket); }
                ']' => { self.advance(); self.add_token(TokenType::RBracket); }
                ',' => { self.advance(); self.add_token(TokenType::Comma); }
                '.' => { self.advance(); self.add_token(TokenType::Dot); }
                ':' => { self.advance(); self.add_token(TokenType::Colon); }
                ';' => { self.advance(); self.add_token(TokenType::Semicolon); }
                '|' => { self.advance(); self.add_token(TokenType::Pipe); }
                '?' => { self.advance(); self.add_token(TokenType::Question); }
                '!' => { self.advance(); self.add_token(TokenType::Exclamation); }
                '%' => { self.advance(); self.add_token(TokenType::Modulo); }
                '^' => { self.advance(); self.add_token(TokenType::ToThePowerOf); }
                
                // Assignment and arithmetic operators
                '=' => { self.advance(); self.add_token(TokenType::Assign); }
                '+' => { self.advance(); self.add_token(TokenType::Plus); }
                '-' => { self.advance(); self.add_token(TokenType::Minus); }
                '*' => { self.advance(); self.add_token(TokenType::MultipliedBy); }
                '/' => { self.advance(); self.add_token(TokenType::DividedBy); }
                
                // Whitespace
                ' ' | '\t' | '\r' => {
                    self.advance(); // Consume whitespace but don't create tokens
                }

                // Newlines
                '\n' => {
                    self.advance();
                    self.add_token(TokenType::Newline);
                    self.line += 1;
                    self.column = 1;
                    self.at_line_start = true;
                }

                // Strings
                '"' | '\'' => self.string()?,
                
                // Numbers
                c if c.is_ascii_digit() => self.number()?,
                
                // Raw string detection: special case for 'r' prefix
                'r' => {
                    // Look ahead for a quote by checking the source string directly
                    let next_pos = self.current_pos + 1;
                    if next_pos < self.source.len() {
                        let next_char = self.source.chars().nth(next_pos);
                        if next_char == Some('"') || next_char == Some('\'') {
                            self.advance(); // consume 'r'
                            self.raw_string()?; // handles the quote and content
                            continue;
                        }
                    }
                    self.identifier_or_keyword()?;
                },
                
                // Identifiers, keywords, and multi-word operators
                c if c.is_ascii_alphabetic() || c == '_' => self.identifier_or_keyword()?,
                
                // Annotations
                '@' => self.annotation()?,

                // Unexpected characters
                _ => {
                    return Err(format!("Unexpected character '{}' at line {} column {}", c, self.line, self.column));
                }
            }
        }
        
        // Emit any necessary Dedent tokens at the end
        while self.indent_stack.len() > 1 {
            self.indent_stack.pop();
            self.add_token_with_literal(TokenType::Dedent, "");
        }

        self.add_token(TokenType::Eof);
        Ok(self.tokens.clone())
    }

    /// Handle indentation at the start of a line
    fn handle_indentation(&mut self) -> Result<(), String> {
        let mut indent_level = 0;
        
        while let Some(c) = self.peek() {
            match c {
                ' ' => {
                    self.advance();
                    indent_level += 1;
                }
                '\t' => {
                    self.advance();
                    // Align tabs to the next multiple of 4
                    indent_level = (indent_level / 4 + 1) * 4;
                }
                _ => break, // Stop on any non-whitespace character
            }
        }

        // Ignore empty lines for indentation purposes
        if self.peek() == Some('\n') {
            return Ok(());
        }

        let current_indent = *self.indent_stack.last().unwrap();

        if indent_level > current_indent {
            self.indent_stack.push(indent_level);
            self.add_token_with_literal(TokenType::Indent, "");
        } else if indent_level < current_indent {
            while *self.indent_stack.last().unwrap() > indent_level {
                self.indent_stack.pop();
                self.add_token_with_literal(TokenType::Dedent, "");
            }
            // Check for inconsistent indentation
            if *self.indent_stack.last().unwrap() != indent_level {
                return Err(format!("Inconsistent indentation at line {}. Expected {} spaces, got {}", 
                    self.line, *self.indent_stack.last().unwrap(), indent_level));
            }
        }
        
        Ok(())
    }
    
    /// Handle identifiers, keywords, and multi-word operators with maximal munch
    fn identifier_or_keyword(&mut self) -> Result<(), String> {
        // First, try to match the longest possible multi-word operator
        for (op, token_type) in MULTI_WORD_OPERATORS {
            if self.source[self.current_pos..].starts_with(op) {
                // Check if this is a complete word boundary match
                let end_pos = self.current_pos + op.len();
                let is_word_boundary = end_pos >= self.source.len() || 
                    !self.source.chars().nth(end_pos).unwrap_or(' ').is_ascii_alphanumeric();
                
                if is_word_boundary {
                    // Found a match - advance past it and create the token
                    for _ in 0..op.len() {
                        self.advance();
                    }
                    self.add_token(*token_type);
                    return Ok(());
                }
            }
        }

        // If no multi-word operator matched, it's a single-word identifier or keyword
        self.advance_while(|c| c.is_ascii_alphanumeric() || c == '_');
        
        let lexeme = &self.source[self.start_pos..self.current_pos];
        
        // Look up in the single-word keyword map (case-insensitive)
        let token_type = KEYWORDS.get(lexeme.to_lowercase().as_str())
            .copied()
            .unwrap_or(TokenType::Identifier);
            
        self.add_token(token_type);
        Ok(())
    }
    
    /// Handle string literals with proper escape sequence support
    fn string(&mut self) -> Result<(), String> {
        let quote_char = self.advance().unwrap(); // Consume the opening quote
        let mut has_interpolation = false;
        
        while let Some(c) = self.peek() {
            if c == quote_char {
                break;
            }
            if c == '\\' {
                // Handle escape sequence
                self.advance(); // Consume '\'
                match self.peek() {
                    Some('n') | Some('t') | Some('r') | Some('\\') | 
                    Some('"') | Some('\'') => {
                        self.advance(); // Consume the escape character
                    }
                    Some('u') => {
                        self.advance(); // Consume 'u'
                        if self.peek() != Some('{') {
                            return Err("Invalid Unicode escape sequence".to_string());
                        }
                        self.advance(); // Consume '{'
                        // Parse hex digits
                        let mut hex_digits = String::new();
                        let mut found_digits = false;
                        while let Some(c) = self.peek() {
                            if c.is_ascii_hexdigit() {
                                self.advance();
                                hex_digits.push(c);
                                found_digits = true;
                            } else if c == '}' {
                                self.advance(); // Consume '}'
                                if !found_digits {
                                    return Err("Empty Unicode escape sequence".to_string());
                                }
                                break;
                            } else {
                                return Err("Invalid Unicode escape sequence".to_string());
                            }
                        }
                        if !found_digits {
                            return Err("Empty Unicode escape sequence".to_string());
                        }
                    }
                    _ => {
                        return Err("Invalid escape sequence".to_string());
                    }
                }
            } else {
                if c == '{' {
                    has_interpolation = true;
                }
                if c == '\n' {
                    self.line += 1;
                    self.column = 1;
                }
                self.advance();
            }
        }

        if self.peek().is_none() {
            return Err("Unterminated string".to_string());
        }

        self.advance(); // Consume the closing quote
        
        // Extract the string content (without quotes)
        let lexeme = &self.source[self.start_pos..self.current_pos];
        let token_type = if has_interpolation {
            TokenType::InterpolatedString
        } else {
            TokenType::String
        };
        self.add_token_with_literal(token_type, lexeme);
        Ok(())
    }

    /// Handle raw string literals (r"..." or r'...') - no escape sequence processing
    fn raw_string(&mut self) -> Result<(), String> {
        let quote_char = self.advance().unwrap(); // consume opening quote

        while let Some(c) = self.peek() {
            if c == quote_char {
                // Check if this quote is escaped (preceded by backslash)
                let prev_pos = self.current_pos.saturating_sub(1);
                if prev_pos >= self.start_pos {
                    let prev_char = self.source.chars().nth(prev_pos);
                    if prev_char == Some('\\') {
                        // This is an escaped quote, treat as literal
                        self.advance();
                        continue;
                    }
                }
                // This is an unescaped closing quote
                break;
            }
            if c == '\n' {
                self.line += 1;
                self.column = 1;
            }
            self.advance();
        }

        if self.peek().is_none() {
            return Err("Unterminated raw string".to_string());
        }

        self.advance(); // consume closing quote

        let lexeme = &self.source[self.start_pos..self.current_pos];
        self.add_token_with_literal(TokenType::String, lexeme);
        Ok(())
    }

    /// Handle numeric literals (integers and floats)
    fn number(&mut self) -> Result<(), String> {
        // Consume the first digit
        self.advance();
        
        // Consume remaining digits
        while let Some(c) = self.peek() {
            if c.is_ascii_digit() || c == '_' {
                self.advance();
            } else {
                break;
            }
        }

        // Look for decimal point
        if self.peek() == Some('.') {
            self.advance(); // Consume the '.'
            
            // Must have at least one digit after decimal point
            if !self.peek().map_or(false, |c| c.is_ascii_digit()) {
                return Err("Invalid float literal".to_string());
            }
            
            // Consume fractional digits
            while let Some(c) = self.peek() {
                if c.is_ascii_digit() || c == '_' {
                    self.advance();
                } else {
                    break;
                }
            }
            
            self.add_token(TokenType::Float);
        } else {
            self.add_token(TokenType::Integer);
        }
        
        Ok(())
    }

    /// Handle annotation tokens (e.g., @Reasoning, @Implementation)
    fn annotation(&mut self) -> Result<(), String> {
        self.advance(); // Consume the '@'
        
        let mut annotation_text = String::new();
        
        while let Some(c) = self.peek() {
            if c.is_ascii_alphabetic() || c == '_' {
                self.advance();
                annotation_text.push(c);
            } else {
                break;
            }
        }
        
        // Map annotation text to token type
        let token_type = match annotation_text.as_str() {
            "Reasoning" => TokenType::AtReasoning,
            "End_Reasoning" => TokenType::AtEndReasoning,
            "Implementation" => TokenType::AtImplementation,
            "End_Implementation" => TokenType::AtEndImplementation,
            "Uncertainty" => TokenType::AtUncertainty,
            "End_Uncertainty" => TokenType::AtEndUncertainty,
            "Request_Clarification" => TokenType::AtRequestClarification,
            "End_Request_Clarification" => TokenType::AtEndRequestClarification,
            "KnowledgeReference" => TokenType::AtKnowledgeReference,
            "End_KnowledgeReference" => TokenType::AtEndKnowledgeReference,
            "TestCases" => TokenType::AtTestCases,
            "End_TestCases" => TokenType::AtEndTestCases,
            "Resource_Constraints" => TokenType::AtResourceConstraints,
            "End_Resource_Constraints" => TokenType::AtEndResourceConstraints,
            "Security_Scope" => TokenType::AtSecurityScope,
            "End_Security_Scope" => TokenType::AtEndSecurityScope,
            "Execution_Model" => TokenType::AtExecutionModel,
            "End_Execution_Model" => TokenType::AtEndExecutionModel,
            "Performance_Hints" => TokenType::AtPerformanceHints,
            "End_Performance_Hints" => TokenType::AtEndPerformanceHints,
            "Progress" => TokenType::AtProgress,
            "End_Progress" => TokenType::AtEndProgress,
            "Feedback" => TokenType::AtFeedback,
            "End_Feedback" => TokenType::AtEndFeedback,
            "Translation_Note" => TokenType::AtTranslationNote,
            "End_Translation_Note" => TokenType::AtEndTranslationNote,
            "Error_Handling" => TokenType::AtErrorHandling,
            "End_Error_Handling" => TokenType::AtEndErrorHandling,
            "Request" => TokenType::AtRequest,
            "End_Request" => TokenType::AtEndRequest,
            "Context" => TokenType::AtContext,
            "End_Context" => TokenType::AtEndContext,
            "Task" => TokenType::AtTask,
            "End_Task" => TokenType::AtEndTask,
            "Requirements" => TokenType::AtRequirements,
            "End_Requirements" => TokenType::AtEndRequirements,
            "Verify" => TokenType::AtVerify,
            "End_Verify" => TokenType::AtEndVerify,
            "Collaboration" => TokenType::AtCollaboration,
            "End_Collaboration" => TokenType::AtEndCollaboration,
            "Iteration" => TokenType::AtIteration,
            "End_Iteration" => TokenType::AtEndIteration,
            "Clarification" => TokenType::AtClarification,
            "End_Clarification" => TokenType::AtEndClarification,
            _ => {
                return Err(format!("Unknown annotation: @{}", annotation_text));
            }
        };
        
        self.add_token_with_literal(token_type, &format!("@{}", annotation_text));
        Ok(())
    }

    // Core lexer primitives

    fn advance(&mut self) -> Option<char> {
        let char = self.chars.next()?;
        // For ASCII characters, len_utf8() should be 1, but let's be explicit
        self.current_pos += 1; // Always advance by 1 character position
        if char != '\n' && char != '\r' && char != '\t' {
            self.column += 1;
        }
        Some(char)
    }
    
    fn advance_while<F>(&mut self, mut predicate: F) 
    where 
        F: FnMut(char) -> bool 
    {
        while let Some(c) = self.peek() {
            if predicate(c) {
                self.advance();
            } else {
                break;
            }
        }
    }

    /// Peek at the next character without advancing
    fn peek_next(&self) -> Option<char> {
        let mut chars_copy = self.chars.clone();
        chars_copy.next(); // Skip current character
        chars_copy.next()  // Get next character
    }

    /// Peek at the current character without advancing
    fn peek(&self) -> Option<char> {
        self.chars.clone().next()
    }
    
    fn add_token(&mut self, token_type: TokenType) {
        let lexeme = &self.source[self.start_pos..self.current_pos];
        self.add_token_with_literal(token_type, lexeme);
    }

    fn add_token_with_literal(&mut self, token_type: TokenType, lexeme: &str) {
        let token_column = self.column.saturating_sub(lexeme.len());
        self.tokens.push(Token {
            token_type,
            lexeme: lexeme.to_string(),
            line: self.line,
            column: token_column,
        });
    }
} 