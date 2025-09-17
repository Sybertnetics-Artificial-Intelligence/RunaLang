# Math Precision BigInteger Module

## Overview

The `math/precision/biginteger` module provides arbitrary precision integer arithmetic that can handle integers of unlimited size, constrained only by available memory. It implements efficient algorithms for large integer operations including multiplication, division, modular arithmetic, prime testing, and factorization, making it essential for cryptographic applications, number theory computations, and mathematical software requiring exact integer arithmetic.

## Key Features

- **Unlimited Size**: Integer values constrained only by available memory
- **Cryptographic Grade**: Secure operations for cryptographic applications
- **Prime Testing**: Multiple algorithms including Miller-Rabin and Lucas-Lehmer
- **Modular Arithmetic**: Efficient operations for cryptographic protocols
- **Factorization**: Advanced algorithms including Pollard's rho and quadratic sieve
- **Bitwise Operations**: Full bitwise manipulation support
- **Base Conversion**: Conversion between different number bases
- **Performance Optimized**: Karatsuba multiplication, Barrett reduction

## Data Types

### BigInteger
Represents an arbitrary precision integer:
```runa
Type called "BigInteger":
    digits as Array[Integer]     Note: Base digits for computation
    is_negative as Boolean       Note: Sign of the integer
    digit_count as Integer       Note: Number of significant digits
```

### ArithmeticResult
Result container with overflow detection:
```runa
Type called "ArithmeticResult":
    result as BigInteger         Note: Computation result
    has_overflow as Boolean      Note: Whether overflow occurred
    error_code as String         Note: Error details if applicable
```

### ModularResult
Result of modular arithmetic operations:
```runa
Type called "ModularResult":
    quotient as BigInteger       Note: Division quotient
    remainder as BigInteger      Note: Division remainder
    gcd as BigInteger           Note: Greatest common divisor
```

### PrimalityResult
Result of primality testing:
```runa
Type called "PrimalityResult":
    is_prime as Boolean         Note: Whether number is prime
    confidence as Float         Note: Probability of correctness
    method_used as String       Note: Testing algorithm used
    witnesses as Array[BigInteger]  Note: Witnesses for composite numbers
```

## Basic Operations

### Creating BigInteger Values
```runa
Import "math/precision/biginteger" as BigInteger

Note: Create from different sources
Let small_int be BigInteger.create_from_integer(42)
Let large_string be BigInteger.create_from_string("123456789012345678901234567890")
Let hex_value be BigInteger.create_from_string("DEADBEEF", 16)
Let binary_value be BigInteger.create_from_string("1010101010", 2)

Note: Create special values
Let zero be BigInteger.ZERO
Let one be BigInteger.ONE
Let negative_one be BigInteger.NEGATIVE_ONE

Display "Large integer: " joined with BigInteger.to_string(large_string, 10)
Display "Hex value: " joined with BigInteger.to_string(hex_value, 10)
```

### Arithmetic Operations
```runa
Note: Basic arithmetic operations
Let a be BigInteger.create_from_string("12345678901234567890")
Let b be BigInteger.create_from_string("98765432109876543210")

Let sum be BigInteger.add(a, b)
Let difference be BigInteger.subtract(a, b)
Let product be BigInteger.multiply(a, b)
Let quotient_remainder be BigInteger.divide_with_remainder(b, a)

Display "Sum: " joined with BigInteger.to_string(sum, 10)
Display "Product: " joined with BigInteger.to_string(product, 10)
Display "Quotient: " joined with BigInteger.to_string(quotient_remainder.quotient, 10)
Display "Remainder: " joined with BigInteger.to_string(quotient_remainder.remainder, 10)
```

### Power Operations
```runa
Note: Exponentiation operations
Let base be BigInteger.create_from_string("123")
Let exponent be BigInteger.create_from_string("45")

Let power_result be BigInteger.power(base, exponent)
Display "123^45 = " joined with BigInteger.to_string(power_result, 10)

Note: Modular exponentiation (efficient for large numbers)
Let modulus be BigInteger.create_from_string("1000000007")
Let mod_power be BigInteger.mod_power(base, exponent, modulus)
Display "123^45 mod 1000000007 = " joined with BigInteger.to_string(mod_power, 10)
```

