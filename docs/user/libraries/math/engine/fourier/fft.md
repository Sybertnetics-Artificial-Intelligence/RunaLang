# Fast Fourier Transform (FFT)

The Fast Fourier Transform (FFT) module provides high-performance implementations of various FFT algorithms optimized for speed and efficiency. This module implements state-of-the-art algorithms that reduce the computational complexity from O(N²) to O(N log N), making it practical for real-time signal processing and large-scale data analysis.

## Overview

FFT algorithms exploit the symmetry and periodicity properties of the discrete Fourier transform to dramatically reduce computational requirements. This module provides multiple algorithm variants optimized for different input sizes, data types, and performance characteristics.

### Key Algorithms

- **Radix-2 FFT**: Classic Cooley-Tukey algorithm for power-of-2 lengths
- **Radix-4 FFT**: Higher radix for improved efficiency
- **Mixed-Radix FFT**: Handles arbitrary composite lengths
- **Prime-Factor FFT**: Optimal for lengths with small prime factors
- **Real FFT**: Specialized algorithms for real-valued signals
- **Multi-dimensional FFT**: For images and higher-dimensional data

## Core Data Structures

### FFTConfig

Configuration parameters for FFT computation:

```runa
Type called "FFTConfig":
    algorithm_type as String      Note: radix2, radix4, mixed_radix, prime_factor
    use_simd as Boolean          Note: enable SIMD optimizations
    use_parallel as Boolean      Note: enable parallel processing
    num_threads as Integer       Note: number of parallel threads
    memory_layout as String      Note: row_major, column_major, interleaved
    precision as String          Note: single, double, extended
```

**Usage Example:**
```runa
Note: Configure high-performance FFT for real-time audio processing
Let config be FFTConfig with:
    algorithm_type = "radix4"
    use_simd = true
    use_parallel = false        Note: real-time constraints
    num_threads = 1
    memory_layout = "interleaved"
    precision = "single"
```

### FFTPlan

Pre-computed plan for optimal FFT execution:

```runa
Type called "FFTPlan":
    size as Integer                              Note: transform size
    config as FFTConfig                          Note: configuration settings
    twiddle_factors as List[Complex]            Note: pre-computed coefficients
    bit_reversal_indices as List[Integer]       Note: bit-reversal permutation
    algorithm_specific_data as Dictionary[String, Any] Note: algorithm-specific optimizations
    is_initialized as Boolean                   Note: plan initialization status
```

### FFTResult

Comprehensive result with performance metrics:

```runa
Type called "FFTResult":
    output as List[Complex]          Note: transformed data
    computation_time as Float        Note: execution time in seconds
    memory_usage as Integer          Note: peak memory usage in bytes
    algorithm_used as String         Note: actual algorithm selected
    optimization_flags as List[String] Note: optimizations applied
```

## Radix-2 FFT Implementation

### Classic Cooley-Tukey Algorithm

The foundational FFT algorithm for power-of-2 lengths:

```runa
Process called "fft_radix2" that takes input as List[Complex], inverse as Boolean returns List[Complex]:
    Let N be input.size()
    If N <= 1:
        Return input
    
    If not is_power_of_two(N):
        Throw Errors.InvalidArgument with "Input size must be power of 2 for radix-2 FFT"
    
    Note: Bit-reversal permutation
    Let bit_reversed be bit_reverse_permutation(input)
    Let twiddle_factors be generate_twiddle_factors(N, inverse)
    
    Note: Iterative butterfly operations
    Let result be List[Complex]
    For element in bit_reversed:
        Call result.append(element)
    
    Let length be 2
    While length <= N:
        For i from 0 to N - 1 step length:
            For j from 0 to length / 2 - 1:
                Let u be result[i + j]
                Let v_index be i + j + length / 2
                Let v be result[v_index]
                Let twiddle be twiddle_factors[j * N / length]
                
                Note: Butterfly operation: (u, v) -> (u + tv, u - tv)
                Let v_twiddle be complex_multiply(v, twiddle)
                Set result[i + j] to complex_add(u, v_twiddle)
                Set result[v_index] to complex_subtract(u, v_twiddle)
        
        Set length to length * 2
    
    Return result
```

### Optimized Butterfly Operations

