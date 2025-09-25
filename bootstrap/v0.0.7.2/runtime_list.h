#ifndef RUNTIME_LIST_H
#define RUNTIME_LIST_H

#include <stddef.h>
#include <stdint.h>

// Opaque list structure - implementation hidden from Runa code
typedef struct List List;

// Runtime list management functions
List* list_create(void);
void list_append(List* list, int64_t value);
int64_t list_get(List* list, int64_t index);
int64_t list_get_integer(List* list, int64_t index);  // Alias for list_get
size_t list_length(List* list);
void list_destroy(List* list);

// Enhanced list operations for v0.0.7.2
void list_set(List* list, int64_t index, int64_t value);
void list_insert(List* list, int64_t index, int64_t value);
int64_t list_remove(List* list, int64_t index);
void list_clear(List* list);
int64_t list_find(List* list, int64_t value);
void list_sort(List* list);
void list_reverse(List* list);
List* list_copy(List* list);
List* list_merge(List* list1, List* list2);

#endif // RUNTIME_LIST_H