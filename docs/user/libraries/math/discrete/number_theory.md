# Number Theory Module

The Number Theory module provides comprehensive tools for working with integers and their mathematical properties. This module covers fundamental concepts in elementary and analytic number theory, making it essential for cryptography, computational mathematics, and theoretical research.

## Quick Start

```runa
Import "math/discrete/number_theory" as NumberTheory

Note: Basic number theory operations
Let is_prime_result be NumberTheory.is_prime(97)
Let gcd_result be NumberTheory.gcd(48, 18)
Let factors be NumberTheory.prime_factorization(60)

Display "97 is prime: " joined with is_prime_result
Display "GCD of 48 and 18: " joined with gcd_result
Display "Prime factors of 60: " joined with NumberTheory.factors_to_string(factors)
```

## Fundamental Concepts

### Divisibility and GCD

The greatest common divisor and related concepts form the foundation of number theory:

```runa
Import "math/discrete/number_theory" as NT

Note: Calculate GCD using different algorithms
Let gcd_euclidean be NT.gcd_euclidean(1071, 462)
Let gcd_binary be NT.gcd_binary(1071, 462)
Let gcd_extended be NT.extended_gcd(1071, 462)

Display "GCD (Euclidean): " joined with gcd_euclidean
Display "GCD (Binary): " joined with gcd_binary

Note: Extended GCD provides Bézout coefficients
Let coefficients be NT.get_bezout_coefficients(gcd_extended)
Let x be NT.get_x_coefficient(coefficients)
Let y be NT.get_y_coefficient(coefficients)
Display "Bézout coefficients: " joined with x joined with ", " joined with y
```

### Least Common Multiple

```runa
Note: Calculate LCM
Let lcm_result be NT.lcm(12, 18)
Let lcm_multiple be NT.lcm_of_list([4, 6, 8, 12])

Display "LCM of 12 and 18: " joined with lcm_result
Display "LCM of [4,6,8,12]: " joined with lcm_multiple
```

## Prime Numbers and Testing

### Primality Testing

```runa
Note: Various primality testing algorithms
Let is_prime_trial be NT.is_prime_trial_division(1009)
Let is_prime_miller be NT.is_prime_miller_rabin(1009, 20)
Let is_prime_fermat be NT.is_prime_fermat_test(1009, 10)

Display "1009 is prime (trial division): " joined with is_prime_trial
Display "1009 is prime (Miller-Rabin): " joined with is_prime_miller
Display "1009 passes Fermat test: " joined with is_prime_fermat

Note: Handle large numbers efficiently
Let large_prime_candidate be NT.create_large_integer("982451653")
Let is_large_prime be NT.is_prime_lucas_lehmer(large_prime_candidate)
```

### Prime Generation

```runa
Note: Generate primes using various methods
Let primes_sieve be NT.sieve_of_eratosthenes(1000)
Let primes_sundaram be NT.sieve_of_sundaram(1000)
Let twin_primes be NT.find_twin_primes(100)

Display "Number of primes up to 1000: " joined with NT.count_primes(primes_sieve)
Display "Twin primes up to 100:"
NT.display_twin_prime_pairs(twin_primes)

Note: Generate next prime
Let next_prime be NT.next_prime(997)
Let prev_prime be NT.previous_prime(1003)
Display "Next prime after 997: " joined with next_prime
```

### Prime Factorization

```runa
Note: Factor integers completely
Let factorization be NT.prime_factorization(3600)
Let factorization_pollard be NT.pollard_rho_factorization(3599)

Display "Prime factorization of 3600:"
NT.display_prime_factors(factorization)

Note: Factor using different algorithms
Let factors_trial be NT.trial_division_factorization(1001)
Let factors_wheel be NT.wheel_factorization(1001)
```

## Modular Arithmetic

### Basic Modular Operations

```runa
Note: Perform modular arithmetic
Let mod_sum be NT.modular_add(47, 38, 13)
Let mod_mult be NT.modular_multiply(47, 38, 13)
Let mod_power be NT.modular_exponentiation(5, 13, 17)

Display "47 + 38 ≡ " joined with mod_sum joined with " (mod 13)"
Display "47 × 38 ≡ " joined with mod_mult joined with " (mod 13)"
Display "5^13 ≡ " joined with mod_power joined with " (mod 17)"
```

### Modular Inverse

