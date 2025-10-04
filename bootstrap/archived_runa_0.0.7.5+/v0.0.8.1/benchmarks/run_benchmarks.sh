#!/bin/bash

# Comprehensive Benchmark Suite for Runa v0.0.7.5
# Compares Runa against C, Rust, Python, and Java

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_DIR="$SCRIPT_DIR/results"
RUNAC="$SCRIPT_DIR/../build/runac"
RUNTIME="$SCRIPT_DIR/../build/runtime.o"

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
echo "║          Runa v0.0.7.5 Benchmark Suite                      ║" | tee -a "$RESULTS_FILE"
echo "╚══════════════════════════════════════════════════════════════╝" | tee -a "$RESULTS_FILE"
echo "" | tee -a "$RESULTS_FILE"

# Check which compilers are available
echo -e "${BLUE}Checking available compilers...${NC}"
HAVE_GCC=$(command -v gcc &> /dev/null && echo "yes" || echo "no")
HAVE_RUSTC=$(command -v rustc &> /dev/null && echo "yes" || echo "no")
HAVE_PYTHON=$(command -v python3 &> /dev/null && echo "yes" || echo "no")
HAVE_JAVAC=$(command -v javac &> /dev/null && echo "yes" || echo "no")
HAVE_JAVA=$(command -v java &> /dev/null && echo "yes" || echo "no")
HAVE_RUNAC=$(test -f "$RUNAC" && echo "yes" || echo "no")

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
        local runa_file="$SCRIPT_DIR/runa/$test_name.runa"
        local runa_asm="$RESULTS_DIR/${test_name}_runa.s"
        local runa_obj="$RESULTS_DIR/${test_name}_runa.o"
        local runa_exe="$RESULTS_DIR/${test_name}_runa"

        $RUNAC "$runa_file" "$runa_asm" 2>&1 | grep -v "^[0-9]*$" || true
        as --64 "$runa_asm" -o "$runa_obj" 2>&1
        gcc "$runa_obj" "$RUNTIME" -lm -o "$runa_exe" 2>&1

        local runa_time=$(time_execution "$runa_exe")
        echo "  Runa:   ${runa_time}ms (avg of 5 runs)" | tee -a "$RESULTS_FILE"
    fi

    # C
    if [ "$HAVE_GCC" = "yes" ]; then
        echo -e "${YELLOW}Compiling C...${NC}"
        local c_file="$SCRIPT_DIR/c/$test_name.c"
        local c_exe="$RESULTS_DIR/${test_name}_c"

        gcc -O2 "$c_file" -o "$c_exe" 2>&1

        local c_time=$(time_execution "$c_exe")
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
        local rust_file="$SCRIPT_DIR/rust/$test_name.rs"
        local rust_exe="$RESULTS_DIR/${test_name}_rust"

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
        local python_file="$SCRIPT_DIR/python/$test_name.py"

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
        local java_file="$SCRIPT_DIR/java/$(echo $test_name | sed 's/.*/\u&/').java"
        local java_class="$(echo $test_name | sed 's/.*/\u&/')"

        javac "$java_file" -d "$RESULTS_DIR" 2>&1

        local java_time=$(time_execution "java -cp $RESULTS_DIR $java_class")
        echo "  Java:   ${java_time}ms (avg of 5 runs)" | tee -a "$RESULTS_FILE"

        if [ "$HAVE_RUNAC" = "yes" ]; then
            local speedup=$(echo "scale=2; $runa_time / $java_time" | bc)
            echo "  Runa is ${speedup}x slower than Java" | tee -a "$RESULTS_FILE"
        fi
    fi
}

# Run benchmarks
benchmark_test "fibonacci"
benchmark_test "primes"
benchmark_test "factorial"

# Compiler self-compilation benchmark
echo "" | tee -a "$RESULTS_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$RESULTS_FILE"
echo -e "${GREEN}COMPILER BENCHMARK: Self-Compilation Time${NC}" | tee -a "$RESULTS_FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$RESULTS_FILE"

if [ "$HAVE_RUNAC" = "yes" ]; then
    echo -e "${YELLOW}Timing Runa self-compilation...${NC}"

    compile_all_modules() {
        for module in string_utils hashtable containers lexer parser codegen main; do
            $RUNAC "$SCRIPT_DIR/../src/${module}.runa" "$RESULTS_DIR/${module}.s" 2>&1 | grep -v "^[0-9]*$" || true
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

echo -e "${GREEN}Done!${NC}"