#ifndef HASHTABLE_H
#define HASHTABLE_H

#include <stdint.h>
#include <stdbool.h>

// Forward declaration for function pointer types
typedef struct HashEntry HashEntry;
typedef struct HashTable HashTable;

// Function pointer types for hash table operations
typedef uint32_t (*HashFunction)(const void* key);
typedef bool (*CompareFunction)(const void* key1, const void* key2);
typedef void (*FreeKeyFunction)(void* key);
typedef void (*FreeValueFunction)(void* value);

// Hash table entry (linked list for collision resolution)
struct HashEntry {
    void* key;
    void* value;
    HashEntry* next;
};

// Hash table structure
struct HashTable {
    HashEntry** buckets;       // Array of bucket pointers
    size_t bucket_count;        // Number of buckets
    size_t entry_count;         // Number of entries
    HashFunction hash_func;     // Hash function
    CompareFunction compare_func; // Key comparison function
    FreeKeyFunction free_key;   // Optional key destructor
    FreeValueFunction free_value; // Optional value destructor
};

// Hash table creation and destruction
HashTable* hashtable_create(size_t initial_buckets,
                            HashFunction hash_func,
                            CompareFunction compare_func);
HashTable* hashtable_create_with_destructors(size_t initial_buckets,
                                            HashFunction hash_func,
                                            CompareFunction compare_func,
                                            FreeKeyFunction free_key,
                                            FreeValueFunction free_value);
void hashtable_destroy(HashTable* table);

// Basic operations
bool hashtable_put(HashTable* table, void* key, void* value);
void* hashtable_get(HashTable* table, const void* key);
bool hashtable_remove(HashTable* table, const void* key);
bool hashtable_contains(HashTable* table, const void* key);
size_t hashtable_size(HashTable* table);
void hashtable_clear(HashTable* table);

// Iteration support
typedef struct HashIterator {
    HashTable* table;
    size_t bucket_index;
    HashEntry* current_entry;
} HashIterator;

HashIterator* hashtable_iterator_create(HashTable* table);
bool hashtable_iterator_has_next(HashIterator* iter);
void hashtable_iterator_next(HashIterator* iter, void** key, void** value);
void hashtable_iterator_destroy(HashIterator* iter);

// Utility functions for common key types
uint32_t hash_string(const void* key);
bool compare_strings(const void* key1, const void* key2);
uint32_t hash_integer(const void* key);
bool compare_integers(const void* key1, const void* key2);
uint32_t hash_pointer(const void* key);
bool compare_pointers(const void* key1, const void* key2);

// Statistics and debugging
typedef struct HashTableStats {
    size_t bucket_count;
    size_t entry_count;
    size_t empty_buckets;
    size_t max_chain_length;
    double average_chain_length;
    double load_factor;
} HashTableStats;

HashTableStats hashtable_get_stats(HashTable* table);
void hashtable_print_stats(HashTable* table);

#endif // HASHTABLE_H