Core computational kernel with SIMD optimization:

```runa
Process called "butterfly_radix2" that takes a as Complex, b as Complex, twiddle as Complex returns List[Complex]:
    Note: Single radix-2 butterfly with twiddle factor
    Let t be complex_multiply(b, twiddle)
    Let u be complex_add(a, t)
    Let v be complex_subtract(a, t)
    Return [u, v]

Process called "butterfly_radix2_simd" that takes inputs as List[Complex], twiddles as List[Complex], stride as Integer returns List[Complex]:
    Note: SIMD-optimized butterfly operations for multiple elements
    Let results be List[Complex]
    Let simd_width be 4  Note: process 4 complex numbers simultaneously
    
    For i from 0 to inputs.size() step simd_width * 2:
        Let a_batch be extract_simd_batch(inputs, i, simd_width)
        Let b_batch be extract_simd_batch(inputs, i + simd_width, simd_width)
        Let twiddle_batch be extract_simd_batch(twiddles, i / 2, simd_width)
        
        Let butterfly_results be simd_butterfly_operation(a_batch, b_batch, twiddle_batch)
        Call results.extend(butterfly_results)
    
    Return results
```

## Radix-4 FFT Implementation

### Higher Radix for Improved Performance

Radix-4 algorithm reduces the number of butterfly stages:

```runa
Process called "fft_radix4" that takes input as List[Complex], inverse as Boolean returns List[Complex]:
    Let N be input.size()
    If N <= 1:
        Return input
    
    If N % 4 != 0:
        Note: Fall back to radix-2 for non-radix-4 sizes
        Return fft_radix2(input, inverse)
    
    Note: Digit-reversal permutation for radix-4
    Let digit_reversed be digit_reverse_permutation_radix4(input)
    Let twiddle_factors be generate_twiddle_factors_radix4(N, inverse)
    
    Let result be List[Complex]
    For element in digit_reversed:
        Call result.append(element)
    
    Let length be 4
    While length <= N:
        For i from 0 to N - 1 step length:
            For j from 0 to length / 4 - 1:
                Let indices be [i + j, i + j + length / 4, i + j + length / 2, i + j + 3 * length / 4]
                Let inputs be [result[indices[0]], result[indices[1]], result[indices[2]], result[indices[3]]]
                Let twiddle_group be extract_radix4_twiddles(twiddle_factors, j, length, N)
                
                Let outputs be butterfly_radix4(inputs, twiddle_group)
                
                For k from 0 to 3:
                    Set result[indices[k]] to outputs[k]
        
        Set length to length * 4
    
    Return result
```

### Radix-4 Butterfly Operation

More complex but more efficient butterfly:

```runa
Process called "butterfly_radix4" that takes inputs as List[Complex], twiddles as List[Complex] returns List[Complex]:
    Note: Radix-4 butterfly: 4 inputs -> 4 outputs with 3 twiddle factors
    Let x0 be inputs[0]
    Let x1 be complex_multiply(inputs[1], twiddles[0])
    Let x2 be complex_multiply(inputs[2], twiddles[1])
    Let x3 be complex_multiply(inputs[3], twiddles[2])
    
    Note: First stage of radix-4 butterfly
    Let a be complex_add(x0, x2)
    Let b be complex_subtract(x0, x2)
    Let c be complex_add(x1, x3)
    Let d be complex_multiply(complex_subtract(x1, x3), Complex{real: 0.0, imag: if inverse then 1.0 Otherwise -1.0})
    
    Note: Second stage
    Let y0 be complex_add(a, c)
    Let y1 be complex_add(b, d)
    Let y2 be complex_subtract(a, c)
    Let y3 be complex_subtract(b, d)
    
    Return [y0, y1, y2, y3]
```

## Real FFT Algorithms

### Real-to-Complex Transform

Optimized FFT for real-valued signals:

