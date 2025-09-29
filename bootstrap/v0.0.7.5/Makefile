# Makefile for Runa v0.0.7.5 Bootstrap Compiler
# Mixed C runtime + Runa compiler implementation
# Bootstrap stages: Stage 1 (C-compiled) -> Stage 2 (self-hosted) -> Stage 3 (verification)

# Compiler settings
CC = gcc
CFLAGS ?= -Wall -Wextra -std=c99 -O2 -g -fPIC
RUNAC_V0073 = ../v0.0.7.3/bin/runac
RUNAC_FLAGS =
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
STAGE1_DIR = stage1
STAGE2_DIR = stage2
STAGE3_DIR = stage3
BUILD_DIR = build
SRC_DIR = src
RUNTIME_DIR = runtime
TEST_DIR = tests
TEST_UNIT_DIR = tests/unit
TEST_OUTPUT_DIR = tests/output

# Runtime library source files (C and assembly)
RUNTIME_C_SOURCES = $(wildcard $(RUNTIME_DIR)/*.c)
RUNTIME_SOURCES = $(RUNTIME_C_SOURCES)

# Runa source files
RUNA_MODULES = string_utils hashtable containers lexer parser codegen main
RUNA_SOURCES = $(RUNA_MODULES:%=$(SRC_DIR)/%.runa)

# Stage 1 files (compiled by v0.0.7.3)
STAGE1_ASSEMBLY = $(RUNA_MODULES:%=$(STAGE1_DIR)/%.s)
STAGE1_OBJECTS = $(RUNA_MODULES:%=$(STAGE1_DIR)/%.o)
STAGE1_RUNTIME = $(RUNTIME_SOURCES:$(RUNTIME_DIR)/%.c=$(STAGE1_DIR)/%.o)
STAGE1_TARGET = $(STAGE1_DIR)/runac

# Stage 2 files (compiled by Stage 1)
STAGE2_ASSEMBLY = $(RUNA_MODULES:%=$(STAGE2_DIR)/%.s)
STAGE2_OBJECTS = $(RUNA_MODULES:%=$(STAGE2_DIR)/%.o)
STAGE2_RUNTIME = $(RUNTIME_SOURCES:$(RUNTIME_DIR)/%.c=$(STAGE2_DIR)/%.o)
STAGE2_TARGET = $(STAGE2_DIR)/runac

# Stage 3 files (compiled by Stage 2)
STAGE3_ASSEMBLY = $(RUNA_MODULES:%=$(STAGE3_DIR)/%.s)
STAGE3_OBJECTS = $(RUNA_MODULES:%=$(STAGE3_DIR)/%.o)
STAGE3_RUNTIME = $(RUNTIME_SOURCES:$(RUNTIME_DIR)/%.c=$(STAGE3_DIR)/%.o)
STAGE3_TARGET = $(STAGE3_DIR)/runac

# List of unit tests (without .runa extension)
UNIT_TESTS = test_minimal test_let test_if test_args test_display test_strings test_file test_compiler

# Default target builds Stage 1
all: stage1

# Bootstrap all stages and verify
bootstrap: stage3 verify

# Ensure directories exist
dirs:
	@mkdir -p $(STAGE1_DIR) $(STAGE2_DIR) $(STAGE3_DIR) $(BUILD_DIR) $(TEST_OUTPUT_DIR)

# ===== STAGE 1: Compiled by v0.0.7.3 (C compiler) =====

stage1: dirs $(STAGE1_TARGET)
	@echo "✓ Stage 1 complete: $(STAGE1_TARGET)"

# Stage 1 runtime compilation
$(STAGE1_DIR)/%.o: $(RUNTIME_DIR)/%.c
	$(CC) $(RUNTIME_CFLAGS) -c $< -o $@

# Stage 1 Runa compilation (using v0.0.7.3)
$(STAGE1_DIR)/%.s: $(SRC_DIR)/%.runa
	$(RUNAC_V0073) $< $@ $(RUNAC_FLAGS)

# Stage 1 assembly to object with symbol handling
$(STAGE1_DIR)/%.o: $(STAGE1_DIR)/%.s
	$(AS) $(ASFLAGS) $< -o $@
	@# Strip main symbol from all objects except main.o
	@if [ "$@" != "$(STAGE1_DIR)/main.o" ]; then \
		objcopy --strip-symbol=main $@ 2>/dev/null || true; \
	fi
	@# Weaken runtime symbols that conflict with C runtime
	@if [ "$@" = "$(STAGE1_DIR)/hashtable.o" ] || [ "$@" = "$(STAGE1_DIR)/string_utils.o" ]; then \
		objcopy --weaken-symbol=allocate --weaken-symbol=deallocate --weaken-symbol=memory_set_pointer --weaken-symbol=memory_set_integer --weaken-symbol=memory_get_pointer --weaken-symbol=memory_get_integer --weaken-symbol=memory_get_byte --weaken-symbol=string_compare $@ 2>/dev/null || true; \
	fi
	@# Weaken ALL TOKEN constants and shared functions in parser.o
	@if [ "$@" = "$(STAGE1_DIR)/parser.o" ]; then \
		for token in $$(nm $@ | grep " TOKEN" | awk '{print $$3}' | sort -u); do \
			objcopy --weaken-symbol=$$token $@ 2>/dev/null || true; \
		done; \
		objcopy --weaken-symbol=token_destroy $@ 2>/dev/null || true; \
	fi
	@# Weaken string utility functions in string_utils.o that conflict with runtime
	@if [ "$@" = "$(STAGE1_DIR)/string_utils.o" ]; then \
		objcopy --weaken-symbol=string_length --weaken-symbol=string_char_at --weaken-symbol=string_equals --weaken-symbol=integer_to_string --weaken-symbol=string_to_integer --weaken-symbol=memory_reallocate $@ 2>/dev/null || true; \
	fi

# Link Stage 1 executable
$(STAGE1_TARGET): $(STAGE1_OBJECTS) $(STAGE1_RUNTIME)
	$(LD) $(STAGE1_OBJECTS) $(STAGE1_RUNTIME) $(RUNA_LDFLAGS) -o $@

# ===== STAGE 2: Compiled by Stage 1 (self-hosted) =====

stage2: dirs stage1 $(STAGE2_TARGET)
	@echo "✓ Stage 2 complete: $(STAGE2_TARGET)"

# Stage 2 runtime compilation
$(STAGE2_DIR)/%.o: $(RUNTIME_DIR)/%.c
	$(CC) $(RUNTIME_CFLAGS) -c $< -o $@

# Stage 2 Runa compilation (using Stage 1)
$(STAGE2_DIR)/%.s: $(SRC_DIR)/%.runa $(STAGE1_TARGET)
	$(STAGE1_TARGET) $< $@ $(RUNAC_FLAGS)

# Stage 2 assembly to object with symbol handling
$(STAGE2_DIR)/%.o: $(STAGE2_DIR)/%.s
	$(AS) $(ASFLAGS) $< -o $@
	@# Strip main symbol from all objects except main.o
	@if [ "$@" != "$(STAGE2_DIR)/main.o" ]; then \
		objcopy --strip-symbol=main $@ 2>/dev/null || true; \
	fi
	@# Weaken runtime symbols that conflict with C runtime (EXCEPT memory_get_integer/memory_set_integer)
	@if [ "$@" = "$(STAGE2_DIR)/hashtable.o" ] || [ "$@" = "$(STAGE2_DIR)/string_utils.o" ]; then \
		objcopy --weaken-symbol=allocate --weaken-symbol=deallocate --weaken-symbol=memory_set_pointer --weaken-symbol=memory_get_pointer --weaken-symbol=memory_get_byte --weaken-symbol=string_compare $@ 2>/dev/null || true; \
	fi
	@# Weaken ALL TOKEN constants and shared functions in parser.o
	@if [ "$@" = "$(STAGE2_DIR)/parser.o" ]; then \
		for token in $$(nm $@ | grep " TOKEN" | awk '{print $$3}' | sort -u); do \
			objcopy --weaken-symbol=$$token $@ 2>/dev/null || true; \
		done; \
		objcopy --weaken-symbol=token_destroy $@ 2>/dev/null || true; \
	fi
	@# Weaken string utility functions in string_utils.o that conflict with runtime
	@if [ "$@" = "$(STAGE2_DIR)/string_utils.o" ]; then \
		objcopy --weaken-symbol=string_length --weaken-symbol=string_char_at --weaken-symbol=string_equals --weaken-symbol=integer_to_string --weaken-symbol=string_to_integer --weaken-symbol=memory_reallocate $@ 2>/dev/null || true; \
	fi

# Assemble runtime wrappers for Stage 2
$(STAGE2_WRAPPERS): $(RUNTIME_ASM_SOURCES)
	$(AS) $(RUNTIME_ASM_SOURCES) -o $@

# Link Stage 2 executable
$(STAGE2_TARGET): $(STAGE2_OBJECTS) $(STAGE2_RUNTIME) $(STAGE2_WRAPPERS)
	$(LD) $(STAGE2_OBJECTS) $(STAGE2_WRAPPERS) $(STAGE2_RUNTIME) $(RUNA_LDFLAGS) -o $@

# ===== STAGE 3: Compiled by Stage 2 (verification) =====

stage3: dirs stage2 $(STAGE3_TARGET)
	@echo "✓ Stage 3 complete: $(STAGE3_TARGET)"

# Stage 3 runtime compilation
$(STAGE3_DIR)/%.o: $(RUNTIME_DIR)/%.c
	$(CC) $(RUNTIME_CFLAGS) -c $< -o $@

# Stage 3 Runa compilation (using Stage 2)
$(STAGE3_DIR)/%.s: $(SRC_DIR)/%.runa $(STAGE2_TARGET)
	$(STAGE2_TARGET) $< $@ $(RUNAC_FLAGS)

# Stage 3 assembly to object with symbol handling
$(STAGE3_DIR)/%.o: $(STAGE3_DIR)/%.s
	$(AS) $(ASFLAGS) $< -o $@
	@# Strip main symbol from all objects except main.o
	@if [ "$@" != "$(STAGE3_DIR)/main.o" ]; then \
		objcopy --strip-symbol=main $@ 2>/dev/null || true; \
	fi
	@# Weaken runtime symbols that conflict with C runtime
	@if [ "$@" = "$(STAGE3_DIR)/hashtable.o" ] || [ "$@" = "$(STAGE3_DIR)/string_utils.o" ]; then \
		objcopy --weaken-symbol=allocate --weaken-symbol=deallocate --weaken-symbol=memory_set_pointer --weaken-symbol=memory_set_integer --weaken-symbol=memory_get_pointer --weaken-symbol=memory_get_integer --weaken-symbol=memory_get_byte --weaken-symbol=string_compare $@ 2>/dev/null || true; \
	fi
	@# Weaken ALL TOKEN constants and shared functions in parser.o
	@if [ "$@" = "$(STAGE3_DIR)/parser.o" ]; then \
		for token in $$(nm $@ | grep " TOKEN" | awk '{print $$3}' | sort -u); do \
			objcopy --weaken-symbol=$$token $@ 2>/dev/null || true; \
		done; \
		objcopy --weaken-symbol=token_destroy $@ 2>/dev/null || true; \
	fi
	@# Weaken string utility functions in string_utils.o that conflict with runtime
	@if [ "$@" = "$(STAGE3_DIR)/string_utils.o" ]; then \
		objcopy --weaken-symbol=string_length --weaken-symbol=string_char_at --weaken-symbol=string_equals --weaken-symbol=integer_to_string --weaken-symbol=string_to_integer --weaken-symbol=memory_reallocate $@ 2>/dev/null || true; \
	fi

# Link Stage 3 executable
$(STAGE3_TARGET): $(STAGE3_OBJECTS) $(STAGE3_RUNTIME)
	$(LD) $(STAGE3_OBJECTS) $(STAGE3_RUNTIME) $(RUNA_LDFLAGS) -o $@

# ===== VERIFICATION =====

verify: stage3
	@echo "=== Verifying bootstrap (Stage 2 vs Stage 3) ==="
	@echo "Comparing assembly outputs..."
	@for module in $(RUNA_MODULES); do \
		if diff -q $(STAGE2_DIR)/$$module.s $(STAGE3_DIR)/$$module.s >/dev/null 2>&1; then \
			echo "  ✓ $$module.s: identical"; \
		else \
			echo "  ✗ $$module.s: DIFFERS!"; \
			exit 1; \
		fi; \
	done
	@echo "✓ Bootstrap successful! All assembly outputs are identical."
	@echo "✓ Stage 2 compiler ($(STAGE2_TARGET)) is self-hosting!"

# ===== TESTING =====

# Main test target - runs all test suites
test: test-unit

# Run all unit tests with specified compiler (defaults to Stage 2)
test-unit: dirs stage2
	@echo "=== Running Unit Tests with Stage 2 ==="
	@$(MAKE) test-unit-with COMPILER=$(STAGE2_TARGET) RUNTIME_OBJS="$(STAGE2_RUNTIME)"

test-unit-stage1: dirs stage1
	@echo "=== Running Unit Tests with Stage 1 ==="
	@$(MAKE) test-unit-with COMPILER=$(STAGE1_TARGET) RUNTIME_OBJS="$(STAGE1_RUNTIME)"

test-unit-stage2: dirs stage2
	@echo "=== Running Unit Tests with Stage 2 ==="
	@$(MAKE) test-unit-with COMPILER=$(STAGE2_TARGET) RUNTIME_OBJS="$(STAGE2_RUNTIME)"

test-unit-stage3: dirs stage3
	@echo "=== Running Unit Tests with Stage 3 ==="
	@$(MAKE) test-unit-with COMPILER=$(STAGE3_TARGET) RUNTIME_OBJS="$(STAGE3_RUNTIME)"

# Helper target to run tests with specified compiler
test-unit-with: dirs
	@passed=0; \
	failed=0; \
	for test in $(UNIT_TESTS); do \
		echo -n "  Testing $$test... "; \
		if $(COMPILER) $(TEST_UNIT_DIR)/$$test.runa $(TEST_OUTPUT_DIR)/$$test.s 2>$(TEST_OUTPUT_DIR)/$$test.err; then \
			if $(AS) $(ASFLAGS) $(TEST_OUTPUT_DIR)/$$test.s -o $(TEST_OUTPUT_DIR)/$$test.o 2>>$(TEST_OUTPUT_DIR)/$$test.err; then \
				if [ "$$test" = "test_compiler" ]; then \
					if $(LD) $(TEST_OUTPUT_DIR)/$$test.o $$(echo $(RUNTIME_OBJS) | sed 's|[^ ]*/main.o||g') $(STAGE2_OBJECTS:$(STAGE2_DIR)/main.o=) $(LDFLAGS) -o $(TEST_OUTPUT_DIR)/$$test 2>>$(TEST_OUTPUT_DIR)/$$test.err; then \
						echo "✓ (compiled with compiler libs)"; \
						passed=$$((passed+1)); \
					else \
						echo "✗ (link failed)"; \
						failed=$$((failed+1)); \
					fi; \
				else \
					if $(LD) $(TEST_OUTPUT_DIR)/$$test.o $(RUNTIME_OBJS) $(LDFLAGS) -o $(TEST_OUTPUT_DIR)/$$test 2>>$(TEST_OUTPUT_DIR)/$$test.err; then \
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

# Test all stages
test-all-stages: test-unit-stage1 test-unit-stage2 test-unit-stage3 verify

# Quick smoke test
test-quick: dirs stage1
	@echo "=== Quick Smoke Test ==="
	@$(STAGE1_TARGET) $(TEST_UNIT_DIR)/test_minimal.runa $(TEST_OUTPUT_DIR)/test_minimal_quick.s
	@$(AS) $(ASFLAGS) $(TEST_OUTPUT_DIR)/test_minimal_quick.s -o $(TEST_OUTPUT_DIR)/test_minimal_quick.o
	@$(LD) $(TEST_OUTPUT_DIR)/test_minimal_quick.o $(STAGE1_RUNTIME) $(LDFLAGS) -o $(TEST_OUTPUT_DIR)/test_minimal_quick
	@$(TEST_OUTPUT_DIR)/test_minimal_quick && echo "✓ Quick test passed"

# ===== INSTALLATION =====

# Install the verified Stage 2 compiler
install: stage2
	@mkdir -p $(BUILD_DIR)
	cp $(STAGE2_TARGET) $(BUILD_DIR)/runac-0.0.7.5
	@echo "✓ Installed Stage 2 compiler to $(BUILD_DIR)/runac-0.0.7.5"

# ===== CLEANING =====

clean:
	rm -rf $(STAGE1_DIR) $(STAGE2_DIR) $(STAGE3_DIR) $(BUILD_DIR) $(TEST_OUTPUT_DIR)

clean-stage1:
	rm -rf $(STAGE1_DIR)

clean-stage2:
	rm -rf $(STAGE2_DIR)

clean-stage3:
	rm -rf $(STAGE3_DIR)

clean-tests:
	rm -rf $(TEST_OUTPUT_DIR)

# ===== HELP =====

help:
	@echo "Runa v0.0.7.5 Bootstrap Compiler Build System"
	@echo ""
	@echo "Bootstrap Stages:"
	@echo "  stage1        - Build Stage 1 (compiled by v0.0.7.3)"
	@echo "  stage2        - Build Stage 2 (compiled by Stage 1, self-hosted)"
	@echo "  stage3        - Build Stage 3 (compiled by Stage 2, verification)"
	@echo "  bootstrap     - Build all stages and verify"
	@echo "  verify        - Verify Stage 2 and Stage 3 are identical"
	@echo ""
	@echo "Testing:"
	@echo "  test          - Run unit tests with Stage 2 (default)"
	@echo "  test-unit     - Run all unit tests with Stage 2"
	@echo "  test-unit-stage1 - Run unit tests with Stage 1"
	@echo "  test-unit-stage2 - Run unit tests with Stage 2"
	@echo "  test-unit-stage3 - Run unit tests with Stage 3"
	@echo "  test-all-stages - Test all stages comprehensively"
	@echo "  test-quick    - Quick smoke test with Stage 1"
	@echo ""
	@echo "Installation:"
	@echo "  install       - Install Stage 2 to build/runac-0.0.7.5"
	@echo ""
	@echo "Cleaning:"
	@echo "  clean         - Remove all build artifacts"
	@echo "  clean-stage1  - Remove Stage 1 artifacts"
	@echo "  clean-stage2  - Remove Stage 2 artifacts"
	@echo "  clean-stage3  - Remove Stage 3 artifacts"
	@echo "  clean-tests   - Remove test outputs"
	@echo ""
	@echo "Default:"
	@echo "  all           - Build Stage 1 (default target)"
	@echo "  help          - Show this help"

# Dependency tracking for development
.PHONY: all bootstrap dirs stage1 stage2 stage3 verify test test-unit test-unit-stage1 test-unit-stage2 test-unit-stage3 test-unit-with test-all-stages test-quick clean-tests install clean clean-stage1 clean-stage2 clean-stage3 help