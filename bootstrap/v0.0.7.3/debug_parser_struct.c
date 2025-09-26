#include <stdio.h>
#include <stddef.h>
#include "parser.h"

int main() {
    printf("Parser size: %zu\n", sizeof(Parser));
    printf("lexer offset: %zu\n", offsetof(Parser, lexer));
    printf("current_token offset: %zu\n", offsetof(Parser, current_token));
    printf("current_program offset: %zu\n", offsetof(Parser, current_program));
    return 0;
}
