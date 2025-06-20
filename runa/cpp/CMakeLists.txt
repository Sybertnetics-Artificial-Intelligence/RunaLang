cmake_minimum_required(VERSION 3.15)
project(runa_vm LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(runa_vm STATIC vm.cpp)
add_executable(runa_vm_test test_vm.cpp)
target_link_libraries(runa_vm_test PRIVATE runa_vm) 