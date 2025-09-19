#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

// Memory management for strings
#define MAX_STRING_LENGTH 65536

// String concatenation - MOST CRITICAL FUNCTION (255 uses)
char* concat(const char* str1, const char* str2) {
    if (!str1 || !str2) return NULL;

    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);

    char* result = malloc(len1 + len2 + 1);
    if (!result) return NULL;

    strcpy(result, str1);
    strcat(result, str2);

    return result;
}

// String length - CRITICAL FUNCTION (74 uses)
long length_of(const char* str) {
    if (!str) return 0;
    return (long)strlen(str);
}

// Substring extraction - CRITICAL FUNCTION (57 uses)
char* substring(const char* str, long start, long length) {
    if (!str) return NULL;

    long str_len = strlen(str);

    // Bounds checking
    if (start < 0 || start >= str_len || length <= 0) {
        char* empty = malloc(1);
        if (empty) empty[0] = '\0';
        return empty;
    }

    // Adjust length if it extends beyond string
    if (start + length > str_len) {
        length = str_len - start;
    }

    char* result = malloc(length + 1);
    if (!result) return NULL;

    strncpy(result, str + start, length);
    result[length] = '\0';

    return result;
}

// Character access - CRITICAL FUNCTION (31 uses)
long char_at(const char* str, long index) {
    if (!str) return 0;

    long str_len = strlen(str);
    if (index < 0 || index >= str_len) return 0;

    return (long)(unsigned char)str[index];
}

// Integer to string conversion - SECONDARY FUNCTION (7 uses)
char* to_string(long value) {
    char* result = malloc(32); // Enough for 64-bit integer
    if (!result) return NULL;

    snprintf(result, 32, "%ld", value);
    return result;
}

// File reading - MINIMAL FUNCTION (3 uses)
char* read_file(const char* filename) {
    if (!filename) return NULL;

    int fd = open(filename, O_RDONLY);
    if (fd == -1) {
        char* empty = malloc(1);
        if (empty) empty[0] = '\0';
        return empty;
    }

    // Get file size
    off_t size = lseek(fd, 0, SEEK_END);
    lseek(fd, 0, SEEK_SET);

    if (size <= 0 || size > MAX_STRING_LENGTH) {
        close(fd);
        char* empty = malloc(1);
        if (empty) empty[0] = '\0';
        return empty;
    }

    char* content = malloc(size + 1);
    if (!content) {
        close(fd);
        return NULL;
    }

    ssize_t bytes_read = read(fd, content, size);
    close(fd);

    if (bytes_read != size) {
        free(content);
        char* empty = malloc(1);
        if (empty) empty[0] = '\0';
        return empty;
    }

    content[size] = '\0';
    return content;
}

// File writing - MINIMAL FUNCTION (3 uses)
long write_file(const char* filename, const char* content) {
    if (!filename || !content) return 0;

    int fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) return 0;

    size_t content_len = strlen(content);
    ssize_t bytes_written = write(fd, content, content_len);
    close(fd);

    return (bytes_written == (ssize_t)content_len) ? 1 : 0;
}

// Memory cleanup function (for future use)
void runa_free(void* ptr) {
    if (ptr) free(ptr);
}