#ifndef LEXER_H
#define LEXER_H

typedef enum {
    TOKEN_EOF,
    TOKEN_PROCESS,
    TOKEN_CALLED,
    TOKEN_RETURNS,
    TOKEN_INTEGER_TYPE,
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
    TOKEN_IDENTIFIER,
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