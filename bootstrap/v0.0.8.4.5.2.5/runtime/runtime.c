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

// OVERRIDE: C implementation of string_equals to fix bootstrap bug
// DISABLED: Now provided by string_utils.runa
#if 0
int64_t string_equals(const char* str1, const char* str2) {
    if (!str1 && !str2) return 1;
    if (!str1 || !str2) return 0;
    return strcmp(str1, str2) == 0 ? 1 : 0;
}
#endif

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

// ============================================================================
// LIST RUNTIME - Dynamic array-based list with automatic resizing
// ============================================================================
//
// List structure (in memory):
//   offset 0:  capacity (max elements before resize)
//   offset 8:  length (current number of elements)
//   offset 16: data pointer (pointer to element array)
//
// Each list element is 8 bytes (int64_t)

typedef struct {
    int64_t capacity;
    int64_t length;
    int64_t* data;
} RunaList;

// Create a new empty list with initial capacity of 8
int64_t list_create() {
    RunaList* list = (RunaList*)calloc(1, sizeof(RunaList));
    list->capacity = 8;
    list->length = 0;
    list->data = (int64_t*)calloc(8, sizeof(int64_t));
    return (int64_t)list;
}

// Return the current number of elements in the list
int64_t list_length(int64_t list_ptr) {
    RunaList* list = (RunaList*)list_ptr;
    return list->length;
}

// Resize the list's internal array (private helper)
static void list_resize(RunaList* list, int64_t new_capacity) {
    int64_t* new_data = (int64_t*)calloc(new_capacity, sizeof(int64_t));
    memcpy(new_data, list->data, list->length * sizeof(int64_t));
    free(list->data);
    list->data = new_data;
    list->capacity = new_capacity;
}

// Add element to end of list
int64_t list_append(int64_t list_ptr, int64_t value) {
    RunaList* list = (RunaList*)list_ptr;

    // Resize if needed (double capacity)
    if (list->length >= list->capacity) {
        list_resize(list, list->capacity * 2);
    }

    // Add element at end
    list->data[list->length] = value;
    list->length++;

    return 0;
}

// Get element at index (no bounds checking for now)
int64_t list_get(int64_t list_ptr, int64_t index) {
    RunaList* list = (RunaList*)list_ptr;
    return list->data[index];
}

// Set element at index (no bounds checking for now)
int64_t list_set(int64_t list_ptr, int64_t index, int64_t value) {
    RunaList* list = (RunaList*)list_ptr;
    list->data[index] = value;
    return 0;
}

// Insert element at index, shifting elements right
int64_t list_insert(int64_t list_ptr, int64_t index, int64_t value) {
    RunaList* list = (RunaList*)list_ptr;

    // Resize if needed
    if (list->length >= list->capacity) {
        list_resize(list, list->capacity * 2);
    }

    // Shift elements right
    for (int64_t i = list->length; i > index; i--) {
        list->data[i] = list->data[i - 1];
    }

    // Insert new element
    list->data[index] = value;
    list->length++;

    return 0;
}

// Remove and return element at index, shifting elements left
int64_t list_remove(int64_t list_ptr, int64_t index) {
    RunaList* list = (RunaList*)list_ptr;

    int64_t value = list->data[index];

    // Shift elements left
    for (int64_t i = index; i < list->length - 1; i++) {
        list->data[i] = list->data[i + 1];
    }

    list->length--;
    return value;
}

// Remove all elements from list
int64_t list_clear(int64_t list_ptr) {
    RunaList* list = (RunaList*)list_ptr;
    list->length = 0;
    return 0;
}

// Free all memory associated with list
int64_t list_destroy(int64_t list_ptr) {
    RunaList* list = (RunaList*)list_ptr;
    free(list->data);
    free(list);
    return 0;
}

// ============================================================================
// SET OPERATIONS
// ============================================================================
//
// Set structure (hash set with linear probing):
//   offset 0:  capacity (size of hash table)
//   offset 8:  count (number of elements)
//   offset 16: data pointer (hash table array)
//   offset 24: used pointer (bitmap of used slots)
//
// Each element is 8 bytes (int64_t)

typedef struct {
    int64_t capacity;
    int64_t count;
    int64_t* data;      // Hash table
    int8_t* used;       // Bitmap: 1 if slot is used, 0 if empty
} RunaSet;

