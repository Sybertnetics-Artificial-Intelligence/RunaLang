#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "containers.h"
#include "hashtable.h"

// Macro to suppress unused parameter warnings
#define UNUSED(x) ((void)(x))

// ==== Vector Implementation ====

Vector* vector_create(void) {
    return vector_create_with_capacity(16);
}

Vector* vector_create_with_capacity(size_t initial_capacity) {
    Vector* vec = malloc(sizeof(Vector));
    if (!vec) return NULL;

    vec->items = malloc(sizeof(void*) * initial_capacity);
    if (!vec->items) {
        free(vec);
        return NULL;
    }

    vec->capacity = initial_capacity;
    vec->size = 0;
    vec->free_item = NULL;
    return vec;
}

Vector* vector_create_with_destructor(void (*free_item)(void*)) {
    Vector* vec = vector_create();
    if (vec) {
        vec->free_item = free_item;
    }
    return vec;
}

void vector_destroy(Vector* vec) {
    if (!vec) return;

    if (vec->free_item) {
        for (size_t i = 0; i < vec->size; i++) {
            if (vec->items[i]) {
                vec->free_item(vec->items[i]);
            }
        }
    }

    free(vec->items);
    free(vec);
}

bool vector_push(Vector* vec, void* item) {
    if (!vec) return false;

    if (vec->size >= vec->capacity) {
        size_t new_capacity = vec->capacity * 2;
        void** new_items = realloc(vec->items, sizeof(void*) * new_capacity);
        if (!new_items) return false;

        vec->items = new_items;
        vec->capacity = new_capacity;
    }

    vec->items[vec->size++] = item;
    return true;
}

void* vector_pop(Vector* vec) {
    if (!vec || vec->size == 0) return NULL;

    return vec->items[--vec->size];
}

void* vector_get(Vector* vec, size_t index) {
    if (!vec || index >= vec->size) return NULL;

    return vec->items[index];
}

bool vector_set(Vector* vec, size_t index, void* item) {
    if (!vec || index >= vec->size) return false;

    if (vec->free_item && vec->items[index]) {
        vec->free_item(vec->items[index]);
    }

    vec->items[index] = item;
    return true;
}

bool vector_insert(Vector* vec, size_t index, void* item) {
    if (!vec || index > vec->size) return false;

    if (vec->size >= vec->capacity) {
        size_t new_capacity = vec->capacity * 2;
        void** new_items = realloc(vec->items, sizeof(void*) * new_capacity);
        if (!new_items) return false;

        vec->items = new_items;
        vec->capacity = new_capacity;
    }

    // Shift elements to the right
    for (size_t i = vec->size; i > index; i--) {
        vec->items[i] = vec->items[i - 1];
    }

    vec->items[index] = item;
    vec->size++;
    return true;
}

bool vector_remove(Vector* vec, size_t index) {
    if (!vec || index >= vec->size) return false;

    if (vec->free_item && vec->items[index]) {
        vec->free_item(vec->items[index]);
    }

    // Shift elements to the left
    for (size_t i = index; i < vec->size - 1; i++) {
        vec->items[i] = vec->items[i + 1];
    }

    vec->size--;
    return true;
}

void vector_clear(Vector* vec) {
    if (!vec) return;

    if (vec->free_item) {
        for (size_t i = 0; i < vec->size; i++) {
            if (vec->items[i]) {
                vec->free_item(vec->items[i]);
            }
        }
    }

    vec->size = 0;
}

size_t vector_size(Vector* vec) {
    return vec ? vec->size : 0;
}

size_t vector_capacity(Vector* vec) {
    return vec ? vec->capacity : 0;
}

bool vector_is_empty(Vector* vec) {
    return !vec || vec->size == 0;
}

bool vector_reserve(Vector* vec, size_t new_capacity) {
    if (!vec || new_capacity <= vec->capacity) return false;

    void** new_items = realloc(vec->items, sizeof(void*) * new_capacity);
    if (!new_items) return false;

    vec->items = new_items;
    vec->capacity = new_capacity;
    return true;
}

bool vector_shrink_to_fit(Vector* vec) {
    if (!vec || vec->size == vec->capacity) return true;

    void** new_items = realloc(vec->items, sizeof(void*) * vec->size);
    if (!new_items && vec->size > 0) return false;

    vec->items = new_items;
    vec->capacity = vec->size;
    return true;
}

void** vector_begin(Vector* vec) {
    return vec ? vec->items : NULL;
}

