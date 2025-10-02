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
#include <sys/stat.h>
#include <unistd.h>
#include "runtime_io.h"

// Maximum file size we'll read (10MB)
#define MAX_FILE_SIZE (10 * 1024 * 1024)

// File handle management
#define MAX_OPEN_FILES 256
#define LINE_BUFFER_SIZE 4096

typedef struct {
    FILE* file;
    char* filename;
    int mode; // 0=read, 1=write, 2=append
} FileHandle;

static FileHandle file_handles[MAX_OPEN_FILES];
static int file_handles_initialized = 0;

static void init_file_handles() {
    if (!file_handles_initialized) {
        for (int i = 0; i < MAX_OPEN_FILES; i++) {
            file_handles[i].file = NULL;
            file_handles[i].filename = NULL;
            file_handles[i].mode = 0;
        }
        file_handles_initialized = 1;
    }
}

static int64_t allocate_file_handle(FILE* file, const char* filename, int mode) {
    init_file_handles();
    for (int64_t i = 0; i < MAX_OPEN_FILES; i++) {
        if (file_handles[i].file == NULL) {
            file_handles[i].file = file;
            file_handles[i].filename = strdup(filename);
            file_handles[i].mode = mode;
            return i;
        }
    }
    return -1; // No available handles
}

static void free_file_handle(int64_t handle) {
    if (handle >= 0 && handle < MAX_OPEN_FILES) {
        if (file_handles[handle].filename) {
            free(file_handles[handle].filename);
            file_handles[handle].filename = NULL;
        }
        file_handles[handle].file = NULL;
        file_handles[handle].mode = 0;
    }
}

static FILE* get_file_from_handle(int64_t handle) {
    if (handle >= 0 && handle < MAX_OPEN_FILES) {
        return file_handles[handle].file;
    }
    return NULL;
}

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

// Open file with mode ("r", "w", "a") and return handle
int64_t runtime_file_open(const char* filename, const char* mode) {
    if (!filename) {
        fprintf(stderr, "[RUNTIME ERROR] file_open: NULL filename\n");
        return -1;
    }
    if (!mode) {
        fprintf(stderr, "[RUNTIME ERROR] file_open: NULL mode\n");
        return -1;
    }

    FILE* file = fopen(filename, mode);
    if (!file) {
        fprintf(stderr, "[RUNTIME ERROR] file_open: Cannot open file '%s' with mode '%s'\n", filename, mode);
        return -1;
    }

    int file_mode = 0;
    if (strchr(mode, 'w')) file_mode = 1;
    else if (strchr(mode, 'a')) file_mode = 2;

    int64_t handle = allocate_file_handle(file, filename, file_mode);
    if (handle < 0) {
        fprintf(stderr, "[RUNTIME ERROR] file_open: Too many open files\n");
        fclose(file);
        return -1;
    }

    return handle;
}

// Close file handle
int64_t runtime_file_close(int64_t handle) {
    FILE* file = get_file_from_handle(handle);
    if (!file) {
        fprintf(stderr, "[RUNTIME ERROR] file_close: Invalid file handle %ld\n", handle);
        return 1;
    }

    int result = fclose(file);
    free_file_handle(handle);
    return result == 0 ? 0 : 1;
}

// Read a line from file
char* runtime_file_read_line(int64_t handle) {
    FILE* file = get_file_from_handle(handle);
    if (!file) {
        fprintf(stderr, "[RUNTIME ERROR] file_read_line: Invalid file handle %ld\n", handle);
        return NULL;
    }

    char* line = (char*)malloc(LINE_BUFFER_SIZE);
    if (!line) {
        fprintf(stderr, "[RUNTIME ERROR] file_read_line: Cannot allocate line buffer\n");
        return NULL;
    }

    if (fgets(line, LINE_BUFFER_SIZE, file) == NULL) {
        free(line);
        return NULL; // EOF or error
    }

    // Remove newline if present
    size_t len = strlen(line);
    if (len > 0 && line[len-1] == '\n') {
        line[len-1] = '\0';
    }

    return line;
}

// Write a line to file
int64_t runtime_file_write_line(int64_t handle, const char* line) {
    FILE* file = get_file_from_handle(handle);
    if (!file) {
        fprintf(stderr, "[RUNTIME ERROR] file_write_line: Invalid file handle %ld\n", handle);
        return 1;
    }

    if (!line) {
        fprintf(stderr, "[RUNTIME ERROR] file_write_line: NULL line\n");
        return 1;
    }

    if (fprintf(file, "%s\n", line) < 0) {
        fprintf(stderr, "[RUNTIME ERROR] file_write_line: Write failed\n");
        return 1;
    }

    return 0;
}

// Check if file exists
int64_t runtime_file_exists(const char* filename) {
    if (!filename) {
        fprintf(stderr, "[RUNTIME ERROR] file_exists: NULL filename\n");
        return 0;
    }

    return access(filename, F_OK) == 0 ? 1 : 0;
}

// Delete a file
int64_t runtime_file_delete(const char* filename) {
    if (!filename) {
        fprintf(stderr, "[RUNTIME ERROR] file_delete: NULL filename\n");
        return 1;
    }

    return remove(filename) == 0 ? 0 : 1;
}

// Get file size (already implemented)
int64_t runtime_file_size(const char* filename) {
    return runtime_get_file_size(filename);
}

// Set file position
int64_t runtime_file_seek(int64_t handle, int64_t offset, int64_t whence) {
    FILE* file = get_file_from_handle(handle);
    if (!file) {
        fprintf(stderr, "[RUNTIME ERROR] file_seek: Invalid file handle %ld\n", handle);
        return 1;
    }

    // Convert whence: 0=SEEK_SET, 1=SEEK_CUR, 2=SEEK_END
    int c_whence = SEEK_SET;
    if (whence == 1) c_whence = SEEK_CUR;
    else if (whence == 2) c_whence = SEEK_END;

    return fseek(file, offset, c_whence) == 0 ? 0 : 1;
}

// Get current file position
int64_t runtime_file_tell(int64_t handle) {
    FILE* file = get_file_from_handle(handle);
    if (!file) {
        fprintf(stderr, "[RUNTIME ERROR] file_tell: Invalid file handle %ld\n", handle);
        return -1;
    }

    long pos = ftell(file);
    return pos < 0 ? -1 : (int64_t)pos;
}

// Check if at end of file
int64_t runtime_file_eof(int64_t handle) {
    FILE* file = get_file_from_handle(handle);
    if (!file) {
        fprintf(stderr, "[RUNTIME ERROR] file_eof: Invalid file handle %ld\n", handle);
        return 1; // Treat invalid handle as EOF
    }

    return feof(file) ? 1 : 0;
}