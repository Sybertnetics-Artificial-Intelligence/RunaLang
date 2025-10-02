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
#include "runtime_list.h"

#define INITIAL_CAPACITY 8

// Internal list structure
struct List {
    int64_t* data;
    size_t capacity;
    size_t length;
};

// Create a new empty list
List* list_create(void) {
    List* list = (List*)malloc(sizeof(List));
    if (!list) {
        fprintf(stderr, "Runtime error: Failed to allocate memory for list\n");
        exit(1);
    }

    list->data = (int64_t*)malloc(INITIAL_CAPACITY * sizeof(int64_t));
    if (!list->data) {
        fprintf(stderr, "Runtime error: Failed to allocate memory for list data\n");
        free(list);
        exit(1);
    }

    list->capacity = INITIAL_CAPACITY;
    list->length = 0;

    return list;
}

// Append a value to the end of the list
void list_append(List* list, int64_t value) {
    if (!list) {
        fprintf(stderr, "Runtime error: Cannot append to null list\n");
        exit(1);
    }

    // Grow capacity if needed
    if (list->length >= list->capacity) {
        size_t new_capacity = list->capacity * 2;
        int64_t* new_data = (int64_t*)realloc(list->data, new_capacity * sizeof(int64_t));
        if (!new_data) {
            fprintf(stderr, "Runtime error: Failed to grow list capacity\n");
            exit(1);
        }
        list->data = new_data;
        list->capacity = new_capacity;
    }

    list->data[list->length] = value;
    list->length++;
}

// Get a value at the specified index
int64_t list_get(List* list, int64_t index) {
    if (!list) {
        fprintf(stderr, "Runtime error: Cannot get from null list\n");
        exit(1);
    }

    if (index < 0 || (size_t)index >= list->length) {
        fprintf(stderr, "Runtime error: List index out of bounds: %ld (list length: %zu)\n",
                index, list->length);
        exit(1);
    }

    return list->data[index];
}

// Alias for list_get (for compatibility with spec)
int64_t list_get_integer(List* list, int64_t index) {
    return list_get(list, index);
}

// Get the length of the list
size_t list_length(List* list) {
    if (!list) {
        return 0;
    }
    return list->length;
}

// Destroy a list and free its memory
void list_destroy(List* list) {
    if (list) {
        if (list->data) {
            free(list->data);
        }
        free(list);
    }
}