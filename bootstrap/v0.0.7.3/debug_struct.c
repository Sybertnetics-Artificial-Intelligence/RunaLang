#include <stdio.h>
#include <stddef.h>
#include "lexer.h"

int main() {
    printf("Token size: %zu\n", sizeof(Token));
    printf("type offset: %zu\n", offsetof(Token, type));
    printf("value offset: %zu\n", offsetof(Token, value));
    printf("line offset: %zu\n", offsetof(Token, line));
    printf("column offset: %zu\n", offsetof(Token, column));
    printf("TokenType size: %zu\n", sizeof(TokenType));
    return 0;
}