// Set functions for collections
#if 1

// Create a new empty set with initial capacity of 16
int64_t set_create() {
    RunaSet* set = (RunaSet*)calloc(1, sizeof(RunaSet));
    set->capacity = 16;
    set->count = 0;
    set->data = (int64_t*)calloc(16, sizeof(int64_t));
    set->used = (int8_t*)calloc(16, sizeof(int8_t));
    return (int64_t)set;
}

// Simple hash function for int64_t
static int64_t set_hash(int64_t value, int64_t capacity) {
    // Mix bits and modulo by capacity
    uint64_t h = (uint64_t)value;
    h ^= h >> 33;
    h *= 0xff51afd7ed558ccdULL;
    h ^= h >> 33;
    h *= 0xc4ceb9fe1a85ec53ULL;
    h ^= h >> 33;
    return (int64_t)(h % (uint64_t)capacity);
}

// Resize set's hash table (private helper)
static void set_resize(RunaSet* set, int64_t new_capacity) {
    int64_t* old_data = set->data;
    int8_t* old_used = set->used;
    int64_t old_capacity = set->capacity;

    set->data = (int64_t*)calloc(new_capacity, sizeof(int64_t));
    set->used = (int8_t*)calloc(new_capacity, sizeof(int8_t));
    set->capacity = new_capacity;
    set->count = 0;

    // Rehash all existing elements
    for (int64_t i = 0; i < old_capacity; i++) {
        if (old_used[i]) {
            // Re-insert this element
            int64_t value = old_data[i];
            int64_t index = set_hash(value, new_capacity);

            // Linear probing to find empty slot
            while (set->used[index]) {
                index = (index + 1) % new_capacity;
            }

            set->data[index] = value;
            set->used[index] = 1;
            set->count++;
        }
    }

    free(old_data);
    free(old_used);
}

// Add element to set (returns 1 if added, 0 if already exists)
int64_t set_add(int64_t set_ptr, int64_t value) {
    RunaSet* set = (RunaSet*)set_ptr;

    // Resize if load factor > 0.7
    if (set->count * 10 > set->capacity * 7) {
        set_resize(set, set->capacity * 2);
    }

    int64_t index = set_hash(value, set->capacity);

    // Linear probing to find slot
    while (set->used[index]) {
        if (set->data[index] == value) {
            return 0;  // Already exists
        }
        index = (index + 1) % set->capacity;
    }

    // Found empty slot
    set->data[index] = value;
    set->used[index] = 1;
    set->count++;
    return 1;
}

// Check if set contains element (returns 1 if yes, 0 if no)
int64_t set_contains(int64_t set_ptr, int64_t value) {
    RunaSet* set = (RunaSet*)set_ptr;

    int64_t index = set_hash(value, set->capacity);
    int64_t start = index;

    // Linear probing to find element
    while (set->used[index]) {
        if (set->data[index] == value) {
            return 1;  // Found
        }
        index = (index + 1) % set->capacity;
        if (index == start) break;  // Wrapped around
    }

    return 0;  // Not found
}

// Remove element from set (returns 1 if removed, 0 if not found)
int64_t set_remove(int64_t set_ptr, int64_t value) {
    RunaSet* set = (RunaSet*)set_ptr;

    int64_t index = set_hash(value, set->capacity);
    int64_t start = index;

    // Linear probing to find element
    while (set->used[index]) {
        if (set->data[index] == value) {
            // Found - mark as deleted
            set->used[index] = 0;
            set->count--;

            // Rehash subsequent elements to fix probe chains
            int64_t next = (index + 1) % set->capacity;
            while (set->used[next]) {
                int64_t rehash_value = set->data[next];
                set->used[next] = 0;
                set->count--;
                set_add(set_ptr, rehash_value);
                next = (next + 1) % set->capacity;
            }

            return 1;  // Removed
        }
        index = (index + 1) % set->capacity;
        if (index == start) break;
    }

    return 0;  // Not found
}

// Get number of elements in set
int64_t set_size(int64_t set_ptr) {
    RunaSet* set = (RunaSet*)set_ptr;
    return set->count;
}

