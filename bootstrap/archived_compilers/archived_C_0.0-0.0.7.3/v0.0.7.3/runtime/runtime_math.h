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
#ifndef RUNTIME_MATH_H
#define RUNTIME_MATH_H

#include <stdint.h>

// Math runtime functions for Runa v0.0.7.2
// All functions work with int64_t for consistency with Runa's integer type system
// Floating point operations are converted to/from fixed point representation

// Trigonometric functions (input in degrees, output in fixed point)
int64_t runtime_sin(int64_t degrees);
int64_t runtime_cos(int64_t degrees);
int64_t runtime_tan(int64_t degrees);

// Mathematical functions
int64_t runtime_sqrt(int64_t n);
int64_t runtime_pow(int64_t base, int64_t exponent);
int64_t runtime_abs(int64_t n);
int64_t runtime_floor(int64_t n);
int64_t runtime_ceil(int64_t n);
int64_t runtime_min(int64_t a, int64_t b);
int64_t runtime_max(int64_t a, int64_t b);
int64_t runtime_random(void);  // Returns random number 0 to RAND_MAX
int64_t runtime_log(int64_t n);  // Natural logarithm
int64_t runtime_exp(int64_t n);  // e^n

#endif // RUNTIME_MATH_H