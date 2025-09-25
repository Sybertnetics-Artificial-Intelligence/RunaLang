#ifndef CONTAINERS_H
#define CONTAINERS_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

// Generic dynamic array (vector) container
typedef struct Vector {
    void** items;           // Array of pointers to items
    size_t capacity;        // Allocated capacity
    size_t size;           // Current number of items
    void (*free_item)(void*); // Optional destructor for items
} Vector;

// Vector operations
Vector* vector_create(void);
Vector* vector_create_with_capacity(size_t initial_capacity);
Vector* vector_create_with_destructor(void (*free_item)(void*));
void vector_destroy(Vector* vec);

bool vector_push(Vector* vec, void* item);
void* vector_pop(Vector* vec);
void* vector_get(Vector* vec, size_t index);
bool vector_set(Vector* vec, size_t index, void* item);
bool vector_insert(Vector* vec, size_t index, void* item);
bool vector_remove(Vector* vec, size_t index);
void vector_clear(Vector* vec);

size_t vector_size(Vector* vec);
size_t vector_capacity(Vector* vec);
bool vector_is_empty(Vector* vec);
bool vector_reserve(Vector* vec, size_t new_capacity);
bool vector_shrink_to_fit(Vector* vec);

// Vector iteration
void** vector_begin(Vector* vec);
void** vector_end(Vector* vec);
void vector_foreach(Vector* vec, void (*callback)(void* item));

// Generic stack container (based on vector)
typedef struct Stack {
    Vector* vec;
} Stack;

// Stack operations
Stack* stack_create(void);
Stack* stack_create_with_destructor(void (*free_item)(void*));
void stack_destroy(Stack* stack);

bool stack_push(Stack* stack, void* item);
void* stack_pop(Stack* stack);
void* stack_peek(Stack* stack);
size_t stack_size(Stack* stack);
bool stack_is_empty(Stack* stack);
void stack_clear(Stack* stack);

// Generic queue container (circular buffer implementation)
typedef struct Queue {
    void** items;           // Array of pointers to items
    size_t capacity;        // Allocated capacity
    size_t front;          // Index of front element
    size_t rear;           // Index where next element will be inserted
    size_t size;           // Current number of items
    void (*free_item)(void*); // Optional destructor for items
} Queue;

// Queue operations
Queue* queue_create(void);
Queue* queue_create_with_capacity(size_t initial_capacity);
Queue* queue_create_with_destructor(void (*free_item)(void*));
void queue_destroy(Queue* queue);

bool queue_enqueue(Queue* queue, void* item);
void* queue_dequeue(Queue* queue);
void* queue_peek(Queue* queue);
size_t queue_size(Queue* queue);
bool queue_is_empty(Queue* queue);
bool queue_is_full(Queue* queue);
void queue_clear(Queue* queue);

// Generic linked list container
typedef struct ListNode {
    void* data;
    struct ListNode* next;
    struct ListNode* prev;
} ListNode;

typedef struct LinkedList {
    ListNode* head;
    ListNode* tail;
    size_t size;
    void (*free_item)(void*); // Optional destructor for items
} LinkedList;

// Linked list operations
LinkedList* container_list_create(void);
LinkedList* list_create_with_destructor(void (*free_item)(void*));
void container_list_destroy(LinkedList* list);

bool list_push_front(LinkedList* list, void* item);
bool list_push_back(LinkedList* list, void* item);
void* list_pop_front(LinkedList* list);
void* list_pop_back(LinkedList* list);
void* list_front(LinkedList* list);
void* list_back(LinkedList* list);

bool list_insert_after(LinkedList* list, ListNode* node, void* item);
bool list_insert_before(LinkedList* list, ListNode* node, void* item);
bool list_remove_node(LinkedList* list, ListNode* node);

ListNode* container_list_find(LinkedList* list, void* item, bool (*compare)(void*, void*));
size_t list_size(LinkedList* list);
bool list_is_empty(LinkedList* list);
void container_list_clear(LinkedList* list);

// List iteration
ListNode* list_begin(LinkedList* list);
ListNode* list_end(LinkedList* list);
ListNode* list_next(ListNode* node);
ListNode* list_prev(ListNode* node);
void list_foreach(LinkedList* list, void (*callback)(void* item));

// Generic set container (based on hash table)
typedef struct Set {
    struct HashTable* table;  // Uses hash table for implementation
    void (*free_item)(void*);
} Set;

// Set operations
Set* set_create(uint32_t (*hash_func)(const void*),
                bool (*compare_func)(const void*, const void*));
Set* set_create_with_destructor(uint32_t (*hash_func)(const void*),
                                bool (*compare_func)(const void*, const void*),
                                void (*free_item)(void*));
void set_destroy(Set* set);

bool set_add(Set* set, void* item);
bool set_remove(Set* set, void* item);
bool set_contains(Set* set, void* item);
size_t set_size(Set* set);
bool set_is_empty(Set* set);
void set_clear(Set* set);

// Set operations
Set* set_union(Set* set1, Set* set2);
Set* set_intersection(Set* set1, Set* set2);
Set* set_difference(Set* set1, Set* set2);
bool set_is_subset(Set* set1, Set* set2);
bool set_is_equal(Set* set1, Set* set2);

// Utility functions for common item types
void free_string_item(void* item);
void free_integer_item(void* item);

#endif // CONTAINERS_H