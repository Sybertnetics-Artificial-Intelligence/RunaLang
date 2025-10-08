# Runa Build System Specification

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
        Call remove_directory_recursive(BUILD_DIR)
    End If

    Call display("✓ Cleaned build artifacts")
End Process

@Implementation:
  Compile all source files to executables.
@End Implementation

Process called "compile":
    Note: Ensure build directory exists
    If not directory_exists(BUILD_DIR):
        Call create_directory(BUILD_DIR)
    End If

    Note: Compile all .runa files in src/
    Let source_files be find_files(SOURCE_DIR, "*.runa")

    For Each source_file in source_files:
        Let output_file be BUILD_DIR + "/" + basename(source_file) + ".o"
        Call display("Compiling " + source_file + "...")
        Call compile_runa_file(source_file, output_file)
    End For

    Call display("✓ Compilation complete")
End Process

@Implementation:
  Run all tests in the test directory.
@End Implementation

Process called "test":
    Note: Ensure project is compiled first
    Call compile()

    Note: Run all test files
    Let test_files be find_files(TEST_DIR, "test_*.runa")

    Let passed be 0
    Let failed be 0

    For Each test_file in test_files:
        Call display("Running " + test_file + "...")
        Let result be run_test_file(test_file)

        If result is "PASS":
            Set passed to passed + 1
        Otherwise:
            Set failed to failed + 1
        End If
    End For

    Call display("✓ Tests: " + string_from(passed) + " passed, " + string_from(failed) + " failed")

    If failed > 0:
        Call panic("Tests failed")
    End If
End Process

@Implementation:
  Build the final executable.
@End Implementation

Process called "build":
    Note: Clean and compile
    Call clean()
    Call compile()

    Note: Link all object files
    Call display("Linking executable...")
    Call link_executable(PROJECT_NAME, BUILD_DIR)

    Call display("✓ Build complete: " + BUILD_DIR + "/" + PROJECT_NAME)
End Process

@Implementation:
  Full build + tests (default task).
@End Implementation

Process called "all":
    Call build()
    Call test()
    Call display("✓ Build and test complete")
End Process

Note: ============================================
Note: TASK REGISTRY
Note: ============================================

Process called "main":
    Note: Parse command line arguments
    Let args be get_command_line_arguments()

    If length of args is 0:
        Note: Default task
        Call all()
        Return
    End If

    Let task_name be args at index 0

    Note: Dispatch to task
    If task_name is "clean":
        Call clean()
    Otherwise if task_name is "compile":
        Call compile()
    Otherwise if task_name is "test":
        Call test()
    Otherwise if task_name is "build":
        Call build()
    Otherwise if task_name is "all":
        Call all()
    Otherwise:
        Call display("Unknown task: " + task_name)
        Call display("Available tasks: clean, compile, test, build, all")
        Call exit_with_code(1)
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
            Call create_directory(dir)
            Call display("Created directory: " + dir)
        End If
    End For
End Process

Process called "copy_resources":
    Note: Copy static resources to build directory

    Let resource_files be find_files("resources", "*")

    For Each resource in resource_files:
        Let dest be "build/resources/" + basename(resource)
        Call copy_file(resource, dest)
        Call display("Copied: " + resource)
    End For
End Process
```

### Compilation Tasks

```runa
Process called "compile_source_files" that takes source_dir as String, output_dir as String:
    Note: Compile all .runa files in directory

    Let source_files be find_files(source_dir, "*.runa")

    For Each source_file in source_files:
        Let relative_path be remove_prefix(source_file, source_dir)
        Let output_file be output_dir + "/" + relative_path + ".o"

        Note: Create output directory if needed
        Let output_dir_path be directory_name(output_file)
        If not directory_exists(output_dir_path):
            Call create_directory_recursive(output_dir_path)
        End If

        Note: Check if recompilation needed (incremental build)
        Let needs_rebuild be true

        If file_exists(output_file):
            Let source_time be file_modified_time(source_file)
            Let output_time be file_modified_time(output_file)

            If output_time >= source_time:
                Set needs_rebuild to false
            End If
        End If

        If needs_rebuild:
            Call display("Compiling: " + source_file)
            Call compile_runa_file(source_file, output_file)
        Otherwise:
            Call display("Skipping (up to date): " + source_file)
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
        Call execute_task(graph, dep)
    End For

    Note: Execute task
    Call display("Running task: " + task_name)
    Call task.action()

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
    Let graph be define_build_graph()
    Let args be get_command_line_arguments()

    Let task_name be if length of args > 0 then args at index 0 otherwise "package"

    Call execute_task(graph, task_name)
    Call display("✓ Task complete: " + task_name)
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
    Call display("=== Stage 1: Compiling Standard Library ===")

    Let stdlib_sources be find_files("stdlib", "*.runa")

    For Each source in stdlib_sources:
        Let output be "build/stdlib/" + basename(source) + ".o"
        Call compile_runa_file(source, output)
    End For

    Call display("✓ Standard library compiled")
