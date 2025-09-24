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

#endif // RUNTIME_LIST_H