// Compatibility wrapper functions for v0.0.7.3 compiler output
// These bridge the gap between what v0.0.7.3 generates and what our runtime provides

#include <stdint.h>
#include <stddef.h>

// Forward declarations for the real runtime functions
extern int64_t memory_get_integer(void* ptr, int64_t offset);
extern int64_t memory_set_integer(void* ptr, int64_t offset, int64_t value);

// Wrapper functions that v0.0.7.3 expects
int64_t memory_get(void* ptr, int64_t offset) {
    return memory_get_integer(ptr, offset);
}

int64_t memory_set(void* ptr, int64_t offset, int64_t value) {
    return memory_set_integer(ptr, offset, value);
}

// Function pointer call wrapper
int64_t call_function_pointer_2args(void* func, int64_t arg1, int64_t arg2) {
    typedef int64_t (*func_ptr)(int64_t, int64_t);
    if (func) {
        return ((func_ptr)func)(arg1, arg2);
    }
    return 0;
}

// Memory reallocation wrapper
extern void* realloc(void* ptr, size_t size);
void* memory_reallocate(void* ptr, int64_t new_size) {
    return realloc(ptr, (size_t)new_size);
}

// File I/O wrappers for file descriptors directly
#include <unistd.h>
#include <string.h>
#include <fcntl.h>

// Open a file and return file descriptor
int64_t file_open_fd(const char* filename, const char* mode) {
    if (!filename) return -1;

    int flags = 0;
    int perms = 0644;

    if (strcmp(mode, "r") == 0) {
        flags = O_RDONLY;
    } else if (strcmp(mode, "w") == 0) {
        flags = O_WRONLY | O_CREAT | O_TRUNC;
    } else if (strcmp(mode, "a") == 0) {
        flags = O_WRONLY | O_CREAT | O_APPEND;
    } else {
        return -1;
    }

    return open(filename, flags, perms);
}

// Close file descriptor
int64_t file_close_fd(int64_t fd) {
    return close(fd);
}

// Write to file descriptor
int64_t file_write_fd(int64_t fd, const char* str) {
    if (!str) return 0;
    ssize_t len = strlen(str);
    ssize_t written = write(fd, str, len);
    return (written == len) ? 1 : 0;
}