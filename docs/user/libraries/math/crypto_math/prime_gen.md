# Prime Generation Module

The prime generation module provides comprehensive prime number generation and primality testing capabilities essential for cryptographic applications. This module implements state-of-the-art algorithms for generating cryptographically secure primes with various special properties.

## Overview

Prime numbers are fundamental to many cryptographic algorithms including RSA, Diffie-Hellman key exchange, DSA, and elliptic curve cryptography. This module provides efficient generation of primes with specific security properties required for different cryptographic applications.

## Mathematical Foundation

### Primality Testing Theory

The module implements several probabilistic and deterministic primality tests:

- **Miller-Rabin Test**: Probabilistic test based on Fermat's Little Theorem extensions
- **Solovay-Strassen Test**: Uses Jacobi symbols and quadratic residues
- **Deterministic Tests**: For small primes using trial division and optimized sieves

### Prime Generation Methods

- **Random Prime Generation**: Generate random primes of specified bit length
- **Safe Prime Generation**: Primes p where (p-1)/2 is also prime (Sophie Germain primes)
- **Strong Prime Generation**: Primes with additional security properties
- **Provable Prime Generation**: Primes with mathematical proof of primality

## Core Data Structures

### PrimeCandidate

Represents a candidate number undergoing primality testing:

```runa
Type called "PrimeCandidate":
    candidate_value as String             Note: The number being tested
    bit_length as Integer                 Note: Number of bits in the candidate
    generation_method as String          Note: How the candidate was generated
    primality_confidence as Float        Note: Probability that number is prime
    test_results as Dictionary[String, Boolean]  Note: Results from various tests
    generation_parameters as Dictionary[String, String]  Note: Generation parameters
```

### PrimalityTest

Configuration and results for primality testing:

```runa
Type called "PrimalityTest":
    test_name as String                   Note: Name of the primality test
    test_parameters as Dictionary[String, String]  Note: Test-specific parameters
    confidence_level as Float            Note: Statistical confidence in result
    iteration_count as Integer           Note: Number of test iterations
    test_duration as Float               Note: Time taken for the test
    error_probability as Float           Note: Probability of false positive
```

## Basic Usage

### Simple Prime Generation

```runa
Use math.crypto_math.prime_gen as PrimeGen

Note: Generate a random 1024-bit prime
Let prime_1024 be PrimeGen.generate_random_prime(1024)

Note: Generate a prime with high confidence
Let config be PrimeGen.create_generation_config()
config.target_bit_length = 2048
config.confidence_level = 99.9999
Let secure_prime be PrimeGen.generate_prime_with_config(config)
```

### Primality Testing

```runa
Note: Test if a number is prime
Let candidate be "179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947245938479716304835356329624224137216"

Let test_config be PrimeGen.create_test_config()
test_config.test_name = "miller_rabin"
test_config.iteration_count = 64
test_config.confidence_level = 99.9999

Let test_result be PrimeGen.test_primality(candidate, test_config)

Match test_result.result_type:
    Case "probable_prime":
        Note: Number is probably prime with high confidence
        Let confidence be test_result.confidence_level
    Case "composite":
        Note: Number is definitely composite
    Case "error":
        Note: Handle testing error
```

## Advanced Prime Generation

### Safe Prime Generation

```runa
Note: Generate safe primes for cryptographic protocols
Process called "generate_safe_prime" that takes bit_length as Integer returns SafePrime:
    Let attempts be 0
    Let max_attempts be 1000000
    
    While attempts < max_attempts:
        Note: Generate random odd number of required bit length
        Let candidate be PrimeGen.generate_random_odd(bit_length)
        
        Note: Check if (candidate - 1) / 2 is prime (Sophie Germain prime)
        Let sophie_germain be PrimeGen.subtract_one_divide_two(candidate)
        Let sg_test_result be PrimeGen.miller_rabin_test(sophie_germain, 64)
        
        If sg_test_result.is_probable_prime:
            Note: Now test if candidate itself is prime
            Let candidate_test be PrimeGen.miller_rabin_test(candidate, 64)
            
            If candidate_test.is_probable_prime:
                Let safe_prime be SafePrime.create()
                safe_prime.prime_value = candidate
                safe_prime.sophie_germain_prime = sophie_germain
                safe_prime.bit_length = bit_length
                safe_prime.generation_method = "safe_prime_generation"
                Return safe_prime
        
        attempts = attempts + 1
    
    Note: Failed to generate safe prime
    Return PrimeGen.create_error_result("safe_prime_generation_failed")
```

### Strong Prime Generation

