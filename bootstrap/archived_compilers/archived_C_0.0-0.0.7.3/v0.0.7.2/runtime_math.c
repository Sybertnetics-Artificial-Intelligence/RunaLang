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
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include "runtime_math.h"

// Fixed point scale factor (1000000 = 6 decimal places)
#define FIXED_POINT_SCALE 1000000
#define PI 3.14159265358979323846

// Convert degrees to radians
static double degrees_to_radians(double degrees) {
    return degrees * (PI / 180.0);
}

// Initialize random seed once
static int random_initialized = 0;
static void init_random() {
    if (!random_initialized) {
        srand((unsigned int)time(NULL));
        random_initialized = 1;
    }
}

// Trigonometric functions
int64_t runtime_sin(int64_t degrees) {
    double radians = degrees_to_radians((double)degrees);
    double result = sin(radians);
    return (int64_t)(result * FIXED_POINT_SCALE);
}

int64_t runtime_cos(int64_t degrees) {
    double radians = degrees_to_radians((double)degrees);
    double result = cos(radians);
    return (int64_t)(result * FIXED_POINT_SCALE);
}

int64_t runtime_tan(int64_t degrees) {
    double radians = degrees_to_radians((double)degrees);
    double result = tan(radians);
    // Clamp to prevent overflow for near-vertical angles
    if (result > 1000000.0) result = 1000000.0;
    if (result < -1000000.0) result = -1000000.0;
    return (int64_t)(result * FIXED_POINT_SCALE);
}

// Square root using Newton's method for integer precision
int64_t runtime_sqrt(int64_t n) {
    if (n < 0) {
        fprintf(stderr, "[RUNTIME ERROR] sqrt: Cannot compute square root of negative number %ld\n", n);
        return 0;
    }

    if (n == 0) return 0;

    // Use floating point for now, with fixed point conversion
    double result = sqrt((double)n);
    return (int64_t)result;
}

// Power function
int64_t runtime_pow(int64_t base, int64_t exponent) {
    if (exponent < 0) {
        // For negative exponents, return 0 (integer division would give 0 anyway)
        return 0;
    }

    int64_t result = 1;
    int64_t abs_exp = exponent;
    int64_t current_base = base;

    // Fast exponentiation by squaring
    while (abs_exp > 0) {
        if (abs_exp & 1) {
            // Check for overflow
            if (result > INT64_MAX / current_base && current_base > 0) {
                fprintf(stderr, "[RUNTIME ERROR] pow: Integer overflow\n");
                return INT64_MAX;
            }
            result *= current_base;
        }
        abs_exp >>= 1;
        if (abs_exp > 0) {
            // Check for overflow
            if (current_base > INT64_MAX / current_base) {
                fprintf(stderr, "[RUNTIME ERROR] pow: Integer overflow\n");
                return INT64_MAX;
            }
            current_base *= current_base;
        }
    }

    return result;
}

// Absolute value
int64_t runtime_abs(int64_t n) {
    if (n == INT64_MIN) {
        // Special case: abs(INT64_MIN) would overflow
        return INT64_MAX;
    }
    return n < 0 ? -n : n;
}

// Floor function (for integers, just returns the value)
int64_t runtime_floor(int64_t n) {
    return n;
}

// Ceil function (for integers, just returns the value)
int64_t runtime_ceil(int64_t n) {
    return n;
}

// Minimum of two values
int64_t runtime_min(int64_t a, int64_t b) {
    return a < b ? a : b;
}

// Maximum of two values
int64_t runtime_max(int64_t a, int64_t b) {
    return a > b ? a : b;
}

// Random number generator
int64_t runtime_random(void) {
    init_random();
    return (int64_t)rand();
}

// Natural logarithm (returns fixed point result)
int64_t runtime_log(int64_t n) {
    if (n <= 0) {
        fprintf(stderr, "[RUNTIME ERROR] log: Cannot compute logarithm of non-positive number %ld\n", n);
        return INT64_MIN;
    }

    double result = log((double)n);
    return (int64_t)(result * FIXED_POINT_SCALE);
}

// Exponential function (e^n)
int64_t runtime_exp(int64_t n) {
    // Limit input to prevent overflow
    double input = (double)n;
    if (input > 20) {
        fprintf(stderr, "[RUNTIME ERROR] exp: Input too large, would cause overflow\n");
        return INT64_MAX;
    }

    double result = exp(input);

    // Check for overflow
    if (result > (double)INT64_MAX) {
        return INT64_MAX;
    }

    return (int64_t)result;
}