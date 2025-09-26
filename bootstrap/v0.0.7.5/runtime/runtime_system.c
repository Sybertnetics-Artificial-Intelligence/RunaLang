#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <errno.h>
#include <limits.h>
#include "runtime_string.h"  // For string_substring

// Internal print functions for runtime errors
static void runtime_print_string(const char* str) {
    if (str) {
        size_t len = strlen(str);
        write(STDERR_FILENO, str, len);
    }
}

static void runtime_print_integer(long value) {
    char buffer[32];
    sprintf(buffer, "%ld", value);
    runtime_print_string(buffer);
}

//=============================================================================
// COMMAND LINE ARGUMENTS
//=============================================================================

// Global storage for command line arguments (set by main)
static int global_argc = 0;
static char **global_argv = NULL;

void runtime_set_command_line_args(int argc, char **argv) {
    global_argc = argc;
    global_argv = argv;
}

// Returns the number of command line arguments
long get_command_line_args_count(void) {
    return (long)global_argc;
}

// Returns the command line argument at the specified index
// Returns NULL if index is out of bounds
char* get_command_line_arg(long index) {
    if (index < 0 || index >= global_argc || !global_argv) {
        return NULL;
    }

    // Return a copy of the argument to prevent modification of original
    char* arg = global_argv[index];
    if (!arg) return NULL;

    size_t len = strlen(arg);
    char* result = malloc(len + 1);
    if (!result) {
        runtime_print_string("PANIC: Failed to allocate memory for command line argument\n");
        exit(1);
    }

    strcpy(result, arg);
    return result;
}

//=============================================================================
// EXIT CONTROL
//=============================================================================

// Exit the program with the specified code
void exit_with_code(long code) {
    exit((int)code);
}

//=============================================================================
// ERROR HANDLING
//=============================================================================

// Print error message and terminate program
void panic(const char* message) {
    if (message) {
        runtime_print_string("PANIC: ");
        runtime_print_string(message);
        runtime_print_string("\n");
    } else {
        runtime_print_string("PANIC: Unknown error occurred\n");
    }
    exit(1);
}

// Assert that a condition is true, otherwise panic with message
void assert(long condition, const char* message) {
    if (!condition) {
        if (message) {
            runtime_print_string("ASSERTION FAILED: ");
            runtime_print_string(message);
            runtime_print_string("\n");
        } else {
            runtime_print_string("ASSERTION FAILED\n");
        }
        exit(1);
    }
}

//=============================================================================
// MEMORY MANAGEMENT
//=============================================================================

// Simple wrapper around malloc for explicit memory allocation
void* allocate(long size) {
    if (size <= 0) {
        runtime_print_string("ERROR: Invalid allocation size: ");
        runtime_print_integer(size);
        runtime_print_string("\n");
        return NULL;
    }

    void* ptr = malloc((size_t)size);
    if (!ptr) {
        runtime_print_string("ERROR: Failed to allocate ");
        runtime_print_integer(size);
        runtime_print_string(" bytes of memory\n");
        return NULL;
    }

    // Initialize to zero for safety
    memset(ptr, 0, (size_t)size);
    return ptr;
}

// Simple wrapper around free for explicit memory deallocation
void deallocate(void* ptr) {
    if (ptr) {
        free(ptr);
    }
}

//=============================================================================
// ENHANCED MEMORY ALLOCATION WITH SAFETY CHECKS
//=============================================================================

// Allocate memory with overflow protection
void* safe_allocate(long count, long size) {
    if (count <= 0 || size <= 0) {
        runtime_print_string("ERROR: Invalid allocation parameters\n");
        return NULL;
    }

    // Check for multiplication overflow
    if (count > LONG_MAX / size) {
        runtime_print_string("ERROR: Allocation size would overflow\n");
        return NULL;
    }

    long total_size = count * size;
    return allocate(total_size);
}

// Reallocate memory safely
void* reallocate(void* ptr, long new_size) {
    if (new_size <= 0) {
        deallocate(ptr);
        return NULL;
    }

    void* new_ptr = realloc(ptr, (size_t)new_size);
    if (!new_ptr) {
        runtime_print_string("ERROR: Failed to reallocate memory to ");
        runtime_print_integer(new_size);
        runtime_print_string(" bytes\n");
        return NULL;
    }

    return new_ptr;
}

