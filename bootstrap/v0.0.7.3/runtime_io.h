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

// Enhanced file I/O operations for v0.0.7.2

// Open file with mode ("r", "w", "a") and return handle
// Returns file handle (>=0) on success, -1 on error
int64_t runtime_file_open(const char* filename, const char* mode);

// Close file handle
// Returns 0 on success, 1 on error
int64_t runtime_file_close(int64_t handle);

// Read a line from file
// Returns allocated string (caller must free) or NULL on EOF/error
char* runtime_file_read_line(int64_t handle);

// Write a line to file (adds newline)
// Returns 0 on success, 1 on error
int64_t runtime_file_write_line(int64_t handle, const char* line);

// Check if file exists
// Returns 1 if exists, 0 if not
int64_t runtime_file_exists(const char* filename);

// Delete a file
// Returns 0 on success, 1 on error
int64_t runtime_file_delete(const char* filename);

// Get file size (alias for runtime_get_file_size)
// Returns size in bytes or -1 on error
int64_t runtime_file_size(const char* filename);

// Set file position
// whence: 0=beginning, 1=current, 2=end
// Returns 0 on success, 1 on error
int64_t runtime_file_seek(int64_t handle, int64_t offset, int64_t whence);

// Get current file position
// Returns position or -1 on error
int64_t runtime_file_tell(int64_t handle);

// Check if at end of file
// Returns 1 if EOF, 0 if not
int64_t runtime_file_eof(int64_t handle);

#endif // RUNTIME_IO_H