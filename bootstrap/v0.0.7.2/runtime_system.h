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
#ifndef RUNTIME_SYSTEM_H
#define RUNTIME_SYSTEM_H

#include <stddef.h>

//=============================================================================
// COMMAND LINE ARGUMENTS
//=============================================================================

// Initialize command line arguments storage (called by main)
void runtime_set_command_line_args(int argc, char **argv);

// Get count of command line arguments
long get_command_line_args_count(void);

// Get command line argument at specified index
char* get_command_line_arg(long index);

//=============================================================================
// EXIT CONTROL
//=============================================================================

// Exit program with specified code
void exit_with_code(long code);

//=============================================================================
// ERROR HANDLING
//=============================================================================

// Print error message and terminate program
void panic(const char* message);

// Assert condition is true, otherwise panic
void assert(long condition, const char* message);

//=============================================================================
// MEMORY MANAGEMENT
//=============================================================================

// Allocate memory
void* allocate(long size);

// Deallocate memory
void deallocate(void* ptr);

// Safe allocation with overflow protection
void* safe_allocate(long count, long size);

// Reallocate memory
void* reallocate(void* ptr, long new_size);

//=============================================================================
// MEMORY DEBUGGING (only available in debug builds)
//=============================================================================

#ifdef DEBUG_MEMORY
void* debug_allocate(long size, const char* file, int line);
void debug_deallocate(void* ptr, const char* file, int line);
long get_total_allocated(void);
long get_allocation_count(void);
#endif

//=============================================================================
// SYSTEM INFORMATION
//=============================================================================

// Get current process ID
long get_process_id(void);

// Get parent process ID
long get_parent_process_id(void);

//=============================================================================
// ENVIRONMENT VARIABLES
//=============================================================================

// Get environment variable value
char* get_environment_variable(const char* name);

// Set environment variable
long set_environment_variable(const char* name, const char* value);

#endif