void** vector_end(Vector* vec) {
    return vec ? vec->items + vec->size : NULL;
}

void vector_foreach(Vector* vec, void (*callback)(void* item)) {
    if (!vec || !callback) return;

    for (size_t i = 0; i < vec->size; i++) {
        callback(vec->items[i]);
    }
}

// ==== Stack Implementation ====

Stack* stack_create(void) {
    Stack* stack = malloc(sizeof(Stack));
    if (!stack) return NULL;

    stack->vec = vector_create();
    if (!stack->vec) {
        free(stack);
        return NULL;
    }

    return stack;
}

Stack* stack_create_with_destructor(void (*free_item)(void*)) {
    Stack* stack = malloc(sizeof(Stack));
    if (!stack) return NULL;

    stack->vec = vector_create_with_destructor(free_item);
    if (!stack->vec) {
        free(stack);
        return NULL;
    }

    return stack;
}

void stack_destroy(Stack* stack) {
    if (!stack) return;

    vector_destroy(stack->vec);
    free(stack);
}

bool stack_push(Stack* stack, void* item) {
    return stack ? vector_push(stack->vec, item) : false;
}

void* stack_pop(Stack* stack) {
    return stack ? vector_pop(stack->vec) : NULL;
}

void* stack_peek(Stack* stack) {
    if (!stack || vector_is_empty(stack->vec)) return NULL;

    return vector_get(stack->vec, stack->vec->size - 1);
}

size_t stack_size(Stack* stack) {
    return stack ? vector_size(stack->vec) : 0;
}

bool stack_is_empty(Stack* stack) {
    return !stack || vector_is_empty(stack->vec);
}

void stack_clear(Stack* stack) {
    if (stack) {
        vector_clear(stack->vec);
    }
}

// ==== Queue Implementation ====

Queue* queue_create(void) {
    return queue_create_with_capacity(16);
}

Queue* queue_create_with_capacity(size_t initial_capacity) {
    Queue* queue = malloc(sizeof(Queue));
    if (!queue) return NULL;

    queue->items = malloc(sizeof(void*) * initial_capacity);
    if (!queue->items) {
        free(queue);
        return NULL;
    }

    queue->capacity = initial_capacity;
    queue->front = 0;
    queue->rear = 0;
    queue->size = 0;
    queue->free_item = NULL;
    return queue;
}

Queue* queue_create_with_destructor(void (*free_item)(void*)) {
    Queue* queue = queue_create();
    if (queue) {
        queue->free_item = free_item;
    }
    return queue;
}

void queue_destroy(Queue* queue) {
    if (!queue) return;

    queue_clear(queue);
    free(queue->items);
    free(queue);
}

bool queue_enqueue(Queue* queue, void* item) {
    if (!queue || queue->size >= queue->capacity) return false;

    queue->items[queue->rear] = item;
    queue->rear = (queue->rear + 1) % queue->capacity;
    queue->size++;
    return true;
}

void* queue_dequeue(Queue* queue) {
    if (!queue || queue->size == 0) return NULL;

    void* item = queue->items[queue->front];
    queue->front = (queue->front + 1) % queue->capacity;
    queue->size--;
    return item;
}

void* queue_peek(Queue* queue) {
    if (!queue || queue->size == 0) return NULL;

    return queue->items[queue->front];
}

size_t queue_size(Queue* queue) {
    return queue ? queue->size : 0;
}

bool queue_is_empty(Queue* queue) {
    return !queue || queue->size == 0;
}

bool queue_is_full(Queue* queue) {
    return queue && queue->size >= queue->capacity;
}

void queue_clear(Queue* queue) {
    if (!queue) return;

    if (queue->free_item) {
        while (queue->size > 0) {
            void* item = queue_dequeue(queue);
            if (item) {
                queue->free_item(item);
            }
        }
    } else {
        queue->size = 0;
        queue->front = 0;
        queue->rear = 0;
    }
}

// ==== Linked List Implementation ====

LinkedList* container_list_create(void) {
    LinkedList* list = malloc(sizeof(LinkedList));
    if (!list) return NULL;

    list->head = NULL;
    list->tail = NULL;
    list->size = 0;
    list->free_item = NULL;
    return list;
}

LinkedList* list_create_with_destructor(void (*free_item)(void*)) {
    LinkedList* list = container_list_create();
    if (list) {
        list->free_item = free_item;
    }
    return list;
}

void container_list_destroy(LinkedList* list) {
    if (!list) return;

    container_list_clear(list);
    free(list);
}

