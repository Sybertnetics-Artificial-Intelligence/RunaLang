#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <ctype.h>
#include "string_utils.h"

// ==== String Builder Implementation ====

StringBuilder* string_builder_create(void) {
    return string_builder_create_with_capacity(256);
}

StringBuilder* string_builder_create_with_capacity(size_t initial_capacity) {
    StringBuilder* sb = malloc(sizeof(StringBuilder));
    if (!sb) return NULL;

    sb->buffer = malloc(initial_capacity);
    if (!sb->buffer) {
        free(sb);
        return NULL;
    }

    sb->buffer[0] = '\0';
    sb->capacity = initial_capacity;
    sb->length = 0;
    return sb;
}

void string_builder_destroy(StringBuilder* sb) {
    if (sb) {
        free(sb->buffer);
        free(sb);
    }
}

static bool string_builder_ensure_capacity(StringBuilder* sb, size_t needed) {
    if (sb->length + needed >= sb->capacity) {
        size_t new_capacity = sb->capacity * 2;
        while (new_capacity < sb->length + needed + 1) {
            new_capacity *= 2;
        }

        char* new_buffer = realloc(sb->buffer, new_capacity);
        if (!new_buffer) return false;

        sb->buffer = new_buffer;
        sb->capacity = new_capacity;
    }
    return true;
}

bool string_builder_append(StringBuilder* sb, const char* str) {
    if (!sb || !str) return false;

    size_t len = strlen(str);
    if (!string_builder_ensure_capacity(sb, len)) return false;

    strcpy(sb->buffer + sb->length, str);
    sb->length += len;
    return true;
}

bool string_builder_append_char(StringBuilder* sb, char c) {
    if (!sb) return false;

    if (!string_builder_ensure_capacity(sb, 1)) return false;

    sb->buffer[sb->length++] = c;
    sb->buffer[sb->length] = '\0';
    return true;
}

bool string_builder_append_int(StringBuilder* sb, int64_t value) {
    char buffer[32];
    snprintf(buffer, sizeof(buffer), "%ld", value);
    return string_builder_append(sb, buffer);
}

bool string_builder_append_format(StringBuilder* sb, const char* format, ...) {
    if (!sb || !format) return false;

    va_list args;
    va_start(args, format);

    // Calculate needed size
    va_list args_copy;
    va_copy(args_copy, args);
    int needed = vsnprintf(NULL, 0, format, args_copy);
    va_end(args_copy);

    if (needed < 0) {
        va_end(args);
        return false;
    }

    if (!string_builder_ensure_capacity(sb, needed)) {
        va_end(args);
        return false;
    }

    vsnprintf(sb->buffer + sb->length, needed + 1, format, args);
    sb->length += needed;

    va_end(args);
    return true;
}

char* string_builder_to_string(StringBuilder* sb) {
    if (!sb) return NULL;

    char* result = sb->buffer;
    sb->buffer = malloc(1);
    sb->buffer[0] = '\0';
    sb->capacity = 1;
    sb->length = 0;

    return result;
}

char* string_builder_get_string(StringBuilder* sb) {
    return sb ? sb->buffer : NULL;
}

size_t string_builder_length(StringBuilder* sb) {
    return sb ? sb->length : 0;
}

void string_builder_clear(StringBuilder* sb) {
    if (sb) {
        sb->buffer[0] = '\0';
        sb->length = 0;
    }
}

// ==== String Tokenizer Implementation ====

StringTokenizer* string_tokenizer_create(const char* str, const char* delimiters) {
    if (!str || !delimiters) return NULL;

    StringTokenizer* tokenizer = malloc(sizeof(StringTokenizer));
    if (!tokenizer) return NULL;

    tokenizer->string = string_duplicate(str);
    if (!tokenizer->string) {
        free(tokenizer);
        return NULL;
    }

    tokenizer->current = tokenizer->string;
    tokenizer->delimiters = delimiters;
    tokenizer->own_string = true;

    return tokenizer;
}

char* string_tokenizer_next(StringTokenizer* tokenizer) {
    if (!tokenizer || !tokenizer->current) return NULL;

    // Skip leading delimiters
    while (*tokenizer->current && strchr(tokenizer->delimiters, *tokenizer->current)) {
        tokenizer->current++;
    }

    if (!*tokenizer->current) {
        tokenizer->current = NULL;
        return NULL;
    }

    char* token_start = tokenizer->current;

    // Find next delimiter
    while (*tokenizer->current && !strchr(tokenizer->delimiters, *tokenizer->current)) {
        tokenizer->current++;
    }

    if (*tokenizer->current) {
        *tokenizer->current = '\0';
        tokenizer->current++;
    }

    return token_start;
}

