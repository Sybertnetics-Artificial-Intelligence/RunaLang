#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// Memory functions
void* allocate(int64_t size) { return calloc(1, size); }
void deallocate(void* ptr) { free(ptr); }
void* reallocate(void* ptr, int64_t old_size, int64_t new_size) {
    void* new_ptr = realloc(ptr, new_size);
    if (new_ptr && new_size > old_size) {
        memset((char*)new_ptr + old_size, 0, new_size - old_size);
    }
    return new_ptr;
}

void* memory_allocate(int64_t size) { return allocate(size); }
void memory_free(void* ptr) { deallocate(ptr); }
void* memory_reallocate(void* ptr, int64_t old_size, int64_t new_size) {
    return reallocate(ptr, old_size, new_size);
}

int64_t memory_get_byte(void* ptr, int64_t offset) {
    return ((unsigned char*)ptr)[offset];
}

void memory_set_byte(void* ptr, int64_t offset, int64_t value) {
    ((unsigned char*)ptr)[offset] = value;
}

int64_t memory_get_integer(void* ptr, int64_t offset) {
    return *(int64_t*)((char*)ptr + offset);
}

void memory_set_integer(void* ptr, int64_t offset, int64_t value) {
    *(int64_t*)((char*)ptr + offset) = value;
}

void* memory_get_pointer(void* ptr, int64_t offset) {
    return *(void**)((char*)ptr + offset);
}

void memory_set_pointer(void* ptr, int64_t offset, void* value) {
    *(void**)((char*)ptr + offset) = value;
}

void memory_copy(void* dest, void* src, int64_t size) {
    memcpy(dest, src, size);
}

void* memory_get_pointer_at_index(void* ptr, int64_t index) {
    return ((void**)ptr)[index];
}

void memory_set_pointer_at_index(void* ptr, int64_t index, void* value) {
    ((void**)ptr)[index] = value;
}

char* memory_pointer_to_string(void* ptr) {
    return (char*)ptr;
}

void* memory_get_substring(const char* str, int64_t start, int64_t length) {
    char* result = malloc(length + 1);
    if (result) {
        strncpy(result, str + start, length);
        result[length] = '\0';
    }
    return result;
}

// File I/O
int64_t file_open_fd(const char* path, int64_t flags) {
    int open_flags = O_RDONLY;
    if (flags == 1) {
        open_flags = O_WRONLY | O_CREAT | O_TRUNC;
    } else if (flags == 2) {
        open_flags = O_RDWR | O_CREAT;
    }
    return open(path, open_flags, 0644);
}

int64_t file_write_fd(int64_t fd, const char* buffer, int64_t size) {
    if (size == 0 && buffer) {
        size = strlen(buffer);
    }
    return write(fd, buffer, size);
}

int64_t file_close_fd(int64_t fd) {
    return close(fd);
}

// System functions
int64_t system_call(int64_t num, int64_t a1, int64_t a2, int64_t a3, int64_t a4, int64_t a5, int64_t a6) {
    return syscall(num, a1, a2, a3, a4, a5, a6);
}

void exit_with_code(int64_t code) {
    exit(code);
}

// String functions (extras)
char* string_concat(const char* a, const char* b) {
    if (!a) return strdup(b);
    if (!b) return strdup(a);
    
    size_t len_a = strlen(a);
    size_t len_b = strlen(b);
    char* result = malloc(len_a + len_b + 1);
    
    if (result) {
        strcpy(result, a);
        strcat(result, b);
    }
    
    return result;
}

char* string_copy(const char* src) {
    return strdup(src);
}

char* string_duplicate(const char* src) {
    return strdup(src);
}

int64_t string_compare(const char* a, const char* b) {
    if (!a && !b) return 0;
    if (!a) return -1;
    if (!b) return 1;
    return strcmp(a, b);
}

int64_t ascii_value_of(const char* str, int64_t index) {
    if (!str || index < 0 || index >= strlen(str)) return 0;
    return (unsigned char)str[index];
}

char* string_substring(const char* str, int64_t start, int64_t length) {
    if (!str) return NULL;
    
    size_t str_len = strlen(str);
    if (start < 0 || start >= str_len) return strdup("");
    
    if (length < 0 || start + length > str_len) {
        length = str_len - start;
    }
    
    char* result = malloc(length + 1);
    if (result) {
        strncpy(result, str + start, length);
        result[length] = '\0';
    }
    
    return result;
}

int64_t string_find(const char* haystack, const char* needle) {
    if (!haystack || !needle) return -1;
    
    char* found = strstr(haystack, needle);
    if (!found) return -1;
    
    return found - haystack;
}

// Command line arguments
static int global_argc = 0;
static char** global_argv = NULL;

void runtime_set_command_line_args(int argc, char** argv) {
    global_argc = argc;
    global_argv = argv;
}

void set_command_line_args(int argc, char** argv) {
    runtime_set_command_line_args(argc, argv);
}

int64_t get_command_line_arg_count() {
    return global_argc;
}

char* get_command_line_arg(int64_t index) {
    if (index < 0 || index >= global_argc) {
        return strdup("");
    }
    return strdup(global_argv[index]);
}

// Runtime helpers
char* runtime_read_file(const char* filename) {
    FILE* f = fopen(filename, "r");
    if (!f) return NULL;

    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);

    char* buffer = malloc(size + 1);
    if (!buffer) {
        fclose(f);
        return NULL;
    }

    fread(buffer, 1, size, f);
    buffer[size] = '\0';
    fclose(f);

    return buffer;
}

// Math functions
double runtime_sin(double degrees) {
    double radians = degrees * M_PI / 180.0;
    return sin(radians);
}

double runtime_cos(double degrees) {
    double radians = degrees * M_PI / 180.0;
    return cos(radians);
}

// Function calling helpers
int64_t call_function_1(void* fn, int64_t arg1) {
    typedef int64_t (*fn_t)(int64_t);
    return ((fn_t)fn)(arg1);
}

int64_t call_function_2(void* fn, int64_t arg1, int64_t arg2) {
    typedef int64_t (*fn_t)(int64_t, int64_t);
    return ((fn_t)fn)(arg1, arg2);
}

int64_t call_function_pointer_2args(void* fn, int64_t arg1, int64_t arg2) {
    return call_function_2(fn, arg1, arg2);
}