bool list_push_front(LinkedList* list, void* item) {
    if (!list) return false;

    ListNode* new_node = malloc(sizeof(ListNode));
    if (!new_node) return false;

    new_node->data = item;
    new_node->prev = NULL;
    new_node->next = list->head;

    if (list->head) {
        list->head->prev = new_node;
    } else {
        list->tail = new_node;
    }

    list->head = new_node;
    list->size++;
    return true;
}

bool list_push_back(LinkedList* list, void* item) {
    if (!list) return false;

    ListNode* new_node = malloc(sizeof(ListNode));
    if (!new_node) return false;

    new_node->data = item;
    new_node->next = NULL;
    new_node->prev = list->tail;

    if (list->tail) {
        list->tail->next = new_node;
    } else {
        list->head = new_node;
    }

    list->tail = new_node;
    list->size++;
    return true;
}

void* list_pop_front(LinkedList* list) {
    if (!list || !list->head) return NULL;

    ListNode* node = list->head;
    void* data = node->data;

    list->head = node->next;
    if (list->head) {
        list->head->prev = NULL;
    } else {
        list->tail = NULL;
    }

    free(node);
    list->size--;
    return data;
}

void* list_pop_back(LinkedList* list) {
    if (!list || !list->tail) return NULL;

    ListNode* node = list->tail;
    void* data = node->data;

    list->tail = node->prev;
    if (list->tail) {
        list->tail->next = NULL;
    } else {
        list->head = NULL;
    }

    free(node);
    list->size--;
    return data;
}

void* list_front(LinkedList* list) {
    return (list && list->head) ? list->head->data : NULL;
}

void* list_back(LinkedList* list) {
    return (list && list->tail) ? list->tail->data : NULL;
}

bool list_insert_after(LinkedList* list, ListNode* node, void* item) {
    if (!list || !node) return false;

    ListNode* new_node = malloc(sizeof(ListNode));
    if (!new_node) return false;

    new_node->data = item;
    new_node->prev = node;
    new_node->next = node->next;

    if (node->next) {
        node->next->prev = new_node;
    } else {
        list->tail = new_node;
    }

    node->next = new_node;
    list->size++;
    return true;
}

bool list_insert_before(LinkedList* list, ListNode* node, void* item) {
    if (!list || !node) return false;

    ListNode* new_node = malloc(sizeof(ListNode));
    if (!new_node) return false;

    new_node->data = item;
    new_node->next = node;
    new_node->prev = node->prev;

    if (node->prev) {
        node->prev->next = new_node;
    } else {
        list->head = new_node;
    }

    node->prev = new_node;
    list->size++;
    return true;
}

bool list_remove_node(LinkedList* list, ListNode* node) {
    if (!list || !node) return false;

    if (node->prev) {
        node->prev->next = node->next;
    } else {
        list->head = node->next;
    }

    if (node->next) {
        node->next->prev = node->prev;
    } else {
        list->tail = node->prev;
    }

    if (list->free_item && node->data) {
        list->free_item(node->data);
    }

    free(node);
    list->size--;
    return true;
}

ListNode* container_list_find(LinkedList* list, void* item, bool (*compare)(void*, void*)) {
    if (!list || !compare) return NULL;

    ListNode* current = list->head;
    while (current) {
        if (compare(current->data, item)) {
            return current;
        }
        current = current->next;
    }

    return NULL;
}

size_t list_size(LinkedList* list) {
    return list ? list->size : 0;
}

bool list_is_empty(LinkedList* list) {
    return !list || list->size == 0;
}

void container_list_clear(LinkedList* list) {
    if (!list) return;

    ListNode* current = list->head;
    while (current) {
        ListNode* next = current->next;

        if (list->free_item && current->data) {
            list->free_item(current->data);
        }

        free(current);
        current = next;
    }

    list->head = NULL;
    list->tail = NULL;
    list->size = 0;
}

ListNode* list_begin(LinkedList* list) {
    return list ? list->head : NULL;
}

ListNode* list_end(LinkedList* list) {
    UNUSED(list);
    return NULL;  // End is represented as NULL
}

ListNode* list_next(ListNode* node) {
    return node ? node->next : NULL;
}

ListNode* list_prev(ListNode* node) {
    return node ? node->prev : NULL;
}

void list_foreach(LinkedList* list, void (*callback)(void* item)) {
    if (!list || !callback) return;

    ListNode* current = list->head;
    while (current) {
        callback(current->data);
        current = current->next;
    }
}