// Create union of two sets (returns new set)
int64_t set_union(int64_t set1_ptr, int64_t set2_ptr) {
    RunaSet* set1 = (RunaSet*)set1_ptr;
    RunaSet* set2 = (RunaSet*)set2_ptr;

    int64_t result = set_create();

    // Add all elements from set1
    for (int64_t i = 0; i < set1->capacity; i++) {
        if (set1->used[i]) {
            set_add(result, set1->data[i]);
        }
    }

    // Add all elements from set2
    for (int64_t i = 0; i < set2->capacity; i++) {
        if (set2->used[i]) {
            set_add(result, set2->data[i]);
        }
    }

    return result;
}

// Create intersection of two sets (returns new set)
int64_t set_intersection(int64_t set1_ptr, int64_t set2_ptr) {
    RunaSet* set1 = (RunaSet*)set1_ptr;
    RunaSet* set2 = (RunaSet*)set2_ptr;

    int64_t result = set_create();

    // Add elements that are in both sets
    for (int64_t i = 0; i < set1->capacity; i++) {
        if (set1->used[i]) {
            int64_t value = set1->data[i];
            if (set_contains(set2_ptr, value)) {
                set_add(result, value);
            }
        }
    }

    return result;
}

// Convert set to list (returns new list with all elements)
int64_t set_to_list(int64_t set_ptr) {
    RunaSet* set = (RunaSet*)set_ptr;
    int64_t list = list_create();

    for (int64_t i = 0; i < set->capacity; i++) {
        if (set->used[i]) {
            list_append(list, set->data[i]);
        }
    }

    return list;
}

// Destroy set and free memory
int64_t set_destroy(int64_t set_ptr) {
    RunaSet* set = (RunaSet*)set_ptr;
    free(set->data);
    free(set->used);
    free(set);
    return 0;
}

#endif // End of disabled set functions

// ============================================================================
// DICTIONARY OPERATIONS
// ============================================================================
//
// Dictionary structure (hash map with linear probing):
//   offset 0:  capacity (size of hash table)
//   offset 8:  count (number of key-value pairs)
//   offset 16: keys pointer (hash table for keys)
//   offset 24: values pointer (hash table for values)
//   offset 32: used pointer (bitmap of used slots)
//
// Keys and values are both int64_t (can store pointers to strings or integers)

typedef struct {
    int64_t capacity;
    int64_t count;
    int64_t* keys;      // Hash table for keys
    int64_t* values;    // Hash table for values
    int8_t* used;       // Bitmap: 1 if slot is used, 0 if empty
} RunaDict;

// Create a new empty dictionary with initial capacity of 16
int64_t dict_create() {
    RunaDict* dict = (RunaDict*)calloc(1, sizeof(RunaDict));
    dict->capacity = 16;
    dict->count = 0;
    dict->keys = (int64_t*)calloc(16, sizeof(int64_t));
    dict->values = (int64_t*)calloc(16, sizeof(int64_t));
    dict->used = (int8_t*)calloc(16, sizeof(int8_t));
    return (int64_t)dict;
}

// Hash function for dictionary keys (same as set hash)
static int64_t dict_hash(int64_t key, int64_t capacity) {
    uint64_t h = (uint64_t)key;
    h ^= h >> 33;
    h *= 0xff51afd7ed558ccdULL;
    h ^= h >> 33;
    h *= 0xc4ceb9fe1a85ec53ULL;
    h ^= h >> 33;
    return (int64_t)(h % (uint64_t)capacity);
}

// Resize dictionary's hash tables (private helper)
static void dict_resize(RunaDict* dict, int64_t new_capacity) {
    int64_t* old_keys = dict->keys;
    int64_t* old_values = dict->values;
    int8_t* old_used = dict->used;
    int64_t old_capacity = dict->capacity;

    dict->keys = (int64_t*)calloc(new_capacity, sizeof(int64_t));
    dict->values = (int64_t*)calloc(new_capacity, sizeof(int64_t));
    dict->used = (int8_t*)calloc(new_capacity, sizeof(int8_t));
    dict->capacity = new_capacity;
    dict->count = 0;

    // Rehash all existing key-value pairs
    for (int64_t i = 0; i < old_capacity; i++) {
        if (old_used[i]) {
            // Re-insert this pair
            int64_t key = old_keys[i];
            int64_t value = old_values[i];
            int64_t index = dict_hash(key, new_capacity);

            // Linear probing to find empty slot
            while (dict->used[index]) {
                index = (index + 1) % new_capacity;
            }

            dict->keys[index] = key;
            dict->values[index] = value;
            dict->used[index] = 1;
            dict->count++;
        }
    }

    free(old_keys);
    free(old_values);
    free(old_used);
}