```runa
Process called "fft_real" that takes signal as List[Float] returns List[Complex]:
    Note: Efficient FFT for real signals using Hermitian symmetry
    Let N be signal.size()
    
    Note: Pack real signal into complex array (imaginary parts = 0)
    Let complex_signal be List[Complex]
    For sample in signal:
        Call complex_signal.append(Complex{real: sample, imag: 0.0})
    
    Note: Perform complex FFT
    Let full_spectrum be fft_radix2(complex_signal, false)
    
    Note: Extract unique part (due to Hermitian symmetry)
    Let unique_spectrum be List[Complex]
    For k from 0 to N / 2:  Note: include DC and Nyquist
        Call unique_spectrum.append(full_spectrum[k])
    
    Return unique_spectrum

Process called "fft_real_optimized" that takes signal as List[Float] returns List[Complex]:
    Note: Memory-efficient real FFT using N/2-point complex FFT
    Let N be signal.size()
    If N % 2 != 0:
        Throw Errors.InvalidArgument with "Real FFT requires even length signal"
    
    Note: Pack pairs of real samples into complex numbers
    Let packed_signal be List[Complex]
    For i from 0 to N / 2 - 1:
        Let complex_sample be Complex with:
            real = signal[2 * i]      Note: even samples
            imag = signal[2 * i + 1]  Note: odd samples
        Call packed_signal.append(complex_sample)
    
    Note: Perform N/2-point complex FFT
    Let packed_spectrum be fft_radix2(packed_signal, false)
    
    Note: Unpack to get full real spectrum
    Let spectrum be unpack_real_spectrum(packed_spectrum, N)
    
    Return spectrum
```

### Complex-to-Real Inverse Transform

Converting complex spectrum back to real signal:

```runa
Process called "ifft_real" that takes spectrum as List[Complex] returns List[Float]:
    Note: Inverse FFT producing real-valued output
    Let N be spectrum.size()
    
    Note: Reconstruct full Hermitian-symmetric spectrum
    Let full_spectrum be List[Complex]
    For k from 0 to N - 1:
        Call full_spectrum.append(spectrum[k])
    
    For k from N to 2 * N - 2:
        Let symmetric_index be 2 * N - 1 - k
        Let conjugate be Complex with:
            real = spectrum[symmetric_index].real
            imag = -spectrum[symmetric_index].imag
        Call full_spectrum.append(conjugate)
    
    Note: Perform inverse complex FFT
    Let complex_result be fft_radix2(full_spectrum, true)
    
    Note: Extract real part
    Let real_signal be List[Float]
    For coefficient in complex_result:
        Call real_signal.append(coefficient.real)
    
    Return real_signal
```

## Multi-Dimensional FFT

### 2D FFT for Image Processing

Separable 2D transform using 1D FFTs:

```runa
Process called "fft_2d" that takes image as List[List[Complex]] returns List[List[Complex]]:
    Note: 2D FFT using row-column decomposition
    Let height be image.size()
    Let width be image[0].size()
    
    Note: Transform each row
    Let row_transformed be List[List[Complex]]
    For row in image:
        Let transformed_row be fft_radix2(row, false)
        Call row_transformed.append(transformed_row)
    
    Note: Transform each column
    Let result be Collections.create_matrix(height, width, Complex{real: 0.0, imag: 0.0})
    For j from 0 to width - 1:
        Let column be List[Complex]
        For i from 0 to height - 1:
            Call column.append(row_transformed[i][j])
        
        Let transformed_column be fft_radix2(column, false)
        For i from 0 to height - 1:
            Set result[i][j] to transformed_column[i]
    
    Return result
```

### 3D FFT for Volume Data

Extension to three-dimensional data:

```runa
Process called "fft_3d" that takes volume as List[List[List[Complex]]] returns List[List[List[Complex]]]:
    Note: 3D FFT using separable transforms
    Let depth be volume.size()
    Let height be volume[0].size()
    Let width be volume[0][0].size()
    
    Note: Transform along first dimension
    Let temp1 be Collections.create_3d_array(depth, height, width, Complex{real: 0.0, imag: 0.0})
    For j from 0 to height - 1:
        For k from 0 to width - 1:
            Let line be List[Complex]
            For i from 0 to depth - 1:
                Call line.append(volume[i][j][k])
            Let transformed_line be fft_radix2(line, false)
            For i from 0 to depth - 1:
                Set temp1[i][j][k] to transformed_line[i]
    
    Note: Transform along second dimension
    Let temp2 be Collections.create_3d_array(depth, height, width, Complex{real: 0.0, imag: 0.0})
    For i from 0 to depth - 1:
        For k from 0 to width - 1:
            Let line be List[Complex]
            For j from 0 to height - 1:
                Call line.append(temp1[i][j][k])
            Let transformed_line be fft_radix2(line, false)
            For j from 0 to height - 1:
                Set temp2[i][j][k] to transformed_line[j]
    
    Note: Transform along third dimension
    Let result be Collections.create_3d_array(depth, height, width, Complex{real: 0.0, imag: 0.0})
    For i from 0 to depth - 1:
        For j from 0 to height - 1:
            Let line be List[Complex]
            For k from 0 to width - 1:
                Call line.append(temp2[i][j][k])
            Let transformed_line be fft_radix2(line, false)
            For k from 0 to width - 1:
                Set result[i][j][k] to transformed_line[k]
    
    Return result
```