## Advanced Mathematical Operations

### Greatest Common Divisor and Least Common Multiple
```runa
Note: GCD and LCM calculations
Let x be BigInteger.create_from_string("1071")
Let y be BigInteger.create_from_string("462")

Let gcd_result be BigInteger.gcd(x, y)
Let lcm_result be BigInteger.lcm(x, y)

Display "GCD(1071, 462) = " joined with BigInteger.to_string(gcd_result, 10)
Display "LCM(1071, 462) = " joined with BigInteger.to_string(lcm_result, 10)

Note: Extended Euclidean algorithm
Let extended_result be BigInteger.extended_gcd(x, y)
Display "Bézout coefficients: " joined with BigInteger.to_string(extended_result.coefficient_x, 10) joined with ", " joined with BigInteger.to_string(extended_result.coefficient_y, 10)
```

### Modular Arithmetic
```runa
Note: Comprehensive modular operations
Let a be BigInteger.create_from_string("12345")
Let b be BigInteger.create_from_string("67890")
Let m be BigInteger.create_from_string("97")

Let mod_sum be BigInteger.mod_add(a, b, m)
Let mod_product be BigInteger.mod_multiply(a, b, m)
Let mod_inverse be BigInteger.mod_inverse(a, m)

Display "(12345 + 67890) mod 97 = " joined with BigInteger.to_string(mod_sum, 10)
Display "(12345 * 67890) mod 97 = " joined with BigInteger.to_string(mod_product, 10)

If BigInteger.is_coprime(a, m):
    Display "Modular inverse of 12345 mod 97 = " joined with BigInteger.to_string(mod_inverse, 10)
```

### Root Calculations
```runa
Note: Integer roots
Let large_number be BigInteger.create_from_string("123456789012345678901234567890")

Let square_root be BigInteger.sqrt(large_number)
Let cube_root be BigInteger.nth_root(large_number, 3)

Display "Square root: " joined with BigInteger.to_string(square_root, 10)
Display "Cube root: " joined with BigInteger.to_string(cube_root, 10)

Note: Perfect power testing
Let is_perfect_square be BigInteger.is_perfect_square(large_number)
Let is_perfect_cube be BigInteger.is_perfect_power(large_number, 3)

Display "Is perfect square: " joined with String(is_perfect_square)
Display "Is perfect cube: " joined with String(is_perfect_cube)
```

## Prime Number Operations

### Primality Testing
```runa
Note: Various primality tests
Let candidate be BigInteger.create_from_string("982451653")

Note: Deterministic test for small numbers
Let is_prime_deterministic be BigInteger.is_prime_deterministic(candidate)

Note: Probabilistic Miller-Rabin test
Let miller_rabin_result be BigInteger.miller_rabin_test(candidate, 20)  Note: 20 rounds

Note: Lucas-Lehmer test (for Mersenne numbers)
Let mersenne_exponent be 31
Let mersenne_prime be BigInteger.subtract(BigInteger.power(BigInteger.create_from_integer(2), BigInteger.create_from_integer(mersenne_exponent)), BigInteger.ONE)
Let is_mersenne_prime be BigInteger.lucas_lehmer_test(mersenne_exponent)

Display "Is prime (deterministic): " joined with String(is_prime_deterministic)
Display "Miller-Rabin confidence: " joined with String(miller_rabin_result.confidence)
Display "Mersenne 2^31-1 is prime: " joined with String(is_mersenne_prime)
```

### Prime Generation
```runa
Note: Generate random primes
Let bit_length be 1024
Let random_prime be BigInteger.generate_random_prime(bit_length)
Display "Random 1024-bit prime: " joined with BigInteger.to_string(random_prime, 16)

Note: Generate safe primes (primes p where (p-1)/2 is also prime)
Let safe_prime be BigInteger.generate_safe_prime(512)
Display "512-bit safe prime: " joined with BigInteger.to_string(safe_prime, 16)

Note: Generate prime with specific properties
Let prime_config be PrimeGenerationConfig with:
    bit_length: 256
    ensure_safe: true
    avoid_weak_primes: true
    custom_tests: Array[String]()

prime_config.custom_tests.add("strong_prime_test")
Let custom_prime be BigInteger.generate_prime_with_config(prime_config)
```

