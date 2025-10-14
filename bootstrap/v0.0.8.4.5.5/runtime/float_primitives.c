/*
 * Float Primitives for Runa v0.0.8.4.5.5
 *
 * These are the foundation primitives that enable float arithmetic.
 * They use inline assembly (SSE2 for Float32/Float64, x87 for Float80).
 *
 * v0.0.8.5 will rewrite these to use pure Runa float operations.
 */

#include <stdint.h>

// ============================================================================
// Float64 Operations (SSE2 - addsd, subsd, mulsd, divsd)
// ============================================================================

void float_add(void* a_ptr, void* b_ptr, void* result_ptr) {
    // Add two Float64 values using SSE2
    __asm__ volatile (
        "movsd (%0), %%xmm0\n\t"      // Load a into xmm0
        "movsd (%1), %%xmm1\n\t"      // Load b into xmm1
        "addsd %%xmm1, %%xmm0\n\t"    // xmm0 = xmm0 + xmm1
        "movsd %%xmm0, (%2)\n\t"      // Store result
        :
        : "r"(a_ptr), "r"(b_ptr), "r"(result_ptr)
        : "%xmm0", "%xmm1", "memory"
    );
}

void float_subtract(void* a_ptr, void* b_ptr, void* result_ptr) {
    // Subtract two Float64 values using SSE2
    __asm__ volatile (
        "movsd (%0), %%xmm0\n\t"      // Load a into xmm0
        "movsd (%1), %%xmm1\n\t"      // Load b into xmm1
        "subsd %%xmm1, %%xmm0\n\t"    // xmm0 = xmm0 - xmm1
        "movsd %%xmm0, (%2)\n\t"      // Store result
        :
        : "r"(a_ptr), "r"(b_ptr), "r"(result_ptr)
        : "%xmm0", "%xmm1", "memory"
    );
}

void float_multiply(void* a_ptr, void* b_ptr, void* result_ptr) {
    // Multiply two Float64 values using SSE2
    __asm__ volatile (
        "movsd (%0), %%xmm0\n\t"      // Load a into xmm0
        "movsd (%1), %%xmm1\n\t"      // Load b into xmm1
        "mulsd %%xmm1, %%xmm0\n\t"    // xmm0 = xmm0 * xmm1
        "movsd %%xmm0, (%2)\n\t"      // Store result
        :
        : "r"(a_ptr), "r"(b_ptr), "r"(result_ptr)
        : "%xmm0", "%xmm1", "memory"
    );
}

void float_divide(void* a_ptr, void* b_ptr, void* result_ptr) {
    // Divide two Float64 values using SSE2
    __asm__ volatile (
        "movsd (%0), %%xmm0\n\t"      // Load a into xmm0
        "movsd (%1), %%xmm1\n\t"      // Load b into xmm1
        "divsd %%xmm1, %%xmm0\n\t"    // xmm0 = xmm0 / xmm1
        "movsd %%xmm0, (%2)\n\t"      // Store result
        :
        : "r"(a_ptr), "r"(b_ptr), "r"(result_ptr)
        : "%xmm0", "%xmm1", "memory"
    );
}

// ============================================================================
// Float32 Operations (SSE2 - addss, subss, mulss, divss)
// ============================================================================

void float32_add(void* a_ptr, void* b_ptr, void* result_ptr) {
    __asm__ volatile (
        "movss (%0), %%xmm0\n\t"
        "movss (%1), %%xmm1\n\t"
        "addss %%xmm1, %%xmm0\n\t"
        "movss %%xmm0, (%2)\n\t"
        :
        : "r"(a_ptr), "r"(b_ptr), "r"(result_ptr)
        : "%xmm0", "%xmm1", "memory"
    );
}

