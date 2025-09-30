/*
 * Copyright 2025 Sybertnetics Artificial Intelligence Solutions
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
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

// Memory functions - v0.0.7.5 expects these exact names
void* allocate(int64_t size) { return calloc(1, size); }
void deallocate(void* ptr) { free(ptr); }
// No need to redefine realloc - it's a standard C function
// The Runa compiler generates calls to the standard realloc

// Three-parameter version for backward compatibility
void* reallocate(void* ptr, int64_t old_size, int64_t new_size) {
    void* new_ptr = realloc(ptr, new_size);
    if (new_ptr && new_size > old_size) {
        memset((char*)new_ptr + old_size, 0, new_size - old_size);
    }
    return new_ptr;
}

// Simple realloc wrapper that preserves existing data without zeroing
void* memory_realloc(void* ptr, int64_t new_size) {
    return realloc(ptr, new_size);
}

// These are already implemented in v0.0.7.5 Runa code
// void* memory_allocate(int64_t size) - implemented in string_utils.runa
// void* memory_reallocate() - implemented in string_utils.runa

// But v0.0.7.3-generated code might need it
// Commented out - already defined in string_utils.o
// void* memory_allocate(int64_t size) { return calloc(1, size); }

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

// 32-bit memory access functions for struct fields that are int32_t
int32_t memory_get_int32(void* ptr, int64_t offset) {
    return *(int32_t*)((char*)ptr + offset);
}

void memory_set_int32(void* ptr, int64_t offset, int32_t value) {
    *(int32_t*)((char*)ptr + offset) = value;
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
int64_t file_open_fd(const char* path) {
    return open(path, O_WRONLY | O_CREAT | O_TRUNC, 0644);
}

int64_t file_open_fd_with_flags(const char* path, int64_t flags) {
    int open_flags = O_RDONLY;
    if (flags == 1) {
        open_flags = O_WRONLY | O_CREAT | O_TRUNC;
    } else if (flags == 2) {
        open_flags = O_RDWR | O_CREAT;
    }
    return open(path, open_flags, 0644);
}

void file_write_fd(int64_t fd, const char* buffer) {
    write(fd, buffer, strlen(buffer));
}

int64_t file_write_fd_with_size(int64_t fd, const char* buffer, int64_t size) {
    if (size == 0 && buffer) {
        size = strlen(buffer);
    }
    return write(fd, buffer, size);
}

void file_close_fd(int64_t fd) {
    close(fd);
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

// Function calling helpers - commented out, already in assembly
// int64_t call_function_1(void* fn, void* arg) - in hashtable.o
// int64_t call_function_2(void* fn, void* arg1, void* arg2) - in hashtable.o

// This one is needed by containers.o but not defined there
int64_t call_function_pointer_2args(void* fn, void* arg1, void* arg2) {
    typedef int64_t (*func_ptr)(void*, void*);
    return ((func_ptr)fn)(arg1, arg2);
}

// String functions needed by v0.0.7.3-generated code
// These are already defined in the assembly:
// void string_copy(char* dest, char* src) - in lexer.o
// char* string_duplicate(char* str) - in string_utils.o
// void string_copy_n(char* dest, char* src, int64_t start, int64_t length) - in lexer.o
// void print_char(int64_t ch) - in lexer.o

// These are already defined in string_utils.s:
// char* integer_to_string(int64_t value) - in string_utils.o
// int64_t string_length(char* str) - in string_utils.o
// int64_t string_equals(char* str1, char* str2) - in string_utils.o

void print(char* str) {
    printf("%s\n", str);
}

int64_t write_file(char* filename, char* content) {
    FILE* file = fopen(filename, "w");
    if (!file) return 0;

    int64_t length = strlen(content);
    int64_t written = fwrite(content, 1, length, file);
    fclose(file);

    return written == length;
}

// Buffered file writing for codegen
// This provides fprintf-like buffered writing using file descriptors
typedef struct {
    int fd;
    char *buffer;
    int64_t buffer_size;
    int64_t buffer_capacity;
} BufferedFile;

static BufferedFile *buffered_files[256] = {0};  // Handle table (max 256 open files)
static int next_handle = 1;

// Open file with buffering - returns handle (not fd)
int64_t file_open_buffered(const char *path, int64_t flags) {
    int open_flags = O_RDONLY;
    if (flags == 1) {
        open_flags = O_WRONLY | O_CREAT | O_TRUNC;
    } else if (flags == 2) {
        open_flags = O_RDWR | O_CREAT;
    }

    int fd = open(path, open_flags, 0644);
    if (fd == -1) {
        return -1;
    }

    // Create buffered file structure
    BufferedFile *bf = malloc(sizeof(BufferedFile));
    if (!bf) {
        close(fd);
        return -1;
    }

    bf->fd = fd;
    bf->buffer_capacity = 65536;  // 64KB initial buffer
    bf->buffer = malloc(bf->buffer_capacity);
    if (!bf->buffer) {
        free(bf);
        close(fd);
        return -1;
    }
    bf->buffer_size = 0;

    // Find free handle slot
    int handle = next_handle;
    for (int i = 1; i < 256; i++) {
        if (buffered_files[i] == NULL) {
            handle = i;
            break;
        }
    }

    buffered_files[handle] = bf;
    if (handle >= next_handle) {
        next_handle = handle + 1;
    }

    return handle;
}

// Write to buffered file
int64_t file_write_buffered(int64_t handle, const char *data, int64_t size) {
    if (handle < 1 || handle >= 256 || !buffered_files[handle]) {
        return -1;
    }

    BufferedFile *bf = buffered_files[handle];

    // Calculate actual size if 0 (use strlen)
    if (size == 0 && data) {
        size = strlen(data);
    }

    if (size == 0) {
        return 0;
    }

    // Grow buffer if needed
    while (bf->buffer_size + size > bf->buffer_capacity) {
        bf->buffer_capacity *= 2;
        char *new_buffer = realloc(bf->buffer, bf->buffer_capacity);
        if (!new_buffer) {
            return -1;
        }
        bf->buffer = new_buffer;
    }

    // Append to buffer
    memcpy(bf->buffer + bf->buffer_size, data, size);
    bf->buffer_size += size;

    return size;
}

// Close buffered file (flushes and frees resources)
void file_close_buffered(int64_t handle) {
    if (handle < 1 || handle >= 256 || !buffered_files[handle]) {
        return;
    }

    BufferedFile *bf = buffered_files[handle];

    // Flush buffer to disk
    if (bf->buffer_size > 0) {
        ssize_t written = write(bf->fd, bf->buffer, bf->buffer_size);
        (void)written;  // Suppress unused variable warning
    }

    // Close and free
    close(bf->fd);
    free(bf->buffer);
    free(bf);
    buffered_files[handle] = NULL;
}
