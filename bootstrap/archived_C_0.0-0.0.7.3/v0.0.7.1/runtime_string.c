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