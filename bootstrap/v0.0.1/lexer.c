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

static Token* token_create(TokenType type, char *value, int line, int column) {
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

        if (lexer->current_char == '"') {
            char *string = lexer_read_string_literal(lexer);
            if (string) {
                return token_create(TOKEN_STRING_LITERAL, string, line, column);
            } else {
                return token_create(TOKEN_ERROR, "Unterminated string", line, column);
            }
        }

        if (isdigit(lexer->current_char)) {
            char *integer = lexer_read_integer(lexer);
            return token_create(TOKEN_INTEGER, integer, line, column);
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
            } else {
                type = TOKEN_IDENTIFIER;
            }

            return token_create(type, word, line, column);
        }

        if (lexer->current_char == ':') {
            lexer_advance(lexer);
            return token_create(TOKEN_COLON, ":", line, column);
        }

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