```runa
Note: Generate strong primes with additional security properties
Process called "generate_strong_prime" that takes bit_length as Integer returns PrimeCandidate:
    Let config be PrimeGen.create_generation_config()
    config.target_bit_length = bit_length
    config.prime_type = "strong"
    
    Note: Strong prime conditions:
    Note: 1. p - 1 has a large prime factor r
    Note: 2. p + 1 has a large prime factor s  
    Note: 3. r - 1 has a large prime factor t
    
    Let attempts be 0
    While attempts < 100000:
        Note: Generate base prime factors
        Let r be PrimeGen.generate_random_prime(bit_length / 3)
        Let s be PrimeGen.generate_random_prime(bit_length / 3)
        Let t be PrimeGen.generate_random_prime(bit_length / 4)
        
        Note: Construct candidate using Chinese Remainder Theorem
        Let candidate be PrimeGen.construct_strong_prime_candidate(r, s, t, bit_length)
        
        Note: Verify strong prime conditions
        If PrimeGen.verify_strong_prime_conditions(candidate, r, s, t):
            Let primality_test be PrimeGen.miller_rabin_test(candidate, 64)
            If primality_test.is_probable_prime:
                Let result be PrimeCandidate.create()
                result.candidate_value = candidate
                result.generation_method = "strong_prime"
                result.bit_length = bit_length
                Return result
        
        attempts = attempts + 1
    
    Note: Fallback to regular prime generation
    Return PrimeGen.generate_random_prime(bit_length)
```

## Primality Testing Algorithms

### Miller-Rabin Test

```runa
Note: Probabilistic primality test with high confidence
Process called "miller_rabin_test" that takes n as String, iterations as Integer returns PrimalityTest:
    Let test_result be PrimalityTest.create()
    test_result.test_name = "miller_rabin"
    test_result.iteration_count = iterations
    
    Note: Handle small cases
    If PrimeGen.is_small_prime(n):
        test_result.is_probable_prime = true
        test_result.confidence_level = 100.0
        Return test_result
    
    If PrimeGen.is_even(n):
        test_result.is_probable_prime = false
        test_result.confidence_level = 100.0
        Return test_result
    
    Note: Write n - 1 = 2^r * d where d is odd
    Let n_minus_1 be PrimeGen.subtract_big_integer(n, "1")
    Let r be 0
    Let d be n_minus_1
    
    While PrimeGen.is_even(d):
        r = r + 1
        d = PrimeGen.divide_by_two(d)
    
    Note: Perform Miller-Rabin iterations
    Let composite_witnesses be 0
    For iteration from 1 to iterations:
        Let a be PrimeGen.random_range("2", PrimeGen.subtract_big_integer(n, "2"))
        Let x be PrimeGen.modular_exponentiation(a, d, n)
        
        If x == "1" or x == n_minus_1:
            Continue  Note: This witness passed
        
        Let composite_indicated be true
        For j from 0 to (r - 2):
            x = PrimeGen.modular_multiply(x, x, n)
            If x == n_minus_1:
                composite_indicated = false
                Break
        
        If composite_indicated:
            composite_witnesses = composite_witnesses + 1
    
    Note: Calculate confidence based on results
    If composite_witnesses == 0:
        test_result.is_probable_prime = true
        test_result.error_probability = PrimeGen.calculate_error_probability(iterations)
        test_result.confidence_level = 100.0 - (test_result.error_probability * 100.0)
    Otherwise:
        test_result.is_probable_prime = false
        test_result.confidence_level = 100.0
    
    Return test_result
```

### Solovay-Strassen Test

```runa
Note: Alternative probabilistic primality test using Jacobi symbols
Process called "solovay_strassen_test" that takes n as String, iterations as Integer returns PrimalityTest:
    Let test_result be PrimalityTest.create()
    test_result.test_name = "solovay_strassen"
    test_result.iteration_count = iterations
    
    Note: Handle trivial cases
    If n == "2":
        test_result.is_probable_prime = true
        test_result.confidence_level = 100.0
        Return test_result
    
    If PrimeGen.is_even(n) or PrimeGen.compare_big_integer(n, "2") < 0:
        test_result.is_probable_prime = false
        test_result.confidence_level = 100.0
        Return test_result
    
    Note: Perform Solovay-Strassen iterations
    Let failures be 0
    For iteration from 1 to iterations:
        Let a be PrimeGen.random_range("2", PrimeGen.subtract_big_integer(n, "1"))
        
        Note: Calculate Jacobi symbol (a/n)
        Let jacobi_symbol be PrimeGen.calculate_jacobi_symbol(a, n)
        
        Note: Calculate a^((n-1)/2) mod n
        Let n_minus_1 be PrimeGen.subtract_big_integer(n, "1")
        Let exponent be PrimeGen.divide_by_two(n_minus_1)
        Let modular_result be PrimeGen.modular_exponentiation(a, exponent, n)
        
        Note: Convert Jacobi symbol to modular form
        Let jacobi_mod_n be PrimeGen.modular_arithmetic(String.from_integer(jacobi_symbol), n)
        
        If modular_result != jacobi_mod_n:
            failures = failures + 1
    
    If failures == 0:
        test_result.is_probable_prime = true
        test_result.error_probability = PrimeGen.power_float(0.5, Float.from_integer(iterations))
        test_result.confidence_level = 100.0 - (test_result.error_probability * 100.0)
    Otherwise:
        test_result.is_probable_prime = false
        test_result.confidence_level = 100.0
    
    Return test_result
```

