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
#ifndef RUNTIME_STRING_H
#define RUNTIME_STRING_H

#include <stdint.h>

// String manipulation runtime functions for Runa v0.0.7.1
// These functions are called from generated assembly code

// Get string length
int64_t string_length(const char* s);

// Get character at position (returns 0 if out of bounds)
char string_char_at(const char* s, int64_t index);

// Extract substring (start is 0-based, returns allocated string)
char* string_substring(const char* s, int64_t start, int64_t length);

// String comparison (returns 1 if equal, 0 if not equal)
int64_t string_equals(const char* s1, const char* s2);

// Get ASCII value of first character in string
int64_t ascii_value_of(const char* c);

// Character classification functions (return 1 if true, 0 if false)
int64_t is_digit(const char* c);
int64_t is_alpha(const char* c);
int64_t is_whitespace(const char* c);

// Additional string manipulation functions for v0.0.7.2

// Concatenate two strings (returns newly allocated string)
char* string_concat(const char* s1, const char* s2);

// Compare two strings lexicographically
// Returns: < 0 if s1 < s2, 0 if equal, > 0 if s1 > s2
int64_t string_compare(const char* s1, const char* s2);

// Convert string to integer
int64_t string_to_integer(const char* s);

// Convert integer to string (returns newly allocated string)
char* integer_to_string(int64_t value);

// Find substring in string (returns index or -1 if not found)
int64_t string_find(const char* haystack, const char* needle);

// Replace all occurrences of old_substr with new_substr
char* string_replace(const char* str, const char* old_substr, const char* new_substr);

// Trim whitespace from both ends of string
char* string_trim(const char* s);

// Split string by delimiter (returns list)
void* string_split(const char* s, const char* delimiter);

#endif // RUNTIME_STRING_H