#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hashtable.h"

// Create a new hash table
HashTable* hashtable_create(size_t initial_buckets,
                            HashFunction hash_func,
                            CompareFunction compare_func) {
    return hashtable_create_with_destructors(initial_buckets, hash_func, compare_func, NULL, NULL);
}

// Create a new hash table with custom destructors
HashTable* hashtable_create_with_destructors(size_t initial_buckets,
                                            HashFunction hash_func,
                                            CompareFunction compare_func,
                                            FreeKeyFunction free_key,
                                            FreeValueFunction free_value) {
    if (initial_buckets == 0 || !hash_func || !compare_func) {
        return NULL;
    }

    HashTable* table = malloc(sizeof(HashTable));
    if (!table) {
        return NULL;
    }

    table->buckets = calloc(initial_buckets, sizeof(HashEntry*));
    if (!table->buckets) {
        free(table);
        return NULL;
    }

    table->bucket_count = initial_buckets;
    table->entry_count = 0;
    table->hash_func = hash_func;
    table->compare_func = compare_func;
    table->free_key = free_key;
    table->free_value = free_value;

    return table;
}

// Destroy a hash table and free all resources
void hashtable_destroy(HashTable* table) {
    if (!table) {
        return;
    }

    // Clear all entries
    hashtable_clear(table);

    // Free the buckets array
    free(table->buckets);

    // Free the table itself
    free(table);
}

// Put a key-value pair into the hash table
bool hashtable_put(HashTable* table, void* key, void* value) {
    if (!table || !key) {
        return false;
    }

    uint32_t hash = table->hash_func(key);
    size_t bucket_index = hash % table->bucket_count;

    HashEntry* current = table->buckets[bucket_index];
    HashEntry* prev = NULL;

    // Search for existing key
    while (current) {
        if (table->compare_func(current->key, key)) {
            // Key exists, update value
            if (table->free_value && current->value) {
                table->free_value(current->value);
            }
            current->value = value;
            return true;
        }
        prev = current;
        current = current->next;
    }

    // Key doesn't exist, create new entry
    HashEntry* new_entry = malloc(sizeof(HashEntry));
    if (!new_entry) {
        return false;
    }

    new_entry->key = key;
    new_entry->value = value;
    new_entry->next = NULL;

    if (prev) {
        prev->next = new_entry;
    } else {
        table->buckets[bucket_index] = new_entry;
    }

    table->entry_count++;
    return true;
}

// Get a value by key from the hash table
void* hashtable_get(HashTable* table, const void* key) {
    if (!table || !key) {
        return NULL;
    }

    uint32_t hash = table->hash_func(key);
    size_t bucket_index = hash % table->bucket_count;

    HashEntry* current = table->buckets[bucket_index];
    while (current) {
        if (table->compare_func(current->key, key)) {
            return current->value;
        }
        current = current->next;
    }

    return NULL;
}

// Remove a key-value pair from the hash table
bool hashtable_remove(HashTable* table, const void* key) {
    if (!table || !key) {
        return false;
    }

    uint32_t hash = table->hash_func(key);
    size_t bucket_index = hash % table->bucket_count;

    HashEntry* current = table->buckets[bucket_index];
    HashEntry* prev = NULL;

    while (current) {
        if (table->compare_func(current->key, key)) {
            // Found the entry to remove
            if (prev) {
                prev->next = current->next;
            } else {
                table->buckets[bucket_index] = current->next;
            }

            // Free key and value if destructors are provided
            if (table->free_key && current->key) {
                table->free_key(current->key);
            }
            if (table->free_value && current->value) {
                table->free_value(current->value);
            }

            free(current);
            table->entry_count--;
            return true;
        }
        prev = current;
        current = current->next;
    }

    return false;
}

// Check if a key exists in the hash table
bool hashtable_contains(HashTable* table, const void* key) {
    return hashtable_get(table, key) != NULL;
}

// Get the number of entries in the hash table
size_t hashtable_size(HashTable* table) {
    return table ? table->entry_count : 0;
}

// Clear all entries from the hash table
void hashtable_clear(HashTable* table) {
    if (!table) {
        return;
    }

    for (size_t i = 0; i < table->bucket_count; i++) {
        HashEntry* current = table->buckets[i];
        while (current) {
            HashEntry* next = current->next;

            // Free key and value if destructors are provided
            if (table->free_key && current->key) {
                table->free_key(current->key);
            }
            if (table->free_value && current->value) {
                table->free_value(current->value);
            }

            free(current);
            current = next;
        }
        table->buckets[i] = NULL;
    }

    table->entry_count = 0;
}