void float32_subtract(void* a_ptr, void* b_ptr, void* result_ptr) {
    __asm__ volatile (
        "movss (%0), %%xmm0\n\t"
        "movss (%1), %%xmm1\n\t"
        "subss %%xmm1, %%xmm0\n\t"
        "movss %%xmm0, (%2)\n\t"
        :
        : "r"(a_ptr), "r"(b_ptr), "r"(result_ptr)
        : "%xmm0", "%xmm1", "memory"
    );
}

void float32_multiply(void* a_ptr, void* b_ptr, void* result_ptr) {
    __asm__ volatile (
        "movss (%0), %%xmm0\n\t"
        "movss (%1), %%xmm1\n\t"
        "mulss %%xmm1, %%xmm0\n\t"
        "movss %%xmm0, (%2)\n\t"
        :
        : "r"(a_ptr), "r"(b_ptr), "r"(result_ptr)
        : "%xmm0", "%xmm1", "memory"
    );
}

void float32_divide(void* a_ptr, void* b_ptr, void* result_ptr) {
    __asm__ volatile (
        "movss (%0), %%xmm0\n\t"
        "movss (%1), %%xmm1\n\t"
        "divss %%xmm1, %%xmm0\n\t"
        "movss %%xmm0, (%2)\n\t"
        :
        : "r"(a_ptr), "r"(b_ptr), "r"(result_ptr)
        : "%xmm0", "%xmm1", "memory"
    );
}

// ============================================================================
// Float80 Operations (x87 FPU - fadd, fsub, fmul, fdiv)
// ============================================================================

void float80_add(void* a_ptr, void* b_ptr, void* result_ptr) {
    __asm__ volatile (
        "fldt (%0)\n\t"               // Load a (80-bit) onto FPU stack
        "fldt (%1)\n\t"               // Load b (80-bit) onto FPU stack
        "faddp\n\t"                   // Pop and add: ST(1) = ST(0) + ST(1), pop
        "fstpt (%2)\n\t"              // Store result (80-bit) and pop
        :
        : "r"(a_ptr), "r"(b_ptr), "r"(result_ptr)
        : "memory"
    );
}

void float80_subtract(void* a_ptr, void* b_ptr, void* result_ptr) {
    __asm__ volatile (
        "fldt (%0)\n\t"
        "fldt (%1)\n\t"
        "fsubp\n\t"
        "fstpt (%2)\n\t"
        :
        : "r"(a_ptr), "r"(b_ptr), "r"(result_ptr)
        : "memory"
    );
}

void float80_multiply(void* a_ptr, void* b_ptr, void* result_ptr) {
    __asm__ volatile (
        "fldt (%0)\n\t"
        "fldt (%1)\n\t"
        "fmulp\n\t"
        "fstpt (%2)\n\t"
        :
        : "r"(a_ptr), "r"(b_ptr), "r"(result_ptr)
        : "memory"
    );
}

void float80_divide(void* a_ptr, void* b_ptr, void* result_ptr) {
    __asm__ volatile (
        "fldt (%0)\n\t"
        "fldt (%1)\n\t"
        "fdivp\n\t"
        "fstpt (%2)\n\t"
        :
        : "r"(a_ptr), "r"(b_ptr), "r"(result_ptr)
        : "memory"
    );
}

// ============================================================================
// String to Float Conversion
// ============================================================================

#include <stdlib.h>

void string_to_float(const char* str, void* result_ptr) {
    // Convert string to Float64 using strtod
    double value = strtod(str, NULL);
    *(double*)result_ptr = value;
}

void print_newline(void) {
    // Print newline character
    const char newline = '\n';
    __asm__ volatile (
        "movq $1, %%rdi\n\t"       // fd = stdout
        "movq %0, %%rsi\n\t"        // buffer = &newline
        "movq $1, %%rdx\n\t"        // count = 1
        "movq $1, %%rax\n\t"        // syscall number for write
        "syscall\n\t"
        :
        : "r"(&newline)
        : "%rax", "%rdi", "%rsi", "%rdx"
    );
}