bool string_tokenizer_has_next(StringTokenizer* tokenizer) {
    if (!tokenizer || !tokenizer->current) return false;

    // Skip delimiters to check if there's a token
    const char* temp = tokenizer->current;
    while (*temp && strchr(tokenizer->delimiters, *temp)) {
        temp++;
    }

    return *temp != '\0';
}

void string_tokenizer_destroy(StringTokenizer* tokenizer) {
    if (tokenizer) {
        if (tokenizer->own_string) {
            free(tokenizer->string);
        }
        free(tokenizer);
    }
}

// ==== String Split Implementation ====

StringArray* string_util_split(const char* str, const char* delimiter) {
    if (!str || !delimiter) return NULL;

    StringArray* array = malloc(sizeof(StringArray));
    if (!array) return NULL;

    array->capacity = 16;
    array->strings = malloc(sizeof(char*) * array->capacity);
    if (!array->strings) {
        free(array);
        return NULL;
    }
    array->count = 0;

    char* temp = string_duplicate(str);
    if (!temp) {
        free(array->strings);
        free(array);
        return NULL;
    }

    char* token = strtok(temp, delimiter);
    while (token) {
        if (array->count >= array->capacity) {
            size_t new_capacity = array->capacity * 2;
            char** new_strings = realloc(array->strings, sizeof(char*) * new_capacity);
            if (!new_strings) {
                // Clean up on failure
                for (size_t i = 0; i < array->count; i++) {
                    free(array->strings[i]);
                }
                free(array->strings);
                free(array);
                free(temp);
                return NULL;
            }
            array->strings = new_strings;
            array->capacity = new_capacity;
        }

        array->strings[array->count] = string_duplicate(token);
        if (!array->strings[array->count]) {
            // Clean up on failure
            for (size_t i = 0; i < array->count; i++) {
                free(array->strings[i]);
            }
            free(array->strings);
            free(array);
            free(temp);
            return NULL;
        }
        array->count++;

        token = strtok(NULL, delimiter);
    }

    free(temp);
    return array;
}

StringArray* string_split_char(const char* str, char delimiter) {
    char delim[2] = {delimiter, '\0'};
    return string_util_split(str, delim);
}

StringArray* string_split_whitespace(const char* str) {
    return string_util_split(str, " \t\n\r\f\v");
}

void string_array_destroy(StringArray* array) {
    if (array) {
        for (size_t i = 0; i < array->count; i++) {
            free(array->strings[i]);
        }
        free(array->strings);
        free(array);
    }
}

// ==== String Utilities ====

char* string_duplicate(const char* str) {
    if (!str) return NULL;

    size_t len = strlen(str);
    char* copy = malloc(len + 1);
    if (!copy) return NULL;

    strcpy(copy, str);
    return copy;
}

char* string_duplicate_n(const char* str, size_t n) {
    if (!str) return NULL;

    char* copy = malloc(n + 1);
    if (!copy) return NULL;

    strncpy(copy, str, n);
    copy[n] = '\0';
    return copy;
}

char* string_join(const char** strings, size_t count, const char* separator) {
    if (!strings || count == 0) return string_duplicate("");

    const char* sep = separator ? separator : "";
    size_t sep_len = strlen(sep);

    // Calculate total length
    size_t total_len = 0;
    for (size_t i = 0; i < count; i++) {
        if (strings[i]) {
            total_len += strlen(strings[i]);
        }
        if (i < count - 1) {
            total_len += sep_len;
        }
    }

    char* result = malloc(total_len + 1);
    if (!result) return NULL;

    char* pos = result;
    for (size_t i = 0; i < count; i++) {
        if (strings[i]) {
            strcpy(pos, strings[i]);
            pos += strlen(strings[i]);
        }
        if (i < count - 1 && sep_len > 0) {
            strcpy(pos, sep);
            pos += sep_len;
        }
    }
    *pos = '\0';

    return result;
}

char* string_join_array(StringArray* array, const char* separator) {
    if (!array) return NULL;
    return string_join((const char**)array->strings, array->count, separator);
}

bool string_starts_with(const char* str, const char* prefix) {
    if (!str || !prefix) return false;
    return strncmp(str, prefix, strlen(prefix)) == 0;
}

bool string_ends_with(const char* str, const char* suffix) {
    if (!str || !suffix) return false;

    size_t str_len = strlen(str);
    size_t suffix_len = strlen(suffix);

    if (suffix_len > str_len) return false;

    return strcmp(str + str_len - suffix_len, suffix) == 0;
}

bool string_contains(const char* str, const char* substring) {
    return str && substring && strstr(str, substring) != NULL;
}

