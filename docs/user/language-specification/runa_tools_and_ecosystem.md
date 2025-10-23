# Runa Tools and Ecosystem

**Version:** 1.0  
**Status:** Canonical  
**Last Updated:** 2024-10-18

---

## Table of Contents

1. [Build System](#build-system)
2. [Testing Framework](#testing-framework)
3. [Annotation System](#annotation-system)
4. [Dependency Management](#dependency-management)

---


# Build System


**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

---

## Table of Contents

1. [Overview](#overview)
2. [Philosophy](#philosophy)
3. [Build File Structure](#build-file-structure)
4. [Basic Build Tasks](#basic-build-tasks)
5. [Dependencies Between Tasks](#dependencies-between-tasks)
6. [Compilation Tasks](#compilation-tasks)
7. [Test Tasks](#test-tasks)
8. [Deployment Tasks](#deployment-tasks)
9. [Advanced Features](#advanced-features)
10. [Comparison with Traditional Build Systems](#comparison-with-traditional-build-systems)
11. [Complete Examples](#complete-examples)
12. [Best Practices](#best-practices)

---

## Overview

**Runa replaces all traditional build systems:**
- ❌ Makefiles
- ❌ npm scripts (package.json)
- ❌ Gradle, Maven (build.gradle, pom.xml)
- ❌ Rake (Rakefile)
- ❌ SCons, CMake
- ❌ Bash build scripts

**With a single unified approach:** `.runa` build files that are executable, type-safe, and cross-platform.

---

## Philosophy

### Why Runa for Builds?

1. **Cross-Platform** - No shell-specific syntax (no `rm -rf` vs `del /f`)
2. **Type-Safe** - Build tasks are validated at compile time
3. **Declarative + Imperative** - Specify what to build AND how to build it
4. **Dependency Graph** - Automatic task ordering and parallelization
5. **First-Class Testing** - Test tasks integrated into build system
6. **One Language** - Code, config, AND builds all in Runa

### Core Concepts

- **Build Tasks** - Named processes that perform build steps
- **Task Dependencies** - Tasks can depend on other tasks (automatic ordering)
- **Artifacts** - Output files produced by tasks
- **Incremental Builds** - Only rebuild what changed
- **Parallelization** - Independent tasks run concurrently

---

## Build File Structure

### Standard Build File

**File:** `build.runa`

```runa
Note: Build configuration for MyProject
Note: This file replaces Makefile, build.sh, etc.

Import "runa/build" as Build

Note: ============================================
Note: PROJECT METADATA
Note: ============================================

Constant PROJECT_NAME as String is "MyProject"
Constant PROJECT_VERSION as String is "1.0.0"
Constant SOURCE_DIR as String is "src"
Constant BUILD_DIR as String is "build"
Constant TEST_DIR as String is "tests"

Note: ============================================
Note: BUILD TASKS
Note: ============================================

@Implementation:
  Clean all build artifacts and temporary files.
@End Implementation

Process called "clean":
    Note: Remove build directory
    If directory_exists(BUILD_DIR):
        proc remove_directory_recursive with BUILD_DIR
    End If

    Display "✓ Cleaned build artifacts"
End Process

@Implementation:
  Compile all source files to executables.
@End Implementation

Process called "compile":
    Note: Ensure build directory exists
    If not directory_exists(BUILD_DIR):
        proc create_directory with BUILD_DIR
    End If

    Note: Compile all .runa files in src/
    Let source_files be find_files with SOURCE_DIR, "*.runa"

    For Each source_file in source_files:
        Let output_file be BUILD_DIR joined with "/" joined with basename(source_file) joined with ".o"
        Display "Compiling " joined with source_file joined with "..."
        proc compile_runa_file with source_file, output_file
    End For

    Display "✓ Compilation complete"
End Process

@Implementation:
  Run all tests in the test directory.
@End Implementation

Process called "test":
    Note: Ensure project is compiled first
    proc compile

    Note: Run all test files
    Let test_files be find_files with TEST_DIR, "test_*.runa"

    Let passed be 0
    Let failed be 0

    For Each test_file in test_files:
        Display "Running " joined with test_file joined with "..."
        Let result be run_test_file with test_file

        If result is "PASS":
            Set passed to passed plus 1
        Otherwise:
            Set failed to failed plus 1
        End If
    End For

    Display "✓ Tests: " joined with string_from(passed) joined with " passed, " joined with string_from(failed) joined with " failed"

    If failed is greater than 0:
        proc panic with "Tests failed"
    End If
End Process

@Implementation:
  Build the final executable.
@End Implementation

Process called "build":
    Note: Clean and compile
    proc clean
    proc compile

    Note: Link all object files
    Display "Linking executable..."
    proc link_executable with PROJECT_NAME, BUILD_DIR

    Display "✓ Build complete: " joined with BUILD_DIR joined with "/" joined with PROJECT_NAME
End Process

@Implementation:
  Full build + tests (default task).
@End Implementation

Process called "all":
    proc build
    proc test
    Display "✓ Build and test complete"
End Process

Note: ============================================
Note: TASK REGISTRY
Note: ============================================

Process called "main":
    Note: Parse command line arguments
    Let args be get_command_line_arguments

    If length of args is 0:
        Note: Default task
        proc all
        Return
    End If

    Let task_name be args at index 0

    Note: Dispatch to task
    If task_name is "clean":
        proc clean
    Otherwise if task_name is "compile":
        proc compile
    Otherwise if task_name is "test":
        proc test
    Otherwise if task_name is "build":
        proc build
    Otherwise if task_name is "all":
        proc all
    Otherwise:
        Display "Unknown task: " joined with task_name
        Display "Available tasks: clean, compile, test, build, all"
        proc exit_with_code with 1
    End If
End Process
```

**Usage:**
```bash
# Run default task (all)
runa build.runa

# Run specific task
runa build.runa clean
runa build.runa compile
runa build.runa test
runa build.runa build
```

---

## Basic Build Tasks

### File Operations

```runa
Process called "setup_directories":
    Note: Create build directory structure

    Let directories be a list containing:
        "build",
        "build/obj",
        "build/bin",
        "build/lib"

    For Each dir in directories:
        If not directory_exists(dir):
            proc create_directory with dir
            Display "Created directory: " joined with dir
        End If
    End For
End Process

Process called "copy_resources":
    Note: Copy static resources to build directory

    Let resource_files be find_files with "resources", "*"

    For Each resource in resource_files:
        Let dest be "build/resources/" joined with basename(resource)
        proc copy_file with resource, dest
        Display "Copied: " joined with resource
    End For
End Process
```

### Compilation Tasks

```runa
Process called "compile_source_files" that takes source_dir as String, output_dir as String:
    Note: Compile all .runa files in directory

    Let source_files be find_files with source_dir, "*.runa"

    For Each source_file in source_files:
        Let relative_path be remove_prefix with source_file, source_dir
        Let output_file be output_dir joined with "/" joined with relative_path joined with ".o"

        Note: Create output directory if needed
        Let output_dir_path be directory_name with output_file
        If not directory_exists(output_dir_path):
            proc create_directory_recursive with output_dir_path
        End If

        Note: Check if recompilation needed (incremental build)
        Let needs_rebuild be true

        If file_exists(output_file):
            Let source_time be file_modified_time with source_file
            Let output_time be file_modified_time with output_file

            If output_time is greater than or equal to source_time:
                Set needs_rebuild to false
            End If
        End If

        If needs_rebuild:
            Display "Compiling: " joined with source_file
            proc compile_runa_file with source_file, output_file
        Otherwise:
            Display "Skipping (up to date): " joined with source_file
        End If
    End For
End Process
```

---

## Dependencies Between Tasks

### Task Dependency System

```runa
Note: Build system with task dependencies

Type called "Task":
    name as String
    dependencies as List[String]
    action as Process
End Type

Type called "BuildGraph":
    tasks as Dictionary[String, Task]
    completed as List[String]
End Type

@Implementation:
  Execute a task and all its dependencies in correct order.
@End Implementation

Process called "execute_task" that takes graph as BuildGraph, task_name as String:
    Note: Check if already completed
    If graph.completed contains task_name:
        Return
    End If

    Note: Get task
    Let task be graph.tasks at key task_name

    Note: Execute dependencies first
    For Each dep in task.dependencies:
        proc execute_task with graph, dep
    End For

    Note: Execute task
    Display "Running task: " joined with task_name
    proc task.action

    Note: Mark as completed
    Add task_name to graph.completed
End Process

@Implementation:
  Define build tasks with dependencies.
@End Implementation

Process called "define_build_graph" returns BuildGraph:
    Let graph be a value of type BuildGraph with
        tasks as an empty dictionary,
        completed as an empty list

    Note: Define tasks
    Set graph.tasks at key "clean" to a value of type Task with
        name as "clean",
        dependencies as an empty list,
        action as clean

    Set graph.tasks at key "setup" to a value of type Task with
        name as "setup",
        dependencies as a list containing "clean",
        action as setup_directories

    Set graph.tasks at key "compile" to a value of type Task with
        name as "compile",
        dependencies as a list containing "setup",
        action as compile_all

    Set graph.tasks at key "test" to a value of type Task with
        name as "test",
        dependencies as a list containing "compile",
        action as run_tests

    Set graph.tasks at key "package" to a value of type Task with
        name as "package",
        dependencies as a list containing "test",
        action as create_package

    Return graph
End Process

Process called "main":
    Let graph be define_build_graph
    Let args be get_command_line_arguments

    Let task_name be if length of args is greater than 0 then args at index 0 otherwise "package"

    proc execute_task with graph, task_name
    Display "✓ Task complete: " joined with task_name
End Process
```

---

## Compilation Tasks

### Multi-Stage Compilation

```runa
@Implementation:
  Multi-stage build process.
  Stage 1: Compile stdlib
  Stage 2: Compile application with stdlib
  Stage 3: Link final executable
@End Implementation

Process called "stage1_compile_stdlib":
    Display "=== Stage 1: Compiling Standard Library ==="

    Let stdlib_sources be find_files with "stdlib", "*.runa"

    For Each source in stdlib_sources:
        Let output be "build/stdlib/" joined with basename(source) joined with ".o"
        proc compile_runa_file with source, output
    End For

    Display "✓ Standard library compiled"
End Process

Process called "stage2_compile_application":
    Display "=== Stage 2: Compiling Application ==="

    Note: Ensure stdlib is compiled first
    proc stage1_compile_stdlib

    Let app_sources be find_files with "src", "*.runa"

    For Each source in app_sources:
        Let output be "build/app/" joined with basename(source) joined with ".o"
        proc compile_runa_file with source, output
    End For

    Display "✓ Application compiled"
End Process

Process called "stage3_link_executable":
    Display "=== Stage 3: Linking Executable ==="

    Note: Ensure application is compiled first
    proc stage2_compile_application

    Note: Collect all object files
    Let stdlib_objects be find_files with "build/stdlib", "*.o"
    Let app_objects be find_files with "build/app", "*.o"

    Let all_objects be concatenate_lists with stdlib_objects, app_objects

    Note: Link final executable
    proc link_executable with "myapp", all_objects, "build/bin/myapp"

    Display "✓ Executable created: build/bin/myapp"
End Process

Process called "build":
    proc stage3_link_executable
    Display "✓ Full build complete"
End Process
```

---

## Test Tasks

### Comprehensive Test Runner

```runa
Type called "TestResult":
    test_name as String
    status as String  Note: PASS, FAIL, ERROR
    duration_ms as Integer
    error_message as String
End Type

@Implementation:
  Run all tests and generate report.
@End Implementation

Process called "run_all_tests" returns List[TestResult]:
    Let test_files be find_files with "tests", "test_*.runa"
    Let results be an empty list of TestResults

    For Each test_file in test_files:
        Let test_name be basename with test_file
        Display "Running: " joined with test_name

        Let start_time be current_time_milliseconds

        Let result be a value of type TestResult with
            test_name as test_name,
            status as "PASS",
            duration_ms as 0,
            error_message as ""

        Note: Run test and capture result
        Let test_output be run_test_file_with_capture with test_file

        Let end_time be current_time_milliseconds
        Set result.duration_ms to end_time minus start_time

        If test_output.exit_code is not 0:
            Set result.status to "FAIL"
            Set result.error_message to test_output.stderr
        End If

        Add result to results
    End For

    Return results
End Process

@Implementation:
  Display test results summary.
@End Implementation

Process called "display_test_summary" that takes results as List[TestResult]:
    Let passed be 0
    Let failed be 0
    Let total_duration be 0

    For Each result in results:
        Set total_duration to total_duration plus result.duration_ms

        If result.status is "PASS":
            Set passed to passed plus 1
            Display "  ✓ " joined with result.test_name joined with " (" joined with string_from(result.duration_ms) joined with "ms)"
        Otherwise:
            Set failed to failed plus 1
            Display "  ✗ " joined with result.test_name joined with " (" joined with string_from(result.duration_ms) joined with "ms)"
            Display "    Error: " joined with result.error_message
        End If
    End For

    Display ""
    Display "=== Test Summary ==="
    Display "Total: " joined with string_from(length of results)
    Display "Passed: " joined with string_from(passed)
    Display "Failed: " joined with string_from(failed)
    Display "Duration: " joined with string_from(total_duration) joined with "ms"

    If failed is greater than 0:
        proc panic with "Tests failed"
    End If
End Process

Process called "test":
    Display "=== Running Test Suite ==="
    Let results be run_all_tests
    proc display_test_summary with results
End Process
```

---

## Deployment Tasks

### Package and Deploy

```runa
@Implementation:
  Create deployable package with all dependencies.
@End Implementation

Process called "package":
    Display "=== Creating Deployment Package ==="

    Note: Ensure build is complete
    proc build

    Note: Create package directory
    Let package_dir be "build/package"
    If directory_exists(package_dir):
        proc remove_directory_recursive with package_dir
    End If
    proc create_directory with package_dir

    Note: Copy executable
    proc copy_file with "build/bin/myapp", package_dir joined with "/myapp"

    Note: Copy resources
    proc copy_directory_recursive with "resources", package_dir joined with "/resources"

    Note: Copy configuration
    proc copy_file with "config.runa", package_dir joined with "/config.runa"

    Note: Create archive
    Let version be get_project_version
    Let archive_name be "myapp-" joined with version joined with ".tar.gz"

    proc create_archive with package_dir, "build/" joined with archive_name

    Display "✓ Package created: build/" joined with archive_name
End Process

@Implementation:
  Deploy package to remote server.
@End Implementation

Process called "deploy" that takes environment as String:
    Display "=== Deploying to " joined with environment joined with " ==="

    Note: Ensure package is created
    proc package

    Note: Get deployment configuration
    Let config be load_deployment_config with environment

    Note: Upload package
    Let version be get_project_version
    Let archive_name be "myapp-" joined with version joined with ".tar.gz"

    Display "Uploading to " joined with config.server joined with "..."
    proc scp_upload with "build/" joined with archive_name, config.server, config.deploy_path

    Note: Extract on remote server
    Display "Extracting on remote server..."
    proc ssh_execute with config.server, "tar -xzf " joined with config.deploy_path joined with "/" joined with archive_name

    Note: Restart service
    Display "Restarting service..."
    proc ssh_execute with config.server, "systemctl restart myapp"

    Display "✓ Deployment complete"
End Process

Process called "deploy_staging":
    proc deploy with "staging"
End Process

Process called "deploy_production":
    Note: Require confirmation for production
    Display "WARNING: Deploying to PRODUCTION"
    Display "Type 'yes' to confirm:"

    Let confirmation be read_line_from_stdin

    If confirmation is not "yes":
        Display "Deployment cancelled"
        Return
    End If

    proc deploy with "production"
End Process
```

---

## Advanced Features

### Parallel Task Execution

```runa
@Implementation:
  Run independent tasks in parallel for faster builds.
@End Implementation

Process called "parallel_compile" that takes source_dirs as List[String]:
    Display "=== Parallel Compilation ==="

    Let tasks be an empty list

    Note: Create compilation task for each directory
    For Each dir in source_dirs:
        Let task be create_async_task with compile_directory, dir
        Add task to tasks
    End For

    Note: Wait for all tasks to complete
    For Each task in tasks:
        proc wait_for_task with task
    End For

    Display "✓ Parallel compilation complete"
End Process

Process called "compile_directory" that takes dir as String:
    Let sources be find_files with dir, "*.runa"

    For Each source in sources:
        proc compile_runa_file with source, "build/" joined with source joined with ".o"
    End For
End Process
```

### Conditional Builds

```runa
@Implementation:
  Conditional compilation based on platform or features.
@End Implementation

Process called "build_for_platform":
    Let platform be get_current_platform

    Display "Building for platform: " joined with platform

    If platform is "linux":
        proc compile_with_flags with "src", "build", "-DLINUX"
    Otherwise if platform is "windows":
        proc compile_with_flags with "src", "build", "-DWINDOWS"
    Otherwise if platform is "macos":
        proc compile_with_flags with "src", "build", "-DMACOS"
    Otherwise:
        proc panic with "Unsupported platform: " joined with platform
    End If
End Process

Process called "build_with_features" that takes features as List[String]:
    Display "Building with features: " joined with join(features, ", ")

    Let flags be ""

    For Each feature in features:
        Set flags to flags joined with " -DFEATURE_" joined with uppercase(feature)
    End For

    proc compile_with_flags with "src", "build", flags
End Process
```

### Watch and Rebuild

```runa
@Implementation:
  Watch source files and rebuild on changes.
@End Implementation

Process called "watch":
    Display "=== Watching for changes ==="
    Display "Press Ctrl+C to stop"

    Let last_build_time be current_time_milliseconds

    While true:
        Note: Check if any source files changed
        Let source_files be find_files with "src", "*.runa"
        Let needs_rebuild be false

        For Each source in source_files:
            Let modified_time be file_modified_time with source

            If modified_time is greater than last_build_time:
                Set needs_rebuild to true
                Break
            End If
        End For

        If needs_rebuild:
            Display "Changes detected, rebuilding..."
            proc build
            Set last_build_time to current_time_milliseconds
            Display "✓ Rebuild complete. Watching..."
        End If

        Note: Sleep before checking again
        proc sleep_milliseconds with 1000
    End While
End Process
```

---

## Comparison with Traditional Build Systems

### Runa vs Makefile

**Makefile (shell-specific, error-prone):**
```makefile
SRC_DIR = src
BUILD_DIR = build
SOURCES = $(wildcard $(SRC_DIR)/*.runa)
OBJECTS = $(SOURCES:$(SRC_DIR)/%.runa=$(BUILD_DIR)/%.o)

all: build test

clean:
	rm -rf $(BUILD_DIR)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.runa
	mkdir -p $(BUILD_DIR)
	runac $< $@

build: $(OBJECTS)
	ld -o $(BUILD_DIR)/myapp $(OBJECTS)

test: build
	./run_tests.sh

.PHONY: all clean build test
```

**Runa (cross-platform, type-safe):**
```runa
Constant SOURCE_DIR as String is "src"
Constant BUILD_DIR as String is "build"

Process called "clean":
    If directory_exists(BUILD_DIR):
        proc remove_directory_recursive with BUILD_DIR
    End If
End Process

Process called "compile":
    Let sources be find_files with SOURCE_DIR, "*.runa"

    For Each source in sources:
        Let output be BUILD_DIR joined with "/" joined with basename(source) joined with ".o"
        proc compile_runa_file with source, output
    End For
End Process

Process called "build":
    proc compile
    proc link_executable with "myapp", BUILD_DIR
End Process

Process called "test":
    proc build
    proc run_test_suite
End Process

Process called "all":
    proc build
    proc test
End Process
```

### Runa vs npm scripts

**package.json (limited, no logic):**
```json
{
  "scripts": {
    "build": "tsc && webpack",
    "test": "jest",
    "clean": "rm -rf build",
    "deploy": "npm run build && scp -r build/ user@server:/path"
  }
}
```

**Runa (full logic, cross-platform):**
```runa
Process called "build":
    proc compile_typescript
    proc run_webpack
End Process

Process called "test":
    proc run_jest_tests
End Process

Process called "clean":
    If directory_exists("build"):
        proc remove_directory_recursive with "build"
    End If
End Process

Process called "deploy":
    proc build

    Let config be load_deploy_config
    proc scp_upload with "build", config.server, config.path
End Process
```

---

## Complete Examples

### Full-Featured Build System

**File:** `build.runa`

```runa
Note: Complete build system for production application

Import "runa/build" as Build
Import "runa/filesystem" as FS
Import "runa/process" as Proc

@Reasoning:
  Production-grade build system with:
  - Multi-stage compilation
  - Parallel builds
  - Incremental compilation
  - Comprehensive testing
  - Deployment automation
@End Reasoning

Note: ============================================
Note: CONSTANTS
Note: ============================================

Constant PROJECT_NAME as String is "MyApp"
Constant PROJECT_VERSION as String is "1.2.3"
Constant SOURCE_DIR as String is "src"
Constant TEST_DIR as String is "tests"
Constant BUILD_DIR as String is "build"
Constant STDLIB_DIR as String is "stdlib"

Note: ============================================
Note: UTILITIES
Note: ============================================

Process called "ensure_directory" that takes path as String:
    If not FS.directory_exists(path):
        proc FS.create_directory_recursive with path
    End If
End Process

Process called "get_timestamp" returns String:
    Let time be Proc.current_time_milliseconds
    Return string_from with time
End Process

Note: ============================================
Note: CLEAN TASK
Note: ============================================

@Implementation:
  Remove all build artifacts and temporary files.
@End Implementation

Process called "clean":
    Display "🧹 Cleaning build artifacts..."

    If FS.directory_exists(BUILD_DIR):
        proc FS.remove_directory_recursive with BUILD_DIR
    End If

    Note: Remove temporary files
    Let temp_files be FS.find_files with ".", "*.tmp"
    For Each temp_file in temp_files:
        proc FS.remove_file with temp_file
    End For

    Display "✓ Clean complete"
End Process

Note: ============================================
Note: SETUP TASK
Note: ============================================

@Implementation:
  Create build directory structure.
@End Implementation

Process called "setup":
    Display "📁 Setting up build directories..."

    Let directories be a list containing:
        BUILD_DIR,
        BUILD_DIR joined with "/stdlib",
        BUILD_DIR joined with "/app",
        BUILD_DIR joined with "/bin",
        BUILD_DIR joined with "/tests"

    For Each dir in directories:
        proc ensure_directory with dir
    End For

    Display "✓ Setup complete"
End Process

Note: ============================================
Note: COMPILATION TASKS
Note: ============================================

@Implementation:
  Compile standard library.
@End Implementation

Process called "compile_stdlib":
    Display "📚 Compiling standard library..."

    Let stdlib_sources be FS.find_files with STDLIB_DIR, "*.runa"
    Let compiled be 0

    For Each source in stdlib_sources:
        Let output be BUILD_DIR joined with "/stdlib/" joined with FS.basename(source) joined with ".o"

        Note: Incremental build - check if recompilation needed
        If Build.needs_recompilation with source, output:
            Display "  Compiling: " joined with source
            proc Build.compile_runa_file with source, output
            Set compiled to compiled plus 1
        End If
    End For

    Display "✓ Standard library compiled (" joined with string_from(compiled) joined with " files)"
End Process

@Implementation:
  Compile application source code.
@End Implementation

Process called "compile_app":
    Display "🔨 Compiling application..."

    Let app_sources be FS.find_files with SOURCE_DIR, "*.runa"
    Let compiled be 0

    For Each source in app_sources:
        Let relative_path be FS.remove_prefix with source, SOURCE_DIR
        Let output be BUILD_DIR joined with "/app/" joined with relative_path joined with ".o"

        Note: Create output directory
        Let output_dir be FS.directory_name with output
        proc ensure_directory with output_dir

        Note: Incremental build
        If Build.needs_recompilation with source, output:
            Display "  Compiling: " joined with source
            proc Build.compile_runa_file with source, output
            Set compiled to compiled plus 1
        End If
    End For

    Display "✓ Application compiled (" joined with string_from(compiled) joined with " files)"
End Process

@Implementation:
  Link final executable.
@End Implementation

Process called "link":
    Display "🔗 Linking executable..."

    Note: Collect all object files
    Let stdlib_objects be FS.find_files with BUILD_DIR joined with "/stdlib", "*.o"
    Let app_objects be FS.find_files with BUILD_DIR joined with "/app", "*.o"

    Let all_objects be concatenate_lists with stdlib_objects, app_objects

    Note: Link executable
    Let executable_path be BUILD_DIR joined with "/bin/" joined with PROJECT_NAME

    proc Build.link_executable with PROJECT_NAME, all_objects, executable_path

    Display "✓ Executable created: " joined with executable_path
End Process

Note: ============================================
Note: BUILD TASK
Note: ============================================

@Implementation:
  Full build pipeline.
@End Implementation

Process called "build":
    Let start_time be Proc.current_time_milliseconds

    proc setup
    proc compile_stdlib
    proc compile_app
    proc link

    Let end_time be Proc.current_time_milliseconds
    Let duration be end_time minus start_time

    Display "✓ Build complete in " joined with string_from(duration) joined with "ms"
End Process

Note: ============================================
Note: TEST TASKS
Note: ============================================

@Implementation:
  Run test suite.
@End Implementation

Process called "test":
    Display "🧪 Running test suite..."

    Note: Ensure build is up to date
    proc build

    Let test_files be FS.find_files with TEST_DIR, "test_*.runa"
    Let passed be 0
    Let failed be 0

    For Each test_file in test_files:
        Let test_name be FS.basename with test_file
        Display "  Running: " joined with test_name

        Let result be Build.run_test_file with test_file

        If result.status is "PASS":
            Set passed to passed plus 1
            Display "    ✓ PASS (" joined with string_from(result.duration_ms) joined with "ms)"
        Otherwise:
            Set failed to failed plus 1
            Display "    ✗ FAIL (" joined with string_from(result.duration_ms) joined with "ms)"
            Display "    " joined with result.error_message
        End If
    End For

    Display ""
    Display "=== Test Summary ==="
    Display "Passed: " joined with string_from(passed)
    Display "Failed: " joined with string_from(failed)

    If failed is greater than 0:
        proc panic with "Tests failed"
    End If

    Display "✓ All tests passed"
End Process

Note: ============================================
Note: PACKAGE TASK
Note: ============================================

@Implementation:
  Create deployment package.
@End Implementation

Process called "package":
    Display "📦 Creating deployment package..."

    Note: Ensure tests pass
    proc test

    Note: Create package directory
    Let package_dir be BUILD_DIR joined with "/package"

    If FS.directory_exists(package_dir):
        proc FS.remove_directory_recursive with package_dir
    End If

    proc FS.create_directory with package_dir

    Note: Copy executable
    proc FS.copy_file with BUILD_DIR joined with "/bin/" joined with PROJECT_NAME, package_dir joined with "/" joined with PROJECT_NAME

    Note: Copy resources
    If FS.directory_exists("resources"):
        proc FS.copy_directory_recursive with "resources", package_dir joined with "/resources"
    End If

    Note: Copy configuration
    proc FS.copy_file with "config.runa", package_dir joined with "/config.runa"

    Note: Create archive
    Let archive_name be PROJECT_NAME joined with "-" joined with PROJECT_VERSION joined with ".tar.gz"
    proc Build.create_archive with package_dir, BUILD_DIR joined with "/" joined with archive_name

    Display "✓ Package created: " joined with BUILD_DIR joined with "/" joined with archive_name
End Process

Note: ============================================
Note: DEPLOYMENT TASKS
Note: ============================================

@Implementation:
  Deploy to staging environment.
@End Implementation

Process called "deploy_staging":
    Display "🚀 Deploying to STAGING..."

    proc package

    Let config be load_deploy_config with "staging"
    Let archive_name be PROJECT_NAME joined with "-" joined with PROJECT_VERSION joined with ".tar.gz"

    proc Build.scp_upload with BUILD_DIR joined with "/" joined with archive_name, config.server, config.deploy_path

    proc Build.ssh_execute with config.server, "systemctl restart " joined with PROJECT_NAME

    Display "✓ Deployed to staging"
End Process

@Implementation:
  Deploy to production environment (requires confirmation).
@End Implementation

Process called "deploy_production":
    Display "🚀 Deploying to PRODUCTION"
    Display "WARNING: This will deploy to live servers"
    Display "Type 'yes' to confirm:"

    Let confirmation be Proc.read_line_from_stdin

    If confirmation is not "yes":
        Display "Deployment cancelled"
        Return
    End If

    proc package

    Let config be load_deploy_config with "production"
    Let archive_name be PROJECT_NAME joined with "-" joined with PROJECT_VERSION joined with ".tar.gz"

    proc Build.scp_upload with BUILD_DIR joined with "/" joined with archive_name, config.server, config.deploy_path

    proc Build.ssh_execute with config.server, "systemctl restart " joined with PROJECT_NAME

    Display "✓ Deployed to production"
End Process

Note: ============================================
Note: MAIN ENTRY POINT
Note: ============================================

Process called "main":
    Let args be Proc.get_command_line_arguments

    If length of args is 0:
        Display "Available tasks: clean, build, test, package, deploy-staging, deploy-production"
        Return
    End If

    Let task be args at index 0

    If task is "clean":
        proc clean
    Otherwise if task is "build":
        proc build
    Otherwise if task is "test":
        proc test
    Otherwise if task is "package":
        proc package
    Otherwise if task is "deploy-staging":
        proc deploy_staging
    Otherwise if task is "deploy-production":
        proc deploy_production
    Otherwise:
        Display "Unknown task: " joined with task
        Display "Available: clean, build, test, package, deploy-staging, deploy-production"
        proc Proc.exit_with_code with 1
    End If
End Process
```

---

## Best Practices

### 1. Use Incremental Builds

```runa
Note: GOOD - Only rebuild what changed
Process called "compile_incremental" that takes source as String, output as String:
    If Build.needs_recompilation with source, output:
        proc Build.compile_runa_file with source, output
    End If
End Process
```

### 2. Parallelize Independent Tasks

```runa
Note: GOOD - Compile directories in parallel
Process called "parallel_build":
    Let dirs be a list containing "src/module1", "src/module2", "src/module3"
    Let tasks be an empty list

    For Each dir in dirs:
        Let task be create_async_task with compile_directory, dir
        Add task to tasks
    End For

    For Each task in tasks:
        proc wait_for_task with task
    End For
End Process
```

### 3. Validate Before Deployment

```runa
Note: GOOD - Always test before deploying
Process called "deploy":
    proc test  Note: Fail fast if tests don't pass
    proc package
    proc upload_to_server
End Process
```

### 4. Use Task Dependencies

```runa
Note: GOOD - Explicit dependency graph
Process called "package":
    proc build  Note: Ensure build is current
    proc test  Note: Ensure tests pass
    Note: Now safe to package
    proc create_deployment_package
End Process
```

### 5. Provide Clear Feedback

```runa
Note: GOOD - Show progress and results
Process called "build":
    Display "🔨 Starting build..."
    Let start_time be current_time_milliseconds

    proc compile

    Let end_time be current_time_milliseconds
    Let duration be end_time minus start_time

    Display "✓ Build complete in " joined with string_from(duration) joined with "ms"
End Process
```

---

## Summary

**Runa replaces all build systems with:**
- ✅ Cross-platform build scripts (no shell dependencies)
- ✅ Type-safe task definitions
- ✅ Built-in dependency management
- ✅ Incremental compilation support
- ✅ Parallel task execution
- ✅ Integrated testing and deployment

**Stop using:** Makefiles, npm scripts, Gradle, Maven, etc.

**Start using:** `build.runa` for ALL build automation.

---

## See Also

- [Runa Data & Config Format](./runa_data_config_format.md) - Configuration files
- [Runa CI/CD Pipelines](./runa_ci_cd_pipelines.md) - Continuous integration
- [Runa Container Specification](./runa_container_specification.md) - Container builds
- [Runa Testing Framework](./runa_testing_framework.md) - Test automation

---

**End of Document**

---

# Testing Framework


**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

---

## Overview

**Runa replaces all testing frameworks with built-in test syntax.**

**Replaces:**
- ❌ Jest, Mocha, Jasmine (JavaScript)
- ❌ pytest, unittest (Python)
- ❌ JUnit, TestNG (Java)
- ❌ RSpec, Minitest (Ruby)
- ❌ Go testing package

---

## Basic Test File

**File:** `tests/test_calculator.runa`

```runa
Note: Unit tests for calculator module
Note: Replaces Jest, pytest, JUnit, etc.

Import "calculator.runa" as Calc
Import "runa/test" as Test

@Reasoning:
  Test suite for calculator functions.
  Ensures arithmetic operations work correctly.
@End Reasoning

Process called "test_addition":
    Note: Test addition function
    Let result be Calc.add with 2, 3
    proc Test.assert_equal with result, 5, "2 + 3 should equal 5"

    Let result2 be Calc.add with -1, 1
    proc Test.assert_equal with result2, 0, "(-1) + 1 should equal 0"
End Process

Process called "test_subtraction":
    Note: Test subtraction function
    Let result be Calc.subtract with 10, 3
    proc Test.assert_equal with result, 7, "10 - 3 should equal 7"

    Let result2 be Calc.subtract with 5, 10
    proc Test.assert_equal with result2, -5, "5 - 10 should equal -5"
End Process

Process called "test_multiplication":
    Let result be Calc.multiply with 4, 5
    proc Test.assert_equal with result, 20, "4 * 5 should equal 20"
End Process

Process called "test_division":
    Let result be Calc.divide with 10, 2
    proc Test.assert_equal with result, 5, "10 / 2 should equal 5"
End Process

Process called "test_division_by_zero":
    Note: Test error handling
    proc Test.assert_raises with ZeroDivisionError, divide_by_zero
End Process

Process called "divide_by_zero":
    proc Calc.divide with 10, 0
End Process

Note: Test runner discovers all processes starting with "test_"
```

**Usage:**
```bash
# Run all tests
runa test

# Run specific test file
runa test tests/test_calculator.runa

# Run with coverage
runa test --coverage
```

---

## Test Assertions

```runa
Process called "test_all_assertions":
    Note: Equality assertions
    proc Test.assert_equal with 5, 5
    proc Test.assert_not_equal with 5, 10

    Note: Boolean assertions
    proc Test.assert_true with true
    proc Test.assert_false with false

    Note: Null checks
    proc Test.assert_null with null
    proc Test.assert_not_null with "value"

    Note: Collection assertions
    Let list be a list containing 1, 2, 3
    proc Test.assert_contains with list, 2
    proc Test.assert_length with list, 3

    Note: String assertions
    proc Test.assert_starts_with with "Hello World", "Hello"
    proc Test.assert_ends_with with "Hello World", "World"
    proc Test.assert_contains_substring with "Hello World", "lo Wo"

    Note: Numeric assertions
    proc Test.assert_greater_than with 10, 5
    proc Test.assert_less_than with 5, 10
    proc Test.assert_in_range with 7, 5, 10

    Note: Exception assertions
    proc Test.assert_raises with ValueError, function_that_throws
End Process
```

---

## Test Fixtures (Setup/Teardown)

```runa
Type called "TestContext":
    database as Database
    test_user as User
End Type

Process called "setup" returns TestContext:
    Note: Run before each test
    Let db be DB.connect_test_database
    Let user be create_test_user with "test@example.com"

    Return a value of type TestContext with
        database as db,
        test_user as user
End Process

Process called "teardown" that takes context as TestContext:
    Note: Run after each test
    proc DB.disconnect with context.database
    proc delete_test_user with context.test_user
End Process

Process called "test_user_creation":
    Let context be setup

    Note: Test logic here
    Let user be context.test_user
    proc Test.assert_equal with user.email, "test@example.com"

    proc teardown with context
End Process
```

---

## Parametrized Tests

```runa
Process called "test_addition_parametrized":
    Let test_cases be a list containing:
        case with 2, 3, 5,
        case with 10, 5, 15,
        case with -1, 1, 0,
        case with 0, 0, 0,
        case with 100, 200, 300

    For Each test_case in test_cases:
        Let result be Calc.add with test_case.a, test_case.b
        proc Test.assert_equal with result, test_case.expected, string_from(test_case.a) joined with " + " joined with string_from(test_case.b) joined with " should equal " joined with string_from(test_case.expected)
    End For
End Process

Type called "TestCase":
    a as Integer
    b as Integer
    expected as Integer
End Type

Process called "case" that takes a as Integer, b as Integer, expected as Integer returns TestCase:
    Return a value of type TestCase with a as a, b as b, expected as expected
End Process
```

---

## Mocking

```runa
Process called "test_with_mock":
    Note: Create mock database
    Let mock_db be Test.create_mock with "Database"

    Note: Define mock behavior
    proc Test.when with mock_db, "query", a list containing "users"
        .then_return with a list containing test_user

    Note: Test function that uses database
    Let users be fetch_users with mock_db

    proc Test.assert_length with users, 1
    proc Test.verify_called with mock_db, "query", a list containing "users"
End Process

Process called "test_user" returns User:
    Return a value of type User with
        id as 1,
        email as "test@example.com"
End Process
```

---

## Integration Tests

**File:** `tests/integration/test_api.runa`

```runa
Note: Integration tests for API

Import "runa/test" as Test
Import "runa/http" as HTTP

Process called "test_user_registration_flow":
    Note: Start test server
    Let server be Test.start_test_server("localhost", 8080)

    Note: Register user
    Let response be HTTP.post with "http://localhost:8080/register", a dictionary containing:
        "email" as "newuser@example.com",
        "password" as "securepassword"
    End Dictionary

    proc Test.assert_equal with response.status_code, 201
    proc Test.assert_contains with response.body, "user_id"

    Note: Login
    Let login_response be HTTP.post with "http://localhost:8080/login", a dictionary containing:
        "email" as "newuser@example.com",
        "password" as "securepassword"
    End Dictionary

    proc Test.assert_equal with login_response.status_code, 200
    proc Test.assert_contains with login_response.body, "auth_token"

    Note: Stop test server
    proc Test.stop_test_server with server
End Process
```

---

## Test Coverage

```runa
Process called "generate_coverage_report":
    Note: Run tests with coverage tracking
    Let results be Test.run_all_tests_with_coverage with "tests/"

    Display "Total Coverage: " joined with string_from(results.coverage_percent) joined with "%"

    Note: Generate HTML report
    proc Test.generate_coverage_html with results, "coverage/index.html"

    Note: Enforce minimum coverage
    If results.coverage_percent is less than 80.0:
        proc panic with "Coverage below 80% threshold"
    End If
End Process
```

---

## Jest/Pytest Comparison

**Before (Jest):**
```javascript
describe('Calculator', () => {
  test('adds two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  test('subtracts two numbers', () => {
    expect(subtract(10, 3)).toBe(7);
  });
});
```

**Before (pytest):**
```python
def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(10, 3) == 7
```

**After (Runa):**
```runa
Process called "test_add":
    proc Test.assert_equal with add with 2, 3, 5
End Process

Process called "test_subtract":
    proc Test.assert_equal with subtract with 10, 3, 7
End Process
```

---

## Snapshot Testing

```runa
Process called "test_ui_component_snapshot":
    Let component be render_user_card with test_user

    Note: Create or compare snapshot
    proc Test.assert_snapshot_matches with component, "user_card_snapshot"
End Process

Process called "update_snapshots":
    Note: Update all snapshots
    proc Test.update_all_snapshots with "tests/"
End Process
```

---

## Performance/Benchmark Tests

```runa
Process called "test_performance":
    Let start_time be current_time_milliseconds

    Note: Run operation 1000 times
    For i from 1 to 1000:
        proc expensive_operation
    End For

    Let end_time be current_time_milliseconds
    Let duration be end_time minus start_time

    proc Test.assert_less_than with duration, 1000, "Operation should complete in under 1 second"
End Process

Process called "benchmark_sorting_algorithms":
    Let data be generate_random_list with 10000

    Let bubble_time be Test.benchmark with bubble_sort, data
    Let quick_time be Test.benchmark with quick_sort, data
    Let merge_time be Test.benchmark with merge_sort, data

    Display "Bubble Sort: " joined with string_from(bubble_time) joined with "ms"
    Display "Quick Sort: " joined with string_from(quick_time) joined with "ms"
    Display "Merge Sort: " joined with string_from(merge_time) joined with "ms"
End Process
```

---

## Summary

**Runa replaces testing frameworks with:**
- ✅ Built-in test syntax (no external framework)
- ✅ Unified assertions
- ✅ Integrated mocking and fixtures
- ✅ Coverage reporting
- ✅ Snapshot testing
- ✅ Performance benchmarks

**Stop using:** Jest, pytest, JUnit, RSpec
**Start using:** `test_*.runa` files with built-in Test module

---

**End of Document**

---

# Annotation System

*Structured Annotations for Direct AI Intent and Interaction*

**Last Updated**: 2025-09-08  
**Note**: This documentation reflects the current implementation with mathematical symbol enforcement.

## Overview

Runa’s annotation system encodes developer and architect intent for AI systems. Annotations are not comments; they are machine-parseable directives and context for AI agents and AI-powered tools. All AI engineers should use them, and developers building AI tools should prefer them to ad-hoc comments when intent must be consumed by machines.

**Mathematical Symbol Note**: All annotation examples use natural language operators (`plus`, `minus`, `is less than`) which are always valid. Mathematical symbols are restricted to mathematical contexts only.

### Implementation Conformance (Bootstrap Compiler)

The bootstrap parser currently recognizes and parses the following top-level annotation blocks:

- @Reasoning ... @End_Reasoning
- @Implementation ... @End_Implementation
- @Uncertainty ... @End_Uncertainty
- @Request_Clarification ... @End_Request_Clarification
- @KnowledgeReference ... @End_KnowledgeReference
- @TestCases ... @End_TestCases
- @Resource_Constraints ... @End_Resource_Constraints
- @Security_Scope ... @End_Security_Scope
- @Execution_Model ... @End_Execution_Model
- @Performance_Hints ... @End_Performance_Hints
- @Progress ... @End_Progress
- @Feedback ... @End_Feedback
- @Translation_Note ... @End_Translation_Note
- @Error_Handling ... @End_Error_Handling

Specified but not yet routed by the bootstrap parser as top-level blocks (reserved and recognized by the lexer, but not consumed as annotation blocks yet):

- @Task, @End_Task
- @Requirements, @End_Requirements
- @Verify, @End_Verify
- @Request, @End_Request
- @Context, @End_Context
- @Collaboration, @End_Collaboration
- @Iteration, @End_Iteration
- @Clarification, @End_Clarification

These remain part of the language specification and are supported in the annotation type system; parser routing will be enabled in a subsequent bootstrap update. Until then, keep these blocks in code for forward-compatibility, or place their content inside parsed blocks (e.g., within @Implementation) if immediate parsing is required.

## Core Concepts

### Annotation Categories and Intent

Runa provides several types of annotations that can be used individually or in combination:

- **Reasoning Annotations**: Convey the why behind decisions to guide AI synthesis and refactoring.
- **Context Annotations**: Describe environment, constraints, and assumptions for AI planning.
- **Verification Annotations**: Declare properties the AI must maintain/verify.
- **Resource/Security Annotations**: Bound what AI may do and under what budgets/capabilities.
- **Task/Requirements Annotations**: Specify formal objectives for AI agents to implement/check.

### Design Principles

1. **Semantic Preservation**: Annotations maintain meaning across different contexts and tools
2. **Tool Agnostic**: Annotations work with various development tools and AI systems
3. **Human Readable**: All annotations use natural language for clarity
4. **Machine Parseable**: Structured format enables automated processing
5. **Optional**: Annotations enhance code but are never required (strongly recommended for AI workflows)
### Usage Guidance (When and Why)

- Use annotations whenever AI agents must consume intent (architecture, constraints, goals, verification) rather than relying on prose.
- Prefer annotations to free-text comments for machine-facing guidance; use comments for human narration.
- Co-locate annotations with the code they govern; keep scopes minimal and precise.
- Treat annotations as normative inputs for AI tooling; conflicting comments yield to annotations.

### Lifecycle and Evaluation Phase

- Parsing: Annotations are parsed at compile-time and made available to tooling.
- Evaluation: Some annotations have compile-time effects (e.g., verification), others inform runtime systems (e.g., execution model) without overhead.
- Precedence: File-local overrides module-level; inner blocks override outer; explicit keys override defaults.

6. **Language Agnostic**: Annotation format works across all target programming languages

## Annotation Categories

### 1. Reasoning and Intent Annotations

#### @Reasoning Block
Documents the logical reasoning process and decision rationale behind code implementations.

What this is used for:
- Capture design rationale, trade-offs, and decision history for AI agents to respect during refactors and generation.
- Provide auditable context for reviewers and future maintainers.

How to use this:
- Place immediately above the implementation it governs.
- Write concise bullet points; prefer measurable criteria and constraints.
- Reference external sources with @KnowledgeReference when applicable.

Example (ideal structure):
```runa
@Reasoning:
    Goal: Reduce p95 latency below 50ms without increasing error rate
    Options considered: cache, batch, rewrite
    Decision: cache because hit-rate > 0.9, memory budget 256MB
    Risks: staleness; Mitigation: ttl=60s, background refresh
@End_Reasoning
```

or

```runa
@Reasoning:
    The quicksort algorithm is preferred over merge sort in this case because:
    1. We have a small dataset that fits in memory (< 10,000 items)
    2. The partial ordering of the data suggests good pivot selection
    3. The implementation is simpler and requires less additional memory
    4. Average case performance is O(n log n) which meets our requirements
@End_Reasoning
```

**Purpose**: Improves code maintainability by documenting the reasoning behind implementation decisions.

#### @Implementation Block
Provides detailed implementation notes and guidance.

What this is used for:
- Specify authoritative implementation structure, invariants, and algorithmic steps the AI should follow.
- Disambiguate between multiple viable implementations.

How to use this:
- Co-locate with the target process/type.
- Use imperative, stepwise instructions; include inputs/outputs and edge-case handling.

Example (ideal structure):
```runa
@Implementation:
    Process: "resize_image"
    Steps:
        1. Validate format ∈ {png,jpg}; Otherwise throw ValueError
        2. Compute scale preserving aspect ratio
        3. Apply bilinear filter; clamp to bounds
        4. Return new buffer with metadata updated
@End_Implementation
```

**Purpose**: Bridges the gap between high-level algorithmic thinking and concrete implementation details.

### 2. Uncertainty and Confidence Annotations

#### @Uncertainty Expression
Represents multiple possible choices with confidence levels.

What this is used for:
- Declare alternatives where multiple approaches are acceptable, with a confidence hint for selection.

How to use this:
- Limit to top 2–4 realistic options.
- Always include a numeric confidence and criteria for promotion/demotion.

Example (ideal structure):
```runa
Let hash_strategy be ?[SipHash, Murmur3] with confidence 0.7
```

**Purpose**: Allows developers to express uncertainty and make informed decisions about implementation choices.

### 3. Knowledge and Context Annotations

#### @KnowledgeReference Block
Links implementation to external knowledge sources.

What this is used for:
- Bind code decisions to vetted sources (papers, specs, standards) for traceability.

How to use this:
- Include stable identifiers (DOI, arXiv, version pins).
- Add a one-line "why relevant" note.

Example (ideal structure):
```runa
@KnowledgeReference:
    concept: "A* Search"
    reference_id: "doi:10.1145/321105.321114"
    version: "canonical"
    relevance: "Optimal pathfinding with admissible heuristics"
@End_KnowledgeReference
```

or

```runa
@KnowledgeReference:
    concept: "Transformer Architecture"
    reference_id: "arxiv:1706.03762"
    version: "as of 2023-10"
    relevant_sections: ["3.1 Scaled Dot-Product Attention", "3.2 Multi-Head Attention"]
    implementation_notes: "Using standard transformer but with modified positional encoding"
@End_KnowledgeReference
```

#### @Context Block
Provides situational context for implementation decisions.

What this is used for:
- Inform agents about deployment constraints, platforms, and business context impacting choices.

How to use this:
- Keep keys stable across a repository; prefer enums over free text.
- Scope narrowly (module or file) to avoid stale global context.

Example (ideal structure):
```runa
@Context:
    deployment_environment: "edge_device"
    latency_budget_ms: 50
    memory_limit_mb: 256
    reliability_target: "99.9%"
@End_Context
```

or

```runa
@Context:
    deployment_environment: "edge_device"
    performance_constraints: "sub_100ms_latency"
    memory_constraints: "max_512MB"
    user_base: "mobile_users"
    criticality: "high"
@End_Context
```

### 4. Task and Specification Annotations

#### @Task Block
Formal task specification for AI-assisted development.

What this is used for:
- Define objective, constraints, and acceptance for an autonomous or assisted task.

How to use this:
- Be testable: specify inputs/outputs and DONE criteria.
- Include priority and deadline only if actionable.

Example (ideal structure):
```runa
@Task:
    objective: "Implement LRU cache"
    inputs: ["capacity:Int", "loader:Function"]
    outputs: ["get/put interface", "eviction policy"]
    acceptance: ["O(1) ops", ">=95% hit-rate on Zipf(1.2)"]
@End_Task
```

or

```runa
@Task:
    objective: "Implement real-time face detection system"
    constraints: [
        "Must run on mobile devices",
        "Battery efficient",
        "Accuracy > 95%",
        "Latency < 50ms per frame"
    ]
    input_format: "Video stream (720p, 30fps)"
    output_format: "Bounding boxes with confidence scores"
    target_language: "Python"
    frameworks: ["OpenCV", "TensorFlow Lite"]
    priority: "Performance over accuracy"
    deadline: "2 weeks"
@End_Task
```

#### @Requirements Block
Detailed functional and non-functional requirements.

What this is used for:
- Contract for features and qualities; drives verification and tests.

How to use this:
- Separate functional vs non-functional; make each requirement verifiable.
- Cross-link to @Verify and @TestCases.

Example (ideal structure):
```runa
@Requirements:
    functional: ["persist user session", "rotate keys"]
    non_functional: ["p95<50ms", "error_rate<0.1%"]
    constraints: ["FIPS140-2", "EU-only data"]
@End_Requirements
```

or

```runa
@Requirements:
    functional: [
        "Detect faces in real-time video",
        "Handle multiple faces per frame",
        "Robust to lighting variations",
        "Work with different face orientations"
    ]
    non_functional: [
        "Response time < 50ms",
        "Memory usage < 100MB",
        "CPU usage < 30%",
        "Battery life impact < 5%"
    ]
    constraints: [
        "No internet connectivity required",
        "Must work offline",
        "Compatible with Android/iOS"
    ]
@End_Requirements
```

### 5. Verification and Quality Annotations

#### @Verify Block
Embedded verification conditions.

What this is used for:
- Assert invariants and postconditions that tooling must check.

How to use this:
- Write assertions using canonical operators; avoid side effects.
- Keep fast-running; move heavy checks to @TestCases.

Example (ideal structure):
```runa
@Verify:
    Assert cache_size is less than or equal to capacity
    Assert ttl is greater than 0
@End_Verify
```

or

```runa
@Verify:
    Assert result is not None
    Assert length of result is greater than 0
    Assert all items in result satisfy validation_criteria
    Assert response_time is less than 100 # milliseconds
    Assert memory_usage is less than 50_000_000 # bytes
@End_Verify

Process called "ProcessUserData" that takes user_input:
    # Implementation with automatic verification
    Let processed_data be transform_input with data as user_input
    Return processed_data
```

#### @TestCases Block
Comprehensive test specifications.

What this is used for:
- Define unit/integration/performance tests that CI can materialize.

How to use this:
- Provide names, inputs, expected outputs, and time/memory budgets where relevant.

Example (ideal structure):
```runa
@TestCases:
    unit_tests: [
        { "name": "hit", "input": ["k"], "prepare": "put(""k"",1)", "expected_output": 1 },
        { "name": "miss", "input": ["z"], "expected_output": null }
    ]
@End_TestCases
```

or

```runa
@TestCases:
    unit_tests: [
        {
            "name": "test_empty_input",
            "input": [],
            "expected_output": [],
            "expected_time": "< 1ms"
        },
        {
            "name": "test_large_dataset",
            "input": "generate_large_dataset(10000)",
            "expected_output": "sorted_dataset",
            "expected_time": "< 100ms"
        }
    ]
    integration_tests: [
        {
            "name": "test_end_to_end_workflow",
            "setup": "initialize_test_environment()",
            "steps": ["load_data", "process_data", "save_results"],
            "assertions": ["data_integrity", "performance_metrics"]
        }
    ]
    performance_tests: [
        {
            "metric": "throughput",
            "target": "> 1000 requests/second",
            "load_pattern": "gradual_increase"
        }
    ]
@End_TestCases
```

### 6. Resource and Security Annotations

#### @Resource_Constraints Block
Specifies computational and memory limitations.

What this is used for:
- Bound resource usage of an operation to protect SLAs and budgets.

How to use this:
- Prefer explicit units; set max iterations/timeouts; pair with @Execution_Model when needed.

Example (ideal structure):
```runa
@Resource_Constraints:
    memory_limit: "256MB"
    cpu_limit: "2 cores"
    execution_timeout: "30 seconds"
@End_Resource_Constraints
```
or

```runa
@Resource_Constraints:
    memory_limit: "256MB"
    cpu_limit: "2 cores"
    execution_timeout: "30 seconds"
    disk_space: "10MB"
    network_bandwidth: "1Mbps"
    optimize_for: "memory"  # or "speed", "battery", "accuracy"
    max_iterations: 10000
    cache_size: "64MB"
@End_Resource_Constraints
```

#### @Security_Scope Block
Defines security capabilities and restrictions.

What this is used for:
- Declare least-privilege capabilities and forbidden actions for code paths.

How to use this:
- List positive capabilities first, then forbidden; specify sandbox level and auditing.

Example (ideal structure):
```runa
@Security_Scope:
    capabilities: ["file.read", "crypto.hash"]
    forbidden: ["net.access"]
    sandbox_level: "strict"
    audit_logging: "detailed"
@End_Security_Scope
```

or

```runa
@Security_Scope:
    capabilities: [
        "file.read",
        "math.compute",
        "memory.local",
        "crypto.hash"
    ]
    forbidden: [
        "net.access",
        "file.write",
        "system.execute",
        "registry.modify"
    ]
    sandbox_level: "strict"
    data_access: "read_only"
    encryption_required: true
    audit_logging: "detailed"
    privilege_level: "user"
@End_Security_Scope
```

### 7. Execution and Performance Annotations

#### @Execution_Model Block
Specifies how code should be executed.

What this is used for:
- Communicate execution mode preferences to runtime/tooling (parallelism, scheduling) under AOTT.

How to use this:
- Choose one mode; specify concurrency and retry policy succinctly; avoid duplicating @Resource_Constraints.

Example (ideal structure):
```runa
@Execution_Model:
    mode: "batch"
    concurrency: "parallel"
    parallelism_level: 4
@End_Execution_Model
```

or

```runa
@Execution_Model:
    mode: "batch"  # or "streaming", "real_time", "interactive"
    concurrency: "parallel"  # or "sequential", "async"
    parallelism_level: 4
    scheduling: "round_robin"
    priority: "normal"  # or "high", "low", "critical"
    retry_policy: "exponential_backoff"
    error_recovery: "graceful_degradation"
    monitoring: "detailed"
@End_Execution_Model
```

#### @Performance_Hints Block
Optimization guidance for implementation.

What this is used for:
- Inform compilers/agents about safe optimizations and thresholds.

How to use this:
- Keep hints orthogonal to correctness; avoid mandatory semantics here (use @Implementation/@Requirements).

Example (ideal structure):
```runa
@Performance_Hints:
    cache_strategy: "aggressive"
    vectorization: "enabled"
    parallel_threshold: 1000
@End_Performance_Hints
```

or

```runa
@Performance_Hints:
    cache_strategy: "aggressive"  # or "conservative", "adaptive"
    vectorization: "enabled"
    memory_layout: "contiguous"
    parallel_threshold: 1000
    batch_size: 32
    prefetch_enabled: true
    compression: "enabled"
    hot_path_optimization: ["search", "sort", "filter"]
@End_Performance_Hints
```

### 8. Communication Flow Annotations

#### @Progress Block
Real-time progress reporting for development tracking.

What this is used for:
- Report status for agents and reviewers; enable dashboards and alerts.

How to use this:
- Update incrementally; keep blockers and confidence current; avoid marketing language.

Example (ideal structure):
```runa
@Progress:
    completion_percentage: 40
    current_milestone: "API complete"
    next_milestone: "Benchmarking"
    blockers: ["missing fixtures"]
@End_Progress
```

or

```runa
@Progress:
    completion_percentage: 75
    current_milestone: "Algorithm implementation completed"
    next_milestone: "Unit testing and optimization"
    estimated_time_remaining: "2 hours"
    blockers: []
    intermediate_results: {
        "tests_passing": 45,
        "code_coverage": "87%",
        "performance_baseline": "85ms average response time"
    }
    confidence_level: 0.9
@End_Progress
```

### 9. Translation and Target-Specific Annotations

#### @Translation_Note Block
Language-specific implementation guidance.

What this is used for:
- Capture target-language adaptations without changing core semantics.

How to use this:
- List supported targets and per-target notes; avoid prescribing global policy.

Example (ideal structure):
```runa
@Translation_Note:
    target_languages: ["Python", "Rust"]
    platform_specific: { "Python": "use asyncio" }
    performance_considerations: { "Rust": "prefer iterators over indexing" }
@End_Translation_Note
```

or

```runa
@Translation_Note:
    target_languages: ["Python", "JavaScript", "Java", "C++"]
    critical_feature: "Asynchronous processing"
    platform_specific: {
        "Python": "Use asyncio with proper event loop management",
        "JavaScript": "Use Promises with async/await syntax",
        "Java": "Use CompletableFuture with proper thread pool",
        "C++": "Use std::async with future objects"
    }
    performance_considerations: {
        "Python": "Consider using multiprocessing for CPU-bound tasks",
        "JavaScript": "Use Web Workers for heavy computations",
        "Java": "Optimize garbage collection settings",
        "C++": "Use move semantics for large objects"
    }
    compatibility_notes: {
        "Python": "Requires Python 3.8+ for proper asyncio support",
        "JavaScript": "Requires ES2017+ for async/await",
        "Java": "Requires Java 8+ for CompletableFuture",
        "C++": "Requires C++11+ for std::async"
    }
@End_Translation_Note
```

### 10. Error Handling and Recovery Annotations

#### @Error_Handling Block
Comprehensive error management strategy.

What this is used for:
- Define error models, recovery paths, and user impact explicitly.

How to use this:
- Enumerate expected errors with probabilities; state fallback behavior and notification policy.

Example (ideal structure):
```runa
@Error_Handling:
    expected_errors: [ { "type": "NetworkTimeout", "recovery": "retry" } ]
    fallback_behavior: "return_cached_result"
    user_notification: "user_friendly_messages"
@End_Error_Handling
```

or

```runa
@Error_Handling:
    strategy: "graceful_degradation"
    expected_errors: [
        {
            "type": "NetworkTimeout",
            "probability": 0.05,
            "recovery": "retry_with_exponential_backoff",
            "max_retries": 3
        },
        {
            "type": "InvalidInput",
            "probability": 0.1,
            "recovery": "sanitize_and_retry",
            "fallback": "use_default_values"
        }
    ]
    fallback_behavior: "return_cached_result"
    error_reporting: "detailed_logging"
    monitoring_alerts: "critical_errors_only"
    user_notification: "user_friendly_messages"
@End_Error_Handling
```

## Advanced Communication Patterns

### Multi-Agent Collaboration

### Iterative Refinement

#### @Iteration Block
Support for iterative development cycles.

What this is used for:
- Coordinate multi-step improvement loops with explicit success criteria.

How to use this:
- Link to previous feedback; keep cycle_number monotonic; update next plan based on measured outcomes.

Example (ideal structure):
```runa
@Iteration:
    cycle_number: 4
    previous_feedback: ["memory spike under load"]
    current_focus: "profile allocations"
    success_criteria: ["peak RSS < 200MB"]
    next_iteration_plan: "switch to arena allocator"
@End_Iteration
```

or

```runa
@Iteration:
    cycle_number: 3
    previous_feedback: [
        "Algorithm too slow for real-time requirements",
        "Memory usage exceeds constraints",
        "Edge cases not properly handled"
    ]
    current_focus: "Performance optimization while maintaining accuracy"
    success_criteria: [
        "Response time < 50ms",
        "Memory usage < 100MB",
        "Accuracy > 95%"
    ]
    next_iteration_plan: "Add comprehensive error handling and edge case coverage"
@End_Iteration
```

## Protocol Implementation Guidelines

### For Hub AI Systems

1. **Clear Intent Expression**: Use reasoning blocks to explain decision rationale
2. **Comprehensive Task Specification**: Provide complete requirements and constraints
3. **Uncertainty Acknowledgment**: Explicitly state confidence levels and alternatives
4. **Context Provision**: Include all relevant environmental and business context
5. **Verification Criteria**: Define clear success and failure conditions

### For Spoke AI Systems

1. **Implementation Fidelity**: Preserve all semantic meaning from Brain annotations
2. **Progress Reporting**: Regular updates on implementation status and challenges
3. **Clarification Requests**: Proactive requests for missing information
4. **Alternative Suggestions**: Propose alternatives when constraints cannot be met
5. **Quality Assurance**: Include verification blocks in implementation

### For Translation Systems

1. **Annotation Preservation**: Maintain all annotations in target language comments
2. **Semantic Mapping**: Ensure target language idioms preserve original intent
3. **Performance Characteristics**: Adapt performance hints to target platform
4. **Error Handling**: Translate error handling patterns to target language conventions

## Example: Complete Communication Flow

```runa
# Brain -> Hat Communication
@Task:
    objective: "Implement user authentication system"
    constraints: ["Secure", "Fast", "User-friendly"]
    target_language: "Python"
    deadline: "3 days"
@End_Task

@Reasoning:
    Using JWT tokens for stateless authentication because:
    1. Scalable across multiple servers
    2. No server-side session storage required
    3. Industry standard with good library support
    4. Includes expiration and claims
@End_Reasoning

@Security_Scope:
    capabilities: ["crypto.hash", "crypto.jwt", "database.read", "database.write"]
    forbidden: ["file.system", "network.external"]
    encryption_required: true
    audit_logging: "enabled"
@End_Security_Scope

@Requirements:
    functional: [
        "User login with email/password",
        "Token generation and validation",
        "Password hashing with salt",
        "Token refresh mechanism"
    ]
    non_functional: [
        "Authentication time < 200ms",
        "Tokens expire in 1 hour",
        "Refresh tokens expire in 30 days",
        "Secure password storage"
    ]
@End_Requirements

# Implementation Example
@Implementation:
    Process called "authenticate_user" that takes email and password:
        @Verify:
            Assert email is not None
            Assert password is not None
            Assert email contains "@"
        @End_Verify
        
        Let user be find_user_by_email with email as email
        If user is None:
            Return AuthResult.failure with message "Invalid credentials"
        
        Let password_valid be verify_password with 
            password as password and 
            hash as user.password_hash
        
        If not password_valid:
            Return AuthResult.failure with message "Invalid credentials"
        
        Let token be generate_jwt_token with user_id as user.id
        Return AuthResult.success with token as token
@End_Implementation

@Progress:
    completion_percentage: 90
    current_milestone: "Core authentication implemented"
    next_milestone: "Token refresh mechanism"
    intermediate_results: {
        "unit_tests_passing": 12,
        "integration_tests_passing": 3,
        "performance_benchmark": "Average 150ms authentication time"
    }
@End_Progress


```

## Best Practices

### Annotation Density
- **High-Level Functions**: Rich annotations with reasoning and context
- **Utility Functions**: Minimal annotations focusing on verification
- **Critical Paths**: Comprehensive annotations including performance and security
- **Experimental Code**: Heavy use of uncertainty and progress annotations

### Consistency Guidelines
- Use consistent terminology across all annotations
- Maintain annotation style within project boundaries
- Follow semantic versioning for annotation schema evolution
- Document project-specific annotation conventions

### Performance Considerations
- Annotations are compile-time only and have no runtime overhead
- Use structured annotations for tool processing
- Keep free-text annotations concise but informative
- Balance annotation density with code readability

### Security and Privacy
- Never include sensitive data in annotations
- Use references rather than embedding confidential information
- Ensure annotations don't leak implementation details inappropriately
- Consider annotation visibility in shared codebases

## Tooling and Ecosystem

### Annotation Processors
- **Static Analysis**: Extract and validate annotation consistency
- **Documentation Generation**: Auto-generate docs from annotations
- **Code Quality Metrics**: Measure annotation coverage and quality
- **Translation Validation**: Verify annotation preservation across languages

### IDE Integration
- **Syntax Highlighting**: Special highlighting for annotation blocks
- **Auto-completion**: Suggest annotation templates and values
- **Validation**: Real-time checking of annotation syntax and semantics
- **Navigation**: Jump between related annotations and implementations

### AI Training Data
- **Corpus Generation**: Use annotated code for training AI models
- **Pattern Recognition**: Learn common annotation patterns
- **Quality Assessment**: Measure annotation effectiveness
- **Evolution Tracking**: Monitor annotation usage over time

This protocol represents a fundamental advancement in AI-assisted development, enabling enhanced code documentation, reasoning, and intelligent analysis while maintaining semantic fidelity and preserving human oversight capabilities.

## Open Issues

1. Finalize payload schemas and validation rules per annotation category with error codes.
2. Define precedence/merging rules across nested scopes with concrete examples.
3. Complete parser routing for reserved blocks and ensure round-trip in tooling.
---

# Dependency Management


**Version:** 1.0
**Status:** Canonical
**Last Updated:** 2025-10-08

---

## Overview

**Runa replaces all package management files:**
- ❌ package.json, package-lock.json (npm)
- ❌ requirements.txt, Pipfile (Python)
- ❌ Cargo.toml, Cargo.lock (Rust)
- ❌ go.mod, go.sum (Go)
- ❌ Gemfile, Gemfile.lock (Ruby)
- ❌ build.gradle, pom.xml (Java)

---

## Basic Dependency File

**File:** `dependencies.runa`

```runa
Note: Project dependencies
Note: Replaces package.json, requirements.txt, Cargo.toml, etc.

Import "runa/package" as Package

Type called "Dependency":
    name as String
    version as String
    source as String  Note: "registry", "git", "path"
    url as String
End Type

Type called "ProjectDependencies":
    name as String
    version as String
    dependencies as List[Dependency]
    dev_dependencies as List[Dependency]
End Type

Process called "define_dependencies" returns ProjectDependencies:
    Return a value of type ProjectDependencies with
        name as "MyApp",
        version as "1.0.0",
        dependencies as a list containing:
            dep("runa-stdlib", "1.0.0", "registry"),
            dep("runa-http", "2.1.0", "registry"),
            dep("runa-database", "1.5.3", "registry")
        End,
        dev_dependencies as a list containing:
            dep("runa-test", "1.0.0", "registry"),
            dep("runa-lint", "0.9.0", "registry")
        End
End Process

Process called "dep" that takes name as String, version as String, source as String returns Dependency:
    Return a value of type Dependency with
        name as name,
        version as version,
        source as source,
        url as ""
End Process

Let PROJECT_DEPS be define_dependencies()
```

**Usage:**
```bash
# Install dependencies
runa install dependencies.runa

# Update dependencies
runa update dependencies.runa
```

---

## Version Constraints

```runa
Process called "define_with_constraints" returns List[Dependency]:
    Return a list containing:
        Note: Exact version
        dep("package-a", "1.0.0", "registry"),

        Note: Semantic versioning
        dep("package-b", "^2.1.0", "registry"),  Note: >= 2.1.0, < 3.0.0
        dep("package-c", "~1.5.0", "registry"),  Note: >= 1.5.0, < 1.6.0

        Note: Git repository
        dep_git("package-d", "main", "https://github.com/user/package-d"),

        Note: Local path
        dep_path("local-lib", "../local-lib")
    End
End Process

Process called "dep_git" that takes name as String, branch as String, url as String returns Dependency:
    Return a value of type Dependency with
        name as name,
        version as branch,
        source as "git",
        url as url
End Process

Process called "dep_path" that takes name as String, path as String returns Dependency:
    Return a value of type Dependency with
        name as name,
        version as "local",
        source as "path",
        url as path
End Process
```

---

## Lockfile Generation

**File:** `dependencies.lock.runa` (auto-generated)

```runa
Note: Dependency lockfile (auto-generated)
Note: Replaces package-lock.json, Cargo.lock, go.sum, etc.
Note: DO NOT EDIT MANUALLY

Type called "LockedDependency":
    name as String
    version as String
    resolved_url as String
    integrity_hash as String
    dependencies as List[String]
End Type

Let LOCKED_DEPENDENCIES be a list containing:
    locked("runa-stdlib", "1.0.0", "https://registry.runa.dev/stdlib-1.0.0.tar.gz", "sha256:abc123..."),
    locked("runa-http", "2.1.0", "https://registry.runa.dev/http-2.1.0.tar.gz", "sha256:def456..."),
    locked("runa-database", "1.5.3", "https://registry.runa.dev/database-1.5.3.tar.gz", "sha256:ghi789...")
End

Process called "locked" that takes name as String, version as String, url as String, hash as String returns LockedDependency:
    Return a value of type LockedDependency with
        name as name,
        version as version,
        resolved_url as url,
        integrity_hash as hash,
        dependencies as an empty list
End Process
```

---

## Comparison: package.json vs dependencies.runa

**Before (package.json):**
```json
{
  "name": "myapp",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.0",
    "mongoose": "^6.5.0"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  },
  "scripts": {
    "start": "node index.js",
    "test": "jest"
  }
}
```

**After (dependencies.runa):**
```runa
Type called "ProjectConfig":
    name as String
    version as String
    dependencies as List[Dependency]
    dev_dependencies as List[Dependency]
    scripts as Dictionary[String, String]
End Type

Process called "load_config" returns ProjectConfig:
    Return a value of type ProjectConfig with
        name as "myapp",
        version as "1.0.0",
        dependencies as a list containing:
            dep("runa-express", "^4.18.0", "registry"),
            dep("runa-mongoose", "^6.5.0", "registry")
        End,
        dev_dependencies as a list containing:
            dep("runa-jest", "^29.0.0", "registry")
        End,
        scripts as a dictionary containing:
            "start" as "runa index.runa",
            "test" as "runa test.runa"
        End Dictionary
End Process

Let CONFIG be load_config()
```

---

## Workspace/Monorepo Support

**File:** `workspace.runa`

```runa
Note: Workspace configuration for monorepo
Note: Replaces npm workspaces, Cargo workspace, etc.

Type called "WorkspaceConfig":
    name as String
    members as List[String]
    shared_dependencies as List[Dependency]
End Type

Process called "define_workspace" returns WorkspaceConfig:
    Return a value of type WorkspaceConfig with
        name as "MyMonorepo",
        members as a list containing:
            "packages/core",
            "packages/ui",
            "packages/api",
            "apps/web",
            "apps/mobile"
        End,
        shared_dependencies as a list containing:
            dep("runa-stdlib", "1.0.0", "registry")
        End
End Process

Let WORKSPACE be define_workspace()
```

---

## Dependency Scripts

```runa
Process called "install_dependencies":
    Let deps be PROJECT_DEPS

    Display "Installing " joined with string_from(length of deps.dependencies) joined with " dependencies..."

    For Each dep in deps.dependencies:
        Display "  Installing: " joined with dep.name joined with "@" joined with dep.version
        proc Package.install with dep
    End For

    Display "✓ Dependencies installed"
End Process

Process called "update_dependencies":
    Let deps be PROJECT_DEPS

    For Each dep in deps.dependencies:
        Let latest_version be Package.get_latest_version with dep.name

        If latest_version is not dep.version:
            Display "Updating " joined with dep.name joined with ": " joined with dep.version joined with " → " joined with latest_version
            proc Package.update with dep.name, latest_version
        End If
    End For

    Display "✓ Dependencies updated"
End Process

Process called "audit_dependencies":
    Display "Auditing dependencies for vulnerabilities..."

    Let vulnerabilities be Package.audit

    If length of vulnerabilities is 0:
        Display "✓ No vulnerabilities found"
    Otherwise:
        For Each vuln in vulnerabilities:
            Display "⚠ " joined with vuln.package joined with ": " joined with vuln.description
        End For

        proc panic with "Vulnerabilities found"
    End If
End Process
```

---

## Summary

**Runa replaces package management with:**
- ✅ Type-safe dependency declarations
- ✅ Unified syntax across all ecosystems
- ✅ Automatic lockfile generation
- ✅ Version constraint validation
- ✅ Workspace/monorepo support

**Stop using:** package.json, requirements.txt, Cargo.toml, etc.
**Start using:** `dependencies.runa`

---

**End of Document**
