#ifndef RUNA_RUNTIME_H
#define RUNA_RUNTIME_H

// Runa v0.1 Runtime Library
// Provides essential string and I/O functions for MicroRuna self-hosted compiler

// String operations - CRITICAL PRIORITY
char* concat(const char* str1, const char* str2);
long length_of(const char* str);
char* substring(const char* str, long start, long length);
long char_at(const char* str, long index);

// Type conversion - SECONDARY PRIORITY
char* to_string(long value);

// File I/O operations - MINIMAL PRIORITY
char* read_file(const char* filename);
long write_file(const char* filename, const char* content);

// Memory management
void runa_free(void* ptr);

#endif // RUNA_RUNTIME_H