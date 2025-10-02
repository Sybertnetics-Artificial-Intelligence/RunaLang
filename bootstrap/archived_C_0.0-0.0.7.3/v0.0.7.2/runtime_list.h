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