### Prime Factorization
```runa
Note: Factor large integers
Let composite be BigInteger.create_from_string("1234567890123456789")

Note: Trial division for small factors
Let small_factors be BigInteger.trial_division(composite, 10000)

Note: Pollard's rho algorithm for larger factors
Let rho_factors be BigInteger.pollard_rho_factorization(composite)

Note: Quadratic sieve for very large numbers
If BigInteger.digit_count(composite) > 50:
    Let qs_factors be BigInteger.quadratic_sieve_factorization(composite)

Display "Small factors found: " joined with String(small_factors.length)
For Each factor in rho_factors:
    Display "Rho factor: " joined with BigInteger.to_string(factor, 10)
```

## Bitwise Operations

### Bit Manipulation
```runa
Note: Bitwise operations on large integers
Let a be BigInteger.create_from_string("0xFF00AA55", 16)
Let b be BigInteger.create_from_string("0x00FFAA55", 16)

Let bitwise_and be BigInteger.bitwise_and(a, b)
Let bitwise_or be BigInteger.bitwise_or(a, b)
Let bitwise_xor be BigInteger.bitwise_xor(a, b)
Let bitwise_not be BigInteger.bitwise_not(a)

Display "AND: " joined with BigInteger.to_string(bitwise_and, 16)
Display "OR: " joined with BigInteger.to_string(bitwise_or, 16)
Display "XOR: " joined with BigInteger.to_string(bitwise_xor, 16)
```

### Bit Shifting
```runa
Note: Shift operations
Let value be BigInteger.create_from_string("12345678901234567890")

Let left_shifted be BigInteger.shift_left(value, 10)   Note: Multiply by 2^10
Let right_shifted be BigInteger.shift_right(value, 5)  Note: Divide by 2^5

Display "Left shifted by 10: " joined with BigInteger.to_string(left_shifted, 10)
Display "Right shifted by 5: " joined with BigInteger.to_string(right_shifted, 10)

Note: Bit counting operations
Let bit_count be BigInteger.bit_length(value)
Let hamming_weight be BigInteger.popcount(value)  Note: Number of 1 bits
Let trailing_zeros be BigInteger.trailing_zero_count(value)

Display "Bit length: " joined with String(bit_count)
Display "Hamming weight: " joined with String(hamming_weight)
Display "Trailing zeros: " joined with String(trailing_zeros)
```

### Bit Testing
```runa
Note: Individual bit operations
Let number be BigInteger.create_from_string("1023")  Note: Binary: 1111111111

For i from 0 to 15:
    Let bit_value be BigInteger.test_bit(number, i)
    Display "Bit " joined with String(i) joined with ": " joined with String(bit_value)

Note: Set and clear bits
Let modified be BigInteger.set_bit(number, 20)     Note: Set bit 20
Set modified to BigInteger.clear_bit(modified, 5)  Note: Clear bit 5
Set modified to BigInteger.flip_bit(modified, 10)  Note: Flip bit 10

Display "Modified: " joined with BigInteger.to_string(modified, 2)
```

## Cryptographic Applications

### RSA Key Generation
```runa
Note: Generate RSA key pair
Process called "generate_rsa_keypair" that takes key_size as Integer returns RSAKeyPair:
    Note: Generate two large primes
    Let p be BigInteger.generate_random_prime(key_size / 2)
    Let q be BigInteger.generate_random_prime(key_size / 2)
    
    Note: Calculate modulus
    Let n be BigInteger.multiply(p, q)
    
    Note: Calculate totient
    Let p_minus_1 be BigInteger.subtract(p, BigInteger.ONE)
    Let q_minus_1 be BigInteger.subtract(q, BigInteger.ONE)
    Let phi_n be BigInteger.multiply(p_minus_1, q_minus_1)
    
    Note: Choose public exponent
    Let e be BigInteger.create_from_integer(65537)  Note: Common choice
    
    Note: Calculate private exponent
    Let d be BigInteger.mod_inverse(e, phi_n)
    
    Return RSAKeyPair with:
        public_key: RSAPublicKey with (n: n, e: e)
        private_key: RSAPrivateKey with (n: n, d: d, p: p, q: q)

Let rsa_keys be generate_rsa_keypair(2048)
Display "RSA modulus: " joined with BigInteger.to_string(rsa_keys.public_key.n, 16)
```

