cmake_minimum_required(VERSION 3.16)
project(RunaVM VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -O2")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -O0 -DDEBUG")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -DNDEBUG")

# Find Python and pybind11
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# Source files
set(VM_SOURCES
    vm.cpp
)

# Create the VM library
add_library(runa_vm STATIC ${VM_SOURCES})
target_include_directories(runa_vm PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Set library properties
set_target_properties(runa_vm PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
    PUBLIC_HEADER vm.h
)

# Create the Python module
pybind11_add_module(runa_vm_python vm_python.cpp)
target_link_libraries(runa_vm_python PRIVATE runa_vm)

# Create test executable
add_executable(test_vm test_vm.cpp)
target_link_libraries(test_vm runa_vm)

# Create performance benchmark executable
add_executable(benchmark_vm benchmark_vm.cpp)
target_link_libraries(benchmark_vm runa_vm)

# Install targets
install(TARGETS runa_vm
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    PUBLIC_HEADER DESTINATION include/runa
)

install(TARGETS runa_vm_python
    LIBRARY DESTINATION lib/python${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR}/site-packages
)

# Install headers
install(FILES vm.h
    DESTINATION include/runa
)

# Testing
enable_testing()
add_test(NAME VMTest COMMAND test_vm)

# Performance testing
add_custom_target(performance_test
    COMMAND benchmark_vm
    DEPENDS benchmark_vm
    COMMENT "Running VM performance benchmarks"
)

# Documentation
find_package(Doxygen)
if(DOXYGEN_FOUND)
    set(DOXYGEN_IN ${CMAKE_CURRENT_SOURCE_DIR}/Doxyfile.in)
    set(DOXYGEN_OUT ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile)
    
    configure_file(${DOXYGEN_IN} ${DOXYGEN_OUT} @ONLY)
    
    add_custom_target(docs
        COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_OUT}
        WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        COMMENT "Generating API documentation with Doxygen"
        VERBATIM
    )
endif()

# Package configuration
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/RunaVMConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY AnyNewerVersion
)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/RunaVMConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/RunaVMConfig.cmake"
    INSTALL_DESTINATION lib/cmake/RunaVM
)

install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/RunaVMConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/RunaVMConfigVersion.cmake"
    DESTINATION lib/cmake/RunaVM
)

# Export targets
install(EXPORT RunaVMTargets
    FILE RunaVMTargets.cmake
    NAMESPACE RunaVM::
    DESTINATION lib/cmake/RunaVM
)

# Custom targets for development
add_custom_target(format
    COMMAND clang-format -i ${VM_SOURCES} vm.h
    COMMENT "Formatting source code"
)

add_custom_target(lint
    COMMAND cppcheck --enable=all --std=c++17 ${VM_SOURCES} vm.h
    COMMENT "Running static analysis"
)

# Performance monitoring
add_custom_target(profile
    COMMAND ${CMAKE_COMMAND} -E echo "Profiling VM performance..."
    COMMAND benchmark_vm --profile
    DEPENDS benchmark_vm
    COMMENT "Running VM profiling"
)

# Memory leak detection (if available)
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    find_program(VALGRIND valgrind)
    if(VALGRIND)
        add_custom_target(memcheck
            COMMAND ${VALGRIND} --tool=memcheck --leak-check=full --show-leak-kinds=all test_vm
            DEPENDS test_vm
            COMMENT "Running memory leak detection"
        )
    endif()
endif()

# Print configuration summary
message(STATUS "RunaVM Configuration:")
message(STATUS "  Version: ${PROJECT_VERSION}")
message(STATUS "  Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "  C++ standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "  Python version: ${Python3_VERSION}")
message(STATUS "  Install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "  Tests enabled: ${BUILD_TESTING}")
message(STATUS "  Documentation: ${DOXYGEN_FOUND}") 