End Process

Process called "stage2_compile_application":
    Call display("=== Stage 2: Compiling Application ===")

    Note: Ensure stdlib is compiled first
    Call stage1_compile_stdlib()

    Let app_sources be find_files("src", "*.runa")

    For Each source in app_sources:
        Let output be "build/app/" + basename(source) + ".o"
        Call compile_runa_file(source, output)
    End For

    Call display("✓ Application compiled")
End Process

Process called "stage3_link_executable":
    Call display("=== Stage 3: Linking Executable ===")

    Note: Ensure application is compiled first
    Call stage2_compile_application()

    Note: Collect all object files
    Let stdlib_objects be find_files("build/stdlib", "*.o")
    Let app_objects be find_files("build/app", "*.o")

    Let all_objects be concatenate_lists(stdlib_objects, app_objects)

    Note: Link final executable
    Call link_executable("myapp", all_objects, "build/bin/myapp")

    Call display("✓ Executable created: build/bin/myapp")
End Process

Process called "build":
    Call stage3_link_executable()
    Call display("✓ Full build complete")
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
    Let test_files be find_files("tests", "test_*.runa")
    Let results be an empty list of TestResults

    For Each test_file in test_files:
        Let test_name be basename(test_file)
        Call display("Running: " + test_name)

        Let start_time be current_time_milliseconds()

        Let result be a value of type TestResult with
            test_name as test_name,
            status as "PASS",
            duration_ms as 0,
            error_message as ""

        Note: Run test and capture result
        Let test_output be run_test_file_with_capture(test_file)

        Let end_time be current_time_milliseconds()
        Set result.duration_ms to end_time - start_time

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
        Set total_duration to total_duration + result.duration_ms

        If result.status is "PASS":
            Set passed to passed + 1
            Call display("  ✓ " + result.test_name + " (" + string_from(result.duration_ms) + "ms)")
        Otherwise:
            Set failed to failed + 1
            Call display("  ✗ " + result.test_name + " (" + string_from(result.duration_ms) + "ms)")
            Call display("    Error: " + result.error_message)
        End If
    End For

    Call display("")
    Call display("=== Test Summary ===")
    Call display("Total: " + string_from(length of results))
    Call display("Passed: " + string_from(passed))
    Call display("Failed: " + string_from(failed))
    Call display("Duration: " + string_from(total_duration) + "ms")

    If failed > 0:
        Call panic("Tests failed")
    End If
End Process

Process called "test":
    Call display("=== Running Test Suite ===")
    Let results be run_all_tests()
    Call display_test_summary(results)
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
    Call display("=== Creating Deployment Package ===")

    Note: Ensure build is complete
    Call build()

    Note: Create package directory
    Let package_dir be "build/package"
    If directory_exists(package_dir):
        Call remove_directory_recursive(package_dir)
    End If
    Call create_directory(package_dir)

    Note: Copy executable
    Call copy_file("build/bin/myapp", package_dir + "/myapp")

    Note: Copy resources
    Call copy_directory_recursive("resources", package_dir + "/resources")

    Note: Copy configuration
    Call copy_file("config.runa", package_dir + "/config.runa")

    Note: Create archive
    Let version be get_project_version()
    Let archive_name be "myapp-" + version + ".tar.gz"

    Call create_archive(package_dir, "build/" + archive_name)

    Call display("✓ Package created: build/" + archive_name)
End Process

@Implementation:
  Deploy package to remote server.
@End Implementation

Process called "deploy" that takes environment as String:
    Call display("=== Deploying to " + environment + " ===")

    Note: Ensure package is created
    Call package()

    Note: Get deployment configuration
    Let config be load_deployment_config(environment)

    Note: Upload package
    Let version be get_project_version()
    Let archive_name be "myapp-" + version + ".tar.gz"

    Call display("Uploading to " + config.server + "...")
    Call scp_upload("build/" + archive_name, config.server, config.deploy_path)

    Note: Extract on remote server
    Call display("Extracting on remote server...")
    Call ssh_execute(config.server, "tar -xzf " + config.deploy_path + "/" + archive_name)

    Note: Restart service
    Call display("Restarting service...")
    Call ssh_execute(config.server, "systemctl restart myapp")

    Call display("✓ Deployment complete")
