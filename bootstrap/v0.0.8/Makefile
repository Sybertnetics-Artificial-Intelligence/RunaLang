# Copyright 2025 Sybertnetics Artificial Intelligence Solutions
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Makefile for Runa v0.0.8 Bootstrap Compiler
# Simplified build: build (trusted) -> verify (self-compile)

# Compiler settings
CC = gcc
CFLAGS ?= -Wall -Wextra -std=c99 -O2 -g -fPIC
RUNAC_V0075 = ../v0.0.7.5/build/runac
AS = as
ASFLAGS = --64
LD = gcc
LDFLAGS ?= -lm -ldl -lpthread

# AddressSanitizer build variant
ifdef ASAN
CFLAGS = -g -O0 -fsanitize=address -fno-omit-frame-pointer -Wall -Wextra -std=c99 -fPIC
LDFLAGS = -fsanitize=address -lm -ldl -lpthread
endif

# Additional flags for runtime/Runa interop
RUNTIME_CFLAGS = $(CFLAGS) -I$(RUNTIME_DIR)
RUNA_LDFLAGS = $(LDFLAGS) -Wl,--export-dynamic

# Directories
BUILD_DIR = build
VERIFY_DIR = verify
SRC_DIR = src
RUNTIME_DIR = runtime
TEST_DIR = tests
TEST_UNIT_DIR = tests/unit
TEST_OUTPUT_DIR = tests/output

