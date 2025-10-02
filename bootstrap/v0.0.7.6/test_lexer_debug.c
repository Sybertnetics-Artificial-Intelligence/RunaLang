#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Minimal test to see what tokens the lexer produces for "Type called"
extern void* lexer_create(const char* source);
extern void* lexer_next_token(void* lexer);
extern int memory_get_int32(void* ptr, int offset);
extern void* memory_get_pointer(void* ptr, int offset);

int main() {
    const char* source = "Type called \"Point\":\n    x as Integer\nEnd Type\n";

    void* lexer = lexer_create(source);
    printf("Lexer created\n");

    for (int i = 0; i < 15; i++) {
        void* token = lexer_next_token(lexer);
        if (!token) break;

        int token_type = memory_get_int32(token, 0);
        void* value = memory_get_pointer(token, 8);

        printf("Token %d: type=%d", i, token_type);
        if (value) {
            printf(" value='%s'", (char*)value);
        }
        printf("\n");

        if (token_type == 0) break; // EOF
    }

    return 0;
}
