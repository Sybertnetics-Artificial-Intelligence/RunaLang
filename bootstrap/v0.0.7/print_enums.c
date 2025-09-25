#include <stdio.h>
#include "lexer.h"

int main() {
    printf("TOKEN_EOF = %d\n", TOKEN_EOF);
    printf("TOKEN_TYPE = %d\n", TOKEN_TYPE);
    printf("TOKEN_DOT = %d\n", TOKEN_DOT);
    printf("TOKEN_IDENTIFIER = %d\n", TOKEN_IDENTIFIER);
    printf("TOKEN_AS = %d\n", TOKEN_AS);
    printf("TOKEN_BY = %d\n", TOKEN_BY);
    printf("TOKEN_PRINT = %d\n", TOKEN_PRINT);
    return 0;
}