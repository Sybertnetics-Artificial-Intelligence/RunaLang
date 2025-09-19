# Runa v0.1 Runtime Library Makefile

CC = gcc
CFLAGS = -Wall -Wextra -O2 -fPIC
AR = ar
ARFLAGS = rcs

# Output files
STATIC_LIB = libruna_runtime.a
SHARED_LIB = libruna_runtime.so
OBJECT_FILES = string_runtime.o

# Default target
all: $(STATIC_LIB) $(SHARED_LIB)

# Build object files
string_runtime.o: string_runtime.c runa_runtime.h
	$(CC) $(CFLAGS) -c string_runtime.c -o string_runtime.o

# Build static library
$(STATIC_LIB): $(OBJECT_FILES)
	$(AR) $(ARFLAGS) $(STATIC_LIB) $(OBJECT_FILES)

# Build shared library
$(SHARED_LIB): $(OBJECT_FILES)
	$(CC) -shared -o $(SHARED_LIB) $(OBJECT_FILES)

# Clean build files
clean:
	rm -f $(OBJECT_FILES) $(STATIC_LIB) $(SHARED_LIB)

# Test the runtime library
test: test_runtime.c $(STATIC_LIB)
	$(CC) $(CFLAGS) test_runtime.c $(STATIC_LIB) -o test_runtime
	./test_runtime

# Install headers (for linking with v0.0 compiled programs)
install-headers:
	mkdir -p ../include
	cp runa_runtime.h ../include/

.PHONY: all clean test install-headers