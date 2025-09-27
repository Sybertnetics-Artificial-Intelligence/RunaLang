#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Simplified test to see what tokens are generated
int main() {
    const char* test_input = "bit_and";
    printf("Testing lexer with input: '%s'\n", test_input);

    // This would normally call lexer functions, but for now just manual check
    if (strcmp(test_input, "bit_and") == 0) {
        printf("Should return TOKEN_BIT_AND (39)\n");
    }

    return 0;
}