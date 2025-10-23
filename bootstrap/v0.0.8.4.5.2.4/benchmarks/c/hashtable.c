#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE_SIZE 1000

typedef struct {
    int key;
    int value;
    int occupied;
} HashEntry;

int hash(int key) {
    return key % TABLE_SIZE;
}

void ht_insert(HashEntry* table, int key, int value) {
    int index = hash(key);
    table[index].key = key;
    table[index].value = value;
    table[index].occupied = 1;
}

int ht_lookup(HashEntry* table, int key) {
    int index = hash(key);
    if (table[index].occupied && table[index].key == key) {
        return table[index].value;
    }
    return 0;
}

int main() {
    HashEntry* table = (HashEntry*)calloc(TABLE_SIZE, sizeof(HashEntry));

    // Insert 10000 key-value pairs
    for (int i = 0; i < 10000; i++) {
        ht_insert(table, i, i * 2);
    }

    // Lookup 10000 values
    int total = 0;
    for (int i = 0; i < 10000; i++) {
        int value = ht_lookup(table, i);
        total += value;
    }

    free(table);
    return 0;
}