### Discrete Logarithm
```runa
Note: Discrete logarithm calculations
Let base be BigInteger.create_from_string("5")
Let result be BigInteger.create_from_string("3125")
Let modulus be BigInteger.create_from_string("7919")

Note: Find x such that base^x ≡ result (mod modulus)
Let discrete_log be BigInteger.discrete_logarithm(base, result, modulus)

If discrete_log.found:
    Display "Discrete log: " joined with BigInteger.to_string(discrete_log.value, 10)
    
    Note: Verify the result
    Let verification be BigInteger.mod_power(base, discrete_log.value, modulus)
    Let is_correct be BigInteger.equals(verification, result)
    Display "Verification: " joined with String(is_correct)
```

### Diffie-Hellman Key Exchange
```runa
Note: Simulate Diffie-Hellman key exchange
Let prime_modulus be BigInteger.generate_safe_prime(1024)
Let generator be BigInteger.create_from_integer(2)

Note: Alice's keys
Let alice_private be BigInteger.generate_random_range(BigInteger.create_from_integer(2), 
    BigInteger.subtract(prime_modulus, BigInteger.ONE))
Let alice_public be BigInteger.mod_power(generator, alice_private, prime_modulus)

Note: Bob's keys
Let bob_private be BigInteger.generate_random_range(BigInteger.create_from_integer(2),
    BigInteger.subtract(prime_modulus, BigInteger.ONE))
Let bob_public be BigInteger.mod_power(generator, bob_private, prime_modulus)

Note: Shared secret calculation
Let alice_shared be BigInteger.mod_power(bob_public, alice_private, prime_modulus)
Let bob_shared be BigInteger.mod_power(alice_public, bob_private, prime_modulus)

Let keys_match be BigInteger.equals(alice_shared, bob_shared)
Display "Shared secrets match: " joined with String(keys_match)
```

## Number Theory Applications

### Chinese Remainder Theorem
```runa
Note: Solve system of congruences
Let remainders be Array[BigInteger]()
Let moduli be Array[BigInteger]()

remainders.add(BigInteger.create_from_string("2"))   Note: x ≡ 2 (mod 3)
remainders.add(BigInteger.create_from_string("3"))   Note: x ≡ 3 (mod 5)  
remainders.add(BigInteger.create_from_string("2"))   Note: x ≡ 2 (mod 7)

moduli.add(BigInteger.create_from_string("3"))
moduli.add(BigInteger.create_from_string("5"))
moduli.add(BigInteger.create_from_string("7"))

Let crt_solution be BigInteger.chinese_remainder_theorem(remainders, moduli)
Display "CRT solution: " joined with BigInteger.to_string(crt_solution, 10)

Note: Verify the solution
For i from 0 to remainders.length - 1:
    Let verification be BigInteger.mod(crt_solution, moduli[i])
    Let is_correct be BigInteger.equals(verification, remainders[i])
    Display "Congruence " joined with String(i) joined with " verified: " joined with String(is_correct)
```

### Jacobi and Legendre Symbols
```runa
Note: Quadratic residue testing
Let a be BigInteger.create_from_string("1001")
Let n be BigInteger.create_from_string("9907")  Note: Prime

Let jacobi_symbol be BigInteger.jacobi_symbol(a, n)
Let legendre_symbol be BigInteger.legendre_symbol(a, n)

Display "Jacobi symbol (1001/9907): " joined with String(jacobi_symbol)
Display "Legendre symbol (1001/9907): " joined with String(legendre_symbol)

Note: Find quadratic residues
If jacobi_symbol == 1:
    Let sqrt_mod be BigInteger.sqrt_mod_prime(a, n)
    If sqrt_mod.exists:
        Display "Square root mod p: " joined with BigInteger.to_string(sqrt_mod.value, 10)
```