// ==== Set Implementation ====

Set* set_create(uint32_t (*hash_func)(const void*),
                bool (*compare_func)(const void*, const void*)) {
    Set* set = malloc(sizeof(Set));
    if (!set) return NULL;

    set->table = hashtable_create(256, hash_func, compare_func);
    if (!set->table) {
        free(set);
        return NULL;
    }

    set->free_item = NULL;
    return set;
}

Set* set_create_with_destructor(uint32_t (*hash_func)(const void*),
                                bool (*compare_func)(const void*, const void*),
                                void (*free_item)(void*)) {
    Set* set = set_create(hash_func, compare_func);
    if (set) {
        set->free_item = free_item;
        // Update hash table to use destructor
        set->table->free_key = free_item;
    }
    return set;
}

void set_destroy(Set* set) {
    if (!set) return;

    hashtable_destroy(set->table);
    free(set);
}

bool set_add(Set* set, void* item) {
    if (!set) return false;

    // In a set, key and value are the same (we only care about keys)
    return hashtable_put(set->table, item, item);
}

bool set_remove(Set* set, void* item) {
    return set ? hashtable_remove(set->table, item) : false;
}

bool set_contains(Set* set, void* item) {
    return set ? hashtable_contains(set->table, item) : false;
}

size_t set_size(Set* set) {
    return set ? hashtable_size(set->table) : 0;
}

bool set_is_empty(Set* set) {
    return !set || hashtable_size(set->table) == 0;
}

void set_clear(Set* set) {
    if (set) {
        hashtable_clear(set->table);
    }
}

Set* set_union(Set* set1, Set* set2) {
    if (!set1 || !set2) return NULL;

    Set* result = set_create(set1->table->hash_func, set1->table->compare_func);
    if (!result) return NULL;

    // Add all elements from set1
    HashIterator* iter = hashtable_iterator_create(set1->table);
    while (hashtable_iterator_has_next(iter)) {
        void* key = NULL;
        hashtable_iterator_next(iter, &key, NULL);
        set_add(result, key);
    }
    hashtable_iterator_destroy(iter);

    // Add all elements from set2
    iter = hashtable_iterator_create(set2->table);
    while (hashtable_iterator_has_next(iter)) {
        void* key = NULL;
        hashtable_iterator_next(iter, &key, NULL);
        set_add(result, key);
    }
    hashtable_iterator_destroy(iter);

    return result;
}

Set* set_intersection(Set* set1, Set* set2) {
    if (!set1 || !set2) return NULL;

    Set* result = set_create(set1->table->hash_func, set1->table->compare_func);
    if (!result) return NULL;

    // Add elements that are in both sets
    HashIterator* iter = hashtable_iterator_create(set1->table);
    while (hashtable_iterator_has_next(iter)) {
        void* key = NULL;
        hashtable_iterator_next(iter, &key, NULL);
        if (set_contains(set2, key)) {
            set_add(result, key);
        }
    }
    hashtable_iterator_destroy(iter);

    return result;
}

Set* set_difference(Set* set1, Set* set2) {
    if (!set1 || !set2) return NULL;

    Set* result = set_create(set1->table->hash_func, set1->table->compare_func);
    if (!result) return NULL;

    // Add elements that are in set1 but not in set2
    HashIterator* iter = hashtable_iterator_create(set1->table);
    while (hashtable_iterator_has_next(iter)) {
        void* key = NULL;
        hashtable_iterator_next(iter, &key, NULL);
        if (!set_contains(set2, key)) {
            set_add(result, key);
        }
    }
    hashtable_iterator_destroy(iter);

    return result;
}

bool set_is_subset(Set* set1, Set* set2) {
    if (!set1 || !set2) return false;

    // Check if all elements of set1 are in set2
    HashIterator* iter = hashtable_iterator_create(set1->table);
    while (hashtable_iterator_has_next(iter)) {
        void* key = NULL;
        hashtable_iterator_next(iter, &key, NULL);
        if (!set_contains(set2, key)) {
            hashtable_iterator_destroy(iter);
            return false;
        }
    }
    hashtable_iterator_destroy(iter);

    return true;
}

bool set_is_equal(Set* set1, Set* set2) {
    if (!set1 || !set2) return false;

    if (set_size(set1) != set_size(set2)) return false;

    return set_is_subset(set1, set2);
}

// ==== Utility Functions ====

void free_string_item(void* item) {
    free(item);
}

void free_integer_item(void* item) {
    free(item);
}