char* string_util_trim(const char* str) {
    if (!str) return NULL;

    // Skip leading whitespace
    while (isspace((unsigned char)*str)) {
        str++;
    }

    if (*str == '\0') {
        return string_duplicate("");
    }

    // Find end
    const char* end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end)) {
        end--;
    }

    size_t len = end - str + 1;
    return string_duplicate_n(str, len);
}

char* string_trim_left(const char* str) {
    if (!str) return NULL;

    while (isspace((unsigned char)*str)) {
        str++;
    }

    return string_duplicate(str);
}

char* string_trim_right(const char* str) {
    if (!str) return NULL;

    size_t len = strlen(str);
    while (len > 0 && isspace((unsigned char)str[len - 1])) {
        len--;
    }

    return string_duplicate_n(str, len);
}

char* string_to_upper(const char* str) {
    if (!str) return NULL;

    char* result = string_duplicate(str);
    if (!result) return NULL;

    for (char* p = result; *p; p++) {
        *p = toupper((unsigned char)*p);
    }

    return result;
}

char* string_to_lower(const char* str) {
    if (!str) return NULL;

    char* result = string_duplicate(str);
    if (!result) return NULL;

    for (char* p = result; *p; p++) {
        *p = tolower((unsigned char)*p);
    }

    return result;
}

char* string_replace_char(const char* str, char old_char, char new_char) {
    if (!str) return NULL;

    char* result = string_duplicate(str);
    if (!result) return NULL;

    for (char* p = result; *p; p++) {
        if (*p == old_char) {
            *p = new_char;
        }
    }

    return result;
}

char* string_replace_all(const char* str, const char* old_str, const char* new_str) {
    if (!str || !old_str || !new_str) return NULL;

    size_t old_len = strlen(old_str);
    if (old_len == 0) return string_duplicate(str);

    size_t new_len = strlen(new_str);

    // Count occurrences
    size_t count = 0;
    const char* pos = str;
    while ((pos = strstr(pos, old_str)) != NULL) {
        count++;
        pos += old_len;
    }

    if (count == 0) return string_duplicate(str);

    // Calculate result length
    size_t str_len = strlen(str);
    size_t result_len = str_len + count * (new_len - old_len);

    char* result = malloc(result_len + 1);
    if (!result) return NULL;

    char* dest = result;
    const char* src = str;

    while ((pos = strstr(src, old_str)) != NULL) {
        size_t prefix_len = pos - src;
        memcpy(dest, src, prefix_len);
        dest += prefix_len;

        memcpy(dest, new_str, new_len);
        dest += new_len;

        src = pos + old_len;
    }

    strcpy(dest, src);

    return result;
}

int64_t string_count_occurrences(const char* str, const char* substring) {
    if (!str || !substring) return 0;

    size_t sub_len = strlen(substring);
    if (sub_len == 0) return 0;

    int64_t count = 0;
    const char* pos = str;

    while ((pos = strstr(pos, substring)) != NULL) {
        count++;
        pos += sub_len;
    }

    return count;
}

int64_t string_index_of(const char* str, const char* substring) {
    if (!str || !substring) return -1;

    const char* pos = strstr(str, substring);
    return pos ? (int64_t)(pos - str) : -1;
}

int64_t string_last_index_of(const char* str, const char* substring) {
    if (!str || !substring) return -1;

    const char* last_pos = NULL;
    const char* pos = str;

    while ((pos = strstr(pos, substring)) != NULL) {
        last_pos = pos;
        pos++;
    }

    return last_pos ? (int64_t)(last_pos - str) : -1;
}

char* string_format(const char* format, ...) {
    if (!format) return NULL;

    va_list args;
    va_start(args, format);

    // Calculate needed size
    va_list args_copy;
    va_copy(args_copy, args);
    int needed = vsnprintf(NULL, 0, format, args_copy);
    va_end(args_copy);

    if (needed < 0) {
        va_end(args);
        return NULL;
    }

    char* result = malloc(needed + 1);
    if (!result) {
        va_end(args);
        return NULL;
    }

    vsnprintf(result, needed + 1, format, args);
    va_end(args);

    return result;
}

char* string_format_int(int64_t value) {
    return string_format("%ld", value);
}

char* string_format_hex(int64_t value) {
    return string_format("0x%lx", value);
}

char* string_format_binary(int64_t value) {
    char buffer[65];  // 64 bits + null terminator
    int pos = 0;

    for (int i = 63; i >= 0; i--) {
        buffer[pos++] = (value & (1LL << i)) ? '1' : '0';
    }
    buffer[pos] = '\0';

    // Remove leading zeros
    const char* start = buffer;
    while (*start == '0' && *(start + 1) != '\0') {
        start++;
    }

    return string_format("0b%s", start);
}