End Process

Process called "deploy_staging":
    Call deploy("staging")
End Process

Process called "deploy_production":
    Note: Require confirmation for production
    Call display("WARNING: Deploying to PRODUCTION")
    Call display("Type 'yes' to confirm:")

    Let confirmation be read_line_from_stdin()

    If confirmation is not "yes":
        Call display("Deployment cancelled")
        Return
    End If

    Call deploy("production")
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
    Call display("=== Parallel Compilation ===")

    Let tasks be an empty list

    Note: Create compilation task for each directory
    For Each dir in source_dirs:
        Let task be create_async_task(compile_directory, dir)
        Add task to tasks
    End For

    Note: Wait for all tasks to complete
    For Each task in tasks:
        Call wait_for_task(task)
    End For

    Call display("✓ Parallel compilation complete")
End Process

Process called "compile_directory" that takes dir as String:
    Let sources be find_files(dir, "*.runa")

    For Each source in sources:
        Call compile_runa_file(source, "build/" + source + ".o")
    End For
End Process
```

### Conditional Builds

```runa
@Implementation:
  Conditional compilation based on platform or features.
@End Implementation

Process called "build_for_platform":
    Let platform be get_current_platform()

    Call display("Building for platform: " + platform)

    If platform is "linux":
        Call compile_with_flags("src", "build", "-DLINUX")
    Otherwise if platform is "windows":
        Call compile_with_flags("src", "build", "-DWINDOWS")
    Otherwise if platform is "macos":
        Call compile_with_flags("src", "build", "-DMACOS")
    Otherwise:
        Call panic("Unsupported platform: " + platform)
    End If
End Process

Process called "build_with_features" that takes features as List[String]:
    Call display("Building with features: " + join(features, ", "))

    Let flags be ""

    For Each feature in features:
        Set flags to flags + " -DFEATURE_" + uppercase(feature)
    End For

    Call compile_with_flags("src", "build", flags)
End Process
```

### Watch and Rebuild

```runa
@Implementation:
  Watch source files and rebuild on changes.
@End Implementation

Process called "watch":
    Call display("=== Watching for changes ===")
    Call display("Press Ctrl+C to stop")

    Let last_build_time be current_time_milliseconds()

    While true:
        Note: Check if any source files changed
        Let source_files be find_files("src", "*.runa")
        Let needs_rebuild be false

        For Each source in source_files:
            Let modified_time be file_modified_time(source)

            If modified_time > last_build_time:
                Set needs_rebuild to true
                Break
            End If
        End For

        If needs_rebuild:
            Call display("Changes detected, rebuilding...")
            Call build()
            Set last_build_time to current_time_milliseconds()
            Call display("✓ Rebuild complete. Watching...")
        End If

        Note: Sleep before checking again
        Call sleep_milliseconds(1000)
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
        Call remove_directory_recursive(BUILD_DIR)
    End If
End Process

Process called "compile":
    Let sources be find_files(SOURCE_DIR, "*.runa")

    For Each source in sources:
        Let output be BUILD_DIR + "/" + basename(source) + ".o"
        Call compile_runa_file(source, output)
    End For
End Process

Process called "build":
    Call compile()
    Call link_executable("myapp", BUILD_DIR)
End Process

Process called "test":
    Call build()
    Call run_test_suite()
End Process

Process called "all":
    Call build()
    Call test()
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
    Call compile_typescript()
    Call run_webpack()
End Process

Process called "test":
    Call run_jest_tests()
End Process

Process called "clean":
    If directory_exists("build"):
        Call remove_directory_recursive("build")
    End If
End Process

Process called "deploy":
    Call build()

    Let config be load_deploy_config()
    Call scp_upload("build", config.server, config.path)
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
        Call FS.create_directory_recursive(path)
    End If
End Process

Process called "get_timestamp" returns String:
    Let time be Proc.current_time_milliseconds()
    Return string_from(time)
End Process

Note: ============================================
Note: CLEAN TASK
Note: ============================================

@Implementation:
  Remove all build artifacts and temporary files.
@End Implementation

Process called "clean":
    Call display("🧹 Cleaning build artifacts...")

    If FS.directory_exists(BUILD_DIR):
        Call FS.remove_directory_recursive(BUILD_DIR)
    End If

    Note: Remove temporary files
    Let temp_files be FS.find_files(".", "*.tmp")
    For Each temp_file in temp_files:
        Call FS.remove_file(temp_file)
    End For

    Call display("✓ Clean complete")
End Process

Note: ============================================
Note: SETUP TASK
Note: ============================================