### Continued Fractions
```runa
Note: Generate continued fraction for rational number
Let numerator be BigInteger.create_from_string("355")
Let denominator be BigInteger.create_from_string("113")  Note: Approximation of π

Let cf_coefficients be BigInteger.rational_to_continued_fraction(numerator, denominator)

Display "Continued fraction coefficients:"
For Each coefficient in cf_coefficients:
    Display "  " joined with BigInteger.to_string(coefficient, 10)

Note: Reconstruct from continued fraction
Let reconstructed be BigInteger.continued_fraction_to_rational(cf_coefficients)
Let matches_original be BigInteger.equals(reconstructed.numerator, numerator) and 
                        BigInteger.equals(reconstructed.denominator, denominator)
Display "Reconstruction successful: " joined with String(matches_original)
```

## Performance Optimization

### Algorithm Selection
```runa
Note: Automatic algorithm selection based on operand size
Process called "multiply_optimized" that takes a as BigInteger, b as BigInteger returns BigInteger:
    Let a_digits be BigInteger.digit_count(a)
    Let b_digits be BigInteger.digit_count(b)
    Let max_digits be Integer.max(a_digits, b_digits)
    
    If max_digits < 100:
        Return BigInteger.multiply_schoolbook(a, b)
    Otherwise If max_digits < 1000:
        Return BigInteger.multiply_karatsuba(a, b)
    Otherwise:
        Return BigInteger.multiply_fft(a, b)

Let large_a be BigInteger.create_from_string("123456789" * 100)  Note: Very large number
Let large_b be BigInteger.create_from_string("987654321" * 100)
Let optimized_product be multiply_optimized(large_a, large_b)
```

### Memory Management
```runa
Note: Configure memory usage for large computations
Let memory_config be BigIntegerMemoryConfig with:
    digit_pool_size: 10000
    enable_digit_pooling: true
    auto_shrink: true
    gc_threshold: 100000000  Note: bytes

BigInteger.configure_memory(memory_config)

Note: Monitor memory usage
Let memory_stats be BigInteger.get_memory_statistics()
Display "Total memory allocated: " joined with String(memory_stats.total_bytes)
Display "Pooled digits available: " joined with String(memory_stats.pooled_digits)
Display "Active BigInteger objects: " joined with String(memory_stats.active_objects)
```

### Parallel Operations
```runa
Note: Parallel computation for independent operations
Let operands be Array[BigInteger]()
For i from 1 to 100:
    operands.add(BigInteger.create_from_string(String(i * 1234567890)))

Note: Parallel sum using multiple threads
Let parallel_config be ParallelConfig with:
    thread_count: 4
    chunk_size: 25

Let parallel_sum be BigInteger.parallel_sum(operands, parallel_config)
Let sequential_sum be BigInteger.sum_array(operands)

Let results_match be BigInteger.equals(parallel_sum, sequential_sum)
Display "Parallel computation verified: " joined with String(results_match)
```

## Conversion and Representation

### Base Conversion
```runa
Note: Convert between different bases
Let decimal_number be BigInteger.create_from_string("1234567890123456789")

Let binary_repr be BigInteger.to_string(decimal_number, 2)
Let octal_repr be BigInteger.to_string(decimal_number, 8)
Let hex_repr be BigInteger.to_string(decimal_number, 16)
Let base36_repr be BigInteger.to_string(decimal_number, 36)

Display "Binary: " joined with binary_repr
Display "Octal: " joined with octal_repr
Display "Hexadecimal: " joined with hex_repr
Display "Base 36: " joined with base36_repr

Note: Parse from different bases
Let from_binary be BigInteger.create_from_string(binary_repr, 2)
Let from_hex be BigInteger.create_from_string(hex_repr, 16)

Let conversion_correct be BigInteger.equals(decimal_number, from_binary) and 
                         BigInteger.equals(decimal_number, from_hex)
Display "Base conversion verified: " joined with String(conversion_correct)
```

