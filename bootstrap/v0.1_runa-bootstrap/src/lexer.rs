use anyhow::Result;

#[derive(Debug, Clone, PartialEq)]
pub enum Token {
    Process,
    Called,
    That,
    Takes,
    Returns,
    End,
    Let,
    Be,
    Return,
    As,
    Type,
    Import,
    Module,
    Of,
    Value,
    With,
    Colon,
    Dot,
    LeftParen,
    RightParen,
    LeftBracket,
    RightBracket,
    Comma,
    Plus,
    Minus,
    Multiply,
    Divide,
    // Constructor tokens
    A,
    // Control flow tokens
    If,
    Otherwise,
    While,
    For,
    Each,
    In,
    Set,
    To,
    Into,
    // I/O tokens
    Print,
    ReadFile,
    WriteFile,
    // Inline assembly tokens
    Inline,
    Assembly,
    // Comparison operators
    Is,
    Equal,
    Not,
    Greater,
    Less,
    Than,
    Or,
    And,
    Integer(i64),
    Float(f64),
    String(String),
    Identifier(String),
    Boolean(bool),
    Eof,
}

pub fn tokenize(source: &str) -> Result<Vec<Token>> {
    let mut tokens = Vec::new();
    let mut chars = source.chars().peekable();
    
    while let Some(&ch) = chars.peek() {
        match ch {
            ' ' | '\t' | '\r' | '\n' => { chars.next(); }
            ':' => { chars.next(); tokens.push(Token::Colon); }
            '.' => { chars.next(); tokens.push(Token::Dot); }
            '(' => { chars.next(); tokens.push(Token::LeftParen); }
            ')' => { chars.next(); tokens.push(Token::RightParen); }
            '[' => { chars.next(); tokens.push(Token::LeftBracket); }
            ']' => { chars.next(); tokens.push(Token::RightBracket); }
            ',' => { chars.next(); tokens.push(Token::Comma); }
            '+' => { chars.next(); tokens.push(Token::Plus); }
            '-' => { chars.next(); tokens.push(Token::Minus); }
            '*' => { chars.next(); tokens.push(Token::Multiply); }
            '/' => { chars.next(); tokens.push(Token::Divide); }
            '"' => {
                chars.next(); // consume opening quote
                let mut string_val = String::new();
                while let Some(&ch) = chars.peek() {
                    chars.next();
                    if ch == '"' { break; }
                    string_val.push(ch);
                }
                tokens.push(Token::String(string_val));
            }
            '0'..='9' => {
                let mut number = String::new();
                let mut is_float = false;
                while let Some(&ch) = chars.peek() {
                    if ch.is_ascii_digit() {
                        number.push(ch);
                        chars.next();
                    } else if ch == '.' && !is_float {
                        is_float = true;
                        number.push(ch);
                        chars.next();
                    } else {
                        break;
                    }
                }
                if is_float {
                    tokens.push(Token::Float(number.parse()?));
                } else {
                    tokens.push(Token::Integer(number.parse()?));
                }
            }
            'a'..='z' | 'A'..='Z' | '_' => {
                let mut ident = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch.is_alphanumeric() || ch == '_' {
                        ident.push(ch);
                        chars.next();
                    } else {
                        break;
                    }
                }
                
                // Special handling for "Note:" comments
                if ident == "Note" && chars.peek() == Some(&':') {
                    chars.next(); // consume ':'
                    // Skip the rest of the line
                    while let Some(&ch) = chars.peek() {
                        chars.next();
                        if ch == '\n' {
                            break;
                        }
                    }
                    continue; // Skip to next token
                }
                
                let token = match ident.as_str() {
                    "Process" => Token::Process,
                    "called" => Token::Called,
                    "that" => Token::That,
                    "takes" => Token::Takes,
                    "returns" => Token::Returns,
                    "End" => Token::End,
                    "Let" => Token::Let,
                    "a" => Token::A,
                    "be" => Token::Be,
                    "Return" => Token::Return,
                    "as" => Token::As,
                    "Type" | "type" => Token::Type,  // Allow both uppercase and lowercase
                    "Import" => Token::Import,
                    "module" => Token::Module,
                    "of" => Token::Of,
                    "value" => Token::Value,
                    "with" => Token::With,
                    // Control flow keywords
                    "If" => Token::If,
                    "Otherwise" => Token::Otherwise,
                    "While" => Token::While,
                    "For" => Token::For,
                    "Each" => Token::Each,
                    "in" => Token::In,
                    "Set" => Token::Set,
                    "to" => Token::To,
                    "into" => Token::Into,
                    // I/O keywords
                    "Print" => Token::Print,
                    "ReadFile" => Token::ReadFile,
                    "WriteFile" => Token::WriteFile,
                    // Inline assembly keywords
                    "Inline" => Token::Inline,
                    "Assembly" => Token::Assembly,
                    // Comparison keywords
                    "is" => Token::Is,
                    "equal" => Token::Equal,
                    "not" => Token::Not,
                    "greater" => Token::Greater,
                    "less" => Token::Less,
                    "than" => Token::Than,
                    "or" => Token::Or,
                    "and" => Token::And,
                    "plus" => Token::Plus,
                    "minus" => Token::Minus,
                    "true" => Token::Boolean(true),
                    "false" => Token::Boolean(false),
                    "Integer" | "Float" | "String" | "Boolean" => Token::Identifier(ident),
                    _ => Token::Identifier(ident),
                };
                tokens.push(token);
            }
            _ => return Err(anyhow::anyhow!("Unexpected character: {}", ch)),
        }
    }
    
    tokens.push(Token::Eof);
    Ok(tokens)
}