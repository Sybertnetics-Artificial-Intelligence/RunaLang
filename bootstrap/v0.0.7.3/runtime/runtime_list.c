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
        fprintf(stderr, "[RUNTIME ERROR] Failed to allocate memory for list\n");
        exit(1);
    }

    list->data = (int64_t*)malloc(INITIAL_CAPACITY * sizeof(int64_t));
    if (!list->data) {
        fprintf(stderr, "[RUNTIME ERROR] Failed to allocate memory for list data\n");
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
        fprintf(stderr, "[RUNTIME ERROR] Cannot append to null list\n");
        exit(1);
    }

    // Grow capacity if needed
    if (list->length >= list->capacity) {
        size_t new_capacity = list->capacity * 2;
        int64_t* new_data = (int64_t*)realloc(list->data, new_capacity * sizeof(int64_t));
        if (!new_data) {
            fprintf(stderr, "[RUNTIME ERROR] Failed to grow list capacity\n");
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
        fprintf(stderr, "[RUNTIME ERROR] Cannot get from null list\n");
        exit(1);
    }

    if (index < 0 || (size_t)index >= list->length) {
        fprintf(stderr, "[RUNTIME ERROR] List index out of bounds: %ld (list length: %zu)\n",
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

// Set a value at the specified index
void list_set(List* list, int64_t index, int64_t value) {
    if (!list) {
        fprintf(stderr, "[RUNTIME ERROR] Cannot set in null list\n");
        exit(1);
    }

    if (index < 0 || (size_t)index >= list->length) {
        fprintf(stderr, "[RUNTIME ERROR] List index out of bounds: %ld (list length: %zu)\n",
                index, list->length);
        exit(1);
    }

    list->data[index] = value;
}

// Insert a value at the specified index
void list_insert(List* list, int64_t index, int64_t value) {
    if (!list) {
        fprintf(stderr, "[RUNTIME ERROR] Cannot insert into null list\n");
        exit(1);
    }

    // Allow insertion at end (index == length)
    if (index < 0 || (size_t)index > list->length) {
        fprintf(stderr, "[RUNTIME ERROR] List insert index out of bounds: %ld (list length: %zu)\n",
                index, list->length);
        exit(1);
    }

    // Grow capacity if needed
    if (list->length >= list->capacity) {
        size_t new_capacity = list->capacity * 2;
        int64_t* new_data = (int64_t*)realloc(list->data, new_capacity * sizeof(int64_t));
        if (!new_data) {
            fprintf(stderr, "[RUNTIME ERROR] Failed to grow list capacity\n");
            exit(1);
        }
        list->data = new_data;
        list->capacity = new_capacity;
    }

    // Shift elements to make room
    for (size_t i = list->length; i > (size_t)index; i--) {
        list->data[i] = list->data[i - 1];
    }

    list->data[index] = value;
    list->length++;
}

// Remove a value at the specified index and return it
int64_t list_remove(List* list, int64_t index) {
    if (!list) {
        fprintf(stderr, "[RUNTIME ERROR] Cannot remove from null list\n");
        exit(1);
    }

    if (index < 0 || (size_t)index >= list->length) {
        fprintf(stderr, "[RUNTIME ERROR] List index out of bounds: %ld (list length: %zu)\n",
                index, list->length);
        exit(1);
    }

    int64_t value = list->data[index];

    // Shift elements to fill the gap
    for (size_t i = (size_t)index; i < list->length - 1; i++) {
        list->data[i] = list->data[i + 1];
    }

    list->length--;
    return value;
}

// Clear all elements from the list
void list_clear(List* list) {
    if (!list) {
        fprintf(stderr, "[RUNTIME ERROR] Cannot clear null list\n");
        exit(1);
    }

    list->length = 0;
}

// Find the index of the first occurrence of value, or -1 if not found
int64_t list_find(List* list, int64_t value) {
    if (!list) {
        return -1;
    }

    for (size_t i = 0; i < list->length; i++) {
        if (list->data[i] == value) {
            return (int64_t)i;
        }
    }

    return -1;
}

// Sort the list in ascending order using quicksort
static void quicksort(int64_t* arr, int64_t low, int64_t high) {
    if (low < high) {
        // Partition
        int64_t pivot = arr[high];
        int64_t i = low - 1;

        for (int64_t j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                // Swap
                int64_t temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }

        // Place pivot
        int64_t temp = arr[i + 1];
        arr[i + 1] = arr[high];
        arr[high] = temp;

        int64_t pi = i + 1;

        // Recursively sort
        quicksort(arr, low, pi - 1);
        quicksort(arr, pi + 1, high);
    }
}

void list_sort(List* list) {
    if (!list || list->length <= 1) {
        return;
    }

    quicksort(list->data, 0, (int64_t)list->length - 1);
}

// Reverse the order of elements in the list
void list_reverse(List* list) {
    if (!list || list->length <= 1) {
        return;
    }

    size_t left = 0;
    size_t right = list->length - 1;

    while (left < right) {
        // Swap
        int64_t temp = list->data[left];
        list->data[left] = list->data[right];
        list->data[right] = temp;

        left++;
        right--;
    }
}

// Create a deep copy of the list
List* list_copy(List* list) {
    if (!list) {
        return NULL;
    }

    List* copy = list_create();

    // Ensure capacity
    if (list->length > copy->capacity) {
        int64_t* new_data = (int64_t*)realloc(copy->data, list->length * sizeof(int64_t));
        if (!new_data) {
            fprintf(stderr, "[RUNTIME ERROR] Failed to allocate memory for list copy\n");
            list_destroy(copy);
            exit(1);
        }
        copy->data = new_data;
        copy->capacity = list->length;
    }

    // Copy data
    memcpy(copy->data, list->data, list->length * sizeof(int64_t));
    copy->length = list->length;

    return copy;
}

// Merge two lists into a new list
List* list_merge(List* list1, List* list2) {
    if (!list1 && !list2) {
        return list_create();
    }

    if (!list1) {
        return list_copy(list2);
    }

    if (!list2) {
        return list_copy(list1);
    }

    List* merged = list_create();
    size_t total_length = list1->length + list2->length;

    // Ensure capacity
    if (total_length > merged->capacity) {
        int64_t* new_data = (int64_t*)realloc(merged->data, total_length * sizeof(int64_t));
        if (!new_data) {
            fprintf(stderr, "[RUNTIME ERROR] Failed to allocate memory for merged list\n");
            list_destroy(merged);
            exit(1);
        }
        merged->data = new_data;
        merged->capacity = total_length;
    }

    // Copy first list
    memcpy(merged->data, list1->data, list1->length * sizeof(int64_t));

    // Copy second list
    memcpy(merged->data + list1->length, list2->data, list2->length * sizeof(int64_t));

    merged->length = total_length;

    return merged;
}