@Implementation:
  Create build directory structure.
@End Implementation

Process called "setup":
    Call display("📁 Setting up build directories...")

    Let directories be a list containing:
        BUILD_DIR,
        BUILD_DIR + "/stdlib",
        BUILD_DIR + "/app",
        BUILD_DIR + "/bin",
        BUILD_DIR + "/tests"

    For Each dir in directories:
        Call ensure_directory(dir)
    End For

    Call display("✓ Setup complete")
End Process

Note: ============================================
Note: COMPILATION TASKS
Note: ============================================

@Implementation:
  Compile standard library.
@End Implementation

Process called "compile_stdlib":
    Call display("📚 Compiling standard library...")

    Let stdlib_sources be FS.find_files(STDLIB_DIR, "*.runa")
    Let compiled be 0

    For Each source in stdlib_sources:
        Let output be BUILD_DIR + "/stdlib/" + FS.basename(source) + ".o"

        Note: Incremental build - check if recompilation needed
        If Build.needs_recompilation(source, output):
            Call display("  Compiling: " + source)
            Call Build.compile_runa_file(source, output)
            Set compiled to compiled + 1
        End If
    End For

    Call display("✓ Standard library compiled (" + string_from(compiled) + " files)")
End Process

@Implementation:
  Compile application source code.
@End Implementation

Process called "compile_app":
    Call display("🔨 Compiling application...")

    Let app_sources be FS.find_files(SOURCE_DIR, "*.runa")
    Let compiled be 0

    For Each source in app_sources:
        Let relative_path be FS.remove_prefix(source, SOURCE_DIR)
        Let output be BUILD_DIR + "/app/" + relative_path + ".o"

        Note: Create output directory
        Let output_dir be FS.directory_name(output)
        Call ensure_directory(output_dir)

        Note: Incremental build
        If Build.needs_recompilation(source, output):
            Call display("  Compiling: " + source)
            Call Build.compile_runa_file(source, output)
            Set compiled to compiled + 1
        End If
    End For

    Call display("✓ Application compiled (" + string_from(compiled) + " files)")
End Process

@Implementation:
  Link final executable.
@End Implementation

Process called "link":
    Call display("🔗 Linking executable...")

    Note: Collect all object files
    Let stdlib_objects be FS.find_files(BUILD_DIR + "/stdlib", "*.o")
    Let app_objects be FS.find_files(BUILD_DIR + "/app", "*.o")

    Let all_objects be concatenate_lists(stdlib_objects, app_objects)

    Note: Link executable
    Let executable_path be BUILD_DIR + "/bin/" + PROJECT_NAME

    Call Build.link_executable(PROJECT_NAME, all_objects, executable_path)

    Call display("✓ Executable created: " + executable_path)
End Process

Note: ============================================
Note: BUILD TASK
Note: ============================================

@Implementation:
  Full build pipeline.
@End Implementation

Process called "build":
    Let start_time be Proc.current_time_milliseconds()

    Call setup()
    Call compile_stdlib()
    Call compile_app()
    Call link()

    Let end_time be Proc.current_time_milliseconds()
    Let duration be end_time - start_time

    Call display("✓ Build complete in " + string_from(duration) + "ms")
End Process

Note: ============================================
Note: TEST TASKS
Note: ============================================

@Implementation:
  Run test suite.
@End Implementation

Process called "test":
    Call display("🧪 Running test suite...")

    Note: Ensure build is up to date
    Call build()

    Let test_files be FS.find_files(TEST_DIR, "test_*.runa")
    Let passed be 0
    Let failed be 0

    For Each test_file in test_files:
        Let test_name be FS.basename(test_file)
        Call display("  Running: " + test_name)

        Let result be Build.run_test_file(test_file)

        If result.status is "PASS":
            Set passed to passed + 1
            Call display("    ✓ PASS (" + string_from(result.duration_ms) + "ms)")
        Otherwise:
            Set failed to failed + 1
            Call display("    ✗ FAIL (" + string_from(result.duration_ms) + "ms)")
            Call display("    " + result.error_message)
        End If
    End For

    Call display("")
    Call display("=== Test Summary ===")
    Call display("Passed: " + string_from(passed))
    Call display("Failed: " + string_from(failed))

    If failed > 0:
        Call panic("Tests failed")
    End If

    Call display("✓ All tests passed")
End Process

Note: ============================================
Note: PACKAGE TASK
Note: ============================================

@Implementation:
  Create deployment package.
@End Implementation

