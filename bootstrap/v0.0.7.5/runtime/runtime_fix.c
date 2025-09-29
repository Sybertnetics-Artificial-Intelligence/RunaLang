#include <stdint.h>
#include <string.h>

// Original functions (with wrong arg order due to v0.0.7.3 bug)
void memory_set_byte_orig(int64_t value, int64_t offset, char* ptr);

// Fixed wrapper
void memory_set_byte(char* ptr, int64_t offset, int64_t value) {
    // Just set it directly - bypass the broken original
    ptr[offset] = (char)value;
}

// Fixed memory_copy_string_to_buffer
void memory_copy_string_to_buffer(char* dest, char* src) {
    if (!dest || !src) return;
    strcpy(dest, src);
}
