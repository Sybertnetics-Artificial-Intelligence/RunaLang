#!/bin/bash

# Comprehensive Benchmark Suite for latest Runa version
# Compares Runa against C, Rust, Python, and Java

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="$SCRIPT_DIR/results"
RUNAC="../build/runac"
RUNTIME="../build/runtime.o"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create results directory
mkdir -p "$RESULTS_DIR"

# Results file
RESULTS_FILE="$RESULTS_DIR/benchmark_results_$(date +%Y%m%d_%H%M%S).txt"

echo "╔══════════════════════════════════════════════════════════════╗" | tee "$RESULTS_FILE"
echo "║          Runa Benchmark Suite                                ║" | tee -a "$RESULTS_FILE"
echo "╚══════════════════════════════════════════════════════════════╝" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

# Check which compilers are available
echo -e "${BLUE}Checking available compilers...${NC}"
HAVE_GCC=$(wsl.exe command -v gcc &> /dev/null && echo "yes" || echo "no")
HAVE_RUSTC=$(command -v rustc &> /dev/null && echo "yes" || echo "no")
HAVE_PYTHON=$(command -v python3 &> /dev/null && echo "yes" || echo "no")
HAVE_JAVAC=$(command -v javac &> /dev/null && echo "yes" || echo "no")
HAVE_JAVA=$(command -v java &> /dev/null && echo "yes" || echo "no")
HAVE_RUNAC=$(test -f "$SCRIPT_DIR/$RUNAC" && echo "yes" || echo "no")

echo "  GCC:    $HAVE_GCC" | tee -a "$RESULTS_FILE"
echo "  Rustc:  $HAVE_RUSTC" | tee -a "$RESULTS_FILE"
echo "  Python: $HAVE_PYTHON" | tee -a "$RESULTS_FILE"
echo "  Java:   $([ "$HAVE_JAVAC" = "yes" ] && [ "$HAVE_JAVA" = "yes" ] && echo "yes" || echo "no")" | tee -a "$RESULTS_FILE"
echo "  Runa:   $HAVE_RUNAC" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

if [ "$HAVE_RUNAC" = "no" ]; then
    echo -e "${RED}ERROR: Runa compiler not found at $RUNAC${NC}"
    exit 1
fi

# Function to time command execution
time_execution() {
    local cmd="$1"
    local runs=5
    local total=0

    for i in $(seq 1 $runs); do
        local start=$(date +%s%N)
        eval "$cmd" > /dev/null 2>&1
        local end=$(date +%s%N)
        local elapsed=$((($end - $start) / 1000000)) # Convert to milliseconds
        total=$(($total + $elapsed))
    done

    echo $(($total / $runs)) # Average in milliseconds
}

# Function to compile and benchmark
benchmark_test() {
    local test_name="$1"
    echo "" | tee -a "$RESULTS_FILE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$RESULTS_FILE"
    echo -e "${GREEN}TEST: $test_name${NC}" | tee -a "$RESULTS_FILE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$RESULTS_FILE"

    # Runa
    if [ "$HAVE_RUNAC" = "yes" ]; then
        echo -e "${YELLOW}Compiling Runa...${NC}"
        local runa_file="runa/$test_name.runa"
        local runa_asm="results/${test_name}_runa.s"
        local runa_obj="results/${test_name}_runa.o"
        local runa_exe="results/${test_name}_runa"

        wsl.exe $RUNAC "$runa_file" "$runa_asm" 2>&1 | grep -v "^[0-9]*$" || true
        wsl.exe as --64 "$runa_asm" -o "$runa_obj" 2>&1
        wsl.exe gcc "$runa_obj" "$RUNTIME" -lm -o "$runa_exe" 2>&1

        local runa_time=$(time_execution "wsl.exe $runa_exe")
        echo "  Runa:   ${runa_time}ms (avg of 5 runs)" | tee -a "$RESULTS_FILE"
    fi

    # C
    if [ "$HAVE_GCC" = "yes" ]; then
        echo -e "${YELLOW}Compiling C...${NC}"
        local c_file="c/$test_name.c"
        local c_exe="results/${test_name}_c"

        wsl.exe gcc -O2 "$c_file" -o "$c_exe" 2>&1

        local c_time=$(time_execution "wsl.exe $c_exe")
        echo "  C:      ${c_time}ms (avg of 5 runs)" | tee -a "$RESULTS_FILE"

        # Calculate speedup
        if [ "$HAVE_RUNAC" = "yes" ]; then
            local speedup=$(echo "scale=2; $runa_time / $c_time" | bc)
            echo "  Runa is ${speedup}x slower than C" | tee -a "$RESULTS_FILE"
        fi
    fi

    # Rust
    if [ "$HAVE_RUSTC" = "yes" ]; then
        echo -e "${YELLOW}Compiling Rust...${NC}"
        local rust_file="rust/$test_name.rs"
        local rust_exe="results/${test_name}_rust"

        rustc -O "$rust_file" -o "$rust_exe" 2>&1

        local rust_time=$(time_execution "$rust_exe")
        echo "  Rust:   ${rust_time}ms (avg of 5 runs)" | tee -a "$RESULTS_FILE"

        if [ "$HAVE_RUNAC" = "yes" ]; then
            local speedup=$(echo "scale=2; $runa_time / $rust_time" | bc)
            echo "  Runa is ${speedup}x slower than Rust" | tee -a "$RESULTS_FILE"
        fi
    fi

    # Python
    if [ "$HAVE_PYTHON" = "yes" ]; then
        echo -e "${YELLOW}Running Python...${NC}"
        local python_file="python/$test_name.py"

        local python_time=$(time_execution "python3 $python_file")
        echo "  Python: ${python_time}ms (avg of 5 runs)" | tee -a "$RESULTS_FILE"

        if [ "$HAVE_RUNAC" = "yes" ]; then
            local speedup=$(echo "scale=2; $python_time / $runa_time" | bc)
            echo "  Runa is ${speedup}x faster than Python" | tee -a "$RESULTS_FILE"
        fi
    fi

    # Java
    if [ "$HAVE_JAVAC" = "yes" ] && [ "$HAVE_JAVA" = "yes" ]; then
        echo -e "${YELLOW}Compiling Java...${NC}"
        local java_file="java/$(echo $test_name | sed 's/.*/\u&/').java"
        local java_class="$(echo $test_name | sed 's/.*/\u&/')"

        javac "$java_file" -d results 2>&1

        local java_time=$(time_execution "java -cp results $java_class")
        echo "  Java:   ${java_time}ms (avg of 5 runs)" | tee -a "$RESULTS_FILE"

        if [ "$HAVE_RUNAC" = "yes" ]; then
            local speedup=$(echo "scale=2; $runa_time / $java_time" | bc)
            echo "  Runa is ${speedup}x slower than Java" | tee -a "$RESULTS_FILE"
        fi
    fi
}

