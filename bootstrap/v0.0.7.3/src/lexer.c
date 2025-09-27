#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "lexer.h"

static char* string_duplicate(const char *str) {
    if (!str) return NULL;
    int len = strlen(str);
    char *dup = malloc(len + 1);
    strcpy(dup, str);
    return dup;
}

static void lexer_advance(Lexer *lexer) {
    if (lexer->current_char == '\n') {
        lexer->line++;
        lexer->column = 0;
    }
    lexer->position++;
    lexer->column++;

    if (lexer->position >= (int)strlen(lexer->source)) {
        lexer->current_char = '\0';
    } else {
        lexer->current_char = lexer->source[lexer->position];
    }
}

static void lexer_skip_whitespace(Lexer *lexer) {
    while (lexer->current_char != '\0' && isspace(lexer->current_char)) {
        lexer_advance(lexer);
    }
}

static void lexer_skip_comment(Lexer *lexer) {
    // Skip the '#' character
    lexer_advance(lexer);

    // Skip until end of line or end of file
    while (lexer->current_char != '\0' && lexer->current_char != '\n') {
        lexer_advance(lexer);
    }
}

// Create token with an owned string (we take ownership)
static Token* token_create_owned(TokenType type, char *value, int line, int column) {
    Token *token = malloc(sizeof(Token));
    token->type = type;
    token->value = value;  // Take ownership
    token->line = line;
    token->column = column;
    return token;
}

// Create token with a string literal or constant (we duplicate)
static Token* token_create(TokenType type, const char *value, int line, int column) {
    Token *token = malloc(sizeof(Token));
    token->type = type;
    token->value = value ? string_duplicate(value) : NULL;
    token->line = line;
    token->column = column;
    return token;
}

static char* lexer_read_string_literal(Lexer *lexer) {
    lexer_advance(lexer); // Skip opening quote
    int start_pos = lexer->position;

    while (lexer->current_char != '\0' && lexer->current_char != '"') {
        lexer_advance(lexer);
    }

    if (lexer->current_char == '"') {
        int length = lexer->position - start_pos;
        char *string = malloc(length + 1);
        strncpy(string, lexer->source + start_pos, length);
        string[length] = '\0';
        lexer_advance(lexer); // Skip closing quote
        return string;
    }

    return NULL; // Unterminated string
}

static char* lexer_read_word(Lexer *lexer) {
    int start_pos = lexer->position;

    while (lexer->current_char != '\0' && (isalnum(lexer->current_char) || lexer->current_char == '_')) {
        lexer_advance(lexer);
    }

    int length = lexer->position - start_pos;
    char *word = malloc(length + 1);
    strncpy(word, lexer->source + start_pos, length);
    word[length] = '\0';

    return word;
}

static char* lexer_read_integer(Lexer *lexer) {
    int start_pos = lexer->position;

    while (lexer->current_char != '\0' && isdigit(lexer->current_char)) {
        lexer_advance(lexer);
    }

    int length = lexer->position - start_pos;
    char *integer = malloc(length + 1);
    strncpy(integer, lexer->source + start_pos, length);
    integer[length] = '\0';

    return integer;
}

Lexer* lexer_create(char *source) {
    Lexer *lexer = malloc(sizeof(Lexer));
    lexer->source = string_duplicate(source);
    lexer->position = 0;
    lexer->line = 1;
    lexer->column = 1;
    lexer->current_char = source[0];
    return lexer;
}

void lexer_destroy(Lexer *lexer) {
    if (lexer) {
        free(lexer->source);
        free(lexer);
    }
}