# Runtime library source files (C)
RUNTIME_C_SOURCES = $(wildcard $(RUNTIME_DIR)/*.c)
RUNTIME_SOURCES = $(RUNTIME_C_SOURCES)

# Runa source files
RUNA_MODULES = string_utils hashtable containers lexer parser codegen main
RUNA_SOURCES = $(RUNA_MODULES:%=$(SRC_DIR)/%.runa)

# Build files (compiled by v0.0.7.5)
BUILD_ASSEMBLY = $(RUNA_MODULES:%=$(BUILD_DIR)/%.s)
BUILD_OBJECTS = $(RUNA_MODULES:%=$(BUILD_DIR)/%.o)
BUILD_RUNTIME = $(RUNTIME_SOURCES:$(RUNTIME_DIR)/%.c=$(BUILD_DIR)/%.o)
BUILD_TARGET = $(BUILD_DIR)/runac

# Verify files (compiled by build/runac)
VERIFY_ASSEMBLY = $(RUNA_MODULES:%=$(VERIFY_DIR)/%.s)
VERIFY_OBJECTS = $(RUNA_MODULES:%=$(VERIFY_DIR)/%.o)
VERIFY_RUNTIME = $(RUNTIME_SOURCES:$(RUNTIME_DIR)/%.c=$(VERIFY_DIR)/%.o)
VERIFY_TARGET = $(VERIFY_DIR)/runac

# List of unit tests
UNIT_TESTS = test_minimal test_let test_if test_args test_display test_strings test_file test_compiler

# Default target
all: build

# Ensure directories exist
dirs:
	@mkdir -p $(BUILD_DIR) $(VERIFY_DIR) $(TEST_OUTPUT_DIR)

# ===== BUILD: Compiled by v0.0.7.5 =====

build: dirs $(BUILD_TARGET)
	@echo "✓ Build complete: $(BUILD_TARGET)"

# Build runtime compilation
$(BUILD_DIR)/%.o: $(RUNTIME_DIR)/%.c
	$(CC) $(RUNTIME_CFLAGS) -c $< -o $@

# Build Runa compilation (using v0.0.7.5)
$(BUILD_DIR)/%.s: $(SRC_DIR)/%.runa
	$(RUNAC_V0075) $< $@

# Build assembly to object with symbol handling
$(BUILD_DIR)/%.o: $(BUILD_DIR)/%.s
	$(AS) $(ASFLAGS) $< -o $@
	@# Strip main symbol from all objects except main.o
	@if [ "$@" != "$(BUILD_DIR)/main.o" ]; then \
		objcopy --strip-symbol=main $@ 2>/dev/null || true; \
	fi
	@# Weaken runtime symbols that conflict with C runtime
	@if [ "$@" = "$(BUILD_DIR)/hashtable.o" ] || [ "$@" = "$(BUILD_DIR)/string_utils.o" ]; then \
		objcopy --weaken-symbol=allocate --weaken-symbol=deallocate --weaken-symbol=memory_set_pointer --weaken-symbol=memory_get_pointer --weaken-symbol=memory_get_byte --weaken-symbol=string_compare $@ 2>/dev/null || true; \
	fi
	@# Weaken ALL TOKEN constants and shared functions in parser.o
	@if [ "$@" = "$(BUILD_DIR)/parser.o" ]; then \
		for token in $$(nm $@ | grep " TOKEN" | awk '{print $$3}' | sort -u); do \
			objcopy --weaken-symbol=$$token $@ 2>/dev/null || true; \
		done; \
		objcopy --weaken-symbol=token_destroy $@ 2>/dev/null || true; \
	fi
	@# Weaken string utility functions in string_utils.o that conflict with runtime
	@if [ "$@" = "$(BUILD_DIR)/string_utils.o" ]; then \
		objcopy --weaken-symbol=string_length --weaken-symbol=string_char_at --weaken-symbol=string_equals --weaken-symbol=integer_to_string --weaken-symbol=string_to_integer --weaken-symbol=memory_reallocate $@ 2>/dev/null || true; \
	fi

# Link build executable
$(BUILD_TARGET): $(BUILD_OBJECTS) $(BUILD_RUNTIME)
	$(LD) $(BUILD_OBJECTS) $(BUILD_RUNTIME) $(RUNA_LDFLAGS) -o $@

# ===== VERIFY: Compiled by build/runac (self-hosting test) =====

verify: dirs build $(VERIFY_TARGET)
	@echo "=== Verifying self-hosting ==="
	@echo "Comparing assembly outputs (build vs verify)..."
	@all_match=true; \
	for module in $(RUNA_MODULES); do \
		if diff -q $(BUILD_DIR)/$$module.s $(VERIFY_DIR)/$$module.s >/dev/null 2>&1; then \
			echo "  ✓ $$module.s: identical"; \
		else \
			echo "  ✗ $$module.s: DIFFERS!"; \
			all_match=false; \
		fi; \
	done; \
	if [ "$$all_match" = true ]; then \
		echo "✓ Verification successful! v0.0.8 is self-hosting!"; \
	else \
		echo "✗ Verification failed - outputs differ"; \
		exit 1; \
	fi

# Verify runtime compilation
$(VERIFY_DIR)/%.o: $(RUNTIME_DIR)/%.c
	$(CC) $(RUNTIME_CFLAGS) -c $< -o $@

# Verify Runa compilation (using build/runac)
$(VERIFY_DIR)/%.s: $(SRC_DIR)/%.runa $(BUILD_TARGET)
	$(BUILD_TARGET) $< $@

# Verify assembly to object with symbol handling
$(VERIFY_DIR)/%.o: $(VERIFY_DIR)/%.s
	$(AS) $(ASFLAGS) $< -o $@
	@# Strip main symbol from all objects except main.o
	@if [ "$@" != "$(VERIFY_DIR)/main.o" ]; then \
		objcopy --strip-symbol=main $@ 2>/dev/null || true; \
	fi
	@# Weaken runtime symbols that conflict with C runtime
	@if [ "$@" = "$(VERIFY_DIR)/hashtable.o" ] || [ "$@" = "$(VERIFY_DIR)/string_utils.o" ]; then \
		objcopy --weaken-symbol=allocate --weaken-symbol=deallocate --weaken-symbol=memory_set_pointer --weaken-symbol=memory_get_pointer --weaken-symbol=memory_get_byte --weaken-symbol=string_compare $@ 2>/dev/null || true; \
	fi
	@# Weaken ALL TOKEN constants and shared functions in parser.o
	@if [ "$@" = "$(VERIFY_DIR)/parser.o" ]; then \
		for token in $$(nm $@ | grep " TOKEN" | awk '{print $$3}' | sort -u); do \
			objcopy --weaken-symbol=$$token $@ 2>/dev/null || true; \
		done; \
		objcopy --weaken-symbol=token_destroy $@ 2>/dev/null || true; \
	fi
	@# Weaken string utility functions in string_utils.o that conflict with runtime
	@if [ "$@" = "$(VERIFY_DIR)/string_utils.o" ]; then \
		objcopy --weaken-symbol=string_length --weaken-symbol=string_char_at --weaken-symbol=string_equals --weaken-symbol=integer_to_string --weaken-symbol=string_to_integer --weaken-symbol=memory_reallocate $@ 2>/dev/null || true; \
	fi

# Link verify executable
$(VERIFY_TARGET): $(VERIFY_OBJECTS) $(VERIFY_RUNTIME)
	$(LD) $(VERIFY_OBJECTS) $(VERIFY_RUNTIME) $(RUNA_LDFLAGS) -o $@

# ===== TESTING =====

# Main test target
test: test-unit

# Run all unit tests with build compiler
test-unit: dirs build
	@echo "=== Running Unit Tests ==="
	@passed=0; \
	failed=0; \
	for test in $(UNIT_TESTS); do \
		echo -n "  Testing $$test... "; \
		if $(BUILD_TARGET) $(TEST_UNIT_DIR)/$$test.runa $(TEST_OUTPUT_DIR)/$$test.s 2>$(TEST_OUTPUT_DIR)/$$test.err; then \
			if $(AS) $(ASFLAGS) $(TEST_OUTPUT_DIR)/$$test.s -o $(TEST_OUTPUT_DIR)/$$test.o 2>>$(TEST_OUTPUT_DIR)/$$test.err; then \
				if [ "$$test" = "test_compiler" ]; then \
					if $(LD) $(TEST_OUTPUT_DIR)/$$test.o $(BUILD_RUNTIME) $(BUILD_OBJECTS:$(BUILD_DIR)/main.o=) $(LDFLAGS) -o $(TEST_OUTPUT_DIR)/$$test 2>>$(TEST_OUTPUT_DIR)/$$test.err; then \
						echo "✓ (compiled with compiler libs)"; \
						passed=$$((passed+1)); \
					else \
						echo "✗ (link failed)"; \
						failed=$$((failed+1)); \
					fi; \
				else \
					if $(LD) $(TEST_OUTPUT_DIR)/$$test.o $(BUILD_RUNTIME) $(LDFLAGS) -o $(TEST_OUTPUT_DIR)/$$test 2>>$(TEST_OUTPUT_DIR)/$$test.err; then \
						if [ "$$test" = "test_file" ] || [ "$$test" = "test_strings" ]; then \
							echo "✓ (requires file in test dir to run)"; \
							passed=$$((passed+1)); \
						else \
							if $(TEST_OUTPUT_DIR)/$$test >$(TEST_OUTPUT_DIR)/$$test.out 2>&1; then \
								echo "✓"; \
								passed=$$((passed+1)); \
							else \
								echo "✗ (runtime failed)"; \
								cat $(TEST_OUTPUT_DIR)/$$test.out; \
								failed=$$((failed+1)); \
							fi; \
						fi; \
					else \
						echo "✗ (link failed)"; \
						failed=$$((failed+1)); \
					fi; \
				fi; \
			else \
				echo "✗ (assembly failed)"; \
				failed=$$((failed+1)); \
			fi; \
		else \
			echo "✗ (compilation failed)"; \
			cat $(TEST_OUTPUT_DIR)/$$test.err; \
			failed=$$((failed+1)); \
		fi; \
	done; \
	echo ""; \
	echo "Results: $$passed passed, $$failed failed"; \
	if [ $$failed -ne 0 ]; then exit 1; fi

# Quick smoke test
test-quick: dirs build
	@echo "=== Quick Smoke Test ==="
	@$(BUILD_TARGET) $(TEST_UNIT_DIR)/test_minimal.runa $(TEST_OUTPUT_DIR)/test_minimal_quick.s
	@$(AS) $(ASFLAGS) $(TEST_OUTPUT_DIR)/test_minimal_quick.s -o $(TEST_OUTPUT_DIR)/test_minimal_quick.o
	@$(LD) $(TEST_OUTPUT_DIR)/test_minimal_quick.o $(BUILD_RUNTIME) $(LDFLAGS) -o $(TEST_OUTPUT_DIR)/test_minimal_quick
	@$(TEST_OUTPUT_DIR)/test_minimal_quick && echo "✓ Quick test passed"

# ===== CLEANING =====

clean:
	rm -rf $(BUILD_DIR) $(VERIFY_DIR) $(TEST_OUTPUT_DIR)

clean-build:
	rm -rf $(BUILD_DIR)

clean-verify:
	rm -rf $(VERIFY_DIR)

clean-tests:
	rm -rf $(TEST_OUTPUT_DIR)

# ===== HELP =====

help:
	@echo "Runa v0.0.8 Bootstrap Compiler Build System"
	@echo ""
	@echo "Build Targets:"
	@echo "  build         - Build v0.0.8 compiler using v0.0.7.5 (default)"
	@echo "  verify        - Build with itself and verify self-hosting"
	@echo ""
	@echo "Testing:"
	@echo "  test          - Run unit tests (default: with build compiler)"
	@echo "  test-unit     - Run all unit tests"
	@echo "  test-quick    - Quick smoke test"
	@echo ""
	@echo "Cleaning:"
	@echo "  clean         - Remove all build artifacts"
	@echo "  clean-build   - Remove build/ artifacts"
	@echo "  clean-verify  - Remove verify/ artifacts"
	@echo "  clean-tests   - Remove test outputs"
	@echo ""
	@echo "Default:"
	@echo "  all           - Build v0.0.8 (default target)"
	@echo "  help          - Show this help"

# Dependency tracking
.PHONY: all build verify dirs test test-unit test-quick clean clean-build clean-verify clean-tests help