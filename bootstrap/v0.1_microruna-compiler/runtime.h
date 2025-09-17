#ifndef RUNA_RUNTIME_H
#define RUNA_RUNTIME_H

// String operations
char* concat(const char* str1, const char* str2);
int length_of(const char* str);
int char_at(const char* str, int index);
char* substring(const char* str, int start, int end);
char* to_string(int value);

// I/O operations
char* read_file(const char* filename);
int write_file(const char* filename, const char* content);

// Display functions
void runa_display_string(const char* str);
void runa_display_int(int value);

// Memory management
void runa_free_string(char* str);

// Conversion functions
int string_to_integer(const char* str);

#endif // RUNA_RUNTIME_H