// Set key-value pair in dictionary (replaces existing value if key exists)
int64_t dict_set(int64_t dict_ptr, int64_t key, int64_t value) {
    RunaDict* dict = (RunaDict*)dict_ptr;

    // Resize if load factor > 0.7
    if (dict->count * 10 > dict->capacity * 7) {
        dict_resize(dict, dict->capacity * 2);
    }

    int64_t index = dict_hash(key, dict->capacity);

    // Linear probing to find slot
    while (dict->used[index]) {
        if (dict->keys[index] == key) {
            // Key exists - update value
            dict->values[index] = value;
            return 0;
        }
        index = (index + 1) % dict->capacity;
    }

    // Found empty slot - insert new pair
    dict->keys[index] = key;
    dict->values[index] = value;
    dict->used[index] = 1;
    dict->count++;
    return 1;
}

// Get value for key (returns 0 if key not found - caller should check dict_has first)
int64_t dict_get(int64_t dict_ptr, int64_t key) {
    RunaDict* dict = (RunaDict*)dict_ptr;

    int64_t index = dict_hash(key, dict->capacity);
    int64_t start = index;

    // Linear probing to find key
    while (dict->used[index]) {
        if (dict->keys[index] == key) {
            return dict->values[index];
        }
        index = (index + 1) % dict->capacity;
        if (index == start) break;
    }

    return 0;  // Not found
}

// Check if dictionary has key (returns 1 if yes, 0 if no)
int64_t dict_has(int64_t dict_ptr, int64_t key) {
    RunaDict* dict = (RunaDict*)dict_ptr;

    int64_t index = dict_hash(key, dict->capacity);
    int64_t start = index;

    // Linear probing to find key
    while (dict->used[index]) {
        if (dict->keys[index] == key) {
            return 1;
        }
        index = (index + 1) % dict->capacity;
        if (index == start) break;
    }

    return 0;
}

// Remove key-value pair from dictionary (returns 1 if removed, 0 if not found)
int64_t dict_remove(int64_t dict_ptr, int64_t key) {
    RunaDict* dict = (RunaDict*)dict_ptr;

    int64_t index = dict_hash(key, dict->capacity);
    int64_t start = index;

    // Linear probing to find key
    while (dict->used[index]) {
        if (dict->keys[index] == key) {
            // Found - mark as deleted
            dict->used[index] = 0;
            dict->count--;

            // Rehash subsequent entries to fix probe chains
            int64_t next = (index + 1) % dict->capacity;
            while (dict->used[next]) {
                int64_t rehash_key = dict->keys[next];
                int64_t rehash_value = dict->values[next];
                dict->used[next] = 0;
                dict->count--;
                dict_set(dict_ptr, rehash_key, rehash_value);
                next = (next + 1) % dict->capacity;
            }

            return 1;
        }
        index = (index + 1) % dict->capacity;
        if (index == start) break;
    }

    return 0;
}

// Get number of key-value pairs in dictionary
int64_t dict_size(int64_t dict_ptr) {
    RunaDict* dict = (RunaDict*)dict_ptr;
    return dict->count;
}

// Get list of all keys in dictionary
int64_t dict_keys(int64_t dict_ptr) {
    RunaDict* dict = (RunaDict*)dict_ptr;
    int64_t list = list_create();

    for (int64_t i = 0; i < dict->capacity; i++) {
        if (dict->used[i]) {
            list_append(list, dict->keys[i]);
        }
    }

    return list;
}

// Get list of all values in dictionary
int64_t dict_values(int64_t dict_ptr) {
    RunaDict* dict = (RunaDict*)dict_ptr;
    int64_t list = list_create();

    for (int64_t i = 0; i < dict->capacity; i++) {
        if (dict->used[i]) {
            list_append(list, dict->values[i]);
        }
    }

    return list;
}

// Destroy dictionary and free memory
int64_t dict_destroy(int64_t dict_ptr) {
    RunaDict* dict = (RunaDict*)dict_ptr;
    free(dict->keys);
    free(dict->values);
    free(dict->used);
    free(dict);
    return 0;
}