# Auto-discover and run all benchmarks
echo -e "${BLUE}Discovering benchmark tests...${NC}"
BENCHMARK_TESTS=()

# Find all .runa files in the runa directory
for runa_file in runa/*.runa; do
    if [ -f "$runa_file" ]; then
        # Extract just the filename without extension
        test_name=$(basename "$runa_file" .runa)
        BENCHMARK_TESTS+=("$test_name")
    fi
done

# Sort tests alphabetically for consistent output
IFS=$'\n' BENCHMARK_TESTS=($(sort <<<"${BENCHMARK_TESTS[*]}"))
unset IFS

echo "Found ${#BENCHMARK_TESTS[@]} benchmark tests: ${BENCHMARK_TESTS[*]}" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

# Run all discovered benchmarks
for test in "${BENCHMARK_TESTS[@]}"; do
    benchmark_test "$test"
done

# Compiler self-compilation benchmark
echo "" | tee -a "$RESULTS_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$RESULTS_FILE"
echo -e "${GREEN}COMPILER BENCHMARK: Self-Compilation Time${NC}" | tee -a "$RESULTS_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$RESULTS_FILE"

if [ "$HAVE_RUNAC" = "yes" ]; then
    echo -e "${YELLOW}Timing Runa self-compilation...${NC}"

    compile_all_modules() {
        for module in string_utils hashtable containers lexer parser codegen main; do
            wsl.exe $RUNAC "../src/${module}.runa" "results/${module}.s" 2>&1 | grep -v "^[0-9]*$" || true
        done
    }

    local bootstrap_time=$(time_execution compile_all_modules)
    echo "  Runa bootstrap time: ${bootstrap_time}ms" | tee -a "$RESULTS_FILE"

    # Compiler size
    local compiler_size=$(ls -lh "$RUNAC" | awk '{print $5}')
    echo "  Compiler binary size: $compiler_size" | tee -a "$RESULTS_FILE"
fi

# Summary
echo "" | tee -a "$RESULTS_FILE"
echo "╔══════════════════════════════════════════════════════════════╗" | tee -a "$RESULTS_FILE"
echo "║                    BENCHMARK COMPLETE                        ║" | tee -a "$RESULTS_FILE"
echo "╚══════════════════════════════════════════════════════════════╝" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"
echo "Results saved to: $RESULTS_FILE" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

# Create clean version without ANSI color codes
CLEAN_RESULTS="$RESULTS_DIR/benchmark_results_clean.txt"
sed 's/\x1b\[[0-9;]*m//g' "$RESULTS_FILE" > "$CLEAN_RESULTS"
echo "Clean results (no color codes) saved to: $CLEAN_RESULTS" | tee -a "$RESULTS_FILE"

# Also create latest_results.txt symlink/copy
cp "$CLEAN_RESULTS" "$RESULTS_DIR/../latest_results.txt"
echo "Latest results also saved to: latest_results.txt"

echo -e "${GREEN}Done!${NC}"