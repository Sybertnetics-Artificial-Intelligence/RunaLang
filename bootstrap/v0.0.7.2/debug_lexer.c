#include <stdio.h>
#include "lexer.h"

int main() {
    char *test_code = "Inline Assembly: \"nop\\n\" Note: Test End Assembly";

    Lexer *lexer = lexer_create(test_code);

    Token *token;
    while ((token = lexer_next_token(lexer)) && token->type != TOKEN_EOF) {
        printf("Token Type: %d, Value: '%s'\n", token->type, token->value ? token->value : "NULL");
        token_destroy(token);
    }

    token_destroy(token);
    lexer_destroy(lexer);
    return 0;
}