```runa
Note: Calculate modular inverses
Let inverse_extended be NT.modular_inverse_extended_gcd(7, 26)
Let inverse_fermat be NT.modular_inverse_fermat(7, 29)

If NT.has_modular_inverse(inverse_extended):
    Let inv_value be NT.get_inverse_value(inverse_extended)
    Display "7^(-1) ≡ " joined with inv_value joined with " (mod 26)"
Otherwise:
    Display "7 has no modular inverse mod 26"
```

### Chinese Remainder Theorem

```runa
Note: Solve systems of congruences
Let moduli be [3, 5, 7]
Let remainders be [2, 3, 2]
Let crt_solution be NT.chinese_remainder_theorem(remainders, moduli)

Display "Solution to system of congruences: " joined with NT.get_crt_solution(crt_solution)
Display "Verification: " joined with NT.verify_crt_solution(crt_solution, remainders, moduli)
```

## Euler's Function and Carmichael Function

### Totient Function

```runa
Note: Calculate Euler's totient function
Let phi_100 be NT.euler_totient(100)
Let phi_list be NT.totient_values_up_to(20)

Display "φ(100) = " joined with phi_100

Note: Properties of totient function
Let is_multiplicative be NT.verify_totient_multiplicative(12, 35)
Let totient_sum be NT.totient_sum_formula(100)
```

### Carmichael Function

```runa
Note: Calculate Carmichael function
Let lambda_100 be NT.carmichael_function(100)
Let carmichael_numbers be NT.find_carmichael_numbers_up_to(10000)

Display "λ(100) = " joined with lambda_100
Display "Found " joined with NT.count_carmichael_numbers(carmichael_numbers) joined with " Carmichael numbers"
```

## Quadratic Residues and Legendre Symbol

### Legendre Symbol

```runa
Note: Calculate Legendre symbols
Let legendre_3_7 be NT.legendre_symbol(3, 7)
Let legendre_5_11 be NT.legendre_symbol(5, 11)

Display "Legendre symbol (3/7): " joined with legendre_3_7
Display "Legendre symbol (5/11): " joined with legendre_5_11

Note: Check if number is quadratic residue
Let is_qr be NT.is_quadratic_residue(3, 7)
Display "3 is quadratic residue mod 7: " joined with is_qr
```

### Jacobi Symbol

```runa
Note: Generalized Legendre symbol
Let jacobi_15_37 be NT.jacobi_symbol(15, 37)
Let jacobi_properties be NT.verify_jacobi_properties(15, 37)

Display "Jacobi symbol (15/37): " joined with jacobi_15_37
```

### Quadratic Equation Solutions

```runa
Note: Solve quadratic congruences
Let solutions be NT.solve_quadratic_congruence(1, 4, 5, 13)
Display "Solutions to x² + 4x + 5 ≡ 0 (mod 13):"
NT.display_congruence_solutions(solutions)

Note: Tonelli-Shanks algorithm for square roots
Let sqrt_mod be NT.tonelli_shanks(3, 7)
If NT.has_square_root(sqrt_mod):
    Display "√3 ≡ " joined with NT.get_square_root(sqrt_mod) joined with " (mod 7)"
```

## Diophantine Equations

### Linear Diophantine Equations

```runa
Note: Solve ax + by = c
Let linear_solution be NT.solve_linear_diophantine(14, 35, 21)

If NT.has_solution(linear_solution):
    Let particular_solution be NT.get_particular_solution(linear_solution)
    Let general_form be NT.get_general_solution_form(linear_solution)
    
    Display "Particular solution: " joined with NT.solution_to_string(particular_solution)
    Display "General form: " joined with NT.general_form_to_string(general_form)
```

### Pell's Equation

```runa
Note: Solve x² - Dy² = 1
Let pell_solutions be NT.solve_pell_equation(61, 10)
Let fundamental_solution be NT.get_fundamental_pell_solution(61)

Display "Fundamental solution to x² - 61y² = 1:"
NT.display_pell_solution(fundamental_solution)

Note: Generate continued solutions
Let continued_solutions be NT.generate_pell_solutions(61, 5)
NT.display_pell_solution_sequence(continued_solutions)
```

## Continued Fractions in Number Theory

### Convergents and Approximation

```runa
Import "math/precision/continued" as Continued

Note: Best rational approximations
Let cf_sqrt2 be NT.continued_fraction_sqrt(2)
Let convergents be Continued.get_convergents(cf_sqrt2, 10)

Display "Best rational approximations to √2:"
NT.display_rational_approximations(convergents)

Note: Solve Pell equation using continued fractions
Let pell_cf_solution be NT.pell_via_continued_fraction(13)
```