## Cryptographic Prime Requirements

### RSA Prime Generation

```runa
Note: Generate primes suitable for RSA key generation
Process called "generate_rsa_primes" that takes key_size as Integer returns Dictionary[String, String]:
    Let prime_bit_length be key_size / 2
    Let primes be Dictionary[String, String].create()
    
    Note: Generate first prime
    Let p be PrimeGen.generate_random_prime(prime_bit_length)
    
    Note: Generate second prime with constraints
    Let q_attempts be 0
    While q_attempts < 10000:
        Let q be PrimeGen.generate_random_prime(prime_bit_length)
        
        Note: Ensure |p - q| is sufficiently large
        Let difference be PrimeGen.absolute_difference(p, q)
        Let min_difference be PrimeGen.power_big_integer("2", String.from_integer(prime_bit_length - 100))
        
        If PrimeGen.compare_big_integer(difference, min_difference) > 0:
            Note: Verify gcd(p-1, q-1) is small
            Let p_minus_1 be PrimeGen.subtract_big_integer(p, "1")
            Let q_minus_1 be PrimeGen.subtract_big_integer(q, "1")
            Let gcd_result be PrimeGen.greatest_common_divisor(p_minus_1, q_minus_1)
            
            If PrimeGen.compare_big_integer(gcd_result, "65536") <= 0:
                primes["p"] = p
                primes["q"] = q
                primes["bit_length"] = String.from_integer(prime_bit_length)
                Return primes
        
        q_attempts = q_attempts + 1
    
    Note: Fallback if constraints cannot be satisfied
    primes["p"] = p
    primes["q"] = PrimeGen.generate_random_prime(prime_bit_length)
    Return primes
```

### Discrete Logarithm Secure Primes

```runa
Note: Generate primes for discrete logarithm-based systems
Process called "generate_dl_secure_prime" that takes bit_length as Integer returns Dictionary[String, String]:
    Let result be Dictionary[String, String].create()
    
    Note: Generate safe prime p = 2q + 1 where q is also prime
    Let safe_prime_result be PrimeGen.generate_safe_prime(bit_length)
    Let p be safe_prime_result.prime_value
    Let q be safe_prime_result.sophie_germain_prime
    
    Note: Find a generator for the multiplicative group Z_p*
    Let generator_found be false
    For candidate_g from 2 to 100:
        Let g be String.from_integer(candidate_g)
        
        Note: Test if g has order q (not 1, 2, or q)
        Let g_squared be PrimeGen.modular_exponentiation(g, "2", p)
        Let g_to_q be PrimeGen.modular_exponentiation(g, q, p)
        
        If g_squared != "1" and g_to_q != "1":
            result["prime"] = p
            result["subgroup_prime"] = q
            result["generator"] = g
            result["bit_length"] = String.from_integer(bit_length)
            generator_found = true
            Break
    
    If not generator_found:
        Note: Use standard generator 2 (usually works for safe primes)
        result["prime"] = p
        result["subgroup_prime"] = q
        result["generator"] = "2"
        result["bit_length"] = String.from_integer(bit_length)
    
    Return result
```

## Performance Optimization

### Sieve-Based Generation