Process called "package":
    Call display("📦 Creating deployment package...")

    Note: Ensure tests pass
    Call test()

    Note: Create package directory
    Let package_dir be BUILD_DIR + "/package"

    If FS.directory_exists(package_dir):
        Call FS.remove_directory_recursive(package_dir)
    End If

    Call FS.create_directory(package_dir)

    Note: Copy executable
    Call FS.copy_file(
        BUILD_DIR + "/bin/" + PROJECT_NAME,
        package_dir + "/" + PROJECT_NAME
    )

    Note: Copy resources
    If FS.directory_exists("resources"):
        Call FS.copy_directory_recursive("resources", package_dir + "/resources")
    End If

    Note: Copy configuration
    Call FS.copy_file("config.runa", package_dir + "/config.runa")

    Note: Create archive
    Let archive_name be PROJECT_NAME + "-" + PROJECT_VERSION + ".tar.gz"
    Call Build.create_archive(package_dir, BUILD_DIR + "/" + archive_name)

    Call display("✓ Package created: " + BUILD_DIR + "/" + archive_name)
End Process

Note: ============================================
Note: DEPLOYMENT TASKS
Note: ============================================

@Implementation:
  Deploy to staging environment.
@End Implementation

Process called "deploy_staging":
    Call display("🚀 Deploying to STAGING...")

    Call package()

    Let config be load_deploy_config("staging")
    Let archive_name be PROJECT_NAME + "-" + PROJECT_VERSION + ".tar.gz"

    Call Build.scp_upload(
        BUILD_DIR + "/" + archive_name,
        config.server,
        config.deploy_path
    )

    Call Build.ssh_execute(config.server, "systemctl restart " + PROJECT_NAME)

    Call display("✓ Deployed to staging")
End Process

@Implementation:
  Deploy to production environment (requires confirmation).
@End Implementation

Process called "deploy_production":
    Call display("🚀 Deploying to PRODUCTION")
    Call display("WARNING: This will deploy to live servers")
    Call display("Type 'yes' to confirm:")

    Let confirmation be Proc.read_line_from_stdin()

    If confirmation is not "yes":
        Call display("Deployment cancelled")
        Return
    End If

    Call package()

    Let config be load_deploy_config("production")
    Let archive_name be PROJECT_NAME + "-" + PROJECT_VERSION + ".tar.gz"

    Call Build.scp_upload(
        BUILD_DIR + "/" + archive_name,
        config.server,
        config.deploy_path
    )

    Call Build.ssh_execute(config.server, "systemctl restart " + PROJECT_NAME)

    Call display("✓ Deployed to production")
End Process

Note: ============================================
Note: MAIN ENTRY POINT
Note: ============================================

Process called "main":
    Let args be Proc.get_command_line_arguments()

    If length of args is 0:
        Call display("Available tasks: clean, build, test, package, deploy-staging, deploy-production")
        Return
    End If

    Let task be args at index 0

    If task is "clean":
        Call clean()
    Otherwise if task is "build":
        Call build()
    Otherwise if task is "test":
        Call test()
    Otherwise if task is "package":
        Call package()
    Otherwise if task is "deploy-staging":
        Call deploy_staging()
    Otherwise if task is "deploy-production":
        Call deploy_production()
    Otherwise:
        Call display("Unknown task: " + task)
        Call display("Available: clean, build, test, package, deploy-staging, deploy-production")
        Call Proc.exit_with_code(1)
    End If
End Process
```

---

## Best Practices

### 1. Use Incremental Builds

```runa
Note: GOOD - Only rebuild what changed
Process called "compile_incremental" that takes source as String, output as String:
    If Build.needs_recompilation(source, output):
        Call Build.compile_runa_file(source, output)
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
        Let task be create_async_task(compile_directory, dir)
        Add task to tasks
    End For

    For Each task in tasks:
        Call wait_for_task(task)
    End For
End Process
```

### 3. Validate Before Deployment

```runa
Note: GOOD - Always test before deploying
Process called "deploy":
    Call test()  Note: Fail fast if tests don't pass
    Call package()
    Call upload_to_server()
End Process
```

### 4. Use Task Dependencies

```runa
Note: GOOD - Explicit dependency graph
Process called "package":
    Call build()  Note: Ensure build is current
    Call test()   Note: Ensure tests pass
    Note: Now safe to package
    Call create_deployment_package()
End Process
```

### 5. Provide Clear Feedback

```runa
Note: GOOD - Show progress and results
Process called "build":
    Call display("🔨 Starting build...")
    Let start_time be current_time_milliseconds()

    Call compile()

    Let end_time be current_time_milliseconds()
    Let duration be end_time - start_time

    Call display("✓ Build complete in " + string_from(duration) + "ms")
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
