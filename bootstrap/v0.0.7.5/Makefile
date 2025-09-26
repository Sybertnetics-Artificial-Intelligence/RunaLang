# Makefile for Runa v0.0.7.5 Bootstrap Compiler
# Mixed C runtime + Runa compiler implementation

# Compiler settings
CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2 -g
RUNAC_V0073 = ../v0.0.7.3/runac
RUNAC_FLAGS =
AS = as
ASFLAGS = --64
LD = gcc
LDFLAGS = -lm

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
	$(CC) $(CFLAGS) -c $< -o $@

# Runa source compilation (Runa -> Assembly -> Object)
$(BUILD_DIR)/%.s: $(SRC_DIR)/%.runa | $(BUILD_DIR)
	$(RUNAC_V0073) $< $@ $(RUNAC_FLAGS)

$(BUILD_DIR)/%.o: $(BUILD_DIR)/%.s
	$(AS) $(ASFLAGS) $< -o $@

# Link final executable
$(TARGET): $(ALL_OBJECTS)
	$(LD) $(ALL_OBJECTS) $(LDFLAGS) -o $@

# Individual component targets
runtime: $(RUNTIME_OBJECTS)

runa-compile: $(RUNA_ASSEMBLY)

runa-assemble: $(RUNA_OBJECTS)

link: $(TARGET)

# Testing targets
test: $(TARGET)
	@echo "Running test suite..."
	@./tests/run_unit_tests.sh
	@./tests/run_integration_tests.sh

test-units: $(TARGET)
	@./tests/run_unit_tests.sh

test-integration: $(TARGET)
	@./tests/run_integration_tests.sh

test-bootstrap: $(TARGET)
	@./tests/test_bootstrap.sh

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

# Component dependencies (will be updated as components are implemented)
# $(BUILD_DIR)/hashtable.o: $(BUILD_DIR)/string_utils.o
# $(BUILD_DIR)/containers.o: $(BUILD_DIR)/hashtable.o
# $(BUILD_DIR)/lexer.o: $(BUILD_DIR)/string_utils.o $(BUILD_DIR)/containers.o
# $(BUILD_DIR)/parser.o: $(BUILD_DIR)/lexer.o $(BUILD_DIR)/containers.o $(BUILD_DIR)/hashtable.o
# $(BUILD_DIR)/codegen.o: $(BUILD_DIR)/parser.o $(BUILD_DIR)/string_utils.o
# $(BUILD_DIR)/main.o: $(BUILD_DIR)/lexer.o $(BUILD_DIR)/parser.o $(BUILD_DIR)/codegen.o