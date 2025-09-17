#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

// String operations
char* concat(const char* str1, const char* str2) {
    if (!str1) str1 = "";
    if (!str2) str2 = "";

    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);
    char* result = malloc(len1 + len2 + 1);

    strcpy(result, str1);
    strcat(result, str2);
    return result;
}

int length_of(const char* str) {
    if (!str) return 0;
    return strlen(str);
}

int char_at(const char* str, int index) {
    if (!str || index < 0 || index >= strlen(str)) {
        return -1; // Out of bounds
    }
    return (unsigned char)str[index];
}

char* substring(const char* str, int start, int end) {
    if (!str) return strdup("");

    int len = strlen(str);
    if (start < 0) start = 0;
    if (end > len) end = len;
    if (start >= end) return strdup("");

    int sub_len = end - start;
    char* result = malloc(sub_len + 1);
    strncpy(result, str + start, sub_len);
    result[sub_len] = '\0';
    return result;
}

char* to_string(int value) {
    char* result = malloc(32); // Enough for any 32-bit integer
    snprintf(result, 32, "%d", value);
    return result;
}

// I/O operations
char* read_file(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        return strdup(""); // Return empty string on error
    }

    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    fseek(file, 0, SEEK_SET);

    char* content = malloc(length + 1);
    fread(content, 1, length, file);
    content[length] = '\0';

    fclose(file);
    return content;
}

int write_file(const char* filename, const char* content) {
    FILE* file = fopen(filename, "w");
    if (!file) {
        return 0; // Failed
    }

    fprintf(file, "%s", content);
    fclose(file);
    return 1; // Success
}

// Display function - outputs to stdout
void runa_display_string(const char* str) {
    if (str) {
        printf("%s\n", str);
    }
}

void runa_display_int(int value) {
    printf("%d\n", value);
}

// Memory cleanup (for proper memory management)
void runa_free_string(char* str) {
    if (str) {
        free(str);
    }
}

// String to integer conversion
int string_to_integer(const char* str) {
    if (!str) return 0;
    return atoi(str);
}

// Entry point support - programs will provide their own _start