//=============================================================================
// MEMORY DEBUGGING SUPPORT
//=============================================================================

#ifdef DEBUG_MEMORY
static long total_allocated = 0;
static long allocation_count = 0;

void* debug_allocate(long size, const char* file, int line) {
    void* ptr = allocate(size);
    if (ptr) {
        total_allocated += size;
        allocation_count++;
        printf("[MEMORY] Allocated %ld bytes at %p (%s:%d) - Total: %ld bytes, Count: %ld\n",
               size, ptr, file, line, total_allocated, allocation_count);
    }
    return ptr;
}

void debug_deallocate(void* ptr, const char* file, int line) {
    if (ptr) {
        allocation_count--;
        printf("[MEMORY] Deallocated %p (%s:%d) - Count: %ld\n",
               ptr, file, line, allocation_count);
    }
    deallocate(ptr);
}

long get_total_allocated(void) {
    return total_allocated;
}

long get_allocation_count(void) {
    return allocation_count;
}

#define allocate(size) debug_allocate(size, __FILE__, __LINE__)
#define deallocate(ptr) debug_deallocate(ptr, __FILE__, __LINE__)
#endif

//=============================================================================
// LOW-LEVEL MEMORY OPERATIONS
//=============================================================================

long memory_get_byte(void* ptr, long offset) {
    unsigned char* byte_ptr = (unsigned char*)ptr + offset;
    return (long)*byte_ptr;
}

long memory_set_byte(void* ptr, long offset, long value) {
    unsigned char* byte_ptr = (unsigned char*)ptr + offset;
    *byte_ptr = (unsigned char)(value & 0xFF);
    return 0;
}

// 32-bit integer access functions for struct fields
long memory_get_integer(void* ptr, long offset) {
    int* int_ptr = (int*)((char*)ptr + offset);
    return (long)*int_ptr;
}

long memory_set_integer(void* ptr, long offset, long value) {
    int* int_ptr = (int*)((char*)ptr + offset);
    *int_ptr = (int)value;
    return 0;
}

long memory_get_pointer(void* ptr, long offset) {
    void** ptr_ptr = (void**)((char*)ptr + offset);
    return (long)*ptr_ptr;
}

long memory_set_pointer(void* ptr, long offset, long value) {
    void** ptr_ptr = (void**)((char*)ptr + offset);
    *ptr_ptr = (void*)value;
    return 0;
}

// System call wrapper for Runa
long system_call(long syscall_num, long arg1, long arg2, long arg3) {
    long result;
    __asm__ volatile (
        "movq %1, %%rax\n"
        "movq %2, %%rdi\n"
        "movq %3, %%rsi\n"
        "movq %4, %%rdx\n"
        "syscall\n"
        "movq %%rax, %0"
        : "=r" (result)
        : "r" (syscall_num), "r" (arg1), "r" (arg2), "r" (arg3)
        : "rax", "rdi", "rsi", "rdx", "rcx", "r11", "memory"
    );
    return result;
}

// String conversion helpers for Runa
char* memory_pointer_to_string(long ptr) {
    // Cast long pointer value to char pointer
    return (char*)ptr;
}

char* memory_get_substring(long ptr, long offset, long length) {
    // Get substring using runtime string_substring function
    char* str = (char*)ptr;
    return string_substring(str, offset, length);
}

//=============================================================================
// SYSTEM INFORMATION
//=============================================================================

// Get the process ID
long get_process_id(void) {
    return (long)getpid();
}

// Get the parent process ID
long get_parent_process_id(void) {
    return (long)getppid();
}

//=============================================================================
// ENVIRONMENT VARIABLES
//=============================================================================

// Get environment variable value
char* get_environment_variable(const char* name) {
    if (!name) {
        return NULL;
    }

    char* value = getenv(name);
    if (!value) {
        return NULL;
    }

    // Return a copy to prevent modification of environment
    size_t len = strlen(value);
    char* result = malloc(len + 1);
    if (!result) {
        panic("Failed to allocate memory for environment variable");
        return NULL;
    }

    strcpy(result, value);
    return result;
}

// Set environment variable
long set_environment_variable(const char* name, const char* value) {
    if (!name) {
        return 0;
    }

    int result;
    if (value) {
        result = setenv(name, value, 1);
    } else {
        result = unsetenv(name);
    }

    return (result == 0) ? 1 : 0;
}