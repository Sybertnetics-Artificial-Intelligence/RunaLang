# Runa Native VM (C++)

This directory contains the C++ implementation of the Runa Virtual Machine (VM).

## Purpose
- High-performance execution of Runa bytecode
- Native memory management and optimization
- Foundation for JIT compilation and advanced features

## Structure
- `vm.h` / `vm.cpp`: Core VM implementation
- `CMakeLists.txt`: Build configuration
- `tests/`: C++ unit tests for the VM

## Build Instructions

```sh
mkdir build
cd build
cmake ..
make
./runa_vm_test
```

## Requirements
- CMake 3.15+
- C++20 compiler (GCC 10+, Clang 11+, MSVC 2019+)

## Status
- [ ] Skeleton implementation
- [ ] Bytecode execution
- [ ] Memory management
- [ ] JIT compilation 