## Mixed-Radix and Prime Factor FFT

### Composite Length FFT

Handling arbitrary composite lengths:

```runa
Process called "fft_mixed_radix" that takes input as List[Complex], factors as List[Integer], inverse as Boolean returns List[Complex]:
    Note: FFT for composite lengths using prime factorization
    Let N be input.size()
    If product_of_factors(factors) != N:
        Throw Errors.InvalidArgument with "Factors must multiply to input size"
    
    Let current_data be List[Complex]
    For element in input:
        Call current_data.append(element)
    
    Note: Apply FFT for each prime factor
    For factor in factors:
        Set current_data to apply_prime_factor_fft(current_data, factor, inverse)
    
    Return current_data

Process called "apply_prime_factor_fft" that takes data as List[Complex], factor as Integer, inverse as Boolean returns List[Complex]:
    Note: Apply FFT decomposition for a single prime factor
    Let N be data.size()
    Let stride be N / factor
    Let result be Collections.create_list_with_size(N, Complex{real: 0.0, imag: 0.0})
    
    For group from 0 to stride - 1:
        Let group_data be List[Complex]
        For i from 0 to factor - 1:
            Call group_data.append(data[group + i * stride])
        
        Let transformed_group be if factor == 2 then fft_radix2(group_data, inverse) 
                                  Otherwise if factor == 4 then fft_radix4(group_data, inverse)
                                  Otherwise dft_direct_prime(group_data, factor, inverse)
        
        For i from 0 to factor - 1:
            Set result[group + i * stride] to transformed_group[i]
    
    Return result
```

### Good-Thomas Prime Factor Algorithm

Optimal algorithm for mutually prime factors:

```runa
Process called "fft_good_thomas" that takes input as List[Complex], N1 as Integer, N2 as Integer, inverse as Boolean returns List[Complex]:
    Note: Good-Thomas algorithm for N = N1 × N2 where gcd(N1, N2) = 1
    Let N be N1 * N2
    If input.size() != N:
        Throw Errors.InvalidArgument with "Input size must equal N1 × N2"
    
    If gcd(N1, N2) != 1:
        Throw Errors.InvalidArgument with "N1 and N2 must be mutually prime"
    
    Note: Chinese Remainder Theorem mapping
    Let mapped_input be Collections.create_matrix(N1, N2, Complex{real: 0.0, imag: 0.0})
    For n from 0 to N - 1:
        Let n1 be n % N1
        Let n2 be n % N2
        Set mapped_input[n1][n2] to input[n]
    
    Note: Transform along first dimension
    Let temp be Collections.create_matrix(N1, N2, Complex{real: 0.0, imag: 0.0})
    For n2 from 0 to N2 - 1:
        Let column be List[Complex]
        For n1 from 0 to N1 - 1:
            Call column.append(mapped_input[n1][n2])
        Let transformed_column be fft_for_size(column, N1, inverse)
        For n1 from 0 to N1 - 1:
            Set temp[n1][n2] to transformed_column[n1]
    
    Note: Transform along second dimension
    Let result_matrix be Collections.create_matrix(N1, N2, Complex{real: 0.0, imag: 0.0})
    For n1 from 0 to N1 - 1:
        Let row be List[Complex]
        For n2 from 0 to N2 - 1:
            Call row.append(temp[n1][n2])
        Let transformed_row be fft_for_size(row, N2, inverse)
        For n2 from 0 to N2 - 1:
            Set result_matrix[n1][n2] to transformed_row[n2]
    
    Note: Map back to linear array
    Let result be List[Complex]
    For n from 0 to N - 1:
        Let n1 be n % N1
        Let n2 be n % N2
        Call result.append(result_matrix[n1][n2])
    
    Return result
```

