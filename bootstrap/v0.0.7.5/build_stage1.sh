#!/bin/bash
# Build Stage 1 compiler working around v0.0.7.3 issues

echo "Building Stage 1 compiler..."

# First, compile all modules with v0.0.7.3
echo "Compiling modules with v0.0.7.3..."
../v0.0.7.3/bin/runac src/string_utils.runa build/string_utils.s || exit 1
../v0.0.7.3/bin/runac src/hashtable.runa build/hashtable.s || exit 1
../v0.0.7.3/bin/runac src/containers.runa build/containers.s || exit 1
../v0.0.7.3/bin/runac src/lexer.runa build/lexer.s || exit 1
../v0.0.7.3/bin/runac src/parser_nodup.runa build/parser.s || exit 1
../v0.0.7.3/bin/runac src/codegen.runa build/codegen.s || exit 1
../v0.0.7.3/bin/runac src/main.runa build/main.s || exit 1

echo "Removing spurious main functions..."
# Remove spurious main functions from all modules except main.s
for f in build/string_utils.s build/hashtable.s build/containers.s build/lexer.s build/parser.s build/codegen.s; do
    sed -i '/^main:/,/^$/d' "$f" 2>/dev/null
done

echo "Removing duplicate token_destroy from lexer..."
# token_destroy appears in both parser and lexer, remove from lexer
sed -i '/^token_destroy:/,/^$/d' build/lexer.s

echo "Removing duplicate runtime functions..."
# Remove functions that conflict with runtime
sed -i '/^memory_reallocate:/,/^$/d' build/string_utils.s
sed -i '/^allocate:/,/^$/d' build/hashtable.s
sed -i '/^deallocate:/,/^$/d' build/hashtable.s

# Remove memory functions that conflict with runtime_system.c
sed -i '/^memory_get_byte:/,/^$/d' build/hashtable.s
sed -i '/^memory_get_pointer:/,/^$/d' build/hashtable.s
sed -i '/^memory_set_pointer:/,/^$/d' build/hashtable.s
sed -i '/^string_compare:/,/^$/d' build/hashtable.s

# Remove string functions that conflict with runtime_string.c
sed -i '/^string_length:/,/^$/d' build/string_utils.s
sed -i '/^string_char_at:/,/^$/d' build/string_utils.s
sed -i '/^string_equals:/,/^$/d' build/string_utils.s
sed -i '/^integer_to_string:/,/^$/d' build/string_utils.s
sed -i '/^string_to_integer:/,/^$/d' build/string_utils.s

echo "Assembling Stage 1 compiler..."
gcc -o build/runac \
    build/main.s \
    build/parser.s \
    build/lexer.s \
    build/codegen.s \
    build/string_utils.s \
    build/hashtable.s \
    build/containers.s \
    runtime/*.c \
    -lm

if [ $? -eq 0 ]; then
    echo "Stage 1 compiler built successfully: build/runac"
else
    echo "Failed to build Stage 1 compiler"
    exit 1
fi