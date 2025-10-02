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
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include "runtime_io.h"

// Maximum file size we'll read (10MB)
#define MAX_FILE_SIZE (10 * 1024 * 1024)

// Get file size
int64_t runtime_get_file_size(const char* filename) {
    struct stat st;
    if (stat(filename, &st) != 0) {
        return -1;
    }
    return (int64_t)st.st_size;
}

// Read entire file contents into a string
char* runtime_read_file(const char* filename) {
    if (!filename) {
        fprintf(stderr, "[RUNTIME ERROR] read_file: NULL filename\n");
        return NULL;
    }

    // Get file size
    int64_t size = runtime_get_file_size(filename);
    if (size < 0) {
        fprintf(stderr, "[RUNTIME ERROR] read_file: Cannot stat file '%s'\n", filename);
        return NULL;
    }

    if (size > MAX_FILE_SIZE) {
        fprintf(stderr, "[RUNTIME ERROR] read_file: File '%s' too large (%ld bytes, max %d)\n",
                filename, size, MAX_FILE_SIZE);
        return NULL;
    }

    // Open file
    FILE* file = fopen(filename, "rb");
    if (!file) {
        fprintf(stderr, "[RUNTIME ERROR] read_file: Cannot open file '%s'\n", filename);
        return NULL;
    }

    // Allocate buffer for content (+1 for null terminator)
    char* content = (char*)malloc(size + 1);
    if (!content) {
        fprintf(stderr, "[RUNTIME ERROR] read_file: Cannot allocate %ld bytes for file content\n",
                size + 1);
        fclose(file);
        return NULL;
    }

    // Read file content
    size_t bytes_read = fread(content, 1, size, file);
    if (bytes_read != (size_t)size) {
        fprintf(stderr, "[RUNTIME ERROR] read_file: Read %zu bytes, expected %ld\n",
                bytes_read, size);
        free(content);
        fclose(file);
        return NULL;
    }

    // Null terminate the string
    content[size] = '\0';

    fclose(file);
    return content;
}

// Write string content to file
int64_t runtime_write_file(const char* filename, const char* content) {
    if (!filename) {
        fprintf(stderr, "[RUNTIME ERROR] write_file: NULL filename\n");
        return 1;
    }

    if (!content) {
        fprintf(stderr, "[RUNTIME ERROR] write_file: NULL content\n");
        return 1;
    }

    // Open file for writing
    FILE* file = fopen(filename, "wb");
    if (!file) {
        fprintf(stderr, "[RUNTIME ERROR] write_file: Cannot open file '%s' for writing\n", filename);
        return 1;
    }

    // Write content
    size_t content_len = strlen(content);
    size_t bytes_written = fwrite(content, 1, content_len, file);

    if (bytes_written != content_len) {
        fprintf(stderr, "[RUNTIME ERROR] write_file: Wrote %zu bytes, expected %zu\n",
                bytes_written, content_len);
        fclose(file);
        return 1;
    }

    fclose(file);
    return 0;  // Success
}