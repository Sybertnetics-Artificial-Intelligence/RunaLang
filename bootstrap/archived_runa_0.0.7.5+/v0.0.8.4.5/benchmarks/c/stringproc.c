#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int string_length(const char* str) {
    int len = 0;
    while (str[len] != '\0') {
        len++;
    }
    return len;
}

void copy_string(char* dest, const char* src) {
    int i = 0;
    while (src[i] != '\0') {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
}

int main() {
    int iterations = 10000;
    char base_str[100] = "Hello";
    char result_str[1000];
    int total_len = 0;

    for (int i = 0; i < iterations; i++) {
        copy_string(result_str, base_str);
        int len = string_length(result_str);
        total_len += len;
    }

    return 0;
}