// Create an iterator for the hash table
HashIterator* hashtable_iterator_create(HashTable* table) {
    if (!table) {
        return NULL;
    }

    HashIterator* iter = malloc(sizeof(HashIterator));
    if (!iter) {
        return NULL;
    }

    iter->table = table;
    iter->bucket_index = 0;
    iter->current_entry = NULL;

    // Find the first non-empty bucket
    for (size_t i = 0; i < table->bucket_count; i++) {
        if (table->buckets[i]) {
            iter->bucket_index = i;
            iter->current_entry = table->buckets[i];
            break;
        }
    }

    return iter;
}

// Check if iterator has more elements
bool hashtable_iterator_has_next(HashIterator* iter) {
    return iter && iter->current_entry != NULL;
}

// Get the next key-value pair from the iterator
void hashtable_iterator_next(HashIterator* iter, void** key, void** value) {
    if (!iter || !iter->current_entry) {
        if (key) *key = NULL;
        if (value) *value = NULL;
        return;
    }

    // Return current entry's key and value
    if (key) *key = iter->current_entry->key;
    if (value) *value = iter->current_entry->value;

    // Move to next entry
    iter->current_entry = iter->current_entry->next;

    // If no more entries in current bucket, find next non-empty bucket
    if (!iter->current_entry) {
        for (size_t i = iter->bucket_index + 1; i < iter->table->bucket_count; i++) {
            if (iter->table->buckets[i]) {
                iter->bucket_index = i;
                iter->current_entry = iter->table->buckets[i];
                break;
            }
        }
    }
}

// Destroy an iterator
void hashtable_iterator_destroy(HashIterator* iter) {
    free(iter);
}

// Hash function for string keys (djb2 algorithm)
uint32_t hash_string(const void* key) {
    const char* str = (const char*)key;
    uint32_t hash = 5381;
    int c;

    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c; // hash * 33 + c
    }

    return hash;
}

// Compare function for string keys
bool compare_strings(const void* key1, const void* key2) {
    return strcmp((const char*)key1, (const char*)key2) == 0;
}

// Hash function for integer keys
uint32_t hash_integer(const void* key) {
    // Treat the pointer as pointing to an integer
    int64_t value = *(const int64_t*)key;
    // Mix the bits for better distribution
    value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
    value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
    value = value ^ (value >> 31);
    return (uint32_t)value;
}

// Compare function for integer keys
bool compare_integers(const void* key1, const void* key2) {
    return *(const int64_t*)key1 == *(const int64_t*)key2;
}

// Hash function for pointer keys
uint32_t hash_pointer(const void* key) {
    // Hash the pointer value itself
    uintptr_t ptr_value = (uintptr_t)key;
    // Mix bits for better distribution
    ptr_value = ptr_value ^ (ptr_value >> 32);
    ptr_value = ptr_value * 0x9e3779b97f4a7c15ULL;
    return (uint32_t)(ptr_value ^ (ptr_value >> 32));
}

// Compare function for pointer keys
bool compare_pointers(const void* key1, const void* key2) {
    return key1 == key2;
}

// Get statistics about the hash table
HashTableStats hashtable_get_stats(HashTable* table) {
    HashTableStats stats = {0};

    if (!table) {
        return stats;
    }

    stats.bucket_count = table->bucket_count;
    stats.entry_count = table->entry_count;

    size_t total_chain_length = 0;
    stats.max_chain_length = 0;

    for (size_t i = 0; i < table->bucket_count; i++) {
        if (!table->buckets[i]) {
            stats.empty_buckets++;
        } else {
            size_t chain_length = 0;
            HashEntry* current = table->buckets[i];
            while (current) {
                chain_length++;
                current = current->next;
            }
            total_chain_length += chain_length;
            if (chain_length > stats.max_chain_length) {
                stats.max_chain_length = chain_length;
            }
        }
    }

    size_t non_empty_buckets = table->bucket_count - stats.empty_buckets;
    stats.average_chain_length = non_empty_buckets > 0 ?
        (double)total_chain_length / non_empty_buckets : 0.0;
    stats.load_factor = (double)table->entry_count / table->bucket_count;

    return stats;
}

// Print statistics about the hash table
void hashtable_print_stats(HashTable* table) {
    HashTableStats stats = hashtable_get_stats(table);

    printf("Hash Table Statistics:\n");
    printf("  Bucket count: %zu\n", stats.bucket_count);
    printf("  Entry count: %zu\n", stats.entry_count);
    printf("  Empty buckets: %zu (%.1f%%)\n",
           stats.empty_buckets,
           (double)stats.empty_buckets * 100.0 / stats.bucket_count);
    printf("  Max chain length: %zu\n", stats.max_chain_length);
    printf("  Average chain length: %.2f\n", stats.average_chain_length);
    printf("  Load factor: %.2f\n", stats.load_factor);
}