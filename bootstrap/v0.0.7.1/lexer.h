/*
 * Copyright 2025 Sybertnetics Artificial Intelligence Solutions
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
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