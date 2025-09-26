# Makefile for Runa v0.0.7.5 Bootstrap Compiler
# Mixed C runtime + Runa compiler implementation

# Compiler settings
CC = gcc
CFLAGS ?= -Wall -Wextra -std=c99 -O2 -g -fPIC
RUNAC_V0073 = ../v0.0.7.3/runac
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
BUILD_DIR = build
SRC_DIR = src
RUNTIME_DIR = runtime
TEST_DIR = tests

# Runtime library source files (C)
RUNTIME_SOURCES = $(wildcard $(RUNTIME_DIR)/*.c)
RUNTIME_OBJECTS = $(RUNTIME_SOURCES:$(RUNTIME_DIR)/%.c=$(BUILD_DIR)/%.o)

# Runa source files (to be compiled to assembly then object files)
RUNA_SOURCES = $(wildcard $(SRC_DIR)/*.runa)
RUNA_ASSEMBLY = $(RUNA_SOURCES:$(SRC_DIR)/%.runa=$(BUILD_DIR)/%.s)
RUNA_OBJECTS = $(RUNA_SOURCES:$(SRC_DIR)/%.runa=$(BUILD_DIR)/%.o)

# All object files
ALL_OBJECTS = $(RUNTIME_OBJECTS) $(RUNA_OBJECTS)

# Final executable
TARGET = $(BUILD_DIR)/runac

# Default target
all: $(TARGET)

# Create build directory
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Runtime library compilation (C to object files)
$(BUILD_DIR)/%.o: $(RUNTIME_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(RUNTIME_CFLAGS) -c $< -o $@

# Runa source compilation (Runa -> Assembly -> Object)
$(BUILD_DIR)/%.s: $(SRC_DIR)/%.runa | $(BUILD_DIR)
	$(RUNAC_V0073) $< $@ $(RUNAC_FLAGS)

# Rule to compile assembly files to object files with automatic symbol handling
$(BUILD_DIR)/%.o: $(BUILD_DIR)/%.s
	$(AS) $(ASFLAGS) $< -o $@
	@# Strip main symbol from all objects except main.o
	@if [ "$@" != "$(BUILD_DIR)/main.o" ]; then \
		objcopy --strip-symbol=main $@ 2>/dev/null || true; \
	fi
	@# Weaken runtime symbols that conflict with C runtime
	@if [ "$@" = "$(BUILD_DIR)/hashtable.o" ] || [ "$@" = "$(BUILD_DIR)/string_utils.o" ]; then \
		objcopy --weaken-symbol=allocate --weaken-symbol=deallocate --weaken-symbol=memory_set_pointer --weaken-symbol=memory_set_integer --weaken-symbol=memory_get_pointer --weaken-symbol=memory_get_integer --weaken-symbol=memory_get_byte --weaken-symbol=string_compare $@ 2>/dev/null || true; \
	fi
	@# Weaken ALL TOKEN constants and shared functions in parser.o (let lexer.o be definitive)
	@if [ "$@" = "$(BUILD_DIR)/parser.o" ]; then \
		for token in $$(nm $@ | grep " TOKEN" | awk '{print $$3}' | sort -u); do \
			objcopy --weaken-symbol=$$token $@ 2>/dev/null || true; \
		done; \
		objcopy --weaken-symbol=token_destroy $@ 2>/dev/null || true; \
	fi
	@# Weaken string utility functions in string_utils.o that conflict with runtime
	@# NOTE: is_whitespace, is_digit, is_alpha NOT weakened - runtime versions removed
	@if [ "$@" = "$(BUILD_DIR)/string_utils.o" ]; then \
		objcopy --weaken-symbol=string_length --weaken-symbol=string_char_at --weaken-symbol=string_equals --weaken-symbol=integer_to_string --weaken-symbol=string_to_integer --weaken-symbol=memory_reallocate $@ 2>/dev/null || true; \
	fi

# Link final executable with runtime libraries
$(TARGET): $(ALL_OBJECTS)
	$(LD) $(ALL_OBJECTS) $(RUNA_LDFLAGS) -o $@

# Individual component targets
runtime: $(RUNTIME_OBJECTS)

runa-compile: $(RUNA_ASSEMBLY)

runa-assemble: $(RUNA_OBJECTS)

link: $(TARGET)

# Testing targets
test: $(TARGET)
	@echo "Running complete test suite..."
	@$(MAKE) test-compile
	@$(MAKE) test-runtime
	@$(MAKE) test-integration
	@$(MAKE) test-bootstrap

test-compile: $(TARGET)
	@echo "Testing Runa compilation..."
	@echo "Process called \"test\" takes x as Integer returns Integer:" > $(TEST_DIR)/test_minimal.runa
	@echo "    Return 42" >> $(TEST_DIR)/test_minimal.runa
	@echo "End Process" >> $(TEST_DIR)/test_minimal.runa
	@$(TARGET) $(TEST_DIR)/test_minimal.runa $(TEST_DIR)/test_minimal.s
	@$(AS) $(ASFLAGS) $(TEST_DIR)/test_minimal.s -o $(TEST_DIR)/test_minimal.o
	@$(LD) $(TEST_DIR)/test_minimal.o $(RUNTIME_OBJECTS) $(LDFLAGS) -o $(TEST_DIR)/test_minimal
	@$(TEST_DIR)/test_minimal && echo "✓ Basic compilation test passed"

test-runtime: $(RUNTIME_OBJECTS)
	@echo "Testing runtime libraries..."
	@$(CC) $(CFLAGS) -DRUNTIME_TEST $(RUNTIME_DIR)/runtime_test.c $(RUNTIME_OBJECTS) -o $(BUILD_DIR)/runtime_test
	@$(BUILD_DIR)/runtime_test && echo "✓ Runtime tests passed"

test-integration: $(TARGET)
	@echo "Running integration tests..."
	@for test in $(TEST_DIR)/*.runa; do \
		echo "  Testing $$test..."; \
		$(TARGET) $$test $${test%.runa}.s || exit 1; \
	done
	@echo "✓ All integration tests passed"

test-bootstrap: $(TARGET)
	@echo "Running bootstrap self-compilation test..."
	@echo "  Stage 1: Compiling with v0.0.7.3..."
	@$(RUNAC_V0073) $(SRC_DIR)/main.runa $(BUILD_DIR)/stage1_main.s
	@echo "  Stage 2: Self-compiling..."
	@$(TARGET) $(SRC_DIR)/main.runa $(BUILD_DIR)/stage2_main.s
	@echo "  Comparing outputs..."
	@diff -q $(BUILD_DIR)/stage1_main.s $(BUILD_DIR)/stage2_main.s && echo "✓ Bootstrap test passed"

test-valgrind: $(TARGET)
	@echo "Running memory tests with Valgrind..."
	@valgrind --leak-check=full --error-exitcode=1 $(TARGET) $(TEST_DIR)/test_minimal.runa $(TEST_DIR)/test_minimal_valgrind.s
	@echo "✓ Memory tests passed"

# Development targets
debug: CFLAGS += -DDEBUG -O0
debug: $(TARGET)

verbose: RUNAC_FLAGS += --verbose
verbose: $(TARGET)

# Clean targets
clean:
	rm -rf $(BUILD_DIR)/*

clean-runa:
	rm -f $(BUILD_DIR)/*.s $(BUILD_DIR)/main.o $(BUILD_DIR)/lexer.o $(BUILD_DIR)/parser.o $(BUILD_DIR)/codegen.o $(BUILD_DIR)/string_utils.o $(BUILD_DIR)/containers.o $(BUILD_DIR)/hashtable.o

clean-runtime:
	rm -f $(RUNTIME_OBJECTS)

# Installation
install: $(TARGET)
	cp $(TARGET) /usr/local/bin/runac

# Help target
help:
	@echo "Runa v0.0.7.5 Bootstrap Compiler Build System"
	@echo ""
	@echo "Targets:"
	@echo "  all           - Build complete compiler (default)"
	@echo "  runtime       - Compile C runtime libraries only"
	@echo "  runa-compile  - Compile Runa sources to assembly"
	@echo "  runa-assemble - Assemble Runa assembly to objects"
	@echo "  link          - Link final executable"
	@echo "  test          - Run complete test suite"
	@echo "  test-units    - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-bootstrap - Run bootstrap self-compilation test"
	@echo "  debug         - Build with debug symbols"
	@echo "  verbose       - Build with verbose output"
	@echo "  clean         - Remove all build artifacts"
	@echo "  clean-runa    - Remove only Runa build artifacts"
	@echo "  clean-runtime - Remove only runtime build artifacts"
	@echo "  install       - Install compiler to /usr/local/bin"
	@echo "  help          - Show this help"

# Dependency tracking for development
.PHONY: all runtime runa-compile runa-assemble link test test-units test-integration test-bootstrap debug verbose clean clean-runa clean-runtime install help

# Component dependencies - enforced for proper build order
$(BUILD_DIR)/string_utils.s: $(SRC_DIR)/string_utils.runa | $(BUILD_DIR)
	$(RUNAC_V0073) $< $@ $(RUNAC_FLAGS)

$(BUILD_DIR)/hashtable.s: $(SRC_DIR)/hashtable.runa $(BUILD_DIR)/string_utils.o | $(BUILD_DIR)
	$(RUNAC_V0073) $< $@ $(RUNAC_FLAGS)

$(BUILD_DIR)/containers.s: $(SRC_DIR)/containers.runa $(BUILD_DIR)/string_utils.o $(BUILD_DIR)/hashtable.o | $(BUILD_DIR)
	$(RUNAC_V0073) $< $@ $(RUNAC_FLAGS)

$(BUILD_DIR)/lexer.s: $(SRC_DIR)/lexer.runa $(BUILD_DIR)/string_utils.o $(BUILD_DIR)/containers.o | $(BUILD_DIR)
	$(RUNAC_V0073) $< $@ $(RUNAC_FLAGS)

$(BUILD_DIR)/parser.s: $(SRC_DIR)/parser.runa $(BUILD_DIR)/lexer.o $(BUILD_DIR)/containers.o $(BUILD_DIR)/hashtable.o | $(BUILD_DIR)
	$(RUNAC_V0073) $< $@ $(RUNAC_FLAGS)

$(BUILD_DIR)/codegen.s: $(SRC_DIR)/codegen.runa $(BUILD_DIR)/parser.o $(BUILD_DIR)/string_utils.o | $(BUILD_DIR)
	$(RUNAC_V0073) $< $@ $(RUNAC_FLAGS)

$(BUILD_DIR)/main.s: $(SRC_DIR)/main.runa $(BUILD_DIR)/lexer.o $(BUILD_DIR)/parser.o $(BUILD_DIR)/codegen.o | $(BUILD_DIR)
	$(RUNAC_V0073) $< $@ $(RUNAC_FLAGS)