bool string_is_empty(const char* str) {
    return !str || *str == '\0';
}

bool string_is_whitespace(const char* str) {
    if (!str) return true;

    while (*str) {
        if (!isspace((unsigned char)*str)) return false;
        str++;
    }

    return true;
}

bool string_is_numeric(const char* str) {
    if (!str || !*str) return false;

    if (*str == '-' || *str == '+') str++;

    bool has_digit = false;
    while (*str) {
        if (!isdigit((unsigned char)*str)) return false;
        has_digit = true;
        str++;
    }

    return has_digit;
}

bool string_is_alpha(const char* str) {
    if (!str || !*str) return false;

    while (*str) {
        if (!isalpha((unsigned char)*str)) return false;
        str++;
    }

    return true;
}

bool string_is_alphanumeric(const char* str) {
    if (!str || !*str) return false;

    while (*str) {
        if (!isalnum((unsigned char)*str)) return false;
        str++;
    }

    return true;
}

bool string_is_identifier(const char* str) {
    if (!str || !*str) return false;

    // First character must be letter or underscore
    if (!isalpha((unsigned char)*str) && *str != '_') return false;
    str++;

    // Rest can be letters, digits, or underscores
    while (*str) {
        if (!isalnum((unsigned char)*str) && *str != '_') return false;
        str++;
    }

    return true;
}

int string_compare_ignore_case(const char* str1, const char* str2) {
    if (!str1 && !str2) return 0;
    if (!str1) return -1;
    if (!str2) return 1;

    while (*str1 && *str2) {
        int c1 = tolower((unsigned char)*str1);
        int c2 = tolower((unsigned char)*str2);

        if (c1 != c2) return c1 - c2;

        str1++;
        str2++;
    }

    return tolower((unsigned char)*str1) - tolower((unsigned char)*str2);
}

bool string_equals_ignore_case(const char* str1, const char* str2) {
    return string_compare_ignore_case(str1, str2) == 0;
}

size_t string_copy_safe(char* dest, size_t dest_size, const char* src) {
    if (!dest || dest_size == 0 || !src) return 0;

    size_t i;
    for (i = 0; i < dest_size - 1 && src[i] != '\0'; i++) {
        dest[i] = src[i];
    }
    dest[i] = '\0';

    return i;
}

size_t string_concat_safe(char* dest, size_t dest_size, const char* src) {
    if (!dest || dest_size == 0 || !src) return 0;

    size_t dest_len = strlen(dest);
    if (dest_len >= dest_size - 1) return dest_len;

    size_t i;
    for (i = 0; dest_len + i < dest_size - 1 && src[i] != '\0'; i++) {
        dest[dest_len + i] = src[i];
    }
    dest[dest_len + i] = '\0';

    return dest_len + i;
}

char* string_escape(const char* str) {
    if (!str) return NULL;

    // Count characters needed
    size_t len = 0;
    for (const char* p = str; *p; p++) {
        switch (*p) {
            case '\n': case '\t': case '\r': case '\\': case '"':
                len += 2;
                break;
            default:
                len++;
        }
    }

    char* result = malloc(len + 1);
    if (!result) return NULL;

    char* dest = result;
    for (const char* src = str; *src; src++) {
        switch (*src) {
            case '\n': *dest++ = '\\'; *dest++ = 'n'; break;
            case '\t': *dest++ = '\\'; *dest++ = 't'; break;
            case '\r': *dest++ = '\\'; *dest++ = 'r'; break;
            case '\\': *dest++ = '\\'; *dest++ = '\\'; break;
            case '"':  *dest++ = '\\'; *dest++ = '"'; break;
            default:   *dest++ = *src;
        }
    }
    *dest = '\0';

    return result;
}

char* string_unescape(const char* str) {
    if (!str) return NULL;

    size_t len = strlen(str);
    char* result = malloc(len + 1);
    if (!result) return NULL;

    char* dest = result;
    for (const char* src = str; *src; src++) {
        if (*src == '\\' && *(src + 1)) {
            src++;
            switch (*src) {
                case 'n':  *dest++ = '\n'; break;
                case 't':  *dest++ = '\t'; break;
                case 'r':  *dest++ = '\r'; break;
                case '\\': *dest++ = '\\'; break;
                case '"':  *dest++ = '"'; break;
                default:   *dest++ = *src;  // Unknown escape, just copy
            }
        } else {
            *dest++ = *src;
        }
    }
    *dest = '\0';

    return result;
}