## Multiplicative Functions

### Common Multiplicative Functions

```runa
Note: Evaluate various multiplicative functions
Let sigma_n be NT.divisor_sum_function(60, 1)  Note: σ₁(n) = sum of divisors
Let sigma_0 be NT.divisor_sum_function(60, 0)  Note: σ₀(n) = number of divisors
Let mu_n be NT.mobius_function(60)

Display "σ(60) = " joined with sigma_n
Display "d(60) = " joined with sigma_0
Display "μ(60) = " joined with mu_n

Note: Jordan's totient function
Let jordan_totient be NT.jordan_totient_function(60, 2)
Display "J₂(60) = " joined with jordan_totient
```

### Dirichlet Convolution

```runa
Note: Convolution of multiplicative functions
Let convolution_result be NT.dirichlet_convolution(NT.mobius_function, NT.constant_function_1, 100)
Let identity_check be NT.verify_mobius_inversion(100)

Display "μ * 1 convolution result: " joined with convolution_result
```

## Analytic Number Theory

### Prime Counting Function

```runa
Note: Estimate prime distribution
Let pi_x be NT.prime_counting_function(1000)
Let li_estimate be NT.logarithmic_integral_estimate(1000)
Let prime_number_theorem_estimate be NT.pnt_estimate(1000)

Display "π(1000) = " joined with pi_x
Display "li(1000) ≈ " joined with li_estimate
Display "PNT estimate: " joined with prime_number_theorem_estimate
```

### Riemann Zeta Function

```runa
Note: Evaluate zeta function at integer points
Let zeta_2 be NT.riemann_zeta(2)
Let zeta_4 be NT.riemann_zeta(4)
Let zeta_approximation be NT.approximate_zeta_series(3, 1000)

Display "ζ(2) = π²/6 = " joined with zeta_2
Display "ζ(4) = π⁴/90 = " joined with zeta_4
Display "ζ(3) ≈ " joined with zeta_approximation
```

## Cryptographic Applications

### RSA-Related Functions

```runa
Note: Generate RSA parameters
Let rsa_primes be NT.generate_rsa_prime_pair(1024)
Let n be NT.multiply_rsa_primes(rsa_primes)
Let phi_n be NT.euler_totient_rsa(rsa_primes)

Note: Choose encryption exponent
Let e be NT.choose_rsa_exponent(phi_n)
Let d be NT.calculate_rsa_private_exponent(e, phi_n)

Display "RSA public key (e, n): (" joined with e joined with ", " joined with n joined with ")"
Display "RSA private key d: " joined with d
```

### Discrete Logarithm

```runa
Note: Baby-step giant-step algorithm
Let discrete_log be NT.baby_step_giant_step(5, 23, 11)  Note: Find x such that 5^x ≡ 23 (mod 11)
If NT.has_discrete_log(discrete_log):
    Display "5^x ≡ 23 (mod 11) where x = " joined with NT.get_discrete_log_value(discrete_log)

Note: Pohlig-Hellman for composite moduli
Let ph_result be NT.pohlig_hellman_discrete_log(3, 15, 17)
```

## Additive Number Theory

### Partition Functions

```runa
Note: Integer partitions
Let partition_count be NT.partition_function(50)
Let restricted_partitions be NT.partition_with_restrictions(20, 5)  Note: Max 5 parts

Display "Number of partitions of 50: " joined with partition_count
Display "Partitions of 20 into at most 5 parts: " joined with restricted_partitions

Note: Generate actual partitions
Let partitions_of_7 be NT.generate_partitions(7)
NT.display_integer_partitions(partitions_of_7)
```

### Sum of Squares

```runa
Note: Express as sum of squares
Let two_squares be NT.sum_of_two_squares(325)
Let four_squares be NT.sum_of_four_squares(325)  Note: Jacobi four-square theorem

If NT.has_two_square_representation(two_squares):
    Display "325 as sum of two squares: " joined with NT.two_squares_to_string(two_squares)

Display "325 as sum of four squares: " joined with NT.four_squares_to_string(four_squares)
```

### Goldbach Conjecture

```runa
Note: Verify Goldbach conjecture for even numbers
Let goldbach_representation be NT.goldbach_representation(100)
Let weak_goldbach be NT.weak_goldbach_representation(27)  Note: Odd number as sum of three primes

Display "100 as sum of two primes: " joined with NT.goldbach_to_string(goldbach_representation)
Display "27 as sum of three primes: " joined with NT.weak_goldbach_to_string(weak_goldbach)
```

