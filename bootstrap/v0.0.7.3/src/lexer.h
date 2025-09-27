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
    TOKEN_BIT_AND,
    TOKEN_BIT_OR,
    TOKEN_BIT_XOR,
    TOKEN_BIT_SHIFT_LEFT,
    TOKEN_BIT_SHIFT_RIGHT,
    TOKEN_BREAK,
    TOKEN_CONTINUE,
    TOKEN_OTHERWISE_IF,
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
    // Enhanced list operations
    TOKEN_LIST_SET,
    TOKEN_LIST_INSERT,
    TOKEN_LIST_REMOVE,
    TOKEN_LIST_CLEAR,
    TOKEN_LIST_FIND,
    TOKEN_LIST_SORT,
    TOKEN_LIST_REVERSE,
    TOKEN_LIST_COPY,
    TOKEN_LIST_MERGE,
    // String manipulation functions
    TOKEN_STRING_CONCAT,
    TOKEN_STRING_COMPARE,
    TOKEN_STRING_TO_INTEGER,
    TOKEN_INTEGER_TO_STRING,
    TOKEN_STRING_FIND,
    TOKEN_STRING_REPLACE,
    TOKEN_STRING_TRIM,
    TOKEN_STRING_SPLIT,
    // Enhanced file I/O operations
    TOKEN_FILE_OPEN,
    TOKEN_FILE_CLOSE,
    TOKEN_FILE_READ_LINE,
    TOKEN_FILE_WRITE_LINE,
    TOKEN_FILE_EXISTS,
    TOKEN_FILE_DELETE,
    TOKEN_FILE_SIZE,
    TOKEN_FILE_SEEK,
    TOKEN_FILE_TELL,
    TOKEN_FILE_EOF,
    // Math operations
    TOKEN_SIN,
    TOKEN_COS,
    TOKEN_TAN,
    TOKEN_SQRT,
    TOKEN_POW,
    TOKEN_ABS,
    TOKEN_FLOOR,
    TOKEN_CEIL,
    TOKEN_MIN,
    TOKEN_MAX,
    TOKEN_RANDOM,
    TOKEN_LOG,
    TOKEN_EXP,
    // ADT/Variant tokens
    TOKEN_PIPE,         // | for variant definitions
    TOKEN_MATCH,        // Match keyword
    TOKEN_WHEN,         // When keyword in match cases
    TOKEN_WITH,         // with keyword for variant fields
    // System/Runtime functions
    TOKEN_GET_COMMAND_LINE_ARGS,
    TOKEN_EXIT_WITH_CODE,
    TOKEN_PANIC,
    TOKEN_ASSERT,
    TOKEN_ALLOCATE,
    TOKEN_DEALLOCATE,
    // Inline Assembly tokens
    TOKEN_INLINE,
    TOKEN_ASSEMBLY,
    TOKEN_NOTE,
    // Function pointer tokens
    TOKEN_POINTER,
    TOKEN_OF,
    // Array tokens
    TOKEN_ARRAY,
    TOKEN_LBRACKET,
    TOKEN_RBRACKET,
    TOKEN_ERROR,
    TOKEN_COUNT  // Must be last - used for array sizing
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