### Special Representations
```runa
Note: Specialized string formats
Let large_number be BigInteger.create_from_string("123456789012345678901234567890")

Note: Scientific notation
Let scientific be BigInteger.to_scientific_notation(large_number)
Display "Scientific: " joined with scientific

Note: Comma-separated format
Let formatted be BigInteger.to_formatted_string(large_number, ",")
Display "Formatted: " joined with formatted

Note: Roman numerals (for small numbers)
Let small_number be BigInteger.create_from_integer(1994)
Let roman = BigInteger.to_roman_numerals(small_number)
Display "Roman: " joined with roman
```

## Error Handling

### Exception Types
The BigInteger module defines several specific exception types:

- **InvalidArgument**: Invalid input parameters
- **DivisionByZero**: Division by zero attempted  
- **ArithmeticOverflow**: Result exceeds implementation limits
- **InvalidBase**: Invalid base for number conversion
- **ComputationTimeout**: Operation exceeded time limits

### Error Handling Examples
```runa
Try:
    Let invalid_base be BigInteger.create_from_string("123", 1)  Note: Invalid base
Catch Errors.InvalidBase as error:
    Display "Invalid base error: " joined with error.message
    Display "Valid bases: 2-36"

Try:
    Let zero_divisor be BigInteger.ZERO
    Let quotient be BigInteger.divide(BigInteger.create_from_integer(100), zero_divisor)
Catch Errors.DivisionByZero as error:
    Display "Division by zero: " joined with error.message
    Let suggestion be SuggestionEngine.get_suggestion(error)
    Display "Suggestion: " joined with suggestion

Try:
    Let timeout_config be ComputationConfig with:
        max_execution_time: 5000  Note: 5 seconds
        
    Let very_large_computation be BigInteger.factorial_with_timeout(100000, timeout_config)
Catch Errors.ComputationTimeout as error:
    Display "Computation timed out: " joined with error.message
    Display "Consider using approximation methods for very large factorials"
```

## Testing and Validation

### Unit Testing
```runa
Note: Comprehensive testing suite
Process called "test_biginteger_arithmetic" returns Boolean:
    Let test_passed be true
    
    Note: Test basic arithmetic
    Let a be BigInteger.create_from_string("123456789")
    Let b be BigInteger.create_from_string("987654321")
    
    Let sum be BigInteger.add(a, b)
    Let expected_sum be BigInteger.create_from_string("1111111110")
    
    If not BigInteger.equals(sum, expected_sum):
        Display "Addition test failed"
        Set test_passed to false
    
    Note: Test multiplication
    Let product be BigInteger.multiply(a, b)
    Let verified_product be BigInteger.create_from_string("121932631112635269")
    
    If not BigInteger.equals(product, verified_product):
        Display "Multiplication test failed" 
        Set test_passed to false
    
    Return test_passed

Let arithmetic_tests_pass be test_biginteger_arithmetic()
Display "Arithmetic tests: " joined with String(arithmetic_tests_pass)
```

### Cryptographic Validation
```runa
Note: Test cryptographic functions
Process called "test_rsa_encryption" that takes key_size as Integer returns Boolean:
    Let keys be generate_rsa_keypair(key_size)
    
    Note: Test message encryption/decryption
    Let message be BigInteger.create_from_string("Hello World", 256)  Note: Convert from ASCII
    
    Let encrypted be BigInteger.mod_power(message, keys.public_key.e, keys.public_key.n)
    Let decrypted be BigInteger.mod_power(encrypted, keys.private_key.d, keys.private_key.n)
    
    Return BigInteger.equals(message, decrypted)

Let rsa_test_passes be test_rsa_encryption(1024)
Display "RSA encryption test: " joined with String(rsa_test_passes)
```

## Best Practices