## Advanced Topics

### Elliptic Curves over Finite Fields

```runa
Note: Basic elliptic curve operations
Let curve be NT.create_elliptic_curve(1, 1, 23)  Note: y² = x³ + x + 1 over F₂₃
Let point_count be NT.count_elliptic_curve_points(curve)
Let points be NT.generate_elliptic_curve_points(curve)

Display "Number of points on curve: " joined with point_count
NT.display_elliptic_curve_points(points)
```

### Quadratic Forms

```runa
Note: Binary quadratic forms
Let qf be NT.create_quadratic_form(1, 0, 1)  Note: x² + y²
Let representations be NT.count_representations(qf, 25)
Let proper_representations be NT.proper_representations(qf, 25)

Display "Number of representations of 25 by x² + y²: " joined with representations
NT.display_quadratic_form_representations(proper_representations)
```

### Class Numbers

```runa
Note: Calculate class numbers
Let class_number be NT.class_number_quadratic_field(-23)
Let class_group be NT.class_group_structure(-23)

Display "Class number of Q(√-23): " joined with class_number
NT.display_class_group_structure(class_group)
```

## Algorithmic Efficiency

### Performance Optimization

```runa
Note: Choose optimal algorithms based on input size
Let factorization_method be NT.optimal_factorization_algorithm(large_number)
Let primality_method be NT.optimal_primality_test(large_number)

Note: Precompute for repeated operations
Let sieve_cache be NT.create_prime_sieve_cache(1000000)
Let factorization_cache be NT.create_factorization_cache(10000)

Note: Use cache for faster operations
Let cached_prime_check be NT.is_prime_cached(997, sieve_cache)
Let cached_factors be NT.factorize_cached(60, factorization_cache)
```

### Memory Management

```runa
Note: Handle large integer computations
Let memory_efficient_gcd be NT.gcd_memory_efficient(very_large_a, very_large_b)
Let streaming_sieve be NT.segmented_sieve(1000000, 2000000)

Note: Monitor computational resources
Let computation_stats be NT.get_computation_statistics()
Display "Prime operations performed: " joined with NT.get_prime_operation_count(computation_stats)
```

## Error Handling and Validation

```runa
Import "core/error_handling" as ErrorHandling

Note: Validate inputs and handle errors
Let gcd_result be NT.gcd_safe(0, 15)
If ErrorHandling.is_error(gcd_result):
    Display "Error in GCD calculation: " joined with ErrorHandling.error_message(gcd_result)
Otherwise:
    Display "GCD result: " joined with ErrorHandling.get_value(gcd_result)

Note: Handle overflow in modular arithmetic
Let safe_mod_power be NT.modular_exponentiation_safe(base, exponent, modulus)
If ErrorHandling.is_overflow_error(safe_mod_power):
    Display "Overflow in modular exponentiation"
```

## Integration Examples

### With Cryptography

```runa
Import "crypto/rsa" as RSA
Import "crypto/discrete_log" as DiscreteLog

Note: Use number theory for cryptographic protocols
Let rsa_keys be RSA.generate_keys_with_nt_primes(2048)
Let dh_parameters be DiscreteLog.generate_safe_prime_group(1024)
```

### With Computational Algebra

```runa
Import "math/algebra/rings" as Rings

Note: Work with rings Z/nZ
Let ring_z15 be Rings.create_quotient_ring_integers(15)
Let element_7 be Rings.create_element(ring_z15, 7)
Let inverse_7 be NT.modular_inverse_in_ring(element_7)
```

## Best Practices

### Choosing Algorithms
- Use trial division for small numbers (< 10⁶)
- Use Miller-Rabin for large primality testing
- Use ECM or QS for factoring large composites
- Precompute sieves for batch prime operations

### Numerical Stability
- Use modular arithmetic to prevent overflow
- Validate input ranges for algorithms
- Handle edge cases (0, 1, negative numbers)
- Use appropriate precision for floating-point estimates

### Security Considerations
- Use cryptographically secure random number generation
- Implement constant-time algorithms for cryptographic applications
- Validate all inputs in security-critical contexts
- Use proven algorithms from established literature

This module provides comprehensive tools for both theoretical and practical applications in number theory, supporting research, education, and real-world computational needs.