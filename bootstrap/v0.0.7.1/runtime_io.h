#ifndef RUNTIME_IO_H
#define RUNTIME_IO_H

#include <stdint.h>

// File I/O runtime functions for Runa
// These functions are called from generated assembly code

// Read entire file contents into a string
// Returns pointer to allocated string or NULL on error
char* runtime_read_file(const char* filename);

// Write string content to file
// Returns 0 on success, 1 on error
int64_t runtime_write_file(const char* filename, const char* content);

// Get file size (used internally but exposed for future use)
int64_t runtime_get_file_size(const char* filename);

#endif // RUNTIME_IO_H