### 1. Choose Appropriate Algorithms
```runa
Note: Algorithm selection guidelines
Process called "recommend_multiplication_algorithm" that takes operand_size as Integer returns String:
    If operand_size < 50:
        Return "schoolbook"          Note: Simple O(n²) for small numbers
    Otherwise If operand_size < 500:
        Return "karatsuba"           Note: O(n^1.585) for medium numbers
    Otherwise If operand_size < 10000:
        Return "toom_cook"           Note: O(n^1.465) for large numbers
    Otherwise:
        Return "fft"                 Note: O(n log n) for very large numbers
```

### 2. Memory Management
```runa
Note: Manage memory efficiently
Process called "optimize_biginteger_memory" that takes computation_size as String returns MemoryConfig:
    Let config be MemoryConfig()
    
    If computation_size == "small":
        config.initial_pool_size = 100
        config.growth_factor = 1.2
    Otherwise If computation_size == "large":
        config.initial_pool_size = 10000  
        config.growth_factor = 1.5
        config.enable_compression = true
    Otherwise:  Note: "massive"
        config.initial_pool_size = 100000
        config.growth_factor = 2.0
        config.enable_compression = true
        config.use_memory_mapping = true
    
    Return config
```

### 3. Security Considerations
```runa
Note: Secure random number generation
Process called "generate_cryptographic_integer" that takes bit_length as Integer returns BigInteger:
    Note: Use cryptographically secure random source
    Let secure_random be SecureRandom.create_system_random()
    
    Let random_bytes be secure_random.generate_bytes(bit_length / 8)
    Let random_bigint be BigInteger.create_from_bytes(random_bytes)
    
    Note: Ensure the number has the desired bit length
    Let target_bit_length be BigInteger.create_from_integer(bit_length - 1)
    Let bit_mask be BigInteger.subtract(BigInteger.power(BigInteger.create_from_integer(2), target_bit_length), BigInteger.ONE)
    
    Return BigInteger.bitwise_or(random_bigint, BigInteger.shift_left(BigInteger.ONE, bit_length - 1))
```

### 4. Performance Monitoring
```runa
Note: Benchmark different algorithms
Process called "benchmark_biginteger_operations" returns BenchmarkResults:
    Let results be BenchmarkResults()
    Let test_operands be generate_test_bigintegers(1000)
    
    Note: Benchmark multiplication algorithms
    Let schoolbook_time be measure_execution_time(fun => BigInteger.multiply_schoolbook(test_operands[0], test_operands[1]))
    Let karatsuba_time be measure_execution_time(fun => BigInteger.multiply_karatsuba(test_operands[0], test_operands[1]))
    
    results.add_result("schoolbook_multiply", schoolbook_time)
    results.add_result("karatsuba_multiply", karatsuba_time)
    
    Return results
```

## Integration Examples

### With Cryptography Module
```runa
Import "math/precision/biginteger" as BigInteger
Import "security/crypto/hash" as Hash

Note: Digital signature using RSA and SHA-256
Process called "rsa_sign_message" that takes message as String, private_key as RSAPrivateKey returns BigInteger:
    Let message_hash be Hash.sha256(message)
    Let hash_bigint be BigInteger.create_from_bytes(message_hash)
    
    Return BigInteger.mod_power(hash_bigint, private_key.d, private_key.n)

Process called "rsa_verify_signature" that takes message as String, signature as BigInteger, public_key as RSAPublicKey returns Boolean:
    Let message_hash be Hash.sha256(message)
    Let hash_bigint be BigInteger.create_from_bytes(message_hash)
    
    Let decrypted_hash be BigInteger.mod_power(signature, public_key.e, public_key.n)
    Return BigInteger.equals(hash_bigint, decrypted_hash)
```

### With Rational Numbers
```runa
Import "math/precision/biginteger" as BigInteger
Import "math/precision/rational" as Rational

Note: Create rational from large integers
Let large_numerator be BigInteger.factorial(100)
Let large_denominator be BigInteger.factorial(99)

Let large_rational be Rational.create_from_bigintegers(large_numerator, large_denominator)
Display "100!/99! = " joined with Rational.to_string(large_rational)
```

The BigInteger module provides the foundation for unlimited precision integer arithmetic in Runa, enabling cryptographic applications, number theory research, and mathematical computations that exceed the limits of standard integer types.