## FFT Planning and Optimization

### Automatic Plan Generation

Creating optimal execution plans:

```runa
Process called "create_fft_plan" that takes size as Integer, config as FFTConfig returns FFTPlan:
    Note: Generate optimal FFT plan based on size and configuration
    Let plan be FFTPlan with:
        size = size
        config = config
        twiddle_factors = List[Complex]
        bit_reversal_indices = List[Integer]
        algorithm_specific_data = Dictionary[String, Any]
        is_initialized = false
    
    Note: Choose optimal algorithm
    Let algorithm be select_optimal_algorithm(size, config)
    Set plan.config.algorithm_type to algorithm
    
    Note: Pre-compute twiddle factors
    Set plan.twiddle_factors to generate_optimized_twiddles(size, algorithm)
    
    Note: Pre-compute permutation indices
    If algorithm == "radix2":
        Set plan.bit_reversal_indices to generate_bit_reversal_indices(size)
    Otherwise if algorithm == "radix4":
        Set plan.bit_reversal_indices to generate_digit_reversal_indices_radix4(size)
    
    Note: Algorithm-specific optimizations
    Set plan.algorithm_specific_data to generate_algorithm_data(size, algorithm, config)
    Set plan.is_initialized to true
    
    Return plan

Process called "select_optimal_algorithm" that takes size as Integer, config as FFTConfig returns String:
    Note: Choose best algorithm based on size characteristics
    If is_power_of_two(size):
        If size >= 1024 and config.use_simd:
            Return "radix4"  Note: radix-4 better for large sizes
        Otherwise:
            Return "radix2"  Note: radix-2 for smaller sizes or no SIMD
    
    Let factors be prime_factorization(size)
    If all_factors_small(factors):  Note: all factors <= 7
        Return "mixed_radix"
    Otherwise:
        Return "chirp_z"  Note: Chirp-Z for large prime factors
```

### Execution with Pre-computed Plan

Using plans for optimal performance:

```runa
Process called "execute_fft_plan" that takes input as List[Complex], plan as FFTPlan, inverse as Boolean returns FFTResult:
    Note: Execute FFT using pre-computed plan
    If not plan.is_initialized:
        Throw Errors.InvalidArgument with "FFT plan not initialized"
    
    If input.size() != plan.size:
        Throw Errors.InvalidArgument with "Input size doesn't match plan size"
    
    Let start_time be current_time()
    Let result be List[Complex]
    
    Note: Execute based on planned algorithm
    If plan.config.algorithm_type == "radix2":
        Set result to execute_planned_radix2(input, plan, inverse)
    Otherwise if plan.config.algorithm_type == "radix4":
        Set result to execute_planned_radix4(input, plan, inverse)
    Otherwise if plan.config.algorithm_type == "mixed_radix":
        Set result to execute_planned_mixed_radix(input, plan, inverse)
    
    Let end_time be current_time()
    
    Let fft_result be FFTResult with:
        output = result
        computation_time = end_time - start_time
        memory_usage = estimate_memory_usage(plan)
        algorithm_used = plan.config.algorithm_type
        optimization_flags = extract_optimization_flags(plan.config)
    
    Return fft_result
```

## Parallel FFT Implementation

### Multi-threaded Radix-2 FFT

Parallel butterfly operations:

