#!/bin/bash
# Runtime correctness test runner.
#
# For each positive test (NN_*.runa):
#   1. Compile with the current stage1/runac
#   2. Assemble + link with runtime.o
#   3. Run the executable and capture exit code
#   4. Compare against the "Expected exit code: N" line in the source
#
# For each negative test (neg_NN_*.runa):
#   1. Compile with the current stage1/runac
#   2. Verify compilation FAILED (non-zero exit)
#   3. Verify the error output contains the substring after "Expected:" comment
#
# Reports PASS/FAIL counts and exits non-zero if any test failed.

set -u

# VERSION_ROOT resolves to the v0.0.8.4.5.3.5 compiler dir (this runner now
# lives at <version>/tests/runtime/, so ../.. is the version root).
VERSION_ROOT=$(cd "$(dirname "$0")/../.." && pwd)
RUNAC=${RUNAC:-$VERSION_ROOT/stage1/runac}
RT_OBJ=$VERSION_ROOT/runtime/runtime.o
TESTS_DIR=$VERSION_ROOT/tests/runtime
TMPS=$(mktemp -d)
trap 'rm -rf "$TMPS"' EXIT

PASS=0
FAIL=0
FAILURES=""

for src in "$TESTS_DIR"/[0-9]*_*.runa; do
    name=$(basename "$src" .runa)
    expected=$(grep -oE "Expected exit code: [0-9]+" "$src" | grep -oE "[0-9]+$" | head -1)
    if [ -z "$expected" ]; then
        FAILURES="$FAILURES\n  $name: no 'Expected exit code:' annotation"
        FAIL=$((FAIL+1))
        continue
    fi
    asm="$TMPS/$name.s"
    obj="$TMPS/$name.o"
    exe="$TMPS/$name.exe"

    if ! "$RUNAC" "$src" "$asm" > "$TMPS/$name.cout" 2>&1; then
        FAILURES="$FAILURES\n  $name: compile failed"
        FAIL=$((FAIL+1))
        continue
    fi
    if ! as "$asm" -o "$obj" 2>"$TMPS/$name.aerr"; then
        FAILURES="$FAILURES\n  $name: assembler failed"
        FAIL=$((FAIL+1))
        continue
    fi
    if ! gcc -no-pie "$obj" "$RT_OBJ" -lm -o "$exe" 2>"$TMPS/$name.lerr"; then
        FAILURES="$FAILURES\n  $name: link failed"
        FAIL=$((FAIL+1))
        continue
    fi

    "$exe" >/dev/null 2>&1
    actual=$?
    if [ "$actual" = "$expected" ]; then
        PASS=$((PASS+1))
        echo "PASS  $name (exit $actual)"
    else
        FAIL=$((FAIL+1))
        FAILURES="$FAILURES\n  $name: expected exit $expected, got $actual"
        echo "FAIL  $name (expected $expected, got $actual)"
    fi
done

for src in "$TESTS_DIR"/neg_*.runa; do
    [ -f "$src" ] || continue
    name=$(basename "$src" .runa)
    compile_msg=$(grep -oE 'Expected: compilation fails with "[^"]+"' "$src" | sed -E 's/.*"([^"]+)".*/\1/')
    link_msg=$(grep -oE 'Expected: link fails with "[^"]+"' "$src" | sed -E 's/.*"([^"]+)".*/\1/')
    if [ -z "$compile_msg" ] && [ -z "$link_msg" ]; then
        FAILURES="$FAILURES\n  $name: no 'Expected: compilation fails with \"...\"' or 'Expected: link fails with \"...\"' annotation"
        FAIL=$((FAIL+1))
        continue
    fi
    asm="$TMPS/$name.s"
    obj="$TMPS/$name.o"
    exe="$TMPS/$name.exe"

    if [ -n "$compile_msg" ]; then
        "$RUNAC" "$src" "$asm" > "$TMPS/$name.cout" 2>&1
        rc=$?
        if [ "$rc" = "0" ]; then
            FAIL=$((FAIL+1))
            FAILURES="$FAILURES\n  $name: compilation unexpectedly SUCCEEDED"
            echo "FAIL  $name (compilation should have failed)"
            continue
        fi
        if grep -q "$compile_msg" "$TMPS/$name.cout"; then
            PASS=$((PASS+1))
            echo "PASS  $name (rejected with expected message)"
        else
            FAIL=$((FAIL+1))
            FAILURES="$FAILURES\n  $name: error did not contain '$compile_msg'"
            echo "FAIL  $name (wrong error - dumped: $(head -5 "$TMPS/$name.cout" | tr '\n' ' '))"
        fi
    else
        # Link-failure negative test: compile must succeed, then ld must fail
        # with the expected message. Used when scoping/use-of-undeclared falls
        # through to a symbol-reference fallback at codegen and is caught only
        # at link time.
        if ! "$RUNAC" "$src" "$asm" > "$TMPS/$name.cout" 2>&1; then
            FAIL=$((FAIL+1))
            FAILURES="$FAILURES\n  $name: compile failed (expected link-fail) - $(head -3 "$TMPS/$name.cout" | tr '\n' ' ')"
            echo "FAIL  $name (compile failed - expected to reach link)"
            continue
        fi
        if ! as "$asm" -o "$obj" 2>"$TMPS/$name.aerr"; then
            FAIL=$((FAIL+1))
            FAILURES="$FAILURES\n  $name: assembler failed - $(head -3 "$TMPS/$name.aerr" | tr '\n' ' ')"
            echo "FAIL  $name (assembler failed)"
            continue
        fi
        gcc -no-pie "$obj" "$RT_OBJ" -lm -o "$exe" > "$TMPS/$name.lout" 2>&1
        rc=$?
        if [ "$rc" = "0" ]; then
            FAIL=$((FAIL+1))
            FAILURES="$FAILURES\n  $name: link unexpectedly SUCCEEDED"
            echo "FAIL  $name (link should have failed)"
            continue
        fi
        if grep -q "$link_msg" "$TMPS/$name.lout"; then
            PASS=$((PASS+1))
            echo "PASS  $name (link rejected with expected message)"
        else
            FAIL=$((FAIL+1))
            FAILURES="$FAILURES\n  $name: link error did not contain '$link_msg'"
            echo "FAIL  $name (wrong link error - dumped: $(head -5 "$TMPS/$name.lout" | tr '\n' ' '))"
        fi
    fi
done

echo
echo "===== SUMMARY: PASS=$PASS FAIL=$FAIL ====="
if [ "$FAIL" -gt 0 ]; then
    echo -e "Failures:$FAILURES"
    exit 1
fi
exit 0