```runa
Note: Use sieve methods for efficient prime generation
Process called "sieve_prime_generation" that takes min_value as String, max_value as String returns List[String]:
    Let range_size be PrimeGen.subtract_big_integer(max_value, min_value)
    Let sieve_limit be PrimeGen.integer_square_root(max_value)
    
    Note: Generate small primes for sieving
    Let small_primes be PrimeGen.sieve_of_eratosthenes(sieve_limit)
    
    Note: Initialize candidate array
    Let candidates be List[Boolean].create_with_size(PrimeGen.big_integer_to_int(range_size))
    For i from 0 to candidates.size:
        candidates[i] = true
    
    Note: Sieve with small primes
    For prime in small_primes:
        Let prime_value be String.from_integer(prime)
        Let start_multiple be PrimeGen.ceiling_divide(min_value, prime_value)
        start_multiple = PrimeGen.multiply_big_integer(start_multiple, prime_value)
        
        Let current_multiple be start_multiple
        While PrimeGen.compare_big_integer(current_multiple, max_value) <= 0:
            Let index be PrimeGen.subtract_big_integer(current_multiple, min_value)
            Let index_int be PrimeGen.big_integer_to_int(index)
            candidates[index_int] = false
            current_multiple = PrimeGen.add_big_integer(current_multiple, prime_value)
    
    Note: Collect remaining candidates
    Let prime_candidates be List[String].create()
    For i from 0 to candidates.size:
        If candidates[i]:
            Let candidate_value be PrimeGen.add_big_integer(min_value, String.from_integer(i))
            prime_candidates.add(candidate_value)
    
    Return prime_candidates
```

### Parallel Prime Testing

```runa
Note: Parallel primality testing for multiple candidates
Process called "parallel_prime_test" that takes candidates as List[String], thread_count as Integer returns List[PrimalityTest]:
    Let results be List[PrimalityTest].create()
    Let chunk_size be candidates.size / thread_count
    
    Note: Divide work among threads
    Let thread_tasks be List[List[String]].create()
    For thread_id from 0 to thread_count:
        Let start_index be thread_id * chunk_size
        Let end_index be (thread_id + 1) * chunk_size
        If thread_id == thread_count - 1:
            end_index = candidates.size
        
        Let thread_chunk be List[String].create()
        For i from start_index to end_index:
            thread_chunk.add(candidates[i])
        thread_tasks.add(thread_chunk)
    
    Note: Execute parallel testing
    Let thread_results be PrimeGen.execute_parallel_testing(thread_tasks)
    
    Note: Combine results
    For thread_result in thread_results:
        For test_result in thread_result:
            results.add(test_result)
    
    Return results
```

## Error Handling and Validation

### Input Validation

```runa
Note: Validate prime generation parameters
Process called "validate_generation_parameters" that takes config as PrimeGenerationConfig returns Boolean:
    Note: Check bit length requirements
    If config.target_bit_length < 64:
        Return false  Note: Too small for cryptographic use
    
    If config.target_bit_length > 8192:
        Return false  Note: Impractically large
    
    Note: Validate prime type
    Match config.prime_type:
        Case "random":
        Case "safe":
        Case "strong":
        Case "provable":
            Note: Valid types
        Otherwise:
            Return false
    
    Note: Check security requirements
    Let confidence_level be config.security_requirements["confidence_level"]
    If confidence_level == "" or Float.parse(confidence_level) < 99.0:
        Return false  Note: Insufficient confidence
    
    Return true
```

### Generation Quality Assessment

```runa
Note: Assess quality of generated primes
Process called "assess_prime_quality" that takes prime as String returns Dictionary[String, String]:
    Let assessment be Dictionary[String, String].create()
    
    Note: Check bit length
    Let actual_bit_length be PrimeGen.bit_length(prime)
    assessment["bit_length"] = String.from_integer(actual_bit_length)
    
    Note: Test for special forms
    Let prime_minus_1 be PrimeGen.subtract_big_integer(prime, "1")
    Let factorization be PrimeGen.partial_factorization(prime_minus_1)
    assessment["p_minus_1_factors"] = factorization
    
    Note: Check if it's a safe prime
    Let half_value be PrimeGen.divide_by_two(prime_minus_1)
    Let is_safe be PrimeGen.miller_rabin_test(half_value, 32)
    assessment["is_safe_prime"] = String.from_boolean(is_safe.is_probable_prime)
    
    Note: Entropy analysis
    Let entropy_score be PrimeGen.calculate_entropy(prime)
    assessment["entropy_score"] = String.from_float(entropy_score)
    
    Return assessment
```

## Related Documentation

- **[Finite Fields](finite_fields.md)** - Finite field arithmetic using generated primes
- **[Elliptic Curves](elliptic_curves.md)** - Elliptic curves over prime fields
- **[Hash Theory](hash_theory.md)** - Hash functions with prime-based constructions
- **[Protocols](protocols.md)** - Cryptographic protocols requiring secure primes
- **[Lattice](lattice.md)** - Lattice-based cryptography with prime moduli