Token* lexer_next_token(Lexer *lexer) {
    while (lexer->current_char != '\0') {
        int line = lexer->line;
        int column = lexer->column;

        if (isspace(lexer->current_char)) {
            lexer_skip_whitespace(lexer);
            continue;
        }

        if (lexer->current_char == '#') {
            lexer_skip_comment(lexer);
            continue;
        }

        if (lexer->current_char == '"') {
            char *string = lexer_read_string_literal(lexer);
            if (string) {
                return token_create_owned(TOKEN_STRING_LITERAL, string, line, column);
            } else {
                fprintf(stderr, "[LEXER ERROR] Unterminated string literal at line %d, column %d\n",
                        line, column);
                return token_create(TOKEN_ERROR, "Unterminated string", line, column);
            }
        }

        if (isdigit(lexer->current_char)) {
            char *integer = lexer_read_integer(lexer);
            return token_create_owned(TOKEN_INTEGER, integer, line, column);
        }

        if (isalpha(lexer->current_char)) {
            char *word = lexer_read_word(lexer);
            TokenType type = TOKEN_ERROR;

            if (strcmp(word, "Process") == 0) {
                type = TOKEN_PROCESS;
            } else if (strcmp(word, "called") == 0) {
                type = TOKEN_CALLED;
            } else if (strcmp(word, "returns") == 0) {
                type = TOKEN_RETURNS;
            } else if (strcmp(word, "Integer") == 0) {
                type = TOKEN_INTEGER_TYPE;
            } else if (strcmp(word, "String") == 0) {
                type = TOKEN_STRING_TYPE;
            } else if (strcmp(word, "Character") == 0) {
                type = TOKEN_CHARACTER_TYPE;
            } else if (strcmp(word, "Return") == 0) {
                type = TOKEN_RETURN;
            } else if (strcmp(word, "End") == 0) {
                type = TOKEN_END;
            } else if (strcmp(word, "Let") == 0) {
                type = TOKEN_LET;
            } else if (strcmp(word, "be") == 0) {
                type = TOKEN_BE;
            } else if (strcmp(word, "Set") == 0) {
                type = TOKEN_SET;
            } else if (strcmp(word, "to") == 0) {
                type = TOKEN_TO;
            } else if (strcmp(word, "plus") == 0) {
                type = TOKEN_PLUS;
            } else if (strcmp(word, "minus") == 0) {
                type = TOKEN_MINUS;
            } else if (strcmp(word, "If") == 0) {
                type = TOKEN_IF;
            } else if (strcmp(word, "Otherwise") == 0) {
                type = TOKEN_OTHERWISE;
            } else if (strcmp(word, "While") == 0) {
                type = TOKEN_WHILE;
            } else if (strcmp(word, "is") == 0) {
                type = TOKEN_IS;
            } else if (strcmp(word, "equal") == 0) {
                type = TOKEN_EQUAL;
            } else if (strcmp(word, "less") == 0) {
                type = TOKEN_LESS;
            } else if (strcmp(word, "greater") == 0) {
                type = TOKEN_GREATER;
            } else if (strcmp(word, "than") == 0) {
                type = TOKEN_THAN;
            } else if (strcmp(word, "not") == 0) {
                type = TOKEN_NOT;
            } else if (strcmp(word, "and") == 0) {
                type = TOKEN_AND;
            } else if (strcmp(word, "or") == 0) {
                type = TOKEN_OR;
            } else if (strcmp(word, "that") == 0) {
                type = TOKEN_THAT;
            } else if (strcmp(word, "takes") == 0) {
                type = TOKEN_TAKES;
            } else if (strcmp(word, "as") == 0) {
                type = TOKEN_AS;
            } else if (strcmp(word, "multiplied") == 0) {
                type = TOKEN_MULTIPLIED;
            } else if (strcmp(word, "divided") == 0) {
                type = TOKEN_DIVIDED;
            } else if (strcmp(word, "modulo") == 0) {
                type = TOKEN_MODULO;
            } else if (strcmp(word, "by") == 0) {
                type = TOKEN_BY;
            } else if (strcmp(word, "bit_and") == 0) {
                type = TOKEN_BIT_AND;
            } else if (strcmp(word, "bit_or") == 0) {
                type = TOKEN_BIT_OR;
            } else if (strcmp(word, "bit_xor") == 0) {
                type = TOKEN_BIT_XOR;
            } else if (strcmp(word, "bit_shift_left") == 0) {
                type = TOKEN_BIT_SHIFT_LEFT;
            } else if (strcmp(word, "bit_shift_right") == 0) {
                type = TOKEN_BIT_SHIFT_RIGHT;
            } else if (strcmp(word, "Break") == 0) {
                type = TOKEN_BREAK;
            } else if (strcmp(word, "Continue") == 0) {
                type = TOKEN_CONTINUE;
            } else if (strcmp(word, "Otherwise If") == 0) {
                type = TOKEN_OTHERWISE_IF;
            } else if (strcmp(word, "Print") == 0) {
                type = TOKEN_PRINT;
            } else if (strcmp(word, "Type") == 0) {
                type = TOKEN_TYPE;
            } else if (strcmp(word, "read_file") == 0) {
                type = TOKEN_READ_FILE;
            } else if (strcmp(word, "write_file") == 0) {
                type = TOKEN_WRITE_FILE;
            } else if (strcmp(word, "Import") == 0) {
                type = TOKEN_IMPORT;
            } else if (strcmp(word, "string_length") == 0) {
                type = TOKEN_STRING_LENGTH;
            } else if (strcmp(word, "string_char_at") == 0) {
                type = TOKEN_STRING_CHAR_AT;
            } else if (strcmp(word, "string_substring") == 0) {
                type = TOKEN_STRING_SUBSTRING;
            } else if (strcmp(word, "string_equals") == 0) {
                type = TOKEN_STRING_EQUALS;
            } else if (strcmp(word, "ascii_value_of") == 0) {
                type = TOKEN_ASCII_VALUE_OF;
            } else if (strcmp(word, "is_digit") == 0) {
                type = TOKEN_IS_DIGIT;
            } else if (strcmp(word, "is_alpha") == 0) {
                type = TOKEN_IS_ALPHA;
            } else if (strcmp(word, "is_whitespace") == 0) {
                type = TOKEN_IS_WHITESPACE;
            } else if (strcmp(word, "list_create") == 0) {
                type = TOKEN_LIST_CREATE;
            } else if (strcmp(word, "list_append") == 0) {
                type = TOKEN_LIST_APPEND;
            } else if (strcmp(word, "list_get") == 0) {
                type = TOKEN_LIST_GET;
            } else if (strcmp(word, "list_get_integer") == 0) {
                type = TOKEN_LIST_GET_INTEGER;
            } else if (strcmp(word, "list_length") == 0) {
                type = TOKEN_LIST_LENGTH;
            } else if (strcmp(word, "list_destroy") == 0) {
                type = TOKEN_LIST_DESTROY;
            } else if (strcmp(word, "list_set") == 0) {
                type = TOKEN_LIST_SET;
            } else if (strcmp(word, "list_insert") == 0) {
                type = TOKEN_LIST_INSERT;
            } else if (strcmp(word, "list_remove") == 0) {
                type = TOKEN_LIST_REMOVE;
            } else if (strcmp(word, "list_clear") == 0) {
                type = TOKEN_LIST_CLEAR;
            } else if (strcmp(word, "list_find") == 0) {
                type = TOKEN_LIST_FIND;
            } else if (strcmp(word, "list_sort") == 0) {
                type = TOKEN_LIST_SORT;
            } else if (strcmp(word, "list_reverse") == 0) {
                type = TOKEN_LIST_REVERSE;
            } else if (strcmp(word, "list_copy") == 0) {
                type = TOKEN_LIST_COPY;
            } else if (strcmp(word, "list_merge") == 0) {
                type = TOKEN_LIST_MERGE;
            } else if (strcmp(word, "file_open") == 0) {
                type = TOKEN_FILE_OPEN;
            } else if (strcmp(word, "file_close") == 0) {
                type = TOKEN_FILE_CLOSE;
            } else if (strcmp(word, "file_read_line") == 0) {
                type = TOKEN_FILE_READ_LINE;
            } else if (strcmp(word, "file_write_line") == 0) {
                type = TOKEN_FILE_WRITE_LINE;
            } else if (strcmp(word, "file_exists") == 0) {
                type = TOKEN_FILE_EXISTS;
            } else if (strcmp(word, "file_delete") == 0) {
                type = TOKEN_FILE_DELETE;
            } else if (strcmp(word, "file_size") == 0) {
                type = TOKEN_FILE_SIZE;
            } else if (strcmp(word, "file_seek") == 0) {
                type = TOKEN_FILE_SEEK;
            } else if (strcmp(word, "file_tell") == 0) {
                type = TOKEN_FILE_TELL;
            } else if (strcmp(word, "file_eof") == 0) {
                type = TOKEN_FILE_EOF;
            } else if (strcmp(word, "sin") == 0) {
                type = TOKEN_SIN;
            } else if (strcmp(word, "cos") == 0) {
                type = TOKEN_COS;
            } else if (strcmp(word, "tan") == 0) {
                type = TOKEN_TAN;
            } else if (strcmp(word, "sqrt") == 0) {
                type = TOKEN_SQRT;
            } else if (strcmp(word, "pow") == 0) {
                type = TOKEN_POW;
            } else if (strcmp(word, "abs") == 0) {
                type = TOKEN_ABS;
            } else if (strcmp(word, "floor") == 0) {
                type = TOKEN_FLOOR;
            } else if (strcmp(word, "ceil") == 0) {
                type = TOKEN_CEIL;
            } else if (strcmp(word, "min") == 0) {
                type = TOKEN_MIN;
            } else if (strcmp(word, "max") == 0) {
                type = TOKEN_MAX;
            } else if (strcmp(word, "random") == 0) {
                type = TOKEN_RANDOM;
            } else if (strcmp(word, "log") == 0) {
                type = TOKEN_LOG;
            } else if (strcmp(word, "exp") == 0) {
                type = TOKEN_EXP;
            } else if (strcmp(word, "string_concat") == 0) {
                type = TOKEN_STRING_CONCAT;
            } else if (strcmp(word, "string_compare") == 0) {
                type = TOKEN_STRING_COMPARE;
            } else if (strcmp(word, "string_to_integer") == 0) {
                type = TOKEN_STRING_TO_INTEGER;
            } else if (strcmp(word, "integer_to_string") == 0) {
                type = TOKEN_INTEGER_TO_STRING;
            } else if (strcmp(word, "string_find") == 0) {
                type = TOKEN_STRING_FIND;
            } else if (strcmp(word, "string_replace") == 0) {
                type = TOKEN_STRING_REPLACE;
            } else if (strcmp(word, "string_trim") == 0) {
                type = TOKEN_STRING_TRIM;
            } else if (strcmp(word, "string_split") == 0) {
                type = TOKEN_STRING_SPLIT;
            } else if (strcmp(word, "Match") == 0) {
                type = TOKEN_MATCH;
            } else if (strcmp(word, "When") == 0) {
                type = TOKEN_WHEN;
            } else if (strcmp(word, "with") == 0) {
                type = TOKEN_WITH;
            } else if (strcmp(word, "get_command_line_args") == 0) {
                type = TOKEN_GET_COMMAND_LINE_ARGS;
            } else if (strcmp(word, "exit_with_code") == 0) {
                type = TOKEN_EXIT_WITH_CODE;
            } else if (strcmp(word, "panic") == 0) {
                type = TOKEN_PANIC;
            } else if (strcmp(word, "assert") == 0) {
                type = TOKEN_ASSERT;
            } else if (strcmp(word, "allocate") == 0) {
                type = TOKEN_ALLOCATE;
            } else if (strcmp(word, "deallocate") == 0) {
                type = TOKEN_DEALLOCATE;
            } else if (strcmp(word, "Inline") == 0) {
                type = TOKEN_INLINE;
            } else if (strcmp(word, "Assembly") == 0) {
                type = TOKEN_ASSEMBLY;
            } else if (strcmp(word, "Note") == 0) {
                type = TOKEN_NOTE;
            } else if (strcmp(word, "Pointer") == 0) {
                type = TOKEN_POINTER;
            } else if (strcmp(word, "of") == 0) {
                type = TOKEN_OF;
            } else if (strcmp(word, "array") == 0) {
                type = TOKEN_ARRAY;
            } else {
                type = TOKEN_IDENTIFIER;
            }

            return token_create_owned(type, word, line, column);
        }

        if (lexer->current_char == ':') {
            lexer_advance(lexer);
            return token_create(TOKEN_COLON, ":", line, column);
        }

        if (lexer->current_char == '(') {
            lexer_advance(lexer);
            return token_create(TOKEN_LPAREN, "(", line, column);
        }

        if (lexer->current_char == ')') {
            lexer_advance(lexer);
            return token_create(TOKEN_RPAREN, ")", line, column);
        }

        if (lexer->current_char == '[') {
            lexer_advance(lexer);
            return token_create(TOKEN_LBRACKET, "[", line, column);
        }

        if (lexer->current_char == ']') {
            lexer_advance(lexer);
            return token_create(TOKEN_RBRACKET, "]", line, column);
        }

        if (lexer->current_char == '.') {
            lexer_advance(lexer);
            return token_create(TOKEN_DOT, ".", line, column);
        }

        if (lexer->current_char == ',') {
            lexer_advance(lexer);
            return token_create(TOKEN_COMMA, ",", line, column);
        }

        if (lexer->current_char == '|') {
            lexer_advance(lexer);
            return token_create(TOKEN_PIPE, "|", line, column);
        }

        fprintf(stderr, "[LEXER ERROR] Unexpected character '%c' at line %d, column %d\n",
                lexer->current_char, lexer->line, lexer->column);
        lexer_advance(lexer);
        return token_create(TOKEN_ERROR, "Unexpected character", line, column);
    }

    return token_create(TOKEN_EOF, NULL, lexer->line, lexer->column);
}

void token_destroy(Token *token) {
    if (token) {
        free(token->value);
        free(token);
    }
}