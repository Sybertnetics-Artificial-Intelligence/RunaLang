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
#define _GNU_SOURCE  // For strdup
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "runtime_string.h"

int64_t string_length(const char* s) {
    if (!s) {
        return 0;
    }
    return (int64_t)strlen(s);
}

char string_char_at(const char* s, int64_t index) {
    if (!s || index < 0) {
        return '\0';
    }

    size_t len = strlen(s);
    if (index >= (int64_t)len) {
        return '\0';
    }

    return s[index];
}

char* string_substring(const char* s, int64_t start, int64_t length) {
    if (!s || start < 0 || length < 0) {
        return NULL;
    }

    size_t str_len = strlen(s);

    // Check bounds
    if (start >= (int64_t)str_len) {
        // Return empty string
        char* result = malloc(1);
        result[0] = '\0';
        return result;
    }

    // Adjust length if it goes beyond string end
    if (start + length > (int64_t)str_len) {
        length = (int64_t)str_len - start;
    }

    char* result = malloc(length + 1);
    strncpy(result, s + start, length);
    result[length] = '\0';

    return result;
}

int64_t string_equals(const char* s1, const char* s2) {
    if (!s1 || !s2) {
        return (s1 == s2) ? 1 : 0;  // Both null is equal
    }

    return (strcmp(s1, s2) == 0) ? 1 : 0;
}

int64_t ascii_value_of(const char* c) {
    if (!c || c[0] == '\0') {
        return 0;
    }

    return (int64_t)c[0];
}

int64_t is_digit(const char* c) {
    if (!c || c[0] == '\0') {
        return 0;
    }

    return isdigit(c[0]) ? 1 : 0;
}

int64_t is_alpha(const char* c) {
    if (!c || c[0] == '\0') {
        return 0;
    }

    return isalpha(c[0]) ? 1 : 0;
}

int64_t is_whitespace(const char* c) {
    if (!c || c[0] == '\0') {
        return 0;
    }

    return isspace(c[0]) ? 1 : 0;
}

// Concatenate two strings (returns newly allocated string)
char* string_concat(const char* s1, const char* s2) {
    if (!s1 && !s2) return NULL;
    if (!s1) return strdup(s2);
    if (!s2) return strdup(s1);

    size_t len1 = strlen(s1);
    size_t len2 = strlen(s2);
    char* result = malloc(len1 + len2 + 1);

    strcpy(result, s1);
    strcat(result, s2);

    return result;
}

// Compare two strings lexicographically
// Returns: < 0 if s1 < s2, 0 if equal, > 0 if s1 > s2
int64_t string_compare(const char* s1, const char* s2) {
    if (!s1 && !s2) return 0;
    if (!s1) return -1;
    if (!s2) return 1;

    return strcmp(s1, s2);
}

// Convert string to integer
int64_t string_to_integer(const char* s) {
    if (!s || !*s) return 0;

    char* endptr;
    long long result = strtoll(s, &endptr, 10);

    // If conversion failed, return 0
    if (endptr == s) return 0;

    return (int64_t)result;
}

// Convert integer to string (returns newly allocated string)
char* integer_to_string(int64_t value) {
    // Maximum int64_t is 19 digits + sign + null terminator
    char buffer[32];
    snprintf(buffer, sizeof(buffer), "%lld", (long long)value);
    return strdup(buffer);
}

// Find substring in string (returns index or -1 if not found)
int64_t string_find(const char* haystack, const char* needle) {
    if (!haystack || !needle) return -1;
    if (!*needle) return 0; // Empty needle is always found at position 0

    const char* result = strstr(haystack, needle);
    if (!result) return -1;

    return (int64_t)(result - haystack);
}

// Replace all occurrences of old_substr with new_substr
char* string_replace(const char* str, const char* old_substr, const char* new_substr) {
    if (!str || !old_substr || !new_substr) return NULL;
    if (!*old_substr) return strdup(str); // Can't replace empty string

    // Count occurrences
    int count = 0;
    const char* pos = str;
    size_t old_len = strlen(old_substr);
    size_t new_len = strlen(new_substr);

    while ((pos = strstr(pos, old_substr)) != NULL) {
        count++;
        pos += old_len;
    }

    if (count == 0) return strdup(str); // Nothing to replace

    // Calculate new string length
    size_t str_len = strlen(str);
    size_t result_len = str_len + (new_len - old_len) * count;
    char* result = malloc(result_len + 1);

    // Perform replacement
    const char* src = str;
    char* dst = result;

    while (*src) {
        if (strncmp(src, old_substr, old_len) == 0) {
            strcpy(dst, new_substr);
            dst += new_len;
            src += old_len;
        } else {
            *dst++ = *src++;
        }
    }
    *dst = '\0';

    return result;
}

// Trim whitespace from both ends of string
char* string_trim(const char* s) {
    if (!s) return NULL;

    // Find first non-whitespace character
    while (*s && isspace(*s)) s++;

    if (!*s) {
        // All whitespace
        char* result = malloc(1);
        result[0] = '\0';
        return result;
    }

    // Find last non-whitespace character
    const char* end = s + strlen(s) - 1;
    while (end > s && isspace(*end)) end--;

    // Copy trimmed string
    size_t len = end - s + 1;
    char* result = malloc(len + 1);
    strncpy(result, s, len);
    result[len] = '\0';

    return result;
}

// Split string by delimiter (returns list)
// Returns a list structure that can be handled by the list runtime
void* string_split(const char* s, const char* delimiter) {
    if (!s || !delimiter) return NULL;

    // Create a list using the list_create function from list runtime
    extern void* list_create(void);
    extern void list_append(void* list, void* item);

    void* result_list = list_create();

    if (!*delimiter) {
        // Empty delimiter - return list with single item
        list_append(result_list, strdup(s));
        return result_list;
    }

    char* str_copy = strdup(s);
    char* token = strtok(str_copy, delimiter);

    while (token != NULL) {
        list_append(result_list, strdup(token));
        token = strtok(NULL, delimiter);
    }

    free(str_copy);
    return result_list;
}