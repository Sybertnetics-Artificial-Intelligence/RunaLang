# Runa v0.0.7.5 Benchmark Suite

This directory contains a comprehensive benchmark suite comparing Runa against C, Rust, Python, and Java.

## Structure

```
benchmarks/
├── runa/          # Runa implementations
├── c/             # C implementations
├── rust/          # Rust implementations
├── python/        # Python implementations
├── java/          # Java implementations
├── results/       # Benchmark results (generated)
├── run_benchmarks.sh  # Main benchmark runner
└── README.md      # This file
```

## Tests

### 1. Fibonacci (fibonacci.*)
- **Purpose**: Tests recursive function calls and stack performance
- **Complexity**: O(2^n) - exponential (intentionally inefficient for stress testing)
- **Input**: Calculates fibonacci(35)
- **Expected Result**: 9227465 (exit code truncated to lower 8 bits)

### 2. Prime Sieve (primes.*)
- **Purpose**: Tests loops, conditionals, and modulo operations
- **Complexity**: O(n * sqrt(n))
- **Input**: Counts primes less than 10,000
- **Expected Result**: 1229 primes

### 3. Factorial (factorial.*)
- **Purpose**: Tests basic arithmetic and recursion
- **Complexity**: O(n)
- **Input**: Calculates sum of factorial(1) through factorial(20)
- **Expected Result**: 0 (success)

### 4. Self-Compilation (compiler benchmark)
- **Purpose**: Measures how fast the compiler can compile itself
- **Metric**: Time to compile all 7 modules (string_utils, hashtable, containers, lexer, parser, codegen, main)

## Running Benchmarks

### Prerequisites

The script will detect available compilers. You need:
- **Runa**: `../build/runac` (required)
- **C**: `gcc` (optional)
- **Rust**: `rustc` (optional)
- **Python**: `python3` (optional)
- **Java**: `javac` and `java` (optional)

### Execute

```bash
cd runa/bootstrap/v0.0.7.5/benchmarks
./run_benchmarks.sh
```

### Results

Results are saved to `results/benchmark_results_YYYYMMDD_HHMMSS.txt` with:
- Average execution time over 5 runs for each test
- Relative performance (speedup/slowdown) compared to other languages
- Compiler self-compilation time
- Binary size

## Expected Performance

Based on similar minimal compilers:

### Execution Speed (typical range)
- **vs C (-O2)**: 2-10x slower (Runa has no optimizer)
- **vs Rust (-O)**: 2-10x slower (similar to C)
- **vs Python**: 10-100x faster (Python is interpreted)
- **vs Java**: 0.5-2x slower/faster (depends on JIT warmup)

### Compilation Speed
- **Self-compile time**: 1-5 seconds (for all 7 modules)
- **Compiler size**: ~200KB (unstripped binary)

## Interpreting Results

### Good Performance Indicators
- Faster than Python by 10x+ (compiled vs interpreted)
- Within 10x of C/Rust (reasonable for unoptimized code)
- Fast compilation times (<5s for self-compile)
- Small binary size (<500KB)

### Areas for Improvement
- If >10x slower than C: codegen inefficiency
- If slower than Python: serious bug
- If self-compile >10s: parser/lexer bottleneck

## Adding New Benchmarks

To add a new benchmark:

1. Create identical implementations in all 5 languages:
   ```
   benchmarks/runa/mytest.runa
   benchmarks/c/mytest.c
   benchmarks/rust/mytest.rs
   benchmarks/python/mytest.py
   benchmarks/java/Mytest.java  # Note: Capital M
   ```

2. Add to `run_benchmarks.sh`:
   ```bash
   benchmark_test "mytest"
   ```

3. Ensure all implementations:
   - Perform identical computation
   - Return result via exit code (for consistency)
   - Use similar algorithm structure

## Notes

- Each test runs 5 times and averages the result
- Tests measure **execution time**, not compilation time (except self-compile benchmark)
- All tests use release/optimized builds where applicable:
  - C: `-O2`
  - Rust: `-O`
  - Runa: (no optimizer yet)
  - Python: standard interpreter
  - Java: standard JVM (JIT enabled)

## Troubleshooting

### "Command not found" errors
- Install missing compiler or skip that language
- The script will automatically skip unavailable languages

### Runa compilation errors
- Ensure `../build/runac` exists and is executable
- Verify runtime object exists at `../build/runtime.o`

### WSL/Linux issues
- Run in WSL: `wsl -e bash run_benchmarks.sh`
- Or use Linux subsystem for accurate timing

## Future Enhancements

- Memory usage benchmarks
- Code size comparison
- More complex algorithms (sorting, tree traversal, etc.)
- Comparison with TinyCC, QBE
- Graphs and visualization