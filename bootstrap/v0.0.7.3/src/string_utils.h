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
#ifndef STRING_UTILS_H
#define STRING_UTILS_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

// String builder for efficient string concatenation
typedef struct StringBuilder {
    char* buffer;
    size_t capacity;
    size_t length;
} StringBuilder;

// String builder operations
StringBuilder* string_builder_create(void);
StringBuilder* string_builder_create_with_capacity(size_t initial_capacity);
void string_builder_destroy(StringBuilder* sb);

bool string_builder_append(StringBuilder* sb, const char* str);
bool string_builder_append_char(StringBuilder* sb, char c);
bool string_builder_append_int(StringBuilder* sb, int64_t value);
bool string_builder_append_format(StringBuilder* sb, const char* format, ...);

char* string_builder_to_string(StringBuilder* sb);  // Transfers ownership
char* string_builder_get_string(StringBuilder* sb);  // Returns internal buffer (don't free)
size_t string_builder_length(StringBuilder* sb);
void string_builder_clear(StringBuilder* sb);

// String tokenization
typedef struct StringTokenizer {
    char* string;          // Copy of the string being tokenized
    char* current;         // Current position in string
    const char* delimiters;  // Delimiter characters
    bool own_string;       // Whether we own the string
} StringTokenizer;

StringTokenizer* string_tokenizer_create(const char* str, const char* delimiters);
char* string_tokenizer_next(StringTokenizer* tokenizer);
bool string_tokenizer_has_next(StringTokenizer* tokenizer);
void string_tokenizer_destroy(StringTokenizer* tokenizer);

// String split (returns array of strings)
typedef struct StringArray {
    char** strings;
    size_t count;
    size_t capacity;
} StringArray;

StringArray* string_util_split(const char* str, const char* delimiter);
StringArray* string_split_char(const char* str, char delimiter);
StringArray* string_split_whitespace(const char* str);
void string_array_destroy(StringArray* array);

// String utilities
char* string_duplicate(const char* str);
char* string_duplicate_n(const char* str, size_t n);
char* string_join(const char** strings, size_t count, const char* separator);
char* string_join_array(StringArray* array, const char* separator);

bool string_starts_with(const char* str, const char* prefix);
bool string_ends_with(const char* str, const char* suffix);
bool string_contains(const char* str, const char* substring);

char* string_util_trim(const char* str);
char* string_trim_left(const char* str);
char* string_trim_right(const char* str);

char* string_to_upper(const char* str);
char* string_to_lower(const char* str);

char* string_replace_char(const char* str, char old_char, char new_char);
char* string_replace_all(const char* str, const char* old_str, const char* new_str);

int64_t string_count_occurrences(const char* str, const char* substring);
int64_t string_index_of(const char* str, const char* substring);
int64_t string_last_index_of(const char* str, const char* substring);

// String formatting
char* string_format(const char* format, ...);
char* string_format_int(int64_t value);
char* string_format_hex(int64_t value);
char* string_format_binary(int64_t value);

// String validation
bool string_is_empty(const char* str);
bool string_is_whitespace(const char* str);
bool string_is_numeric(const char* str);
bool string_is_alpha(const char* str);
bool string_is_alphanumeric(const char* str);
bool string_is_identifier(const char* str);  // Valid C identifier

// String comparison
int string_compare_ignore_case(const char* str1, const char* str2);
bool string_equals_ignore_case(const char* str1, const char* str2);

// Memory-safe string operations
size_t string_copy_safe(char* dest, size_t dest_size, const char* src);
size_t string_concat_safe(char* dest, size_t dest_size, const char* src);

// Escape sequences
char* string_escape(const char* str);    // Add escape sequences
char* string_unescape(const char* str);  // Remove escape sequences

#endif // STRING_UTILS_H