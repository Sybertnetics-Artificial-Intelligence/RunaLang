#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    const char* original = "Hello";
    int start = 0;
    int length = 2;

    char* result = malloc(length + 1);
    memcpy(result, original + start, length);
    result[length] = '\0';

    printf("Original: %s\n", original);
    printf("Substring: %s\n", result);
    printf("Length: %d\n", (int)strlen(result));

    free(result);
    return 0;
}