```runa
Process called "fft_radix2_parallel" that takes input as List[Complex], num_threads as Integer, inverse as Boolean returns List[Complex]:
    Note: Parallel radix-2 FFT using thread-level parallelism
    Let N be input.size()
    Let bit_reversed be bit_reverse_permutation(input)
    Let twiddle_factors be generate_twiddle_factors(N, inverse)
    
    Let result be List[Complex]
    For element in bit_reversed:
        Call result.append(element)
    
    Let length be 2
    While length <= N:
        Let num_groups be N / length
        Let threads_per_stage be MathCore.min(num_threads, num_groups)
        
        Note: Parallel butterfly operations within each stage
        Call parallel_butterfly_stage(result, length, twiddle_factors, threads_per_stage, N)
        
        Set length to length * 2
    
    Return result

Process called "parallel_butterfly_stage" that takes data as List[Complex], length as Integer, twiddles as List[Complex], num_threads as Integer, N as Integer returns Nothing:
    Note: Execute butterfly operations in parallel
    Let groups_per_thread be (N / length) / num_threads
    Let thread_results be List[List[Complex]]
    
    Note: Launch parallel workers (simplified - actual threading would be more complex)
    For thread_id from 0 to num_threads - 1:
        Let start_group be thread_id * groups_per_thread
        Let end_group be MathCore.min((thread_id + 1) * groups_per_thread, N / length)
        
        Let thread_result be execute_butterfly_range(data, start_group, end_group, length, twiddles, N)
        Call thread_results.append(thread_result)
    
    Note: Merge thread results back into data array
    Call merge_parallel_results(data, thread_results)
```

### Cache-Optimal FFT

Optimizing for memory hierarchy:

```runa
Process called "fft_cache_optimal" that takes input as List[Complex], cache_size as Integer, inverse as Boolean returns List[Complex]:
    Note: Cache-oblivious FFT algorithm
    Let N be input.size()
    If N <= cache_size / 16:  Note: fits in cache with some margin
        Return fft_radix2(input, inverse)  Note: use standard algorithm
    
    Note: Divide-and-conquer approach for cache efficiency
    Let half_size be N / 2
    Let even_samples be List[Complex]
    Let odd_samples be List[Complex]
    
    For i from 0 to N - 1 step 2:
        Call even_samples.append(input[i])
        If i + 1 < N:
            Call odd_samples.append(input[i + 1])
    
    Note: Recursive calls on smaller datasets
    Let even_fft be fft_cache_optimal(even_samples, cache_size, inverse)
    Let odd_fft be fft_cache_optimal(odd_samples, cache_size, inverse)
    
    Note: Combine results with cache-friendly access pattern
    Let result be combine_fft_results_cache_optimal(even_fft, odd_fft, N, inverse)
    
    Return result
```

## Specialized FFT Variants

### Chirp-Z Transform

Generalized FFT for arbitrary frequencies:

```runa
Process called "chirp_z_transform" that takes input as List[Complex], M as Integer, W as Complex, A as Complex returns List[Complex]:
    Note: Chirp-Z transform for evaluating DFT at arbitrary points
    Let N be input.size()
    
    Note: Multiply input by chirp sequence
    Let chirped_input be List[Complex]
    For n from 0 to N - 1:
        Let power_factor be complex_power(A, -n)
        Let chirp_factor be complex_power(W, n * n / 2)
        Let sample be complex_multiply(complex_multiply(input[n], power_factor), chirp_factor)
        Call chirped_input.append(sample)
    
    Note: Convolve with chirp filter using FFT
    Let filter_length be N + M - 1
    Let padded_size be next_power_of_two(filter_length)
    
    Let chirp_filter be generate_chirp_filter(M, W, padded_size)
    Let padded_input be zero_pad(chirped_input, padded_size)
    
    Let input_fft be fft_radix2(padded_input, false)
    Let filter_fft be fft_radix2(chirp_filter, false)
    
    Let convolution_result be List[Complex]
    For i from 0 to padded_size - 1:
        Let product be complex_multiply(input_fft[i], filter_fft[i])
        Call convolution_result.append(product)
    
    Let convolved be fft_radix2(convolution_result, true)
    
    Note: Extract and post-multiply by chirp sequence
    Let result be List[Complex]
    For m from 0 to M - 1:
        Let chirp_factor be complex_power(W, m * m / 2)
        Let sample be complex_multiply(convolved[m], chirp_factor)
        Call result.append(sample)
    
    Return result
```

### Sliding DFT with FFT

Efficient sliding window spectral analysis:

