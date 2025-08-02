//! Defines the tokens that are produced by the lexer and consumed by the parser.

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum TokenType {
    // Literals
    Integer,
    Float,
    String,
    Boolean,
    Identifier,

    // Keywords - Variable declarations
    Let,
    Define,
    Set,
    Constant,

    // Keywords - Control flow
    If,
    Otherwise,
    Unless,
    When,
    Match,
    Switch,
    Case,
    Default,

    // Keywords - Loops
    For,
    Each,
    In,
    While,
    Do,
    Repeat,
    Times,
    Loop,
    Forever,
    From,
    To,
    Step,
    By,

    // Keywords - Functions/Processes
    Process,
    Called,
    That,
    Takes,
    Returns,
    Return,
    Yield,
    Print,
    Display,

    // Keywords - Connecting words
    Be,
    As,
    With,
    And,
    Or,
    Not,
    Of,
    The,
    A,
    An,
    Else,

    // Keywords - Types and Data Structures
    Type,
    Struct,
    Enum,
    Is,
    Are,

    // Multi-word Operators
    IsEqualTo,
    IsNotEqualTo,
    IsGreaterThan,
    IsLessThan,
    IsGreaterThanOrEqualTo,
    IsLessThanOrEqualTo,
    CalledWith, // Added for natural function call syntax
    
    // Natural language function call patterns
    Call,
    Invoke,
    Execute,

    // Mathematical and Assignment Operators
    Plus,
    Minus,
    MultipliedBy,
    DividedBy,
    Modulo,
    ToThePowerOf,
    Assign,

    // Punctuation and Delimiters
    LParen,
    RParen,
    LBrace,
    RBrace,
    LBracket,
    RBracket,
    Colon,
    Semicolon,
    Comma,
    Dot,
    Pipe,
    At,
    Question,
    Exclamation,

    // Indentation
    Indent,
    Dedent,
    Newline,

    // Misc
    Comment,
    Wildcard,

    // End of File
    Eof,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Token {
    pub token_type: TokenType,
    pub lexeme: String,
    pub line: usize,
    pub column: usize,
} 