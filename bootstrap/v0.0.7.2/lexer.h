#ifndef LEXER_H
#define LEXER_H

typedef enum {
    TOKEN_EOF,
    TOKEN_PROCESS,
    TOKEN_CALLED,
    TOKEN_RETURNS,
    TOKEN_INTEGER_TYPE,
    TOKEN_STRING_TYPE,
    TOKEN_CHARACTER_TYPE,
    TOKEN_RETURN,
    TOKEN_END,
    TOKEN_COLON,
    TOKEN_STRING_LITERAL,
    TOKEN_INTEGER,
    TOKEN_LET,
    TOKEN_BE,
    TOKEN_SET,
    TOKEN_TO,
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_IF,
    TOKEN_OTHERWISE,
    TOKEN_WHILE,
    TOKEN_IS,
    TOKEN_EQUAL,
    TOKEN_NOT_EQUAL,
    TOKEN_LESS,
    TOKEN_GREATER,
    TOKEN_GREATER_EQUAL,
    TOKEN_LESS_EQUAL,
    TOKEN_THAN,
    TOKEN_NOT,
    TOKEN_AND,
    TOKEN_OR,
    TOKEN_THAT,
    TOKEN_TAKES,
    TOKEN_AS,
    TOKEN_MULTIPLIED,
    TOKEN_DIVIDED,
    TOKEN_MODULO,
    TOKEN_BY,
    TOKEN_PRINT,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_TYPE,
    TOKEN_DOT,
    TOKEN_COMMA,
    TOKEN_IDENTIFIER,
    TOKEN_READ_FILE,
    TOKEN_WRITE_FILE,
    TOKEN_IMPORT,
    TOKEN_STRING_LENGTH,
    TOKEN_STRING_CHAR_AT,
    TOKEN_STRING_SUBSTRING,
    TOKEN_STRING_EQUALS,
    TOKEN_ASCII_VALUE_OF,
    TOKEN_IS_DIGIT,
    TOKEN_IS_ALPHA,
    TOKEN_IS_WHITESPACE,
    TOKEN_LIST_CREATE,
    TOKEN_LIST_APPEND,
    TOKEN_LIST_GET,
    TOKEN_LIST_GET_INTEGER,
    TOKEN_LIST_LENGTH,
    TOKEN_LIST_DESTROY,
    // String manipulation functions
    TOKEN_STRING_CONCAT,
    TOKEN_STRING_COMPARE,
    TOKEN_STRING_TO_INTEGER,
    TOKEN_INTEGER_TO_STRING,
    TOKEN_STRING_FIND,
    TOKEN_STRING_REPLACE,
    TOKEN_STRING_TRIM,
    TOKEN_STRING_SPLIT,
    // ADT/Variant tokens
    TOKEN_PIPE,         // | for variant definitions
    TOKEN_MATCH,        // Match keyword
    TOKEN_WHEN,         // When keyword in match cases
    TOKEN_WITH,         // with keyword for variant fields
    TOKEN_ERROR
} TokenType;

typedef struct {
    TokenType type;
    char *value;
    int line;
    int column;
} Token;

typedef struct {
    char *source;
    int position;
    int line;
    int column;
    char current_char;
} Lexer;

Lexer* lexer_create(char *source);
void lexer_destroy(Lexer *lexer);
Token* lexer_next_token(Lexer *lexer);
void token_destroy(Token *token);

#endif