```runa
Process called "sliding_fft_update" that takes old_fft as List[Complex], new_sample as Float, old_sample as Float, window_size as Integer returns List[Complex]:
    Note: Update FFT result for sliding window
    Let updated_fft be List[Complex]
    
    For k from 0 to old_fft.size() - 1:
        Note: Sliding DFT update formula
        Let phase_increment be 2.0 * MathCore.pi() * k / window_size
        Let rotation_factor be Complex with:
            real = MathCore.cos(phase_increment)
            imag = MathCore.sin(phase_increment)
        
        Note: Remove old sample and add new sample
        Let sample_diff be new_sample - old_sample
        Let updated_value be complex_multiply(old_fft[k], rotation_factor)
        Set updated_value to complex_add(updated_value, Complex{real: sample_diff, imag: 0.0})
        
        Call updated_fft.append(updated_value)
    
    Return updated_fft
```

## Performance Analysis and Benchmarking

### FFT Performance Profiling

Measuring and optimizing FFT performance:

```runa
Process called "benchmark_fft_algorithms" that takes sizes as List[Integer], iterations as Integer returns Dictionary[String, List[Float]]:
    Note: Comprehensive FFT algorithm benchmarking
    Let results be Dictionary[String, List[Float]]
    let algorithms be ["radix2", "radix4", "mixed_radix"]
    
    For algorithm in algorithms:
        Let algorithm_times be List[Float]
        
        For size in sizes:
            Let test_data be generate_random_complex_signal(size)
            Let total_time be 0.0
            
            For iteration from 0 to iterations - 1:
                Let start_time be current_time()
                Let fft_result be execute_fft_algorithm(test_data, algorithm)
                Let end_time be current_time()
                Set total_time to total_time + (end_time - start_time)
            
            Let average_time be total_time / iterations
            Call algorithm_times.append(average_time)
        
        Collections.set_item(results, algorithm, algorithm_times)
    
    Return results

Process called "analyze_fft_accuracy" that takes size as Integer, algorithm as String returns Dictionary[String, Float]:
    Note: Verify FFT accuracy using round-trip test
    Let test_signal be generate_test_signal(size)
    
    Note: Forward transform
    Let spectrum be execute_fft_algorithm(test_signal, algorithm)
    
    Note: Inverse transform
    Let reconstructed be execute_ifft_algorithm(spectrum, algorithm)
    
    Note: Compute error metrics
    Let max_error be 0.0
    Let rms_error be 0.0
    
    For i from 0 to size - 1:
        Let error be complex_magnitude(complex_subtract(reconstructed[i], test_signal[i]))
        If error > max_error:
            Set max_error to error
        Set rms_error to rms_error + error * error
    
    Set rms_error to MathCore.sqrt(rms_error / size)
    
    Let accuracy_report be Dictionary[String, Float]
    Collections.set_item(accuracy_report, "max_absolute_error", max_error)
    Collections.set_item(accuracy_report, "rms_error", rms_error)
    Collections.set_item(accuracy_report, "snr_db", -20.0 * MathCore.log10(rms_error + 1e-15))
    
    Return accuracy_report
```

### Memory Usage Analysis

Profiling memory consumption patterns:

```runa
Process called "analyze_fft_memory_usage" that takes size as Integer, algorithm as String returns Dictionary[String, Integer]:
    Note: Analyze memory usage patterns for different FFT algorithms
    Let memory_profile be Dictionary[String, Integer]
    
    Let input_memory be size * 16  Note: complex numbers = 16 bytes each
    Collections.set_item(memory_profile, "input_memory", input_memory)
    
    Let twiddle_memory be estimate_twiddle_memory(size, algorithm)
    Collections.set_item(memory_profile, "twiddle_factors_memory", twiddle_memory)
    
    Let working_memory be estimate_working_memory(size, algorithm)
    Collections.set_item(memory_profile, "working_memory", working_memory)
    
    Let peak_memory be input_memory + twiddle_memory + working_memory
    Collections.set_item(memory_profile, "peak_memory_usage", peak_memory)
    
    Let cache_efficiency be estimate_cache_efficiency(size, algorithm)
    Collections.set_item(memory_profile, "cache_efficiency_percent", cache_efficiency)
    
    Return memory_profile
```

The FFT module provides state-of-the-art implementations optimized for various use cases, from real-time signal processing to large-scale scientific computing, offering the flexibility to choose the most appropriate algorithm for specific performance requirements and computational constraints.